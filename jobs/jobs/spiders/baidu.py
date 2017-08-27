# -*- coding: utf-8 -*-
import scrapy
import json


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['talent.baidu.com']
    start_urls = ['http://talent.baidu.com/']
    positionUrl = "http://talent.baidu.com/baidu/web/httpservice/getPostList"

    totalPage = 0
    recruitType = 2
    pageSize = 10
    curPage = 1

    headers = {
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'x-requested-with':
        "XMLHttpRequest",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'dnt':
        "1",
        'accept-encoding':
        "gzip, deflate",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "BAIDUID=FAE9252DF96BB3DAF785BE2846F0A31F:FG=1; PSTM=1501399369; BIDUPSID=BD873B7587D2FA50DA131FAC245AE819; hjstat_uv=2401439942895123570|679544; hjstat_ss=1116366304_1_1501676181_679544; pgv_pvi=8749803520; pgv_si=s515303424; BCLID=11578152906496802351; BDSFRCVID=k9KsJeC62xKf5gbZZckyUO0ZHe2j9VoTH6aV-F3ry_LzMCf-JQk2EG0Pqx8g0KubhTWsogKK0eOTHvTP; H_BDCLCKID_SF=tJPHoDI-JKL3j-bmKKT0M-FD-q5t546B2C6XsJOOaCk2VljRy4oTj6jBj-KjQ-Rzyec7Wf5vtUc1efjDefno3MvB-fnjBxKjbKTUXCnyfCOJoDblQft20b_beMtjBbQa2n4HKb7jWhk2eq72ybjx05TXDG0Oq6_jJn3fL-085njMHD5Gq4bohjP1LlOeBtQmJJrC2MO5yDOAoROGLqocDhInbJQlqxRyQg-q3R76QDjVqb5D5RoA0xtIXn080x-jLT6uVn0MW-5Dobjz5PnJyUnQbtnnBn5nLnLH_I_-fC_bMCv65nt_24kthfQH-4oX2D5KWjrJabC3sb5eKU6qLT5Xj45ea4jqyHQ2QDTGBKJAObKGD-nZ3h0njxQy2h3hWKrX0h6mJ4nDqPjJyfonDh8L2a7MJUntKD-joq3O5hvvhb5O3M7-3hOhDG8Ht6kJJJKsLnjVMRj_ePoG-tT8Mt_Hqxby26nnHm6eaJ5nJDoWOnL4XToAW4tXQRo9JpT75RIjWMTmQpP-HJAzKRb1QjFDXp5pWCrZL6RCKl0MLPjWbb0xynoDMh0iKUnMBMPj5mOnaPQmLIFahIPlDjK5ePtjhpobetjK2CntsJOOaCvEMt5Ry4oTj6Dd3R5QBR5zyD7W2U5vtUc1eqvjy-Ab3MvB-JjZ3bJkJjcWQITq2RQ6MRovQft20b_beMtjBbLLLbuOKJ7jWhk2eq72ybjx05TXjaKtqT0qfR3J3RTXKRrJq45ph46E-t6H-UnLq-P8W57Z0l8KttnveC5T-l6A-PP-3tPjXfv-tDL8-J7mWIQHS66DDn5BBUAhXtbhexTI2br4KKJx-4PWeIJo5t5s3h-yhUJiB5O-Ban7LfbxfJOKHICwj5tM3e; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; H_PS_PSSID=1450_21116_17001_20719; cflag=15%3A3; locale=zh; BDUSS=0tUzYxOTVyRkpzMnJyaExwWXVWQkVlS3ZMVDVzcX5aUjZxUkFLUllYR3BjbXhaSVFBQUFBJCQAAAAAAAAAAAEAAABTYownb3lzbGJveQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKnlRFmp5URZYm; JSESSIONID=4BB28E4A28B1042596B8093C956799D8.dayee-client4; CCK=rO0ABXNyABRqYXZhLnNlY3VyaXR5LktleVJlcL35T7OImqVDAgAETAAJYWxnb3JpdGhtdAASTGphdmEvbGFuZy9TdHJpbmc7WwAHZW5jb2RlZHQAAltCTAAGZm9ybWF0cQB%2BAAFMAAR0eXBldAAbTGphdmEvc2VjdXJpdHkvS2V5UmVwJFR5cGU7eHB0AANERVN1cgACW0Ks8xf4BghU4AIAAHhwAAAACJI00Kvv40mUdAADUkFXfnIAGWphdmEuc2VjdXJpdHkuS2V5UmVwJFR5cGUAAAAAAAAAABIAAHhyAA5qYXZhLmxhbmcuRW51bQAAAAAAAAAAEgAAeHB0AAZTRUNSRVQ%3D; Hm_lvt_50e85ccdd6c1e538eb1290bc92327926=1503237950,1503237964,1503237988,1503238030; Hm_lpvt_50e85ccdd6c1e538eb1290bc92327926=1503238030",
        'cache-control':
        "no-cache",
        'postman-token':
        "c85bef54-f093-c226-5171-b62bdbff5cd3"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        self.totalPage = int(jdict['totalPage'])
        jdatas = jdict['postList']
        for entry in jdatas:
            entry['pid'] = entry['postId']
            yield entry

        if self.curPage < self.totalPage:
            self.curPage += 1
            yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='GET',
            headers=self.headers,
            formdata={
                'curPage': str(self.curPage),
                'pageSize': str(self.pageSize),
                'recruitType ': str(self.recruitType),
            },
            callback=self.parse)
