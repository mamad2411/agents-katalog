---
name: refactoring-safely
description: Refactorizar sin cambiar comportamiento y sin romper — red de tests de caracterización primero, pasos pequeños y reversibles, nunca mezclar un cambio de comportamiento con un refactor, strangler fig para reescrituras grandes, medir antes y después, y commits separados. Usar al limpiar código heredado, al extraer o renombrar un símbolo, función o módulo en código, al pagar deuda técnica, al preparar un módulo para una feature nueva, o cuando sentís que "primero habría que ordenar esto".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Refactorizar con red

Refactorizar es **cambiar la estructura sin cambiar el comportamiento observable**. Si el
comportamiento cambia, no es refactor: es una feature o un fix, y va por otro carril. La regla de
oro: en cualquier momento del proceso el sistema sigue verde. Nunca "roto a medias mientras ordeno".

## 1. Red de seguridad primero

Antes de tocar una línea, asegurate de poder detectar si rompés algo.

- ¿Hay tests que cubren el comportamiento actual? Corrélos y vé que pasen (ese es tu baseline).
- Si no hay, escribí **tests de caracterización**: capturan lo que el código hace HOY (aunque sea
  raro), no lo que debería hacer. Su objetivo es congelar el comportamiento durante el refactor.
- Para código difícil de testear, caracterizá por el borde observable (respuesta de API, salida
  de función pura) antes de meterte adentro.
- Sin ninguna red, no refactorices a ciegas: primero conseguí observabilidad (`verify`,
  `evidence-and-verification`), aunque sea un smoke manual reproducible.

```
# ❌ refactor sin red: "lo probé mentalmente, debería andar"
# ✅ refactor con red:
yarn test path/al/modulo   # verde ANTES
# ...refactor en pasos...
yarn test path/al/modulo   # verde DESPUÉS, misma salida
```

## 2. Un cambio de comportamiento nunca junto a un refactor

Este es el error que más caro sale. Si mezclás, cuando algo falla no sabés si fue el refactor o el
cambio, y la revisión se vuelve imposible.

- Refactor y cambio de comportamiento van en **commits distintos**, idealmente en **PRs distintos**.
- Secuencia sana: (1) refactorizá con tests en verde → merge; (2) sobre lo limpio, hacé el cambio
  de comportamiento con su propio test.
- Ver `scope-discipline`: si estás "aprovechando" para cambiar algo más, frená.

## 3. Pasos pequeños y reversibles

- Un refactor grande es una secuencia de micro-pasos, cada uno con los tests en verde: extraer
  función, renombrar, mover, introducir parámetro, reemplazar condicional por polimorfismo.
- Después de cada paso: corré los tests. Si se pusieron rojos, el último paso fue el culpable —
  revertilo, es un solo paso.
- Preferí las transformaciones que la herramienta hace por vos (rename/extract del IDE, o
  codemods) sobre editar a mano: son mecánicas y difíciles de romper.
- Commiteá seguido. Cada commit deja el sistema verde, así cualquier punto es reversible.

## 4. Strangler fig para lo grande

No reescribas un módulo grande de un saque. Rodealo y reemplazalo por dentro:

1. Poné una fachada/interfaz delante de lo viejo.
2. Redirigí el tráfico a través de la fachada (sin cambiar comportamiento todavía).
3. Implementá la versión nueva detrás de la fachada, ruta por ruta o caso por caso.
4. Migrá el tráfico gradualmente; el viejo y el nuevo conviven mientras dure.
5. Cuando nada usa el viejo, borralo.

Cada paso es mergeable y reversible. Nunca hay una ventana de "todo reescrito pero nada probado".

## 5. Medir antes y después

- Si el refactor busca performance, tenés que **medir**, no suponer (`code-efficiency`,
  `performance-load-testing`). Un "quedó más limpio" no justifica una regresión de latencia.
- Si busca claridad/mantenibilidad, la métrica es cualitativa pero honesta: ¿bajó la complejidad,
  la duplicación, los usos? (`code-complexity-metrics`, `dead-code-duplication`).
- El comportamiento observable **no debe cambiar**: misma salida, mismos errores, mismos contratos.

## 6. Cuándo NO refactorizar

- No refactorices código que vas a borrar pronto.
- No refactorices sin red solo porque "es obvio".
- No refactorices fuera del alcance de tu tarea "de paso" (anotá la deuda en
  `technical-debt-management` y seguí).
- No refactorices en el mismo PR en que arreglás un bug urgente: primero el fix con su test.

## Anti-patrones

- "Refactor" que en realidad cambia comportamiento y nadie lo nota hasta producción.
- Reescritura big-bang de un módulo entero sin pasos intermedios verdes.
- Borrar los tests viejos "porque estorban" en vez de mantenerlos como red.
- Commit gigante "refactor varios" imposible de revisar o revertir.
- Optimizar sin medir y llamarlo mejora.

## Checklist

- [ ] Tengo red: tests que pasan y cubren el comportamiento actual (o de caracterización).
- [ ] El comportamiento observable no cambia (misma salida, errores y contratos).
- [ ] Ningún cambio de comportamiento va mezclado con el refactor.
- [ ] Avancé en pasos chicos; corrí los tests después de cada uno.
- [ ] Lo grande fue por strangler fig, no big-bang.
- [ ] Si era por performance, medí antes y después.
- [ ] Commits separados y reversibles; cada uno deja el sistema verde.

## Evidencia / DoD

Pegá la salida de los tests **verde antes** y **verde después** del refactor, mostrando que la
suite es la misma. Si fue por performance, pegá la medición antes/después. Un refactor sin
baseline verde reproducible es `WRITTEN`, no verificado (`evidence-and-verification`). Enlaza con
`technical-debt-management` (qué deuda pagaste) y `scope-discipline` (que no te fuiste de tema).
