import scrapy


class GoogleSearchResultItem(scrapy.Item):
    partslink_number = scrapy.Field()
    link = scrapy.Field()
    pass

class AmazonProductItem(scrapy.Item):
    partslink_number = scrapy.Field()
    link = scrapy.Field()
    weight = scrapy.Field()
    pass
