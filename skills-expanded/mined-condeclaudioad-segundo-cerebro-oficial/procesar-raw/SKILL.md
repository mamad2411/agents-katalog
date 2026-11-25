---
name: procesar-raw
description: Procesa lo nuevo de RAW/ hacia WIKI/ — lee los archivos enteros, extrae decisiones, datos y reglas, actualiza los temas, el índice y el changelog, y marca los 3 huecos más grandes. Usar con /procesar-raw, "procesá RAW", "procesá esto" o cuando la persona tira material nuevo en RAW/. No para responder preguntas sueltas.
argument-hint: "[opcional: archivo o carpeta concreta de RAW/]"
---

# /procesar-raw — de lo crudo a lo ordenado

## 1 · Qué hay nuevo

- Si te pasaron un archivo, ese. Si no: listá `RAW/` y quedate con los archivos **que no están citados** en `WIKI/` ni en `changelog/` (`grep -rl "<nombre-de-archivo>" WIKI changelog`).
- Si son más de 5, procesá los 5 más nuevos y anotá el resto como pendiente. Mejor 5 bien que 30 mal.

## 2 · Leer de verdad

- Abrí cada archivo **entero**. Nunca resumas un archivo que no abriste.
- Sacá: decisiones (con fecha y quién decidió), datos con su fuente, conceptos, reglas de trabajo, tareas pendientes.
- Tirá el ruido: saludos, repeticiones, lo que no cambia nada.
- **Más de una persona hablando** (llamada, podcast, reunión): separá quién dijo qué. Lo que dijo otro no es una decisión de la persona.
- Cifras dichas de memoria se anotan como *"dicho el <fecha>"*, no como dato verificado.

## 3 · Ordenar en WIKI

- Cada dato va al tema que le corresponde. Si el tema no existe, lo creás (`WIKI/<tema>.md`, nombre corto en minúsculas con guiones).
- Un RAW que toca tres temas se reparte en los tres.
- **No dupliques: ampliá.** Si el tema ya dice algo, actualizalo con la fecha. Si lo nuevo contradice lo viejo, gana lo más reciente y explícito, y dejás una línea: *"Antes: X (fecha). Cambió a Y (fecha, fuente)."*
- Cada afirmación lleva su fuente: link relativo al RAW.
- Conectá temas con `[[tema]]`.

## 4 · Índice, changelog, memorias

- `WIKI/index.md`: temas nuevos en una línea cada uno.
- Si apareció una **regla de cómo trabajar** (no un dato), proponé guardarla con `/recordar`.
- `changelog/AAAA-MM.md`: entrada **arriba**, con qué procesaste, qué temas tocaste y los 3 huecos.

## 5 · Reportar (corto)

```
Procesé: 3 archivos (lista)
Toqué: negocio, clientes, ads (+1 nuevo: proveedores)
Pendientes en RAW: 4
Los 3 huecos:
1. <qué tema/dato falta> → <qué fuente lo cerraría>
2. …
3. …
```

Si hay remoto: commit + push (regla de `CLAUDE.md`).

## Reglas

- RAW es solo lectura. Nunca lo edites.
- Si un archivo no tiene nada que valga, decilo (*"sin valor para WIKI"*) y cuenta como procesado.
- No inventes contenido para llenar la WIKI.
