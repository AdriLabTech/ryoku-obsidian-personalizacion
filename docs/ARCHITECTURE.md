# Ryoku Obsidian — Arquitectura

**Obsidian es un perfil de `ryoku-perfiles`, no un shell paralelo** (decisión y motivos en `AUDIT.md` §8). Se activa con `perfil apply obsidian` (selector `Super+Alt+P`).

## Piezas

```
ryoku-perfiles/
├─ perfiles/obsidian.json        spec: rice (forma, fuentes, barra, dock), kitty, starship, cursor, iconos, reloj
├─ assets/paletas/obsidian.json  paleta fija (30 roles + color0–15), color.mode = fixed
├─ tools/obsidian_scene.py       fondo (cairo): disco de semitono, torii, anillos, reflejo, cotas, grano
├─ tools/icons_obsidian.py       tema de iconos: Papirus-Dark → grises
├─ tools/estilo.py   (+entrada)  reloj minimal/fecha inline/calendario paper, ventana slide, terminal, prompt, fastfetch
├─ tools/paneles.py  (+entrada)  radios 2, borde 1, panel de ajustes a la izquierda (420 px)
├─ tools/relojes.py  (+entrada)  caja del reloj para el colocador
├─ tools/wallpapers.py (+GEN)    registra el generador `obsidian`
├─ ventanas/obsidian.css         capa GTK: bordes 1 px, radio 2, foco con anillo blanco
├─ launcher/perfil/StyleObsidian.qml   estilo de lanzador (variante `perfil`)
└─ docs/obsidian/                estos documentos
```

## Flujo de datos

```
perfiles/obsidian.json ─┐
paleta ─────────────────┼─ perfil build ─▶ ~/.config/ryoku/rices/obsidian/{rice.json,palette.json,wall.png}
tools/obsidian_scene.py ┘                           │
                                                    ▼  perfil apply
          ryoku-hub rice apply ─▶ shell.json / desktop.json / plugins ─▶ Quickshell (qs -c shell) + Hyprland (Lua)
          ~/.config/ryoku/perfiles/{actual,personaje} ─▶ plugin claude-code, lanzador, capas
          ~/.config/kitty/user.conf, starship, fastfetch, gtk.css (entre marcas), tema de iconos, cursor
```

## Lo que se reutiliza (no se duplica)

| Función | Quién la da | Cambio de Obsidian |
|---|---|---|
| Barra, dock, lanzador, paneles | shell de Ryoku (`qs -c shell`) | solo ajustes del rice + un estilo de lanzador |
| Reloj, calendario, estadísticas | widgets de escritorio de Ryoku | cara/estilo/fuente/posición |
| Notificaciones | servicio y tarjetas del shell | solo paleta, radios y borde |
| Claude Code | plugin `claude-code` (hooks + puente `auto`, ya habilitado) | ninguno; personaje `adrian` |
| Mobile Bridge | `~/Proyectos/ryoku-mobile-bridge` + plugin `mobile-bridge` (ya habilitado) | ninguno |
| Animación de ventanas | Hyprland + `ryoku-genie` | solo `windowStyle: slide` |
| Fondos / varias pantallas | Hyprland + Ryoku (`ryogami wallpaper`) | fondo único, 3840×2160 |
| Copia de seguridad | `restic` (timer diario) + tar previo | ver restauración |

## Servicios y procesos

Obsidian **no añade procesos, servicios, temporizadores ni dependencias**. Los generadores (`obsidian_scene.py`, `icons_obsidian.py`) son scripts que se ejecutan a mano en `perfil build`; solo requieren `python3`, `pycairo`, `numpy`, `Pillow` y `Papirus-Dark` (ya instalados).

## Arranque y persistencia

`perfil apply` escribe el estado en `~/.config/ryoku/` (lo que Ryoku restaura en cada sesión). No hay unidad systemd propia. Un `ryoku update` no toca nada de lo anterior: los ficheros son del rice/overlay del usuario.

## Dependencias de plataforma

Hyprland 0.56.2 (Lua), Quickshell 0.3.2, Qt 6.12, paquetes `ryoku*` 1.0.3. `ryoku doctor` avisa si cambia algún original que haya forkeado un perfil (los forks del lanzador son los de la capa de aplicaciones ya existente).

## Recuperación

Ver `VALIDATION.md` §Restauración.
