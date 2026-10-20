---
name: backend-task
description: Implementa una funcionalidad en el backend FastAPI basada en una spec ASDD aprobada.
argument-hint: "<nombre-feature> (debe existir .github/specs/<nombre-feature>.spec.md)"
agent: Backend Developer
tools:
  - edit/createFile
  - edit/editFiles
  - read/readFile
  - search/listDirectory
  - search
  - execute/runInTerminal
---

Implementa el backend para el feature especificado, siguiendo la spec aprobada.

**Feature**: ${input:featureName:nombre del feature en kebab-case}

## Pasos obligatorios:

1. **Lee la spec** en `.github/specs/${input:featureName:nombre-feature}.spec.md` — si no existe, detente e informa al usuario.
2. **Revisa el código existente** en `backend/app/` para entender patrones actuales.
3. **Implementa en orden**:
   - `backend/app/models/` — modelo Pydantic
   - `backend/app/repositories/` — repositorio con Motor
   - `backend/app/services/` — servicio con lógica de negocio
   - `backend/app/routes/` — router FastAPI
4. **Registra el router** en `backend/app/main.py`.
5. **Verifica sintaxis** ejecutando: `cd backend && poetry run python -m py_compile app/main.py`

## Restricciones:
- Sigue el patrón de wiring: `db = get_db()` → `repo = XRepository(db)` → `service = XService(repo)` en el router.
- NO inyectar `get_db()` en servicios.
- Todas las operaciones de DB deben ser `async`/`await`.
