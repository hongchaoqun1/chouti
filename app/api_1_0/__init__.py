from flask import Blueprint
import flask_restful as restful

from . import authrntication, posts, users, comments, errors

api = restful.Api(prefix='/api/v1')
# api.add_resource(users.UserInfoResource, '/user')
api.add_resource(users.RegistResource, "/regist/")
api.add_resource(users.SessionResource, "/login/")
api.add_resource(posts.PostResource, "/post/")
api.add_resource(posts.CommentResource, "/comment/")
# api.add_resource(posts.ArticleResource, "/article/<pid>")