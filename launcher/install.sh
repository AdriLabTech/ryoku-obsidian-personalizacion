#!/usr/bin/env bash
# Instala la variante de lanzador «perfil» en Ryoku: ficheros en el overlay user_edits (sobreviven a las
# actualizaciones), copia viva en ~/.config/quickshell para verla ya y catálogo con la entrada nueva.
# Uso: install.sh [--activar]   (--activar fija launcher.json: variant = perfil)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
rel="quickshell/shell/modules/launcher"
overlay="$HOME/.config/ryoku/user_edits/$rel"
live="$HOME/.config/$rel"

mkdir -p "$overlay/variants" "$live/variants"
rm -rf "$overlay/variants/perfil" "$live/variants/perfil"
cp -r "$here/perfil" "$overlay/variants/perfil"
cp -r "$here/perfil" "$live/variants/perfil"

python3 - "$live/catalog.json" "$overlay/catalog.json" <<'PY'
import json, sys
base = json.load(open(sys.argv[1]))
base["variants"] = [v for v in base["variants"] if v["id"] != "perfil"]
base["variants"].append({
    "id": "perfil", "name": "Perfil",
    "description": "Una forma distinta de ver las apps en cada perfil de escritorio (cuadrícula, terminal, cuaderno, muralla…).",
    "entrypoint": "variants/perfil/Main.qml", "preview": "variants/perfil/Preview.qml", "capabilities": []})
for dst in sys.argv[1:]:
    json.dump(base, open(dst, "w"), indent=2)
PY

if [ "${1:-}" = "--activar" ]; then
  python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.config/ryoku/launcher.json")
d = json.load(open(p)); d["variant"] = "perfil"
json.dump(d, open(p, "w"), indent=2)
PY
fi
echo "lanzador «perfil» instalado"
