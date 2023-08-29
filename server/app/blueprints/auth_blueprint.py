from flask import Blueprint, request, jsonify, session, make_response
import json
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS, HTTP_404_NOT_FOUND, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
import random
from app.forms_db import db, User
from app import mail
from flask_mail import Message
import datetime
from flask_jwt_extended import create_access_token
from markupsafe import Markup
from os import urandom

auth_blueprint = Blueprint("auth", __name__)

# validate password
def is_valid_password(password):
    # Define your password validation criteria
    min_length = 8
    contains_uppercase = any(char.isupper() for char in password)
    contains_lowercase = any(char.islower() for char in password)
    contains_digit = any(char.isdigit() for char in password)
    contains_special = any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?~' for char in password)

    return (
        len(password) >= min_length and
        contains_uppercase and
        contains_lowercase and
        contains_digit and
        contains_special
    )

# generate 6 digits code
def generate_random_code():
    return random.randint(100000, 999999)

# send code to email
def sendEmail(eml, code):
    msg = Message("Authentication Code", recipients=[eml])
    msg.html = f"<div style='padding:8px 5px; background-color:#66CA98; color:#f5f5f5; border-radius:20px;'> \
                    <h3 style='padding:5px 2px; text-align:center; color:#f5f5f5;'>GBST Authentication Code</h3> \
                    <p style='color:#f5f5f5;'>Here is your authentication code for GBST. <br/> <b>NB:</b> \
                    Code expires in 10 mins.</p> \
                    <h4 style='text:center;'>{code}</h4> \
                <div>" 
    # msg.body = f"{code}"
        # send auth code to email
    mail.send(msg)

# home
@auth_blueprint.route('/', methods=['GET'])
def index():
    return "home page"

# get  user
@auth_blueprint.get('/user')
def get_user():
    email = request.json.get('email', '')
    user = User.query.filter_by(email=email).first()
    return {"user": user.username}, HTTP_200_OK



# register user
@auth_blueprint.route('/register', methods=['POST'])
def register():

    username = request.json['username'];
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']

    user_by_email = User.query.filter_by(email=email).first()
    user_by_username = User.query.filter_by(username=username).first()

    if user_by_username:
        return {"error_message": "Username already exists"}, HTTP_409_CONFLICT
    if user_by_email:
        return {"error_message": "User email already exists"}, HTTP_409_CONFLICT
    if not username:
         return{"error_message": ""}, HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return {"error_message":"Invalid email address"}, HTTP_400_BAD_REQUEST
    if not is_valid_password(password):
        return {"error_message": "Invalid password"}, HTTP_400_BAD_REQUEST
    if not role:
        return {"error_message": "Select your role"}, HTTP_400_BAD_REQUEST
    # hash user password
    hashed_password = generate_password_hash(password)
    # expiration time
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    # generateotp
    otp = generate_random_code()


    # send authentication code to user
    sendEmail(email, otp)
    try:
       
            # add user to database
        user = User(
            username=username, email=email, 
            role=role, password=hashed_password, otp=otp, 
            expiration_time=expiration_time
            )
        db.session.add(user)
        db.session.commit()
        return {"success_message": f"Authentication code sent to  {email}"}, HTTP_200_OK
    except Exception as e:
            return {"error_message": f"error sending authentication code. Reason{e}"}, HTTP_500_INTERNAL_SERVER_ERROR
    
    # # add user to database
    # user = User(email=email, password=hashed_password, otp=otp, expiration_time=expiration_time)
    # db.session.add(user)
    # db.session.commit()

    # return {"success": "Verification code has been sent to ur email", "email": email}, HTTP_201_CREATED

# verify user
@auth_blueprint.route('/verify-user', methods=['POST'])
def verify_user():

    # Retrieve the user's email from the session
    email = request.json.get('email','')
    # get code from form
    input_code = request.json['code']
    # fetch user from database with retrieved email
    user = User.query.filter_by(email=email).first()
    # get code from database and compare with submitted code

    # if email is not in session
    if not email:
        return {"error_message": "Sorry, we cannot verify user at this time." +
                "You are probably verified or not yet registered. " +
                "Kindly Sign in if you are a registered user or Sign up if you are not"},HTTP_400_BAD_REQUEST
    
    # if user does not exist in database
    if user is None:
        return {"error_message": "User does not exist, kindly Sign up to continue"}, HTTP_404_NOT_FOUND
    
    #  if user is already verified
    if user.is_verified:
        return {"error_message": "User already verified."}, HTTP_400_BAD_REQUEST
    
    # compare input code and retrieved code
    user_otp = user.otp
    if input_code != user_otp:
        return {"error_message": "Code does not match"}, HTTP_400_BAD_REQUEST
    
    # compare input code and retrieved code
    if input_code ==  user_otp:

        # print(input_code ==  user.otp)
        # update user is_verified status in the databse
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        # delete email from session
        session.pop('email', None)
        return {"success_message": "User verification successful"},  HTTP_200_OK

"""
    Consuming tokens:
    - Once a login button is clicked, the auth/login end point is called
    - This returns the access and refresh token
    - Pass the access token into the Ajax header in order to access a protected endpoint
    - This can be done with fetch, fetch api makes a post request to the protected endpoint
        in the useEffect hook function

    As per the refresh token

"""            
             
# user login
@auth_blueprint.route('/login', methods=['POST'])
def login():
        
        matric_no = request.json.get('matricNo')
        password = request.json.get('password')

        # clean inputs
        matric_no =  Markup.escape(matric_no)
        password =  Markup.escape(password)

        user = User.query.filter_by(matricNo=matric_no).first()

        if not user:
            return {"error_message": "User not found. Sign up to continue"}, HTTP_401_UNAUTHORIZED_ACCESS

        # check if user is signed up but not authenticate
        if user and not user.is_verified:
            return {"error_message": "User not yet authenticate"}, HTTP_401_UNAUTHORIZED_ACCESS
        
        if user and user.is_verified:
            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct:

                access_token = create_access_token(identity=user.id)
                # generate csrf token
                csrf_token = urandom(16).hex();

                response = jsonify({'message': 'Login successful', "email": user.email, 'csrf_token': csrf_token})
                
                # Set the http-only JWT cookie
                response.set_cookie('access_token', access_token, httponly=True)
                # Set the double submit token as a readable cookie
                response.set_cookie('csrf_token', csrf_token)

                return response, HTTP_200_OK
            else:
                return {"error_message": "Incorrect password"}, HTTP_401_UNAUTHORIZED_ACCESS
                
# user logout
@auth_blueprint.post('/logout')
def logout():
    response = jsonify({"success_messsage": "logout successful"})
    response.delete_cookie('access_token')
    response.delete_cookie('csrf_token')
    return response
              