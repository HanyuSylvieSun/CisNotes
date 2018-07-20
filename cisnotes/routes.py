from flask import render_template, url_for, flash, redirect, request
from cisnotes import app, db, bcrypt
from cisnotes.models import User, Post
from cisnotes.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

posts = [
   {
     "author" : "Sylvie Sun",
     "title" : "take CIS-121",
     "content" : "just don't",
     "date" : "April. 18",
   }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts, title = "hello")

@app.route("/about")
def about():
    return render_template("about.html", title = "about")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    myform = RegistrationForm()
    if myform.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(myform.password.data)
        user = User(username = myform.username.data, email = myform.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{myform.username.data}, welcome to CisNotes <3', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register", form = myform)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    myform = LoginForm()
    if myform.validate_on_submit():
        user = User.query.filter_by(email = myform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, myform.password.data):
            login_user(user, remember = myform.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Can\' find your acount, please check your usename and password', 'danger')
        #return redirect(url_for('home'))
    return render_template('login.html', title = "Login", form = myform)

@app.route("/logout")
def logout():
    logout_user()
    flash("You've successfully logged out. Hope to see you again!", "success")
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = "Account")
