# AGENTS.md — Convenciones generales del repo

Estas convenciones aplican a todo el repositorio. Para reglas específicas de la app (Tauri/Vite/TS/CSS), ver `markdown-viewer/AGENTS.md`.

## Principios

- Priorizar **robustez**, **performance** y **accesibilidad (WCAG 2.1 AA)** en cambios de UI.
- Mantener cambios **pequeños y verificables**; evitar refactors masivos sin necesidad.

## Higiene

- No editar artefactos generados: `**/dist/**`, `**/node_modules/**`.
- Mantener textos de UI en **español**.
- Preferir helpers/módulos compartidos antes de duplicar lógica.

## Git

- Mensajes de commit: Conventional Commits (ej. `feat(ui): ...`, `fix(json): ...`).
- No crear branches a menos que se pida explícitamente.

