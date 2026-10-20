---
name: clean-code-review
description: Revisión de Clean Code y arquitectura para TypeScript/NestJS en Atlas (separación de capas, acoplamiento, nombres, funciones/clases con exceso de responsabilidad, duplicación, errores silenciosos, sobreingeniería). No impone patrones por moda; cada hallazgo debe tener un costo real de mantenibilidad.
---

# clean-code-review

**Propósito.** Mejorar mantenibilidad sin sobrearquitectura.

**Cuándo usarla.** En revisión de un módulo/PR, o al detectar deuda estructural.
**Cuándo NO.** Para bugs de seguridad (usa `security-audit`) o rendimiento (usa `performance-audit`).

**Fuentes obligatorias.** El código a revisar, `.claude/rules/10-typescript-backend.md`, el grafo graphify, `docs/audit/`.

**Entradas.** Módulos/archivos objetivo. Sin entrada, muestrea `src/modules/`, `src/common/`, `src/database/`.

**Condiciones de parada.** No propongas un patrón sin un costo de mantenibilidad concreto que lo justifique.

**Flujo por fases.**
1. Capas: ¿controladores delgados? ¿lógica en services? ¿modelos ORM devueltos al transporte?
2. Acoplamiento entre módulos: dependencias circulares, repositories exportados sin consumidor.
3. Nombres ambiguos; funciones/clases con demasiadas responsabilidades; archivos gigantes.
4. Duplicación semántica (p.ej. helpers reimplementados, modelos duplicados).
5. Errores silenciosos: `catch {}` vacíos, promesas sin await.
6. Anidamiento excesivo, abstracciones prematuras, sobreingeniería.
7. Consistencia de convenciones entre módulos.

**Comandos permitidos.** Lectura, grep, `graphify`, `yarn type-check`, `yarn lint`, `/simplify` sobre el diff.
**Comandos prohibidos.** Refactors masivos sin cobertura de tests que los respalde.

**Evidencia requerida.** `archivo:línea` + costo concreto de mantener el código como está.

**Entregables.** Informe: resumen con nota de salud, hallazgos por severidad (Alta/Media/Baja) con evidencia+recomendación, aspectos positivos, no verificado.

**Formato.** Español; cada hallazgo justifica su costo real.

**Checklist final.** ¿Cada hallazgo con costo de mantenibilidad? ¿Nada impuesto por moda? ¿Positivos reconocidos?

**Limitaciones.** Estática; no ejecuta el código.

**Trazabilidad.** `CLAUDE_ORGANIZAR_SKILLS_BACKEND.md` §11 + auditoría 2026-07-21 (Arquitectura y Clean Code).
