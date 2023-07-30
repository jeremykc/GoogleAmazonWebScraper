""" Scrape Amazon for the weight of each car part in a given list of Amazon product links. """
import scrapy
import os
import pandas as pd
from urllib.parse import urlencode
from .base_spider import BaseSpider
from ..items import AmazonProductItem
from ..itemloaders import AmazonProductItemLoader


class AmazonSpider(BaseSpider):
    name = 'amazon_spider'
    allowed_domains = ['proxy.scrapeops.io', 'amazon.com']
    custom_settings = {
        # Specify export options
        'FEED_EXPORT_FIELDS': {
            'partslink_number': 'partslink_number', 
            'weight': 'weight (pounds)', 
            'link':'link'
        },

        # Specify pipeline to use
        'ITEM_PIPELINES': {'carpart_weight_scraper.pipelines.WeightConversionPipeline': 300},          
    }


    def __init__(self, start=0, end=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = int(start)
        self.end = int(end)


    def start_requests(self):
        # List of dictionaries with amazon links to scrape
        amazon_links_data = self.fetch_amazon_links(self.start, self.end)
        print(f'\namazon_links_data:\n{amazon_links_data[:100]}\n')

        for record in amazon_links_data:
            # Check if record is valid
            if not isinstance(record,dict) or 'link' not in record or not isinstance(record['link'], str):
                print('Invalid entry:', record, type(record), '\n')
                continue
            
            # Create request
            yield scrapy.Request(
                url=self.get_proxy_url(record['link']),
                callback=self.parse,
                meta={'partslink_number': record['partslink_number'], 'link': record['link']},
            )


    def parse(self, response):
        # Extract weight from page
        weight = response.xpath('//th[normalize-space(text())="Item Weight"]/following-sibling::td/text()').extract_first()
        if not weight:
            print('Weight not found for', response.meta['partslink_number'], 'at:', response.meta['link'])

        item_loader = AmazonProductItemLoader(item=AmazonProductItem(), response=response)
        item_loader.add_value('partslink_number', response.meta['partslink_number'])
        item_loader.add_value('link', response.meta['link'])
        item_loader.add_value('weight', weight)

        print(item_loader.load_item(), '\n')
        yield item_loader.load_item()


    # ------------------------------------------------------- #
    #                     Helper Functions                    #
    # ------------------------------------------------------- #
    def fetch_amazon_links(self, start, end):
        """ Fetch a list of dictionaries with amazon links from a CSV file, and return a slice of the list """
        amazon_links_file_path = 'data/in/amazon_links.csv'
        if not os.path.exists(amazon_links_file_path):
            raise FileNotFoundError(amazon_links_file_path, ': file not found')
        return pd.read_csv(amazon_links_file_path)[start:end].to_dict('records')
