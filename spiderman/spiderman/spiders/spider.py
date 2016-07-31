#-*- coding: utf-8 -*-

import logging
import time
import os.path
import re
import scrapy
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider,DropItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
from spiderman.items import Movie
from spiderman import settings
from django.core.paginator import Page
from _mysql import NULL



logger = logging.getLogger(__name__)
timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
basedir = os.path.join(settings.BASEDIR,'%(name)s_%(time)s.csv') 
meta = {
        'splash':{
            'endpoint':'render.html',
            'args':{
                'wait':10,
                'images':1,
                'render_all':1
                }
            }
        }


class Iqiyi(scrapy.Spider):
    """抓取爱奇艺电影"""
    name = 'iqiyi'
    allowed_domains = [
        "iqiyi.com"
    ]
    start_urls = [
        "http://list.iqiyi.com/www/1/-------------4-1-1-iqiyi--.html"
    ]
    
    def parse(self,response):
        for sel in response.xpath('//div[@class="site-piclist_pic"]'):
            item = Movie()
            name = sel.xpath('a/@title').extract()
            desc = sel.xpath('a/@title').extract()
            image = sel.xpath('a/img/@src').extract()
            link = sel.xpath('a/@href').extract()
            albumid = sel.xpath('a/@data-qidanadd-albumid').extract()
            item['name'] = [t.encode('utf-8') for t in name][0]
            item['desc'] = [t.encode('utf-8') for t in desc][0]
            item['image'] = [t.encode('utf-8') for t in image][0]
            item['link'] = [t.encode('utf-8') for t in link][0]
            item['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['utime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['albumid'] = [t.encode('utf-8') for t in albumid][0]
            yield item
        next_page = response.xpath('//a[@data-key="down"]')
        host = "http://list.iqiyi.com"
        if next_page:
            path = response.xpath('//a[@data-key="down"]/@href').extract_first()
            url = host + path
            print url
            yield scrapy.Request(url, self.parse)
            
            
if __name__ == '__main__':
    #定一个爬虫进程，方便在脚本中启动脚本，并可以在一个进程中同时启动多个爬虫
    process = CrawlerProcess(get_project_settings())
    process.crawl(iqiyi)
    process.start()
            
                



        
             