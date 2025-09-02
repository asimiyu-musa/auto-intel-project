import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()

class CarReviewItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    source = scrapy.Field()
    verdict = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
