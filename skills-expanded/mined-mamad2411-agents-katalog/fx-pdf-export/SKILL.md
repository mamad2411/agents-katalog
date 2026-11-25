---
name: fx-pdf-export
description: Factory-internal skill that generates branded PDFs from Markdown via md-to-pdf (Puppeteer/Chromium) with TimeKast styling, optional cover, auto-TOC from H2s, and appendices. Primary invocation is the `/pdf` slash command; Python driver `scripts/build_pdf.py` reads metadata from the MD header and `project/planning/project-config.md`.
family: factory-internal
runtime: true
last-verified: 2026-04-23
---

# fx-pdf-export — Markdown → Branded PDF

> **Scope:** kit-wide utility for turning planning/design/proposal MDs into
> shareable PDFs with a consistent look.
> **Invocación:** `/pdf <ruta.md> [flags]` — slash command en `.claude/commands/pdf.md`.

---

## 1. Cuándo usar

| Trigger                                     | Path         |
| ------------------------------------------- | ------------ |
| "genera un PDF de este doc", "export a PDF" | `/pdf <md>`  |
| "PDF rápido sin portada"                    | `--no-cover` |
| "PDF para cliente con portada y logos"      | default      |
| "agrega apéndices al PDF"                   | `--appendix` |

No usar para:

- HTML marketing landings → no es plantilla web
- Slides → usar herramientas específicas de presentaciones
- Reportes automáticos recurrentes → mejor pipeline dedicado

---

## 2. Prerequisitos

```bash
npx -y md-to-pdf --version   # se auto-instala al primer uso
python3 --version            # 3.8+
```

No hay que instalar nada permanentemente — `npx -y` resuelve `md-to-pdf` y
Puppeteer al vuelo la primera vez.

---

## 3. Fast path — `npx md-to-pdf` directo

Sin portada ni TOC, solo estiliza el MD con el CSS del kit:

```bash
npx -y md-to-pdf \
  --stylesheet .claude/skills/fx-pdf-export/resources/timekast-style.css \
  --pdf-options '{"format":"A4","margin":{"top":"20mm","bottom":"20mm","left":"20mm","right":"20mm"},"printBackground":true}' \
  project/planning/MI_DOC.md
```

Output: `project/planning/MI_DOC.pdf` junto al MD.

---

## 4. Full path — script Python

```bash
# Con logos (auto-detecta de project/planning/project-config.md o raíz)
python3 .claude/skills/fx-pdf-export/scripts/build_pdf.py project/planning/00_DISCOVERY_BRIEF.md

# Sin logos
python3 .claude/skills/fx-pdf-export/scripts/build_pdf.py project/planning/00_DISCOVERY_BRIEF.md --no-logos

# Con apéndice
python3 .claude/skills/fx-pdf-export/scripts/build_pdf.py project/planning/00_DISCOVERY_BRIEF.md \
  --appendix "Apéndice A — Catálogo Figma:project/planning/FIGMA_SCREEN_CATALOG.md"

# Output custom
python3 .claude/skills/fx-pdf-export/scripts/build_pdf.py project/planning/00_DISCOVERY_BRIEF.md \
  --output docs/exports/brief.pdf
```

---

## 5. Detección automática de metadata

| Dato                                   | Origen                                                 | Fallback                             |
| -------------------------------------- | ------------------------------------------------------ | ------------------------------------ |
| Título                                 | H1 del MD (`# Discovery Brief — Kuen`)                 | Nombre del archivo                   |
| Fecha / Versión / Stakeholders / Autor | `**Fecha:** …` al inicio del MD                        | Valores genéricos                    |
| Logo TimeKast                          | `project/planning/project-config.md` → `timekast_logo` | `*timekast*` o `unnamed.png` en raíz |
| Logo Cliente                           | `project/planning/project-config.md` → `client_logo`   | `*logo*.{png,webp,svg,jpg}` en raíz  |

Para omitir logos: `--no-logos`.

---

## 6. Flags

| Flag                             | Default                        | Descripción                                      |
| -------------------------------- | ------------------------------ | ------------------------------------------------ |
| `--no-logos`                     | `false`                        | Omitir logos en portada                          |
| `--no-toc`                       | `false`                        | Omitir tabla de contenidos                       |
| `--no-cover`                     | `false`                        | Sin portada (fast path con CSS)                  |
| `--appendix "Título:archivo.md"` | —                              | Agregar apéndice (repetible)                     |
| `--output path.pdf`              | `<input>.pdf`                  | Ruta del PDF de salida                           |
| `--skip-lines N`                 | `9`                            | Líneas de header del MD a omitir (ya en portada) |
| `--css path.css`                 | `resources/timekast-style.css` | CSS custom                                       |

---

## 7. Personalización del CSS

Editar `resources/timekast-style.css`. Variables:

| Variable   | Default   | Qué controla   |
| ---------- | --------- | -------------- |
| `--purple` | `#5B2D8E` | Color primario |
| `--green`  | `#00C853` | Acento         |
| `--teal`   | `#4DB6AC` | Gradientes     |

Para branding diferente por cliente, pasar `--css path/to/cliente.css`.

---

## 8. Estructura

```
.claude/skills/fx-pdf-export/
├── SKILL.md
├── resources/
│   └── timekast-style.css       # CSS del kit (Inter + morado/verde/teal)
└── scripts/
    └── build_pdf.py             # Driver Python (metadata + cover + TOC + appendix)
```

---

## 9. Troubleshooting

| Síntoma                 | Causa probable                                 | Fix                                                    |
| ----------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| "No logos found"        | No hay `timekast_logo`/`client_logo` en config | Usar `--no-logos` o agregar paths en project-config    |
| Portada con meta vacía  | MD no tiene `**Fecha:** …` en header           | Agregar bloque de metadata o `--no-cover`              |
| Contenido se corta raro | `--skip-lines` no coincide con tu header       | Ajustar `--skip-lines` al número real de líneas header |
| TOC vacío               | Doc no tiene H2 (`##`)                         | Usar `--no-toc` o agregar H2                           |
| PDF sin estilo          | CSS path inválido                              | Verificar `--css` apunta a archivo existente           |

---

## 10. Anti-patrones

| ❌ Don't                                              | ✅ Do                                                       |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| Editar el CSS del kit para un cliente específico      | Pasar `--css cliente.css` y dejar el kit intacto            |
| Pegar logos en el MD como imágenes inline             | Apuntar `project-config.md` → `timekast_logo`/`client_logo` |
| Hardcodear rutas absolutas en scripts que usan el PDF | Usar rutas relativas a project root (lo resuelve el script) |
| Generar PDFs con `md-to-pdf` sin `printBackground`    | Dejar `printBackground:true` (colores de la portada)        |

---

_TimeKast Factory — fx-pdf-export skill_
