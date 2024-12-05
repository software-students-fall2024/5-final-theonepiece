""" 
Web app frontend
"""

from flask import Flask, render_template

app = Flask(__name__)


# @app.route("/")
# def home():
#     """Render main page"""
#     return render_template("index.html")

@app.route("/")
def login():
    """Render login page"""
    return render_template("Login.html")

@app.route("/signup")
def signup():
    """Render Signup page"""
    return render_template("Signup.html")

@app.route("/menu")
def menu():
    """Render menu page"""
    return render_template("Menu.html")

@app.route("/calendar")
def calendar():
    """Render calendar page"""
    return render_template("Calendar.html")

@app.route("/analytics")
def analytics():
    """Render Analytics page"""
    return render_template("Analytics.html")


# write new functions here
if __name__ == "__main__":
    app.run(debug=True, port=8080)
