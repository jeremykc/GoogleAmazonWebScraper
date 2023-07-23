from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class GoogleSearchResultItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    # Remove the Google tracking parameters from link
    link_in = MapCompose(lambda x: 'http' + x.split('http')[1].split('&')[0])
