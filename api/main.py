from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route pour scraper des livres
@app.route('/book', methods=['GET'])
def scrape_books():
    # URL du site à scraper (Books to Scrape)
    url = 'https://books.toscrape.com/'

    # Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url)

    # Vérifier si la requête est réussie (200 OK)
    if response.status_code == 200:
        # Analyser le HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraire les titres et les prix des livres
        books = soup.find_all('article', class_='product_pod')
        books_data = []
        for book in books:
            title = book.h3.a['title']  # Titre du livre
            price = book.find('p', class_='price_color').get_text()  # Prix du livre
            books_data.append({'title': title, 'price': price})

        # Retourner les données en format JSON
        return jsonify(books_data)
    else:
        return jsonify({"error": f"Échec de la requête, code de réponse : {response.status_code}"}), 500

# Lancer l'application sur le port 0000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
