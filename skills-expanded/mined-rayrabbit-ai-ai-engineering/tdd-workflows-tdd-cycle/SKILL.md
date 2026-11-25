---
name: tdd-workflows-tdd-cycle
description: Strict execution of the TDD cycle Phases 1 to 6 with RED-GREEN-REFACTOR gates.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: rayrabbit-ai
  version: "1.0"
  generatedBy: "1.6.0"
---

## Instrucciones de Ejecución TDD

Ejecuta un ciclo riguroso de Test-Driven Development aplicando las 15 Invariantes del repositorio:

### Umbrales de Cobertura
- Cobertura mínima de líneas: 80%
- Cobertura mínima de ramas: 75%
- Cobertura de rutas críticas: 100%

### Triggers de Refactorización
- Complejidad ciclomática > 10
- Longitud de función/método > 20 líneas
- Longitud de clase > 200 líneas
- Duplicación de bloques de código > 3 líneas

### Fases del Ciclo
1. **Fase 1: Especificación y Diseño del Test**: Define escenarios Given/When/Then, casos límite y matriz de errores.
2. **Fase 2: RED (Test que falla)**:
   - Escribe el test unitario antes de implementar código de producción.
   - Ejecuta en terminal: demuestra que falla por falta de implementación (no por errores de sintaxis).
   - Commit: `test(red): <descripción>`.
   - **COMPUERTA**: STOP y reporte al operador.
3. **Fase 3: GREEN (Implementación mínima)**:
   - Implementa ÚNICAMENTE el código necesario para pasar el test en rojo.
   - Ejecuta la suite completa: verifica que pasa y valida la suite `@legacy_baseline`.
   - Verifica reporte de cobertura.
   - Commit: `feat(green): <descripción>`.
   - **COMPUERTA**: STOP y reporte al operador.
4. **Fase 4: REFACTOR (Calidad y limpieza)**:
   - Reduce complejidad, elimina duplicaciones y aplica principios SOLID.
   - Mantén la suite verde tras cada modificación.
   - Commit: `refactor: <descripción>`.
5. **Fase 5: INTEGRATION (Pruebas de Interfaz)**:
   - Diseña tests de integración que modelen la interacción entre módulos (fail-first).
   - Implementa integración mínima hasta verde.
   - Commit: `test(integration): <descripción>`.
6. **Fase 6: HARDENING (Casos límite y revisión final)**:
   - Añade pruebas de stress, boundary y error recovery.
   - Commit: `chore(hardening): <descripción>`.
