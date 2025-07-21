import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import base64

def obtener_galeria(web_1):
    url = web_1
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, como Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error al acceder:", e)
        return {"imagenes": [], "botones": []}

    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []

    content_div = soup.find("div", id="content")
    if not content_div:
        print("No se encontró div#content")
        return {"imagenes": [], "botones": []}

    index_container = content_div.find("div", class_="container index-container")
    if not index_container:
        print("No se encontró div.container.index-container")
        return {"imagenes": [], "botones": []}

    for gallery_div in index_container.find_all("div", class_="gallery"):
        enlace = gallery_div.find("a")
        if not enlace:
            continue

        # Extraer imagen absoluta desde <img class="lazyload">
        img_tag = enlace.find("img", class_="lazyload")
        src_relativo = img_tag.get("data-src", "") if img_tag else ""
        src_absoluto = urljoin(web_1, src_relativo)

        # Guardar directamente el enlace de la imagen en lugar de convertir a base64
        src_data_uri = src_absoluto

        # # Descargar imagen y convertir a base64
        # try:
        #     img_response = requests.get(src_absoluto, headers=headers, timeout=10)
        #     img_response.raise_for_status()
        #     content_type = img_response.headers.get("Content-Type", "image/jpeg")
        #     img_base64 = base64.b64encode(img_response.content).decode("utf-8")
        #     src_data_uri = f"data:{content_type};base64,{img_base64}"
        # except requests.exceptions.RequestException:
        #     src_data_uri = ""

        href = enlace.get("href", "")
        combinacion = href.strip("/").split("/g/")[-1]

        caption_div = enlace.find("div", class_="caption")
        caption = caption_div.text.strip() if caption_div else ""

        resultados.append({
            "src": src_data_uri,
            "caption": caption,
            "combinacion": combinacion,
            "url_completa": href
        })

    botones = []
    paginacion = soup.find("section", class_="pagination")
    if paginacion:
        for a_tag in paginacion.find_all("a"):
            href = a_tag.get("href", "").strip()
            clase = a_tag.get("class", [])

            if "first" in clase:
                nombre = "First"
            elif "previous" in clase:
                nombre = "Before"
            elif "next" in clase:
                nombre = "Next"
            elif "last" in clase:
                nombre = "Last"
            elif "page" in clase:
                nombre = a_tag.text.strip()
            else:
                continue

            botones.append({
                "nombre": nombre,
                "href": href
            })

    return {"imagenes": resultados, "botones": botones}
