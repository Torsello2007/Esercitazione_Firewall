from flask import Flask, request, jsonify
from flask_cors import CORS
from database_wrapper import db

app = Flask(__name__)
CORS(app)

# Rotta principale per evitare il 404 quando apri il link
@app.route('/')
def home():
    return "Il backend del ristorante Sushi è attivo! Vai su /prodotti per vedere il menu."

@app.route('/prodotti')
def p():
    return jsonify(db.get_prodotti())

@app.route('/ordini', methods=['GET', 'POST'])
def o():
    if request.method == 'POST':
        db.add_ordine(request.json['tavolo'], request.json['cliente'])
        return jsonify({"status": "ok"})
    return jsonify(db.get_ordini())

@app.route('/stato/<int:id>', methods=['POST'])
def s(id):
    db.set_stato(id, request.json['stato'])
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000)