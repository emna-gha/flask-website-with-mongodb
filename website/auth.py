from flask import Blueprint,render_template,request,flash,redirect,session,url_for
from .models import User 
from . import db
from passlib.hash import pbkdf2_sha256

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = db.users.find_one ({ "email": request.form.get('email') })
        #in case the email exists in db succes otherwise error
        if user:
            #check if the password in db matches the one entered by user
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']) :
                flash('Logged in successfully',category='sucess')
                User().start_session(user)
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
    if request.method== "POST":
        search=request.form.get('search')
        users=db.users.find_one({'username':search})
        return redirect(url_for('profile', id=users['_id']))
       
    return render_template('list-users.html',users=db.users.find())
    
@auth.route('/profile/<id>', methods=['GET','POST'])
def profile_by_id(id):
    user=db.users.find_one({'_id':id})
    return render_template('profile_by_id.html',user=user)


@auth.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')
 
@auth.route('/send-money', methods=['GET','POST'])
def sendmoney():
    if request.method == 'POST':
        money=request.form.get('money')
        #verify whether the user has enough balance or not
        if int(money) > int(session['user']['balance']):
            flash('You do not have enough money to send',category='error')
        else:
            flash('Money sent successfully',category='success')
            #update the current balance of the sender after sending money
            new_balance= (int(session['user']['balance']) - int(money))
            db.users.update_one( {'email': session['user']['email']}, {'$set': {'balance': str(new_balance)}})
            
    return render_template('send-money.html')


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
            return redirect('/list-users')
       
    return render_template('sign-up.html')

