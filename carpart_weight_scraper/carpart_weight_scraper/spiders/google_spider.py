""" Scrape Google SERP for the top Amazon link for each car part in a given list of IDs. """
import scrapy
import os
import pandas as pd
from urllib.parse import urlencode
from carpart_weight_scraper.items import GoogleSearchResultItem
from carpart_weight_scraper.itemloaders import GoogleSearchResultItemLoader


# ------------------------------------------------------- #
#                     Global Variables                    #
# ------------------------------------------------------- #
if 'SCRAPEOPS_API_KEY' in os.environ:
    SCRAPEOPS_API_KEY = os.environ.get('SCRAPEOPS_API_KEY')
else:
    raise ValueError('SCRAPEOPS_API_KEY environment variable not set')


# ------------------------------------------------------- #
#                     Helper Functions                    #
# ------------------------------------------------------- #
def fetch_partslink_numbers():
    """ Fetch list of partslink numbers from a CSV file """
    partslink_numbers_file_path = 'data/in/partslink_numbers.csv' 
    if not os.path.exists(partslink_numbers_file_path):
        raise FileNotFoundError(partslink_numbers_file_path, ': file not found')
    return pd.read_csv(partslink_numbers_file_path, header=None).iloc[:,0]


def create_google_url(query):
    """ Create a Google search URL from a query """
    google_dict = {'q': query, 'num': 10, }
    return 'https://www.google.com/search?' + urlencode(google_dict)


def get_proxy_url(url):
    """ Create a ScrapeOps Proxy URL from a given URL """
    payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


# ------------------------------------------------------- #
#                      Scrapy Spider                      #
# ------------------------------------------------------- #
class GoogleSpider(scrapy.Spider):
    name = "google_spider"
    allowed_domains = ['proxy.scrapeops.io', 'google.com']
    custom_settings = {
        # Specify export options
        'FEEDS': {'data/out/%(name)s_%(time)s.csv': {'format': 'csv', 'overwrite': True}},
        'FEED_EXPORT_FIELDS': ['partslink_number', 'link'],
    }
    

    def start_requests(self):
        # List of partslink numbers to search for on Google 
        partslink_numbers = fetch_partslink_numbers()

        idx=0; limit=3
        for partslink_number in partslink_numbers:
            if idx >= limit: 
                break; 
            idx += 1

            # Append the partslink number to the query base
            query = 'site:amazon.com Partslink Number ' + partslink_number
            
            # Create a Google search URL from a query and an optional site
            google_url = create_google_url(query)
            # TODO: use static, already encoded URL, to avoid encoding issues

            # Create a ScrapeOps Proxy URL from a Google search URL
            google_url = get_proxy_url(google_url)
            
            yield scrapy.Request(url=google_url, callback=self.parse, meta={'partslink_number': partslink_number})


    def parse(self, response):
        # Extract first URL in SERP response, when JavaScript is enabled
        link = response.xpath('(//h3/parent::a)/@href').get()

        # Extract first URL in SERP response, when JavaScript is disabled
        if not link:            
            link = response.xpath('(//h3/parent::div/parent::div/parent::a)/@href').get()
            print('\nNOTE: No link found... Trying JS Disabled XPath selector for', response.meta['partslink_number'])
        
        item_loader = GoogleSearchResultItemLoader(item=GoogleSearchResultItem(), response=response)
        item_loader.add_value('partslink_number', response.meta['partslink_number'])
        item_loader.add_value('link', link)

        print(item_loader.load_item())
        yield item_loader.load_item()
