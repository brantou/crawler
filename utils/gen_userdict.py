#!/usr/bin/python
# -*- coding: utf-8 -*-

from util import get_html, get_soup


def fetch_lagou():
    words = []
    url = 'https://www.lagou.com/'
    soup = get_soup(url)
    category_list = soup.find_all('div', attrs={'class': 'menu_sub dn'})
    for category in category_list:
        dls = category.find_all('dl')
        for dl in dls:
            names = dl.dd.find_all('a')
            for name in names:
                words.append(name.text)
    return words


def fetch_zhipin():
    words = []
    url = 'http://www.zhipin.com/'
    soup = get_soup(url)
    job_menu = soup.find('div', attrs={'class': 'job-menu'})
    dls = job_menu.find_all('dl')
    for dl in dls:
        divs = dl.find_all('div', attrs={'class': 'text'})
        for div in divs:
            names = div.find_all('a')
            for name in names:
                words.append(name.text)
    return words


def fetch_stackoverflow():
    words = []
    for pageNo in range(1, 20):
        url = 'https://stackoverflow.com/tags?page=%d&tab=popular' % (pageNo)
        soup = get_soup(url)
        tags_list = soup.find('div', attrs={'id': 'tags_list'})
        trs = tags_list.table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                words.append(td.a.text)
    return words


if __name__ == '__main__':
    words = []
    words += fetch_zhipin()
    words += fetch_lagou()
    words += fetch_stackoverflow()
    word_set = set()
    for word in words:
        if len(word.split('/')) > 1 or len(word.split('.')) > 1:
            continue
        if len(word.split('-')) > 1:
            word = word.split('-')[0]
        word = word.replace(' ', '')
        if word not in word_set:
            word_set.add(word)

    with open('userdict.txt', 'w') as fd:
        for word in word_set:
            fd.write(word.encode('utf8'))
            fd.write(' ' + str(len(word)))
            fd.write(' nz')
            fd.write('\n')
