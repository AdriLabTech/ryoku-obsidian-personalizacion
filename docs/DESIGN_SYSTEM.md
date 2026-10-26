# Ryoku Obsidian — Sistema de diseño

Los tokens viven **en un solo sitio**: `assets/paletas/obsidian.json` (colores, como roles Material 3 que consume el shell) y `perfiles/obsidian.json` (forma, tipografía, movimiento). No hay HEX sueltos en componentes QML: el único QML propio es `launcher/perfil/StyleObsidian.qml`, que declara sus siete colores como propiedades al principio del fichero con los mismos valores.

## Color

| Token | Valor | Uso | Contraste sobre `surface` `#0B0B0D` |
|---|---|---|---|
| `background` | `#050505` | fondo, terminal | — |
| `surface` | `#0B0B0D` | paneles, ventanas | — |
| `surfaceContainerHigh` | `#151518` | superficie secundaria | — |
| `outlineVariant` | `#29292E` | separadores y bordes de reposo | 1,36 (decorativo) |
| `outline` | `#5A5A62` | borde de hover y de foco discreto | 2,88 |
| `onSurfaceVariant` | `#85858D` | texto secundario | **5,37** |
| `onSurface` | `#E6E6E9` | texto principal | 15,79 |
| `primary` | `#FFFFFF` | énfasis máximo | 19,66 |
| `error` | `#E5736F` | única excepción semántica fuerte (error/aviso) | — |

Contrastes calculados con la fórmula WCAG 2.x (script en el historial de la sesión; reproducible con `python3` en 10 líneas).

**Ajuste respecto a la paleta inicial:** el texto secundario `#77777F` daba 4,43:1 sobre `surface` y 4,10:1 sobre `#151518`, por debajo de 4,5:1. Se subió a `#85858D` (5,37 / 4,98). Es el único cambio de valor; la identidad monocroma se conserva.

**Excepciones de color (funcionales, no decorativas):** `error` y, en la paleta ANSI de la terminal, rojo/verde/amarillo muy desaturados (`#C9706C`, `#8DB09A`, `#C4B27E`) para que `git diff` y los tests sean legibles. El resto de `color0–15` son grises.

**Lo que NO es monocromo y no se puede cambiar sin forkear el shell** (ver `VALIDATION.md`): ticks de colores del panel de estadísticas, barra verde del disco, borde bermellón de las notificaciones (`Theme.vermLit`, constante de marca de Ryoku).

## Tipografía

| Rol | Familia | Por qué |
|---|---|---|
| Interfaz, etiquetas, menús, fecha | **Space Grotesk** (paquete `otf-space-grotesk`) | ya es la fuente de UI de Ryoku; geométrica, buena a 11–13 px, cifras claras |
| Cifras del reloj, terminal | **JetBrainsMono Nerd Font Mono** | el shell la fija para las cifras del reloj; cifras tabulares y ligaduras en terminal |
| Título del calendario | Fraunces | la usa el shell para títulos (marca Ryoku); no se sustituye |

Tres familias en pantalla, las tres ya instaladas y ya usadas por Ryoku; no se añade ninguna. Compatibilidad con caracteres internacionales comprobada con el texto en español de las capturas (acentos, ñ, ·); otros alfabetos **no verificados**.

## Forma

- Radios: **2 px** (ventanas Hyprland, widgets, GTK). Sin cápsulas.
- Bordes: **1 px** (`border_width: 1`); activo `#E6E6E9`, inactivo `#29292E`.
- Sin sombras, sin blur, sin brillo (`shadowEnabled/blurEnabled/glowEnabled: false`). Jerarquía por tono y borde.
- Espaciado de ventanas: `gapsIn 6`, `gapsOut 12`.
- Unidad base 4 px.

## Iconografía

`ryoku-obsidian`: **Papirus-Dark convertido a grises** (`tools/icons_obsidian.py`). Una sola biblioteca → mismo grosor, proporciones y geometría; vectorial (SVG). El color de cada relleno se sustituye por un gris de la misma luminancia dentro de 24–E6. Sin emojis. Tamaños 16/22/24/32/48/64.

## Composición del escritorio libre

Lienzo de diseño 1920×1080, adaptable por proporciones (el fondo se escala; los widgets de Ryoku se colocan con coordenadas del rice, ver «Adaptación»).

- **Mitad izquierda vacía**: reloj (`minimal`, escala 2,2) en `x=140, y=500`; descanso visual.
- **Centro-derecha**: disco de obsidiana (centro `1160,548`, radio 345), torii en alzado con cotas, anillos de instrumento, horizonte y reflejo.
- **Extremo derecho**: panel de estadísticas (CPU, GPU, memoria, red, disco, temperaturas) y calendario, ambos nativos; el disco se desplazó a la izquierda tras comprobar en captura que el texto de las estadísticas sobre los puntos blancos era ilegible.
- **Zona a reservar a la izquierda-arriba**: plugins `claude-code` (0,32) y `mobile-bridge` (0,288), ya colocados por el Hub.
- Pie: marcas de mira y ficha técnica (`01 // OBSIDIANA`, `PAPER #050505 · INK #E6E6E9`), igual que las piezas gráficas de Ryoku.

## Movimiento

Motor de animación: el del shell de Ryoku (curvas y duraciones propias, `Motion.*`) y el de Hyprland. Obsidian solo elige estilos, no inventa un segundo motor:

| Qué | Ajuste | Razón |
|---|---|---|
| Abrir/cerrar ventanas | `windowStyle: slide` | desplazamiento lineal sin rebote (el estilo `pop` rebota) |
| Barra | `barAnim: 0` | sin animación decorativa permanente |
| Borde animado | off | no hay bucles de animación sin información |
| Lanzador | `ColorAnimation 120 ms OutCubic` en la selección | indicador pequeño 120–180 ms |
| Efecto genio (minimizar al dock) | el de `ryoku-genie`, sin cambios | ya existe y funciona; no se duplica |

Reducción de movimiento: el shell tiene `theme.motion.reduce` (Hub); Obsidian lo deja en su valor del usuario. **No se comprobó** que cada animación respete `reduce`.

## Adaptación a pantallas

- Hyprland en escala 1 en ambos monitores (1920×1080@165). El fondo se entrega a **3840×2160** y Ryoku lo ajusta a cada pantalla.
- El reloj y los widgets se guardan como coordenadas del rice (`clockX/Y`); `tools/colocar.py` calcula zonas tranquilas para los demás perfiles. Con otra resolución habría que re-ejecutar `perfil build obsidian` (o fijar `reloj` a mano). **No es adaptación automática en vivo**: es la limitación del modelo de Ryoku.
