#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import requests
import time
import urllib
import hashlib


def translate(src, dict_name='youdao', lfrom='zh-ChS', lto='en'):
    dicts = {
        'youdao': _youdao_translate,
        'bing': _bing_translate,
        'google': _google_translate,
        'baidu': _baidu_translate,
    }
    translate_func = dicts.get(dict_name)
    if translate:
        return translate_func(src, lfrom, lto)
    else:
        return src


def _youdao_translate(src, lfrom='AUTO', lto='AUTO'):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'accept':
        "application/json, text/javascript, */*; q=0.01",
        'origin':
        "http://fanyi.youdao.com",
        'x-devtools-emulate-network-conditions-client-id':
        "528ca5f2-f42a-40dc-b8e1-134b4d1f7814",
        'x-requested-with':
        "XMLHttpRequest",
        'user-agent':
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        'content-type':
        "application/x-www-form-urlencoded",
        'dnt':
        "1",
        'referer':
        "http://fanyi.youdao.com/?keyfrom=dict2.index",
        'accept-encoding':
        "gzip, deflate",
        'accept-language':
        "zh-CN,zh;q=0.8,en;q=0.6",
    }
    cli = 'fanyideskweb'
    salt = str(int(time.time() * 1000))
    key = "rY0D^0'nM0}g5Mm1z%1G4"
    sign = hashlib.md5((cli + src + salt + key).encode('utf-8')).hexdigest()
    payload = {
        'action': 'FY_BY_CLICK',
        'client': cli,
        'doctype': 'json',
        'from': lfrom,
        'i': src,
        'keyfrom': 'fanyi.web',
        'salt': salt,
        'sign': sign,
        'smartresult': 'dict',
        'to': lto,
        'typoResult': 'true',
        'version': '2.1',
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    return response.json()


def _baidu_translate(src, lfrom='zh', lto='en'):
    lfrom = lfrom.split('-')[0]
    lto = lto.split('-')[0]
    url = 'http://fanyi.baidu.com/v2transapi'
    payload = {
        'from': lfrom,
        'to': lto,
        'query': src,
        'simple_means_flag': 3,
        'transtype': 'translang'
    }
    response = requests.request("POST", url, data=payload)
    return response.json()['trans_result']['data']


def _bing_translate(src, lfrom='zh-CHS', lto='en'):
    pass


def _google_translate(src, lfrom='zh-CHS', lto='en'):
    pass


if __name__ == '__main__':
    print(translate(u'翻译测试', 'baidu'))
