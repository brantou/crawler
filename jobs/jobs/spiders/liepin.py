# -*- coding: utf-8 -*-
import scrapy
from jobs.items import LiepinItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']
    positionUrl = 'http://www.liepin.com/'
    curPage = 1
    header = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        job_list = response.css('ul.sojob-list > li')
        for job in job_list:
            item = LiepinItem()
            job_info = job.css('div.sojob-item-main > div.job-info')
            item['pid'] = job_info.css('h3 > a::attr(href)').extract_first()
            item['positionName'] = job_info.css(
                'h3::attr(title)').extract_first()
            job_infos = job.css(
                'p.condition.clearfix::attr(title)').extract_first().split('_')
            item['salary'] = job_infos[0]
            item['city'] = job_info[1]
            item['education'] = job_infos[2]
            item['workYear'] = job_info[3]
            company_info = job.css('div.sojob-item-main > div.company-info')
            item['companyShortName'] = company_info.css(
                'p.company-name > a::text').extract_first()
            item['industryField'] = company_info.css(
                'p.field-financing > span > a::text').extract_first()
            item['companyLabelList'] = company_info.css(
                'p.temptation.clearfix > span::text').extract()
            yield item

        self.curPage += 1
        yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl, headers=self.headers, callback=self.parse)
