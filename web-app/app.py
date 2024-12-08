"""
Web Application Entry Point

This script initializes and configures the Flask web application.
It sets up:
- Flask app initialization
- Secret key configuration for session management
- Integration with Flask-Login for user authentication
- Registration of blueprints for modular application structure

Modules and Packages:
- Flask: Core framework for the web application
- Flask-Login: Manages user authentication and session handling
- Custom Modules:
  - `database.db`: Database connection and management
  - `user.user`: User management logic and blueprints

Routes:
- (Commented out) Main route for the homepage

Blueprints:
- User blueprint: Handles user-related routes under the `/user` prefix
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required, logout_user
from database import db
from user.user import user, login_manager

app = Flask(__name__)
app.secret_key = "secret_key"  # needed for flask login sessions

login_manager.init_app(app)
app.register_blueprint(user, url_prefix="/user")

" Route on Launch "
@app.route("/")
def index():
    """Redirect to right page if logged in or not"""
    if current_user.is_authenticated:
        return render_template("Calendar.html")
    return redirect(url_for("user.login"))

" Route for signup page "
@app.route("/signup")
def signup():
    """Render Signup page"""
    return render_template("Signup.html")

" Route for login page "
@login_required
@app.route("/menu")
def menu():
    """Render menu page"""
    return render_template("Menu.html")

" Route for successful login"
@login_required
@app.route("/calendar")
def calendar():
    """Render calendar page"""
    return render_template("Calendar.html")

" Route for analytics section "
@app.route("/analytics")
@login_required
def analytics():
    """Render Analytics page"""
    return render_template("Analytics.html")

" Route for search section "
@app.route("/search")
@login_required
def search():
    """Render Search page"""
    return render_template("Search.html")

" Route for user info page "
" Contains First Name, Last Name, and Email"
@app.route("/user-info", methods=["GET", "POST"])
@login_required
def user_info():
    """Handle displaying and updating user information"""
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")

        db.users.update_one(
            {"email": current_user.email},
            {"$set": {"firstname": firstname, "lastname": lastname}}
        )

        return redirect(url_for("user_info"))

    user_data = db.users.find_one({"email": current_user.email})

    user_info = {
        "email": user_data["email"],
        "firstname": user_data.get("firstname", ""),
        "lastname": user_data.get("lastname", ""),
    }

    return render_template("edit-user-info.html", user_info=user_info)

" Delete account route"
@app.route("/delete-acct")
@login_required 
def delete_acct():
    return render_template("delete-acct.html")

" Logout route redirecting to sign in page"
@app.route('/logout')
def logout():
    """Log out the user and redirect to the login page"""
    logout_user()  # This function logs out the current user
    return redirect(url_for('user.login'))  # Redirect to the login page




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
