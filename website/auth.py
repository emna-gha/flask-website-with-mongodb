from flask import Blueprint,render_template,request,flash,redirect,session
from .models import User 
from . import db
from passlib.hash import pbkdf2_sha256

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = db.users.find_one ({ "email": request.form.get('email') })
        if user:
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']) :
                flash('Logged in successfully',category='sucess')
                User().start_session(user)
                return redirect('/profile')
            else:
                flash('Incorrect password,try again', category='error')
        else:
            flash('email does not exist', category='error')   
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        userName= request.form.get('userName')
        password1= request.form.get('password1')
        password2 = request.form.get('password2')
        # check if  the inputs are valid before confirming registration
        if len(email)<4 :
            #flash is used to print a text on the screen
            flash('Email must be greater than 3 characters', category = 'error')
        elif len(userName)<2:
            flash('Username must contain more than 1 characters', category='error')
        elif password1 != password2 :
             flash('your passwords doesn\'t match.', category='error')
        elif len(password1)<7:
             flash('Password must be equal or longer than 7 charachters', category='error')
             
        #check for existing email before confirming registration and adding user to db
        elif db.users.find_one ({ "email": email }):
            flash('Can not use this email.It already exists', category='error')
        else:
            User().signup()
            # add user to database
            flash ('A new account is created', category='success')
            
       
    return render_template('sign-up.html')

@auth.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')
