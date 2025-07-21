
console.log("JS externo cargado correctamente.");
function cargarLocal(url, id) {
    fetch("/local-img?url=" + encodeURIComponent(url))
        .then(res => res.text())
        .then(base64 => {
            console.log("Base64 recibido:", base64.slice(0, 100)); // muestra un fragmento
            if (base64 && base64.startsWith("data:image")) {
                document.getElementById(id).src = base64;
            } else {
                console.warn("No se recibió imagen válida");
            }
        })
        .catch(err => console.error("Error en carga local:", err));
}
