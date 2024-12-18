
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Mini-App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }
            h1 { color: #333; }
            button {
                padding: 10px 20px;
                margin-top: 20px;
                font-size: 18px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Willkommen zur Telegram Mini-App!</h1>
        <p>Dies ist eine einfache Demo einer Telegram Mini-App.</p>
        <button onclick="alert('Danke für deinen Klick!')">Klick mich!</button>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=False)
