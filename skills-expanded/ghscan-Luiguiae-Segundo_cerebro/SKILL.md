# SKILL: profundizador-conceptos

**Nombre:** profundizador-conceptos
**Versión:** 0.1
**Entorno:** Claude Code con web search
**Filesystem objetivo:** `~/Documents/Segundo_cerebro/`

---

## Activación

Esta skill se activa cuando el usuario pega un borrador de concepto (texto libre o ruta a `.md` existente) y dice alguna variante de:

- "profundiza este concepto"
- "investiga más sobre esto"
- "robustece el concepto"
- "busca fuentes para esto"

El input puede ser:
- Texto pegado directamente en el chat
- Una ruta relativa a un archivo existente en `Conocimiento/Conceptos/`

---

## Flujo de ejecución

### PASO 1 — Extracción de ejes

Lee el borrador de entrada (texto pegado o archivo `.md` en `Conocimiento/Conceptos/`).

Identifica entre 3 y 5 **ejes de investigación**: temas centrales, tensiones, afirmaciones que necesitan respaldo, o datos numéricos sin fuente.

Prioriza los 3 ejes con mayor impacto para el argumento del concepto.

> No informas al usuario. Pasas directamente al Paso 2.

---

### PASO 2 — Investigación web

Por cada eje priorizado, lanza búsquedas web con queries específicos.

Busca: artículos, papers, posts, reportes, datos con fecha.

**Criterios de calidad para incluir un hallazgo:**
- Tiene autor o institución identificable
- El dato o argumento es verificable
- Agrega algo que el borrador no tiene

Descarta fuentes débiles: sin autor, sin fecha, contenido genérico.

**Mínimo 2 fuentes sólidas por eje.** Si un eje no produce fuentes de calidad, descártalo y notifícalo en el output.

---

### PASO 3 — Construcción del concepto enriquecido

Toma el borrador original y enriquécelo con los hallazgos.

**Reglas de enriquecimiento:**
- No reemplaces el argumento central del borrador — expándelo
- Cada dato numérico debe tener: cifra, fecha, fuente
- Cada afirmación nueva debe citar su origen
- No inventes datos. Si no encontraste respaldo para algo, déjalo igual que en el borrador o márcalo con `[sin fuente verificada]`

---

## Output format

Entrega un archivo `.md` con la siguiente estructura:

```markdown
---
titulo: [título del concepto]
tipo: concepto
fecha: YYYY-MM-DD
tags: [tag1, tag2, tag3]
relacionado: []
fuentes:
  - titulo: "[título del artículo o post]"
    url: "[url]"
    fecha_acceso: YYYY-MM-DD
---

# [Título]

## El concepto
[Definición central — del borrador, expandida si aplica]

## Por qué importa
[Argumento de relevancia — enriquecido con hallazgos]

## Datos y evidencia
[Sección nueva: cifras, estudios, ejemplos concretos encontrados en la investigación]

## Tensiones y límites
[Qué cuestiona o contradice este concepto — del borrador o hallado en la investigación]

## Ejes investigados
[Lista de los 3 ejes usados para la búsqueda, con 1 línea de qué se encontró en cada uno]
```

---

## Restricciones — v0.1

- **No guarda el archivo en disco automáticamente.** Entrega el `.md` en chat. El usuario decide cuándo y con qué nombre guardarlo.
- **No investiga más de 3 ejes por ejecución.**
- **No modifica `INDEX.md`** — eso lo hace `generar_index.py` por separado.
- Si el input es una ruta a `.md` y el archivo no existe, informa y detente.
- Output siempre en **español**.

---

## Ejemplo de activación

```
Usuario: "Jarvis, profundiza este concepto:

El diseño de fricción intencional consiste en agregar pequeñas resistencias
al flujo de una interfaz para reducir decisiones impulsivas..."
```

Claude ejecuta los 3 pasos en silencio y entrega el `.md` enriquecido.
