# -*- coding: utf-8 -*-
import scrapy
import json
from jobs.items import JobsItem

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    # allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/jobs/']
    positionUrl = 'http://www.lagou.com/jobs/positionAjax.json?'

    totalPageCount = 0
    curPage = 1

    city = u'上海'
    keywords = [u'大数据',u'云计算',u'docker',u'中间件','Node.js',
                u'数据挖掘',u'自然语言处理',u'搜索算法',u'精准推荐',
                u'全栈工程师',u'图像处理',u'机器学习',u'语音识别']
    kd_cur = 0
    keyword = keywords[0]

    item_fns = ['city','education','workYear', 'salary',
                'firstType', 'secondType',
                'positionName','positionAdvantage', 'positionLables',
                'companyFullName', 'companyShortName',
                'companySize', 'companyLabelList',
                'financeStage', 'industryField', 'industryLables',
                'district', 'isSchoolJob', 'jobNature', 'createTime']

    headers = {
        'origin': "https://www.lagou.com",
        'x-anit-forge-code': "0",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-devtools-emulate-network-conditions-client-id': "10bf7e10-9a65-4107-af06-8c1e4e2adfb0",
        'x-requested-with': "XMLHttpRequest",
        'x-anit-forge-token': "None",
        'x-devtools-request-id': "34764.994",
        'dnt': "1",
        'referer': "https://www.lagou.com/jobs/list_golang?labelWords=&fromSearch=true&suginput=",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie': "PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; _gat=1; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; SEARCH_ID=a50321fae35144159899efa4748969f9; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501315350; _ga=GA1.2.1475031428.1501230295; LGSID=20170729153328-36c6e933-7430-11e7-a5f5-525400f775ce; LGRID=20170729160222-406c00aa-7434-11e7-a676-525400f775ce; TG-TRACK-CODE=search_code; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E4%B8%8A%E6%B5%B7; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502115562; _ga=GA1.2.1475031428.1501230295; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; LGRID=20170807221829-4925d8ec-7b7b-11e7-8499-525400f775ce; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1502115517; _ga=GA1.2.1475031428.1501230295; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; LGRID=20170807221749-312e97c2-7b7b-11e7-8499-525400f775ce; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=index_search; SEARCH_ID=8540f6617de14ed6bdd94899253c347c",
        'cache-control': "no-cache",
        'postman-token': "f1871599-3a8e-0745-a34b-b8c17c4328f2"
    }

    def start_requests(self):
         return [scrapy.http.FormRequest(
             self.positionUrl,
             formdata={
                 'pn':str(self.curPage),
                 'kd':self.keyword,
                 'city': self.city},
             headers=self.headers,
             callback=self.parse)]


    def parse(self, response):
        print response.body
        item = JobsItem()
        jdict = json.loads(response.body)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        jresult = jposresult["result"]
        self.totalPageCount = int(jposresult['totalCount'])/int(jcontent['pageSize']) + 1
        for entry in jresult:
            item['pid'] = entry['positionId']
            item['keyword'] = self.keyword
            for fn in self.item_fns:
                item[fn] = entry[fn]
                yield item

        if self.curPage <= self.totalPageCount:
            self.curPage += 1
            yield scrapy.http.FormRequest(
                self.positionUrl,
                formdata = {
                    'pn': str(self.curPage),
                    'kd': self.keyword,
                    'city': self.city},
                headers=self.headers,
                callback=self.parse)
        elif self.kd_cur < len(self.keywords)-1:
            self.curPage = 1
            self.totalPageCount = 0
            self.kd_cur += 1
            self.keyword = self.keywords[self.kd_cur]
            yield scrapy.http.FormRequest(
                self.positionUrl,
                headers=self.headers,
                formdata = {
                    'pn': str(self.curPage),
                    'kd': self.keyword,
                    'city': self.city},
                callback=self.parse)
