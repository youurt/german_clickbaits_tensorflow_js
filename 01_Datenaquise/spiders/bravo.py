from datetime import datetime
import scrapy
from scrapy.http.request import Request
from klickscraper.items import BravoItem


class BravoSpider(scrapy.Spider):
    name = 'bravo'
    allowed_domains = ['www.bravo.de']
    start_urls = ['http://www.bravo.de/']
    scraped_at = datetime.now()

    def start_requests(self):
        yield Request(
            url="https://www.bravo.de/?exclude%5B0%5D=388363&page=1",
            dont_filter=True,
            callback=self.parse_next)

    def parse_next(self, response):
        next_page = response.css(
            ".button-more").css("._button").css("a::attr(href)").get()

        yield Request(
            url=f"https://www.bravo.de{next_page}",
            dont_filter=True,
            callback=self.parse_page_content)

    def parse_page_content(self, response):

        headline = response.css(".headline").css("a::attr(href)").getall()

        for line in headline:
            if not "https" in line:
                yield Request(
                    url=f"https://www.bravo.de{line}",
                    dont_filter=True,
                    callback=self.parse_items)

        next_page = response.css(
            ".button-more").css("._button").css("a::attr(href)").get()

        if next_page:
            yield Request(
                url=f"https://www.bravo.de{next_page}",
                dont_filter=True,
                callback=self.parse_page_content)
        else:
            return

    def parse_items(self, response):

        yield BravoItem(
            text=" ".join(response.css("p::text").getall()),
            scraped_at=self.scraped_at,
            url=response.url,
            title=response.css('title::text').get())
