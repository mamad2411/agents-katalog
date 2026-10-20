---
name: outcome-first
description: Gate de arranque — antes de leer código obliga a definir el resultado observable (quién ve o puede hacer qué, dónde, desde qué estado), los criterios de aceptación verificables y el kill-test más barato que demostraría que NO está hecho; después se trabaja hacia atrás desde ahí. También fija la comunicación resultado-primero en checkpoints y entregas. Usar al recibir cualquier tarea, carril, slice o bug, antes de planificar o explorar, cuando se dio algo por terminado y nadie se pone de acuerdo en si está hecho, y al redactar un reporte de avance o de cierre.
effort: medium
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Resultado primero

Si no podés describir cómo se ve "hecho" antes de empezar, no vas a poder reconocerlo cuando
llegues, ni demostrarlo cuando lo afirmes. El resultado observable se define **antes** de abrir
el primer archivo: es lo que convierte la exploración en búsqueda dirigida y el cierre en una
comprobación, no en una opinión.

## Cuándo aplica

- Al recibir una tarea, antes de `factual-discovery` y de cualquier plan.
- Al abrir cada slice (ver `vertical-slicing`): un slice sin resultado observable propio está mal cortado.
- Al tomar un bug: el resultado es "el repro deja de fallar y el comportamiento correcto es Q".
- Al escribir cualquier checkpoint o entrega.

## 1. La ficha de resultado

Escribila en el reporte del carril antes de leer código. Una ficha por resultado; un carril suele tener varias.

```text
RESULTADO
Actor:          <rol concreto: paciente, médico, admin de la organización, job nocturno>
Dónde:          <ruta, pantalla, endpoint o superficie>
Estado inicial: <datos y permisos de partida>
Acción:         <lo que hace el actor>
Observable:     <lo que ve / recibe / puede hacer después>
Persistencia:   <qué queda guardado y cómo se comprueba: recarga, query, otro usuario>
Borde / error:  <al menos un caso que debe manejar y cómo se ve>
Fuera:          <lo que explícitamente NO incluye>
Peldaño:        UNKNOWN
```

El peldaño arranca en `UNKNOWN` y solo sube con evidencia (ver `evidence-and-verification`).

## 2. Criterios de aceptación verificables

Un criterio sirve si otra persona puede ejecutarlo y obtener **sí o no** sin preguntarte nada.

| Un buen criterio es | ❌ | ✅ |
|---|---|---|
| Observable desde afuera | "El servicio maneja bien los solapamientos" | "Crear un turno que pisa otro devuelve 409 y la agenda no cambia" |
| Binario | "La pantalla carga rápido" | "LCP ≤ umbral del proyecto medido en la ruta X" |
| Con datos concretos | "Valida el formulario" | "Enviar con el email vacío muestra el error asociado al campo y conserva el resto" |
| Centrado en el actor | "Se agrega la columna `status`" | "El médico ve la solicitud como *Rechazada* tras recargar" |
| Incluye permiso | "El usuario edita el registro" | "...y otro usuario del mismo tenant sin el rol recibe 403" |

Si un criterio no se deja escribir así, el requisito está incompleto o es ambiguo: registralo y
resolvelo (ver `requirements-and-acceptance` y `anti-hallucination-guard`), no lo rellenes con suposiciones.

Numerá los criterios (`REQ-<carril>-<n>`): son las filas contra las que después mapeás evidencia y diff.

## 3. El kill-test

El kill-test es **la prueba más barata que demostraría que NO está hecho**. Se define al arrancar,
cuando todavía no tenés cariño por tu solución, y se corre antes de entregar.

| Tipo de cambio | Kill-test típico |
|---|---|
| Mutación con persistencia | Recargar / volver a consultar: ¿el dato sigue ahí y es el correcto? |
| Autorización | Repetir el request como otro usuario u otro tenant: ¿sigue respondiendo? |
| Validación | Mandar el request directo salteando la UI: ¿el servidor lo rechaza? |
| Acción idempotente / con reintento | Ejecutarla dos veces: ¿duplicó el efecto? |
| Transición de estado | Intentar la transición desde un estado inválido |
| Listado / búsqueda | Cero resultados, un resultado, y más de una página |
| UI | Viewport angosto, tema oscuro, navegación solo con teclado |
| Fix de bug | El repro original, exactamente como se reportó |
| Generador / seed | Correrlo dos veces: ¿la segunda corrida cambia algo? |

Buen kill-test: barato (minutos), independiente de tu implementación, y con un resultado que no
admite interpretación. Si pasa, no probaste que está bien; probaste que no está mal *de esa forma*.
Por eso se declara "No cubierto".

## 4. Trabajar hacia atrás

Desde el observable hacia el código, no al revés:

```text
Observable → superficie que lo muestra → contrato que la alimenta → regla que lo decide → dato que lo sostiene
```

1. Ubicá la **superficie** real donde debe verse el resultado (ruta, componente, endpoint).
2. Seguí hacia atrás solo por lo que ese resultado necesita. Lo que no está en el camino no se lee (ver `context-thrift`).
3. En cada eslabón preguntá: ¿ya existe? ¿qué le falta para este resultado? Eso es tu lista de cambios.
4. El plan de slices sale de ahí: cada slice deja algo observable, aunque sea chico.
5. Si un eslabón no hace falta para el resultado, no se toca: no inventes capas (ver `scope-discipline`).

## 5. Comunicación resultado-primero

**Checkpoints** — empiezan por el hecho, no por la intención:
qué cambió · qué se comprobó · qué falló. Sin listas de herramientas usadas ni de lo que "vas a" hacer.

**Entrega** — la primera frase es el resultado real alcanzado **o** el bloqueo real. Después, en
orden: evidencia → cambios → no cubierto → riesgos.

❌ "Estuve revisando la arquitectura del módulo, analicé los servicios involucrados y realicé varios
ajustes orientados a mejorar el flujo de reservas..."

✅ "El médico ya puede bloquear un rango de agenda y el bloqueo persiste tras recargar
(`VERIFIED`, salida abajo). **No funciona todavía**: bloquear sobre un turno ya confirmado devuelve
500 en vez de 409."

Un resultado parcial se dice como parcial en la primera línea. Nunca se esconde detrás de una
narración de esfuerzo (ver `progress-reporting`).

## Anti-patrones

- Arrancar a leer código "para entender" sin saber qué resultado se busca.
- Definir el resultado en términos internos ("se agrega el servicio X") en lugar de observables.
- Criterios sin borde, sin permiso o sin persistencia: solo describen el camino feliz.
- Definir el kill-test al final, a medida de lo que sabés que pasa.
- Redefinir el resultado durante el trabajo para que coincida con lo que quedó hecho.
- Slices que no dejan nada observable ("primero toda la capa de datos").
- Abrir el reporte con proceso y dejar el fallo para el último párrafo.

## Evidencia / DoD

Para cerrar, el reporte contiene:

1. La ficha de resultado escrita **al inicio** (si cambió en el camino, el cambio y quién lo aprobó).
2. Criterios numerados, cada uno con su veredicto y su evidencia literal.
3. El kill-test definido al inicio, el comando con que se corrió y su salida.
4. Primera línea de la entrega = resultado real o bloqueo real.
5. Criterios no cumplidos o no verificados, listados explícitamente.

## Checklist

- [ ] ¿Escribí la ficha de resultado antes de abrir código?
- [ ] ¿El resultado está dicho desde el actor, no desde la implementación?
- [ ] ¿Cada criterio es observable, binario y con datos concretos?
- [ ] ¿Hay al menos un criterio de borde/error, uno de permiso y uno de persistencia cuando aplican?
- [ ] ¿Definí el kill-test al arrancar y lo corrí antes de entregar?
- [ ] ¿Leí solo lo que está en el camino hacia el resultado?
- [ ] ¿Cada slice deja algo observable?
- [ ] ¿Mi entrega abre con el resultado real o el bloqueo real?
