---
name: work-define
description: Crear o actualizar una Historia de Usuario. Usar cuando se necesite crear, documentar, actualizar o estandarizar historias de usuario. Activar cuando el usuario solicite una nueva historia de usuario, describa una necesidad funcional, pida refinar requisitos, estructurar funcionalidades o alinear historias existentes a las convenciones del proyecto.
license: MIT
---

# Skill: Historia de usuario

Guía para **crear o actualizar** historias de usuario en el repo del producto.

> **Alcance de una US:** El `README.md` es un documento **funcional**. Registra el valor para el usuario, los **criterios de aceptación** (lista plana con ids `AC-XXX`, categoría entre paréntesis y enunciado RFC 2119) y el estado de avance. El detalle de implementación (DTOs, endpoints, esquemas) va en `docs/specs/technical-docs/` — creado y mantenido por el skill **`design-define`**, nunca directamente desde aquí — o en tareas `TK-XXX`, nunca en la narrativa de la historia. Los documentos técnicos **no son parte de la descripción funcional**; se enlazan desde la sección Referencias de la US y pueden citarse para justificar criterios de INVEST o condiciones del DoR.

La plantilla canónica está en `assets/user-story-template.md` (léela antes de escribir cualquier US).

## Mapa de referencias

Carga el archivo correspondiente cuando vayas a ejecutar la tarea; el detalle íntegro vive en `references/`.

| Necesitas… | Archivo |
| ---------- | ------- |
| Flujo paso a paso de **crear** y **actualizar**, cómo preguntar al usuario, validación antes de crear, checklist completo, ejemplos, anti-patrones y handoffs del ciclo | [`references/flow.md`](references/flow.md) |
| Detalle de **RFC 2119** (tabla de modalidades), **ISO 25010** (categorías de criterios de aceptación no funcionales), rúbrica **INVEST** y **DoR** ampliado | [`references/quality-criteria.md`](references/quality-criteria.md) |
| Estructura del `README.md` de una US | [`assets/user-story-template.md`](assets/user-story-template.md) |

---

## Resolución de idioma

El idioma de la US (criterios de aceptación, INVEST, DoR y texto natural) se decide en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si no, usar el idioma del mensaje del usuario y **preguntar al usuario si desea persistir su preferencia de idioma en la memoria**.
3. Si no se puede inferir, **preguntar al usuario** qué idioma prefiere y, tras su respuesta, **preguntar si desea persistir su preferencia de idioma en la memoria**; no decidir el idioma por cuenta propia.

---

## Ubicación de archivos


| Artefacto             | Ruta                                                                                                                   |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Historia de usuario   | `docs/specs/user-stories/US-XXX-[nombre-corto]/README.md`                                                            |
| Archivos de apoyo     | `docs/specs/user-stories/US-XXX-[nombre-corto]/assets/`                                                              |
| Documentación técnica | `docs/specs/technical-docs/[capability].md` (propiedad del skill `design-define`; este skill solo la referencia, nunca la crea ni edita directamente) |
| Glosario              | `docs/specs/glossary.md` (opcional)                                                                                  |


### Convenciones del nombre de carpeta

- Formato: `US-XXX-[nombre-corto]` con `US-XXX` en mayúsculas y número de 3 dígitos.
- Nombre corto: minúsculas, kebab-case, sin artículos ni palabras vacías.
- Si esta historia se vincula manualmente a un work item de un sistema de seguimiento externo (ver `Work Item (<sistema>)` en la plantilla), el nombre completo `US-XXX-[nombre-corto]` debe respetar el límite de longitud de título que imponga ese sistema; si el nombre corto propuesto lo supera, acortarlo antes de crear la carpeta.
- Ejemplos: `US-001-seleccion-item-sdp-desde-receta`, `US-004-resumen-costos-receta`.
- Archivos de apoyo en `assets/`; enlazarlos desde Referencias con rutas relativas, p. ej. `![Descripción](assets/nombre.png)`.

---

## Información requerida antes de redactar

Antes de crear o editar cualquier US, el agente debe tener clara la siguiente información. **No inventar nada** — si algún dato no es explícito, preguntar al usuario.


| Dato                                            | Cómo obtenerlo                                                                           | Si no está disponible                                                                 |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Actor y valor de negocio**                    | Del contexto o descripción del usuario                                                   | Preguntar al usuario                                                                  |
| **Criterios de aceptación (AC-XXX)**            | Del contexto o descripción del usuario                                                   | Preguntar; sin al menos un `AC-XXX` INVEST no es valorable y la historia solo puede crearse en Draft |
| **Idioma de preferencia**                       | Ver [Resolución de idioma](#resolución-de-idioma) | Preguntar al usuario; no decidir el idioma por cuenta propia                          |
| **Referencias de diseño** (solo US de UI)       | Figma, prototipos u otros enlaces aportados por el usuario                               | Sin ellas la historia no puede declararse Ready                                       |
| **Dependencias con otras US o sistemas**        | Indicadas por el usuario o inferibles del contexto                                       | Preguntar; afectan las dimensiones I y E de INVEST                                    |
| **ID de la US**                                 | Proporcionado por el usuario                                                             | Inferir el siguiente libre revisando carpetas `US-`* en `docs/specs/user-stories/`  |
| **Repositorios afectados**                      | Proporcionados por el usuario o inferibles del repo                                      | Sin ellos la historia no puede declararse Ready                                       |


> El único dato estrictamente obligatorio para crear la historia es tener identificado el actor y el valor de negocio. Si INVEST no es completamente valorable con la información disponible, la historia se crea con `Estado: Draft` y las lagunas documentadas en Observaciones. El estado **Ready** requiere todos los datos sin excepción.

---

## Flujo (resumen)

El procedimiento completo —cómo preguntar al usuario, validación antes de crear, los pasos de **Crear** y **Actualizar**, el checklist y los ejemplos/anti-patrones— está en [`references/flow.md`](references/flow.md). Síntesis:

- **Crear:** fijar ID y carpeta `US-XXX-[nombre-corto]/` → redactar el `README.md` con la plantilla (Descripción RFC 2119, Referencias, Criterios `AC-XXX` con categoría y enunciado RFC 2119, Repositorios, Complejidad Fibonacci, INVEST, DoR, Observaciones) → si el requerimiento define modelos, APIs o flujos, **delegar la documentación técnica a `/design-define` mediante subagente** y agregar las referencias devueltas a la sección Referencias → glosario si aplica → cierre.
- **Actualizar:** identificar y leer el `README.md` → aplicar cambios conservando ids `AC-XXX` (renumerar solo si se reordenan/eliminan) → revalidar → confirmar. Ante conflicto `TK-XXX` ↔ US, **la US prevalece**.
- **Cierre:** si queda **Draft**, cerrar lagunas con preguntas estructuradas (una por laguna, máx. tres por bloque); si queda **Ready**, sugerir como próximos pasos definir los casos de prueba (si el usuario acepta, invocar `/test-define`) y crear las `TK-XXX` con `/work-plan` (nunca crear TCs ni tareas directamente desde este skill).

Las modalidades **RFC 2119**, las **categorías de AC-XXX** (funcionales e ISO 25010) y las rúbricas **INVEST** y **DoR** detalladas están en [`references/quality-criteria.md`](references/quality-criteria.md).

---

## Criterios para `Estado: Ready` (resumen)

Promover a **Ready** solo si se cumplen todos; el detalle de cada criterio está en [`references/quality-criteria.md`](references/quality-criteria.md#definition-of-ready-dor).

- Sección **Criterios de aceptación** completa: al menos un `AC-XXX` con categoría entre paréntesis y enunciado RFC 2119 en MAYÚSCULAS.
- **DoR** completado según la plantilla (Dependencias listas, Inputs/outputs claros, Repositorios definidos, sin decisiones técnicas pendientes, Referencias de UI cuando aplique, sin aclaraciones pendientes).
- **INVEST** sin dimensiones en `No cumple`.
- **Repositorios afectados** identificados.
- **Observaciones** sin aclaraciones ni pendientes abiertos.

Si falta cualquiera, mantener `Estado: Draft` con las lagunas documentadas en Observaciones.
