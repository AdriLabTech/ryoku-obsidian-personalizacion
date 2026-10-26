#!/usr/bin/env python3
"""Tema de iconos `ryoku-obsidian`: Papirus-Dark pasado a escala de grises, sigue siendo vectorial.

Misma geometría y grosor que Papirus (un solo conjunto coherente); solo cambia el color de cada
relleno/trazo a un gris con su misma luminancia, dentro del rango de la paleta Obsidian.
Se instala en ~/.local/share/icons/ryoku-obsidian; los enlaces simbólicos se conservan.

    icons_obsidian.py [--destino DIR] [--externos]   (--externos: solo apps con icono propio, tema ya generado)
"""
import colorsys
import os
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

SRC = Path("/usr/share/icons/Papirus-Dark")
DEST = Path.home() / ".local/share/icons/ryoku-obsidian"
SIZES = {"16x16", "22x22", "24x24", "32x32", "48x48", "64x64"}   # tamaños que declara el tema
LO, HI = 0x24, 0xE6          # gris más oscuro y más claro que se emiten (la paleta va de #0B0B0D a #E6E6E9)

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
RGB = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")
NAMED = {"white": "#ffffff", "black": "#000000"}


def grey(r, g, b):
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    v = round(LO + lum ** 0.9 * (HI - LO))
    return f"#{v:02x}{v:02x}{v:02x}"


def conv_hex(m):
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return grey(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def conv_rgb(m):
    return grey(*(int(x) for x in m.groups()))


def convert(text):
    text = HEX.sub(conv_hex, text)
    text = RGB.sub(conv_rgb, text)
    return re.sub(r'(fill|stroke|stop-color|flood-color)="(white|black)"', lambda m: f'{m.group(1)}="{NAMED[m.group(2)]}"', text)


def work(args):
    src, dst = args
    if src.suffix == ".svg":
        try:
            dst.write_text(convert(src.read_text(encoding="utf-8")), encoding="utf-8")
            return 1
        except UnicodeDecodeError:
            pass
    shutil.copy2(src, dst)
    return 0


SATURADO = 40    # diferencia máxima entre canales (0-255) a partir de la cual un icono externo se pasa a gris


def desktop_icons():
    """Nombres de `Icon=` de las apps visibles (sistema y usuario) que el tema no resuelve."""
    nombres = set()
    for d in ("/usr/share/applications", str(Path.home() / ".local/share/applications")):
        for f in Path(d).glob("*.desktop"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"^(NoDisplay|Hidden)=true", t, re.M):
                continue
            m = re.search(r"^Icon=(.+)$", t, re.M)
            if m and not m.group(1).strip().startswith("/"):
                nombres.add(m.group(1).strip())
    return nombres


def buscar_externo(nombre):
    """Mejor fichero del icono fuera del tema (hicolor, pixmaps, ~/.local/share/icons): el más grande."""
    cand = []
    for raiz in ("/usr/share/icons/hicolor", "/usr/share/pixmaps", str(Path.home() / ".local/share/icons/hicolor")):
        for f in Path(raiz).rglob(nombre + ".*"):
            if f.suffix in (".png", ".svg"):
                cand.append(f)
    cand.sort(key=lambda f: (f.suffix != ".svg", -f.stat().st_size))
    return cand[0] if cand else None


def saturacion(f):
    if f.suffix == ".svg":
        mx = 0
        for c in re.findall(r"#([0-9a-fA-F]{6})(?![0-9a-fA-F])", f.read_text(encoding="utf-8", errors="ignore")):
            r, g, b = int(c[:2], 16), int(c[2:4], 16), int(c[4:], 16)
            mx = max(mx, max(r, g, b) - min(r, g, b))
        return mx
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(f).convert("RGBA")).astype(int)
    m = a[..., 3] > 20
    return int((a[..., :3].max(-1) - a[..., :3].min(-1))[m].max()) if m.any() else 0


def externos(dest):
    """Iconos de apps que traen su propio icono (Claude, Steam, Spotify, Ryoku Hub…): copia en grises al tema."""
    from PIL import Image
    import numpy as np
    en_tema = {f.stem for f in dest.glob("*/*/*.*")} | {f.stem for f in dest.glob("*/*/*/*.*")}
    hechos = []
    for nombre in sorted(desktop_icons() - en_tema):
        f = buscar_externo(nombre)
        if not f or saturacion(f) < SATURADO:
            continue
        for tam in ("48x48", "64x64"):
            d = dest / tam / "apps"
            d.mkdir(parents=True, exist_ok=True)
            if f.suffix == ".svg":
                (d / f"{nombre}.svg").write_text(convert(f.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                px = int(tam.split("x")[0])
                im = Image.open(f).convert("RGBA").resize((px, px), Image.LANCZOS)
                a = np.asarray(im).astype(float)
                lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]) / 255
                v = np.round(LO + lum ** 0.9 * (HI - LO))
                a[..., 0] = a[..., 1] = a[..., 2] = v
                Image.fromarray(a.astype("uint8"), "RGBA").save(d / f"{nombre}.png")
        hechos.append(nombre)
    os.system(f"gtk-update-icon-cache -f -t '{dest}' >/dev/null 2>&1")
    return hechos


def main():
    dest = Path(sys.argv[sys.argv.index("--destino") + 1]) if "--destino" in sys.argv else DEST
    if "--externos" in sys.argv:                      # solo los iconos externos, sin regenerar el tema entero
        print("externos en grises:", ", ".join(externos(dest)) or "ninguno")
        return
    if dest.exists():
        shutil.rmtree(dest)
    jobs = []
    links = []
    done = {}                                         # directorio real ya convertido -> su destino (para enlazar, no duplicar)

    def walk(src, dst, top=False):
        dst.mkdir(parents=True, exist_ok=True)
        for e in sorted(src.iterdir()):
            if top and e.name not in SIZES:
                continue
            d = dst / e.name
            real = e.resolve()
            if e.is_dir():                            # incluye enlaces a directorio
                if real in done:
                    os.symlink(os.path.relpath(done[real], d.parent), d)
                else:
                    done[real] = d
                    walk(real, d)
            elif e.is_symlink():
                os.symlink(os.readlink(e), d)         # enlace a fichero: se conserva (ahorra ~400 MB)
                links.append((e, d))
            elif e.name != "icon-theme.cache":
                jobs.append((e, d))

    walk(SRC, dest, top=True)
    jobs2 = []
    with ProcessPoolExecutor() as ex:
        n = sum(ex.map(work, jobs, chunksize=64))
    # un enlace que no resuelve dentro del tema nuevo (apuntaba fuera de los tamaños copiados) se sustituye por su fichero convertido
    for orig, d in links:
        if not d.exists():
            d.unlink()
            jobs2.append((orig.resolve(), d))
    with ProcessPoolExecutor() as ex:
        n += sum(ex.map(work, jobs2, chunksize=64))
    idx = (SRC / "index.theme").read_text(encoding="utf-8")
    idx = re.sub(r"^Name=.*$", "Name=ryoku-obsidian", idx, count=1, flags=re.M)
    idx = re.sub(r"^Comment=.*$", "Comment=Papirus-Dark en escala de grises para Ryoku Obsidian", idx, count=1, flags=re.M)
    idx = re.sub(r"^Inherits=.*$", "Inherits=hicolor", idx, count=1, flags=re.M)
    dirs = [x for x in re.search(r"^Directories=(.*)$", idx, re.M).group(1).split(",") if (dest / x).is_dir()]
    idx = re.sub(r"^Directories=.*$", "Directories=" + ",".join(dirs), idx, count=1, flags=re.M)
    idx = re.sub(r"^ScaledDirectories=.*$", "", idx, flags=re.M)
    (dest / "index.theme").write_text(idx, encoding="utf-8")
    os.system(f"gtk-update-icon-cache -f -t '{dest}' >/dev/null 2>&1")
    print(f"ok: {n} SVG convertidos -> {dest}")
    print("externos en grises:", ", ".join(externos(dest)) or "ninguno")


if __name__ == "__main__":
    main()
