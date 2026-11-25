---
name: qa-evidence-reporting
description: Cómo se reporta la evidencia de QA para poder cerrar un carril, feature o bug — qué pegar (comandos con su salida literal, traces, capturas por viewport, IDs de casos, veredictos PASS/FAIL/BLOCKED), plantilla de reporte y la regla de nunca parafrasear la salida. Usar al cerrar cualquier trabajo con QA, al escribir el reporte final de un carril, al adjuntar resultados a un PR o issue, o cuando alguien dice "ya lo probé" sin evidencia que lo respalde.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Reporte de evidencia de QA

Un resultado de QA sin evidencia pegada **no existe**. "Probé y anda" no es reporte. Esta skill fija
qué se adjunta para que otro pueda creer —y reproducir— el resultado. Es la cara de QA de
`evidence-and-verification` (la escalera de afirmaciones) y consume `visual-proof` para la parte visual.

## Regla de oro
La evidencia es la **salida literal** del comando o la herramienta, recortada pero nunca
parafraseada ni reescrita. Si no la pegaste, no la tenés.

## Qué pegar según el tipo
| Prueba | Evidencia mínima |
|---|---|
| Unit/integración | Comando + resumen de la corrida (suites/tests, pass/fail, tiempo) literal |
| API | Comando + status y cuerpo relevante de la respuesta; para negativos, el rechazo real |
| E2E Playwright | Comando + resultado; trace/screenshot en fallo; consola/red sin errores |
| Visual | Capturas por viewport (móvil/tablet/desktop) y tema claro/oscuro, inspeccionadas (`visual-proof`) |
| Performance | Percentiles vs umbral, no promedios (`performance-load-testing`) |
| Datos | Queries de verificación con conteos (`data-quality-validation`) |
| Seguridad | Tests negativos de autorización con su rechazo (`security-testing`) |

## Veredicto por caso
Cada caso/criterio cierra con uno de:
- **PASS** — se ejercitó el camino y la salida coincide con lo esperado.
- **FAIL** — se ejercitó y no coincide (adjuntar salida + hipótesis).
- **BLOCKED** — no se pudo ejercitar (qué lo bloqueó, qué se intentó, qué lo desbloquea).
- **SKIP** — sin superficie observable (por qué).
Compilar o leer el código NO es PASS.

## Plantilla de reporte
```md
# Reporte QA — <carril/feature/bug>
Versión: <commit SHA>   Entorno: <local/CI/staging>   Fecha: <YYYY-MM-DD>

## Cobertura (trazabilidad)
| REQ / Caso | Nivel | Veredicto |
|-----------|-------|-----------|
| REQ-1     | API   | PASS      |
| REQ-2     | E2E   | FAIL → #123 |

## Evidencia
### <caso>  — PASS
Comando:
```
<literal>
```
Salida:
```
<literal, recortada>
```
Demuestra: <una frase>

## No cubierto
<qué quedó sin ejercitar y por qué — obligatorio>

## Defectos abiertos
- #123 <título> — severidad <...>
```

## "No cubierto" es obligatorio
Todo reporte declara qué NO se probó. Es lo que impide que un PASS parcial se lea como total.
Un reporte sin "No cubierto" está incompleto.

## Anti-patrones
- Parafrasear la salida ("los tests pasaron") en vez de pegarla.
- Captura de pantalla de código en vez de la salida del comando.
- Declarar PASS sobre algo que solo compiló.
- Omitir el "No cubierto" para que parezca completo.
- Reporte sin versión ni entorno: irreproducible.

## Checklist
- [ ] Versión (SHA) y entorno indicados.
- [ ] Cada caso con veredicto PASS/FAIL/BLOCKED/SKIP.
- [ ] Salida literal pegada (no parafraseada) por cada afirmación.
- [ ] Traces/capturas adjuntas donde corresponde.
- [ ] Sección "No cubierto" presente.
- [ ] Defectos abiertos enlazados a su bug.

## Evidencia / DoD
Este reporte ES la evidencia de cierre. No se declara "probado" un carril sin él completo, con
al menos un caso PASS por criterio de aceptación y cero FAIL sin bug asociado.
