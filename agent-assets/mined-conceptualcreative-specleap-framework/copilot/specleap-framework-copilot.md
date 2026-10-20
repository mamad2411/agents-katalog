# GitHub Copilot Instructions — DevFlow Pro SDD

## Metodología: Spec-Driven Development

> **Primero la especificación, luego el código. Nunca al revés.**

### Flujo de Trabajo
1. Crear spec antes de codificar (`openspec/specs/`)
2. Crear propuesta de cambio (`openspec/changes/`)
3. Implementar según spec
4. Tests obligatorios con Testing Report
5. Code review obligatorio
6. Merge solo con aprobación

### Estructura del Proyecto
```
openspec/
├── specs/           # Especificaciones (source of truth)
├── changes/         # Propuestas de cambios
└── templates/       # Plantillas
```

### Formato de Specs
- Usar GIVEN/WHEN/THEN para escenarios
- SHALL = obligatorio, SHOULD = recomendado, MAY = opcional
- Estados: draft → review → approved → implemented

### Código
- Variables/funciones en inglés
- Comentarios en español
- TypeScript strict mode
- Tests con 80%+ cobertura en lógica de negocio

### Commits
```
tipo(alcance): descripción en español

## Qué se hizo
## Por qué
## Refs: Asana/Spec
```

Tipos: feat, fix, refactor, docs, test, chore, style, perf

### Testing Report (OBLIGATORIO)
Cada feature debe documentar:
- Tests ejecutados y resultados
- Cobertura por módulo
- Status de code review

### Reglas
1. Sin spec no hay código
2. Sin tests no hay merge
3. Sin review no hay deploy
