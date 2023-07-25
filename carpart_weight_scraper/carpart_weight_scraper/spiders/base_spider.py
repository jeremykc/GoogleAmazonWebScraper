import os
from urllib.parse import urlencode
from scrapy import Spider

class BaseSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.SCRAPEOPS_API_KEY = self.get_scrapeops_api_key()

    def get_scrapeops_api_key(self):
        """ Return the ScrapeOps API Key """
        if 'SCRAPEOPS_API_KEY' in os.environ:
            return os.environ.get('SCRAPEOPS_API_KEY')
        else:
            raise ValueError('SCRAPEOPS_API_KEY environment variable not set')

    def get_proxy_url(self, url):
        """ Create a ScrapeOps Proxy URL from a given URL """
        payload = {'api_key': self.SCRAPEOPS_API_KEY, 'url': url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
        return proxy_url
