# Ryoku Obsidian — Auditoría (2026-10-26)

Auditoría de solo lectura previa a cualquier cambio. Todo lo de abajo se midió en el equipo de Adrián el 2026-10-26; lo que no se pudo comprobar está marcado **(no verificado)**.

## 1. Plataforma

| Qué | Valor | Cómo se obtuvo |
|---|---|---|
| Distribución | Arch Linux (rolling) | `/etc/os-release` |
| Kernel | 7.2.11-arch1-1, x86_64 | `uname` |
| Compositor | **Hyprland 0.56.2** (Wayland, configuración en **Lua**) | `hyprctl version` |
| Inicio de sesión | SDDM → `ryoku-wayland-session` → `start-hyprland` | `pgrep -a` |
| Shell gráfico | **Quickshell 0.3.2** (`qs -c shell`), Qt 6.12.0 | `quickshell --version`, `pacman -Q` |
| Paquetes de Ryoku | `ryoku 1.0.3.r5417` (+ `ryoku-desktop-hyprland`, `ryoku-hub`, `ryoku-hypr-plugins`…) | `pacman -Q` |
| GPU | Intel Iris Xe (Raptor Lake-P) + NVIDIA RTX 4070 Max-Q, `nvidia-open 615.78`, Mesa 26.2 | `lspci`, `pacman -Q` |
| Audio | PipeWire 1.6.10 (+ pulse/alsa) | `pacman -Q` |
| Monitores | `HDMI-A-1` 1920×1080@165 en (0,0), escala 1 · `eDP-2` (portátil) 1920×1080@165 en (1920,0), escala 1 (admite también 2560×1440@165) | `hyprctl monitors -j` |
| Fuentes relevantes | Space Grotesk (paquete `otf-space-grotesk`), Inter, JetBrainsMono Nerd Font (Mono), Komiki Mono (local) | `fc-list`, `pacman -Q` |
| Iconos | temas `ryoku-<perfil>` en `~/.local/share/icons` (uno por perfil) | `ls` |

## 2. Quickshell y el shell de Ryoku

- Hay **dos instancias** de `qs`, ambas legítimas: `qs -c shell` (el shell de Ryoku: barra, dock, lanzador, paneles, reloj) y `qs -c genie` (overlay del efecto genio, repo `ryoku-genie`). Más `qs` efímeros para selectores (`perfiles`, `ryopin`…). No hay procesos duplicados del mismo shell.
- Configuraciones en `~/.config/quickshell/`: `shell` (Ryoku), `hub`, `genie`, `perfiles`, `plugins`, `ryoshot`, `ryostore`, `ryovm`, `stage`, `welcome`, `keys`, `notas`…
- **El árbol `shell` no se bifurca** (lo dice `ryoku owner`): se cambia con `ryoku-shell`, el Hub, un plugin o el **overlay** `~/.config/ryoku/user_edits/` (un fichero regular allí gana al de Ryoku en cada `ryoku update`; `ryoku reset <ruta>` lo deshace).
- Hay forks vivos en el overlay: `DockSurface.qml`, `launcher/catalog.json`, `launcher/variants/perfil/*.qml` (11 estilos de lanzador) y `Theme.qml` parcheado por `shell/install.sh` de este repo.
- IPC: `qs -c shell ipc call shell openSurface <monitor> quick-settings` (probado en sesiones anteriores).
- Errores en los registros: **(no verificado en esta auditoría; se revisa en `VALIDATION.md`)**.

## 3. Mecanismos oficiales de personalización

`ryoku owner --map` define quién es dueño de cada fichero:

| Clase | Ejemplo | Cómo se cambia |
|---|---|---|
| Distribuido por paquete (se re-escribe en cada `ryoku update`) | `/usr/share/ryoku/**`, `~/.config/quickshell/shell` | solo vía overlay / `ryoku-shell` / Hub / plugin |
| Generado | `gtk.css` (matugen), paleta del shell | Hub o comando, nunca a mano |
| Semilla / override propio | `~/.config/kitty/user.conf`, rices en `~/.config/ryoku/rices/<slug>/` | en su sitio, sobreviven |
| Overlay | `~/.config/ryoku/user_edits/**` | ficheros propios; ganan al original |

El mecanismo de «tema completo» de Ryoku es el **rice** (`ryoku-hub rice save|apply|restore`): un JSON con apariencia de Hyprland, barra, dock, reloj, visualizador, tema… Este repo (`ryoku-perfiles`) ya construye sobre él 12 perfiles (`perfil apply <slug>`, selector `Super+Alt+P`).

## 4. Notificaciones, calendario, estadísticas, reloj

Son **módulos nativos del shell de Ryoku** (panel de ajustes rápidos con `notifications`, `weather`, `home`; reloj y calendario de escritorio con `clockDesign`/`calendarStyle`; panel de estadísticas del escritorio). Los estilos se eligen por rice. No se reemplaza ninguno: se estilan.

## 5. Claude Code

- Existe el plugin **`claude-code`** (`~/Documentos/ryoku-plugins/claude-code`), **habilitado**, widget de escritorio con personaje animado, `bridge: auto`, `permissionMode: plan`. Lee el estado de sesión mediante el puente del propio plugin (hooks de Claude Code instalados en `~/.claude`; detalle del protocolo en el repo del plugin).
- También está `claude-companion` (deshabilitado). No se tocan.
- Cada perfil elige un personaje (`personaje` en el spec). Los trajes de temporada cambian con `season: auto`.
- Hooks y `settings.json` propios: el clasificador los protege; este trabajo **no los modifica**.

## 6. Mobile Bridge

- Implementación existente: `~/Proyectos/ryoku-mobile-bridge` (app Android Kotlin/Ktor + plugin de escritorio `mobile-bridge` y cliente Python `bin/ryoku-mobile-client`; REST + WebSocket, token en fichero 0600, ver `docs/API.md` y `docs/SECURITY.md` del repo).
- El plugin está **habilitado** en `plugins.json` (`desktopWidget` x=0, y=288, escala 1,2). La nota del vault decía «pendiente de activar»: está desactualizada.
- Se respeta tal cual; Obsidian solo reserva su zona en la composición (zona prohibida `0,300–500,505` en `tools/colocar.py`).

## 7. Referencias visuales

- **Lenguaje de Ryoku** (vault `09 - Claude/Referencias/Estilo visual Ryoku.md`): papel y tinta, bordes finos, sin sombras, radio pequeño, grano ~5,5 %, mármol halftone, torii y sol rojo como motivos, etiquetas pequeñas en mayúsculas con tracking, Space Grotesk para UI.
- Recursos oficiales ya en disco: `~/Imágenes/Wallpapers/ryoku.png`, `new-ryoku-walls-v0-…webp`, `perfil-ryoku.png` (no se redistribuyen ni se copian al repo).
- Procedencia de lo que usa Obsidian: **todo el arte es propio** (generado por código, `tools/obsidian_scene.py`); no se descarga nada.
- Referencias de diseño genéricas (editorial monocromo, interfaces oscuras): consultadas como criterio de composición, sin copiar recursos.

## 8. Decisión de arquitectura (consecuencia de la auditoría)

La especificación pedía un shell nuevo en Quickshell. La auditoría muestra que **sería una duplicación contraria a sus propias reglas** (no duplicar lo que Ryoku ya hace, no sustituir lo funcional, respetar el mecanismo oficial, y el árbol `shell` no se puede bifurcar):

> **Ryoku Obsidian = un perfil más de `ryoku-perfiles`** (`perfil apply obsidian`), compuesto por: rice (sistema de tokens), fondo propio, paleta fija monocroma, capa de ventanas GTK, estilo de lanzador, tema de iconos, ajustes del reloj/calendario/estadísticas nativos y las zonas reservadas para `claude-code` y `mobile-bridge`.

Ventajas: reversible con un comando, sobrevive a `ryoku update`, no añade procesos ni dependencias, reutiliza las integraciones ya verificadas.

## 9. Riesgos

| Riesgo | Mitigación |
|---|---|
| La paleta de Ryoku sale del fondo (matugen); un fondo monocromo cae al azul por defecto | `paleta` fija (`assets/paletas/obsidian.json`, `color.mode: fixed`) |
| `ryoku update` puede cambiar el original de un fork del overlay | `ryoku doctor` avisa; los forks son los ya existentes |
| El árbol de este repo tiene cambios sin confirmar de otras sesiones | no se hace `git add -A`; solo rutas de Obsidian |
| Sin herramienta para simular ratón | la interacción se verifica por IPC y capturas, no con clics reales |
| Sensor de GPU NVIDIA vs Intel: no exponen lo mismo | el panel nativo ya decide qué mostrar; no se añaden métricas propias |

## 10. Fuentes

- Hyprland: <https://wiki.hypr.land/> (versión 0.56, configuración Lua).
- Quickshell: <https://quickshell.org/docs/> (0.3.x).
- Qt Quick: <https://doc.qt.io/qt-6/qtquick-index.html>.
- Documentación del propio Ryoku: `ryoku help`, `ryoku owner`, `/usr/share/ryoku/**` y los README de este repo.
- Notas del vault: `Personalización de Ryoku (Kami)`, `Estilo visual Ryoku`, `Ryoku Mobile Bridge`.

> No se abrieron las URL web en esta sesión; se citan como la documentación de referencia de cada API, y las propiedades concretas se verifican contra el sistema instalado en cada etapa.
