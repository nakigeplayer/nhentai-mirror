#!/bin/bash

# Crear carpeta si no existe
mkdir -p server

# Iniciar servidor estático en segundo plano
python3 -m http.server -d server --bind 0.0.0.0 --port 9999 &

# Iniciar Flask como proceso principal
python3 app.py
