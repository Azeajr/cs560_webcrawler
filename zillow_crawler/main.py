from pathlib import Path

from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.statscollectors import StatsCollector
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker

from zillow_crawler.models import ZillowListing, ZillowPage, engine
from zillow_crawler.spiders.zillow_houses import ZillowHousesSpider

import plotext as plt

collected_stats = None


def main():
    console = Console()
    process = CrawlerProcess(
        settings=get_project_settings(),
    )
    clawler = process.create_crawler(ZillowHousesSpider)
    process.crawl(clawler)
    process.start()

    stats = clawler.stats.get_stats()
    console.print(stats)

    with Live(console=console, refresh_per_second=4) as live:
        cons = console
        session = sessionmaker(bind=engine)()
        listings = session.query(ZillowListing).all()
        pages = session.query(ZillowPage).all()

        for listing in listings:
            cons.print(listing.address)

        average_price = (
            session.query(ZillowListing).with_entities(ZillowListing.price).all()
        )
        average_price = sum([price[0] for price in average_price]) / len(average_price)
        cons.print(f"Average price: {average_price}")

        results = (
            session.query(ZillowListing.city, ZillowListing.state, ZillowListing.price)
            .where(ZillowListing.state == "CT")
            .all()
        )

        cities = [city for city, *_ in results]
        prices = [price for *_, price in results]

        plt.bar(cities, prices, width=1)
        plt.show()

        # renderables = [
        #     Panel(
        #         f"[bold italic]{book.book_name}[/bold italic]\n[green]{book.product_price}[/green]",
        #         border_style="yellow",
        #     )
        #     for book in books
        # ]
        # live.update(Panel(Columns(renderables, equal=True), title="Books"))
        session.close()

        # table = Table(title="Books")
        # table.add_column("Book Name")
        # table.add_column("Product Price")
        # for book in books:
        #     table.add_row(book.book_name, book.product_price)

        # live.update(Panel.fit(table, title="Books"))


if __name__ == "__main__":
    main()
