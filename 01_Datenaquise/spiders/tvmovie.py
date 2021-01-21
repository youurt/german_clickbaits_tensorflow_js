import scrapy
from scrapy import Request
from klickscraper.items import TvMovieItem
from datetime import datetime


class TvmovieSpider(scrapy.Spider):
    name = 'tvmovie'
    allowed_domains = ['www.tvmovie.de']
    start_urls = ['http://www.tvmovie.de/news']
    scraped_at = datetime.now()

    def start_requests(self):
        for i in range(787):
            yield Request(
                url=f'https://www.tvmovie.de/news?page={i}',
                dont_filter=True,
                callback=self.parse_page)

    def parse_page(self, response):
        for a in response.css("a::attr(href)").getall():
            if "/news/" in a:
                yield Request(
                    url=f"https://www.tvmovie.de/{a}",
                    dont_filter=True,
                    callback=self.parse_page_content)

    def parse_page_content(self, response):
        yield TvMovieItem(
            text=" ".join(response.css("p::text").getall()),
            scraped_at=self.scraped_at,
            url=response.url,
            title=response.css('title::text').get())
