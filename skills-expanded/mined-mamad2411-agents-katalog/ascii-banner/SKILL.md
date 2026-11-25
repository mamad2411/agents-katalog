---
name: ascii-banner
description: Genera texto en arte ASCII (tipografia ANSI Shadow, bloques ██╗) para encabezados de README, banners de CLI o docs, opcionalmente con marco de doble linea. Usar cuando se pida "arte ascii", "titulo en ascii", "banner" o el estilo del OG image de ASCII Motion.
---

# ascii-banner

```bash
python3 ~/.claude/skills/ascii-banner/banner.py "COMPANION" --frame
```

- Sin `--frame`: solo las letras. `--font RUTA.flf` usa otra fuente FIGlet.
- La primera vez descarga la fuente a `~/.cache/ascii-banner/` (commit fijado + sha256).
- Soporta ASCII 32-126. Acentos y ñ fallan con error explicito: quitarlos o preguntar.

## En un README

- Siempre dentro de un bloque de codigo sin lenguaje (```), encima del `# Titulo`, que se queda: es el que leen buscadores y lectores de pantalla.
- Ancho util: ~80 columnas. Si la palabra se pasa, partirla en dos lineas (una llamada por linea) o quitar `--frame`.
- GitHub no anima texto: para animacion, exportar GIF/SVG desde ASCII Motion y usar imagen con `alt`.
- Repo con CHANGELOG: una entrada por el cambio.
