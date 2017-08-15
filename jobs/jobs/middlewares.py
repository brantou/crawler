# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

class JobsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class ProxyMode:
    CHANGE_EVERY_REQ, RANDOM_EVERY_REQ, RANDOM_ONCE_INIT, CUSTOM_SET = range(4)

class RandomHttpProxyMiddleware(object):
    def __init__(self, crawler):
        self.proxy_index = 0
        self.proxies = []
        self.proxy_mode = crawler.settings.get('PROXY_MODE', ProxyMode.CHANGE_EVERY_REQ)
        self.proxy_file = crawler.settings.get('PROXY_FILE')
        self.chosen_proxy = ''
        if self.proxy_file is None:
            raise KeyError('PROXY_FILE setting is missing')
        if !os.path.exists(self.proxy_file):
            raise KeyError('PROXY_FILE not exists')

        if self.proxy_mode == ProxyMode.CUSTOM_SET:
            self.chosen_proxy = crawler.settings.get('CUSTOM_PROXY')
            if self.chosen_proxy:
                raise KeyError('CUSTOM_PROXY setting is missing')
            self.proxies.append(self.chosen_proxy)
            return

        if self.proxy_mode >= ProxyMode.CHANGE_EVERY_REQ and self.proxy_mode <= ProxyMode.RANDOM_ONCE_INIT:
            with open(self.proxy_file, "r") as fd:
                lines = fd.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or self._in_proxies("http://" + line):
                        continue
                    self.proxies.append("http://"  + line)

         if self.proxy_mode == ProxyMode.RANDOM_ONCE_INIT:
             self.chosen_proxy = random.choice(self.proxies)

    def _in_proxyes(self, proxy):
        """
        返回一个代理是否在代理列表中
        """
        for p in self.proxies:
            if proxy == p:
                return True
        return False

    def _remove_proxy(self, proxy):
        self.proxies.remove(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        if len(self.proxies) == 0:
            raise ValueError('All proxies are unusable, cannot proceed')

        proxy_address = None
        if self.proxy_mode == ProxyMode.RANDOM_EVERY_REQ:
            proxy_address = random.choice(self.proxies)
        elif self.proxy_mode == ProxyMode.CHANGE_EVERY_REQ:
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
            proxy_address = self.proxies[self.proxy_index]
        else:
            proxy_address = self.chosen_proxy

        request.meta['proxy'] = proxy_address
        logger.debug('Using proxy <%s>, %d proxies left' % (
                proxy_address, len(self.proxies)))

    def process_response(self, request, response, spider):
        """
        检查response.status,
        根据status是否在允许的状态码中决定是否切换到下一个proxy
        """
        if "proxy" in request.meta.keys():
            logger.debug("%s %s %s" % (request.meta["proxy"], response.status, request.url))
        else:
            logger.debug("None %s %s" % (response.status, request.url))

        # status不是正常的200,
        # 而且不在spider声明的正常爬取过程中可能出现的status列表中,
        # 则认为代理无效, 切换代理
        if response.status != 200 \
                and (not hasattr(spider, "website_possible_httpstatus_list") \
                             or response.status not in spider.website_possible_httpstatus_list):
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return

        if self.proxy_mode >= ProxyMode.CHANGE_EVERY_REQ \
           and self.proxy_mode <= ProxyMode.RANDOM_ONCE_INIT:
            proxy = request.meta['proxy']
            try:
                self._remove_proxy(proxy)
            except:
                pass
            request.meta["exception"] = True

            if self.proxy_mode == ProxyMode.RANDOM_ONCE_INIT:
                self.chosen_proxy = random.choice(self.proxies)

            logger.debug('Removing failed proxy <%s>, %d proxies left' % (
                proxy, len(self.proxies)))
