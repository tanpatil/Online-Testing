import flask
from flask import render_template, request, redirect, url_for
import requests
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    args = {
        'title':'TestMate', 
        'name':'Sumuk'
    }
    return render_template('index.html', args=args)


@app.route('/internal_test', methods=['GET'])
def internal_test():
    response = requests.get('http://localhost:5000/internal')
    response = response.json()
    if response['status'] == 200:
        return "<h1>Able to connect to the API. All systems Go!"
    else:
        return "<h1>Something went wrong>"



@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            data = {
                'authorization': {
                    'username': request.form['username'],
                    'password': request.form['password']
                }
            }
            response = requests.post('http://localhost:5000/login')
            response = response.json()
            if response['status'] == 200:
                
    return render_template('login.html', error=error)

app.run(debug=True, port=80)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass