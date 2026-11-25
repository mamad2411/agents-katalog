---
name: design-define
description: "Crear o actualizar documentación técnica (modelos de datos, APIs/endpoints, flujos/procesos, diagramas de clases/contexto/contenedores/componentes) en docs/specs/technical-docs/, organizada por capability, para que sirva como referencia de implementación de historias de usuario (US-XXX), tareas técnicas (TK-XXX) y tareas de mantenimiento (WI-XXX). Activar cuando el usuario pida documentar o especificar un modelo, entidad, DTO, contrato de API, endpoint, flujo, proceso técnico o un diagrama (clases, C4, arquitectura de la capability); cuando pida «más detalle» sobre un elemento técnico sin especificación mencionado en una US, TK o WI; o cuando otro skill (work-define, work-plan) delegue la creación de la especificación técnica. También activar con «/design-define», «documento técnico», «technical doc», «especificación técnica» o «diseño técnico», aunque el usuario no nombre la capability."
license: MIT
---

# Skill: Documentación técnica por capability

Guía para **crear o actualizar** documentos técnicos en `docs/specs/technical-docs/`. Cada documento pertenece a una **capability** (una capacidad del sistema: facturación, autenticación, catálogo…) y estandariza los **modelos de datos**, **APIs/endpoints**, **flujos/procesos** y **diagramas** (clases, contexto, contenedores, componentes…) de esa capability, con elementos identificables (`MD-XX`, `API-XX`, `FL-XX`, `DG-XX`) que las US, TK y WI enlazan como referencia de implementación.

> **Alcance:** este skill produce **especificación técnica**, no documentación funcional ni código. El valor de negocio y los criterios de aceptación viven en la US (`work-define`); el plan de implementación vive en las TK/WI (`work-plan`); las decisiones de arquitectura viven en ADRs (`docs/adr/`, nunca creados desde aquí). Un documento técnico describe **qué forma tienen** los modelos, contratos y flujos — no por qué se eligió una tecnología ni cómo se codifica.

La plantilla canónica está en `assets/technical-doc-template.md` (léela antes de escribir cualquier documento). Los estándares de cada tipo de elemento están en `references/element-standards.md`.

## Subagente

**Si el proyecto define el subagente `docs-specialist`, ejecutar este skill bajo ese subagente.** Si no existe en el proyecto:

- **Invocación directa por el usuario:** ejecutar el flujo normalmente, sin subagente.
- **Invocación desde otro skill** (`work-define`, `work-plan`): ejecutar este skill bajo un **subagente genérico** (el de propósito general que exponga el cliente). La delegación siempre ocurre en un subagente — con `docs-specialist` si existe, genérico si no — para aislar el contexto del skill llamador y que la respuesta final sea solo las referencias devueltas.

Este skill es frecuentemente **invocado por otros skills mediante un subagente** (`work-define` al detectar que una US define flujos, modelos o APIs; `work-plan` cuando una TK/WI menciona elementos técnicos sin especificación). En ese modo, ver [Modo delegado](#modos-de-invocación).

---

## Mapa de referencias

Carga el archivo correspondiente cuando vayas a ejecutar la tarea; el detalle íntegro vive en `references/`.

| Necesitas… | Archivo |
| ---------- | ------- |
| Flujo paso a paso de **crear** y **actualizar**, grilling de preguntas, validación antes de crear, modo delegado, checklist, ejemplos, anti-patrones y handoffs | [`references/flow.md`](references/flow.md) |
| Estándares de definición de **modelos de datos** (`MD-XX`), **APIs/endpoints** (`API-XX`), **flujos/procesos** (`FL-XX`) y **diagramas** (`DG-XX`: clases, contexto, contenedores, componentes): tablas, diagramas Mermaid, ejemplos | [`references/element-standards.md`](references/element-standards.md) |
| Estructura del documento técnico de una capability | `assets/technical-doc-template.md` |

---

## Resolución de idioma

El idioma del documento técnico (descripciones y texto natural; los nombres de campos, rutas y payloads siguen la convención del código) se decide en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla. En modo delegado, usar la preferencia que transmita el skill llamador o el idioma de la US/TK/WI de origen.
2. Si no, usar el idioma del mensaje del usuario y **preguntar al usuario si desea persistir su preferencia de idioma en la memoria**.
3. Si no se puede inferir, **preguntar al usuario** qué idioma prefiere y, tras su respuesta, **preguntar si desea persistir su preferencia de idioma en la memoria**; no decidir el idioma por cuenta propia.

---

## Ubicación de archivos

| Artefacto | Ruta |
| --------- | ---- |
| Documento técnico de capability | `docs/specs/technical-docs/[capability].md` |
| Archivos de apoyo (imágenes, esquemas exportados) | `docs/specs/technical-docs/assets/[capability]/` |
| Glosario | `docs/specs/glossary.md` (opcional) |

### Convenciones

- **Un documento por capability.** Si el documento de la capability ya existe, se **actualiza** (se añaden o modifican elementos); nunca crear un segundo documento para la misma capability.
- Nombre de archivo: capability en minúsculas, kebab-case, sin artículos ni palabras vacías. Ejemplos: `facturacion.md`, `gestion-recetas.md`, `autenticacion.md`.
- Dentro del documento, cada elemento lleva id secuencial **por tipo**, único en el ámbito de la capability: modelos `MD-01, MD-02, …`; APIs `API-01, API-02, …`; flujos `FL-01, FL-02, …`; diagramas `DG-01, DG-02, …`. No renumerar elementos existentes: los ids son estables porque otras historias y tareas ya pueden enlazarlos.
- Cada elemento es un encabezado `###` con el formato `### MD-01: Nombre` para que sea enlazable por ancla, p. ej. `docs/specs/technical-docs/facturacion.md#md-01-factura`.
- El documento lleva **fecha de creación** y **última actualización**. Las lagunas abiertas se registran en **Observaciones** del propio documento.

---

## Modos de invocación

| Modo | Quién invoca | Entrada típica | Salida esperada |
| ---- | ------------ | -------------- | --------------- |
| **Directo** | El usuario | «Documenta el modelo de factura», «especifica la API de pagos», «dame más detalle del flujo de aprobación de la TK-004» | Documento creado/actualizado + resumen al usuario + oferta de enlazarlo desde la US/TK/WI relacionada |
| **Delegado** | `work-define` o `work-plan` vía subagente | Contexto de la US/TK/WI + los elementos técnicos a especificar | Documento creado/actualizado y, **como respuesta final del subagente, la lista de referencias** (ruta relativa + ancla de cada elemento) para que el skill llamador las agregue a la sección Referencias del artefacto |

En modo delegado, el grilling de preguntas se dirige igualmente al usuario (el subagente hereda la herramienta de preguntas estructuradas); si el entorno no permite preguntar, documentar las lagunas en Observaciones y reportarlas en la respuesta final en lugar de inventar. **En modo directo**, si el entorno tampoco permite preguntar (p. ej. sesión desatendida/programada sin nadie que responda en el momento), aplicar el mismo criterio: no inventar, documentar cada laguna en Observaciones citando el elemento afectado, y destacarlas de forma prominente al principio del resumen final — a diferencia del modo delegado, aquí no hay un skill llamador que las recoja, así que es el propio resumen al usuario el único lugar donde quedan visibles.

---

## Cómo preguntar al usuario (grilling)

Cuando este skill (o sus referencias) indique **preguntar, pedir, confirmar, validar o sugerir** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** del cliente (la que renderiza opciones tappables o un selector) en lugar de prosa libre. Reglas:

- **Opciones cortas y mutuamente excluyentes** (2–4 por pregunta) cuando la respuesta admita categorías; entrada libre solo si no hay forma razonable de enumerar opciones (p. ej. la descripción de un campo).
- **No repreguntar** lo que ya está respondido en el contexto, en `.agents/MEMORY.md`, en la US/TK/WI de origen o en el documento técnico existente.
- **Recopilación inicial (antes de redactar):** una sola tanda con hasta **tres preguntas por bloque**; agrupar las lagunas detectadas, no ir descubriendo turno a turno. Si hay más de tres lagunas, encadenar tandas hasta agotarlas o hasta que el usuario indique que lo restante quede como Observación.
- **Fallback:** si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3…).

El detalle de **qué preguntar por tipo de elemento** (campos sin tipo, códigos de error sin definir, ramas de flujo ambiguas…) está en [`references/flow.md`](references/flow.md#grilling-por-tipo-de-elemento).

---

## Información requerida antes de redactar

**No inventar nada** — si un dato no es explícito ni inferible del repo, preguntar al usuario (o reportarlo como laguna, en cualquier modo, cuando el entorno no permite preguntar — ver [Modos de invocación](#modos-de-invocación)).

| Dato | Cómo obtenerlo | Si no está disponible |
| ---- | -------------- | --------------------- |
| **Capability** a la que pertenece el elemento | Indicada por el usuario/skill llamador, o inferible de la US/TK/WI y de los documentos existentes en `technical-docs/` | Preguntar; proponer opciones a partir de los documentos existentes antes de crear una capability nueva |
| **Tipo(s) de elemento** (modelo, API, flujo, diagrama) | Del pedido o del contenido de la US/TK/WI | Preguntar |
| **Contenido de cada elemento** (campos, contratos, pasos) | Del input recibido, del código existente del repo, o de la US/TK/WI de origen | Grilling de preguntas; lo irresoluble queda en Observaciones |
| **Artefacto(s) que lo consumirán** (US/TK/WI) | Del contexto o del skill llamador | Opcional en modo directo; si existe, ofrecer enlazar la referencia al terminar |
| **Idioma de preferencia** | Ver [Resolución de idioma](#resolución-de-idioma) | Preguntar; no decidir por cuenta propia |

---

## Flujo (resumen)

El procedimiento completo está en [`references/flow.md`](references/flow.md). Síntesis:

- **Crear/actualizar:** resolver capability → leer el documento existente si lo hay → detectar lagunas y hacer el grilling → redactar los elementos con `assets/technical-doc-template.md` y los estándares de `references/element-standards.md` → asignar ids estables → actualizar la fecha de última actualización → glosario si aplica.
- **Enlazar:** en modo delegado, devolver las referencias (ruta + ancla) al skill llamador; en modo directo, ofrecer agregar la referencia a la sección Referencias de la US/TK/WI relacionada.
- **Cierre:** si quedaron lagunas en Observaciones, ofrecerle al usuario las preguntas que las cerrarían (misma mecánica de grilling).

---

## Mensaje al usuario

Solo resultados y lo que el usuario debe saber o decidir. No incluir razonamiento interno ni narración del trabajo en curso («leí la US», «creé el archivo»). Si hay pendientes, listarlos agrupados por elemento (`MD-XX`, `API-XX`, `FL-XX`, `DG-XX`). En modo delegado, la respuesta final del subagente es **datos para el skill llamador** (rutas y anclas), no prosa para el humano.
