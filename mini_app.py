
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Lade die index.html aus dem templates-Ordner
    return render_template("index.html")

@app.route("/login")
def login():
    # Einfache Rückgabe für die Login-Seite als Platzhalter
    return "<h1>Login-Seite wird hier bald hinzugefügt!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
