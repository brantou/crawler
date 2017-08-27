# -*- coding: utf-8 -*-
import scrapy
import json


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['zhaopin.meituan.com']
    start_urls = ['http://zhaopin.meituan.com/']
    positionUrl = 'http://zhaopin.meituan.com/search'
    detailUrl = 'http://zhaopin.meituan.com/%d/jobDetail'

    headers = {
        'origin':
        "http://zhaopin.meituan.com",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'content-type':
        "application/json",
        'accept':
        "*/*",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
    }

    pageIndex = 1
    pageSize = 8
    itemCount = 0

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        if jdict['code'] != 200:
            return

        pageInfo = jdict['pageInfo']
        self.itemCount = pageInfo['itemCount']
        pageList = jdict['pageList']
        for page in pageList:
            yield scrapy.http.FormRequest(
                url=self.detailUrl % (page['id']),
                method='POST',
                headers=self.headers,
                callback=self.parse_detail)

        if self.pageIndex * self.pageSize < self.itemCount:
            self.pageIndex += 1
            yield self.next_request()

    def parse_detail(self, response):
        jdict = json.loads(response.body)
        if jdict['code'] == 200:
            jdata = jdict['data']
            jdata['pid'] = jdata['id']
            yield jdata

    def next_request(self):
        payload = json.dumps({
            "pageInfo": {
                "pageIndex": self.pageIndex,
                "pageSize": self.pageSize,
                "itemCount": self.itemCount,
            },
            "workLocations": [],
            "jobTypes": [],
            "jobSubTypes": [],
            "keyword": ""
        })
        print(payload)

        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='POST',
            headers=self.headers,
            body=payload,
            callback=self.parse)
