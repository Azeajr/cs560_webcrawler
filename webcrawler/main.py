"""Main module for the zillow_crawler project."""

import time
from multiprocessing import Manager, Process, Value
from time import sleep

from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from zillow_crawler.models import ZillowListing, ZillowPage, engine
from zillow_crawler.spiders.zillow_houses import ZillowHousesSpider


def start_crawler_task(
    completed: Value = Value("b", False),
    total_crawl_time: Value = Value("f", 0.0),
    crawler_stats: dict = None,
):
    """Start the crawler."""
    start_timer = time.time()  # used to time crawling time
    process = CrawlerProcess(settings=get_project_settings())
    crawler = process.create_crawler(ZillowHousesSpider)
    process.crawl(crawler)
    process.start()

    total_crawl_time.value = time.time() - start_timer
    crawler_stats.update(crawler.stats.get_stats())

    sleep(5)

    completed.value = True


def main():
    """Main function for the zillow_crawler project."""
    console = Console()

    with Manager() as manager:
        crawler_completed = manager.Value("b", False)
        total_crawl_time = manager.Value("f", 0.0)
        crawler_stats = manager.dict()
        crawler_process = Process(
            target=start_crawler_task,
            args=(crawler_completed, total_crawl_time, crawler_stats),
        )
        crawler_process.start()
        main_layout = Layout(name="root")
        main_layout.split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1),
        )

        session = sessionmaker(bind=engine)()

        with Live(console=console, refresh_per_second=1) as live:
            while not crawler_completed.value:
                listings = session.query(ZillowListing).all()
                pages = session.query(ZillowPage).all()

                progress = Progress(
                    TextColumn("[bold blue]{task.description}"),
                    BarColumn(
                        bar_width=None,
                    ),
                    "[progress.completed]${task.completed:_.2f}",
                    console=console,
                    transient=True,
                    expand=True,
                )

                results = (
                    session.query(
                        ZillowListing.city,
                        func.avg(ZillowListing.price).label("average_price"),
                    )
                    .filter(ZillowListing.state == "CT")
                    .group_by(ZillowListing.city)
                    .order_by(ZillowListing.city)
                    .all()
                )

                cities = [city for city, *_ in results]
                prices = [price for *_, price in results]

                max_price = max(prices, default=100)

                for city, price in zip(cities, prices):
                    progress.add_task(
                        f"[green]{city}", completed=price, total=max_price
                    )

                renderables = [
                    Panel(
                        f"[bold]{listing.address}[/bold]"
                        f"\n\nPrice: [green]${listing.price:_.2f}[/green]"
                        f"\nSqft: {listing.sqft}"
                        f"\nBedrooms: {listing.bedrooms}"
                        f"\nBathrooms: {listing.bathrooms}",
                        border_style="yellow",
                    )
                    for listing in listings
                ]
                left_panel = Panel(
                    Columns(renderables, equal=True, expand=True),
                    title="Houses Located",
                    border_style="green",
                )

                right_panel = Panel(
                    progress,
                    title="CT Average House Prices by City",
                    border_style="green",
                )
                main_layout["left"].update(left_panel)
                main_layout["right"].update(right_panel)
                live.update(main_layout)

        crawler_process.join()
        session.close()

        console.print(f"Total houses scraped: {len(listings)}")
        console.print(f"Total pages scraped: {len(pages)}")

        crawler_stats = dict(crawler_stats)

        # console.print(f"Crawler stats: {crawler_stats}")
        console.print(f"Total crawl time: {crawler_stats['elapsed_time_seconds']}")
        console.print(f"Finish reason: {crawler_stats['finish_reason']}")


if __name__ == "__main__":
    main()
