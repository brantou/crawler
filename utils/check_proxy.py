#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2

def check_gn_proxy(proxy, protocal_type='HTTP'):
    url = "http://icanhazip.com"
    proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    if protocal_type == "HTTPS":
        proxy_handler = urllib2.ProxyHandler({'https': "https://" + proxy})
        url = "https://icanhazip.com"

    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    try:
        response = opener.open(url,timeout=3)
        res_ip = response.read().strip()
        return response.code == 200 and res_ip == proxy.split(":")[0]
    except Exception:
        return False

if __name__ == '__main__':
    print(check_gn_proxy("183.169.128.30:80"))
    print(check_gn_proxy("183.222.102.104:8080"))

