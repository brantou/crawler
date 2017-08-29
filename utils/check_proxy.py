#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib2
import json
from ip_info import get_local_ip


def check_gn_proxy(proxy, protocal_type='HTTP'):
    url = 'http://icanhazip.com'
    proxy_handler = urllib2.ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    })
    if protocal_type == 'HTTPS':
        url = 'https://icanhazip.com'

    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url, timeout=3)
        res_ip = response.read().strip()
        return response.code == 200 and res_ip == proxy.split(':')[0]
    except Exception:
        return False


def check_baidu(proxy):
    url = 'http://www.baidu.com/js/bdsug.js?v=1.0.3.0'
    proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy})
    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url, timeout=3)
        return response.code == 200 and response.url == url
    except Exception:
        return False


def check_proxy(self_ip, proxy, protocal_type='HTTP'):
    proxy_type = ''
    url = 'http://httpbin.org/get'
    proxy_handler = urllib2.ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    })
    if protocal_type == 'HTTPS':
        url = 'https://httpbin.org/get'

    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url, timeout=3)
        if response.code == 200:
            content = json.loads(response.read().strip())
            headers = content['headers']
            ip = content['origin']
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                proxy_type = 'anoy_l'
            elif proxy_connection:
                proxy_type = 'anoy_n'
            else:
                proxy_type = 'anoy_h'

            return True, proxy_type
        else:
            return False, proxy_type
    except Exception:
        return False, proxy_type


if __name__ == '__main__':
    local_ip = get_local_ip()
    with open('proxies.dat', 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            line = line.strip()
            print(line, check_proxy(local_ip, line))
