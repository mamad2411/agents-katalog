---
name: uat-acceptance-signoff
description: Aceptación de usuario/negocio y sign-off — criterios de aceptación verificables, guion de UAT sobre datos realistas, quién valida y quién firma, gestión de los defectos hallados, decisión go/no-go y evidencia del sign-off. Usar al cerrar una feature o carril de cara al negocio, antes de habilitar algo en producción, al coordinar la validación con el responsable funcional/clínico, o cuando "está terminado" técnicamente pero nadie del negocio lo aprobó.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# UAT y sign-off

UAT valida que lo construido **resuelve la necesidad del negocio**, no solo que "pasa los tests".
Es la última compuerta antes de exponer algo. Distinta del QA técnico (`qa-strategy`,
`qa-orchestration`): UAT la ejecuta o valida quien representa al usuario/negocio, sobre criterios
de aceptación acordados de antemano (`requirements-and-acceptance`).

## Precondiciones
- Criterios de aceptación escritos y verificables ANTES de construir (no se negocian durante UAT).
- QA técnico en verde: unit, API, E2E, regresión relevante. UAT no es para encontrar bugs básicos.
- Entorno estable (staging) con datos realistas y **sintéticos** (nunca datos reales de pacientes;
  ver `data-privacy-sensitive`, `synthetic-test-data-generation`).
- Versión desplegada identificable (commit SHA; ver `deployment-verification-smoke`).

## Guion de UAT
Para cada criterio de aceptación, un paso concreto redactado en lenguaje del negocio:
> Dado <contexto de negocio>, cuando <acción del usuario>, entonces <resultado observable esperado>.

- Cubrí el camino feliz de cada criterio y los casos de negocio importantes (no todos los bordes
  técnicos: eso ya lo cubrió QA).
- Incluí roles reales: quién hace qué (médico, administrativo, paciente) y qué debería o no poder.

## Roles y firma
- **Ejecutor**: valida los pasos (usuario referente o QA acompañando al negocio).
- **Aprobador**: quien tiene autoridad para aceptar (dueño de producto / responsable funcional; en
  temas clínicos, el responsable clínico). Definí quién es antes de empezar.
- El sign-off es explícito: quién aprobó, qué versión, con qué salvedades, cuándo.

## Gestión de defectos en UAT
Clasificá cada hallazgo y su efecto en la decisión:
| Severidad | Efecto |
|---|---|
| Bloqueante | No-go. Se corrige y se re-valida el criterio afectado. |
| Mayor | Go condicionado o no-go según el caso; acuerdo explícito. |
| Menor / cosmético | Go con backlog; registrado, no olvidado. |
- Todo defecto se registra como bug reproducible (`bug-reporting-standard`), no como comentario suelto.

## Go / No-Go
Decisión registrada con base en: criterios cumplidos, defectos abiertos por severidad, riesgos
residuales y salvedades aceptadas. Un "go con salvedades" lista las salvedades y su dueño/plazo.

## Anti-patrones
- Cambiar los criterios de aceptación durante UAT para que "pase".
- UAT usada para encontrar bugs que QA técnico debía haber cubierto.
- Datos reales de producción en el entorno de UAT.
- "Lo aprobó alguien" sin registro de quién, qué versión ni salvedades.
- Menores convertidos en "ya lo vemos" sin backlog (se pierden).

## Checklist
- [ ] Criterios de aceptación acordados y sin cambios durante UAT.
- [ ] QA técnico en verde y versión (SHA) identificada.
- [ ] Guion cubre cada criterio en lenguaje de negocio.
- [ ] Aprobador definido y con autoridad (clínico si aplica).
- [ ] Defectos clasificados por severidad y registrados como bugs.
- [ ] Decisión go/no-go con salvedades, dueño y plazo.

## Evidencia / DoD
Para declarar UAT superada, pegá/adjuntá:
1. Guion ejecutado con resultado por criterio (OK / falla + bug).
2. Versión desplegada (SHA) y entorno.
3. Lista de defectos con severidad y estado.
4. Registro de sign-off: aprobador, fecha, decisión go/no-go, salvedades.
Sin sign-off explícito registrado, el estado es `BLOCKED`, no aprobado.
