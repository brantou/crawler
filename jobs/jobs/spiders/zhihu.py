# -*- coding: utf-8 -*-
import scrapy
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    loginUrl = 'https://www.zhihu.com/#signin'
    siginUrl = 'https://www.zhihu.com/login/email'

    feedUrl = 'https://www.zhihu.com/api/v3/feed/topstory'
    nextFeedUrl = ''
    curFeedId = 0

    custom_settings = {
        "COOKIES_ENABLED": True,
    }

    headers = {
        'Host':
        'www.zhihu.com',
        'Connection':
        'keep-alive',
        'Origin':
        'https://www.zhihu.com',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Content-Type':
        'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'X-Requested-With':
        'XMLHttpRequest',
        'DNT':
        1,
        'Referer':
        'https://www.zhihu.com/',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Requests:':
        1,
    }

    cookies = {
        'd_c0':
        '"AHCAtu1iqAmPTped76X1ZdN0X_qAwhjdLUU=|1458699045"',
        '__utma':
        '51854390.1407411155.1458699046.1458699046.1458699046.1',
        '__utmv':
        '51854390.000--|3=entry_date=20160322=1',
        '_zap':
        '850897bb-cba4-4d0b-8653-fd65e7578ac2',
        'q_c1':
        'b7918ff9a5514d2981c30050c8c732e1|1502937247000|1491446589000',
        'aliyungf_tc':
        'AQAAACtKLW+lywEAOhSntJwFFTilwpwt',
        '_xsrf':
        'f3ab08fc68489f44ae77236555367c70',
        'r_cap_id':
        '"M2NjNDAwNTZmY2ExNDA3NzgzNjZkZDA1ODNjZWJkNjI=|1503458111|36984ab33f21997b742d97ace2e02043cbb0a76e"',
        'cap_id':
        '"ZTIxMmM5Yzg1MGJkNDcxNjgxYzZjMjNlYTg3OGE0Yzk=|1503457914|8dce8550bca28e427771a0e7e1fe1bafb6e170f6"',
    }

    def start_requests(self):
        return [
            scrapy.http.FormRequest(
                self.loginUrl,
                headers=self.headers,
                cookies=self.cookies,
                meta={'cookiejar': 1},
                callback=self.post_login)
        ]

    def post_login(self, response):
        xsrf = response.css(
            'div.view-signin > form > input[name=_xsrf]::attr(value)'
        ).extract_first()
        self.headers['X-Xsrftoken'] = xsrf

        return [
            scrapy.http.FormRequest(
                self.siginUrl,
                method='POST',
                headers=self.headers,
                meta={'cookiejar': response.meta['cookiejar']},
                formdata={
                    '_xsrf': xsrf,
                    'captcha_type': 'cn',
                    'email': 'xxxxxx@163.com',
                    'password': 'xxxxxx',
                },
                callback=self.after_login)
        ]

    def after_login(self, response):
        jdict = json.loads(response.body)
        print('after_login', jdict)
        if jdict['r'] == 0:
            z_c0 = response.headers.getlist('Set-Cookie')[2].split(';')[
                0].split('=')[1]
            self.headers['authorization'] = 'Bearer ' + z_c0
            return scrapy.http.FormRequest(
                url=self.feedUrl,
                method='GET',
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                    'action_feed': 'True',
                    'limit': '10',
                    'action': 'down',
                    'after_id': str(self.curFeedId),
                    'desktop': 'true'
                },
                callback=self.parse)
        else:
            print(jdict['error'])

    def parse(self, response):
        with open('zhihu.json', 'a') as fd:
            fd.write(response.body)
        jdict = json.loads(response.body)
        jdatas = jdict['data']
        for entry in jdatas:
            entry['pid'] = entry['id']
            yield entry

        jpaging = jdict['paging']
        self.curFeedId += len(jdatas)
        if jpaging['is_end'] == False and self.curFeedId < 50:
            self.nextFeedUrl = jpaging['next']
            yield self.next_request(response)

    def next_request(self, response):
        return scrapy.http.FormRequest(
            url=self.nextFeedUrl,
            method='GET',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            callback=self.parse)
