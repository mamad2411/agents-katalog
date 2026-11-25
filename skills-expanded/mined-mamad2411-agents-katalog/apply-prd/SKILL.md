---
name: apply-prd
description: Implementa un ticket o PRD de extremo a extremo, delegando exploración, implementación y revisión a subagentes, y cerrando con commit, push y PR.
---

# Apply PRD

Implementa el ticket o PRD indicado con el menor scope viable, respetando el codebase y dejando un PR verificable.

## Input

- Ticket o PRD: URL, ID de Linear, o texto pegado por el usuario.
- Commit message opcional.

## Reglas

- Actúa como orquestador: mantén bajo tu contexto delegando exploración, codificación y revisión a subagentes.
- Antes de decidir términos de dominio, lee `AGENTS.md`, `CONTEXT.md` y `docs/domain.md`.
- No expandas scope. Si detectas trabajo valioso fuera del ticket, anótalo como follow-up.
- Si hay ambigüedad, decide con esta prioridad:
  1. Convenciones del codebase.
  2. Opción más conservadora.
  3. Menor cantidad de archivos tocados.
  4. Opción más fácil de revertir.
- Pregunta solo si falta información que pueda cambiar comportamiento de negocio, implique datos destructivos, permisos externos o decisiones irreversibles.
- No ejecutes migraciones. Solo genera archivos de migración cuando aplique y documenta el comando manual.
- Para commit, push y PR, sigue la estructura de `commit-push-pr`.

## Subagentes

### Explorador

Debe devolver:

- Objetivo del ticket en una frase.
- Scope explícito: qué sí y qué no.
- Criterios de aceptación verificables.
- Mapa de impacto:
  - archivos a leer;
  - archivos a modificar;
  - archivos a crear;
  - archivos que no deben tocarse.
- Entidades de schema involucradas.
- Riesgos y dependencias.
- Convenciones detectadas.

### Implementador

Debe:

- Hacer cambios acotados al mapa de impacto.
- Respetar patrones existentes de naming, imports, errores, tipos y estructura.
- Crear o actualizar tests cuando haya lógica afectada.
- Reportar cualquier archivo tocado fuera del mapa como desviación.

### Revisor

Debe comparar el diff final contra:

- Criterios de aceptación.
- Scope del ticket.
- Convenciones del codebase.
- Riesgos detectados.
- Tests, lint y typecheck.
- Acciones manuales pendientes.

Debe devolver hallazgos bloqueantes y no bloqueantes.

## Workflow

1. **Extraer ticket**
   - Lee el ticket/PRD completo.
   - Extrae objetivo, scope, criterios de aceptación, supuestos y dudas críticas.
   - Si es un ticket de Linear, revisa descripción, comentarios relevantes y links adjuntos.

2. **Mapear codebase**
   - Lanza el subagente Explorador.
   - Revisa `AGENTS.md`, `CONTEXT.md` y `docs/domain.md`.
   - Lee documentación local de módulos afectados si existe.
   - Define el mapa de impacto antes de implementar.

3. **Planear**
   - Ordena cambios por menor blast radius.
   - Identifica migraciones, tests y validaciones necesarias.
   - Lista acciones manuales que quedarán pendientes para el usuario.

4. **Implementar**
   - Crea rama `feat/<slug>` o `fix/<slug>`.
   - Lanza el subagente Implementador con el mapa de impacto.
   - Mantén los cambios dentro del scope.
   - Si necesitas salir del mapa, documenta la desviación.

5. **Validar**
   - Corre tests relevantes, lint y typecheck.
   - Si fallan, depura hasta 3 intentos razonables.
   - Si algo queda fallando, documenta la limitación con evidencia.

6. **Revisar**
   - Lanza el subagente Revisor.
   - Corrige hallazgos bloqueantes.
   - Si queda un riesgo no bloqueante, anótalo en el PR.

7. **Commit, push y PR**
   - Usa la estructura de `commit-push-pr`.
   - Crea commit con Conventional Commits.
   - Abre PR con el template de `references/pr-template.md`.
   - Solo abre draft si hay bloqueo real: imposibilidad técnica, permisos faltantes, dependencia no instalable, credenciales externas o decisión crítica sin resolver.

## Output

Devuelve:

- URL del PR.
- Resumen de cambios.
- Validaciones ejecutadas.
- Acciones manuales pendientes, si existen.

El template del PR vive en `references/pr-template.md`.
