---
name: crear-skill
description: Convierte una tarea que se repite en una skill de Claude Code (subir de Nivel 1 a Nivel 2) — entrevista con opciones, escribe .claude/skills/<nombre>/SKILL.md, la prueba con un caso real y la suma al catálogo. Usar con /crear-skill, "convertí esto en skill", "esto lo hago todas las semanas" o cuando una tarea se explica por tercera vez.
argument-hint: "[la tarea, ej. \"responder consultas de clientes\"]"
---

# /crear-skill — de hablarlo cada vez a llamarlo por su nombre

Una skill es **un método probado, guardado**. La llamás por su nombre y la IA va sola, sin pedirte el contexto de nuevo. La skill no es un prompt largo: es tu forma de hacer algo, escrita una vez.

## 1 · ¿Califica?

Preguntá en bloque, con opciones:
1. ¿Cada cuánto la hacés? A) 2-3 veces por semana o más **(califica)** · B) Una vez por semana · C) Menos
2. ¿Tenés un método que funciona (tuyo o de alguien que te enseñó)? A) Sí, siempre lo hago igual · B) Más o menos · C) No, cada vez distinto

Si es **C en la 1** o **C en la 2**: todavía es Nivel 1. Decilo sin vueltas: *"Primero hacela 3 veces hablándola conmigo. Cuando veas que siempre pedís lo mismo, la guardamos."* Y anotá la tarea como candidata en `SKILLS/README.md` § Candidatas.

## 2 · Entrevista (con opciones donde se pueda)

- **Qué entra:** qué le pasás cada vez (un link, un archivo, un nombre, nada).
- **Los pasos:** cómo la hacés vos, en orden. Si ya la hicieron juntos en esta sesión o en una anterior, **reconstruí los pasos de ahí** y pedile que confirme.
- **Un ejemplo bueno:** pedile una salida real que ya aprobó. Es lo que más mejora una skill. Si no hay, queda como hueco.
- **Qué es "bien hecho":** 3-5 criterios que se puedan chequear.
- **Qué nunca hace:** límites (*"nunca envía"*, *"nunca gasta"*, *"nunca publica"*).
- **Dónde deja el resultado:** chat, `OUTPUTS/`, un borrador.
- **¿Necesita ver el resultado antes de que salga?** Casi siempre sí: entonces la skill entrega **borrador**, nunca ejecuta lo final.

## 3 · Escribila

`.claude/skills/<nombre-corto>/SKILL.md` — nombre en minúsculas con guiones, un verbo si se puede (`responder-consultas`, `buscar-ofertas`).

```markdown
---
name: <nombre-corto>
description: <Qué hace en una frase>. Usar cuando <frases con las que la persona la pediría>. No usar para <lo que se parece pero no es>.
argument-hint: "[qué se le pasa]"
---

# /<nombre-corto> — <para qué sirve en 5 palabras>

## Antes de arrancar
Qué leer del cerebro (WIKI, MEMORIA) y qué pedir si falta.

## Pasos
1. …
2. …

## Bien hecho es
- criterio chequeable
- …

## Nunca
- …

## Entrega
Dónde queda el resultado y qué se le dice a la persona.
```

La `description` es lo más importante: es lo que la IA lee para decidir si la usa. Escribí las frases reales con las que la persona la pediría.

## 4 · Probala con un caso real

- Corréla ya, sobre un caso de verdad.
- Compará la salida con los criterios de "bien hecho". Lo que falló se corrige **en la skill**, no en la salida.
- Hasta que no corrió bien una vez, no está terminada.

## 5 · Registrala

- Línea en `SKILLS/README.md`: `| /<nombre> | qué hace | cada cuánto | creada <fecha> |`.
- Entrada arriba en `changelog/AAAA-MM.md`.
- Si la skill ya tiene reglas fijas del tipo *"si pasa X, hacé Y"* y no necesita revisión, decí: *"Esta podría subir a rutina con `/crear-rutina`."* Solo decilo; no la subas.

## Mantenimiento

Cuando la persona corrige una salida de la skill, **la corrección va a la skill** (con fecha), no solo a esa salida. Una skill que no aprende de sus correcciones repite el error para siempre.
