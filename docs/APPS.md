# Ryoku Obsidian — Apps externas, iconos y bloqueo (2026-10-26)

Código en `apps/` (instalador `apps/instalar_apps.sh`), `tools/icons_obsidian.py --externos` y `tools/lockscreen_obsidian.py`.

| Pieza | Qué se hizo | Estado |
|---|---|---|
| Iconos con color propio | `icons_obsidian.py --externos` pasa a grises (misma curva que el tema) los iconos de apps que el tema no trae: claude-desktop, spotify-launcher, steam (Geometry Dash), ryoku-hub, ryostore, ryotunes, ryovm, low-noise-hub, scrcpy, yazi, java, Limine. Se ejecuta también al final de una regeneración completa | **Visto** en el lanzador y en la comparación antes/después (`screenshots/12`) |
| Pantalla de bloqueo | tema qylock `pixel-obsidian` (derivado de pixel-hollowknight): vídeo de 5 s con el fondo del perfil (respiración, barrido, grano), acentos grises, Space Grotesk. `perfiles/obsidian.json` → `"lock": "pixel-obsidian"` | **Visto** con `sddm-greeter-qt6 --test-mode` (formulario, reloj y fondo). Activo (`ryoku-hub lock list`) |
| VS Code | extensión local `ryoku.obsidian` (tema «Ryoku Obsidian»): interfaz en grises, **código a color** (rosa, verde lima, azul, ámbar, malva…; sin resaltado semántico para que no lo pise); iconos `vs-minimal` | **Visto** (captura): interfaz gris, código a color |
| Obsidian (app) | snippet `.obsidian/snippets/ryoku-obsidian.css` sobre Obsidianite + activado en `appearance.json` | Sin captura de la app: mostrar el vault expone notas personales |
| Zen | `ryoku-obsidian.css` importado desde `userChrome.css` (2 perfiles) + `user.js` (acento) | **Sin captura** (su barra lateral lista pestañas privadas). Nombres de variables de Zen sin comprobar contra su código |
| Spotify | tema spicetify `Obsidian` (color.ini + user.css), `spicetify backup apply` | **Visto** (captura) |
| Qt | `qt6ct.conf` → `icon_theme=ryoku-obsidian` | **No visto** |
| Discord | cliente oficial + CSS inyectado por el puerto de depuración de Chromium (`apps/discord/`: `ryoku-discord` lanza y `inject.mjs` inyecta; lanzador de usuario `~/.local/share/applications/discord.desktop`). Variables reales volcadas del cliente (2026-10). Monocromo, Space Grotesk, esquinas rectas | **Visto** (captura CDP) y probado el ciclo cerrar→abrir. Límites: puerto 9223 solo en 127.0.0.1 (cualquier proceso local podría usarlo); modificar el cliente va contra los términos de Discord (riesgo bajo, no cero); tras una recarga del cliente hay que reinyectar (`ryoku-discord`); una actualización de Discord puede renombrar variables |
| Nautilus (GTK) | tematizado por Ryoku desde la paleta del perfil | **Visto** (captura) |
| Chromium, Android Studio/IntelliJ | sin tocar | Pendiente |

Copias previas en `~/Archivo/Backups/` (`*.antes-obsidian`, `*.antes-zen-2026-10-26`).
Deshacer: VS Code → restaurar `settings.json`; Spotify → `spicetify restore`; Zen → borrar el `@import` y `ryoku-obsidian.css`; bloqueo → `ryoku-hub lock set pixel-hollowknight`.
Limitación: VS Code, Spotify y Zen no vuelven solos al estilo anterior con `perfil apply <otro>`.

## Regresiones tras `ryoku update` (v1.0.5) y arreglos

- El fondo, el reloj y los plugins volvieron a los valores por defecto → `perfil apply obsidian` los restaura.
- `rice apply` dejaba **desactivados** `claude-code` y `mobile-bridge` → el perfil declara `"plugins"` y `perfil` los reactiva (`set_plugins`).
- El lema por defecto de `fastfetch` cambió de texto en 1.0.5 y ahora también se sustituye. El logo es el Arch 3D giratorio de Ryoku (naranja): se mantiene a propósito, no es monocromo.
