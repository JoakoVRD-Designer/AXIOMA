#!/usr/bin/env python3
"""Arma index.html (el reproductor de la presentación) a partir de deck.json y slides/*.html.

Uso:  python3 build.py
Luego abre index.html en el navegador (Chrome recomendado). No necesita internet,
salvo para cargar las tipografías Inter y JetBrains Mono (si no hay, usa Arial).
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
deck = json.load(open(os.path.join(AQUI, "deck.json"), encoding="utf-8"))

secciones = []
for nombre in deck["order"]:
    ruta = os.path.join(AQUI, "slides", nombre + ".html")
    if not os.path.exists(ruta):
        sys.exit(f"Falta slides/{nombre}.html (está en deck.json > order)")
    html = open(ruta, encoding="utf-8").read().strip()
    if not re.match(r"<section\b", html):
        sys.exit(f"slides/{nombre}.html debe empezar con <section ...>")
    secciones.append(html)

fuentes = "".join(
    f'<link rel="stylesheet" href="{f["href"]}">\n' for f in deck.get("faces", {}).values()
)

PLANTILLA = open(os.path.join(AQUI, "player.tpl.html"), encoding="utf-8").read()
salida = (
    PLANTILLA.replace("{{TITULO}}", deck.get("title", "Presentación"))
    .replace("{{FUENTES}}", fuentes)
    .replace("{{SLIDES}}", "\n".join(secciones))
)
open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8").write(salida)
print(f"index.html generado con {len(secciones)} diapositivas: {', '.join(deck['order'])}")
