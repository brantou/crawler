# -*- coding: utf-8 -*-
import scrapy
import json
from jobs.items import JobsItem
from urllib import quote


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/']
    positionUrl = 'https://www.lagou.com/jobs/positionAjax.json?'
    totalCount = 0
    pageSize = 0
    curPage = 1

    city = '上海'
    keywords = [
        'APP设计师',
        '.NET',
        'ARM开发',
        'ASP',
        'Android',
        'BD经理',
        'BI工程师',
        'C',
        'C#',
        'C++',
        'CDN',
        'CEO',
        'CFO',
        'CMO',
        'COCOS2D-X',
        'COO',
        'CTO',
        'DB2',
        'DBA其它',
        'DSP开发',
        'Delphi',
        'ETL',
        'F5',
        'FPGA开发',
        'Flash',
        'Flash设计师',
        'Go',
        'HRBP',
        'HRD/HRM',
        'HTML5',
        'Hadoop',
        'Hive',
        'IDC',
        'IT支持',
        'Java',
        'JavaScript',
        'MongoDB',
        'MySQL',
        'Node.js',
        'Oracle',
        'PCB工艺',
        'PHP',
        'Perl',
        'Python',
        'Ruby',
        'SEM',
        'SEO',
        'SQLServer',
        'Shell',
        'U3D',
        'UI设计师',
        'VB',
        'WEB安全',
        'WP',
        'html5',
        'iOS',
        'web前端',
        '专利',
        '主编',
        '交互设计师',
        '交互设计总监',
        '交互设计经理/主管',
        '交易员',
        '产品助理',
        '产品实习生',
        '产品总监',
        '产品经理',
        '产品运营',
        '产品部经理',
        '人事/HR',
        '人力资源',
        '仓储',
        '代理商销售',
        '企业软件其它',
        '会计',
        '全栈工程师',
        '公关总监',
        '内容编辑',
        '内容运营',
        '出纳',
        '分析师',
        '前台',
        '前端开发其它',
        '副主编',
        '副总裁',
        '功能测试',
        '助理',
        '单片机',
        '原画师',
        '合规稽查',
        '后端开发其它',
        '员工关系',
        '品牌公关',
        '品类运营',
        '售前咨询',
        '售前工程师',
        '售后客服',
        '售后工程师',
        '商业数据分析',
        '商务总监',
        '商务渠道',
        '商品经理',
        '商家运营',
        '图像处理',
        '图像识别',
        '培训经理',
        '多媒体设计师',
        '大客户代表',
        '媒介经理',
        '安全专家',
        '实施工程师',
        '审计',
        '客户代表',
        '客服总监',
        '客服经理',
        '射频工程师',
        '嵌入式',
        '市场总监',
        '市场推广',
        '市场策划',
        '市场营销',
        '市场顾问',
        '平面设计师',
        '并购',
        '并购总监',
        '广告协调',
        '广告设计师',
        '律师',
        '性能测试',
        '总助',
        '手机测试',
        '技术合伙人',
        '技术总监',
        '技术经理',
        '投资助理',
        '投资总监',
        '投资经理',
        '投资者关系',
        '投资顾问',
        '招聘',
        '搜索算法',
        '政府关系',
        '数据产品经理',
        '数据仓库',
        '数据分析师',
        '数据挖掘',
        '数据运营',
        '文案策划',
        '文秘',
        '新媒体运营',
        '无线交互设计师',
        '无线产品设计师',
        '机器学习',
        '机器视觉',
        '材料工程师',
        '架构师',
        '模具设计',
        '法务',
        '活动策划',
        '活动运营',
        '测试其它',
        '测试工程师',
        '测试开发',
        '测试总监',
        '测试经理',
        '海外市场',
        '海外运营',
        '淘宝客服',
        '深度学习',
        '清算',
        '渠道销售',
        '游戏制作人',
        '游戏动作',
        '游戏场景',
        '游戏数值策划',
        '游戏测试',
        '游戏特效',
        '游戏界面设计师',
        '游戏策划',
        '游戏角色',
        '游戏运营',
        '灰盒测试',
        '热传导',
        '物流',
        '理财顾问',
        '用户研究员',
        '用户研究总监',
        '用户研究经理/主管',
        '用户运营',
        '电商产品经理',
        '电话销售',
        '电路设计',
        '病毒分析',
        '白盒测试',
        '硬件',
        '硬件交互设计师',
        '硬件开发其它',
        '硬件测试',
        '移动产品经理',
        '移动开发其它',
        '税务',
        '算法工程师',
        '精准推荐',
        '精益工程师',
        '系统安全',
        '系统工程师',
        '系统管理员',
        '系统集成',
        '结算',
        '绩效考核经理',
        '网店运营',
        '网络安全',
        '网络工程师',
        '网络推广',
        '网络营销',
        '网页交互设计师',
        '网页产品经理',
        '网页产品设计师',
        '网页设计师',
        '美术设计师（2D/3D）',
        '自动化',
        '自动化测试',
        '自然语言处理',
        '薪资福利经理',
        '融资',
        '融资总监',
        '行业研究',
        '行政',
        '行政总监/经理',
        '视觉设计师',
        '视觉设计总监',
        '视觉设计经理/主管',
        '记者',
        '设计总监',
        '设计经理/主管',
        '语音识别',
        '财务',
        '财务总监/经理',
        '资产管理',
        '资信评估',
        '运维其它',
        '运维工程师',
        '运维开发工程师',
        '运维总监',
        '运维经理',
        '运营专员',
        '运营总监',
        '运营经理',
        '采购专员',
        '采购总监',
        '采购经理',
        '销售专员',
        '销售助理',
        '销售总监',
        '销售经理',
        '销售顾问',
        '项目助理',
        '项目总监',
        '项目经理',
        '风控',
        '风控总监',
        '驱动开发',
        '高端技术职位其它',
        '黑盒测试',
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
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
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
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503803797; _ga=GA1.2.1475031428.1501230295; LGRID=20170827111636-22b244c2-8ad6-11e7-8f3c-5254005c3644; SEARCH_ID=52d0e756ac5d41b395d4a9e57ab74b72; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20170728162449-adcee15cc85848189cfb891619b80998; LGUID=20170728162451-3a327df6-736e-11e7-b9bc-5254005c3644; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20170807221703-15e8d3a5-7b7b-11e7-839b-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503587852; _ga=GA1.2.1475031428.1501230295; LGRID=20170824231731-59096c0b-88df-11e7-8ea0-5254005c3644; JSESSIONID=ABAAABAACBHABBI1DE966CF9357E8BD2D82C53257584955; X_HTTP_TOKEN=2274185a2011ec03f73ab98f8ceaf490; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1501230293; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503807054; _ga=GA1.2.1475031428.1501230295; LGSID=20170827121054-b83e61a1-8add-11e7-8f3c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2Fheiheceshi%2F%3FlabelWords%3Dlabel; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Go%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20170827121054-b83e632d-8add-11e7-8f3c-5254005c3644; SEARCH_ID=ced77b843c064940a3c12c51d8720ca1",
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        jcontent = jdict['content']
        jposresult = jcontent['positionResult']
        jresult = jposresult['result']
        self.totalCount = int(jposresult['totalCount'])
        self.pageSize = int(jcontent['pageSize'])
        print('[lagou][%s]totalCount: %d, pageNo: %d, pageSize: %d' %
              (self.keyword, int(jposresult['totalCount']), self.curPage,
               int(jcontent['pageSize'])))
        for entry in jresult:
            if len(entry) < 10:
                continue
            item = JobsItem()
            item['pid'] = str(entry['positionId']) + "_" + str(
                entry['publisherId'])
            item['keyword'] = self.keyword
            for fn in self.item_fns:
                item[fn] = entry[fn]

            yield item

        if self.curPage * self.pageSize < self.total:
            self.curPage += 1
            yield self.next_request()
        elif self.kd_cur < len(self.keywords) - 1:
            self.curPage = 1
            self.pageSize = 0
            self.totalCount = 0
            self.kd_cur += 1
            self.keyword = self.keywords[self.kd_cur]
            yield self.next_request()

    def next_request(self):
        self.headers['referer'] = "https://www.lagou.com/jobs/list_" + quote(
            self.keyword
        ) + "?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput="

        return scrapy.http.FormRequest(
            self.positionUrl,
            headers=self.headers,
            formdata={'pn': str(self.curPage),
                      'kd': self.keyword},
            callback=self.parse)
