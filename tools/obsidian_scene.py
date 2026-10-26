#!/usr/bin/env python3
"""Fondo de Ryoku Obsidian: casi negro, dibujo monocromo en blanco y gris.

Arte propio, generado por código (sin recursos de terceros). Motivos de la marca Ryoku
(sol, torii, mármol halftone) tratados como arquitectura: un disco de obsidiana en
semitono con venas de mármol, un torii en alzado que lo cruza, anillos de instrumento y
un reflejo en el suelo. Toda la mitad izquierda queda vacía para el reloj y los widgets.

    obsidian_scene.py salida.png [--ancho 3840]

Se dibuja con cairo en coordenadas de 1920x1080 y se escala al ancho pedido.
"""
import math
import sys

import cairo
import numpy as np
from PIL import Image

VW, VH = 1920, 1080               # coordenadas de diseño
BG = (0x05, 0x05, 0x05)
CX, CY, R = 1160.0, 548.0, 345.0  # disco
HORIZON = 905.0
LIGHT = np.array([0.55, -0.42, 0.72])   # luz desde arriba a la derecha y delante
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def rgb(v, a=1.0):
    """Gris v (0..1) como fuente cairo."""
    return v, v, v, a


def fbm(shape, seed, octaves=5, base=4):
    """Ruido de valor por octavas, 0..1, sin dependencias (rejillas aleatorias ampliadas)."""
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((n + 1, n + 1)).astype(np.float32)
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(img, np.float32) / 255.0
        tot += amp
        amp *= 0.5
    return out / tot


def disc_dots(ctx):
    """Disco de obsidiana en semitono: esfera iluminada desde la derecha, con venas de mármol."""
    pitch = 7.2                                   # paso de la retícula (unidades de diseño)
    n = int(2 * R / pitch) + 6
    noise = fbm((512, 512), 7, 5, 3)
    warp = fbm((512, 512), 11, 4, 3)

    def sample(a, x, y):
        u = min(max((x - (CX - R)) / (2 * R), 0), 0.999)
        v = min(max((y - (CY - R)) / (2 * R), 0), 0.999)
        return a[int(v * 512), int(u * 512)]

    ca, sa = math.cos(math.radians(35)), math.sin(math.radians(35))   # retícula girada
    for i in range(-n, n):
        for j in range(-n, n):
            gx, gy = i * pitch, j * pitch
            x, y = CX + gx * ca - gy * sa, CY + gx * sa + gy * ca
            dx, dy = (x - CX) / R, (y - CY) / R
            d2 = dx * dx + dy * dy
            if d2 >= 1:
                continue
            nz = math.sqrt(1 - d2)
            lam = max(0.0, dx * LIGHT[0] + dy * LIGHT[1] + nz * LIGHT[2])
            # venas de mármol: líneas finas que serpentean según el ruido
            t = (dx * 3.1 + dy * 1.7) + 2.6 * (sample(warp, x, y) - 0.5) + 1.4 * (sample(noise, x, y) - 0.5)
            vein = abs(math.sin(t * math.pi * 1.35)) ** 14
            tone = lam ** 1.25 * (0.62 + 0.38 * sample(noise, x, y)) + 0.50 * vein * lam
            rim = max(0.0, 1 - nz) ** 3.0 * max(0.0, dx * 0.9 - dy * 0.35) * 0.8    # filo de luz a la derecha
            term = min(1.0, max(0.0, (lam - 0.04) / 0.22))                           # terminador: la sombra cae suave
            v = min(1.0, tone * 0.82 * term + rim)
            if v < 0.035:
                continue
            r = pitch * 0.52 * math.sqrt(v)
            ctx.new_sub_path()
            ctx.arc(x, y, r, 0, math.tau)
        # relleno por columna: menos llamadas a fill
        ctx.fill()


def rings(ctx):
    """Anillos de instrumento alrededor del disco: tramos de arco y marcas, nunca un blanco completo."""
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    ctx.set_source_rgba(*rgb(1, 0.20))
    ctx.set_line_width(0.9)
    ctx.arc(CX, CY, R + 24, 0, math.tau)
    ctx.stroke()
    ctx.set_source_rgba(*rgb(1, 0.10))
    for r, a0, a1 in [(R + 70, -170, 20), (R + 70, 60, 118), (R + 118, -95, 8), (R + 118, 150, 205), (R + 190, 200, 262)]:
        ctx.arc(CX, CY, r, math.radians(a0), math.radians(a1))
        ctx.stroke()
    # regla: marcas cada 2°, más largas cada 10°, en un tramo del anillo interior
    for k in range(-92, 38):
        ang = math.radians(k * 2)
        big = k % 5 == 0
        r0, r1 = R + 30, R + (46 if big else 38)
        ctx.set_source_rgba(*rgb(1, 0.34 if big else 0.16))
        ctx.set_line_width(1.0 if big else 0.7)
        ctx.move_to(CX + r0 * math.cos(ang), CY + r0 * math.sin(ang))
        ctx.line_to(CX + r1 * math.cos(ang), CY + r1 * math.sin(ang))
        ctx.stroke()
    # cruz de centro, sin llegar a tocar el disco
    ctx.set_source_rgba(*rgb(1, 0.22))
    ctx.set_line_width(0.8)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ctx.move_to(CX + dx * (R + 92), CY + dy * (R + 92))
        ctx.line_to(CX + dx * (R + 150), CY + dy * (R + 150))
        ctx.stroke()


def kasagi_path(ctx, cx, yk, w):
    """Viga superior curvada hacia arriba en los extremos."""
    n = 80
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        u = abs(2 * t - 1)
        x = cx - w / 2 + w * t
        top.append((x, yk - 36 * u ** 2.3))
        bot.append((x, yk + 25 - 22 * u ** 2.3))
    ctx.move_to(*top[0])
    for p in top[1:]:
        ctx.line_to(*p)
    for p in reversed(bot):
        ctx.line_to(*p)
    ctx.close_path()


def torii(ctx):
    """Torii en alzado, sólido negro con filo de luz a la derecha; oculta lo que hay detrás."""
    cx, y0, hgt, w = CX - 6, HORIZON, 540.0, 470.0
    yk = y0 - hgt
    px = w * 0.37                                  # separación de los pilares desde el centro
    tw0, tw1 = 46.0, 37.0                           # ancho del pilar en la base y arriba
    black = (BG[0] / 255,) * 3

    def fill_stroke(alpha_line=0.62, lw=1.3):
        ctx.set_source_rgb(*black)
        ctx.fill_preserve()
        ctx.set_source_rgba(*rgb(1, alpha_line))
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_MITER)
        ctx.stroke()

    for s in (-1, 1):                              # pilares, algo inclinados hacia dentro
        xb, xt = cx + s * (px + 6), cx + s * (px - 4)
        ctx.move_to(xb - tw0 / 2, y0)
        ctx.line_to(xt - tw1 / 2, yk + 40)
        ctx.line_to(xt + tw1 / 2, yk + 40)
        ctx.line_to(xb + tw0 / 2, y0)
        ctx.close_path()
        fill_stroke(0.50)
        # sombreado de líneas verticales en la cara izquierda (la que no recibe luz)
        ctx.set_source_rgba(*rgb(1, 0.14))
        ctx.set_line_width(0.7)
        for k in range(1, 6):
            f = k / 7
            ctx.move_to(xb - tw0 / 2 + tw0 * f * 0.55, y0)
            ctx.line_to(xt - tw1 / 2 + tw1 * f * 0.55, yk + 40)
            ctx.stroke()
        # filo de luz en el borde derecho
        ctx.set_source_rgba(*rgb(1, 0.95))
        ctx.set_line_width(1.6)
        ctx.move_to(xb + tw0 / 2, y0)
        ctx.line_to(xt + tw1 / 2, yk + 40)
        ctx.stroke()
        # base: zócalo
        ctx.rectangle(xb - tw0 / 2 - 6, y0 - 22, tw0 + 12, 22)
        fill_stroke(0.50)

    # nuki: la viga de abajo, atraviesa los pilares
    ny = yk + 128
    ctx.rectangle(cx - w * 0.5 + 40, ny, w - 80, 20)
    fill_stroke(0.55)
    ctx.set_source_rgba(*rgb(1, 0.9))
    ctx.set_line_width(1.2)
    ctx.move_to(cx - w * 0.5 + 40, ny)
    ctx.line_to(cx + w * 0.5 - 40, ny)
    ctx.stroke()
    # shimaki + kasagi
    ctx.rectangle(cx - w * 0.43, yk + 24, w * 0.86, 20)
    fill_stroke(0.50)
    kasagi_path(ctx, cx, yk, w)
    fill_stroke(0.72, 1.4)
    ctx.set_source_rgba(*rgb(1, 1))                 # filo superior de luz
    ctx.set_line_width(1.6)
    n = 80
    for i in range(n + 1):
        t = i / n
        u = abs(2 * t - 1)
        x, y = cx - w / 2 + w * t, yk - 36 * u ** 2.3
        (ctx.move_to if i == 0 else ctx.line_to)(x, y)
    ctx.stroke()


def cotas(ctx):
    """Cotas de plano: línea con remates y una cifra. Dan escala y precisión sin decorar."""
    cx, y0, hgt, w = CX - 6, HORIZON, 540.0, 470.0
    yk = y0 - hgt
    ctx.set_source_rgba(*rgb(1, 0.34))
    ctx.set_line_width(0.9)
    xv = cx - w / 2 - 46
    ctx.move_to(xv, yk - 36)
    ctx.line_to(xv, y0)
    for y in (yk - 36, y0):
        ctx.move_to(xv - 6, y)
        ctx.line_to(xv + 6, y)
    ctx.stroke()
    ctx.set_source_rgba(*rgb(1, 0.10))              # líneas de referencia hasta el objeto
    for y in (yk - 36, y0):
        ctx.move_to(xv + 6, y)
        ctx.line_to(cx - w / 2 + 6 if y == yk - 36 else cx - w * 0.37 - 30, y)
        ctx.stroke()
    ctx.select_font_face("Space Grotesk", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(10.5)
    ctx.set_source_rgba(*rgb(0.70, 0.62))
    ctx.save()
    ctx.translate(xv - 12, (yk + y0) / 2 + 24)
    ctx.rotate(-math.pi / 2)
    ctx.show_text("H 576")
    ctx.restore()
    xh = cx + w / 2 + 0
    yh = y0 + 38
    ctx.set_source_rgba(*rgb(1, 0.34))
    ctx.move_to(cx - w / 2, yh)
    ctx.line_to(xh, yh)
    for x in (cx - w / 2, xh):
        ctx.move_to(x, yh - 6)
        ctx.line_to(x, yh + 6)
    ctx.stroke()
    ctx.set_source_rgba(*rgb(0.70, 0.62))
    ctx.move_to(cx - 18, yh + 22)
    ctx.show_text("W 470")


def floor(ctx, disc_layer):
    """Horizonte, líneas de agua que se abren hacia abajo y reflejo del disco desvanecido."""
    # reflejo: el disco volteado respecto al horizonte, con degradado de opacidad
    ctx.save()
    ctx.rectangle(0, HORIZON, VW, VH - HORIZON)
    ctx.clip()
    ctx.push_group()
    ctx.translate(0, 2 * HORIZON)
    ctx.scale(1, -1)
    ctx.set_source_surface(disc_layer, 0, 0)
    ctx.paint()
    grp = ctx.pop_group()
    fade = cairo.LinearGradient(0, HORIZON, 0, HORIZON + 190)
    fade.add_color_stop_rgba(0, 1, 1, 1, 0.34)
    fade.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    ctx.set_source(grp)
    ctx.mask(fade)
    ctx.restore()
    # horizonte con desvanecido hacia la izquierda
    g = cairo.LinearGradient(300, 0, 1920, 0)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(0.30, 1, 1, 1, 0.20)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.42)
    ctx.set_source(g)
    ctx.set_line_width(1.0)
    ctx.move_to(300, HORIZON)
    ctx.line_to(VW, HORIZON)
    ctx.stroke()
    # líneas de agua, separación creciente
    y, step = HORIZON, 5.0
    k = 0
    while y < VH and k < 18:
        y += step
        step *= 1.32
        k += 1
        gg = cairo.LinearGradient(700, 0, 1920, 0)
        a = 0.17 * (1 - k / 20)
        gg.add_color_stop_rgba(0, 1, 1, 1, 0.0)
        gg.add_color_stop_rgba(0.5, 1, 1, 1, a * 0.6)
        gg.add_color_stop_rgba(1, 1, 1, 1, a)
        ctx.set_source(gg)
        ctx.set_line_width(0.8)
        ctx.move_to(700, y)
        ctx.line_to(VW, y)
        ctx.stroke()


def marks(ctx):
    """Marcas de mira y ficha técnica, como en las piezas gráficas de Ryoku."""
    ctx.set_source_rgba(*rgb(1, 0.30))
    ctx.set_line_width(0.9)
    for x, y in ((CX, HORIZON + 8), (1840, 1020), (1010, 1020)):
        ctx.move_to(x - 7, y)
        ctx.line_to(x + 7, y)
        ctx.move_to(x, y - 7)
        ctx.line_to(x, y + 7)
        ctx.stroke()
    ctx.select_font_face("Space Grotesk", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(10.5)
    ctx.set_source_rgba(*rgb(0.62, 0.55))

    def spaced(txt, x, y, track=2.2, right=False):
        w = sum(ctx.text_extents(c).x_advance + track for c in txt) - track
        cur = x - w if right else x
        for c in txt:
            ctx.move_to(cur, y)
            ctx.show_text(c)
            cur += ctx.text_extents(c).x_advance + track

    spaced("01 // OBSIDIANA", 1820, 1024, right=True)
    spaced("PAPER #050505   INK #E6E6E9", 1030, 1024)


def render(width=3840):
    s = width / VW
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, round(VH * s))
    ctx = cairo.Context(surf)
    ctx.scale(s, s)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    ctx.set_source_rgb(*(c / 255 for c in BG))
    ctx.paint()
    # resplandor muy tenue detrás del disco, sin degradado multicolor (solo gris)
    glow = cairo.RadialGradient(CX + 120, CY + 80, 40, CX + 120, CY + 80, 760)
    glow.add_color_stop_rgba(0, 1, 1, 1, 0.075)
    glow.add_color_stop_rgba(0.55, 1, 1, 1, 0.022)
    glow.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    ctx.set_source(glow)
    ctx.paint()

    # el disco se dibuja en su propia capa para poder reflejarlo
    layer = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, round(VH * s))
    lc = cairo.Context(layer)
    lc.scale(s, s)
    lc.set_source_rgba(*rgb(0.84))
    disc_dots(lc)
    rings(ctx)
    ctx.save()
    ctx.scale(1 / s, 1 / s)
    ctx.set_source_surface(layer, 0, 0)
    ctx.paint()
    ctx.restore()
    # el reflejo usa la capa a escala de diseño: se pinta con su propia escala
    refl = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW, VH)
    rc = cairo.Context(refl)
    rc.scale(1 / 1, 1 / 1)
    rc.save()
    rc.scale(VW / width, VW / width)
    rc.set_source_surface(layer, 0, 0)
    rc.paint()
    rc.restore()
    floor(ctx, refl)
    torii(ctx)
    cotas(ctx)
    marks(ctx)

    img = Image.frombuffer("RGBA", (surf.get_width(), surf.get_height()), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("L")
    a = np.asarray(img, np.float32)
    rng = np.random.default_rng(3)
    a += rng.normal(0, 1.6, a.shape)                # grano fino, mismo en los tres canales
    a = np.clip(a, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "L").convert("RGB")


if __name__ == "__main__":
    ancho = 3840
    if "--ancho" in sys.argv:
        ancho = int(sys.argv[sys.argv.index("--ancho") + 1])
    out = sys.argv[1]
    render(ancho).save(out)
    print("ok", out)
