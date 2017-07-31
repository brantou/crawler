# -*- coding: utf-8 -*-
import scrapy


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
