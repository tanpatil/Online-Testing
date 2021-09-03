import sys
sys.path.append('.')
from flask import Flask, request, jsonify, make_response   , render_template, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
import datetime
from functools import wraps

import src.microservices.user_control as uc

connected = False
import mysql.connector

try:
    mydb = mysql.connector.connect(
      host="13.235.17.41",
      user="sumuk",
      password="sumuk", 
      database='testdb'
    )
    connected = True
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

mycursor = mydb.cursor()

if not connected:
    exit()

app = Flask(__name__) 

SECRET_KEY='Th1s1ss3cr3t'

# HELPERS
def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):

       token = None 

       if 'x-access-tokens' in request.headers:  
          token = request.headers['x-access-tokens'] 


       if not token:  
          return jsonify({'message': 'a valid token is missing'})   


       try:  
          data = jwt.decode(token, SECRET_KEY) 
          current_user = uc.get_by_id(data['public_id'])  
       except:
          return jsonify({'message': 'token is invalid'})  


       return f(current_user, *args,  **kwargs)  
    return decorator 


@app.route('/', methods=['GET'])
def home():
    return '''<h1> Welcome to the TestMate API</h1>'''


@app.route('/internal', methods=['GET'])
def internal_conn_test():
    return jsonify({
        'status':200, 
        'message':'all ok'
    })
        
#REGISTRATION
@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()
    res = uc.create_user(name=data['name'], password=data['password'], role=data['role'], cursor=mycursor)
    if res['status']==200:
        mydb.commit()
        return jsonify({'status':200, 'message':'ADDED THE USER', 'object':None})
    else:
        return jsonify({'message': 'errored out', 'obj':res})   

#LOGIN
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    res = uc.check_password(name=auth.username, auth_pass=auth.password)
    if res['status']==200:  
        token = jwt.encode({'public_id': res['object']['id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, SECRET_KEY)  
        return jsonify({'token' : token.decode('UTF-8')}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    name = current_user['name']
    return {'status':200, 'message':f'Authenticated as {name}', 'object':uc.get_all_users(mycursor=mycursor)}


#TESTING
@app.route('/test_protected', methods=['GET'])
@token_required
def test_protected(current_user):
    return jsonify({'status':200, 'message':f"Authenticated as {current_user}"})


#TESTING_UNPROTECTED
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status':200, 'message':'OK'})


if  __name__ == '__main__':  
     app.run(host='localhost', debug=True) 
