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
    # Landing is the login/register page
    return render_template('landing.html')
@app.route('/register', methods=['POST'])
def register():
    if not User.validateUser(request.form):
        # Flashed messages made by validateUser describing any errors
        return redirect('/')
    else:
        # instantiating bcrypt to avoid saving passwords in plaintext, making the user significantly more secure
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
    #Since this is all serverside, this should still be secure. If not, passing in the password as well should encapsulate well enough. Would definitely ask superior if this is secure
    possUser=User.getByEmail(data)
    if possUser and bcrypt.check_password_hash(possUser['password'],request.form["password"]):
        #userId added to session in case user info beyond firstName required. Can easily use User.findById() if necessary.
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
    #yfinance used for simplicity and reliability, instead of scraping the data myself, as the data scraping fails if yahoo updates its website too much.
    data=yf.Ticker("aapl").history(period='max')
    #creating the line graph
    fig=Figure()
    axis=fig.add_subplot(1,1,1)
    axis.grid()
    axis.set_title("Open Prices")
    axis.set_xlabel("Days")
    axis.plot(data['Open'].values)
    #passing the graph to the template to render.
    output=io.BytesIO()
    FigureCanvas(fig).print_png(output)
    graph='data:image/png;base64,'
    graph+= base64.b64encode(output.getvalue()).decode('utf8')
    return render_template('home.html', data=data,graph=graph, userFirstName=userFirstName)