import scrapy
from urllib.parse import urljoin


class DKUSpider(scrapy.Spider):
    name = "DKUSpider"
    start_urls = [
        "https://dukekunshan.edu.cn/en",
    ]

    def parse(self, response):
        products = response.xpath(
            # "//*[contains(@class, 'leaf')]/a/@href").extract()
            "//*[contains(@class, '')]/a/@href").extract()
        for p in products:
            url = urljoin(response.url, p)
            yield{
                'url': url
            }
            # yield scrapy.Request(url, callback=self.parse)
