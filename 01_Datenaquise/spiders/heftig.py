import scrapy
from scrapy import Request
import json
from klickscraper.items import HeftigItem
from datetime import datetime


class HeftigSpider(scrapy.Spider):
    name = 'heftig'
    start_urls = ['http://heftig.de/']
    scraped_at = datetime.now()

    def start_requests(self):
        for page in range(9):
            yield Request(
                url=f'https://www.heftig.de/_main_json/{page}.json',
                dont_filter=True,
                callback=self.parse_page)

    def parse_page(self, response):
        results = json.loads(response.body)["feed"]
        for feed in results:
            yield Request(
                url=feed["link"],
                dont_filter=True,
                callback=self.parse_content,
                cb_kwargs=dict(headline=feed["headline"], id=feed["id"]))

    def parse_content(self, response, headline, id):
        yield HeftigItem(
            text=" ".join(response.css("p::text").getall()),
            scraped_at=self.scraped_at,
            url=response.url,
            headline=headline,
            page_id=id)
