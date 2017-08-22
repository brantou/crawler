# -*- coding: utf-8 -*-
import scrapy


class A100offerSpider(scrapy.Spider):
    name = '100offer'
    allowed_domains = ['cn.100offer.com']
    start_urls = ['https://cn.100offer.com/']
    loginUrl = 'https://cn.100offer.com/signin'
    signinUrl = 'https://cn.100offer.com/talents/sign_in.json'
    positionUrl = 'https://cn.100offer.com/job_positions/positions_list'

    curPage = 1

    headers = {
        'accept':
        "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
        'origin':
        "https://cn.100offer.com",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'x-requested-with':
        "XMLHttpRequest",
        'content-type':
        "application/x-www-form-urlencoded; charset=UTF-8",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
    }

    def start_requests(self):
        return [
            scrapy.http.FormRequest(
                self.loginUrl, meta={'cookiejar': 1}, callback=self.post_login)
        ]

    def post_login(self, response):
        csrf = response.css(
            'head > meta[name=csrf-token]::attr(content)').extract_first()
        self.headers['X-CSRF-Token'] = csrf
        return [
            scrapy.http.FormRequest.from_response(
                response,
                headers=self.headers,
                meta={'cookiejar': response.meta['cookiejar']},
                formdata={
                    'commit': u'确定',
                    'refer': u'',
                    'talent[email]': u'xxxxxx@gmail.com',
                    'talent[password]': u'xxxxxx',
                    'talent[remember_me]': u'0',
                    'utf8': u'✓',
                },
                callback=self.after_login)
        ]

    def after_login(self, response):
        return self.next_request(response)

    def parse(self, response):
        with open('100offer.html', 'w') as fd:
            fd.write(response.body)

    def next_request(self, response):
        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='GET',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            formdata={
                'locations': 'all',
                'company_size': 'all',
                'degree': 'all',
                'industry': 'all',
                'work_year': '0,11',
                'page': str(self.curPage)
            },
            callback=self.parse)
