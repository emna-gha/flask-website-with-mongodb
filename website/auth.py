from flask import Blueprint,render_template,request,flash,redirect,session,url_for
from .models import User 
from . import db
from passlib.hash import pbkdf2_sha256
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = db.users.find_one ({ "email": request.form.get('email') })
        if user:
            #check if the user with that email has a matching password in db with the one entered to login
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']) :
                flash('Logged in successfully',category='sucess')
                User().start_session(user)
                #login_user(user, remember=True)#remember that the user is logged in until he restarts his session
                return redirect('/list-users')
            else:
                flash('Incorrect password,try again', category='error')      
        else:
            flash('email does not exist', category='error')   
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth.route('/list-users')
def getlist():
    return render_template('list-users.html',users=db.users.find())
    

@auth.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')
 
 
@auth.route('/change_password', methods=['GET','POST'])
def changepassword():
    if request.method == 'POST':
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        if password1 == "" or password2 == "" or password1 == password2:
            print(session['user']['password'])
            flash('Please refill the field',category='error')
            return redirect('/change_password')
        else:
            new_password=pbkdf2_sha256.encrypt(password2)
            db.users.update_one( {'email': session['user']['email']}, {'$set': {'password': new_password}})
            flash('Password Changed Successfully',category='success')
            return redirect('/profile')
    else:
        return render_template('change_password.html')
        
        
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
            # add user to database
            User().signup()
            flash ('A new account is created', category='success')
            return redirect('/profile')
       
    return render_template('sign-up.html')

