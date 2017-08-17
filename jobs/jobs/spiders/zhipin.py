# -*- coding: utf-8 -*-
import scrapy


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['http://www.zhipin.com/']
    start_urls = ['http://http://www.zhipin.com//']

    def parse(self, response):
        pass
