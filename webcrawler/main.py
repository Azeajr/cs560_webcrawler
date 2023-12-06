"""Main module for the zillow_crawler project."""

from multiprocessing import Manager, Process, Value
from time import sleep
import datetime

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

from webcrawler.zillow_crawler.models import ZillowListing, ZillowPage, engine
from webcrawler.zillow_crawler.spiders.zillow_houses import ZillowHousesSpider


# The arguments for the start_crawler_task function are used to communicate
# from the start_crawler_task process to the main process. These are special
# multiprocessing objects that can be shared between processes.
def start_crawler_task(
    completed: Value = Value("b", False),
    crawler_stats: dict = None,
):
    """
    Start the crawler. This function is run in a separate process.

    Args:
        completed (Value, optional): Value object to indicate if the crawler
            has completed. Defaults to Value("b", False).
        crawler_stats (dict, optional): Dictionary to store the crawler stats.
            Defaults to None.
    """
    process = CrawlerProcess(settings=get_project_settings())
    crawler = process.create_crawler(ZillowHousesSpider)
    process.crawl(crawler)
    process.start()

    # get crawler stats
    crawler_stats.update(crawler.stats.get_stats())

    sleep(5)
    # indicate that the crawler has completed
    completed.value = True


def main():
    """Main function for the zillow_crawler project."""
    # create a console object to render the UI
    console = Console()

    # create a multiprocessing manager to share objects between processes
    with Manager() as manager:
        # boolean value to indicate if the crawler has completed
        crawler_completed = manager.Value("b", False)
        # dictionary to store the crawler stats
        crawler_stats = manager.dict()

        # start the crawler in a separate process
        crawler_process = Process(
            # function to run in the process
            target=start_crawler_task,
            # arguments to pass to the function
            args=(crawler_completed, crawler_stats),
        )
        crawler_process.start()

        # create the main layout
        # This layout is used to render the UI make it easier to structure
        # the UI. The layout is rendered in a separate process using the
        # rich.live.Live object.
        main_layout = Layout(name="root")
        main_layout.split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1),
        )

        # create a SQLAlchemy session to query the database
        session = sessionmaker(bind=engine)()

        # render the UI
        with Live(console=console, refresh_per_second=1) as live:
            # loop until the crawler has completed
            while not crawler_completed.value:
                # query the database for the listings and pages
                listings = session.query(ZillowListing).all()
                pages = session.query(ZillowPage).all()

                # create a progress bar to show the average house prices
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

                # query the database for the average house prices by city
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

                # get the cities and prices from the query results
                cities = [city for city, *_ in results]
                prices = [price for *_, price in results]

                # get the max price to set the progress bar total
                max_price = max(prices, default=100)

                # add the cities and prices to the progress bar
                for city, price in zip(cities, prices):
                    progress.add_task(
                        f"[green]{city}", completed=price, total=max_price
                    )

                # renderables contain the listings to show in the left panel
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

                # add the renderables to the left panel
                left_panel = Panel(
                    Columns(renderables, equal=True, expand=True),
                    title="Houses Located",
                    border_style="green",
                )

                # add the progress bar to the right panel
                # Even though this uses Progress bar class, it is not a
                # progress bar. I am using the Progress bar to show the average
                # house prices by city as a bar chart.
                right_panel = Panel(
                    progress,
                    title="CT Average House Prices by City",
                    border_style="green",
                )
                main_layout["left"].update(left_panel)
                main_layout["right"].update(right_panel)
                live.update(main_layout)

        # wait for the crawler process to finish
        crawler_process.join()
        # close the SQLAlchemy session
        session.close()

        # Use the final listings and pages lists to show the total number of
        # listings and pages scraped.
        console.print(f"Total houses scraped: {len(listings)}")
        console.print(f"Total pages scraped: {len(pages)}")

        # convert the crawler_stats dictionary to a regular dictionary
        crawler_stats = dict(crawler_stats)

        # console.print(f"Crawler stats: {crawler_stats}")
        # print the total crawl time
        # Uses implied string concatenation to format the timedelta object
        console.print(
            "Total crawl time:"
            f" {datetime.timedelta(seconds=crawler_stats['elapsed_time_seconds'])}"
        )

        # print the finish reason
        console.print(f"Finish reason: {crawler_stats['finish_reason']}")


if __name__ == "__main__":
    main()
