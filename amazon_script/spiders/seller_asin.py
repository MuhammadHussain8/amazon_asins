from scrapy import Spider
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SellerAsin(Spider):
    name = 'seller_asin'

    def start_requests(self):
        url = self.asin_url
        yield SeleniumRequest(url=url)

    def parse(self, response):
        for url in response.css('span[data-component-type="s-product-image"] a::attr(href)').extract():
            item = dict()
            item['ASIN'] = url.split('dp/')[1].split('/ref')[0]
            yield item

        if response.css('.a-pagination .a-last a::attr(href)').extract_first():
            url = 'https://www.amazon.co.uk/{}'.format(response.css('.a-pagination .a-last a::attr(href)').extract_first())
            yield SeleniumRequest(url=url)


class RunSpider():

    SETTINGS = get_project_settings()
    process = CrawlerProcess(settings=SETTINGS)

    def run_process(self, url):
        self.process.crawl(SellerAsin, asin_url=url)
        self.process.start()
