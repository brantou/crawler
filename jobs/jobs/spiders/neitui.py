# -*- coding: utf-8 -*-
import scrapy
from jobs.items import NeituiItem


class NeituiSpider(scrapy.Spider):
    name = 'neitui'
    allowed_domains = ['www.neitui.me']
    start_urls = ['http://www.neitui.me/']
    positionUrl = 'http://www.neitui.me/?name=job&handle=lists&page='
    curPage = 1
    headers = {
        'x-devtools-emulate-network-conditions-client-id':
        "348a57a3-9290-45f3-af21-7222c2cd355e",
        'upgrade-insecure-requests':
        "1",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'accept':
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "PHPSESSID=815c63d61251e21fa506c4456867cf7d; Hm_lvt_21de977c0eb6fd0c491abddcb289ff96=1502937435; Hm_lpvt_21de977c0eb6fd0c491abddcb289ff96=1503048973; Hm_lvt_21de977c0eb6fd0c491abddcb289ff96=1502937435; Hm_lpvt_21de977c0eb6fd0c491abddcb289ff96=1503137368",
        'cache-control':
        "no-cache",
        'postman-token':
        "da1d8247-3bbc-fb6e-0a4f-9fbb14c9277a"
    }

    def start_requests(self):
        return [self.next_request()]

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
            if len(infos) < 7:  # discard incomplete data
                continue
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
            self.positionUrl + str(self.curPage),
            headers=self.headers,
            callback=self.parse)
