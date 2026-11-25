---
name: chatgpt-web-subagent
description: >
  Router to ChatGPT web skills. Use when the user says chatgpt-web-subagent
  or asks for ChatGPT web without naming image / deep research / search.
  Pick chatgpt-web-image, chatgpt-web-deep-research, or chatgpt-web-search
  and follow that skill. Do not generate the artifact in Codex/Cursor;
  open chatgpt.com.
---

# ChatGPT web — router

Leé `chatgpt-web-core`, después **una** skill:

| Pedido | Skill |
|---|---|
| Imágenes, stills, key art, concepto | `chatgpt-web-image` |
| Informe largo, Deep Research, “miles de fuentes” | `chatgpt-web-deep-research` |
| Búsqueda corta con links | `chatgpt-web-search` |

No pidas 5 imágenes en un prompt. No aplanes el chip de Deep Research. Guardá el archivo, decí la ruta, borrá el chat del job.
