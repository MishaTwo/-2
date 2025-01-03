from . import app, login_manager
from flask import render_template, request, redirect, flash, url_for
from .models import User, Directory
from .models.base import session
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user
import pandas
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import yagmail
import os

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mailing', methods=['GET', 'POST'])
@login_required
def mailing():
    if request.method == 'POST':
            folder_path = str(request.form['folder_path'].replace('"', ''))
            file_path = str(request.form['file_path'].replace('"', ''))
            email_column = int(request.form['email_column']) - 1
            file_column = int(request.form['file_column']) - 1
            title = request.form["title"]
            from_email = current_user.email
            print(from_email)
            print(current_user.password)
            df = pandas.read_excel(file_path)

            emails = df.iloc[:, email_column].tolist()
            file_names = df.iloc[:, file_column].tolist()
            
            if '@gmail.com' in from_email:
                smtp_host = 'smtp.gmail.com'
                smtp_port=465
            elif '@ukr.net' in from_email:
                smtp_host = 'smtp.ukr.net'
                smtp_port=465

            for i in range(len(emails)):
                file = rf"{folder_path}\{file_names[i]}"
                yag = yagmail.SMTP(from_email, password=current_user.password, host=smtp_host, port=smtp_port)
                yag.send(to=emails[i], subject=title, contents=file)
            return render_template("mailing.html")
    return render_template("mailing.html")

@app.route('/directory', methods=["POST", "GET"])
def directory():
    if request.method == "POST":

        try:
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form['email']
            file = request.form['file']
            uid = current_user.id

            directory=Directory(
                name=name,
                surname=surname,
                uid=uid,
                email=email,
                file=file,
            )
            
            session.add(directory)
            session.commit()

            return redirect(url_for("directory"))
        except Exception as exc:
            return redirect(url_for('directory')), flash(exc)

    all_dir = session.query(Directory).all()
    return render_template('directory.html', all_dir=all_dir)
     
@app.route('/registration', methods=["POST", "GET"])
def registration():
        if current_user.is_authenticated:
             return redirect(url_for("home"))
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            new_user= User(
                username = username,
                password=password,
                email = email,
            )
            try:
                session.add(new_user)
                session.commit()
                return redirect(url_for("login")), flash("Дякуємо за реєстрацію!")
            except Exception as exc:
                  return flash(exc)
        return render_template('registration.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
        if current_user.is_authenticated:
             return redirect(url_for("home"))
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            user = session.query(User).filter_by(email=email).first()
            if not user:
                flash("Error!")
                return redirect(url_for("registration"))
            else:
                login_user(user)
                return redirect(url_for("home"))

        return render_template('login.html', form=form)

@app.route('/log_out')
def log_out():
     logout_user()
     return redirect(url_for('login'))