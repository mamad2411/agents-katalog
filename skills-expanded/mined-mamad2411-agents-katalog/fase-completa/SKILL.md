---
name: fase-completa
description: Ejecuta el ciclo completo de una fase: build → quality gates → docs → commit → release.
---

# Skill: Fase Completa

Ejecuta una fase del proyecto de principio a fin de forma autónoma.

## Instrucciones para el Agente:

### 1. Pre-ejecución
- Leer `MASTER_PLAN.md` para obtener las tareas de la fase
- Verificar que no hay cambios pendientes (`git status`)

### 2. Ejecución de Tareas
- Ejecutar cada tarea de la fase en orden
- Si una falla: intentar corrección una vez
- Si sigue fallando: reportar y detenerse

### 3. Quality Gates (obligatorio al final)
```bash
pnpm typecheck      # 0 errores
pnpm test:unit      # todos passing
pnpm test:e2e       # todos passing
```

### 4. Documentación
- Actualizar `docs/AI_LOG.md` con entrada de la fase:
  - Fecha y hora
  - Modelo utilizado
  - Archivos creados/modificados
  - Errores corregidos
  - Tests ejecutados

### 5. Git
```bash
git add -A
git commit -m "feat(fase-X): descripción de la fase"
git push origin main
```

### 6. Release (opcional)
- Si todos los tests pasan: `gh release create vX.Y.Z --title "Fase X: nombre" --notes-file CHANGELOG.md`
- Si hay tests fallando: `gh release create vX.Y.Z --prerelease --title "Fase X: nombre (prerelease)" --notes-file CHANGELOG.md`

### 7. Reporte
- Devolver resumen: tareas completadas, tests, release creado
