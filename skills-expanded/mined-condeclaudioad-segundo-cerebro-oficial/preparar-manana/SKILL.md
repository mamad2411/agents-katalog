---
name: preparar-manana
description: El hábito nocturno — la persona cuenta con detalle las tareas de mañana y la IA adelanta esta noche todo lo que puede (borradores, investigación, presentaciones, guiones), dejando los entregables listos para revisar a primera hora. Nunca envía ni publica nada. Usar con /preparar-manana, "preparame mañana", "estas son mis tareas de mañana".
argument-hint: "[las tareas, o dictalas en un audio]"
---

# /preparar-manana — mañana empieza la noche anterior

El hábito: a la noche anotás todas las tareas de mañana y se las contás a tu IA **con lujo de detalle**, como se las contarías a tu mano derecha. Ella adelanta todo lo que se puede adelantar. A la mañana revisás en vez de arrancar de cero.

## 1 · Escuchar

- Pedí que cuente cada tarea con el detalle que tenga: para qué es, para quién, qué sería "bien hecho". Si mandó un audio transcripto, trabajá sobre eso.
- Guardá lo que contó tal cual en `RAW/AAAA-MM-DD-manana.md` (fecha de mañana). Es la fuente.

## 2 · Clasificar cada tarea

| Tarea | ¿Qué puede adelantar la IA esta noche? | ¿Qué queda solo para la persona? |
|---|---|---|

Se puede adelantar casi siempre: borradores de mensajes, investigación, una presentación o los puntos clave de una clase, guiones o puntos para grabar, una primera versión de un documento, ordenar datos, preparar el brief para otro proyecto.
Queda para la persona: decidir, aprobar, poner la cara, apretar enviar, pagar, publicar.

Si una tarea es ambigua, preguntá con opciones antes de adelantar a ciegas.

## 3 · Ejecutar lo que se puede

- Usá las skills que existan (`SKILLS/README.md`) y el contexto del cerebro.
- Cada entregable va a `OUTPUTS/AAAA-MM-DD-manana/` (fecha de mañana), un archivo por tarea.
- **Nunca envíes, publiques, pagues ni cambies algo en un sistema externo.** Todo queda como borrador.

## 4 · Dejar la lista de la mañana

`OUTPUTS/AAAA-MM-DD-manana/LEEME.md`:

```markdown
# Mañana · <fecha>

## Revisá primero (ya está adelantado)
1. <tarea> → <archivo> · qué falta: aprobar / ajustar X

## Solo vos
- <tarea> · por qué no se pudo adelantar

## Lo que no pude hacer
- <tarea> · qué faltó (un dato, un acceso)
```

Changelog arriba (una línea) y commit. En el chat: cuántas adelantaste, cuántas quedan solo para la persona, el link.

## Honestidad

Cuánto se adelanta depende de qué tareas son. Un día de llamadas se adelanta poco; un día de producción, mucho. No prometas porcentajes.
