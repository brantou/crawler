# -*- coding: utf-8 -*-
import scrapy
from jobs.items import NeituiItem


class NeituiSpider(scrapy.Spider):
    name = 'neitui'
    allowed_domains = ['www.neitui.me']
    start_urls = ['http://www.neitui.me/']
    positionUrl = 'http://www.neitui.me/'
    curPage = 1
    header = {}

    def start_requests(self):
        return [self.next_request]

    def parse(self, response):
        job_list = response.css('ul.list-items > li.clearfix')
        for job in job_list:
            item = NeituiItem()
            job_info = job.css('div.media > div.media-body > div.positionleft')
            item['pid'] = job_info.css('div.mt5.clearfix > a::attr(href)'
                                       ).extract_first().split('/')[-1]
            item['positionName'] = job_info.css(
                'div.mt5.clearfix > a::text').extract_first()
            infos = job_info.css('div > span::text').extract()
            item['salary'] = infos[1]
            item['workYear'] = infos[2]
            item['education'] = infos[3]
            item['city'] = infos[4]
            item['financeStage'] = infos[6]
            item['companyShortName'] = job_info.css(
                'div.grey.mt5 > span > a::text').extract_first()
            yield item

        self.curPage += 1
        yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl, headers=self.headers, callback=self.parse)
