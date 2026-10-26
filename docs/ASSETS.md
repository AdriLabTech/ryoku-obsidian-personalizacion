# Ryoku Obsidian — Inventario de recursos

| Recurso | Ubicación | Procedencia y licencia | Uso |
|---|---|---|---|
| Fondo «Obsidiana» | generado por `tools/obsidian_scene.py` → `~/Imágenes/Wallpapers/perfil-obsidian.png` (3840×2160, no va en el repo) | **Arte propio**, dibujado por código (cairo + numpy + Pillow). Sin recursos de terceros. Motivos de marca (sol, torii, mármol) reinterpretados | fondo de ambos monitores |
| Tema de iconos `ryoku-obsidian` | `~/.local/share/icons/ryoku-obsidian` (generado por `tools/icons_obsidian.py`; ~390 MB en disco por el tamaño de bloque de ~88 000 SVG pequeños) | **Derivado de Papirus-Dark** (GPL-3.0, paquete `papirus-icon-theme` del sistema). El derivado conserva la licencia GPL-3.0; **no se redistribuye**: se regenera en local desde el paquete | iconos GTK/Qt, dock y lanzador |
| Space Grotesk | paquete `otf-space-grotesk` 2.0.0 | OFL (según el paquete; **no se revisó el texto de licencia en esta sesión**) | UI |
| JetBrainsMono Nerd Font Mono | fuentes del sistema | OFL | cifras del reloj, terminal |
| Fraunces | usada por el shell de Ryoku | la distribuye Ryoku | título del calendario |
| Cursor `Bibata-Modern-Ice` | `/usr/share/icons` | GPL-3.0 | cursor (el que ya usaban los perfiles base) |
| Paleta | `assets/paletas/obsidian.json` | propia | colores del shell, apps y terminal |
| Capa de ventanas | `ventanas/obsidian.css` | propia | marcos GTK |
| Lanzador | `launcher/perfil/StyleObsidian.qml` | propio, derivado de `StyleKami.qml` (también propio) | lanzador |

No se descargó ningún archivo externo, tema, script ni imagen. No se usaron imágenes generadas por IA.

## Referencias consultadas (no incorporadas)

- Vault: `Estilo visual Ryoku` (marca, tipografía, sin sombras, grano).
- Fondos de Ryoku ya presentes en disco (`ryoku.png`, `perfil-ryoku.png`): vistos como referencia, **no copiados ni modificados**.
