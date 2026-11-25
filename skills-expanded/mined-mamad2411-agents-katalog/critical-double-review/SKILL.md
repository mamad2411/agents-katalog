---
name: critical-double-review
description: Gate OBLIGATORIO de doble revisión ultra crítica de lo entregado — toda captura de Playwright se inspecciona DOS veces (una pasada de verificación y una segunda pasada adversarial que busca activamente por qué la entrega NO sirve), con veredicto escrito por captura, calificación de calidad sin indulgencia y re-captura tras cada corrección. Usar SIEMPRE después de tomar capturas de Playwright, antes de declarar verificada cualquier pantalla, antes de abrir o actualizar un PR con cambios de UI, y antes de cerrar el turno. No tiene excepción por tamaño ni por apuro.
effort: high
---

# Doble revisión ultra crítica

`visual-proof` exige tomar las capturas y mirarlas. Esta skill exige algo más duro: **mirarlas
dos veces, y la segunda vez como el revisor más exigente que va a recibir el trabajo**. La primera
mirada confirma lo que esperabas ver; por eso no alcanza. Quien hizo el cambio mira la captura
buscando que esté bien, y el ojo encuentra lo que busca. La segunda pasada existe para romper ese
sesgo: se busca que esté mal.

> ## ⛔ No negociable (regla 35)
> Ninguna entrega con superficie visual se declara verificada, ningún PR con UI se entrega y
> ningún turno se cierra **sin las dos pasadas escritas en la evidencia**. Una sola pasada es
> `VERIFIED_FUNCTIONAL_ONLY` como máximo, por más capturas que haya.

## 1. Cuándo aplica

Siempre que exista al menos una captura de Playwright en el trabajo: prueba visual, E2E con
screenshot, trace de fallo, captura para el PR o para un reporte. Si el cambio tocó UI y **no**
hay capturas, primero se toman según `visual-proof` §3–§4; esta skill no reemplaza esa matriz.

## 2. Primera pasada — verificación

Objetivo: confirmar que cada celda de la matriz muestra lo que el requisito pide.

1. Abrí **cada** captura como imagen (leerla, no listarla). Una captura no abierta no existe.
2. Recorré la lista de `visual-proof` §5 completa por captura.
3. Contrastá contra el **criterio de aceptación** literal, no contra tu recuerdo de lo que hiciste.
4. Anotá una línea por captura: `P1 — <archivo> — OK | DEFECTO: <qué, dónde>`.

## 3. Segunda pasada — adversarial y ultra crítica

Se hace **después** de cerrar la primera y, si hubo correcciones, sobre las **re-capturas**.
Postura obligatoria: *"soy el cliente, el revisor del PR y el usuario con el celular más chico;
mi trabajo es rechazar esto"*. Se parte de la hipótesis de que la entrega **tiene** defectos.

Para cada captura, respondé por escrito estas preguntas. "No aplica" exige decir por qué.

| # | Pregunta | Qué suele esconder |
|---|---|---|
| 1 | ¿Qué es lo **primero** que un usuario vería mal acá? | El defecto obvio que la primera pasada normalizó |
| 2 | ¿Hay algún píxel de texto cortado, solapado, desalineado o pegado al borde? | Recortes a 360 px, truncados sin tooltip |
| 3 | ¿Esto se ve **terminado** o se ve como un prototipo? | Espaciado inconsistente, alineaciones "casi", tipografía mezclada |
| 4 | ¿Es coherente con las pantallas vecinas del producto? | Componentes nuevos que no usan los tokens ni el patrón existente |
| 5 | En tema oscuro, ¿hay algo que desaparece, encandila o pierde contraste? | Fondos o bordes hardcodeados |
| 6 | ¿El estado vacío, de error y de carga orienta, o está mudo? | Vacío sin acción, error crudo del backend |
| 7 | ¿La jerarquía guía la vista a la acción principal? | Dos botones primarios, acción clave enterrada |
| 8 | ¿Algún dato se ve inventado, real o sensible? | PHI en capturas, datos ficticios presentados como reales |
| 9 | ¿La captura muestra **lo que pide el requisito** o algo parecido? | Semántica cambiada por conveniencia |
| 10 | Si tuviera que rechazar este PR, ¿por qué lo rechazaría? | La respuesta honesta a esta es la más valiosa |

Cada pregunta con un hallazgo se convierte en defecto con severidad:

| Severidad | Criterio | Efecto |
|---|---|---|
| `BLOQUEANTE` | Rompe el requisito, oculta información, ilegible, PHI expuesta, roto en un viewport o tema | La entrega no sale. Corregir y repetir ambas pasadas en esa celda |
| `MAYOR` | Se nota a simple vista, incoherente con el producto, estado mal resuelto | Corregir antes de entregar |
| `MENOR` | Detalle fino (1–2 px, matiz) | Corregir si está en alcance; si no, registrar en el reporte |

## 4. Calificación de la entrega

Al terminar la segunda pasada, emitís una calificación por pantalla, sin indulgencia:

| Nota | Significa |
|---|---|
| `RECHAZADA` | Hay al menos un `BLOQUEANTE` o un `MAYOR` sin corregir |
| `ACEPTABLE CON RESERVAS` | Solo quedan `MENOR` registrados, con motivo de por qué no se corrigieron |
| `APROBADA` | Ambas pasadas sin hallazgos abiertos sobre las capturas finales |

Reglas de la nota:

1. **La nota la baja cualquier hallazgo abierto**; no la sube el esfuerzo invertido.
2. "Se ve bien" no es una nota. Una `APROBADA` sin la tabla de la §3 respondida es inválida.
3. Si dudás entre dos notas, **va la más baja**.
4. Una entrega `RECHAZADA` no se entrega, no se sube al PR como terminada y no se reporta como
   `HECHO`: se corrige o queda `A MEDIAS` con el defecto descripto.

## 5. Corrección y re-captura

Defecto → corrección (`archivo:línea`) → **re-captura de la misma celda** → **las dos pasadas otra
vez sobre la re-captura**. La evidencia vieja no prueba código nuevo (regla 30). Una corrección
de CSS puede romper otro viewport: re-capturá también las celdas vecinas del mismo componente.

## 6. Qué no es una segunda pasada

- ❌ Volver a mirar la misma imagen dos segundos después con la misma lista.
- ❌ Hacerla antes de cerrar la primera, mezclando ambas.
- ❌ Hacerla sobre capturas viejas después de haber corregido.
- ❌ Responder las diez preguntas con "OK" en bloque.
- ❌ Delegarla al mismo subagente que implementó el cambio (regla 70.4.8). Si se delega, que sea a
  un revisor independiente con este contrato, y el agente principal igual lee su resultado.

## Evidencia / DoD

En `evidencia/` (y enlazado desde el `REPORTE.md`), un archivo `doble-revision.md` con:

- [ ] Tabla de capturas: viewport (px) × tema × estado → ruta.
- [ ] **Pasada 1**: una línea por captura (`OK` o defecto).
- [ ] **Pasada 2**: las diez preguntas de §3 respondidas por captura (o agrupadas por pantalla
      cuando las celdas son idénticas en contenido, declarándolo).
- [ ] Defectos con severidad → corrección `archivo:línea` → ruta de la re-captura → resultado de
      las dos pasadas sobre la re-captura.
- [ ] Nota final por pantalla (`RECHAZADA` / `ACEPTABLE CON RESERVAS` / `APROBADA`).
- [ ] *No cubierto*: celdas no capturadas y por qué.

Sin este archivo, el peldaño visual máximo es `VERIFIED_FUNCTIONAL_ONLY`, y se dice así.

## Checklist

- [ ] Abrí cada captura como imagen en la pasada 1.
- [ ] Cerré la pasada 1 antes de empezar la 2.
- [ ] Pasada 2 con postura de rechazo y las diez preguntas respondidas.
- [ ] Cada hallazgo con severidad.
- [ ] Correcciones re-capturadas y re-revisadas en ambas pasadas.
- [ ] Nota por pantalla, la más baja ante la duda.
- [ ] Ninguna pantalla `RECHAZADA` entregada como terminada.
- [ ] Sin datos reales de personas en las imágenes (`data-privacy-phi`).

Relacionadas: `visual-proof` (matriz y captura) · `ui-quality-review` (criterios de calidad) ·
`frontend-beautiful-ui` · `evidence-and-verification` · `pr-mergeable-gate` (la entrega del PR).
