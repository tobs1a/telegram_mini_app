from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Flask-App einrichten
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Datenbankmodell für Variationen
class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Startseite: Liste der Variationen anzeigen
@app.route("/")
def index():
    variations = Variation.query.all()
    return render_template("index.html", variations=variations)

# Variation bewerten und Bilder hinzufügen
@app.route("/variation/<int:id>", methods=["GET", "POST"])
def variation(id):
    variation = Variation.query.get_or_404(id)
    ratings = Rating.query.filter_by(variation_id=id).all()
    total_stars = sum(r.stars for r in ratings)
    average_stars = total_stars / len(ratings) if ratings else 0

    if request.method == "POST":
        stars = int(request.form.get("stars"))
        comment = request.form.get("comment")
        file = request.files.get("image")
        filename = None
        if file:
            upload_folder = os.path.join("static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            filename = file.filename
            file.save(os.path.join(upload_folder, filename))

        new_rating = Rating(variation_id=id, stars=stars, comment=comment, image_filename=filename)
        db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for("variation", id=id))

    return render_template("variation.html", variation=variation, ratings=ratings, average_stars=average_stars)

# Initialisiere die Datenbank und füge Variationen hinzu
@app.before_first_request
def create_tables():
    db.create_all()
    if not Variation.query.first():
       variations = [
    "Costa Canna Dynamics - forte", "Demecan 25:01 Calama", "IMC 17/1", "Nimbus EASY 24/1",
    "Tilray THC18 Spotlight Porto", "Demecan 20:01 Florestura", "Cannamedical Indica Forte",
    "Pedanios 31/1 COS-CA", "Peace Naturals 33/1 GC", "29/1 Amici WC", "madrecan 18/1 SHA",
    "remexian 27/1 PSL", "enua 22/1 WCK CA", "remexian 27/1 PBB", "17/1 N!CE DD", 
    "18/1 N!CE Cannabisblüten CC", "Cookies MD 22/1", "Peace Naturals 29/1 GC", 
    "alephSana amber 26/1", "Nimbus EASY 22/1", "MAC 1+", "420 Natural 25/1 CA GG4",
    "Peace Naturals 31/1 GC", "Pedanios 27/1 PND-CA", "Demecan 24:01 Cresina", 
    "Peace Naturals 31/1 SC", "420 Evolution 30/1 CA GMO", "26/1 N!CE C", 
    "Cannabis Flos 20/1 UY Ku.Big Buddah", "Cannabis Flos 23/1 CO Ku.Kush Mints",
    "420 Natural 18/1 CA ZRP", "Tilray THC25 Spotlight Montevideo", "RE:CANNIS 16/1 Sativa",
    "Nimbus 26/1 ZRP", "Mother 28 B8 CAN", "420 Natural 22/1 CA GG4", "CannabiStada 19/1",
    "CannabiStada 25/1 GG", "Typ 1 Aphria", "Cannamedical Sativa classic", "Pedanios 10/10 EQI-CA",
    "420 Compound 27/1 CA GAP", "enua 25/1 CCK CA", "CRAFT Black Triangle 27:01", 
    "Navcora THC22 Spotlight Montevideo", "CM 20/1 GG4", "AVAAY 28/1 KH", "BG GOG",
    "CM 20/1 LLY", "Adrex 20 KBN COL", "Canopy TCK 27", "MC Lean Drop", "Avaay 22/1 LSB",
    "madrecan 18/1 MAC", "Canopy LSK 16", "420 Evolution 20/1 CA PLD", "IMC THC22 T05",
    "enua 27/1 DSH CA", "Bathera 25/1", "Drapalin 27/1 Pink Gas", "madrecan 18/1 RCH", 
    "ADREX 29/1 SPC CAN", "Tilray THC25 Indica No.2", "GROW 18 HF Mac", "Aleph Citrin 23/1",
    "Cannamedical Indica forte NG", "Bathera 30/1 Polar Pop", "Canopy GDB 12", 
    "Cannamedical Indica ultra SF", "AVAAY 21/1 PYC", "LOT 420 GLT", "ADREX 24/1 VC CAN",
    "31/1 Amici AS", "Hexacan 22:01", "OHT CKZ 1", "CNBS GELO 20/1", "Cannamedical Hybrid classic",
    "CM 24/1 ZA", "Cannamedical Sativa vita", "Cannabis Flos 22/1 PT Ku. Sirius DAB Canify",
    "420 Evolution 27/1 CA ICC", "Tilray THC15 Spotlight Porto", "Roxton Air BS01", 
    "IMC THC27 PBM", "23/1 N!CE C", "Tilray THC22 Spotlight Porto", "AVAAY 23/1 CRE",
    "420 Evolution 25/1 CA BUL", "Tilray THC18 Spotlight Porto", "remexian 22/1 GG4 minis",
    "Blackrose 14 PT", "420 Evolution 25/1 CA ICC", "IMC THC20 T02", "420 Compound 30/1 CA GAP",
    "CM 20/1 Karl OG", "420 Evolution 30/1 CA FLM", "Cannamedical Hybrid forte NM",
    "Cannamedical Balanced forte", "420 Evolution 27/1 CA FLM", "420 Evolution 27/1 CA STR",
    "CannabiStada 17/1", "Bathera 23/1", "remexian 25/1", "Alpinolin 22/1", 
    "Drapalin 1/17 Maluti CBD", "Vasco WR", "Weeco 20/1", "Weeco 23/1", "Therismos 25/1 DSM",
    "ACA 24/1 C", "420 Compound 22/1 CA MWZ", "remexian 24/1 GRG", "Tilray THC22 Spotlight Porto",
    "remexian 30/1 PRT TFT", "Cannamedical Balanced classic", "420 Evolution 25/1 CA MAC",
    "Sumo Canada Craft No.4", "Navcora THC22 Spotlight Porto", "Tilray THC22 Sativa No.2",
    "Stratus Indica THC20", "AVAAY Signature 28/1 GPM", "27/1 Amici WC", "Ostara Balance", 
    "420 Evolution 25/1 CA TGP", "Bediol", "CM 24/1 Spritzer", "IMC THC22 T01", "IMC THC21 T01",
    "IMC THC20 T01 HK", "Cannabis 1A 18/1"
        ]
        for name in variations:
            db.session.add(Variation(name=name))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
