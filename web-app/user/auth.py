from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, login_user
from user.models import User
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client["fiscal_db"]

auth = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    user_data = User.find_by_username(db, user_id)
    if user_data:
        return User(username=user_data["username"])
    return None


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.validate_login(db, username, password)
        if user:
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("Login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        existing_user = User.find_by_email(db, email)
        if existing_user:
            flash("Username already exists", "danger")
        else:
            User.create_user(db, email, password, firstname, lastname)
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("Signup.html")



