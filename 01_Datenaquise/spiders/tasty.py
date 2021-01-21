import scrapy
from datetime import datetime
import json
from scrapy import Request, Selector
from klickscraper.items import TastyQuizItem


class TastySpider(scrapy.Spider):
    name = 'tasty'
    allowed_domains = ['www.buzzfeed.de']
    start_urls = ['http://www.buzzfeed.de/']
    scraped_at = datetime.now()

    def start_requests(self):
        for page in range(5):
            yield Request(
                url=f"https://www.buzzfeed.com/de/feedpage/feed/search_buzzes?page={page}&page_name=tag&response_format=json&page_size=100&keywords__in=einfach%20tasty,--primarykeyword-einfach%20tasty",
                dont_filter=True,
                callback=self.parse_main)

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
        yield TastyQuizItem(
            text=" ".join(cleaned_body),
            scraped_at=self.scraped_at,
            url=response.url,
            title=response.css('title::text').get())
