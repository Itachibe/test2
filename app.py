from flask import Flask, jsonify, request, render_template
import requests
import json

app = Flask(__name__)

# URLs de l'API
urls = [
    "https://librex.mikata.ru/api.php?q=gentoo&p=2&t=0",
    "https://librex.pufe.org/api.php?q=gentoo&p=2&t=0",
    "https://search.femboy.hu/api.php?q=gentoo&p=2&t=0"
]

# Mapping des valeurs de type de recherche à leurs codes respectifs
type_mapping = {
    "text": 0,
    "image": 1,
    "video": 2,
    "torrent": 3,
    "tor": 4
}

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        # Récupération des paramètres de la requête GET
        keyword = request.args.get("q")
        page = request.args.get("p", 0)
        search_type = request.args.get("t", "text")
    elif request.method == "POST":
        # Récupération des paramètres de la requête POST
        keyword = request.form.get("q")
        page = request.form.get("p", 0)
        search_type = request.form.get("t", "text")

    # Vérification de la valeur de search_type et conversion en entier
    if search_type in type_mapping:
        search_type = type_mapping[search_type]
    else:
        search_type = 0

    # Paramètres de la requête
    params = {
        "q": keyword,
        "p": page,
        "t": search_type
    }

    # Essayer chaque URL jusqu'à ce qu'une réponse valide soit obtenue
    for url in urls:
        response = requests.get(url, params=params)

        # Si la réponse est valide, utiliser les données
        if response.status_code == 200:
            data = json.loads(response.text)
            if search_type == 0:
                return render_template("result.html", data=data["results"])
            elif search_type == 1:
                return render_template("image_result.html", data=data["results"])
            elif search_type == 2:
                return render_template("video_result.html", data=data["results"])
            elif search_type == 3:
                return render_template("torrent_result.html", data=data["results"])
            elif search_type == 4:
                return render_template("tor_result.html", data=data["results"])

    # Si aucune réponse valide n'a été obtenue, renvoyer une erreur
    return "La requête a échoué pour toutes les URLs"

@app.route("/search", methods=["GET", "POST"])
def search_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
