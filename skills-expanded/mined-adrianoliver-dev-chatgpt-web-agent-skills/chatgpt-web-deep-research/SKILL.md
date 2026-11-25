---
name: chatgpt-web-deep-research
description: >
  Runs ChatGPT Deep Research on chatgpt.com (plus-menu chip, not a
  paragraph). Pastes the mega-prompt first, binds Deep research, waits for
  Researching... (minutes), downloads the cited report to a named file,
  tells the human the path, then deletes that chat. Use when the user
  asks for Deep Research, informe citado, chatgpt-web-deep-research.
  Not for a quick @web search and not for image generation.
---

# ChatGPT web — Deep Research

Lee `chatgpt-web-core`. Abrí `https://chatgpt.com`. **No** uses Codex para el informe.

Deep Research ≠ search. Un párrafo en &lt;30s **falló**.

## Orden (probado 2026-09)

1. Snapshot de Recientes (para no borrar chats ajenos).
2. **New chat**.
3. Pegá el mega-prompt **primero** (sin `@deep research` en el texto).
4. Think on.
5. `+` → **Deep research / Get a detailed report**. Chip azul + tabs Suggested / Reports.
6. **Send ya.** No type, no toggle Think: aplanan el chip.
7. Plan card (a menudo iframe). Start si hay countdown.
8. Éxito: **Researching...** minutos. **Quedate en ese hilo.**
9. Harvest a disco (abajo). Contá citations / searches en el mensaje final.
10. Si 0 citations y 0 searches: **decilo**. No lo vendas como informe con “miles de fuentes”. En Plus: Sol + Maximum.

## Qué pedir en el prompt

Fuentes primarias. Hecho vs inferencia vs especulación. Nada de cifras inventadas.

## Guardar (el punto que la gente extraña)

Antes de cerrar el hilo:

1. Copiá el informe completo (botón copiar del mensaje, o Download/Export si aparece, o Share → copiar).
2. Escribí el markdown a:
   `<out>/<run>/<run>-deep-research.md`
   Si hay PDF nativo: `<run>-deep-research.pdf` al lado.
3. `snapshot.txt` en la misma carpeta: URL del chat, modelo, conteo de searches/citations, ruta del archivo.
4. **En el chat de Cursor**, listá la ruta absoluta. Eso es el deliverable.
5. Recién entonces **Delete** ese chat de chatgpt.com (ver núcleo).

No dejes el report “en el hilo”. chatgpt.com no es el archivo.

## La persona en un chat nuevo

```
Usa chatgpt-web-deep-research.
[tema]. Guardá el informe con nombre y decime la ruta. Después borra ese chat.
```
