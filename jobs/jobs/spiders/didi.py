# -*- coding: utf-8 -*-
import scrapy
import json


class DidiSpider(scrapy.Spider):
    name = 'didi'
    allowed_domains = ['job.didichuxing.com']
    start_urls = ['http://job.didichuxing.com']
    positionUrl = 'http://job.didichuxing.com/recruit/api/front/list'
    detailUrl = 'http://job.didichuxing.com/recruit/api/front/view/%d'

    headers = {
        'accept':
        "application/json, text/plain, */*",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
    }

    pageIndex = 1
    pageSize = 10
    itemCount = 0

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        jdata = jdict['data']
        self.itemCount = jdata['total']
        items = jdata['items']
        for item in items:
            yield scrapy.http.FormRequest(
                url=self.detailUrl % (item['jdId']),
                method='GET',
                headers=self.headers,
                callback=self.parse_detail)

        if self.pageIndex * self.pageSize < self.itemCount:
            self.pageIndex += 1
            yield self.next_request()

    def parse_detail(self, response):
        jdict = json.loads(response.body)
        jdata = jdict['data']
        jdata['pid'] = response.url.split('/')[-1]
        yield jdata

    def next_request(self):
        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='GET',
            headers=self.headers,
            formdata={
                "channelCode": "501",
                "page": str(self.pageIndex),
                "recruitType": "1",
                "size": str(self.pageSize)
            },
            callback=self.parse)
