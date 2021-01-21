import json
import scrapy
from scrapy import Request
from klickscraper.items import WikinewsItem
from datetime import datetime


class WikitextSpider(scrapy.Spider):
    name = 'wikitext'
    allowed_domains = ['www.de.wikinews.org']
    start_urls = ['http://www.de.wikinews.org/']
    scraped_at = datetime.now()
    # categories = ['Themenportal_Politik', 'Themenportal_Wirtschaft' 'Themenportal_Kultur', 'Themenportal_Unfall', 'Themenportal_Wetter', 'Themenportal_Sport',
    #               'Themenportal_Arbeit_und_Soziales', 'Themenportal_Umwelt', 'Themenportal_Computer', 'Themenportal_Wissenschaft', 'Themenportal_Recht']

    # Um die um die Kategorie zu ändern, bitte dieses Feld mit der entsprechenden Kategorie anpassen
    _smallcategories = ["Themenportal_Kultur"]

    def start_requests(self):
        for category in self._smallcategories:
            yield Request(
                url=f"https://de.wikinews.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&format=json&cmlimit=max",
                dont_filter=True,
                callback=self.parse_first_page,
                cb_kwargs=dict(category=category))

    def parse_first_page(self, response, category):
        pageIds = []
        results = json.loads(response.body)
        articles = results["query"]["categorymembers"]
        for article in articles:
            pageIds.append(article["pageid"])

        for page_id in pageIds:
            yield Request(
                url=f"https://de.wikinews.org/w/api.php?action=query&format=json&prop=extracts&pageids={page_id}&explaintext=true&exintro=true",
                cb_kwargs=dict(category=category, page_id=page_id),
                callback=self.parse_page_content,
                dont_filter=True)

        if "continue" in results:
            yield Request(
                url=f"https://de.wikinews.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&format=json&cmlimit=max&cmcontinue={results['continue']['cmcontinue']}",
                cb_kwargs=dict(category=category),
                callback=self.parse_first_page,
                dont_filter=True)
        else:
            return

    def parse_page_content(self, response, category, page_id):
        results = json.loads(response.body)

        yield WikinewsItem(
            page_id=page_id,
            title=results["query"]["pages"][str(page_id)]["title"],
            extract=results["query"]["pages"][str(page_id)]["extract"],
            category=category,
            scraped_at=self.scraped_at)
