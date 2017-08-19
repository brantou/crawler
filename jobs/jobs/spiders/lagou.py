# -*- coding: utf-8 -*-
import scrapy
import json
from jobs.items import JobsItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/']
    positionUrl = 'https://www.lagou.com/jobs/positionAjax.json?'

    totalPageCount = 0
    curPage = 1

    city = u'上海'
    keywords = [
        u'大数据', u'云计算', u'docker', u'中间件', 'Node.js', u'数据挖掘', u'自然语言处理',
        u'搜索算法', u'精准推荐', u'全栈工程师', u'图像处理', u'机器学习', u'语音识别'
    ]
    kd_cur = 0
    keyword = keywords[0]

    item_fns = [
        'city', 'education', 'workYear', 'salary', 'firstType', 'secondType',
        'positionName', 'positionAdvantage', 'positionLables',
        'companyFullName', 'companyShortName', 'companySize',
        'companyLabelList', 'financeStage', 'industryField', 'industryLables',
        'district', 'isSchoolJob', 'jobNature', 'createTime'
    ]

    headers = {
        'origin':
        "https://www.lagou.com",
        'x-anit-forge-code':
        "0",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'x-requested-with':
        "XMLHttpRequest",
        'x-anit-forge-token':
        "None",
        'dnt':
        "1",
        'referer':
        "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_golang%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_checkmore; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502382038; _ga=GA1.2.1475031428.1501230295; LGSID=20170811001727-66af8955-7de7-11e7-96c3-525400f775ce; LGRID=20170811001930-b074a8af-7de7-11e7-96c3-525400f775ce; SEARCH_ID=a614dcefbf1d400780199aa2e9b1c95e; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502115517; _ga=GA1.2.1475031428.1501230295; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; LGRID=20170807221749-312e97c2-7b7b-11e7-8499-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; _ga=GA1.2.1475031428.1501230295; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502897724; LGSID=20170816233506-7a902bd5-8298-11e7-be41-525400f775ce; LGRID=20170816233523-84dd2b0e-8298-11e7-be41-525400f775ce; SEARCH_ID=b1bfc38325524b19834cbce76deddaa6",
        'cache-control':
        "no-cache",
        'postman-token':
        "fdd777d6-9b34-b322-5c2d-c6164023e669"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        jcontent = jdict['content']
        jposresult = jcontent['positionResult']
        jresult = jposresult['result']
        self.totalPageCount = int(jposresult['totalCount']) / int(
            jcontent['pageSize']) + 1
        for entry in jresult:
            item = JobsItem()
            item['pid'] = entry['positionId']
            item['keyword'] = self.keyword
            for fn in self.item_fns:
                item[fn] = entry[fn]
                yield item

        if self.curPage <= self.totalPageCount:
            self.curPage += 1
            yield self.next_request()
        elif self.kd_cur < len(self.keywords) - 1:
            self.curPage = 1
            self.totalPageCount = 0
            self.kd_cur += 1
            self.keyword = self.keywords[self.kd_cur]
            yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl,
            headers=self.headers,
            formdata={'pn': str(self.curPage),
                      'kd': self.keyword},
            callback=self.parse)
