from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour scraper les articles du flux RSS
def scrape_bbc_news():
    url = "http://feeds.bbci.co.uk/news/rss.xml"
    response = requests.get(url)

    # Vérifier si la requête a réussi (status code 200)
    if response.status_code == 200:
        # Utiliser lxml comme parser XML
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.findAll('item')

        # Liste pour stocker les articles
        news_items = []
        for i in items:
            news_i = {
                'title': i.title.text if i.title else 'No title',
                'description': i.description.text if i.description else 'No description',
                'link': i.link.text if i.link else 'No link',
                'pubDate': i.pubDate.text if i.pubDate else 'No date'
            }
            news_items.append(news_i)

        return news_items
    else:
        return []

# Route principale pour afficher les articles en JSON
@app.route('/news', methods=['GET'])
def get_news():
    news = scrape_bbc_news()
    return jsonify(news)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
