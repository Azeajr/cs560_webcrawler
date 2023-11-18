from scrapy.crawler import CrawlerProcess
from zillow_crawler.spiders.books_toscrape import BooksToscrapeSpider
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess(
        settings=get_project_settings(),
    )
    process.crawl(BooksToscrapeSpider)
    process.start()


if __name__ == "__main__":
    main()
