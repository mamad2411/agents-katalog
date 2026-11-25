---
name: chatgpt-web-core
description: >
  Shared ChatGPT web UI contract: chatgpt.com in a real browser (not Codex
  imagegen), New chat vs continue, Think, plus-menu tools, named harvest on
  disk, tell the human the path, then delete agent-created chats. Use when
  another chatgpt-web-* skill says to read this first.
---

# ChatGPT web — núcleo

Cursor / Codex **no** generan el artefacto final. Abren `https://chatgpt.com` (Browser de Cursor, Chrome con sesión, o Cua Driver). Las cookies del Browser de Cursor **no** son las de Chrome.

## Chat nuevo vs continuar

| Caso | Acción |
|---|---|
| Job nuevo | **New chat** |
| ChatGPT sigue generando / Researching | Continuar ese hilo |
| Misma pieza, regenerar porque falló QA | Continuar |
| Shot / informe siguiente | **New chat** |
| Tool aplanado (texto en &lt;30s en vez de research) | **New chat** |

Al **empezar** el job: anotá los títulos que ya estaban en Recientes. Al final solo borramos chats **nuevos de este job**.

## Tools

- Imagen: `@create image` → **Create image**. Un prompt = **una** imagen.
- Search corto: `@web search` o `+` → Web search.
- Deep Research: **pega el prompt primero** → Think → `+` → **Deep research** → Send **sin** type después del chip (aplana la pill).
- Work: Free muestra Unlock with Plus → blocked.
- Computer Use nativo de ChatGPT: hace falta la app desktop. Preferí **Cua Driver** en Cursor para controlar Chrome.

Plus: Luna / Terra / Sol + Maximum. Free: Think sí; no finjas el switcher.

## Composer

- Send = botón **Send prompt** (círculo azul). Enter suele hacer newline.
- Autocomplete de `@` a menudo es `generic`; click por texto visible.
- Sidebar expandido puede tapar el composer: ciérralo para generar, abrilo para borrar chats.
- File picker del Simple Browser de Cursor a veces no rellena el diálogo nativo: usá Chrome + pegar imagen (`clipboard` + `Ctrl+V`) o pedile a la persona el file picker.

## Dónde guardar (obligatorio)

Resolvé **una** carpeta de salida, en este orden:

1. La ruta que dio la persona.
2. Si hay workspace de proyecto: `<workspace>/chatgpt-web/<run>/`
3. Si no: `~/Documents/ChatGPT-web/<run>/` (Windows: `%USERPROFILE%\Documents\ChatGPT-web\<run>\`)

`<run>` = `YYYY-MM-DD-<slug>` en ASCII (`2026-09-13-steam-wishlists`).

| Artefacto | Nombre |
|---|---|
| Deep Research | `<run>-deep-research.md` (y PDF si ChatGPT lo ofrece) |
| Search corto | `<run>-search.md` |
| Imagen KEEP | nombre semántico pedido (`hero.png`, `portrait.png`) en `approved/` |
| Imagen FAIL | `rejected/<shot>-attemptNN.png` |
| Meta del job | `snapshot.txt` (URLs de los hilos, qué se guardó) |

PNG &lt; 2048 bytes no cuenta. Screenshot de UI no es harvest.

### Decile a la persona dónde quedó

El mensaje final **tiene** que listar rutas absolutas, no “lo guardé en el inbox”. Ejemplo:

```
Guardado:
  C:\Users\alex\Documents\ChatGPT-web\2026-09-13-wishlists\2026-09-13-wishlists-deep-research.md
```

Si no podés escribir a disco, **pará** y pedí carpeta. No dejes el informe solo en chatgpt.com.

## Borrar el chat (después de guardar)

El historial de chatgpt.com se llena de “New chat” / “Create image” basura. Después de **guardar y verificar** el archivo en disco:

1. Solo hilos **creados en este job** (compará contra el snapshot de Recientes).
2. Sidebar → ⋯ en ese chat → **Delete** → confirmar.
3. No borres chats personales que ya existían (estudio, idiomas, trabajo).
4. Si el KEEP falló y vas a regenerar: **no** borres ese hilo todavía.
5. Si la persona dice “no borres nada”, obedecé.

Nunca borres la cuenta, nunca *Clear all chats* salvo que lo pidan con el texto exacto.

## Cua Driver (opcional, recomendado)

Para pulsar Chrome de verdad: [Cua Driver](https://cua.ai/cua-driver) + MCP `cua-driver mcp`. Receta: `docs/cua-driver.md`. No mezcles Computer Use de ChatGPT con Cua en el mismo gesto.

## Honestidad

No prometas millones de wishlists ni “miles de fuentes” si el job hizo 0 searches. No copies franquicias. No apagues el PC.
