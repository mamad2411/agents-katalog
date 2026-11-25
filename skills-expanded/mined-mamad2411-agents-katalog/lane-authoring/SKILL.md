---
name: lane-authoring
description: Estándar de la casa para definir un carril — la unidad de trabajo full-stack que atraviesa dos o tres repos hermanos y se cierra con evidencia. Cubre su estructura documental (requisitos, criterios REQ-n, plan de implementación, plan de prueba, checklist de QA, contrato de resultado), el predecesor explícito, en qué repos vive y cómo se declara cerrado. Usar al abrir un carril nuevo, al recibir un pedido grande y no saber por dónde cortarlo en entregas cerrables de punta a punta, o al revisar si un carril está bien definido antes de arrancar el trabajo.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Autoría de carriles

Un **carril** es una porción de trabajo entregable de punta a punta: cruza los repos que
haga falta (API, web, mobile, modelo), se implementa en slices verticales y se cierra con
evidencia observable. No es una tarea suelta ni un ticket de una sola capa.

## Cuándo aplica

- Al abrir un carril nuevo a partir de un pedido, épica o backlog.
- Al partir algo grande en carriles independientes y ordenables.
- Antes de arrancar: si el carril no tiene resultado observable y criterios verificables,
  no está listo — volvé a `requirements-and-acceptance` y `outcome-first`.

## 1. Un carril = un resultado observable

- Enunciá el carril por lo que un actor podrá ver o hacer al terminar, no por los archivos
  que se tocan. "El doctor bloquea una franja de su agenda y deja de recibir solicitudes ahí",
  no "agregar endpoint de bloqueo".
- Tamaño: cerrable con evidencia en una tanda de trabajo acotada. Si necesita más de ~5 slices
  verticales, es dos carriles.
- **Predecesor explícito**: declará de qué carril depende y por qué. Sin dependencia, escribí
  "ninguno". No arranques un carril cuyo predecesor no está cerrado.

## 2. En qué repos vive

Declará al inicio los repos que toca y qué cambia en cada uno (contrato, backend, UI, modelo,
seeds). Eso fija el alcance de ramas y PRs — ver `git-workflow-multirepo`.

## 3. Estructura documental

Un carril se documenta con estos artefactos (un archivo por tema o secciones de uno solo):

| Artefacto | Contenido |
|---|---|
| `requirements` | Qué se pide, contexto, ambigüedades registradas (no resueltas por conveniencia) |
| Criterios `REQ-<carril>-<n>` | Cada requisito como criterio verificable dado-cuando-entonces |
| `implementation-plan` | Slices verticales en orden, archivos previstos por repo |
| `test-plan` | Qué se prueba en cada nivel y con qué datos (ver `test-plan-authoring`) |
| `qa-checklist` | Gates aplicables al alcance (seguridad, a11y, datos, visual) |
| `contrato de resultado` | Resultado observable + kill-test más barato que probaría que NO está hecho |

## 4. Criterios REQ-n

- Numerados y trazables: cada uno mapea a evidencia de cierre (test, respuesta de API, captura).
- Estado por criterio: `SATISFIED | PARTIAL | MISSING | AMBIGUOUS | BLOCKED`.
- No implementar un criterio `AMBIGUOUS` hasta intentar resolverlo por código/runtime o
  registrar la decisión — ver `anti-hallucination-guard`.

## 5. Ciclo de vida

`DEFINIR → DESCUBRIR → PLANIFICAR → IMPLEMENTAR → VALIDAR → QA → CORREGIR → CERRAR`.
El descubrimiento factual (`factual-discovery`) va antes de tocar código; el corte en slices
(`vertical-slicing`) antes de implementar; la evidencia (`evidence-and-verification`) antes de
declarar cerrado.

## 6. Cierre con evidencia

Un carril se cierra sólo cuando:

- Todos los criterios REQ están `SATISFIED` o el residual está documentado como riesgo aceptado.
- Los gates aplicables pasaron con evidencia pegada (no paráfrasis).
- Existe un reporte de cierre: criterios y resultado, archivos por repo, endpoints, tests,
  comandos con su salida literal, bugs hallados/corregidos, riesgos residuales, bloqueos.

No se cierra con QA en rojo, ni con un criterio "casi", ni con TODO en lugar de implementación.

## Plantilla mínima

```markdown
# Carril <id> — <resultado observable en una frase>
Predecesor: <id | ninguno>   Repos: <api, web, ...>
## Requisitos y ambigüedades
## Criterios
- REQ-<id>-1 (dado ... cuando ... entonces ...) — estado
## Plan de implementación (slices)
## Plan de prueba
## Checklist de QA (gates aplicables)
## Contrato de resultado (observable + kill-test)
```

## Checklist

- [ ] El carril está enunciado por su resultado observable, no por archivos.
- [ ] Predecesor declarado (o "ninguno") y cerrado si existe.
- [ ] Repos afectados y su cambio, declarados.
- [ ] Criterios REQ-n numerados, verificables y con estado.
- [ ] Ambigüedades registradas, no resueltas por conveniencia.
- [ ] Contrato de resultado con kill-test.
- [ ] Gates de QA aplicables al alcance, listados.
