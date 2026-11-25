---
name: bug-reporting-standard
description: Estándar de la casa para reportar un bug de forma reproducible y accionable — pasos exactos, resultado esperado vs actual, entorno, evidencia (logs, trace, captura, request id), severidad vs prioridad, alcance afectado e indicación de si es una regresión. Usar al abrir un issue de bug, al documentar un fallo hallado en QA, al triar el backlog de defectos, o al convertir un "no anda" en algo que otra persona pueda reproducir y arreglar.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Reporte de bug

Un bug sin pasos de reproducción es una anécdota. El reporte tiene que permitir que otra persona
lo reproduzca y lo arregle sin volver a preguntar. Alimenta a `root-cause-debugging` (para el fix)
y se registra según `github-issues-projects`.

## Cuándo aplica

- Al abrir un issue de bug o documentar un fallo de QA.
- Al triar defectos del backlog.
- Al convertir un "no funciona" difuso en un reporte reproducible.

## 1. Anatomía del reporte

```markdown
## Título: <síntoma concreto, no "no anda">
### Pasos para reproducir
1. ...
2. ...
### Esperado
### Actual
### Entorno
- app/versión/commit, navegador/dispositivo, rol de usuario, tenant, entorno (dev/staging)
### Evidencia
- request id, log recortado, trace/screenshot, respuesta de red
### Severidad / Prioridad
### Alcance
### ¿Regresión?  (funcionaba antes en <versión/commit>)
```

## 2. Reproducción

- Pasos numerados, desde un estado conocido, con los datos exactos usados.
- Frecuencia: siempre / intermitente / una vez. Si es intermitente, decilo — cambia el enfoque
  del diagnóstico.
- Un repro mínimo vale más que una narración larga.

## 3. Esperado vs actual

Separá siempre lo que debería pasar de lo que pasó. "Está mal" no dice cuál de los dos falla.
Cuando exista, citá el criterio de aceptación (`REQ-…`) que se viola.

## 4. Evidencia (sin datos sensibles)

- Log recortado a lo relevante, trace de Playwright, captura, `request id`, código y cuerpo de la
  respuesta de red.
- **Nunca** pegues PII real ni secretos/tokens en el reporte — enmascarálos. Ver `data-privacy-sensitive`.

## 5. Severidad vs prioridad (son distintas)

| | Definición | Ejemplo |
|---|---|---|
| **Severidad** | Impacto técnico del fallo | Pérdida de datos = crítica |
| **Prioridad** | Urgencia de arreglarlo | Typo en home con mucho tráfico = alta prioridad, baja severidad |

Un fallo de baja severidad puede ser de alta prioridad y viceversa. Asigná ambas.

## 6. Alcance y regresión

- **Alcance**: a qué usuarios/roles/tenants/pantallas afecta, y si hay workaround.
- **Regresión**: ¿funcionaba antes? Si sí, indicá en qué versión/commit y qué cambió cerca —
  acelera el diagnóstico.

## Anti-patrones

- "No funciona" / "se rompió" como título.
- Sin pasos, o pasos que empiezan desde un estado desconocido.
- Mezclar esperado y actual.
- Pegar datos sensibles/tokens reales como evidencia.
- Marcar todo como crítico (inflación de severidad que anula el triaje).

## Checklist

- [ ] Título describe el síntoma concreto.
- [ ] Pasos reproducibles desde un estado conocido + frecuencia.
- [ ] Esperado vs actual separados; criterio violado citado si existe.
- [ ] Evidencia adjunta y sin datos sensibles.
- [ ] Severidad y prioridad asignadas por separado.
- [ ] Alcance y estado de regresión indicados.
