#!/usr/bin/env python3
"""Emblema del perfil Obsidian para fastfetch (assets/emblems/obsidian.png): disco con torii recortado del fondo.

El negro pasa a transparente (por luminancia) para que se funda con la terminal; solo grises.
Requiere el fondo generado: `perfil build obsidian` (o tools/obsidian_scene.py).
"""
from pathlib import Path

import numpy as np
from PIL import Image

WALL = Path.home() / "Imágenes/Wallpapers/perfil-obsidian.png"
OUT = Path(__file__).resolve().parent.parent / "assets/emblems/obsidian.png"


def main():
    im = Image.open(WALL).convert("L").crop((1640, 400, 3080, 1840)).resize((512, 512), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32)
    alpha = np.clip((a - 8) / 40, 0, 1) * 255                 # fondo negro -> transparente
    rgba = np.dstack([np.clip(a * 1.15, 0, 255)] * 3 + [alpha]).astype(np.uint8)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(OUT)
    print("emblema ->", OUT)


if __name__ == "__main__":
    main()
