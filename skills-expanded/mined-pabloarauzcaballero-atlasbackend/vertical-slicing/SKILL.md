---
name: vertical-slicing
description: Cómo cortar un carril o feature en slices verticales pequeños y observables — cada slice atraviesa sólo las capas que necesita (contrato/datos → backend → frontend → integración → tests), es demostrable por sí mismo y se ordena por riesgo. Usar al planificar la implementación de un carril, al ver un plan organizado por capas horizontales ("primero todo el backend"), o cuando un cambio creció tanto que no se puede probar hasta el final. Partir un pedido grande en unidades entregables es `lane-authoring`; acá la unidad ya está definida.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Corte en slices verticales

Un slice vertical entrega una porción del resultado observable atravesando las capas que hagan
falta, no una capa entera del sistema. El objetivo es tener algo ejercitable y verificable
seguido, no acumular cambios para probar al final. Complementa a `lane-authoring` (define el
carril) y a `outcome-first` (define el resultado).

## Cuándo aplica

- Al planificar cómo se implementa un carril o feature.
- Cuando el plan dice "primero todo el backend, después toda la UI" — eso es horizontal, mal.
- Cuando un cambio se volvió tan grande que no hay nada que probar hasta el cierre.

## 1. Vertical, no horizontal

- **Vertical (bien)**: "crear una franja de bloqueo y verla desaparecer de disponibilidad" —
  toca contrato, backend, UI y test, pero es una rebanada fina y demostrable.
- **Horizontal (mal)**: "implementar todos los endpoints de agenda", luego "toda la UI de agenda".
  Nada es observable hasta el final y el riesgo se descubre tarde.

## 2. Capas por slice — sólo las necesarias

Un slice puede recorrer, en este orden cuando aplica:

`A. contrato/datos → B. backend → C. frontend → D. integración → E. tests`

Pero **no inventes capas**: si un requisito se completa sin tocar el backend (por ejemplo, un
arreglo puramente visual), no agregues una capa de datos para justificar una arquitectura. El
slice toca lo que el resultado exige y nada más — ver `scope-discipline`.

## 3. Cada slice es observable y probable

- Al terminar un slice tiene que haber algo que se pueda **ver correr** y verificar, aunque sea
  un pedazo chico del resultado final.
- Definí para cada slice: objetivo, archivos previstos, comportamiento observable esperado.
- Verificá al cerrar el slice (`evidence-and-verification`), no acumules 20 cambios para el final.

## 4. Orden por riesgo

- Poné primero el slice que **más incertidumbre elimina**: la integración dudosa, el contrato con
  otro repo, la query que puede no escalar. Fallar temprano es barato.
- Los slices de bajo riesgo y alto volumen (más pantallas del mismo patrón) van después.
- Respetá dependencias: si C necesita el contrato de A, A va primero.

## 5. Andamiaje mínimo

Está bien un primer slice "de punta a punta pero mínimo" (un solo campo, un solo caso) para
validar que las capas conectan, y después ensanchar. Es preferible a construir cada capa completa
a ciegas.

## Anti-patrones

- Plan por capas horizontales.
- Slices que no se pueden demostrar hasta el final.
- Inventar backend/datos para un cambio que era sólo de UI.
- Dejar los tests como un slice final separado en vez de cerrar cada slice con su prueba.
- Empezar por lo fácil y descubrir el riesgo real el último día.

## Checklist

- [ ] El plan está en slices verticales, no en capas horizontales.
- [ ] Cada slice es observable y tiene su verificación.
- [ ] Ningún slice inventa capas que el resultado no exige.
- [ ] Los slices están ordenados por riesgo/incertidumbre y respetan dependencias.
- [ ] El primer slice reduce la mayor incertidumbre del carril.
