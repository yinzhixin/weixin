#coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import hashlib
import logging
from .dataprocess import output, DataPrecess
from .. import superman

superman.settings.configure()


logger = logging.getLogger('django')


@csrf_exempt
def apply(req):
    """用于公众平台验证服务器可用性"""
    if req.method == 'GET':
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
        return HttpResponse(echostr)
    elif req.method == 'POST':
        try:
            xml = output(req)
            logger.info("request IP: %s" % req.META.get('REMOTE_ADDR',None))
            logger.info("request body: %s" % req.body)
            return HttpResponse(xml)
        except Exception:
            logger.error("wulalalallalalala~")
            return HttpResponseBadRequest("bad request!")
    else:
        logger.error("bad request!")
        return HttpResponseBadRequest("bad request!")

@csrf_exempt
def wechat(req):
    """接收普通消息接口"""
    return HttpResponse("success!")

class QueryData(object):
    """django db api """
    def __init__(self):
        super(QueryData, self).__init__()
        self.cursor = connections['test'].cursor
    
    def movie_data(self):
        """返回电影信息，可优化为配置项"""
        self.cursor.execute("select * from movie order by rand() limit 5")
        return self.cursor

    def joke_data(self):
        """待扩展"""
        pass

if __name__ == '__main__':
    db = QueryData()
    movie = DataPrecess.dictfetchall(db.movie_data())
    print movie

