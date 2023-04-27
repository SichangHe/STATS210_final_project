import scrapy
from urllib.parse import urljoin
from sortedcontainers import SortedList
import re


class Spider(scrapy.Spider):
    name = "Spider"

    def __init__(self, url='', ** kwargs):
        self.start_urls = {url}

    def parse(self, response):
        record = SortedList()
        blacked = SortedList()  # debug
        unrecorded = SortedList()  # debug

        keyword = "https://dukekunshan\.edu\.cn"
        keyword = re.compile(keyword)

        # blacklist filters
        blacklist_filter = re.compile(
            "(about/about)|(/event-list[/?])|(/node)|(node_tid)|(\.pdf)|(\.docx)|(print/)|(/recruiting-events[/?])|(/printpdf/)|(photo.*\?)|([0-9]{4}-[0-9]{2}(?![0-9]))")

        products = response.xpath(
            "//*[contains(@class, '')]/a/@href").extract()
        for p in products:
            url = urljoin(response.url, p).strip().split('#', 1)[0].strip('/')
            if not re.search(keyword, url):
                if unrecorded.__contains__(url):
                    continue
                unrecorded.add(url)  # debug
                continue
            if re.search(blacklist_filter, url):
                if blacked.__contains__(url):
                    continue
                blacked.add(url)  # debug
                continue
            if record.__contains__(url):
                continue
            record.add(url)
        for url in record:
            yield{
                'url': url
            }
        for bla in blacked:
            yield{
                'blacklisted': bla
            }
        for un in unrecorded:
            yield{
                'unrecorded': un
            }
