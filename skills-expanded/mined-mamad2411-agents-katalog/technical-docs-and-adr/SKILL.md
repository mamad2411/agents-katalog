---
name: technical-docs-and-adr
description: Documentación técnica que se mantiene viva — registros de decisión de arquitectura (ADR) con contexto/decisión/consecuencias/estado, runbooks operativos, READMEs útiles, docs junto al código y diagramas como fuente. Usar al tomar una decisión de arquitectura no trivial, al escribir el README de un módulo o repo, al preparar un runbook de operación o incidente, o al decidir qué merece documentarse y qué se explica solo con el código.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Documentación técnica y ADR

La mejor documentación es el código claro y los tests. Lo que el código NO puede contar es el
**porqué**: por qué se eligió esto y no lo otro, qué se descartó, qué operar cuando algo falla.
Documentá eso, y solo eso. Doc que repite el código envejece y miente; borrala.

## 1. ADR — registro de decisión de arquitectura

Cada decisión técnica no trivial (elegir una librería, un patrón de datos, un límite de servicio,
un trade-off de consistencia) se registra en un ADR corto, versionado junto al código
(`docs/adr/NNNN-titulo.md`). Formato de Michael Nygard:

```
# NNNN. Título de la decisión

Estado: propuesto | aceptado | deprecado | reemplazado por ADR-0042
Fecha: 2026-09-19

## Contexto
Qué problema y qué fuerzas están en juego (restricciones, requisitos, lo que ya existe).
Hechos, no opiniones.

## Decisión
Qué se decidió hacer, en voz activa: "Usaremos locking optimista con versión de fila".

## Consecuencias
Lo que resulta de la decisión: lo bueno, lo malo y lo que ahora es más difícil.
Las alternativas descartadas y por qué.
```

Reglas de ADR:
- Uno por decisión, corto (una pantalla). Numerados y en orden.
- **Inmutables**: un ADR no se edita para cambiar de opinión; se crea uno nuevo con estado
  `aceptado` que marca al viejo como `reemplazado por`. El historial de decisiones es el valor.
- Se escribe cuando la decisión se toma, no meses después "para documentar".

## 2. Runbook operativo

Para todo servicio que corre en producción, un runbook responde "algo pasa, ¿qué hago?":
- cómo se despliega y cómo se hace rollback (`release-and-rollback`, `coolify-operations`);
- health/readiness y dónde están logs, métricas y traces (`backend-observability`);
- fallas conocidas y su mitigación paso a paso;
- contactos/dueños y cómo escalar (`incident-response-postmortem`);
- procedimientos delicados (restore de backup, rotación de secretos) enlazados a su skill.

El runbook se prueba: si nadie lo siguió nunca, no sabés si funciona (igual que un backup sin
restore, `backup-restore-dr`).

## 3. README útil

El README de un repo o módulo dice, en este orden: qué es y para quién, cómo levantarlo en local
(comandos reales que funcionan), cómo correr los tests, la estructura de carpetas en dos líneas, y
dónde está el resto (ADRs, runbook, contrato de API). No es un manual: es un mapa hacia lo demás.

## 4. Qué documentar y qué no

| Documentar | No documentar |
|---|---|
| Por qué de una decisión (ADR) | Qué hace una función (lo dice su nombre y su test) |
| Cómo operar/desplegar/recuperar (runbook) | Historial de cambios (eso es git) |
| Contrato de API para el consumidor (`api-openapi-docs`) | Comentarios que repiten la línea siguiente |
| Invariantes y trampas no obvias | Tutoriales de la librería (linkeá su doc oficial) |
| Cómo levantar el proyecto (README) | Código comentado "por si acaso" |

Regla: si el código puede expresarlo, expresalo en el código (`clean-code`), no en un doc que se
desincroniza. Un comentario o doc es un fallo de expresión que a veces vale la pena.

## 5. Diagramas como fuente

- Preferí diagramas en texto versionable (PlantUML, Mermaid) sobre imágenes que nadie puede
  editar. Un diagrama es código: vive en el repo, se revisa en el diff.
- El modelo de datos es un caso especial: el diagrama es la **fuente de verdad** que genera el
  esquema, no una ilustración (`data-modeling-plantuml`, `model-driven-schema`).
- Un diagrama debe mostrar el mecanismo real (flujo de datos, límites de confianza), no cajas
  decorativas. Si no aclara nada que el texto ya dice, sacalo.

## 6. Docs junto al código y vivos

- La doc vive en el repo, cerca de lo que describe, y se actualiza en el mismo PR que el cambio.
  Un cambio de comportamiento con doc desactualizada es un PR incompleto.
- Distinguí lo que va en CLAUDE.md/rules (instrucciones al agente, `claude-md-authoring`) de lo que
  va en docs (conocimiento para humanos). No dupliques entre ambos.

## Anti-patrones

- Doc en una wiki externa que nadie actualiza y contradice al repo.
- ADR editado para "cambiar la decisión" borrando la historia.
- README con comandos que ya no existen.
- Diagrama-imagen imposible de versionar ni editar.
- Documentar el qué (lo obvio) y omitir el porqué (lo valioso).

## Checklist

- [ ] La decisión no trivial quedó en un ADR con contexto/decisión/consecuencias/estado.
- [ ] El ADR es nuevo, no una edición que borra la decisión anterior.
- [ ] El servicio en producción tiene runbook de deploy, rollback, observabilidad y escalado.
- [ ] El README levanta el proyecto con comandos que de verdad funcionan.
- [ ] Los diagramas están en texto versionable y muestran el mecanismo real.
- [ ] La doc se actualizó en el mismo PR que el cambio de comportamiento.
- [ ] No dupliqué en docs lo que ya dicen el código o el CLAUDE.md.
