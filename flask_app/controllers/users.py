from flask import render_template, session, redirect, request, flash, Response
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
import yfinance as yf
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
@app.route('/')
def main():
    return render_template('landing.html')
@app.route('/register', methods=['POST'])
def register():
    if not User.validateUser(request.form):
        return redirect('/')
    else:
        bcrypt=Bcrypt()
        pwHash = bcrypt.generate_password_hash(request.form['password'])
        data={'firstName':request.form['firstName'],
        'lastName':request.form['lastName'],
        'email':request.form['email'],
        'password':pwHash}
        User.save(data)
        return redirect('/')
@app.route('/checker', methods =["POST"])
def checker():
    bcrypt=Bcrypt()
    data={'email':request.form['email']}
    possUser=User.getByEmail(data)
    if possUser and bcrypt.check_password_hash(possUser['password'],request.form["password"]):
        session["userId"]=possUser['id']
        session['userFirstName']=possUser['firstName']
        return redirect('/home')
    elif not possUser:
        flash("Invalid Email Address")
        return redirect('/')
    else:
        flash("Invalid Password")
        return redirect('/')
@app.route('/home')
def home():
    userFirstName=session['userFirstName']
    data=yf.Ticker("aapl").history(period='max')
    fig=Figure()
    axis=fig.add_subplot(1,1,1)
    axis.grid()
    axis.set_title("Open Prices")
    axis.set_xlabel("Days")
    axis.plot(data['Open'].values)
    output=io.BytesIO()
    FigureCanvas(fig).print_png(output)
    graph='data:image/png;base64,'
    graph+= base64.b64encode(output.getvalue()).decode('utf8')
    return render_template('home.html', data=data,graph=graph, userFirstName=userFirstName)