# -*- coding: utf-8 -*-
import scrapy
import json


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['http://job.alibaba.com/']
    positionUrl = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'

    totalPage = 0
    pageIndex = 1
    pageSize = 10

    headers = {
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'origin':
        "https://job.alibaba.com",
        'x-requested-with':
        "XMLHttpRequest",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'dnt':
        "1",
        'referer':
        "https://job.alibaba.com/zhaopin/positionList.htm",
        'accept-encoding':
        "gzip, deflate, br",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie':
        "t=529c8a503c4336e01b42feef6f83d119; l=AnFxKAqEPjdNM3MIITAEY4zxAfYL2eXQ; JSESSIONID=EF6YIY4TL2-7GCNTAN0RH2ADYMMYZPO1-GWINI66J-RC1; v=0; cookie2=10162fd762f07ec9868258352ec3b968; _tb_token_=38e8f4131885e; cna=1OZ3DwF+cCECAbSnFDrpAFUK; _hvn_login=\"0,3\"; csg=0621b2b2; tmp0=A8VbiiV6ijcmBnjzDMLAxE%2FtS8iw7Ec3Y2YidZMZnatOZrndjC1dQxWsjSK2ga342M5K0mnkkshYcNBo0yCujiGkEsG6mUZ%2FyU5hV4R0yvvwrHubcTekAR8hMSGmMPE56sC9Y0v48PZ0ODXG36UR5VuPFWLflgZESq0TJ4a4z0CcmyhlQNCArRk3ik4zIj%2B5EgaQ%2FEyDiCKKzVtFBCDikTJpHkHMBUMbrYzWTz3%2BO2vShVV1Xml8ZaJoL7EEc7T3oekuv87k75y1k79tgvIyLw%3D%3D; isg=Are3WpCaohZAUCYJslICxM7fRq0LcIfUpu2mIwlkVgbtuNT6EExmL2XY5C4d; t=529c8a503c4336e01b42feef6f83d119; l=AnFxKAqEPjdNM3MIITAEY4zxAfYL2eXQ; JSESSIONID=EF6YIY4TL2-7GCNTAN0RH2ADYMMYZPO1-GWINI66J-RC1; v=0; cookie2=10162fd762f07ec9868258352ec3b968; _tb_token_=38e8f4131885e; cna=1OZ3DwF+cCECAbSnFDrpAFUK; _hvn_login=\"0,3\"; csg=0621b2b2; tmp0=A8VbiiV6ijcmBnjzDMLAxE%2FtS8iw7Ec3Y2YidZMZnatOZrndjC1dQxWsjSK2ga342M5K0mnkkshYcNBo0yCujiGkEsG6mUZ%2FyU5hV4R0yvvwrHubcTekAR8hMSGmMPE56sC9Y0v48PZ0ODXG36UR5VuPFWLflgZESq0TJ4a4z0CcmyhlQNCArRk3ik4zIj%2B5EgaQ%2FEyDiCKKzVtFBCDikTJpHkHMBUMbrYzWTz3%2BO2vShVV1Xml8ZaJoL7EEc7T3oekuv87k75y1k79tgvIyLw%3D%3D; isg=Are3WpCaohZAUCYJslICxM7fRq0LcIfUpu2mIwlkVgbtuNT6EExmL2XY5C4d",
        'cache-control':
        "no-cache",
        'postman-token':
        "cdec794f-9f94-ffb0-ef52-a66a06c561b9"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        jdict = json.loads(response.body)
        jreturnVal = jdict['returnValue']
        self.totalPage = int(jreturnVal['totalPage'])
        jdatas = jreturnVal['datas']
        for entry in jdatas:
            item = {}
            item['pid'] = entry['id']
            for key in entry:
                item[key] = entry[key]
            yield item

        self.pageIndex += 1
        if self.pageIndex <= self.totalPage:
            yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            url=self.positionUrl,
            method='POST',
            headers=self.headers,
            formdata={
                'pageIndex': str(self.pageIndex),
                'pageSize': str(self.pageSize),
            },
            callback=self.parse)
