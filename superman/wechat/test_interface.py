#coding: utf-8

import requests


url = "http://127.0.0.1:8000/wechat/test/"
data = """
    <xml>
    <ToUserName><![CDATA[gh_c8026a854987]]></ToUserName>
    <FromUserName><![CDATA[o-ijPw0j4UvYgJbcRuT6r2au7Huo]]></FromUserName>
    <CreateTime>1465874986</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[123]]></Content>
    <MsgId>6295885125314082434</MsgId>
    </xml>
"""


r = requests.post(url, data=data)
print r.content





"""
POST /wechat/test?
signature=f980308dbeeb0e78bae466c19f889a0d0c434416
&timestamp=1465872572&nonce=935575977&openid=o-ijPw0j4UvYgJbcRuT6r2au7Huo
"""