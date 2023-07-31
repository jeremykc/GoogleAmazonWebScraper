""" Scrape Google SERP for the top Amazon link for each car part in a given list of IDs. """
import scrapy
import os
import pandas as pd
from urllib.parse import urlencode
from .base_spider import BaseSpider
from ..items import GoogleSearchResultItem
from ..itemloaders import GoogleSearchResultItemLoader


class GoogleSpider(BaseSpider):
    name = "google_spider"
    allowed_domains = ['proxy.scrapeops.io', 'google.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['partslink_number', 'link'],
    }
    

    def __init__(self, start=0, end=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = int(start)
        self.end = int(end)


    def start_requests(self):
        # List of partslink numbers to search for on Google 
        partslink_numbers = self.fetch_partslink_numbers(self.start, self.end)
        print(f'\npartslink_numbers:\n{partslink_numbers[:100]}\n')
        
        for partslink_number in partslink_numbers:
            # Append the partslink number to base query
            query = 'site:amazon.com Partslink Number ' + partslink_number
            
            yield scrapy.Request(
                url=self.get_proxy_url(self.create_google_url(query)), 
                callback=self.parse,
                meta={'partslink_number': partslink_number}
            )


    def parse(self, response):
        # Extract first URL in SERP response, when JavaScript is enabled
        link = response.xpath('(//h3/parent::a)/@href').get()

        # Extract first URL in SERP response, when JavaScript is disabled
        if not link:            
            link = response.xpath('(//h3/parent::div/parent::div/parent::a)/@href').get()
            print(f'NOTE: Link not found for {response.meta["partslink_number"]}. Trying again with JS Disabled XPath selector...')
        
        # Check if link is valid
        if not link:
            print(f'NOTE: Link not found for {response.meta["partslink_number"]}.')

        item_loader = GoogleSearchResultItemLoader(item=GoogleSearchResultItem(), response=response)
        item_loader.add_value('partslink_number', response.meta['partslink_number'])
        item_loader.add_value('link', link)

        print(item_loader.load_item(), '\n')
        yield item_loader.load_item()


    # ------------------------------------------------------- #
    #                     Helper Functions                    #
    # ------------------------------------------------------- #
    def fetch_partslink_numbers(self, start, end):
        """ Fetch list of partslink numbers from a CSV file, and return a slice of the list """
        partslink_numbers_file_path = 'data/in/partslink_numbers.csv' 
        if not os.path.exists(partslink_numbers_file_path):
            raise FileNotFoundError(f'Input file not found: {partslink_numbers_file_path}')
        return pd.read_csv(partslink_numbers_file_path, header=None).iloc[start:end,0]

    def create_google_url(self, query):
        """ Create a Google search URL from a query """
        google_dict = {'q': query, 'num': 10, }
        return 'https://www.google.com/search?' + urlencode(google_dict)
