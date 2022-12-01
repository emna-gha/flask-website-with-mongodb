#this file is defined as the blueprint of our app
#it includes all the roots,urls needed
from flask import Blueprint,render_template,request,redirect,flash,session
from . import db
from passlib.hash import pbkdf2_sha256

views = Blueprint(' views', __name__)


@views.route('/')
def home():
    return render_template("home.html")



        

