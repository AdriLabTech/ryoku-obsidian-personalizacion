#!/usr/bin/env bash
# Instala el tema monocromo de Obsidian en las apps externas que se pueden tematizar sin sudo.
# Zen: hoja de usuario + user.js en los perfiles locales; VS Code: extensión «ryoku.obsidian» (ya registrada si se hizo antes).
# Uso: instalar_apps.sh [zen|vscode|spotify|discord|obsidian <vault>]    (sin argumento: todo)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
want="${1:-all}"

if [ "$want" = all ] || [ "$want" = zen ]; then
  for p in "$HOME"/.config/zen/*Default*; do
    [ -f "$p/prefs.js" ] || continue
    mkdir -p "$p/chrome"
    cp "$here/zen/ryoku-obsidian.css" "$p/chrome/ryoku-obsidian.css"
    grep -q 'ryoku-obsidian.css' "$p/chrome/userChrome.css" 2>/dev/null || printf '@import "ryoku-obsidian.css";\n' >> "$p/chrome/userChrome.css"
    cp "$here/zen/user.js" "$p/user.js"
    echo "zen: $p"
  done
fi

if [ "$want" = all ] || [ "$want" = vscode ]; then
  ext="$HOME/.vscode/extensions/ryoku.obsidian-1.0.0"
  rm -rf "$ext"; mkdir -p "$ext"; cp -r "$here/vscode/package.json" "$here/vscode/themes" "$ext/"
  echo "vscode: $ext (elegir «Ryoku Obsidian» en Ctrl+K Ctrl+T)"
fi

if [ "$want" = all ] || [ "$want" = spotify ]; then
  t="$HOME/.config/spicetify/Themes/Obsidian"; mkdir -p "$t"; cp "$here/spicetify/color.ini" "$here/spicetify/user.css" "$t/"
  spicetify config current_theme Obsidian color_scheme obsidian >/dev/null && spicetify apply >/dev/null
  echo "spotify: spicetify con el tema Obsidian (deshacer: spicetify restore)"
fi

if [ "$want" = all ] || [ "$want" = discord ]; then
  mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
  ln -sf "$here/discord/ryoku-discord" "$HOME/.local/bin/ryoku-discord"
  sed 's|^Exec=.*|Exec=/home/'"$USER"'/.local/bin/ryoku-discord --url -- %u|' /usr/share/applications/discord.desktop > "$HOME/.local/share/applications/discord.desktop"
  echo "discord: lanzador «ryoku-discord» (CSS por puerto de depuración 127.0.0.1:9223). Deshacer: rm ~/.local/share/applications/discord.desktop"
fi

if [ "$want" = obsidian ]; then
  vault="${2:?uso: instalar_apps.sh obsidian <ruta-del-vault>}"
  mkdir -p "$vault/.obsidian/snippets"; cp "$here/obsidian/ryoku-obsidian.css" "$vault/.obsidian/snippets/"
  echo "obsidian: snippet copiado; actívalo en Ajustes → Apariencia → Fragmentos CSS"
fi
