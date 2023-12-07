"""
This module contains the Scrapy settings for the Zillow crawler.

Attributes:

    BOT_NAME (str): The name of the bot.
    SPIDER_MODULES (list[str]): The list of modules where the spiders are
        located.
    NEWSPIDER_MODULE (str): The name of the module where the new spiders are
        located.
    USER_AGENT (str): The user agent to use for the bot.
    ROBOTSTXT_OBEY (bool): Whether to obey the robots.txt file.
    CONCURRENT_REQUEST (int): The maximum number of concurrent requests to
        perform.
    DOWNLOAD_DELAY (int): The amount of time in seconds to wait before
        performing a request.
    CONCURRENT_REQUESTS_PER_DOMAIN (int): The maximum number of concurrent
        requests to perform for a single domain.
    DEFAULT_REQUEST_HEADERS (dict[str, str]): The default request headers.
        Control the encoding of the request.
    ITEM_PIPELINES (dict[str, int]): The item pipelines to use.
    AUTOTHROTTLE_ENABLED (bool): Whether to enable the AutoThrottle extension.
    AUTOTHROTTLE_START_DELAY (int): The initial download delay to use for
        AutoThrottle.
    AUTOTHROTTLE_MAX_DELAY (int): The maximum download delay to use for
        AutoThrottle.
    AUTOTHROTTLE_TARGET_CONCURRENCY (float): The average number of requests
        Scrapy should be sending in parallel to each remote server.
    AUTOTHROTTLE_DEBUG (bool): Whether to enable showing throttling stats for
        every response received.
    CLOSESPIDER_PAGECOUNT (int): The maximum number of pages to crawl.
    REQUEST_FINGERPRINTER_IMPLEMENTATION (str): The request fingerprinter
        implementation to use.  This controls the algorithm used to generate
        the request fingerprint.
    TWISTED_REACTOR (str): The Twisted reactor to use. This controls the
        networking engine to use for HTTP requests.
    FEED_EXPORT_ENCODING (str): The encoding to use for exporting the feed.
    LOG_ENABLED (bool): Whether to enable scrapy's default logging.
    CLOSESPIDER_PAGECOUNT (int): The maximum number of pages to crawl.
"""
# Scrapy settings for zillow_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "zillow_crawler"

SPIDER_MODULES = ["zillow_crawler.spiders"]
NEWSPIDER_MODULE = "zillow_crawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "zillow_crawler (+http://www.yourdomain.com)"
# First user agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
# User agent for Linux
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
# USER_AGENT = None
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32
CONCURRENT_REQUEST = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 30
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # This is the default value
    "Accept-Language": "en",  # This is the default value
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "UTF-8",  # This is the default value
    "Referer": "https://www.google.com/",
    "DNT": "1",  # Do Not Track Request Header
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "zillow_crawler.middlewares.ZillowCrawlerSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "zillow_crawler.middlewares.ZillowCrawlerDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "zillow_crawler.pipelines.ZillowListingPipeline": 300,
    "zillow_crawler.pipelines.ZillowPagePipeline": 400,
}
# ITEM_PIPELINES = {
#     "zillow_crawler.pipelines.BooksToscrapePipeline": 300,
# }
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Configure logging
LOG_ENABLED = False
# Set the maximum number of pages to crawl
# This is more of an exponential limit than a hard limit

CLOSESPIDER_PAGECOUNT = 1  # 2
# CLOSESPIDER_PAGECOUNT = 3 # 8
# CLOSESPIDER_PAGECOUNT = 4  # 16
# CLOSESPIDER_PAGECOUNT = 5  # 32
# CLOSESPIDER_PAGECOUNT = 100


# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }

