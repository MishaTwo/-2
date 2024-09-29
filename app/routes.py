from . import app, login_manager
from flask import render_template, request, redirect, flash, url_for
from app.models import User, News, Directory
from app.models.base import session
from app.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd
from werkzeug.utils import secure_filename
import yagmail
import os

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/mailing", methods=["POST", "GET"])
@login_required
def mailing():
    if request.method == 'POST':
        try:
            file_path = request.form["file_path"]
            folder_path = request.form["folder_path"]
            email_column = int(request.form["email_column"])
            file_column = int(request.form["file_column"])
            for i in range(2):
                folder_path = folder_path.replace('"', '')
                file_path = file_path.replace('"', '')
            email_passowrd = current_user.password
            title = request.form["title"]
            from_email = current_user.email

            df = pd.read_excel(file_path)

            emails = df.iloc[:, email_column - 1]
            file_names = df.iloc[:, file_column - 1]
            
            for i in range(len(emails)):
                email = emails[i]
                file_name = file_names[i]
                file_send = yagmail.SMTP(from_email, email_passowrd)
                file = rf"{folder_path}\{file_name}"
                    
                file_send.send(
                    to=email,
                    subject=title,
                    attachments=file

                )
            flash(str("Все розісланно!"))
            return redirect(url_for("mailing"))
        except Exception as exc:
            flash(str(exc))
            return redirect(url_for("mailing"))
    return render_template('mailing_list.html')

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

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")


@app.route('/mail_news', methods=['GET', 'POST'])
def mail_news():
    news = session.query(News).all()
    if request.method == "POST":
        new_id = request.form["new"]
        new = session.query(News).get(new_id)
        image_path = os.path.join('app/static/css/img', new.image)

        os.remove(image_path)
        
        try:
            session.delete(new)
            session.commit()
            return redirect(url_for('mail_news'))
        except Exception as exc:
            return flash(exc)
    return render_template("news.html", news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == "POST":
        news = request.form["news"]
        image = request.files.get('image')
        filename = secure_filename(image.filename)
        image_path = os.path.join('app/static/css/img', filename)


        try:
            image.save(image_path)

            news = News(
                news=news,
                image=filename,
            )
            session.add(news)
            session.commit()
            return redirect(url_for("mail_news"))
        except Exception as exc:
            return flash(exc)
    else:
        return render_template('add_news.html')