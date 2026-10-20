---
name: pdf-export
description: Generate professionally styled PDFs from Markdown docs using md-to-pdf (Puppeteer). Auto-reads project metadata. Supports logos, TOC, appendices, and brand theming.
allowed-tools: Read, Write, Terminal
---

# PDF Export Skill

> Convierte documentos Markdown en PDFs profesionales con branding, logos, índice y apéndices.
> **Stack:** `md-to-pdf` (Puppeteer/Chromium) + CSS custom + Python build script.

---

## Cuándo Usar

| Trigger                          | Acción                           |
| -------------------------------- | -------------------------------- |
| "genera un PDF", "exporta a PDF" | Ejecutar script                  |
| "PDF con portada y logos"        | Modo completo (logos opcionales) |
| "PDF rápido sin portada"         | Modo rápido (1 comando)          |

---

## Prerequisitos

```bash
npx -y md-to-pdf --version  # Se auto-instala
```

---

## Modo Rápido (sin portada)

```bash
npx -y md-to-pdf \
  --stylesheet .agent/skills/utils/pdf-export/resources/timekast-style.css \
  --pdf-options '{"format":"A4","margin":{"top":"20mm","bottom":"20mm","left":"20mm","right":"20mm"},"printBackground":true}' \
  docs/planning/MI_ARCHIVO.md
```

---

## Modo Completo

### Uso

```bash
# Con logos (busca automáticamente en el proyecto)
python3 .agent/skills/utils/pdf-export/scripts/build_pdf.py docs/planning/00_DISCOVERY_BRIEF.md

# Sin logos
python3 .agent/skills/utils/pdf-export/scripts/build_pdf.py docs/planning/00_DISCOVERY_BRIEF.md --no-logos

# Con apéndice
python3 .agent/skills/utils/pdf-export/scripts/build_pdf.py docs/planning/00_DISCOVERY_BRIEF.md \
  --appendix "Apéndice A — Catálogo Figma:docs/planning/FIGMA_SCREEN_CATALOG.md"

# Output custom
python3 .agent/skills/utils/pdf-export/scripts/build_pdf.py docs/planning/00_DISCOVERY_BRIEF.md \
  --output docs/exports/brief.pdf
```

### Detección Automática

El script auto-detecta metadata del proyecto:

| Dato                                | De dónde lo lee                                     | Fallback           |
| ----------------------------------- | --------------------------------------------------- | ------------------ |
| Título                              | H1 del markdown (`# Discovery Brief — Kuen`)        | Nombre del archivo |
| Fecha, Versión, Stakeholders, Autor | Header del MD (`**Fecha:** ...`)                    | Valores genéricos  |
| Logo TimeKast                       | `docs/planning/project-config.md` → `timekast_logo` | Sin logo           |
| Logo Cliente                        | `docs/planning/project-config.md` → `client_logo`   | Sin logo           |
| Logo TimeKast (fallback)            | Busca `*timekast*` o `unnamed.png` en raíz          | —                  |
| Logo Cliente (fallback)             | Busca `*logo*` webp/png/svg en raíz                 | —                  |

### Opciones CLI

| Flag                             | Default       | Descripción                                          |
| -------------------------------- | ------------- | ---------------------------------------------------- |
| `--no-logos`                     | false         | Omitir logos en portada                              |
| `--no-toc`                       | false         | Omitir tabla de contenidos                           |
| `--no-cover`                     | false         | Sin portada (como modo rápido pero con CSS)          |
| `--appendix "Título:archivo.md"` | —             | Agregar apéndice (repetible)                         |
| `--output path.pdf`              | `<input>.pdf` | Ruta del PDF de salida                               |
| `--skip-lines N`                 | 9             | Líneas de header del MD a omitir (ya van en portada) |
| `--css path.css`                 | skill default | CSS custom                                           |

---

## Personalización CSS

Editar `resources/timekast-style.css` — variables principales:

| Variable   | Default   | Qué controla   |
| ---------- | --------- | -------------- |
| `--purple` | `#5B2D8E` | Color primario |
| `--green`  | `#00C853` | Color acento   |
| `--teal`   | `#4DB6AC` | Gradientes     |

---

## Estructura

```
skills/utils/pdf-export/
├── SKILL.md
├── resources/
│   └── timekast-style.css
└── scripts/
    └── build_pdf.py
```

---

_TimeKast Factory — PDF Export Skill_
