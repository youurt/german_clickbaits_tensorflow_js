from datetime import datetime
import scrapy
from scrapy.http.request import Request
from klickscraper.items import FrauenseiteItem


class FrauenseiteSpider(scrapy.Spider):
    name = 'frauenseite'
    allowed_domains = ['www.frauenseite.net']
    scraped_at = datetime.now()

    def start_requests(self):
        yield Request(
            url=f"https://www.frauenseite.net/t/familie",
            callback=self.parse_first_page,
            dont_filter=True)

    def parse_first_page(self, response):

        results = response.css(".more").css("a::attr(href)").getall()
        for page in results:
            yield Request(
                url=page,
                dont_filter=True,
                callback=self.parse_first_content)

        next_item = response.css(
            '[id="load-more-articles"]').css("a::attr(href)").get()

        if next_item:
            yield Request(
                url=f"https://www.frauenseite.net/t/familie{next_item}",
                dont_filter=True,
                callback=self.parse_first_page)
        else:
            return

    def parse_first_content(self, response):
        yield FrauenseiteItem(
            text=" ".join(response.css("p::text").getall()),
            scraped_at=self.scraped_at,
            url=response.url,
            title=response.css('title::text').get())
