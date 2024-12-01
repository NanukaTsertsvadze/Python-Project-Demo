from flask import Flask, redirect, render_template,url_for,request,session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests 
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pythonproject'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.sqlite'
db = SQLAlchemy(app)
errors = Blueprint('errors', __name__)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)

    
with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def aboutus():
    return render_template("aboutus.html")

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        user = Info.query.filter_by(email=username).first()
        if user:
            if check_password_hash(user.password, password):
                return redirect(url_for('profile'))   
            else:
                flash("The password or username is not right", "error")
        else:
            flash("This User is not registred in to our Site <3", "error")
    return render_template("signin.html")

@app.route("/profile")
def profile():
    if 'username' in session:
        key = '887aaff89bee4fd742287bfd4afa2483'
        city = 'Tbilisi'
        payload = {'q': city, 'appid': key, 'units': 'metric'}
        resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload)
        result = resp.json()
        # print(json.dumps(result, indent=4))
        temperature = result['main']['temp']
        name = session['username']
        return render_template("profile.html", name=name, temperature=temperature)
    else:
        return redirect(url_for("signin"))


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("signin"))

@app.route("/Signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        firstname = request.form['Firstname']
        lastname = request.form['Lastname']
        email = request.form['email']
        password = request.form['password']
        sex= request.form.get('sex')
        if firstname == "" or lastname == "" or email == "" or password == "" or sex == "":
            flash("Fill all the gaps, So you  can end signin up <3", "error")
        elif email.isdecimal():
            flash("Email can not be number.Pleas, enter correct email", "error")
        else:
            person = Info(Firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password), sex=sex)
            db.session.add(person)
            db.session.commit()
            flash("You successfully signed up. Welcome to BLISsTORE <3", "info")
    return  render_template("signup.html")

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500

@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404

app.register_blueprint(errors)

if __name__ == "__main__":
    app.run(debug=True)
