from flask import Flask, render_template
from scraper import obtener_galeria
from scraper_2 import obtener_detalles
import os
app = Flask(__name__)
web_1 = "https://nhentai.net"  # 🔁 Cambia por tu URL real

from flask import Flask, render_template
from scraper import obtener_galeria
from scraper_2 import obtener_detalles

@app.route("/")
def galeria():
    resultado = obtener_galeria(web_1)
    return render_template(
        "galeria.html",
        imagenes=resultado["imagenes"],
        botones=resultado["botones"],
        web_1=web_1
    )

@app.route("/g/<code>")
def detalles(code):
    resultado = obtener_detalles(web_1, code)
    return render_template(
        "detalles.html",
        texto=resultado["texto"],
        imagenes=resultado["imagenes"],
        code=code,
        web_1=web_1
    )

from flask import request

@app.route("/<path:subpath>")
def ruta_personalizada(subpath):
    full_url = f"{web_1}{request.full_path}"
    resultado = obtener_galeria(full_url)
    return render_template(
        "galeria.html",
        imagenes=resultado["imagenes"],
        botones=resultado["botones"],
        web_1=full_url
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # usa 5000 como fallback
    app.run(host="0.0.0.0", port=port)

