import scrapy
from scrapy import Request, Selector
import json
from klickscraper.items import BuzzfeedItem
from datetime import datetime


class BuzzfeedSpider(scrapy.Spider):
    name = 'buzzfeed'
    allowed_domains = ['buzzfeed.de']
    start_urls = ['http://buzzfeed.de/']
    scraped_at = datetime.now()

    def start_requests(self):
        for page in range(5):
            yield Request(
                url=f'https://www.buzzfeed.com/de/feedpage/feed/home?page={page}&page_name=home&response_format=json',
                dont_filter=True,
                callback=self.parse_main,)

    def parse_main(self, response):
        results = json.loads(response.body)['content']
        atag = Selector(text=results).css("a::attr(href)").getall()
        for a in atag:
            if "https" in a:
                yield Request(
                    url=a,
                    dont_filter=True,
                    callback=self.parse_page)

    def parse_page(self, response):
        cleaned_body = []
        for i in response.css("p::text").getall():
            if not "BuzzFeed" in i:
                cleaned_body.append(i)
        print()
        yield BuzzfeedItem(
            text=" ".join(cleaned_body),
            scraped_at=self.scraped_at,
            url=response.url,
            title=response.css('title::text').get())
