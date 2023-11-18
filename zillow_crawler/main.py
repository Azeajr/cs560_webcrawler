from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker

from zillow_crawler.models import Book, engine
from zillow_crawler.spiders.books_toscrape import BooksToscrapeSpider


def main():
    console = Console()
    process = CrawlerProcess(
        settings=get_project_settings(),
    )
    process.crawl(BooksToscrapeSpider)
    process.start()

    with Live(console=console, refresh_per_second=4) as live:
        cons = console
        session = sessionmaker(bind=engine)()
        books = session.query(Book).all()

        renderables = [
            Panel(
                f"[bold italic]{book.book_name}[/bold italic]\n[green]{book.product_price}[/green]",
                border_style="yellow",
            )
            for book in books
        ]
        live.update(Panel(Columns(renderables, equal=True), title="Books"))
        session.close()

        # table = Table(title="Books")
        # table.add_column("Book Name")
        # table.add_column("Product Price")
        # for book in books:
        #     table.add_row(book.book_name, book.product_price)

        # live.update(Panel.fit(table, title="Books"))


if __name__ == "__main__":
    main()
