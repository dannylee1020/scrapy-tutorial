from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, DateTime, Float, Boolean, Text
from scrapy.utils.project import get_project_settings


Base = declarative_base()

def db_connect():
    '''
    create database connection using database setting from settings.py
    '''
    return create_engine('postgresql+psycopg2://dhyungseoklee:scrapypw@localhost/scrapy_tutorial')
# 

def create_table(engine):
    Base.metadata.create_all(engine)

# Association table for many to many between quote and tag
quote_tag = Table('quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quote.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Quote(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key = True)
    quote_content = Column('quote_content', Text())
    author_id = Column(Integer, ForeignKey('author.id'))
    tags = relationship('Tag', secondary = 'quote_tag', 
        lazy = 'dynamic', backref = 'quote') #many to many relationship for tag and quote


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique = True)
    birthday = Column('birthday', DateTime)
    bornlocation = Column('born_location', String(150))
    bio = Column('bio', Text())
    quotes = relationship('Quote', backref='author') # one author to many quotes. 


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key = True)
    name = Column('name', String(30), unique = True)
    quotes = relationship('Quote', secondary = 'quote_tag',
        lazy = 'dynamic', backref = 'tag') # many to many for quote and tag



