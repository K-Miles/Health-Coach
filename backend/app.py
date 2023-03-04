from flask import Flask, request, render_template, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("secrets/serviceAccount.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in  request.form and 'password' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        decoded_token = auth


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    msg = ''