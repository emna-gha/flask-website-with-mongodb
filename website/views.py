#this file is defined as the blueprint of our app
#it includes all the roots,urls needed
from flask import Blueprint,render_template

views = Blueprint(' views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')



