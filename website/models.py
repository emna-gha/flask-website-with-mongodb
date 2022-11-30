from flask import Flask,flash, jsonify,request,session,render_template,redirect,url_for
import uuid
from passlib.hash import pbkdf2_sha256

from . import db

class User:
    
    def start_session(self, user):
        #if "email" in session:
            session['logged_in']=True
            session['user'] = user
            #return render_template('profile.html')
        #else:
            #return redirect(url_for("auth.login"))
            return jsonify(user), 200
    
    def signup(self):
        print(request.form) #just to test on my console while debugging
        
        #create the user object
        user={
        "_id":uuid.uuid4().hex,
        "username":request.form.get('userName'),
        "email":request.form.get("email"),
        "password":request.form.get('password1')
        }
        #encrypt the password for security 
        user['password']= pbkdf2_sha256.encrypt(user['password'])
        
        if db.users.insert_one(user):
            return self.start_session(user)
           
        return jsonify ({"error": "signup failed"}),400
    
#class sendmoney(self):
    #id= primary key
    #balance=
    #amount=
    #user_id= foreign key('user.id')