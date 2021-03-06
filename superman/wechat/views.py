#coding: utf-8

import hashlib
import logging
import json
import datetime
import decimal
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .dataprocess import Interface_Data_Process
from .dataprocess import curtime
from .dataprocess import DatabaseProcess
from .dataprocess import verify_source
from .dataprocess import CJsonEncoder

logger = logging.getLogger('django')

@csrf_exempt
def test(req):
    """微信程序入口"""
    if req.method == 'GET':
        echostr = verify_source(req)
        return HttpResponse(echostr)
    elif req.method == 'POST':
        try:
            #logger.info("request body: %s" % req.body)
            #插入user表
            db = DatabaseProcess()
            user = Interface_Data_Process.get_input(req)
            db.insert_user(user.username,str(user.content), user.req_ip,user.current_time,user.current_time)
            #插入movie_user_rel表
            movie_dict = db.get_movie_data()
            movie_list = []
            for movie in movie_dict:
                movie_list.append(str(movie['id']))
            movie_id_list = '|'.join(movie_list)
            movie_user_data = (user['username'], movie_id_list, curtime())
            db.insert_movie_user(movie_user_data)
            #给微信返回xml
            xmltemplate = Interface_Data_Process.output(req)
            xml = xmltemplate.format(user, movie_dict)
            return HttpResponse(xml)
        except Exception, e:
            logger.error("ERROR!ERROR!ERROR!:%s" % e)
            return HttpResponseBadRequest("query data fail!")
    else:
        logger.error("bad request!")
        return HttpResponseBadRequest("bad request!")

@csrf_exempt
def wechat(req):
    """验证应用根路径http://127.0.0.1:8000/wechat/可用性"""
    return HttpResponse("success!")



@csrf_exempt
def query(req):
    db = DatabaseProcess(db='dev')
    db_data = db.get_movie_data(tab='t_compete_monitor_conf', num=10)
    data = json.dumps(db_data, cls=CJsonEncoder)
    #logger.info(data)
    response = HttpResponse(data)
    response['Access-Control-Allow-Origin'] = '*'
    return response




