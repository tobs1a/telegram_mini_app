
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secretkey123'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(100), nullable=True)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("profile", telegram_id=session["telegram_id"]))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        telegram_id = request.form["telegram_id"]
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='sha256')
        if User.query.filter_by(telegram_id=telegram_id).first():
            return "Benutzer existiert bereits!"
        new_user = User(telegram_id=telegram_id, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        telegram_id = request.form["telegram_id"]
        password = request.form["password"]
        user = User.query.filter_by(telegram_id=telegram_id).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["telegram_id"] = user.telegram_id
            return redirect(url_for("profile", telegram_id=user.telegram_id))
        return "Falsche Telegram-ID oder Passwort!"
    return render_template("login.html")

@app.route("/profile/<telegram_id>", methods=["GET", "POST"])
def profile(telegram_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if request.method == "POST":
        user.username = request.form["username"]
        user.bio = request.form["bio"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("profile", telegram_id=telegram_id))
    return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("telegram_id", None)
    return redirect(url_for("index"))

if not os.path.exists("users.db"):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
