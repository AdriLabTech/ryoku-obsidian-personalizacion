#!/usr/bin/env python3
"""Instala el tema de bloqueo «pixel-obsidian» (qylock) con el fondo del perfil Obsidian.

Parte de `pixel-hollowknight` (GPLv3, ya instalado por Ryoku) y cambia el vídeo de fondo (el disco de
semitono con torii, con respiración lenta, grano monocromo y una banda de barrido), los acentos
(grises) y la fuente (Space Grotesk). Main.qml mantiene su estructura. El rojo de error se conserva:
es un color semántico.

Uso: lockscreen_obsidian.py     (luego: ryoku-hub lock set pixel-obsidian  -> pide pkexec para el greeter)
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("~/.local/share/qylock/themes/pixel-hollowknight").expanduser()
DST = Path("~/.local/share/qylock/themes/pixel-obsidian").expanduser()
WALL = Path("~/Imágenes/Wallpapers/perfil-obsidian.png").expanduser()
FONT = Path("/usr/share/fonts/OTF/SpaceGrotesk-Medium.otf")
FRAMES, FPS = 120, 24         # 5 s en bucle


def frame(base, i, rng):
    """Fotograma i: respiración de brillo (un ciclo por bucle), banda de barrido y grano igual en los tres canales."""
    t = i / FRAMES
    a = base * (0.90 + 0.10 * np.sin(2 * np.pi * t))
    y0 = int(t * (a.shape[0] + 160)) - 160
    a[max(y0, 0):max(y0 + 160, 0)] *= 1.05
    a += rng.normal(0, 3.0, a.shape[:2])[..., None]
    return np.clip(a, 0, 255).astype(np.uint8)


def main():
    for f in (SRC, WALL, FONT):
        if not f.exists():
            sys.exit(f"falta {f}")
    base = np.array(Image.open(WALL).convert("L").resize((1920, 1080), Image.LANCZOS), dtype=np.float32)
    base = np.repeat(base[..., None], 3, axis=2)
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("bg.mp4", "font"))
    (DST / "font").mkdir()
    shutil.copy2(FONT, DST / "font" / FONT.name)
    rng = np.random.default_rng(5)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(FRAMES):
            Image.fromarray(frame(base, i, rng)).save(f"{tmp}/f{i:03d}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%03d.png",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(DST / "bg.mp4")], check=True)
    qml = (DST / "Main.qml").read_text()
    qml = qml.replace('"#f5aa5b"', '"#E6E6E9"').replace('"#8498ab"', '"#8E8E96"').replace('"#d0050403"', '"#d00B0B0D"')
    (DST / "Main.qml").write_text(qml)
    conf = (DST / "theme.conf").read_text()
    conf = re.sub(r"color=.*", "color=#E6E6E9", conf)
    conf = re.sub(r"font=.*", "font=Space Grotesk", conf)
    (DST / "theme.conf").write_text(conf)
    meta = (DST / "metadata.desktop").read_text().replace("pixel-hollowknight", "pixel-obsidian")
    (DST / "metadata.desktop").write_text(meta)
    (DST / "PROVENANCE.txt").write_text(
        "Pixel Obsidian: derivado de pixel-hollowknight (qylock, Darkkal44, GPLv3; ver LICENSE).\n"
        "Cambios: bg.mp4 generado del fondo del perfil Obsidian (ryoku-perfiles/tools/lockscreen_obsidian.py),\n"
        "acentos en grises (Main.qml, theme.conf) y fuente Space Grotesk (SIL OFL).\n")
    print("tema de bloqueo ->", DST, f"({(DST / 'bg.mp4').stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
