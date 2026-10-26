# Ryoku Obsidian — Validación (2026-10-26)

Entorno: Hyprland 0.56.2, Quickshell 0.3.2, `eDP-2` y `HDMI-A-1` a 1920×1080@165, escala 1. Capturas con `grim`, **guardadas solo en local** (scratchpad de la sesión), no publicadas.

## Implementado y verificado

| Qué | Cómo se verificó |
|---|---|
| Fondo monocromo estricto, 3840×2160 | `max|R−G| = 0` en todos los píxeles (script Pillow/numpy); inspección visual de 3 iteraciones |
| Paleta: 30 roles + 16 colores, solo grises salvo semánticos | el shell la carga: `~/.cache/ryoku/matugen-carrier.json` contiene `outline #5A5A62`, `primary #FFFFFF`, `surface #0B0B0D` |
| Contraste de texto | cálculo WCAG: principal 15,8:1, secundario 5,4:1 (corregido desde 4,4:1) |
| `perfil build obsidian` y `perfil apply obsidian` | ejecutados sin error; `~/.config/ryoku/perfiles/actual` = `obsidian` |
| Escritorio libre | captura de `eDP-2`: reloj, fecha, calendario y estadísticas legibles, sin solapes; corregido un solape real (estadísticas sobre el disco) |
| Terminal con ventana abierta | captura de `HDMI-A-1` (kitty con Claude Code): tema monocromo, borde 1 px, JetBrainsMono |
| Notificación | `notify-send` + captura: tarjeta legible, jerarquía título/cuerpo, arriba a la derecha |
| Iconos | 659 531 colores en 88 040 SVG, **0** no grises; `gsettings` y `gtk-3.0/settings.ini` apuntan a `ryoku-obsidian` |
| Recursos | sin descargas externas; todo generado en local |
| Estabilidad básica | `qs -c shell` 5,4 % CPU medio y ~1,0 GB RSS (32 min de vida); `qs -c genie` 0 % y 180 MB; sin procesos duplicados. **Sin línea base previa**: no se puede atribuir el consumo a Obsidian |

## Implementado, no verificado del todo

| Qué | Qué falta |
|---|---|
| Panel de ajustes rápidos (izquierda, 420 px) | el id de superficie es `quicksettings` (sin guion; con `quick-settings` no hace nada); `openSurface` no produjo captura, no se vio |
| Capa de ventanas GTK | CSS escrito y aplicado por `perfil apply`; **no se abrió Nautilus** para verla |
| Iconos en Nautilus/dock | tema aplicado; no se vio ningún icono real en pantalla |
| Widgets `claude-code` y `mobile-bridge` | vistos en `HDMI-A-1` (2026-10-26): busto y panel «Móvil» arriba a la izquierda, bajo el reloj. Claude: estado y puente `CONNECTED` reales. Móvil: «Sin conexión / OSError» porque el móvil no está en la red (`check` OK; sin probar con móvil físico) |
| Reducción de movimiento | no probada |
| Terminal: kitty/starship/fastfetch | `perfil apply` los escribe; solo se vio kitty indirectamente |
| Persistencia tras reinicio de sesión y reinicio del shell | no probado |
| Desconexión/reconexión de monitor, otras resoluciones | no probado |
| Rendimiento prolongado | solo una instantánea |
| Bloqueo de pantalla | sin cambios (`pkexec`, como en los demás perfiles) |

## Corregido tras la validación (2026-10-26)

- **El lanzador nunca cargaba `StyleObsidian`**: `launcher/perfil/Main.qml` no tenía `obsidian` en el mapa `styles` y caía a Kami (tonos marrones, cursor bermellón). Añadida la entrada, `launcher/install.sh` + `ryoku-shell reload`; captura posterior: monocromo, «01 // BUSCAR», cursor gris. **Todo perfil nuevo necesita su entrada en `styles`.**

## Defectos conocidos (abiertos)

1. **Colores fuera de la paleta en widgets nativos**: ticks de color del panel de estadísticas y barra verde del disco (valores fijos en `modules/desktop/stats/StatsWidget.qml`); borde bermellón de las notificaciones (`Theme.vermLit`, constante de marca). Se podrían cambiar forkeando esos ficheros del shell, pero `ryoku owner` avisa de que forkear el árbol del shell puede romperlo; **no se hizo**. Alternativa: pedir a Ryoku una opción de tema.
2. **Reloj en 12 h («am»)**: lo decide `TimeFormat.is24h` del shell (ajuste del sistema/Hub), no el rice; Obsidian lo respeta. Con 24 h el bloque del reloj es más corto.
3. **Marca `力`** en el lanzador de la barra: es la marca de Ryoku; solo se cambia desde el Hub (Profile).
4. **Posición del reloj fija** (`x=140,y=500`): con otra resolución hay que reconstruir el perfil.
5. **Tema de iconos pesado en disco** (~390 MB con 88 000 ficheros).
6. **Widget Claude con `debugOverlay: true`** en `plugins.json`: muestra la tabla de depuración (state/anim/frame/fps/char/bridge) junto al busto. Es un ajuste del plugin, no del perfil; ponerlo a `false` para escritorio limpio.
7. **Nada confirmado en git**: el repo tiene ya cambios sin confirmar de otras sesiones; los ficheros de Obsidian están sin `git add`.

## Restauración

| Qué | Cómo |
|---|---|
| Volver al perfil anterior | `perfil apply cyberpunk` (era el activo) |
| Volver a la línea base de Ryoku | `perfil apply ryoku` o `ryoku-hub rice restore` |
| Restaurar configuración completa previa | `~/Archivo/Backups/ryoku-antes-obsidian-2026-10-26.tar.zst` (`.config/ryoku`, `kitty/user.conf`, `hypr`, `quickshell`, `gtk-3.0/4.0`; extraer con `tar --zstd -xf … -C ~` tras revisar su contenido) |
| Quitar Obsidian por completo | `perfil apply <otro>`; `rm -r ~/.config/ryoku/rices/obsidian ~/.local/share/icons/ryoku-obsidian ~/Imágenes/Wallpapers/perfil-obsidian*.png`; borrar los ficheros nuevos del repo |
| Backup periódico | `restic` diario ya cubre `~/.config` e `~/Proyectos` |

## Cómo mantenerlo

- Editar `perfiles/obsidian.json`, `assets/paletas/obsidian.json` o `tools/obsidian_scene.py` → `perfil build obsidian && perfil apply obsidian`.
- Regenerar iconos tras actualizar Papirus: `python3 tools/icons_obsidian.py`.
- Tras `ryoku update`: `ryoku doctor --check`.

## Criterios de aceptación: estado

Identidad visual: **cumplido en lo verificable** (paleta, fondo, fuentes, iconos); excepciones en «Defectos». Composición: **cumplido** en el escritorio libre. Funcionalidad: calendario/estadísticas/notificaciones **vistos funcionando**; Claude Code y Mobile Bridge **no comprobados en pantalla**. Animaciones: **parcial** (estilos elegidos, sin medición de fluidez). Estabilidad: **parcial**. Documentación: **cumplido**.
