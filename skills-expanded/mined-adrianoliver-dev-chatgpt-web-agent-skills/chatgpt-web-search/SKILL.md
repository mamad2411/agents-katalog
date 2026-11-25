---
name: chatgpt-web-search
description: >
  Runs ChatGPT web search on chatgpt.com (@web search or plus-menu Web
  search), Think on, short sourced answer saved to a named markdown file.
  Tells the human the path, then deletes the chat. Use when the user asks
  for a ChatGPT web search, @web search, chatgpt-web-search, or a quick
  sourced brief — not Deep Research and not image generation.
---

# ChatGPT web — search

Lee `chatgpt-web-core`. Abrí `https://chatgpt.com`.

Esto es una respuesta corta con links, no el job Deep Research de minutos. Si piden “miles de fuentes”, usá `chatgpt-web-deep-research`.

## Receta

1. Snapshot de Recientes. **New chat**.
2. `@web search` (elige Web search) **o** `+` → Web search.
3. Think on.
4. Prompt concreto: pregunta + qué no inventar + “listá URLs al final”.
5. Esperá búsquedas reales en la UI.
6. Guardá `<out>/<run>/<run>-search.md` + `snapshot.txt`.
7. Decí la ruta absoluta.
8. **Delete** ese chat.

## La persona en un chat nuevo

```
Usa chatgpt-web-search.
[pregunta]. Fuentes al final. Guardá el .md y decime la ruta. Después borra el chat.
```
