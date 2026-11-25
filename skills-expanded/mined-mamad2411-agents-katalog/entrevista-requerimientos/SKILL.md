---
name: entrevista-requerimientos
description: Metodologia profesional para cerrar un requerimiento preguntando - como el analista de Mesa de Servicios detecta vacios y ambiguedades, formula preguntas puntuales en lenguaje de negocio (sin codigo, sin jerga), las agrupa en rondas cortas, usa faast-brain para no preguntar lo que el negocio ya sabe, maneja respuestas vagas o contradictorias, y decide cuando el requerimiento esta CERRADO con la checklist de completitud por tipo (bug, proyecto, cotizacion) y la clasificacion (tipo, cliente o transversal, producto, prioridad). Cargala antes de analizar cualquier solicitud.
---

# Entrevista de requerimientos — preguntar poco, preguntar bien (Mesa de Servicios)

El objetivo del analista no es "hacer preguntas": es **cerrar el requerimiento** con el
minimo de idas y vueltas, de forma que quien lo reciba despues (lider de producto, PO,
desarrollo) no tenga que volver a preguntarle nada al cliente. Cada pregunta cuesta tiempo
del cliente y confianza; por eso se pregunta solo lo que ninguna fuente ni el negocio
responden, y se pregunta de forma que la respuesta cierre el tema.

## Principios
1. **Primero se lee, despues se pregunta.** La solicitud normalizada (`solicitud.md`) y el
   brain (`faast-brain`) se leen ANTES de formular la primera pregunta. Lo que ya se sabe se
   CONFIRMA en una frase ("Entendemos que operan Confirming en modo 2.0; si no es asi,
   avisanos"), no se pregunta como si fuera nuevo.
2. **Lenguaje de negocio, siempre.** El cliente es gente de operaciones, finanzas, comercial.
   Prohibido: endpoints, tablas, campos de base de datos, nombres de servicios, "parsear",
   "refactorizar", "deployar", "nullable". Permitido y obligatorio: nombres de pantallas,
   botones, documentos, perfiles y procesos tal como el cliente los llama (usa el glosario).
3. **Una pregunta = una decision.** Cada pregunta busca cerrar UN vacio concreto. Nada de
   "¿nos puedes contar mas?": eso devuelve otra señal dispersa. Mejor: "Cuando la factura llega
   sin orden de compra, ¿se rechaza, se deja pendiente o se aprueba con una alerta?"
4. **Ofrece opciones cuando las hay.** Preguntar con alternativas concretas ("A, B o C, ¿o
   es otra cosa?") acelera y revela supuestos. Pero la ultima opcion siempre deja espacio a
   lo que no previste.
5. **Rondas cortas y ordenadas.** Maximo 5-7 preguntas por ronda, de lo mas estructural (que
   problema resuelve, quien lo usa) a lo mas fino (casos borde). Lo que bloquea entender el
   pedido va primero; lo cosmetico, al final o nunca.
6. **Nunca suponer para avanzar.** Si una respuesta no llega, el vacio queda marcado como
   "pendiente" en el documento; no se rellena con lo que "parece razonable".
7. **Profesional y breve.** Sin preambulos largos, sin disculpas, sin tecnicismos. Se agradece
   la respuesta, se confirma lo entendido en una linea, y se sigue.

## El ciclo
```
leer solicitud.md + brain → separar SABIDO / FALTA / CONTRADICE
        ↓
ronda N de preguntas (preguntas.md) → esperar respuestas del cliente (via mesa)
        ↓
registrar respuestas tal cual + lo que se decidio → actualizar SABIDO / FALTA
        ↓
¿checklist de completitud del tipo cumplida?  no → otra ronda (max 3; si no cierra, escalar)
        ↓ si
clasificar (tipo, cliente/transversal, producto, prioridad) → CERRADO → redactor
```
Tres rondas es el tope razonable. Si tras tres rondas sigue abierto, el problema no es de
preguntas: se escala al lider de mesa (reunion de trabajo con el cliente o decision de alcance).

## Checklist de completitud por tipo (el requerimiento esta CERRADO cuando todo esta ✔)

### BUG (algo que deberia funcionar de una forma y funciona de otra)
- [ ] **Que ve mal el usuario**, en una frase, como lo vive el negocio
- [ ] **Pasos exactos** como usuario para llegar al problema (pantalla, accion, dato)
- [ ] **Esperado vs. obtenido**, en terminos de negocio
- [ ] **Desde cuando** ocurre y si antes funcionaba (¿cambio algo: version, proceso, dato?)
- [ ] **A quien afecta**: un usuario, un perfil, un cliente, todos (alcance → cliente o transversal)
- [ ] **Frecuencia**: siempre, a veces, solo con ciertos datos
- [ ] **Impacto de negocio**: que proceso se frena, hay dinero o plazos de por medio, hay solucion provisoria
- [ ] **Evidencia disponible**: capturas, documentos, ejemplos concretos (el ID de una operacion real sirve)
- [ ] **Ambiente** donde ocurre (produccion, pruebas) y **usuario/perfil** con el que ocurre

### PRY (proyecto / funcionalidad nueva o cambio)
- [ ] **Problema u oportunidad** de negocio que origina el pedido (el "para que")
- [ ] **Objetivo** medible en terminos de negocio (menos tiempo, menos errores, nuevo ingreso)
- [ ] **Quienes lo usan** (perfiles/roles) y quien lo aprueba por el lado del cliente
- [ ] **Alcance**: que incluye y, tan importante, **que NO incluye**
- [ ] **Flujo deseado** de punta a punta, con los ejemplos concretos del cliente
- [ ] **Reglas de negocio** que rigen (plazos, montos, aprobaciones, excepciones)
- [ ] **Dependencias**: otros sistemas, otras areas, datos que deben existir, terceros
- [ ] **Restricciones**: fecha objetivo y su motivo, normativa, presupuesto si lo hay
- [ ] **Criterios de exito**: como sabra el cliente que quedo bien (base de los criterios de aceptacion)
- [ ] **Alcance de cliente**: ¿es para un cliente, para varios o transversal al producto?

### CTZ (cotizacion / pedido que requiere valorizacion y aprobacion comercial)
- [ ] Todo lo de PRY (una cotizacion es un proyecto aun no aprobado) **y ademas**:
- [ ] **Entregables** concretos que el cliente espera recibir
- [ ] **Supuestos** sobre los que se cotiza (lo que se da por cierto; si cambia, cambia la cotizacion)
- [ ] **Exclusiones** explicitas (lo que NO esta cotizado)
- [ ] **Plazo esperado** por el cliente y flexibilidad
- [ ] **Quien decide** la contratacion y que necesita para decidir (propuesta formal, demo, referencias)
- [ ] **Condiciones** relevantes (etapas, hitos de pago si el cliente las menciona, vigencia)
La valorizacion en si (esfuerzo, precio) NO la decide la Mesa: la propuesta deja el espacio y
el lider de mesa/comercial la completa, pidiendo estimacion al equipo de desarrollo si hace falta.

## Clasificacion (parte del cierre)
| Dimension | Valores | Como se decide |
|---|---|---|
| **Tipo** | BUG · PRY · CTZ | Bug = algo roto que ya existia. PRY = algo nuevo o cambio, ya aprobado o interno. CTZ = requiere valorizacion y aprobacion comercial antes de ser trabajo. Ante la duda entre PRY y CTZ: si hay que cobrar o aprobar presupuesto, es CTZ |
| **Alcance** | `cliente:{codigo}` · `transversal` | ¿Afecta/beneficia a un cliente especifico o al producto para todos? Un bug que ven todos es transversal aunque lo reporte un cliente |
| **Producto** | el del catalogo de faast-brain (factoring, confirming, leasing, cobranza, backoffice...) | Del contexto; si toca varios, el principal + los secundarios |
| **Prioridad sugerida** | critica · alta · media · baja | Por impacto de negocio y urgencia declarada; la define el lider de producto al priorizar, la Mesa solo sugiere con fundamento |

## Formato de una ronda (`preguntas.md`)
```markdown
## Ronda 1 — {fecha}
Lo que ya tenemos claro (solo confirmar): {1-3 frases}

1. **{tema}** — {pregunta concreta}. Opciones: a) … b) … c) otra: ___
2. **{tema}** — {pregunta}
...
(max 7)

### Respuestas — {fecha}
1. {respuesta tal cual del cliente} → **Decidido:** {lo que queda cerrado}
2. {respuesta} → **Pendiente:** {sigue abierto porque…}
```

## Manejo de situaciones
- **Respuesta vaga** ("como siempre", "lo normal"): se repregunta con un ejemplo concreto
  ("¿'lo normal' es que el supervisor apruebe y luego tesoreria gire, como en Factoring?").
- **Respuesta que contradice una fuente anterior:** se señala sin confrontar ("en la reunion
  se habia mencionado X; con esta respuesta entendemos que ahora es Y, ¿confirmas?") y
  prevalece la confirmacion mas reciente, dejando registro del cambio.
- **El cliente pide "lo mismo que tiene el competidor / que vi en otro sistema":** se pide
  describirlo en su propio proceso; lo externo es referencia, no requerimiento.
- **El cliente propone la solucion tecnica** ("agreguen una columna en la tabla"): se agradece
  y se reconduce al problema de negocio ("¿que necesitan ver y para que?"); el como lo decide
  desarrollo.
- **Silencio del cliente:** tras un recordatorio por mesa, la solicitud queda "esperando
  respuesta" con lo pendiente visible; no se cierra a medias.
- **Pedido fuera de alcance del producto o inviable segun el brain:** se documenta igual y se
  escala al lider de mesa con el fundamento; la Mesa no rechaza sola.
