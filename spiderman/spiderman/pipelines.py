# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from twisted.enterprise import adbapi
import MySQLdb.cursors
import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
logger = logging.getLogger(__name__)


class SpidermanPipeline(object):
    """存储接口"""
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db = 'test',
            host = '123.56.26.7',
            port = 3306,
            user = 'test',
            passwd = 'test',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
            )

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.insert_item,*(item,spider))
        d.addErrback(self.handle_err)
        return d

    def insert_item(self,tx,item,spider):
        logger.info("ready to insert!")
        if spider.name == 'iqiyi':
            #print item
            tx.execute('''insert IGNORE into movie (MOVIE_NAME, MOVIE_DESC, MOVIE_IMAGE, MOVIE_LINK, CREATE_TIME, UPDATE_TIME, ALBUMID) values (%s, %s, %s, %s, %s, %s, %s)''' ,\
            (item['name'], item['desc'],item['image'],item['link'],item['ctime'],item['utime'], item['albumid']))
        logger.info("insert complete!")

    def handle_err(self,e):
        logger.error(e)
