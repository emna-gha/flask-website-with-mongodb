#this file is created in order to make website folder a package
from flask import Flask 
import pymongo 

#Database linking

client= pymongo.MongoClient('127.0.0.1',27017)
db = client.user_login_system

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= 'secret_key_must_not_be_shared_with_anybody_in_production'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    
    return app

