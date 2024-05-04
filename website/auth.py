from flask import Blueprint, render_template, request, flash, redirect
from .models import User, UserBooks, Review
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func

auth = Blueprint("auth", __name__)


@auth.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html", user=current_user)

    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    user_username = User.query.filter_by(username=username).first()
    user_email = User.query.filter(func.lower(User.email) == email.lower()).first()
    if user_email:
        flash("Account already exists", category="error")
        return redirect("/login")
    if user_username:
        flash("Username already taken", category="error")
        return redirect("/sign_in")
    if not email or not username or not email or not password1 or not password2:
        flash("Missing data", category="error")
        return redirect("/sign_in")
    elif len(password1) < 6:
        flash("Password needs to be at least 6 character long", category="error")
    elif password1 != password2:
        flash("Password don't match", category="error")
    else:
        new_user = User(
            email=email, username=username, password=generate_password_hash(password1)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Account created!", category="success")
        return redirect("/")
    return redirect("/sign_in")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", user=current_user)

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash("Logged in", category="success")
            return redirect("/")
        else:
            flash("Wrong password", category="error")
            return redirect("/login")
    else:
        flash("User doesn't exists", category="error")
        return redirect("/login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@auth.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "GET":
        return render_template("delete_account.html", user=current_user)

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            db.session.query(UserBooks).filter(
                UserBooks.person_id == current_user.id
            ).delete()
            db.session.query(Review).filter(
                Review.person_id == current_user.id
            ).delete()
            db.session.query(User).filter(User.id == current_user.id).delete()
            db.session.commit()
            return redirect("/sign_in")
        else:
            flash("Wrong password", category="error")
            return redirect("/delete_account")
    else:
        flash("User doesn't exists", category="error")
        return redirect("/delete_account")


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile.html", user=current_user)

    username = request.form.get("username")
    email = request.form.get("email")
    prev_password = request.form.get("prev_password")
    print(prev_password)
    new_password = request.form.get("new_password")
    user_username = User.query.filter_by(username=username).first()
    print(user_username)
    user_email = User.query.filter_by(email=email).first()
    if prev_password and not check_password_hash(current_user.password, prev_password):
        flash("Wrong password", category="error")
        return redirect("/profile")
    elif new_password and len(new_password) < 6:
        flash("New password needs to be 6 characters long", category="error")
        return redirect("/profile")
    if not email or not username:
        flash("Missing data", category="error")
    elif user_email and email != current_user.email:
        flash("Email already taken", category="error")
    elif user_username and username != current_user.username:
        flash("Username already taken", category="error")
    else:
        current_user.username = username
        current_user.email = email
        if prev_password and new_password:
            current_user.password = generate_password_hash(new_password)
        db.session.commit()
        login_user(current_user, remember=True)
        flash("Data changed!", category="success")
        return redirect("/")
    return redirect("/profile")
