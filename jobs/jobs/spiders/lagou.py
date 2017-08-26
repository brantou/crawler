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
    #keywords = [
    #    u'大数据', u'云计算', u'docker', u'中间件', 'Node.js', u'数据挖掘', u'自然语言处理',
    #    u'搜索算法', u'精准推荐', u'全栈工程师', u'图像处理', u'机器学习', u'语音识别'
    #]
    keywords = [
        u'.NET',
        u'APP设计师',
        u'ARM开发',
        u'ASP',
        u'Android',
        u'BD经理',
        u'BI工程师',
        u'C',
        u'C#',
        u'C++',
        u'CDN',
        u'CEO',
        u'CFO',
        u'CMO',
        u'COCOS2D-X',
        u'COO',
        u'CTO',
        u'DB2',
        u'DBA其它',
        u'DSP开发',
        u'Delphi',
        u'ETL',
        u'F5',
        u'FPGA开发',
        u'Flash',
        u'Flash设计师',
        u'Go',
        u'HRBP',
        u'HRD/HRM',
        u'HTML5',
        u'Hadoop',
        u'Hive',
        u'IDC',
        u'IT支持',
        u'Java',
        u'JavaScript',
        u'MongoDB',
        u'MySQL',
        u'Node.js',
        u'Oracle',
        u'PCB工艺',
        u'PHP',
        u'Perl',
        u'Python',
        u'Ruby',
        u'SEM',
        u'SEO',
        u'SQLServer',
        u'Shell',
        u'U3D',
        u'UI设计师',
        u'VB',
        u'WEB安全',
        u'WP',
        u'html5',
        u'iOS',
        u'web前端',
        u'专利',
        u'主编',
        u'交互设计师',
        u'交互设计总监',
        u'交互设计经理/主管',
        u'交易员',
        u'产品助理',
        u'产品实习生',
        u'产品总监',
        u'产品经理',
        u'产品运营',
        u'产品部经理',
        u'人事/HR',
        u'人力资源',
        u'仓储',
        u'代理商销售',
        u'企业软件其它',
        u'会计',
        u'全栈工程师',
        u'公关总监',
        u'内容编辑',
        u'内容运营',
        u'出纳',
        u'分析师',
        u'前台',
        u'前端开发其它',
        u'副主编',
        u'副总裁',
        u'功能测试',
        u'助理',
        u'单片机',
        u'原画师',
        u'合规稽查',
        u'后端开发其它',
        u'员工关系',
        u'品牌公关',
        u'品类运营',
        u'售前咨询',
        u'售前工程师',
        u'售后客服',
        u'售后工程师',
        u'商业数据分析',
        u'商务总监',
        u'商务渠道',
        u'商品经理',
        u'商家运营',
        u'图像处理',
        u'图像识别',
        u'培训经理',
        u'多媒体设计师',
        u'大客户代表',
        u'媒介经理',
        u'安全专家',
        u'实施工程师',
        u'审计',
        u'客户代表',
        u'客服总监',
        u'客服经理',
        u'射频工程师',
        u'嵌入式',
        u'市场总监',
        u'市场推广',
        u'市场策划',
        u'市场营销',
        u'市场顾问',
        u'平面设计师',
        u'并购',
        u'并购总监',
        u'广告协调',
        u'广告设计师',
        u'律师',
        u'性能测试',
        u'总助',
        u'手机测试',
        u'技术合伙人',
        u'技术总监',
        u'技术经理',
        u'投资助理',
        u'投资总监',
        u'投资经理',
        u'投资者关系',
        u'投资顾问',
        u'招聘',
        u'搜索算法',
        u'政府关系',
        u'数据产品经理',
        u'数据仓库',
        u'数据分析师',
        u'数据挖掘',
        u'数据运营',
        u'文案策划',
        u'文秘',
        u'新媒体运营',
        u'无线交互设计师',
        u'无线产品设计师',
        u'机器学习',
        u'机器视觉',
        u'材料工程师',
        u'架构师',
        u'模具设计',
        u'法务',
        u'活动策划',
        u'活动运营',
        u'测试其它',
        u'测试工程师',
        u'测试开发',
        u'测试总监',
        u'测试经理',
        u'海外市场',
        u'海外运营',
        u'淘宝客服',
        u'深度学习',
        u'清算',
        u'渠道销售',
        u'游戏制作人',
        u'游戏动作',
        u'游戏场景',
        u'游戏数值策划',
        u'游戏测试',
        u'游戏特效',
        u'游戏界面设计师',
        u'游戏策划',
        u'游戏角色',
        u'游戏运营',
        u'灰盒测试',
        u'热传导',
        u'物流',
        u'理财顾问',
        u'用户研究员',
        u'用户研究总监',
        u'用户研究经理/主管',
        u'用户运营',
        u'电商产品经理',
        u'电话销售',
        u'电路设计',
        u'病毒分析',
        u'白盒测试',
        u'硬件',
        u'硬件交互设计师',
        u'硬件开发其它',
        u'硬件测试',
        u'移动产品经理',
        u'移动开发其它',
        u'税务',
        u'算法工程师',
        u'精准推荐',
        u'精益工程师',
        u'系统安全',
        u'系统工程师',
        u'系统管理员',
        u'系统集成',
        u'结算',
        u'绩效考核经理',
        u'网店运营',
        u'网络安全',
        u'网络工程师',
        u'网络推广',
        u'网络营销',
        u'网页交互设计师',
        u'网页产品经理',
        u'网页产品设计师',
        u'网页设计师',
        u'美术设计师（2D/3D）',
        u'自动化',
        u'自动化测试',
        u'自然语言处理',
        u'薪资福利经理',
        u'融资',
        u'融资总监',
        u'行业研究',
        u'行政',
        u'行政总监/经理',
        u'视觉设计师',
        u'视觉设计总监',
        u'视觉设计经理/主管',
        u'记者',
        u'设计总监',
        u'设计经理/主管',
        u'语音识别',
        u'财务',
        u'财务总监/经理',
        u'资产管理',
        u'资信评估',
        u'运维其它',
        u'运维工程师',
        u'运维开发工程师',
        u'运维总监',
        u'运维经理',
        u'运营专员',
        u'运营总监',
        u'运营经理',
        u'采购专员',
        u'采购总监',
        u'采购经理',
        u'销售专员',
        u'销售助理',
        u'销售总监',
        u'销售经理',
        u'销售顾问',
        u'项目助理',
        u'项目总监',
        u'项目经理',
        u'风控',
        u'风控总监',
        u'驱动开发',
        u'高端技术职位其它',
        u'黑盒测试',
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
            if len(entry) < 10:
                continue
            item = JobsItem()
            item['pid'] = self.keyword + str(entry['positionId']) + "_" + str(
                entry['publisherId'])
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
