#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
from bs4 import BeautifulSoup
from ip_info import get_local_ip
from check_proxy import check_proxy
from util import get_html, get_soup

logger = logging.getLogger(__name__)

postman_headers = {
    "Cache-Control":
    "no-cache",
    "X-Postman-Interceptor-Id":
    "ef2745b4-246d-8362-b6f7-bd2ef45dd910",
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Postman-Token":
    "534b6064-fc3e-c577-da27-fefeca24346b",
    "Accept":
    "*/*",
    "DNT":
    "1",
    "Accept-Encoding":
    "gzip, deflate",
    "Accept-Language":
    "zh-CN,zh;q=0.8,en;q=0.6",
    "Cookie":
    "auth=2e7ac706e8461dd98bb679502951b17b; JSESSIONID=C6550B3EB31544825D03BC5A8EB60EFA; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1502597177; Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1502767721; auth=2e7ac706e8461dd98bb679502951b17b; JSESSIONID=C55C93B915D81D5ED6082F0C0C492E80; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1502597177; Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1502789892",
}


def _filter_proxy(resp_time, proxy):
    if resp_time < 0.5:
        return [proxy]
    else:
        return []


def fetch_kxdaili(page):
    """
    从http://www.kxdaili.com抓取免费代理
    """
    proxies = []
    try:
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % page
        soup = get_soup(url)
        table_tag = soup.find("table", attrs={"class": "segment"})
        trs = table_tag.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text.split(" ")[0]
            proxy = "%s:%s" % (ip, port)
            proxies += _filter_proxy(float(latency), proxy)
    except:
        logger.warning("fail to fetch from kxdaili")
    return proxies


def img2port(img_url):
    """
    http://proxy.mimvp.com 的端口号用图片来显示,
    本函数将图片url映射到端口
    """
    url2port = {
        "4vMpAO0OO0O": 80,
        "4vMpQO0OO0O": 81,
        "zvMpTI4": 3128,
        "4vMpDgw": 8080,
        "4vOpDg4": 8088,
        "4vMpDg5": 8089,
        "4vMpTE4": 8118,
        "4vMpTIz": 8123,
        "4vOpDg4": 8888,
        "5vMpDAw": 9000,
    }
    code = img_url.split("=")[-1]
    for k in url2port:
        if code.find(k) > 0:
            return url2port[k]
    return None


def fetch_mimvp():
    """
    从http://proxy.mimvp.com/free.php 抓免费代理
    """
    querys = [
        "proxy=in_tp",
        "proxy=in_hp",
        "proxy=in_tp&sort=p_transfer",
        "proxy=in_hp&sort=p_transfer",
        "proxy=in_tp&sort=p_ping",
        "proxy=in_hp&sort=p_ping",
    ]
    proxies = []
    try:
        for query in querys:
            url = "http://proxy.mimvp.com/free.php?%s" % (query)
            soup = get_soup(url)
            table = soup.find("div", attrs={"class": "free-list"}).table
            tds = table.tbody.find_all("td")
            for i in range(0, len(tds), 10):
                ip = tds[i + 1].text
                port = img2port(tds[i + 2].img["src"])
                protocal_types = tds[i + 3]["title"].split("/")
                response_time = tds[i + 7]["title"][:-1]
                transport_time = tds[i + 8]["title"][:-1]
                proxy = "%s:%s" % (ip, port)
                if port is not None:
                    proxies += _filter_proxy(float(response_time), proxy)
    except:
        logger.warning("fail to fetch from mimvp")
    return proxies


def fetch_xici():
    """
    http://www.xicidaili.com/nn/
    """
    proxies = []
    try:
        url = "http://www.xicidaili.com/wt/"
        soup = get_soup(url)
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            speed = tds[6].div["title"][:-1]
            latency = tds[7].div["title"][:-1]
            if float(speed) < 0.5 and float(latency) < 1.0:
                proxies.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxies


def fetch_ip181():
    """
    http://www.ip181.com/
    """
    proxies = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            response_time = tds[4].text[:-2]
            proxy = "%s:%s" % (ip, port)
            proxies += _filter_proxy(float(response_time), proxy)
    except Exception as e:
        logger.warning("fail to fetch from ip181: %s" % e)
    return proxies


def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁
    """
    proxies = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"}).table
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                proxies.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxies


def fetch_66ip():
    """
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxies = []
    try:
        # 修改getnum大小可以一次获取不同数量的代理
        url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        content = get_html(url)
        urls = content.split("</script>")[-1].split("<br />")
        for u in urls:
            if u.strip():
                proxies.append(u.strip())
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxies


def fetch_data5u():
    """
    http://www.data5u.com/
    """
    proxies = []
    try:
        url = "http://www.data5u.com/free/anoy/%E9%AB%98%E5%8C%BF/index.html"
        response = requests.request("GET", url, headers=postman_headers)
        soup = BeautifulSoup(response.text, "lxml")
        div = soup.find("div", attrs={"class": "wlist"})
        uls = div.find_all("ul", attrs={"class": "l2"})
        for ul in uls:
            spans = ul.find_all("span")
            ip = spans[0].li.text
            port = spans[1].li.text
            protocal_types = spans[3].li.text.split(",")
            response_time = spans[7].li.text[:-2]
            proxy = "%s:%s" % (ip, port)
            proxies += _filter_proxy(float(response_time), proxy)
    except:
        logger.warning("failed to fetch from data5u")
    return proxies


def fetch_kdaili(page=1):
    """
    http://www.kuaidaili.com/
    """
    proxies = []
    try:
        url = "http://www.kuaidaili.com/free/inha/%d/" % page
        response = requests.request("GET", url, headers=postman_headers)
        soup = BeautifulSoup(response.text, "lxml")
        div = soup.find("div", attrs={"id": "list"})
        trs = div.table.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            response_time = tds[5].text[:-1]
            proxy = "%s:%s" % (ip, port)
            proxies += _filter_proxy(float(response_time), proxy)
    except:
        logger.warning("failed to fetch kuaidaili")
    return proxies


def fetch_ip002(page=1):
    """
    http://www.ip002.net/free.html
    """
    proxies = []
    try:
        url = "http://www.ip002.net/free_%d.html" % page
        soup = get_soup(url)
        table = soup.find(
            "table", attrs={"class": "table table-bordered table-hover"})
        trs = table.tbody.find_all("tr")
        for i in range(2, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            response_time = tds[4].text.split("/")[0]
            proxy = "%s:%s" % (ip, port)
            proxies += _filter_proxy(float(response_time) / 1000.00, proxy)
    except:
        logger.warning("failed to fetch ip002")
    return proxies


def fetch_all(endpage=2):
    proxies = []
    for i in range(1, endpage):
        proxies += fetch_kxdaili(i)
    proxies += fetch_mimvp()
    proxies += fetch_xici()
    proxies += fetch_ip181()
    proxies += fetch_httpdaili()
    proxies += fetch_66ip()
    proxies += fetch_ip002()
    proxies += fetch_data5u()
    proxies += fetch_kdaili()
    valid_proxies = []
    logger.info("checking proxies validation")
    self_ip = get_local_ip()
    for p in proxies:
        bEnable, proxy_type = check_proxy(self_ip, p)
        print(p, bEnable, proxy_type)
        if bEnable and proxy_type == "anoy_h":
            valid_proxies.append(p)
    return valid_proxies


if __name__ == '__main__':
    import sys
    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(name)-8s %(asctime)s %(levelname)-8s %(message)s',
        '%a, %d %b %Y %H:%M:%S', )
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    proxies = fetch_all()
    with open("proxies.dat", "w") as fd:
        for proxy in proxies:
            fd.write(proxy + "\n")
