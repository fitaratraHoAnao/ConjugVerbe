from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/conjuguer/<verbe>', methods=['GET'])
def conjuguer(verbe):
    # URL du verbe à conjuguer
    url = f'https://leconjugueur.lefigaro.fr/php5/index.php?verbe={verbe}'

    # Envoyer une requête GET à la page
    response = requests.get(url)

    # Vérifier que la requête est réussie
    if response.status_code == 200:
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire la section de conjugaison
        conjugaison_section = soup.find_all('div', class_='temps')
        conjugaison_data = {}

        # Boucler sur chaque section pour récupérer les conjugaisons
        for section in conjugaison_section:
            temps = section.find('h3').get_text(strip=True)
            conjugaison = [li.get_text(strip=True) for li in section.find_all('li')]
            conjugaison_data[temps] = conjugaison

        # Retourner les conjugaisons sous forme de JSON
        return jsonify(conjugaison_data)
    else:
        return jsonify({'error': 'Impossible de récupérer la conjugaison'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
