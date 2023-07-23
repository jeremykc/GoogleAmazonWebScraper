import os

BOT_NAME = "carpart_weight_scraper"

SPIDER_MODULES = ["carpart_weight_scraper.spiders"]
NEWSPIDER_MODULE = "carpart_weight_scraper.spiders"

EXTENSIONS = {
    # ScrapeOps Monitor
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,                     # Activate The ScrapeOps Monitor Extension
}

DOWNLOADER_MIDDLEWARES = {
    # ScrapeOps Proxy
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,   # Activate The ScrapeOps Proxy SDK Middleware

    # ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,               # Activate The ScrapeOps Monitor Retry Middleware
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,             # Disable The Default Retry Middleware

    # Scrapy Rotating User Agents
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,        # Activate The Scrapy Rotating User Agents Middleware
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,     # Disable The Default User Agent Middleware
}


# ------------------------------------------------------- #
#                    ScrapeOps Settings                   #
# ------------------------------------------------------- #
SCRAPEOPS_API_KEY = os.environ.get('SCRAPEOPS_API_KEY')

# Enable The ScrapeOps Proxy Aggregator
SCRAPEOPS_PROXY_ENABLED = True

# Maximum concurrent requests for ScrapeOps Proxy (Free Limit)
CONCURRENT_REQUESTS = 1


# ------------------------------------------------------- #
#                     Scrapy Settings                     #
# ------------------------------------------------------- #
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "carpart_weight_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "carpart_weight_scraper.middlewares.GoogleCarpartScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "carpart_weight_scraper.middlewares.GoogleCarpartScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "carpart_weight_scraper.pipelines.GoogleCarpartScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True    # Can change order of scraped results in CSV file
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"