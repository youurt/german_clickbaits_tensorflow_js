from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


class Wiki(DeclarativeBase):
    __tablename__ = "wiki"
    page_id = Column('page_id', String(255), primary_key=True)
    title = Column("title", String(255))
    category = Column("category", String(255))
    scraped_at = Column("scraped_at", DateTime)
    extract = Column("extract", Text)


class Buzz(DeclarativeBase):
    __tablename__ = "buzz"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Heftig(DeclarativeBase):
    __tablename__ = "heftig"
    page_id = Column('page_id', String(255), primary_key=True)
    headline = Column("headline", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Movie(DeclarativeBase):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Frau(DeclarativeBase):
    __tablename__ = "frau"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Quiz(DeclarativeBase):
    __tablename__ = "quiz"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Tasty(DeclarativeBase):
    __tablename__ = "tasty"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Bravo(DeclarativeBase):
    __tablename__ = "bravo"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
    url = Column("url", String(255))


class Promipool(DeclarativeBase):
    __tablename__ = "promipool"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)


class Webde(DeclarativeBase):
    __tablename__ = "webde"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    scraped_at = Column("scraped_at", DateTime)
    text = Column("text", Text)
