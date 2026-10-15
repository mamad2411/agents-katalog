---
name: work-plan
description: "Planifica trabajo de distintos tipos sin generar código ni pruebas. Dos tipos de plan: (1) tareas técnicas (TK-XXX) bajo una historia de usuario existente; (2) tareas de mantenimiento (WI-XXX) sin historia asociada — bugs, refactor, deuda técnica, actualización de dependencias, tareas operativas. Activar siempre que el usuario pida planificar implementación, descomponer trabajo, definir alcance técnico, documentar especificaciones técnicas o planificar mantenimiento / deuda técnica / refactor, aunque no nombre «tarea», «TK» o «WI». Activar también — por defecto — cuando solo entregue una referencia a una historia (p. ej. «US-004», «planifica US-007», «tareas para esta historia»): proponer stubs agrupados por repositorio que cubran los criterios de aceptacion (AC-XXX). Selecciona el tipo según haya o no historia asociada y carga su definición desde references/."
license: MIT
---

# Skill: Planificar trabajo

Guía general para **planificar trabajo** produciendo documentos de especificación —no código ni pruebas— de **distintos tipos**. Cada tipo de plan tiene su propia definición (flujos, plantillas, validaciones) en `references/`. El cuerpo de este `SKILL.md` contiene únicamente lo **transversal** a todos los tipos; el detalle de cada tipo se carga solo cuando se necesita.

> **Qué no hace este skill (cualquier tipo):** no implementa código, no ejecuta pruebas, no crea ADRs. Lo que no está acordado va a **Observaciones** o se pregunta al usuario — nunca se inventa.

---

## Regla de handoff (transversal)

Todo paso a otra fase del ciclo se realiza **invocando el skill correspondiente**, nunca ejecutando ese trabajo directamente desde este skill. El ciclo es `work-define` → `work-plan` → `work-implement` → `work-integrate` (con `pr-create` como alternativa de cierre).

- **Si el usuario pide implementar** (escribir código, crear/ejecutar pruebas, "impleméntalo", "hazlo", "desarróllalo") mientras se está en `work-plan`: **invocar `/work-implement`** pasándole el contexto del artefacto. Este skill **no** escribe código ni ejecuta pruebas bajo ninguna circunstancia.
- **Solo se implementa trabajo en `Estado: Ready`.** Si el artefacto sigue en `Draft` (stub o incompleto), no hacer handoff a implementación: completarlo primero en este skill.
- **Si el conflicto es funcional** (contradice el `README.md` de una US), escalar a **`work-define`**; este skill no modifica la US.
- **Si una TK/WI menciona elementos técnicos sin especificación** (un modelo, API o flujo citado que no existe en `docs/specs/technical-docs/`) y el usuario pide más detalle sobre alguno de ellos, **delegar mediante subagente a `/design-define`**: ese skill hace el grilling técnico, crea/actualiza el documento de la capability y devuelve las referencias (ruta + ancla) para agregarlas a la sección **Referencias** de la TK/WI. Este skill **no** crea ni edita documentos en `technical-docs/`.

No sustituir una invocación de skill por "hacer el trabajo aquí". El handoff es explícito y por skill en cada frontera del ciclo.

---

## Subagente

**Si el proyecto define el subagente `docs-specialist`, ejecutar este skill bajo ese subagente**, sea cual sea el tipo de plan. Si no existe, ejecutar el flujo normalmente.

---

## Cómo preguntar al usuario

Cuando este skill (o cualquiera de sus referencias) indique **preguntar, pedir, confirmar, validar o sugerir** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** del cliente (la que renderiza opciones tappables o un selector) en lugar de redactar la pregunta como prosa libre. Reglas:

- **Opciones cortas y mutuamente excluyentes** (2–4 por pregunta) cuando la respuesta admita categorías; usar entrada libre solo si no hay forma razonable de enumerar opciones (p. ej. el objetivo breve de un stub).
- **No repreguntar** lo que ya está respondido en el contexto, en `.agents/MEMORY.md`, o en los documentos existentes del repo.
- **Recopilación inicial:** agrupar las preguntas pendientes en una sola tanda (hasta tres por bloque); no ir descubriendo huecos turno a turno.
- **Confirmaciones de creación:** una pregunta por turno con opciones claras (p. ej. Opciones: [Confirmar] / [Ajustar] / [Cancelar]); no crear archivos antes de la confirmación.
- **Fallback:** si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3…).

Cada vez que una referencia diga *preguntar al usuario*, *validar con el usuario*, *confirmar* o *sugerir al usuario* asume este mecanismo; no se repite allí.

---

## Resolución de idioma

El idioma de los documentos generados y de los mensajes al usuario se decide en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si no, usar el idioma del mensaje del usuario y **preguntar al usuario si desea persistir su preferencia de idioma en la memoria**.
3. Si no se puede inferir, **preguntar al usuario** qué idioma prefiere y, tras su respuesta, **preguntar si desea persistir su preferencia de idioma en la memoria**; no decidir el idioma por cuenta propia.

---

## Selección del tipo de plan

**Antes de cualquier otra cosa**, identificar qué tipo de plan corresponde y cargar su definición. No mezclar tipos en una misma ejecución.

La señal que distingue los tipos es **si el trabajo tiene una historia de usuario asociada o no**.

| Tipo de plan | Cómo se identifica | Definición a leer |
|--------------|--------------------|-------------------|
| **Tarea técnica de historia de usuario** | El trabajo **referencia una historia de usuario**: prefijo de historia `US-XXX` (p. ej. «planifica US-007», «tareas para esta historia»), una historia ubicada bajo el árbol de user-stories del repo, o la edición de una `TK-XXX` que cuelga de una US. | `references/user-story-tasks.md` — **leer antes de redactar.** |
| **Tarea de mantenimiento** | El trabajo **no tiene una historia de usuario asociada** (corrección de bug, refactor, deuda técnica, actualización de dependencias, tarea operativa), o el usuario pide explícitamente «plan/tarea de mantenimiento». | `references/maintenance-tasks.md` — **leer antes de redactar.** |

Reglas de selección:

- **Hay historia asociada → tarea de historia de usuario. No la hay → mantenimiento.** Leer la referencia correspondiente y seguir **únicamente** su flujo.
- Si no está claro **si existe o no** una historia asociada (p. ej. una referencia ambigua que podría apuntar a una US), **preguntar al usuario** antes de continuar; no asumir la existencia de una US ni inventarla.
- Si el tipo seleccionado aún no tiene su flujo definido, la propia referencia indica cómo proceder (p. ej. confirmar con el usuario en lugar de inventar estructura).

---

## Integración con un sistema de seguimiento externo (condicional)

La sincronización con un sistema de seguimiento de trabajo externo (Azure DevOps, Jira u otro) es transversal a los tipos de plan que crean work items, pero **solo aplica si el repositorio está vinculado a uno**. Este skill solo resuelve **si** hay vinculación y **qué** referencia cargar; todo el detalle propio de cada sistema (herramienta MCP, campos, tipos de work item, configuración de conexión, límites de formato) vive exclusivamente en su archivo de `references/` — nunca aquí ni en las referencias de tipo de plan.

1. **Detectar** la vinculación leyendo `.agents/MEMORY.md` (raíz del repo): buscar la señal `work_item_tracking: <sistema>` con valor no vacío (p. ej. `azure_devops`).
2. **Si NO hay señal** → el repo no usa un tracker externo. Continuar con el flujo del tipo de plan usando ID secuencial local; **no** leer ninguna referencia de tracker.
3. **Si hay señal** → cargar `references/<sistema>.md` (p. ej. `references/azure-devops.md` para `work_item_tracking: azure_devops`) y seguir **únicamente** sus pasos antes de crear cualquier archivo local. Si no existe un archivo de referencia para el sistema indicado, informar al usuario y continuar con ID secuencial local.

**Regla de fidelidad (transversal a cualquier sistema):** toda la información del documento local debe quedar representada en el work item externo — en un campo dedicado si el sistema lo expone (p. ej. un campo de criterios de aceptación), o dentro de la descripción si no lo expone. Ninguna sección del `.md` puede omitirse al sincronizar; el objetivo es poder reconstruir el documento completo a partir del work item si el archivo local se perdiera. Qué campo usa cada sistema para qué sección es detalle de su archivo de referencia.

---

## Mensaje al usuario

Solo resultados y lo que el usuario debe saber o decidir. No incluir razonamiento interno, cadenas de pensamiento ni narración del trabajo en curso («leí la US», «creé el archivo»). Si hay pendientes o aclaraciones, listarlos en viñetas agrupadas por artefacto.

---

## Mapa de referencias

| Archivo | Cuándo leerlo |
|---------|---------------|
| `references/user-story-tasks.md` | Tipo de plan = tarea técnica de historia de usuario. Contiene modos de invocación, ubicaciones, flujos (stub, TK completa, actualizar, sugerir stubs desde US), checklist, ejemplos y anti-patrones. |
| `references/maintenance-tasks.md` | Tipo de plan = tarea de mantenimiento. |
| `references/<sistema>.md` (p. ej. `azure-devops.md`) | Solo si se detecta vinculación a un tracker externo (ver [Integración con un sistema de seguimiento externo](#integración-con-un-sistema-de-seguimiento-externo-condicional)); el archivo concreto depende del valor de `work_item_tracking`. |
| `assets/task-template.md` | Plantilla canónica de una tarea de historia de usuario (`TK-XXX`). Leer antes de redactar el documento. |
| `assets/work-item-template.md` | Plantilla canónica de una tarea de mantenimiento (`WI-XXX`). Leer antes de redactar el documento. |
