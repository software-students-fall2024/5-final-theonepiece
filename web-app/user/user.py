from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    session,
    flash,
    jsonify,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    UserMixin,
)
from flask_bcrypt import Bcrypt
from database import db
from bson import ObjectId
from dotenv import load_dotenv
import os
import google.generativeai as genai

user = Blueprint("user", __name__)
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "user.login"

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

class User(UserMixin):
    def __init__(
        self, email, password=None, firstname=None, lastname=None, events=None
    ):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.events = events if events else []
        self.id = email  # no username, just use email

    @staticmethod
    def find_by_email(db, email):
        return db.users.find_one({"email": email})

    @staticmethod
    def create_user(db, email, password, firstname, lastname):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user_data = {
            "email": email,
            "password": hashed_password,
            "firstname": firstname,
            "lastname": lastname,
            "events": [],
        }
        return db.users.insert_one(user_data)

    @staticmethod
    def validate_login(db, email, password):
        user = db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user["password"], password):
            return User(
                email=user["email"],
                password=user["password"],
                firstname=user.get("firstname"),
                lastname=user.get("lastname"),
                events=user.get("events", []),
            )
        return None

    def add_event(self, db, event):
        """user-side add an event"""
        db.users.update_one({"email": self.email}, {"$push": {"events": event}})

    def get_events(self, db):
        user_data = db.users.find_one({"email": self.email})
        return user_data.get("events", [])

    def delete_event(self, db, event_id):
        """user-side delete event"""
        db.users.update_one(
            {"email": self.email}, {"$pull": {"events": {"_id": event_id}}}
        )

    def edit_event(self, db, event_id, updated_event):
        """user-side in database edit event by ID"""
        db.users.update_one(
            {"email": self.email, "events._id": event_id},
            {
                "$set": {
                    "events.$.Amount": updated_event.get("Amount"),
                    "events.$.Category": updated_event.get("Category"),
                    "events.$.Date": updated_event.get("Date"),
                    "events.$.Memo": updated_event.get("Memo"),
                }
            },
        )


@login_manager.user_loader
def load_user(user_id):
    user_data = User.find_by_email(db, user_id)
    if user_data:
        return User(
            email=user_data["email"],
            firstname=user_data.get("firstname"),
            lastname=user_data.get("lastname"),
            events=user_data.get("events", []),
        )
    return None


# default event categories
DEFAULT_CATEGORIES = [
    "Food",
    "Rent",
    "Phone",
    "Transportation",
    "Education",
    "Entertainment",
]

# user routes


@user.route("/add-event", methods=["POST"])
@login_required
def add_event():
    """POST request accept JSON payload to add event"""
    data = request.json
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date")
    memo = data.get("memo")

    event = {
        "_id": str(ObjectId()),
        "Amount": float(amount),
        "Category": category,
        "Date": date,
        "Memo": memo,
    }

    current_user.add_event(db, event)
    
    return jsonify({"message": "Event added successfully"}), 200


@user.route("/delete-event/<event_id>", methods=["DELETE"])
@login_required
def delete_event(event_id):
    """DELETE request to remove an event by ID"""
    current_user.delete_event(db, event_id)
    return jsonify({"message": "Event deleted successfully"}), 200


@user.route("/edit-event/<event_id>", methods=["PUT"])
@login_required
def edit_event(event_id):
    """PUT request to edit an event by ID"""
    data = request.json
    updated_event = {
        "Amount": float(data.get("amount")),
        "Category": data.get("category"),
        "Date": data.get("date"),
        "Memo": data.get("memo"),
    }

    current_user.edit_event(db, event_id, updated_event)

    return jsonify({"message": "Event updated successfully"}), 200


@user.route("/get-events", methods=["GET"])
@login_required
def get_events():
    """GET route return all events of user as JSON based on date"""
    filter_date = request.args.get("date")  # format: YYYY-MM-DD

    events = current_user.get_events(db)
    if filter_date:
        events = [e for e in events if e["Date"] == filter_date]
        
    return jsonify(events), 200

@user.route("/search-events/<word>", methods=["GET"])
@login_required
def search_events(word):
    """GET route return all events of user as JSON based on date"""
    if(not word):
        word=""
        
    events = current_user.get_events(db) or []
    print()
    events_category_memo = [e for e in events if (e["Category"] and word.lower() in e["Category"].lower()) or (e["Memo"] and word.lower() in e["Memo"].lower())]
    
    return render_template("Search.html",searchVal=word,events=events_category_memo)
        


@user.route("/analytics-data", methods=["GET"])
@login_required
def analytics_data():
    """Return aggregated analytics data grouped by month and category."""
    events = current_user.get_events(db)

    grouped_data = {}

    for event in events:
        # Extract year and month from Date
        event_date = event["Date"]
        year_month = "-".join(event_date.split("-")[:2])  # Extract "YYYY-MM"

        # Initialize data structure for the month if not present
        if year_month not in grouped_data:
            grouped_data[year_month] = {}

        # Aggregate Amount by Category
        category = event["Category"]
        if category not in grouped_data[year_month]:
            grouped_data[year_month][category] = 0

        grouped_data[year_month][category] += event["Amount"]

    # Debug: Print the grouped data
    print("Grouped Analytics Data:", grouped_data)

    return jsonify(grouped_data), 200

@user.route("/ai-analysis", methods=["POST"])
@login_required
def ai_analysis():
    """Generate AI insights based on user's events."""
    try:
        user_events = current_user.get_events(db)

        # format events into a string for the AI
        events_summary = "\n".join(
            [f"- {event['Category']}: ${event['Amount']} on {event['Date']} ({event['Memo']})"
             for event in user_events]
        )

        prompt = (
            f"Make sure to reference the specific event or event(s) by their memo or category when specifying tips.\n"
            f"Do not return any JSON or markdown. Only return plaintext plain-english responses.\n"
            f"When providing budget-saving tips, make sure to reference how much money they spent in that specific category or event.\n"
            f"If provided more than 3 events, focus on giving suggestions to save costs on only the most expensive categories.\n"
            f"Provide budget-saving tips based on these user events provided in JSON format. Be as concise as possible:\n\n{events_summary}"
        )

        # generate AI content
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content(prompt)

        return jsonify({"analysis": response.text}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Unable to analyze data"}), 500



@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.validate_login(db, email, password)
        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password. Try again.", "error")
    return render_template("Login.html")


@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        existing_user = User.find_by_email(db, email)
        if existing_user:
            flash("An account with that email already exists!", "error")
        else:
            User.create_user(db, email, password, firstname, lastname)
            return redirect(url_for("user.login"))
    return render_template("Signup.html")


@user.route("/delete-acct", methods=["POST", "GET"])
@login_required
def delete_account():
    """Delete the logged-in user's account."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == current_user.email:
            user = db.users.find_one({"email": email})

            if user and bcrypt.check_password_hash(user["password"], password):
                db.users.delete_one({"email": email})

                logout_user()

                flash("Your account has been successfully deleted.", "success")
                return redirect(url_for("user.login"))
            else:
                flash("Invalid email or password. Please try again.", "error")
        else:
            flash("The provided email does not match the current user.", "error")

    return render_template("delete-acct.html")


@user.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("user.login"))
