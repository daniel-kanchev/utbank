import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from utbank.items import Article


class UtSpider(scrapy.Spider):
    name = 'ut'
    start_urls = ['https://www.utbank.co.uk/news-and-media/']

    def parse(self, response):
        links = response.xpath('').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('').get().strip()
        date = response.xpath('').get().strip()
        date = datetime.strptime(date, '')
        date = date.strftime('%Y/%m/%d')
        content = response.xpath('').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        # item.add_value('author', author)
        # item.add_value('category', category)
        # item.add_value('tags', tags)

        return item.load_item()

# response.xpath('').get()

