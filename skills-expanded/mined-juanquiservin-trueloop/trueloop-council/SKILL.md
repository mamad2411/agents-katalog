---
name: trueloop-council
description: Convoca un consejo de mentalidades (CEO, CFO, CTO, Product, Security, Growth, Devil's Advocate y más) para atacar una decisión desde lentes independientes y producir una recomendación clara. Úsalo cuando el usuario escriba /trueloop-council, pida opinión desde varias perspectivas, tenga que decidir algo difícil de revertir, esté atorado entre opciones, o pregunte "¿esto es buena idea?".
argument-hint: <la decisión que hay que tomar>
---

# TRUELOOP · Consejo de mentalidades

No todo problema es una tarea. Algunos son **decisiones**, y una decisión mal tomada
no se arregla con más iteraciones del loop: se arregla pensándola bien una vez.

Este comando no escribe código. Convoca lentes independientes, los enfrenta, y produce
una recomendación que el humano puede ejecutar.

## Paso 1 · Entiende la decisión de verdad

Antes de convocar a nadie, reformula la pregunta en una frase y **enséñasela al usuario**.
La mitad de las decisiones difíciles se disuelven cuando se enuncian bien.

Si la pregunta trae una opción escondida como premisa ("¿cobramos $29 o $49?" cuando la
pregunta real es "¿cobramos por suscripción?"), **dilo antes de seguir**.

## Paso 2 · Elige las mentalidades

Lee `references/mindsets.md` del skill `trueloop` - están las 40 con contrato completo.

**Regla de composición**: 3-5 mentalidades con lentes **genuinamente distintos**.
Si dos van a decir lo mismo, cambia una. La redundancia se siente como consenso
y no lo es.

**Incluye siempre `devils-advocate`** cuando la decisión sea difícil de revertir.

### Consejos preconfigurados

| Si la pregunta es… | Convoca |
|---|---|
| ¿construimos esto? | ceo · cfo · competitive · devils-advocate |
| ¿esta arquitectura? | cto · security · performance · simplifier |
| ¿ya podemos lanzar? | qa · security · product · customer-success · devils-advocate |
| ¿cuánto cobramos? | cfo · cmo · growth · competitive |
| ¿esto es seguro? | security · red-team · privacy · legal |
| ¿por qué no crece? | growth · data-analyst · ux · user-researcher |
| me saturé, hay demasiadas opciones | chief-of-staff · simplifier · ceo |
| ¿qué nos va a matar? | devils-advocate · red-team · cfo · cto |

Di al usuario a quién convocaste y **por qué esos y no otros**, en una línea cada uno.

## Paso 3 · Ronda independiente

Lanza los subagentes **en paralelo, en un solo mensaje** (`Task`).

**Ninguno ve la respuesta de los otros en esta ronda.** La independencia es lo único que
evita el anclaje, y el anclaje es lo que convierte un consejo en un eco.

A cada uno dale:
- la decisión, tal como quedó reformulada
- el contexto real: `.trueloop/PROJECT.md`, `SPEC.md`, estado del repo, lo que aplique
- sus **preguntas clave** y **banderas rojas** del catálogo
- instrucción de cerrar con: **postura · razones · qué tendría que ser cierto para
  cambiar de opinión · su nivel de confianza**

Ese último punto es el más valioso. Una postura sin condición de cambio es un dogma.

## Paso 4 · Síntesis (sin promediar)

**La síntesis no promedia. Nombra el choque.**

```
╔══ CONSEJO · <decisión> ══════════════════════════════════════╗

 COINCIDEN
   Los cuatro coinciden en que <...> porque <...>

 CHOCAN            ← esto es lo más valioso del ejercicio
   CFO dice <A>.  CTO dice <B>.
   No es un desacuerdo de opinión: optimizan cosas distintas.
   CFO optimiza costo a 12 meses; CTO optimiza costo de cambiar de opinión.
   Quien tenga razón depende de <la variable real que decide>.

 LO QUE NADIE VIO
   <lo que salta al juntar las cuatro respuestas y ninguna traía sola>

 RECOMENDACIÓN
   <una decisión clara, no un "depende">
   Condiciones: <bajo qué supuestos vale>
   Señal de cambio: <si pasa X, esta recomendación deja de valer>
   Primer paso concreto: <qué hacer el lunes>

 RIESGO PRINCIPAL
   <el que sobrevivió al devil's advocate>
╚══════════════════════════════════════════════════════════════╝
```

## Reglas duras

- **Nunca termines en "depende".** Si de verdad depende, di **de qué** y **qué haría
  falta saber** para decidir. Eso ya es una recomendación: averiguar eso primero.
- **Nunca escondas el desacuerdo.** El choque entre dos lentes es información, no ruido.
  Un consejo donde todos coinciden probablemente estaba mal compuesto.
- **Nunca inventes datos.** Si el CFO necesita números que no existen, la salida es
  "hay que estimar esto antes de decidir", no una cifra inventada.
- Si el usuario ya trae una decisión tomada y busca validación, **dilo con respeto** y
  da el mejor contraargumento de todos modos. Para eso te contrató.

## Registro

Si hay un proyecto TRUELOOP activo, anexa la decisión y su razón a
`.trueloop/DECISIONS.md` con fecha. Dentro de un mes nadie se va a acordar de por qué,
y ese olvido es carísimo.
