#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
import random

from flask import render_template, request, redirect, url_for, make_response, flash, session, jsonify

from . import main
from app import db
from ..model import Student, Class


@main.route('/',methods=['GET','POST'])
def ind():
    is_authenticated = 0
    username = None
    new_list = [{"title":'复仇者联盟', "article": "哈期待啊"}, {"title":'美国队长', "article": "哈期待啊"}]
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "ab" and password =="123456789":
            is_authenticated = 1 
            
    return render_template('index.html', is_authenticated=is_authenticated, username=username, news = new_list)


# 定义一个随机字符串,保存session
SESSION = {}

# 定义一个session处理类
class MakeSession:
    def __init__(self):
        pass

    def genarateRandom(self):
        session_id = str(random.randint(0,80000))
        return session_id

    def setValue(self, key, value, symbol=False):
        '''
        设置session的函数,主要功能
        1,设置随机字符串
        2,设置小字典
        3,如果是第一次登录,设置cookie到客户端
        '''
        session_id = self.genarateRandom()
        SESSION[session_id] = {}
        SESSION[session_id][key] = value
        SESSION[session_id]["is_login"] = True

        response = make_response("登录成功")
             
        if symbol == True:
            expire_time = time.time() + 7*3600*24
            response.set_cookie('session_id',session_id, expires=expire_time)   
                #path 指定cookie生效路径    
        else:
            response.set_cookie('session_id',session_id)         
        return response
        

    def getValue(self):
        #从客户端获取session_id
        #找到自己的数据
        pass    

user = {"ab":"sb", "ac":"wc"}
@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data_json=request.get_data().decode('utf-8')
        data_dict=json.loads(data_json)
        
        username = data_dict['username']
        password = data_dict['password']
        checkbox = data_dict['checkbox']

        if username in user and user[username] ==password:
           make_session = MakeSession()
           session = make_session.setValue("username", username, True)
           return session
        else:
            flash('登录失败')    
            
    return render_template('login.html')    

# 内容页面,需要登录才能看
@main.route('/manage/')
def manage():
    session_id = request.cookies.get("session_id")
    if session_id in SESSION:
        username = SESSION[session_id]["username"]
        return render_template('/manage.html', money=username) 
    else:
        response = make_response("请先登录")
        return response   

@main.route("/logout/")
def logout():
     response = make_response("退出成功")
     response.set_cookie('session_id',"quit", expires=time.time())
     return response

@main.route("/regist/")
def regist():
    return render_template("regist.html")

@main.route("/verify/")
def verify():
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    #构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\Longview.otf', 40)
    #构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    response = make_response(buf.getvalue())
    return response      


@main.route("/test")
def test():
    return render_template("text.html")    

@main.route("/test2")
def test2():
    return render_template("text2.html")