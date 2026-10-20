---
name: evidence-and-verification
description: Gate de verificación por observación en runtime y escalera de afirmaciones (UNKNOWN → DISCOVERED → WRITTEN → RUNS → TESTED → VERIFIED → REGRESSION_VERIFIED). Usar SIEMPRE antes de decir "listo", "funciona", "arreglado", "implementado" o "probado"; al cerrar un slice, un carril o un bug; y al redactar cualquier reporte de estado. Exige salida literal pegada, veredicto PASS/FAIL/BLOCKED/SKIP y la sección "No cubierto". Leer código o compilar nunca cuenta como verificación.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Evidencia y verificación

Verificar es **observar el artefacto real ejecutándose** y ver con tus propios ojos el
comportamiento que cambiaste. Leer el diff no es verificar. Compilar no es verificar.
"Debería funcionar" es FAIL. Ninguna palabra de cierre puede ser más fuerte que la
evidencia que tenés pegada.

## Cuándo aplica

- Antes de cualquier afirmación de estado: en el chat, en un commit, en un PR, en un reporte.
- Al terminar cada slice (ver `vertical-slicing`), no al final de veinte cambios acumulados.
- Al cerrar un bug: el fix no existe hasta que la reproducción original pasa (ver `root-cause-debugging`).

## 1. La escalera de afirmaciones

Cada peldaño habilita un vocabulario y prohíbe el resto. Registrá el peldaño actual en el
reporte de evidencia del carril (dónde vive ese reporte: definilo en el CLAUDE.md del proyecto).

| Peldaño | Significa | Evidencia exigida | Podés decir | Prohibido decir |
|---|---|---|---|---|
| 0 `UNKNOWN` | No hay evidencia suficiente | — | "sin verificar", "pendiente de discovery" | implementado, funciona, corregido |
| 1 `DISCOVERED` | Localizaste las piezas reales | Rutas de archivo, endpoints, modelos, tests existentes | "encontré X en `ruta:línea`" | que algo cambió |
| 2 `WRITTEN` | El cambio existe en disco | Diff real, archivos guardados | "código escrito", "cambio aplicado al archivo" | compila, funciona |
| 3 `RUNS` | La capa tocada compila/arranca | Typecheck/build/arranque con exit code 0 pegado | "compila", "arranca" | cumple el requisito, funciona |
| 4 `TESTED` | Tests dirigidos pasan | Salida del runner con los tests relevantes en verde | "los tests dirigidos pasan" | flujo de usuario verificado |
| 5 `VERIFIED` | Comportamiento observado en runtime | E2E o ejercicio manual del camino real + persistencia real + consola/red revisadas | "verificado: <qué>" | sin regresiones, listo para cerrar |
| 6 `REGRESSION_VERIFIED` | Verificado + regresión del módulo en verde + gates aplicables | Dirigido PASS, regresión PASS, gates de seguridad/a11y/responsive/visual que apliquen, reporte | "listo", "cerrado", "done" | — |

Reglas de la escalera:

1. **Solo se sube con evidencia nueva.** El esfuerzo invertido no es evidencia.
2. **No se saltan peldaños** cuando los intermedios aplican: de `WRITTEN` a `VERIFIED` sin `RUNS` es overclaim.
3. **Un fallo baja el peldaño.** Un test rojo después de `TESTED` te devuelve a `WRITTEN`.
4. **Un cambio posterior invalida** la verificación del área tocada: editaste después de `VERIFIED` → volvés a `WRITTEN` para esa área y re-ejecutás.
5. UI con cambio visual: `VERIFIED` exige además prueba visual (ver `visual-proof`); sin ella declarás `VERIFIED_FUNCTIONAL_ONLY`.
6. "Listo/done/cerrado" solo existe en el peldaño 6. Por debajo, nombrá el peldaño real.

Equivalencias falsas que nunca se usan: escrito ≠ compila · compila ≠ funciona · unit test pasa ≠ el
flujo funciona · E2E dirigido pasa ≠ sin regresiones · responde 200 ≠ semántica, persistencia ni UI
correctas · lint limpio ≠ comportamiento correcto · "no vi errores" ≠ no hay errores.

## 2. Qué cuenta como "ejercitado", por superficie

| Superficie | Ejercitar significa | No alcanza con |
|---|---|---|
| API | Request real contra el servicio corriendo, con auth real; status + cuerpo + efecto en la base | Test unitario con el ORM mockeado |
| Base de datos | Query de conteo/estado antes y después; constraint probado con un insert que debe fallar | Leer el DDL |
| Web | Navegador real sobre la ruta, acción del usuario, recarga para confirmar persistencia, consola y red sin errores inesperados | Que el componente compile |
| Mobile | App corriendo en emulador/dispositivo sobre la pantalla tocada | `analyze` limpio |
| Generador / script | Ejecutarlo y diffear su salida; re-ejecutarlo para probar idempotencia | Leer el script |
| Job / evento / notificación | Dispararlo y observar el efecto y el reintento sin duplicado | Log de "encolado" |
| Documentación ejecutable (OpenAPI, ejemplos) | Validador/linter + un request que coincida con el contrato | Revisión visual |

Si el cambio toca persistencia, la evidencia mínima incluye una lectura directa del dato persistido.

## 3. Veredictos

| Veredicto | Cuándo | Qué se exige |
|---|---|---|
| **PASS** | Ejercitaste el camino cambiado y la salida coincide con lo esperado | Comando + salida literal + qué demuestra |
| **FAIL** | Lo ejercitaste y no coincide | Comando + salida + expected/actual + hipótesis de causa |
| **BLOCKED** | No pudiste ejercitarlo (stack caído, superficie que todavía no existe, dependencia externa rota) | Qué bloqueó, qué intentaste, qué lo desbloquea |
| **SKIP** | El cambio no tiene superficie observable (comentarios, docs sin build) | Por qué no hay nada que observar |

**BLOCKED es un veredicto honesto y correcto.** La falla no es estar bloqueado: la falla es
convertir BLOCKED en PASS "porque compila". FAIL tampoco se suaviza como "casi listo".

Formato obligatorio del reporte:

```text
VEREDICTO:   PASS | FAIL | BLOCKED | SKIP
Peldaño:     <peldaño alcanzado de la escalera>
Superficie:  API · BD · Web · Mobile · Generador · Job · Docs
Comando:     <literal, copiable>
Salida:      <literal, recortada>
Demuestra:   <una frase>
No cubierto: <lo que quedó sin ejercitar — nunca vacío sin justificar>
```

"No cubierto" es obligatorio: es lo que impide que un PASS parcial se lea como total. Si de verdad
cubriste todo, escribí qué revisaste para afirmarlo.

## 4. Salida literal

1. Pegá el comando exacto y su salida real. Recortar con `[...]` sí; parafrasear, nunca.
2. Incluí el exit code o la línea de resumen del runner (tests pasados/fallados/omitidos).
3. Mirá los **omitidos**: una suite con tests salteados no es un verde completo; declaralo.
4. La salida tiene que ser de **después** del último edit. Salida vieja = evidencia vencida.
5. Nunca escribas de memoria lo que "salió": si no lo podés pegar, no lo corriste.

❌ "Corrí los tests y pasan todos."

✅
```text
$ yarn test src/appointments
Tests: 42 passed, 42 total — exit 0
Demuestra: la regla de solapamiento rechaza el turno duplicado.
No cubierto: concurrencia real contra la base (los tests mockean el ORM).
```

## 5. Kill-test y evidencia negativa

- **Kill-test**: si existe una prueba barata que podría demostrar que estás equivocado, corréla
  antes de entregar — recarga de página, request directo, query a la base, grep adicional, re-ejecución
  del test, inspección del DOM. Definila al arrancar (ver `outcome-first`).
- **Evidencia negativa**: "no encontré X" solo vale si declarás dónde buscaste (patrones, rutas, repos).
  Ausencia de búsqueda no es evidencia de ausencia.

## Anti-patrones

- Declarar full-stack cuando solo existe la UI, o solo el endpoint.
- Mockear el backend en un E2E y llamar a eso integración verificada.
- Verificar el camino feliz y callar que no se probó ningún borde.
- Reportar esfuerzo ("revisé a fondo") en lugar de resultado.
- Correr la verificación, editar "un detalle" y no volver a correrla.
- Bajar el listón del test para que dé verde (ver `rationalization-guard`).

## Evidencia / DoD

Para afirmar "listo" tiene que estar pegado, con fecha posterior al último edit:

1. Reporte en el formato de §3 con veredicto PASS y peldaño `REGRESSION_VERIFIED`.
2. Salida literal del test dirigido y de la regresión del módulo.
3. Lectura del dato persistido cuando hay persistencia.
4. Resultado de cada gate aplicable (`security-guardrails`, `frontend-accessibility`, `visual-proof`).
5. "No cubierto" completo y riesgos residuales.

## Checklist

- [ ] ¿El peldaño que declaro coincide con la evidencia que tengo pegada?
- [ ] ¿Ejercité el artefacto real, en la superficie que cambié?
- [ ] ¿La salida es literal y posterior al último edit?
- [ ] ¿Miré omitidos, consola y respuestas 4xx/5xx inesperadas?
- [ ] ¿Corrí el kill-test más barato?
- [ ] ¿Declaré "No cubierto"?
- [ ] ¿Usé BLOCKED en vez de inflar a PASS?
- [ ] ¿Ninguna palabra de mi reporte es más fuerte que mi peldaño?
