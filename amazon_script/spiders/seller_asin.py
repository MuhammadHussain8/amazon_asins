from scrapy import Spider
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

    uk_proxy = [
        '104.248.169.218:8118', '176.248.120.70:3128', '46.101.50.133:8080', '51.158.172.165:8811', '51.158.165.18:8811',
        '78.141.222.210:8080', '78.141.211.143:8080', '167.172.180.46:42580', '167.172.184.166:43827', '51.77.144.148:3128',
        '167.172.180.40:34265', '51.158.165.18:8811', '51.158.165.18:8811', '163.172.47.182:8080', '167.172.184.166:40607',
        '167.172.180.46:35884', '51.158.186.242:8811', '51.158.172.165:8811', '167.172.180.46:37121'
    ]

    us_proxy = [
        '66.97.120.140:3128', '152.44.143.138:8080', '18.191.170.143:3128', '52.14.114.87:3128', '138.124.180.62:3128',
        '192.154.249.73:8000', '18.222.178.66:4444', '156.19.50.150:3128', '47.225.156.67:8080', '97.125.145.145:8080',
        '107.178.9.186:8080', '35.175.196.224:3128', '173.208.235.202:3128', '173.208.209.178:3128'
    ]

    def run_process(self, url):
        if '.uk' in url:
            self.SETTINGS['ROTATING_PROXY_LIST'] = self.uk_proxy
        else:
            self.SETTINGS['ROTATING_PROXY_LIST'] = self.us_proxy
        process = CrawlerProcess(settings=self.SETTINGS)
        process.crawl(SellerAsin, asin_url=url)
        process.start()
