from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

app = Flask(__name__)

# Route pour effectuer une recherche de conjugaison
@app.route('/recherche', methods=['GET'])
def recherche():
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "La requête est manquante"}), 400

    try:
        # URL de conjugaison du verbe sur le site
        search_url = "https://leconjugueur.lefigaro.fr/conjugaison/verbe/" + urllib.parse.quote(query)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            conjugaison_resultats = []

            # Scrapper les temps de conjugaison (par exemple div.temps contient les temps)
            for item in soup.select('div.temps'):
                conjugaison_resultats.append(item.get_text(strip=True))
            
            # Si aucun résultat n'est trouvé
            if not conjugaison_resultats:
                return jsonify({
                    "query": query,
                    "resultats": ["Aucun résultat trouvé"]
                }), 404
            
            # Retourner les résultats sous forme de JSON
            return jsonify({
                "verbe": query,
                "resultats": conjugaison_resultats
            }), 200
        else:
            return jsonify({"error": "Impossible d'accéder à la page de conjugaison"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Point d'entrée principal
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Utilise le port assigné par Render
    app.run(host='0.0.0.0', port=port, debug=True)
    
