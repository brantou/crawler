# -*- coding: utf-8 -*-
import scrapy
from jobs.items import LiepinItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/']
    positionUrl = 'https://www.liepin.com/zhaopin/?ckid=6bbfc3230c0b51b8&fromSearchBtn=2&degradeFlag=0&industries=040%2C420%2C010%2C030&init=-1&dqs=020&headckid=6bbfc3230c0b51b8'

    headers = {
        'upgrade-insecure-requests':
        "1",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'accept':
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "gr_user_id=c16f79ec-88d3-4c33-a195-e28eea77f2c3; __uuid=1502937530390.55; _uuid=EE0EB1A7FFA8481E2151B9D2BC2FA184; _fecdn_=1; verifycode=d7ccc750bcb6414ea9f65aebfe48d03b; abtest=0; JSESSIONID=6CBB5FB3B4358663B2DC113C1981F568; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=109ab3b3-a15d-440c-bcab-4c04be40eea1; __tlog=1502937530391.84%7C00000000%7CR000000035%7Cs_o_009%7Cs_o_009; __session_seq=24; __uv_seq=20; _mscid=00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1502937531,1502937750; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1503045664; gr_user_id=c16f79ec-88d3-4c33-a195-e28eea77f2c3; __uuid=1502937530390.55; _uuid=EE0EB1A7FFA8481E2151B9D2BC2FA184; verifycode=d7ccc750bcb6414ea9f65aebfe48d03b; slide_guide_home=1; abtest=0; JSESSIONID=0EBA04D3E330C5357DB0D4B51D31597F; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=109ab3b3-a15d-440c-bcab-4c04be40eea1; __tlog=1502937530391.84%7C00000000%7CR000000035%7Cs_o_009%7Cs_o_009; __session_seq=25; __uv_seq=21; _mscid=00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1502937531,1502937750; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1503134671",
        'cache-control':
        "no-cache",
        'postman-token':
        "98d65f4a-def5-2d46-43bf-82a5cc1fcf72"
    }

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
            item['city'] = job_infos[1]
            item['education'] = job_infos[2]
            item['workYear'] = job_infos[3]
            company_info = job.css('div.sojob-item-main > div.company-info')
            item['companyShortName'] = company_info.css(
                'p.company-name > a::text').extract_first()
            item['industryField'] = company_info.css(
                'p.field-financing > span > a::text').extract_first()
            item['companyLabelList'] = company_info.css(
                'p.temptation.clearfix > span::text').extract()
            yield item

        page_list = response.css('div.pager > div.pagerbar > a')
        for page in page_list:
            if page.css('a::text').extract_first() == u'下一页':
                if page.css('a::attr(class)').extract_first() != 'disabled':
                    self.positionUrl = page.css(
                        'a::attr(href)').extract_first()
                else:
                    self.positionUrl = ""
        if self.positionUrl != "":
            yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl, headers=self.headers, callback=self.parse)
