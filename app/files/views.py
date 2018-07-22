import os
import string
import random
from PIL import Image

from flask import current_app
from flask import Flask, render_template, request, make_response
from flask_login import login_required

from . import files
from ..utils import params_error, json_response



#生成随机图片名
def newName(shuffix, length=32):
    my_str = string.ascii_letters + '0123456789' 
    new_name = ''.join(random.choice(my_str) for i in range(length))
    return new_name + shuffix

#上传文件类型检查
def allowedFile(shuffix):
    return shuffix.lower() in current_app.config["ALLOWED_EXTENSIONS"]
        
@files.route("/upload", methods=["POST"])
@login_required
def uploadFile():
    img_name = None
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = file.filename 
        shuffix = os.path.splitext(file_name)[-1]
        print(shuffix)

        if allowedFile(shuffix):
            new_name = newName(shuffix)
            img_name = new_name
            new_path = os.path.join(current_app.config['UPLOAD_FOLDED'], new_name)
            
            file.save(new_path)

            img = Image.open(new_path)
            print(img.size)
            img.thumbnail((200,200))
            img.save(new_path)

        else:
            response = make_response("上传的格式不对")
            return response    
        return json_response({"url":img_name})
    
