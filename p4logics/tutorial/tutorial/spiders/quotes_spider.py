from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self) :
        urls = "https://quotes.toscrape.com/"
        tag = getattr(self,"tag", None)
        if tag is not None:
            url = urls + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self,response):
        for quote in response.css('div.quote'):
            yield{
                "text" : quote.css('span::text').get(),
                "author" : quote.css('small.author::text').get(),
                "tag" : quote.css('div.tags a.tag::text').getall()
            }

            next_page = response.css("li.next a::attr(href)").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page,callback=self.parse)
'''
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f'saved file {filename} in tutorial')
'''
    