import json

from flask import Flask, request, make_response
from flask_restful import Resource
from flask_login import login_required,current_user

from ..model import News, NewsType, User, Comment
from ..utils import json_response, params_error, jsonChack
from app import db

class PostResource(Resource):
    def get(self):
        article = request.args.get("article",'')
        if article == '': 
            news = News.query.all()
            data = []
            for new in news:
                post = {}
                post["title"] = new.title
                post["content"] = new.content
                data.append(post)
            if len(data) == 0:
                data.append("没有数据")    
        else:
            data = {}
            try: 
                int(article)
            except Exception as e:
                return params_error("传入id不正确")    
            post = News.query.filter_by(id=int(article))
            if post:
                post = post[0]
                data["title"] = post.title
                data["url"] = post.url
                data["content"] = post.content
            else:
                data['msg'] = "没有指定的文章"            
        return json_response(data)  
    
    @login_required
    def post(self):
        data = request.get_data().decode('utf-8')
        data_dict = json.loads(data)
        print(data_dict)
        title = data_dict["title"] #标题,不可以空
        content = data_dict["content"] #内容, 如果是图片,可空
        ntype = data_dict["type"] #类型, 不可以空
        url = data_dict["url"] # 地址, 如果是新闻,可空
        

        error = {}
        #错误处理暂时不写

        if error:
            return params_error(error)         
        
        user = current_user._get_current_object()
        news_type = NewsType.query.filter_by(id=ntype).first()
        news = News(title= title, content=content, user=user, type=news_type, url=url) 
        db.session.add(news)
        db.session.commit()

        return json_response("提交成功")

    def put(self):
        pass

    def delete(self):
        pass            

class CommentResource(Resource):
    @login_required
    def post(self):
        data = request.get_data().decode("utf-8")
        data_dict = json.loads(data)
        print(data_dict)
        error = jsonChack(data_dict, "reply_id")
        if error:
            return params_error(error)
        
        # {"comment": comment, "pid": pid,"up": 0, "down":0, "device":"iphone", "reply_id":''}

        pid = data_dict["pid"]
        uid = data_dict["uid"]

        user = current_user._get_current_object()
        news = News.query.get(int(pid))
        if news is None:
            return params_error("文章不存在")

        print(data_dict)
        comment = Comment()
        comment.user = user 
        comment.news = news  
        comment.up = data_dict["up"]  
        comment.down = data_dict["down"] 
        comment.device = data_dict["device"]
        comment.content = data_dict["comment"]
        comment.reply_id = data_dict["reply_id"]
        db.session.add(comment)
        db.session.commit()

        return json_response("创建成功")
        
    def get(self):
        pid = request.args.get("pid", "")
        try: 
            int(pid)
        except Exception as e:
            return params_error("传入id不正确")
        news = News.query.get(int(pid)) 
        comment = Comment.query.filter_by(news=news)
        return_data = []
        if comment:
            for com in comment:
                data = {}
                data["content"] = com.content
                data["id"] = com.id
                data["reply_id"] = com.reply_id
                return_data.append(data)
        else:
            return_data.append("暂无评论")
        return json_response(return_data)


