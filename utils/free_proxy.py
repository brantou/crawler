#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import logging

logger = logging.getLogger(__name__)

def get_html(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36")
    html = urllib2.urlopen(request)
    return html.read()

def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup

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
            if float(latency) < 0.5: # 输出延迟小于0.5秒的代理
                proxy = "%s:%s" % (ip, port)
                proxies.append(proxy)
    except:
        logger.warning("fail to fetch from kxdaili")
    return proxies

def img2port(img_url):
    """
    http://proxy.mimvp.com 的端口号用图片来显示, 本函数将图片url映射到端口
    """
    code = img_url.split("=")[-1]
    if code.find("4vMpAO0OO0O")>0:
        return 80
    elif code.find("4vMpQO0OO0O")>0:
        return 81
    elif code.find("zvMpTI4")>0:
        return 3128
    elif code.find("4vMpDgw")>0:
        return 8080
    elif code.find("4vOpDg4")>0:
        return 8088
    elif code.find("4vMpDg5")>0:
        return 8089
    elif code.find("4vMpTE4")>0:
        return 8118
    elif code.find("4vMpTIz")>0:
        return 8123
    elif code.find("4vOpDg4")>0:
        return 8888
    elif code.find("5vMpDAw")>0:
        return 9000
    else:
        return None

def fetch_mimvp():
    """
    从http://proxy.mimvp.com/free.php 抓免费代理
    """
    proxy_types = ["in_tp", "in_hp"]
    sort_fns = ["", "p_transfer", "p_ping"]
    proxies = []
    try:
        for proxy_type in proxy_types:
            for sort_fn in sort_fns:
                url = "http://proxy.mimvp.com/free.php?proxy="+ proxy_type
                url += "&sort=" + sort_fn
                soup = get_soup(url)
                table = soup.find("div", attrs={"class": "free-list"}).table
                tds = table.tbody.find_all("td")
                for i in range(0, len(tds), 10):
                    ip = tds[i+1].text
                    port = img2port(tds[i+2].img["src"])
                    protocal_types = tds[i+3]["title"].split("/")
                    response_time = tds[i+7]["title"][:-1]
                    transport_time = tds[i+8]["title"][:-1]
                    if "HTTP" in protocal_types \
                       and port is not None \
                       and float(response_time) < 1 :
                        proxy = "%s:%s" % (ip, port)
                        proxies.append(proxy)
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
            if float(speed) < 3 and float(latency) < 1:
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
            latency = tds[4].text[:-2]
            if float(latency) < 1:
                proxies.append("%s:%s" % (ip, port))
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
                if type == u"匿名":
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
        url = "http://www.data5u.com/free/gngn/index.shtml"
        soup = get_soup(url)
        div = soup.find("div", attrs={"class": "wlist"})
        uls = div.find_all("ul", attrs={"class":"l2"})
        for ul in uls:
            spans = ul.find_all("span")
            ip = spans[0].li.text
            port = spans[1].li.text
            protocal_types = spans[3].li.text.split(",")
            response_time = spans[7].li.text[:-2]
            if float(response_time) < 0.5:
                proxy = "%s:%s" % (ip, port)
                proxies.append(proxy)
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
        soup = get_soup(url)
        div = soup.find("div", attrs={"id":"list"})
        trs = div.table.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            response_time = tds[5].text[:-1]
            if float(response_time) < 0.5:
                proxy = "%s:%s" % (ip,port)
                proxies.append(proxy)
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
        table = soup.find("table", attrs={"class":"table table-bordered table-hover"})
        trs = table.tbody.find_all("tr")
        for i in range (2, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            response_time = tds[4].text.split("/")[0]
            if float(response_time) < 500:
                proxy = "%s:%s" % (ip,port)
                proxies.append(proxy)
    except:
        logger.warning("failed to fetch ip002")
    return proxies

def check(proxy):
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    try:
        response = opener.open(url,timeout=3)
        return response.code == 200 and response.url == url
    except Exception:
        return False

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
    for p in proxies:
        if check(p):
            valid_proxies.append(p)
            print(p)
    return valid_proxies

if __name__ == '__main__':
    import sys
    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    proxies = fetch_all()
    for p in proxies:
        if check(p):
            print(p)
