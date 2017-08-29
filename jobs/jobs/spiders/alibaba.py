# -*- coding: utf-8 -*-
import scrapy
import json


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['http://job.alibaba.com/']
    positionUrl = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'

    totalPage = 0
    pageIndex = 1
    pageSize = 10

    headers = {
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'origin':
        "https://job.alibaba.com",
        'x-requested-with':
        "XMLHttpRequest",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        jreturnVal = jdict['returnValue']
        self.totalPage = int(jreturnVal['totalPage'])
        jdatas = jreturnVal['datas']
        for entry in jdatas:
            entry['pid'] = entry['id']
            yield entry

        if self.pageIndex < self.totalPage:
            self.pageIndex += 1
            yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='POST',
            headers=self.headers,
            formdata={
                'pageIndex': str(self.pageIndex),
                'pageSize': str(self.pageSize),
            },
            callback=self.parse)
