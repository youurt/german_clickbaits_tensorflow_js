import scrapy
from scrapy.http.request import Request
from datetime import datetime
from klickscraper.items import PromipoolItem


class PromipoolSpider(scrapy.Spider):
    name = 'promipool'
    scraped_at = datetime.now()

    def start_requests(self):
        for i in range(1800):
            yield Request(
                url=f"https://www.promipool.de/bm/ajax/block/288/de_DE/default?ngbmContext%5Bez_location_id%5D=2&_hash=MjRcjm7uETK0RH8ZhldIgwcozMZ0p80ExONE08k0NmU%3D&page={i}",
                dont_filter=True,
                callback=self.parse_url)

    def parse_url(self, response):
        follow_ulrs = response.css("a::attr(href)").getall()
        for f in follow_ulrs:
            yield Request(
                url=f,
                dont_filter=True,
                callback=self.parse_page)

    def parse_page(self, response):
        yield PromipoolItem(title=response.css('title::text').get(),
                            text=" ".join(response.css("p::text").getall()),
                            scraped_at=self.scraped_at)
