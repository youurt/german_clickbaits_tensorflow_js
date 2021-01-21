import scrapy


class WikinewsItem(scrapy.Item):
    page_id = scrapy.Field()
    title = scrapy.Field()
    scraped_at = scrapy.Field()
    category = scrapy.Field()
    extract = scrapy.Field()


class BuzzfeedItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class HeftigItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    headline = scrapy.Field()
    page_id = scrapy.Field()


class TvMovieItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class FrauenseiteItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class BuzzfeedQuizItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class TastyQuizItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class BravoItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class PromipoolItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    title = scrapy.Field()


class WebdeItem(scrapy.Item):
    text = scrapy.Field()
    scraped_at = scrapy.Field()
    title = scrapy.Field()
