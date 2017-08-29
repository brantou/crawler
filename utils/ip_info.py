#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import xml.sax


class IpHandler(xml.sax.ContentHandler):
    fns = [
        'ip', 'host', 'isp', 'city', 'countrycode', 'countryname', 'latitude',
        'longitude'
    ]

    def __init__(self):
        self.ip_info = {}
        self._curTag = ''

    def startElement(self, tag, attributes):
        self._curTag = tag

    def endElement(self, tag):
        self._curTag = ''

    def characters(self, content):
        if self._curTag in self.fns:
            self.ip_info[self._curTag] = content


def get_ip_info(ip=''):
    url = 'http://api.geoiplookup.net/'
    if ip != '':
        url += '?query=' + ip
    response = requests.request('GET', url)
    Handler = IpHandler()
    xml.sax.parseString(response.text, Handler)
    return Handler.ip_info


def get_local_ip():
    url = 'http://icanhazip.com'
    response = requests.request('GET', url)
    return response.text


if (__name__ == '__main__'):
    print(get_ip_info())
    print(get_ip_info('8.8.8.8'))
