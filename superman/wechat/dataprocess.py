#coding: utf-8

import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 


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
        <ArticleCount>2</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[夺宝奇兵]]></Title> 
        <Description><![CDATA[123456]]></Description>
        <PicUrl><![CDATA[http://pic6.qiyipic.com/image/20150317/da/e9/aa/v_105073913_m_601_m3_195_260.jpg]]></PicUrl>
        <Url><![CDATA[http://www.iqiyi.com/v_19rrh5zbfo.html]]></Url>
        </item>
        <item>
        <Title><![CDATA[五鼠闹东京]]></Title>
        <Description><![CDATA[宋朝时，陷空岛住着五个结拜兄弟。五鼠的武艺名声在外，庞太师派人送重金，想收买五鼠为他效力。正直侠义的五鼠不愿为奸臣卖力，白玉堂、徐庆和蒋平三人将送礼的人打了一顿，赶了回去。白玉堂在丁月华的激将下，私闯开封府，盗走了包公的尚方宝剑。庞太师对五鼠怀恨在心，派人投毒欲害死五鼠。白玉堂的四位兄长都误食中毒，并被庞太师派的杀手追杀。危急之中，展昭赶来，杀退追兵，救出四条好汉……]]></Description>
        <PicUrl><![CDATA[http://pic5.qiyipic.com/image/20150122/77/5b/v_108871223_m_601_m1.jpg]]></PicUrl>
        <Url><![CDATA[http://www.iqiyi.com/lib/m_202418314.html]]></Url>
        </item>
        </Articles>
        </xml>
        """
    xml = xmltemplate.format(get_input(req))
    return xml