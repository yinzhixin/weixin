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

class ObjectDict(dict):
    """类字典对象，属性操作"""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
        
    def __setattr__(self, name, value):
        self[name] = value
        

class DatabaseProcess(object):
    """django db api """
    def __init__(self):
        super(DatabaseProcess, self).__init__()
        self.cursor = connections['test'].cursor()
    
    def get_movie_data(self, num=5):
        """返回电影信息，可优化为配置项"""
        self.cursor.execute("select * from movie order by rand() limit %s" % num)
        return DataTranform.dictfetchall(self.cursor)

    def get_joke_data(self):
        """待扩展"""
        pass

    def insert_user(self,*data):
        sql = '''
        INSERT INTO user 
        (open_id, input_content, req_ip, create_time, last_time) 
        VALUES
        %s''' % data
        self.cursor.execute(sql)      

    def insert_movie_user(self, *data):
        sql = '''
        INSERT INTO user_movie_rel
        (open_id, movie_id, create_time)
        VALUES
        %s''' % data
        self.cursor.execute(sql)


class DataTranform(object):
    """定义了处理cursor返回数据的处理方式"""
    def __init__(self):
        super(DataTranform, self).__init__()

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

def encode_str(text, code='utf-8'):
    text.encode(code)
    return text

def curtime(format='%Y-%m-%d %H:%M:%S'):
    current_time = time.strftime(format, time.localtime())
    return current_time

class Interface_Data_Process(object):
    """处理微信接口的入参与出参"""
    def __init__(self, arg):
        super(Interface_Data_Process, self).__init__()

    @classmethod      
    def get_input(cls, req):
        """获取用户信息"""
        user = ObjectDict()
        root = ET.fromstring(req.body)
        user.devname = root.find('.//ToUserName').text
        user.username = root.find('.//FromUserName').text    #user open_id
        user.content = root.find('.//Content').text    #用户输入
        logger.info("type of content:%s" % type(user.content))
        #content = root.find('.//Content').text.encode('utf-8')
        #logger.info("type of content:%s" % type(content) + content)
        user.create_time = root.find('.//CreateTime').text   #用户访问时间
        user.req_ip = req.META.get('REMOTE_ADDR', None)
        user.current_time = curtime() 
        return user

    @classmethod
    def output(cls, req):
        """图文消息出参"""
        xmltemplate = """
            <xml>
            <ToUserName><![CDATA[{0[username]}]]></ToUserName>
            <FromUserName><![CDATA[{0[devname]}]]></FromUserName>
            <CreateTime>{0[create_time]}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>5</ArticleCount>
            <Articles>
            <item>
            <Title><![CDATA[{1[0][movie_name]}]]></Title> 
            <Description><![CDATA[{1[0][movie_desc]}]]></Description>
            <PicUrl><![CDATA[{1[0][movie_image]}]]></PicUrl>
            <Url><![CDATA[{1[0][movie_link]}]]></Url>
            </item>
            <item>
            <Title><![CDATA[{1[1][movie_name]}]]></Title> 
            <Description><![CDATA[{1[1][movie_desc]}]]></Description>
            <PicUrl><![CDATA[{1[1][movie_image]}]]></PicUrl>
            <Url><![CDATA[{1[1][movie_link]}]]></Url>
            </item>
            <item>
            <Title><![CDATA[{1[2][movie_name]}]]></Title> 
            <Description><![CDATA[{1[2][movie_desc]}]]></Description>
            <PicUrl><![CDATA[{1[2][movie_image]}]]></PicUrl>
            <Url><![CDATA[{1[2][movie_link]}]]></Url>
            </item>
            <item>
            <Title><![CDATA[{1[3][movie_name]}]]></Title> 
            <Description><![CDATA[{1[3][movie_desc]}]]></Description>
            <PicUrl><![CDATA[{1[3][movie_image]}]]></PicUrl>
            <Url><![CDATA[{1[3][movie_link]}]]></Url>
            </item>
            <item>
            <Title><![CDATA[{1[4][movie_name]}]]></Title> 
            <Description><![CDATA[{1[4][movie_desc]}]]></Description>
            <PicUrl><![CDATA[{1[4][movie_image]}]]></PicUrl>
            <Url><![CDATA[{1[4][movie_link]}]]></Url>
            </item>
            </Articles>
            </xml>
            """
        return xmltemplate


def verify_source(req):
    """验证get来源是否为微信"""
    timestamp = req.GET.get('timestamp','None')
    nonce = req.GET.get('nonce','None')
    signature = req.GET.get('signature','None')
    logger.info(signature)
    token = 'yinzhixin'
    templist = sorted([timestamp,nonce,token])    #字典排序  
    tempstr = ''.join(templist)         #排序后合并为字符串
    encryptstr = hashlib.sha1(tempstr).hexdigest()      #对字符串哈希加密
    logger.info("Encrypt:%s" %encryptstr)
    if signature == encryptstr:
        echostr = req.GET.get('echostr','None')
    else:
        echostr = "false"
    return echostr
