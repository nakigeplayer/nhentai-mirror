#!/bin/bash

# Render asigna el puerto en $PORT
PORT=${PORT:-8000}

mkdir -p server

# Servidor estático en otro puerto que NO sea $PORT
python3 -m http.server 9999 -d server &

# Flask escucha en el puerto asignado por Render
exec python3 app.py
