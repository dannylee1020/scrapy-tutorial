import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # self.logger.info('hello this is my first spider')
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader(item = QuoteItem(), selector = quote)
            
            # load data to item objects
            loader.add_xpath('quote_content', ".//span[@class='text']/text()")
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            # get url to author page
            author_url = quote.css('.author+a::attr(href)').get()
            # go to the author page and pass the collected quote info
            yield response.follow(author_url, self.parse_author, meta = {'quote_item': quote_item})

        # go to next page
        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)

        
# get author information from author page
    def parse_author(self, response):
        # load collected item from first page
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item = quote_item, response = response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_born_location', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()