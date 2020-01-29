import scrapy
from craigslist.items import CraigslistItem

class CraigSpider(scrapy.Spider):
    name = "craig_spider"
    #allowed_urls = ['https://newyork.craigslist.org/']
    #start_urls = ['https://newyork.craigslist.org/search/brk/apa']
    start_urls = ['https://newyork.craigslist.org/search/que/apa']

    def parse(self, response):
        num_items = int(response.xpath('//span[@class="totalcount"]/text()').get())
        #page_urls = [f'https://newyork.craigslist.org/search/brk/apa?s={i}' for i in range(0, num_items, 120)]
        page_urls = [f'https://newyork.craigslist.org/search/que/apa?s={i}' for i in range(0, num_items, 120)]

        for url in page_urls[:]:
            yield scrapy.Request(url=url, callback=self.parse_results_page)

    def parse_results_page(self, response):
        listings = response.xpath('//p[@class="result-info"]')

        for listing in listings:
            date = listing.xpath('./time/@datetime').get()
            description = listing.xpath('./a/text()').get()
            price = listing.xpath('./span[@class="result-meta"]/span[@class="result-price"]/text()').get()
            size = listing.xpath('.//span[@class="result-meta"]/span[@class="housing"]/text()').get()
            try:
                size = size.strip()
            except:
                pass
            area = listing.xpath('./span[@class="result-meta"]/span[@class="result-hood"]/text()').get()

            item= CraigslistItem()
            item['date'] = date
            item['description'] = description
            item['price'] = price
            item['size'] = size
            item['area'] = area

            yield item
