from flask import Flask, render_template

from flask import request
from scraper import obtener_galeria
from scraper_2 import obtener_detalles
import os
app = Flask(__name__)

web_1 = "https://nhentai.net"  # 🔁 Cambia por tu URL real

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
    
@app.route("/local-img")
def cargar_local_img():
    img_url = request.args.get("url")
    if not img_url:
        return "", 400

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        res = requests.get(img_url, headers=headers, timeout=10)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type") or "image/jpeg"
        b64 = base64.b64encode(res.content).decode("utf-8")
        return f"data:{content_type};base64,{b64}", 200
    except Exception as e:
        print("Error al generar imagen base64:", e)
        return "", 500


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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
