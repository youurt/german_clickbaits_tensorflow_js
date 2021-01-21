from scrapy import signals
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from klickscraper.items import WikinewsItem, BuzzfeedItem, HeftigItem, TvMovieItem, FrauenseiteItem, BuzzfeedQuizItem, TastyQuizItem, BravoItem, PromipoolItem, WebdeItem
import klickscraper.models as models
import os


class SqlitePipeline:
    def __init__(self, settings):
        self.database = settings.get("DATABASE")
        self.database_dev = settings.get("DATABASE_DEV")
        self.sessions = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        if "IS_APP_ENGINE" in os.environ:
            # GAE + Cloud SQL
            engine = create_engine(URL(**self.database))
            # GAE + Big Query
            #engine = create_engine("bigquery://regionale-preise/scraping", credentials_path="C:/Users/jwendt/Documents/regionale-preise-96dcb5ae4f68.json")
        else:
            # LOKAL
            engine = create_engine(URL(**self.database_dev))
        return engine

    def create_tables(self, engine):
        models.DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, WikinewsItem):
            wiki_exists = session.query(models.Wiki).filter_by(
                page_id=item["page_id"]).first()
            if wiki_exists is not None:
                w = wiki_exists
            else:
                w = models.Wiki(**{i: item[i] for i in item if i in [
                    "page_id", "title", "scraped_at", "category", "extract"]})

            try:
                session.add(w)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, BuzzfeedItem):
            buzz_exists = session.query(models.Buzz).filter_by(
                title=item["title"]).first()
            if buzz_exists is not None:
                b = buzz_exists
            else:
                b = models.Buzz(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(b)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, HeftigItem):
            heftig_exists = session.query(models.Heftig).filter_by(
                page_id=item["page_id"]).first()
            if heftig_exists is not None:
                h = heftig_exists
            else:
                h = models.Heftig(**{i: item[i] for i in item if i in [
                    "page_id", "headline", "scraped_at", "text", "url"]})

            try:
                session.add(h)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, TvMovieItem):
            movie_exists = session.query(models.Movie).filter_by(
                title=item["title"]).first()
            if movie_exists is not None:
                m = movie_exists
            else:
                m = models.Movie(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(m)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, FrauenseiteItem):
            frau_exists = session.query(models.Frau).filter_by(
                title=item["title"]).first()
            if frau_exists is not None:
                f = frau_exists
            else:
                f = models.Frau(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(f)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, BuzzfeedQuizItem):
            quiz_exists = session.query(models.Quiz).filter_by(
                title=item["title"]).first()
            if quiz_exists is not None:
                q = quiz_exists
            else:
                q = models.Quiz(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(q)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, TastyQuizItem):
            tasty_exists = session.query(models.Tasty).filter_by(
                title=item["title"]).first()
            if tasty_exists is not None:
                t = tasty_exists
            else:
                t = models.Tasty(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(t)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, BravoItem):
            bravo_exists = session.query(models.Bravo).filter_by(
                title=item["title"]).first()
            if bravo_exists is not None:
                br = bravo_exists
            else:
                br = models.Bravo(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text", "url"]})

            try:
                session.add(br)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, PromipoolItem):
            promi_exists = session.query(models.Promipool).filter_by(
                title=item["title"]).first()
            if promi_exists is not None:
                pr = promi_exists
            else:
                pr = models.Promipool(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text"]})

            try:
                session.add(pr)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item

    def process_item(self, item, spider):
        session = self.sessions[spider]

        if isinstance(item, WebdeItem):
            webde_exists = session.query(models.Webde).filter_by(
                title=item["title"]).first()
            if webde_exists is not None:
                we = webde_exists
            else:
                we = models.Webde(**{i: item[i] for i in item if i in [
                    "title", "scraped_at", "text"]})

            try:
                session.add(we)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item
