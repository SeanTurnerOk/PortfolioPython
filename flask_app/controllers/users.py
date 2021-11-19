from flask import render_template, session, redirect, request, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import bcrypt
@app.route('/')
def main():
    return render_template('landing.html')
@app.route('/register', methods=['POST'])
def register():
    if not User.validateUser(request.form):
        return redirect('/')
    else:
        pwHash = bcrypt.generate_password_hash(request.form['password'])
        data={'firstName':request.form['firstName'],
        'lastName':request.form['lastName'],
        'email':request.form['email'],
        'password':pwHash}
        User.save(data)
        return redirect('/')