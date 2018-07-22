from flask import render_template, request, redirect, url_for, make_response, flash

from ..utils import mulPage

from . import posts

#全局变量模拟分类资源
message_list = []
for i in range(40):
    username = str(i) + (".com")
    email = str(i) + ("@163.com")
    message = {"username":username, "email": email}
    message_list.append(message)

# 调用函数创建分页
@posts.route("/value/<int:page>", methods=["GET", "POST"])
def value(page):
    coo = request.cookies
    print(coo)
    tags, message_lists = mulPage(message_list, page,limit=4 ,num=5)
    return render_template("home/value.html", message_lists=message_lists, tags=tags)

#提交数据
@posts.route("/index/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        message = {"username":username, "email": email}
        message_list.append(message)
        return render_template("home/index.html", message_lists=message_list)
    return render_template("home/index.html") 

@posts.route("/article/", methods=["GET"])
def article():
    wd = request.args.get("wd")
    page = request.args.get("pn","")
    print(wd, page)
    return render_template('/posts/article.html')
    


