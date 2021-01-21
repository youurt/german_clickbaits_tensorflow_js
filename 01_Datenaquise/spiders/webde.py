import scrapy
from scrapy.http.request import Request
from datetime import datetime
from klickscraper.items import WebdeItem


class WebdeSpider(scrapy.Spider):
    name = 'webde'
    scraped_at = datetime.now()

    def start_requests(self):
        for i in range(287):
            yield Request(
                url=f"https://web.de/magazine/unterhaltung/stars/p{i}",
                dont_filter=True,
                callback=self.parse_url)

    def parse_url(self, response):
        follow_ulrs = response.css(
            ".teaser-article__full").css("a::attr(href)").getall()
        for f in follow_ulrs:
            yield Request(
                url=f,
                dont_filter=True,
                callback=self.parse_page)

    def parse_page(self, response):
        print()
        if len(response.css("p::text").getall()) > 10:
            text = " ".join(response.css("p::text").getall())
        else:
            text = None
        yield WebdeItem(title=response.css('title::text').get(),
                        text=text,
                        scraped_at=self.scraped_at)
