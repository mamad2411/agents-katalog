# Cursor Rules — DevFlow Pro SDD

## Metodología: Spec-Driven Development
Primero la especificación, luego el código. Nunca al revés.

## Estructura
- `openspec/specs/` — Especificaciones (source of truth)
- `openspec/changes/` — Propuestas de cambios
- `openspec/templates/` — Plantillas

## Flujo de Trabajo
1. Crear/actualizar spec antes de codificar
2. Crear propuesta en `openspec/changes/CHANGE-XXXX-nombre/`
3. Implementar según spec
4. Escribir tests con Testing Report
5. Code review obligatorio
6. Merge con aprobación

## Formato de Specs
- Escenarios: GIVEN/WHEN/THEN
- Requisitos: SHALL (obligatorio), SHOULD (recomendado), MAY (opcional)
- Estados: draft → review → approved → implemented

## Código
- Idioma código: inglés
- Idioma comentarios: español
- TypeScript strict mode
- Cobertura mínima: 80% lógica de negocio

## Commits
Formato: `tipo(alcance): descripción en español`
Tipos: feat, fix, refactor, docs, test, chore, style, perf
Incluir: refs a Asana y Spec

## Testing Report (OBLIGATORIO)
Cada feature documenta:
- Resultados de tests (unit, integration, e2e)
- Cobertura por módulo
- Status de code review

## Reglas de Oro
1. Sin spec no hay código
2. Sin tests no hay merge
3. Sin review no hay deploy
