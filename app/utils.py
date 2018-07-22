from flask import jsonify
import copy 
    
def mulPage(message_list, page, limit=3, num=5):
    '''
    用于生成分页的函数
    主要参数是:
    message_length:资源的长度
    page: 请求当前的页面
    limit: 每页资源的个数
    num: 每页分页的数量
    base_url: 配置url
    '''
    if num%2 ==0:
        a = int(num/2-1)
        b = int(num/2+1)
    else:
        a = int(num/2)
        b = int(num/2+1)

    page_num = len(message_list)//limit +1
    tags = []
    s = page-a
    e = page+b
    if s <=0:
        s = 1
        e = e - (page-3)
    if e > page_num:
        s = s-(e-page_num)+1
        e = page_num+1
    for i in range(s,e):
        if i == page:
            tag = "<li class='active'><a href='/value/{0}'>{1}</a></li>".format(i,i)
        elif i == 0:
            tag = "<li><a href='/value/1'>&laquo;</a></li>" 
        elif i == page_num+1:
            tag = "<li><a href='/value/{0}'>&raquo;</a></li>".format(i-1)      
        else:    
            tag = "<li><a href='/value/{0}'>{1}</a></li>".format(i,i)
        tags.append(tag)

    start = (page-1)*limit
    end = page*limit

    message_lists=message_list[start:end]

    return tags, message_lists  

def json_response(data):
    res = {
        "msg": "ok",
        "status": True,
        "state": 200,
        "data": data
    }
    return jsonify(res)

def params_error(data):
    res = {
        "msg": "参数错误",
        "status": False,
        "state": 403,
        "error": data
    }
    return jsonify(res)

def jsonChack(v,*args):
    val = copy.deepcopy(v)
    error = {}
    for i in args:
        val.pop(i)

    for i in val:
        if val[i] == "":
            error[i] = "该参数为空"
    return error       
