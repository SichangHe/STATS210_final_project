import scrapy
from urllib.parse import urljoin


class Spider(scrapy.Spider):
    name = "Spider"

    def __init__(self, url='', ** kwargs):
        self.start_urls = {url}
        # print(self.start_urls)
        # super(Spider, self).__init__(** kwargs)
        meta = {'download_timeout': 5}

    def parse(self, response):
        products = response.xpath(
            "//*[contains(@class, '')]/a/@href").extract()
        for p in products:
            url = urljoin(response.url, p).strip().split('#', 1)[0].strip('/')
            yield{
                'url': url
            }
