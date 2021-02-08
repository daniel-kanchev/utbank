import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from utbank.items import Article


class UtSpider(scrapy.Spider):
    name = 'ut'
    start_urls = ['https://www.utbank.co.uk/news-and-media/']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            link = article.xpath('./div[@class="media-and-news-post-inner"]/div[@class="text"]/a/@href').get()
            date = " ".join(article.xpath('.//time//text()').get().split()[1:])[:-1]
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response, date):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="mainheader"]/text()').get().strip()

        date = datetime.strptime(date, '%d %B %Y')
        date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="two-thirds"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
