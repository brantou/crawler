# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    salary = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    positionName = scrapy.Field()
    positionAdvantage = scrapy.Field()
    positionLables = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    companyLabelList = scrapy.Field()
    financeStage = scrapy.Field()
    industryField = scrapy.Field()
    industryLables = scrapy.Field()
    district = scrapy.Field()
    isSchoolJob = scrapy.Field()
    jobNature = scrapy.Field()
    keyword = scrapy.Field()
    createTime = scrapy.Field()


class ZhipinItem(scrapy.Item):
    pid = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    salary = scrapy.Field()
    positionName = scrapy.Field()
    positionLables = scrapy.Field()
    companyShortName = scrapy.Field()
    industryField = scrapy.Field()
    financeStage = scrapy.Field()
    companySize = scrapy.Field()


class LiepinItem(scrapy.Item):
    pid = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    salary = scrapy.Field()
    positionName = scrapy.Field()
    industryField = scrapy.Field()
    companyShortName = scrapy.Field()
    companyLabelList = scrapy.Field()


class NeituiItem(scrapy.Item):
    pid = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    salary = scrapy.Field()
    positionName = scrapy.Field()
    companyShortName = scrapy.Field()
    financeStage = scrapy.Field()
