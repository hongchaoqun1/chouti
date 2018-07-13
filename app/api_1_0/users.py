import json

from flask import make_response, jsonify, request, session
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required

from app import db
from ..model import User
from ..utils import json_response, params_error

#注册
class RegistResource(Resource):
    def post(self):
        data_json = request.get_data().decode("utf-8")
        data_dict = json.loads(data_json)
        print(data_dict)

        username = data_dict['username']
        password = data_dict["password"]
        password2 = data_dict["password2"]
        #邮箱改成了手机
        email = data_dict["phone"]

        error = {}
        '''
        错误列表:
        用户名存在
        手机存在
        密码不一样
        '''
        user = User.query.filter_by(username = username).first()
        if user:
            error["username"] = "用户名已存在"
        user_phone = User.query.filter_by(email = email).first()
        if user_phone:
            error["phone"] = "手机号已经被注册"
        if password != password2:
            error[password] = "密码不一致"
        print(error)
        if error:
            return jsonify({"status":False, "error": error, "msg": "参数错误"})            
        
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()


        return jsonify({"data":"ok", "status": True, "error":None, "msg": "注册成功"})
        

#登录
class SessionResource(Resource):
    def post(self):
        data_json = request.get_data().decode("utf-8")
        data_dict = json.loads(data_json)
        print(data_dict)

        username = data_dict["username"]
        password = data_dict['password']
        # code = data_dict["imgCode"]

        error = {}

        # if code != session['verifycode']:
        #     error["验证码"] = "验证码不对"
        #     return params_error(error)

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user, False)
            return json_response("登录成功")
        else:
            error['error'] = "用户名或密码错误"
            return params_error(error)   
    
    @login_required
    def delete(self):
        return json_response("退出成功")
                     

#手机验证码
class WirelessCodeResource(Resource):
    pass  
   