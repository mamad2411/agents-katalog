---
name: incident-response-postmortem
description: Respuesta a incidentes de producción y postmortem sin culpables — clasificar severidad, asignar roles (comandante, comunicación, operador), mitigar antes que diagnosticar, comunicar con cadencia, y después reconstruir la línea de tiempo, la causa raíz y las acciones correctivas con dueño y fecha. Usar cuando un servicio se cae o degrada, ante una posible brecha de datos, al coordinar la respuesta en caliente, y al escribir el postmortem una vez resuelto.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Respuesta a incidentes y postmortem

Un incidente es cualquier cosa que afecta a los usuarios en producción: caída, degradación,
datos incorrectos o una posible exposición de datos. En una plataforma de salud, la sospecha de
acceso indebido a datos de pacientes es un incidente de máxima prioridad. El objetivo en caliente
es **restaurar el servicio**; el aprendizaje viene después, sin buscar culpables.

## 1. Clasificar severidad

Definí los umbrales concretos en el CLAUDE.md/runbook del proyecto; como guía:

| Sev | Qué es | Respuesta |
|---|---|---|
| **SEV1** | Caída total, pérdida/corrupción de datos, o sospecha de brecha de datos sensibles | Todo el equipo, ya, 24/7 |
| **SEV2** | Funcionalidad crítica degradada para muchos usuarios | Respuesta inmediata en horario, guardia si aplica |
| **SEV3** | Impacto acotado, con workaround | Se agenda, no despierta a nadie |

Ante la duda entre dos niveles, subí. Una sospecha de brecha de datos es SEV1 hasta que se
demuestre lo contrario, y dispara la ruta legal/compliance (`regulatory-compliance-mapping`,
`data-privacy-sensitive`).

## 2. Roles (aunque el equipo sea chico)

- **Comandante del incidente**: coordina, decide, no ejecuta el fix con las manos. Una sola persona.
- **Operador(es)**: investiga y aplica la mitigación.
- **Comunicación**: informa a stakeholders/usuarios con la cadencia acordada.

En un equipo de pocas personas una puede tener dos sombreros, pero el rol de comandante siempre
está asignado explícitamente: "yo comando este incidente".

## 3. En caliente: mitigar antes que entender

El orden importa. No te pongas a depurar la causa raíz mientras el sitio está caído.

1. **Estabilizá**: ¿hay una acción rápida que restaura el servicio? Rollback del último deploy
   (`release-and-rollback`), feature flag off, escalar recurso, cortar la fuente del daño.
   El rollback es casi siempre la mitigación más rápida y segura.
2. **Contené el daño**: si hay datos en riesgo, frená la escritura/exposición antes que perseguir
   el porqué.
3. **Comunicá** que estás en eso, con la primera actualización, aunque no tengas la causa.
4. Recién con el servicio estable, pasá a la causa raíz (`root-cause-debugging`).

Usá la observabilidad para orientarte, no para adivinar: logs, métricas y traces
(`backend-observability`). Registrá cada acción con hora — es la base de la línea de tiempo.

## 4. Comunicación

- Cadencia fija (p.ej. cada 30 min en SEV1) aunque sea "seguimos trabajando, sin novedad".
- Mensaje honesto: qué pasa, a quién afecta, qué estás haciendo, cuándo la próxima actualización.
  Sin promesas de tiempo que no podés cumplir.
- Un solo canal oficial del incidente. La coordinación técnica no se mezcla con el anuncio a usuarios.

## 5. Postmortem sin culpables

Dentro de los pocos días siguientes (definí el plazo en el runbook), escribí el postmortem. Es un
documento de aprendizaje, no un juicio. Blameless de verdad: la gente actuó razonablemente con la
información que tenía; lo que falló fue el sistema (proceso, guardas, visibilidad), y eso es lo que
se arregla.

Estructura:
- **Resumen**: qué pasó, impacto (usuarios, duración, datos), severidad.
- **Línea de tiempo**: hechos con hora — detección, acciones, hitos, resolución. Sin interpretación.
- **Causa raíz**: la cadena completa hasta la causa que explica TODOS los síntomas
  (`root-cause-debugging`). Los "5 por qué" hasta llegar a una causa sistémica, no a "fulano se equivocó".
- **Qué funcionó y qué no**: de la respuesta misma (detección tardía, runbook incompleto, alerta faltante).
- **Acciones correctivas**: cada una con **dueño y fecha**, y priorizadas. Una acción sin dueño no existe.

## 6. Cerrar el ciclo

- Las acciones correctivas entran al backlog como ítems rastreables (`github-issues-projects`), no
  se quedan en el documento.
- Si el incidente reveló una regla que "el agente/equipo debería haber seguido", convertila en una
  guarda determinista (`hooks-and-guardrails`) o en una skill/rule, no en un recordatorio.
- Si hubo o pudo haber exposición de datos personales/clínicos, seguí el proceso de notificación de
  brechas con el responsable legal (`regulatory-compliance-mapping`) — no lo decidas por tu cuenta.

## Anti-patrones

- Depurar la causa raíz con el sitio caído en vez de hacer rollback y estabilizar.
- Incidente sin comandante: tres personas tocando producción a la vez sin coordinar.
- Postmortem que nombra culpables → la próxima vez nadie reporta ni cuenta la verdad.
- Acciones correctivas sin dueño ni fecha → se repite el incidente.
- No comunicar "porque todavía no sé la causa".
- Tratar una sospecha de brecha de datos sensibles como un bug técnico más.

## Checklist en caliente

- [ ] Severidad asignada (subí ante la duda; brecha de datos sensibles = SEV1).
- [ ] Comandante del incidente nombrado.
- [ ] Mitigué/estabilicé antes de diagnosticar (rollback como primera opción).
- [ ] Daño contenido si había datos en riesgo.
- [ ] Comunicación iniciada con cadencia fija.
- [ ] Cada acción registrada con hora.

## Checklist del postmortem

- [ ] Línea de tiempo factual con horas.
- [ ] Causa raíz sistémica que explica todos los síntomas, sin culpables.
- [ ] Acciones correctivas con dueño y fecha, cargadas al backlog.
- [ ] Guardas/alertas nuevas para que no se repita.
- [ ] Ruta legal/compliance seguida si hubo riesgo de datos personales o clínicos.
