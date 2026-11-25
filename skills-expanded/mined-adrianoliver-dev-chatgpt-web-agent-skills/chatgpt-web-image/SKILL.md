---
name: chatgpt-web-image
description: >
  Runs ChatGPT Images on chatgpt.com as a directed art loop: attach 3–4
  refs, @create image + Think, one still per prompt, visually QA each
  download, keep and name keepers or regenerate, tell the human the folder,
  then delete agent chats. Use when the user asks for ChatGPT images,
  GPT image, stills, key art, chatgpt-web-image. Never ask for 5 images
  in one prompt.
---

# ChatGPT web — imágenes (loop de dirección)

Lee `chatgpt-web-core`. Abrí `https://chatgpt.com`. **No** uses Codex ni el imagegen nativo de Cursor para el archivo final.

## Veto

Un prompt “haz 5” produce collage y extras. Una imagen por Send.

## UI rápida

New chat por shot. `@create image` → Create image. Think on. Send = **Send prompt**. Plus: Sol + Maximum. Regen del mismo shot: **continuar** el hilo. Chrome + pegar refs por clipboard suele ganar al file picker del Simple Browser.

## Loop (obligatorio)

1. **Leé** lore + assets con visión (tool Read). Si es un juego/producto: leé *ese* repo (docs + PNGs), no un pack genérico.
2. Lista de shots con **nombre de archivo final** (`hero.png`, `portrait.png`, …).
3. **Una imagen por Send.** Nunca “generate a set of 5”.
4. Primer Send de cada shot: **New chat** + 3–4 refs. Pedile el file picker a la persona si el Browser no lo rellena.
5. `@create image` → Think → prompt del shot. Send.
6. Esperá **un** PNG descargable. Collage, grid o 2+ frames → reject.
7. **Read** el PNG. Score contra refs + checklist.
8. **Keep:** copiá a `<out>/<run>/approved/<nombre>.png`.
9. **Fail:** **continuar el mismo hilo**. *ONE image only. Same shot. Match the attached refs. Fix: …* Máx. **3** reintentos. Luego preguntá.
10. Shot KEEP → ya podés **Delete** ese chat. Shot siguiente = **New chat** + refs otra vez.
11. Mensaje final: lista absoluta de keepers. Después borra los hilos de este job que sigan vivos.

## Checklist KEEP (si falla uno, regen)

- Exactamente 1 frame.
- Match de las refs (cara, props, paleta).
- Sin HUD, logos, watermarks, texto horneado (salvo que el brief lo pida).
- El encuadre es el shot pedido.

## La persona en un chat nuevo

```
Usa chatgpt-web-image.
[N] stills de [proyecto]. Loop QA. Subí refs. Una imagen por prompt.
Guardalas con nombre en [carpeta] y decime las rutas. Borra los chats cuando estén KEEP.
```
