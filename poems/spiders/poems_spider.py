# -*- coding: utf-8 -*-
"""
A spider that crawl poems from http://www.gushiwen.org
"""
import scrapy
from scrapy_redis.spiders import RedisSpider

class PoemsSpiderSpider(RedisSpider):
    name = 'poem_urls'
    allowed_domains = ['http://gushiwen.org/']
    # start_urls = ['http://www.gushiwen.org/shiwen/']
    TYPE_START = 15
    TYPE_END = -3

    def parse(self, response):
        # 提取类别
        types = response.css('div.right div:first-child .cont a::text').extract()
        types = types[self.TYPE_START:self.TYPE_END]
        type_links = response.css('div.right div:first-child .cont a::attr(href)').extract()
        type_links = type_links[self.TYPE_START:self.TYPE_END]
        for type, link in zip(types, type_links):
            yield scrapy.http.Request(link, callback=self.parse_a_type_of_poems, dont_filter=True, meta={'type': type})

    def parse_a_type_of_poems(self, response):
        # authors = response.css('.left>.sons span::text').extract()
        # authors = map(lambda author: author[1:-1], authors)
        anchors = response.css('.left>.sons a')
        names = anchors.css('a::text').extract()
        links = anchors.css('a::attr(href)').extract()
        links = map(lambda link: response.urljoin(link), links)
        
        for name, url in zip(names, links):
            yield {
                'type': response.meta['type'],
                'name': name,
                'url': url,
            }