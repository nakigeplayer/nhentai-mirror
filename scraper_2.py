import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import base64

def obtener_detalles(web_1, code):
    base_url = f"{web_1}/g/{code}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    texto_final = []
    imagenes = []

    # Parte 1: Textos, encabezados y etiquetas
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error al acceder:", e)
        return {"texto": "", "imagenes": []}

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", id="content")
    if not content:
        print("No se encontró div#content")
        return {"texto": "", "imagenes": []}

    info = content.find("div", id="bigcontainer")
    if info:
        info_block = info.find("div", id="info-block")
        if info_block:
            info_div = info_block.find("div", id="info")
            if info_div:
                for nivel in ["h1", "h2", "h3"]:
                    encabezado = info_div.find(nivel, class_="title")
                    if encabezado:
                        partes = []
                        for clase in ["before", "pretty", "after"]:
                            span = encabezado.find("span", class_=clase)
                            if span and span.text.strip():
                                partes.append(span.text.strip())
                        if partes:
                            texto_final.append(" ".join(partes))

    seccion_tags = content.find("section", id="tags")
    if seccion_tags:
        contenedores = seccion_tags.find_all("div", class_="tag-container")
        for cont in contenedores:
            titulo_nodo = cont.find(text=True, recursive=False)
            titulo = titulo_nodo.strip().rstrip(":") if titulo_nodo else "Sin título"
            texto_final.append(f"{titulo}:")

            if titulo.lower() == "pages":
                valor = cont.find("span", class_="tags")
                if valor:
                    texto_final.append(valor.text.strip())
                continue

            if titulo.lower() == "uploaded":
                time_tag = cont.find("time")
                if time_tag and time_tag.text.strip():
                    texto_final.append(time_tag.text.strip())
                continue

            tags_span = cont.find("span", class_="tags")
            if tags_span:
                for a_tag in tags_span.find_all("a"):
                    href = a_tag.get("href", "")
                    nombre_span = a_tag.find("span", class_="name")
                    nombre = nombre_span.text.strip() if nombre_span else ""
                    if href and nombre:
                        texto_final.append(f'<a href="{href}">{nombre}</a>')

    thumbnail_container = content.find("div", id="thumbnail-container")
    thumbs = thumbnail_container.find("div", class_="thumbs") if thumbnail_container else None
    thumb_divs = thumbs.find_all("div", class_="thumb-container") if thumbs else []
    total = len(thumb_divs)

    for i in range(1, total + 1):
        pagina_url = f"{web_1}/g/{code}/{i}/"
        try:
            res = requests.get(pagina_url, headers=headers, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            continue

        sub_soup = BeautifulSoup(res.text, "html.parser")
        sub_content = sub_soup.find("div", id="content")
        if not sub_content:
            continue

        section = sub_content.find("section", id="image-container")
        if section:
            img_tag = section.find("img")
            if img_tag and img_tag.get("src"):
                src = img_tag.get("src")
                img_url = urljoin(web_1, src)

                # Guardar el enlace directo de la imagen en la lista
                imagenes.append(img_url)

                # # try:
                #     # img_response = requests.get(img_url, headers=headers, timeout=10)
                #     # img_response.raise_for_status()
                #     # content_type = img_response.headers.get("Content-Type", "image/jpeg")
                #     # img_base64 = base64.b64encode(img_response.content).decode("utf-8")
                #     # data_uri = f"data:{content_type};base64,{img_base64}"
                #     # imagenes.append(data_uri)
                # # except requests.exceptions.RequestException:
                #     # continue

    return {
        "texto": "\n".join(texto_final),
        "imagenes": imagenes
    }
