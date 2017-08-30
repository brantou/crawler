# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2


def get_html(url):
    request = urllib2.Request(url)
    request.add_header(
        'User-Agent',
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    )
    html = urllib2.urlopen(request)
    return html.read()


def get_soup(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    return soup
