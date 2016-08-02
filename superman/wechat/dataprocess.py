#coding: utf-8

import time
import logging
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 
from django.db import connections, transaction
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('django')


class QueryData(object):
    """django db api """
    def __init__(self):
        super(QueryData, self).__init__()
        self.cursor = connections['test'].cursor()
    
    def movie_data(self):
        """返回电影信息，可优化为配置项"""
        self.cursor.execute("select * from movie order by rand() limit 5")
        return self.cursor

    def joke_data(self):
        """待扩展"""
        pass



class DataPrecess(object):
    """定义了处理cursor返回数据的处理方式"""
    def __init__(self):
        super(DataPrecess, self).__init__()

    @classmethod
    def dictfetchall(cls,cursor):
        '''将cursor查询到的每行数据作为dict元素包含在list中返回'''
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @classmethod
    def namedtuplefetchall(cls,cursor):
        '''将cursor查询到的所有数据作为namedtuple返回'''
        desc = cursor.description   #返回sql中查询的列信息的list
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]


def get_input(req):
    """检验xml入参，并获取接收和发送ID"""
    #logger.info(req.body)
    root = ET.fromstring(req.body)
    devname = root.find('.//ToUserName').text
    username = root.find('.//FromUserName').text    #user open_id
    content = root.find('.//Content').text          #用户输入
    create_time = root.find('.//CreateTime').text   #用户访问时间
    #timestamp = int(time.time())#自定义访问时间
    return dict(fromname=devname, toname=username, createtime=create_time)


def output(req):
    """图文消息出参"""
    xmltemplate = """
        <xml>
        <ToUserName><![CDATA[{0[toname]}]]></ToUserName>
        <FromUserName><![CDATA[{0[fromname]}]]></FromUserName>
        <CreateTime>{0[createtime]}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>5</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{1[0][movie_name]}]]></Title> 
        <Description><![CDATA[{1[0][movie_desc]}]></Description>
        <PicUrl><![CDATA[{1[0][movie_image]}]]></PicUrl>
        <Url><![CDATA[{1[0][movie_link]}]]></Url>
        </item>
        <item>
        <Title><![CDATA[{1[1][movie_name]}]]></Title> 
        <Description><![CDATA[{1[1][movie_desc]}]></Description>
        <PicUrl><![CDATA[{1[1][movie_image]}]]></PicUrl>
        <Url><![CDATA[{1[1][movie_link]}]]></Url>
        </item>
        <item>
        <Title><![CDATA[{1[2][movie_name]}]]></Title> 
        <Description><![CDATA[{1[2][movie_desc]}]></Description>
        <PicUrl><![CDATA[{1[2][movie_image]}]]></PicUrl>
        <Url><![CDATA[{1[2][movie_link]}]]></Url>
        </item>
        <item>
        <Title><![CDATA[{1[3][movie_name]}]]></Title> 
        <Description><![CDATA[{1[3][movie_desc]}]></Description>
        <PicUrl><![CDATA[{1[3][movie_image]}]]></PicUrl>
        <Url><![CDATA[{1[3][movie_link]}]]></Url>
        </item>
        <item>
        <Title><![CDATA[{1[4][movie_name]}]]></Title> 
        <Description><![CDATA[{1[4][movie_desc]}]></Description>
        <PicUrl><![CDATA[{1[4][movie_image]}]]></PicUrl>
        <Url><![CDATA[{1[4][movie_link]}]]></Url>
        </item>
        </Articles>
        </xml>
        """
    try:
        query = QueryData()
        movie_dict = DataPrecess.dictfetchall(query.movie_data())
        logger.info(movie_dict)
        xml = xmltemplate.format(get_input(req), movie_dict)
    except Exception, e:
        logger.error(e)   
    return xml
