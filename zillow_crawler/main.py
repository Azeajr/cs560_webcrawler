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
import time

collected_stats = None


def main():
    console = Console()
    process = CrawlerProcess(
        settings=get_project_settings(),
    )
    clawler = process.create_crawler(ZillowHousesSpider)
    start_timer = time.time()   #used to time crawling time
    total_houses = 0            #total houses scraped
    total_pages = 0             #total pages scraped

    process.crawl(clawler)
    process.start()
    total_crawl_time = time.time() - start_timer

    stats = clawler.stats.get_stats()
    console.print(stats)

    with Live(console=console, refresh_per_second=4) as live:
        cons = console
        session = sessionmaker(bind=engine)()
        listings = session.query(ZillowListing).all()
        pages = session.query(ZillowPage).all()

        for listing in listings:
            cons.print(listing.address)
        
        
        total_pages = len(pages)

        total_houses = len(listings)    #total number of houses scraped

        results = (
            session.query(ZillowListing.city, ZillowListing.state, ZillowListing.price)
            .where(ZillowListing.state == "CT")
            .all()
        )

        cities = [city for city, *_ in results]
        prices = [price for *_, price in results]

        plt.bar(cities, prices, width=1)
        plt.show()

        renderables = [
            Panel(
                f"[bold]{listing.address}[/bold]\n\nPrice: [green]${listing.price:0.2f}[/green]"
                f"\nSqft: {listing.sqft}\nBedrooms: {listing.bedrooms}\nBathrooms: {listing.bathrooms}",
                border_style="yellow",
            )
            for listing in listings            
        ]
        live.update(Panel.fit(Columns(renderables, equal=True), title = "Houses Located"))

        cons.print(f"\nTotal crawl time: {time.strftime('%H:%M:%S', time.gmtime(total_crawl_time))}")        
        cons.print(f"Total houses escraped: {total_houses}")
        cons.print(f"Total pages scraped: {total_pages}")
        
        session.close()


if __name__ == "__main__":
    main()
