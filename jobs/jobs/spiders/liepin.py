# -*- coding: utf-8 -*-
import scrapy


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['http://www.liepin.com/']
    start_urls = ['http://http://www.liepin.com//']

    def parse(self, response):
        pass
