
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secretkey123'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='image', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(100), nullable=False, default="Anonym")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Seed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = file.filename
            upload_folder = os.path.join("static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            new_image = Image(filename=filename)
            db.session.add(new_image)
            db.session.commit()
            return redirect(url_for("gallery"))
    return render_template("upload.html")

@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    images = Image.query.all()
    if request.method == "POST":
        comment_text = request.form.get("comment")
        username = request.form.get("username")
        image_id = request.form.get("image_id")
        if comment_text and username:
            new_comment = Comment(image_id=image_id, text=comment_text, username=username)
            db.session.add(new_comment)
            db.session.commit()
    return render_template("gallery.html", images=images)

@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    return render_template("calendar.html")

@app.route("/seed-finder", methods=["GET", "POST"])
def seed_finder():
    seeds = Seed.query.all()
    if request.method == "POST":
        search_query = request.form.get("search_query")
        seeds = Seed.query.filter(Seed.name.like(f"%{search_query}%") | Seed.region.like(f"%{search_query}%")).all()
    return render_template("seed_finder.html", seeds=seeds)

if __name__ == "__main__":
    if not os.path.exists("app.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
