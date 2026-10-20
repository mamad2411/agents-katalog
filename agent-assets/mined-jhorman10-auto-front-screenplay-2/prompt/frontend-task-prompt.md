---
name: frontend-task
description: Implementa una funcionalidad en el frontend React/Vite basada en una spec ASDD aprobada.
argument-hint: "<nombre-feature> (debe existir .github/specs/<nombre-feature>.spec.md)"
agent: Frontend Developer
tools:
  - edit/createFile
  - edit/editFiles
  - read/readFile
  - search/listDirectory
  - search
  - execute/runInTerminal
---

Implementa el frontend para el feature especificado, siguiendo la spec aprobada.

**Feature**: ${input:featureName:nombre del feature en kebab-case}

## Pasos obligatorios:

1. **Lee la spec** en `.github/specs/${input:featureName:nombre-feature}.spec.md` — si no existe, detente e informa al usuario.
2. **Revisa el código existente** en `frontend/src/` para entender patrones actuales.
3. **Implementa en orden**:
   - `frontend/src/services/` — servicio con llamadas a API (si aplica)
   - `frontend/src/hooks/` — hook custom (si hay estado complejo)
   - `frontend/src/components/` — componentes reutilizables
   - `frontend/src/pages/` — página + CSS Module
4. **Registra la ruta** en `frontend/src/App.jsx`.
5. **Verifica** el build: `cd frontend && npm run build`

## Restricciones:
- USAR CSS Modules exclusivamente — sin frameworks CSS globales.
- El estado de autenticación SIEMPRE viene de `useAuth` hook.
- Las variables de entorno deben usar prefijo `VITE_`.
- Firebase tokens se obtienen del usuario actual y se envían como `Bearer` en el header de Authorization.
