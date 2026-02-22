from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin pour le frontend

# Données fictives pour la démonstration
etudiants_data = [
    {"id": 1, "nom": "Jean Dupont", "classe": "Tle S1"},
    {"id": 2, "nom": "Marie Curie", "classe": "1ère L2"},
    {"id": 3, "nom": "Isaac Newton", "classe": "Tle S2"},
    {"id": 4, "nom": "Albert Einstein", "classe": "2nde S"},
]

presences_data = [
    {"nom": "Jean Dupont", "date": "2026-02-21", "statut": "Présent"},
    {"nom": "Marie Curie", "date": "2026-02-21", "statut": "Absente"},
    {"nom": "Isaac Newton", "date": "2026-02-20", "statut": "Présent"},
    {"nom": "Albert Einstein", "date": "2026-02-20", "statut": "Présent"},
]

@app.route('/etudiants', methods=['GET'])
def get_etudiants():
    return jsonify(etudiants_data)

@app.route('/presences', methods=['GET'])
def get_presences():
    return jsonify(presences_data)

if __name__ == '__main__':
    print("Serveur backend IDENTIA lancé sur http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
