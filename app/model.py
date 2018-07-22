#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime

from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

registrations = db.Table('registrations',
   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
   db.Column('class_id', db.Integer, db.ForeignKey('classes.id')),
)        

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    classes = db.relationship('Class',secondary=registrations,backref=db.backref('students', lazy="dynamic"), lazy="dynamic")

class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    ctime = db.Column(db.DateTime(), default=datetime.utcnow)
    news = db.relationship('News', backref = 'user', lazy = 'dynamic')
    favor = db.relationship("Favor", backref= "user", lazy = "dynamic")
    comment = db.relationship("Comment", backref= "user", lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) 

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)    
        
class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    userinfo_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ntype = db.Column(db.Integer, db.ForeignKey("news_type.id"))
    ctime = db.Column(db.DateTime(), default=datetime.utcnow)
    title = db.Column(db.String(32))
    url = db.Column(db.String(128))
    content = db.Column(db.String(256))
    favor = db.relationship("Favor", backref= "news", lazy = "dynamic")
    comment = db.relationship("Comment", backref= "news", lazy = "dynamic")
    
class NewsType(db.Model):
    __tablename__ = "news_type"
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(32))    
    news = db.relationship('News', backref="type", lazy="dynamic")

# 点赞表            
class Favor(db.Model):
    __tablename__ = "favor"
    id = db.Column(db.Integer, primary_key=True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    ctime = db.Column(db.DateTime(), default = datetime.utcnow)

    __tableargs__ = (
        db.UniqueConstraint("user_info_id", "news_id", name="uix_uid_nid")
    )

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"))
    reply_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=True, default=True)
    up = db.Column(db.Integer)
    down = db.Column(db.Integer)
    #是DataTime
    ctime = db.Column(db.DateTime(), default=datetime.utcnow)
    device = db.Column(db.String(32))
    content = db.Column(db.String(256))


from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))