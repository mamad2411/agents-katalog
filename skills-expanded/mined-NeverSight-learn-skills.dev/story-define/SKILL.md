---
name: story-define
description: Crear o actualizar una Historia de Usuario. Usar cuando se necesite crear, documentar, actualizar o estandarizar historias de usuario. Activar cuando el usuario solicite una nueva historia de usuario, describa una necesidad funcional, pida refinar requisitos, estructurar funcionalidades o alinear historias existentes a las convenciones del proyecto.
license: MIT
---

# Skill: Historia de usuario

Guía para **crear o actualizar** historias de usuario en el repo del producto.

> **Alcance de una US:** El `README.md` es un documento **funcional**. Registra el valor para el usuario, los **criterios de aceptación** (subsecciones *Reglas de negocio* con ids `BR-XX` y *Escenarios* con ids `SC-XX`) y el estado de avance. El detalle de implementación (DTOs, endpoints, esquemas) va en `docs/specs/technical-docs/` o en tareas `TK-XXX`, nunca en la narrativa de la historia. Los documentos técnicos **no son parte de la descripción funcional**; pueden referenciarse únicamente para justificar criterios de INVEST o condiciones del DoR.

La plantilla canónica está en `assets/user-story-template.md` (léela antes de escribir cualquier US).

## Subagente requerido

**Este skill debe ejecutarse bajo el agente/subagente `docs-specialist`** (`agents/docs-specialist.md`; en el proyecto destino instalar como `.cursor/agents/docs-specialist.md`). No ejecutar el flujo normativo de la US sin ese contexto.

---

## Cómo preguntar al usuario
 
Cuando este skill indique **preguntar, pedir, confirmar, validar o sugerir** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** que ofrezca el cliente (la que renderiza opciones tappables o un selector de respuesta) en lugar de redactar la pregunta como prosa libre. Reglas:
 
- **Opciones cortas y mutuamente excluyentes** (2–4 por pregunta) cuando la respuesta admita categorías; usar entrada libre solo si no hay forma razonable de enumerar opciones (p. ej. el texto del valor de negocio).
- **No repreguntar** lo que ya está respondido en el contexto, en `.agents/MEMORY.md` o en el `README.md` que se está editando.
- **Recopilación inicial (antes de redactar):** una sola tanda con hasta **tres preguntas por bloque**; agrupar huecos de información, no ir descubriendo turno a turno.
- **Confirmaciones de flujo (después de redactar o en cierre Draft):** **una pregunta por turno** cuando sea posible; si hay más de tres lagunas, encadenar tandas como en el paso 5 del flujo de creación.
- **Fallback**: si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3…).
Cada sección posterior que diga *preguntar al usuario*, *validar con el usuario* o *sugerir al usuario* asume este mecanismo; no se vuelve a repetir.

---

## Resolución de idioma

Orden canónico para el idioma de la US, criterios Gherkin, INVEST, DoR y texto natural del skill. Detenerse en el primer paso que aplique:

1. **`.agents/MEMORY.md`** (raíz del repo) → línea `preferred language: <ISO 639-1>` (p. ej. `es`, `en`). Si no existe esa línea pero hay claves legacy (`language:`, `idioma:`, `Project language:`), usarlas solo como fallback al leer MEMORY antiguo.
2. **Idioma del turno del usuario** (mensaje actual).
3. **Preguntar al usuario** qué idioma prefiere y persistir la respuesta en `.agents/MEMORY.md` con `preferred language: <código>`.

---

## Ubicación de archivos


| Artefacto             | Ruta                                                                                                                   |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Historia de usuario   | `docs/specs/user-stories/US-XXX-[nombre-corto]/README.md`                                                            |
| Archivos de apoyo     | `docs/specs/user-stories/US-XXX-[nombre-corto]/assets/`                                                              |
| Documentación técnica | `docs/specs/technical-docs/` (no parte de la descripción funcional; referenciable solo para justificar INVEST o DoR) |
| Glosario              | `docs/specs/glossary.md` (opcional)                                                                                  |


---

## Convenciones del nombre de carpeta

- Formato: `US-XXX-[nombre-corto]` con `US-XXX` en mayúsculas y número de 3 dígitos.
- Nombre corto: minúsculas, kebab-case, sin artículos ni palabras vacías.
- Ejemplos: `US-001-seleccion-item-sdp-desde-receta`, `US-004-resumen-costos-receta`.
- Archivos de apoyo en `assets/`; enlazarlos desde Referencias con rutas relativas, p. ej. `![Descripción](assets/nombre.png)`.

---

## Información requerida antes de redactar

Antes de crear o editar cualquier US, el agente debe tener clara la siguiente información. **No inventar nada** — si algún dato no es explícito, preguntar al usuario.


| Dato                                            | Cómo obtenerlo                                                                           | Si no está disponible                                                                 |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Actor y valor de negocio**                    | Del contexto o descripción del usuario                                                   | Preguntar al usuario                                                                  |
| **Criterios de aceptación (BR y SC)**           | Del contexto o descripción del usuario                                                   | Preguntar; sin al menos una `BR-XX` y un `SC-XX` INVEST no es valorable y la historia solo puede crearse en Draft |
| **Idioma de preferencia**                       | Ver [Resolución de idioma](#resolución-de-idioma) | Preguntar y persistir en `.agents/MEMORY.md` con `preferred language: <código>`        |
| **Referencias de diseño** (solo US de UI)       | Figma, prototipos u otros enlaces aportados por el usuario                               | Sin ellas la historia no puede declararse Ready                                       |
| **Dependencias con otras US o sistemas**        | Indicadas por el usuario o inferibles del contexto                                       | Preguntar; afectan las dimensiones I y E de INVEST                                    |
| **ID de la US**                                 | Proporcionado por el usuario                                                             | Inferir el siguiente libre revisando carpetas `US-`* en `docs/specs/user-stories/`  |
| **Unidades de trabajo**                         | Proporcionadas por el usuario o inferibles del repo                                      | Sin ellas la historia no puede declararse Ready                                       |


> El único dato estrictamente obligatorio para crear la historia es tener identificado el actor y el valor de negocio. Si INVEST no es completamente valorable con la información disponible, la historia se crea con `Estado: Draft` y las lagunas documentadas en Observaciones. El estado **Ready** requiere todos los datos sin excepción.

---

## Validación antes de crear

Antes de crear archivos, verificar las siguientes condiciones. Si alguna falla, **no crear** — informar al usuario y resolver primero.

**¿Qué verificar?**

- **Duplicado de ID:** si el usuario proporciona `US-XXX`, confirmar que esa carpeta no existe en `docs/specs/user-stories/`.
- **Solapamiento de alcance:** revisar los títulos y descripciones de otras US para detectar si el actor + valor + alcance ya está cubierto por una historia existente.
- **INVEST parcialmente valorable:** si la información recibida no permite valorar todas las dimensiones, la historia **sí puede crearse** pero con `Estado: Draft` y las lagunas documentadas en Observaciones. Solo es un bloqueante si el actor o el valor de negocio son completamente desconocidos.
**Si hay conflicto de ID o solapamiento de alcance:**

```
⚠️ No es posible crear la historia todavía:
- <razón concreta>
- [US-XXX: Título](docs/specs/user-stories/US-XXX-nombre/README.md) — <razón del solapamiento, si aplica>
```

Sugerir al usuario: (a) ajustar el alcance, (b) actualizar la US existente, o (c) proporcionar la información faltante.

---

## Flujo: Crear una historia nueva

1. **Fijar el ID y nombre de carpeta**
  - Usar el `US-XXX` indicado por el usuario o inferir el siguiente libre listando carpetas `US-*` en `docs/specs/user-stories/`.
  - Proponer el `nombre-corto` en kebab-case; validar con el usuario si hay ambigüedad.
  - Crear la carpeta `US-XXX-[nombre-corto]/` y `assets/` si habrá archivos vinculados.
2. **Escribir el `README.md`** usando `assets/user-story-template.md` como molde:
  - **Descripción:** Como/Quiero/Para con modalidad normativa RFC 2119 (ver [Notas — RFC 2119](#rfc-2119)) en el idioma de preferencia.
  - **Referencias:** enlaces de diseño y archivos en `assets/`; los archivos aportados no deben quedar solo en el chat.
  - **Criterios de aceptación** (sección con dos subsecciones; ids solo `BR-XX` y `SC-XX`):
    - **Reglas de negocio:** cada regla con id secuencial **BR-01**, **BR-02**, … y palabra clave normativa en MAYÚSCULAS (**DEBE**, **NO DEBE**, **DEBERÍA**, etc.). Los ids son únicos en el ámbito de la US; renumerar si se reordenan o eliminan reglas.
    - **Escenarios:** cada escenario con id secuencial **SC-01**, **SC-02**, … en la línea `Escenario: SC-XX - <nombre>`. Redactar en formato Gherkin con la palabra clave de cada paso en **TODO MAYÚSCULAS** en el idioma de preferencia (**DADO / CUANDO / ENTONCES / Y / PERO** en español; **GIVEN / WHEN / THEN / AND / BUT** en inglés). Los escenarios no deben contradecir ninguna obligación (**DEBE**) ni prohibición (**NO DEBE**) de las reglas de negocio.
  - **Unidades de trabajo:** al nivel de granularidad del repo (p. ej. `frontend`, `backend`, o `micro-autenticacion`, `micro-catalogo`).
  - **Complejidad sugerida:** story points solo en valores Fibonacci 1, 2, 3, 5, 8, 13 con justificación breve de alcance, riesgo e incertidumbre.
  - **Validación — INVEST:** tabla con las seis dimensiones (I, N, V, E, S, T); valor de cada una: `Cumple` / `No cumple` / `Parcial` con nota. Si alguna dimensión falla, documentarlo sin disimular.
  - **Validación — Definition of Ready (DoR):** tabla con los seis criterios de la plantilla. Para cada uno: `Cumple` / `No cumple` / `Parcial` (el criterio **Referencias de UI** admite además `No aplica`). Ver criterios exactos en el checklist de Ready.
  - **Observaciones:** (1) prerrequisitos o dependencias aún no listas; (2) datos o aclaraciones pendientes del usuario o producto; (3) decisiones pendientes; (4) otras notas. Si no hay nada que reportar en algún ítem, dejarlo vacío.
3. **Documentación técnica** (solo si el usuario la pide explícitamente)
  - Crear o actualizar documentos en `docs/specs/technical-docs/`.
  - **No integrarla en la descripción funcional** de la US. Solo puede referenciarse desde las secciones INVEST u Observaciones del DoR para justificar complejidad, dependencias o restricciones técnicas que condicionan algún criterio (p. ej. *«Ver `technical-docs/contrato-api.md` — justifica la estimación de la dimensión E»*).
4. **Glosario** (si aplica)
  - Si aparecen términos de dominio nuevos, crear o reutilizar entrada en `docs/specs/glossary.md` con definición breve en contexto producto/dominio.
5. **Cierre**
  - Si la US queda en **Draft**, identificar las lagunas documentadas en Observaciones (datos faltantes, dependencias sin confirmar, dimensiones de INVEST en `Parcial` o `No cumple`, criterios del DoR sin satisfacer) y ofrecer al usuario, mediante la **herramienta de preguntas estructuradas**, las preguntas concretas que cerrarían cada laguna. Reglas:
    - Una pregunta por laguna, con opciones cuando la respuesta admita categorías (idioma, formato, prioridad, dependencias enumerables, story points Fibonacci); entrada libre solo para campos narrativos (refinamiento del valor, reglas nuevas, criterios verificables).
    - Respetar el máximo de tres preguntas por bloque; si hay más lagunas, encadenar tandas hasta agotarlas o hasta que el usuario indique que prefiere mantener el resto como Draft.
    - Tras recibir respuestas, actualizar las secciones afectadas del `README.md`, revalidar los checklists de INVEST y DoR, y promover a `Estado: Ready` solo si quedan completos. Si alguna laguna sigue abierta, mantener `Draft` y reflejar el residual en Observaciones.
  - Si la US queda en **Ready**, sugerir explícitamente al usuario que ejecute `/story-plan` para crear las tareas `TK-XXX`.
  - Si el usuario pide crearlas en continuidad o en el mismo turno: **invocar `/story-plan` obligatoriamente**; no crear tareas directamente desde este skill. El conocimiento y las reglas de formato de los `TK-XXX` residen en ese skill.

---

## Flujo: Actualizar una historia existente
 
1. **Identificar el archivo** — por ID, nombre-corto o título.
2. **Leer el `README.md` actual** completo antes de editar.
3. **Aplicar los cambios** solicitados por el usuario. Reglas invariantes:
  - Si el cambio afecta reglas de negocio: mantener los ids `BR-XX` existentes; renumerar solo si se reordenan o eliminan reglas.
  - Si el cambio afecta escenarios: mantener los ids `SC-XX` existentes; renumerar solo si se reordenan o eliminan escenarios.
  - Si hay conflicto entre el texto de un `TK-XXX` y el `README.md` de la US: **la US prevalece**. Corregir las tareas, no la historia.
  - Si el usuario cambia el estado a **Ready**: verificar todas las condiciones del checklist de Ready antes de guardar.
4. **Criterios de aceptación:** si se añaden o modifican, aplicar las mismas reglas de formato del flujo de creación (paso 2).
5. **Si la US queda en `Estado: Draft`** tras los cambios (sea porque ya lo estaba, sea porque los cambios la degradaron desde Ready), ofrecer al usuario las preguntas que cerrarían las lagunas residuales mediante la **herramienta de preguntas estructuradas**, aplicando las mismas reglas del paso 5 del flujo de creación (una pregunta por laguna, opciones cuando la respuesta admita categorías, máximo tres por bloque, encadenar tandas si hace falta). Si las respuestas completan los checklists de INVEST y DoR, promover a `Estado: Ready`. Si el usuario prefiere mantener Draft o salta preguntas, respetarlo y reflejar el residual en Observaciones.
6. **Confirmar** mostrando las secciones modificadas.

---

## Checklist antes de redactar

**Información:**

- Actor y valor de negocio claros
- Reglas de negocio con suficiente detalle para valorar INVEST
- Idioma de preferencia determinado y `.agents/MEMORY.md` actualizado si fue necesario
- Si es US de UI: referencias de diseño presentes o acordadas
- Dependencias con otras US o sistemas identificadas
**Validación:**
- ID `US-XXX` sin carpeta existente (creación) o carpeta identificada (actualización)
- Sin solapamiento de alcance con US existentes
- Actor y valor de negocio identificados (mínimo para crear); si INVEST no es completamente valorable → `Estado: Draft` con lagunas en Observaciones
**Condiciones para `Estado: Ready`:**
- Sección **Criterios de aceptación** completa: al menos una `BR-XX` y un `SC-XX`; escenarios en Gherkin con palabras clave en MAYÚSCULAS y en el idioma de preferencia del documento
- DoR completado según la plantilla
- Unidades de trabajo identificadas
- Observaciones sin aclaraciones ni pendientes abiertos
**Formato:**
- Plantilla `assets/user-story-template.md` leída
- Reglas de negocio con identificadores `BR-01`, `BR-02`, … sin saltos; escenarios con `SC-01`, `SC-02`, … sin saltos
- Palabras clave normativas en MAYÚSCULAS en el idioma de preferencia (DEBE, NO DEBE, DEBERÍA…)
- Archivos del usuario guardados en `assets/` y enlazados con ruta relativa
- Detalle técnico en `technical-docs/` o `TK-XXX`, no en el `README.md`

---

## Ejemplos

**Ejemplo 1 — Entrada mínima viable**

- *Entrada:* «US nueva: como farmacéutico quiero ver alertas de interacción al añadir un medicamento a la receta, para evitar recetas inseguras. Reglas: mostrar alerta antes de guardar; permitir continuar con justificación.»
- *Salida:* Carpeta `US-0XX-alertas-interaccion-receta/` con `README.md` completo (Como/Quiero/Para, BR-01 y BR-02 con modalidad RFC 2119, SC-01 y SC-02 en Gherkin con caso feliz y excepción, INVEST y DoR completados, story points con justificación).

**Ejemplo 2 — Falta información**

- *Entrada:* «Historia de exportar informes.»
- *Comportamiento:* El agente no crea carpetas; lanza una tanda de preguntas mediante la **herramienta de preguntas estructuradas** (quién exporta, formatos admitidos, permisos, qué se entiende por "informe", criterios verificables) con opciones cuando aplique. Solo procede a redactar cuando puede valorar INVEST y escribir Gherkin.

**Ejemplo 3 — Historia con UI**

- *Entrada:* Historia con enlace a Figma y capturas en `assets/`.
- *Salida:* `README.md` con sección Referencias completa; fila Referencias de UI en DoR en `Cumple` o `Parcial` con notas; `Estado: Ready` solo si Gherkin y DoR lo permiten.

**Ejemplo 4 — Ready y tareas**

- *Entrada:* Historia cerrada en Ready; el usuario dice: «crea las tareas para implementarla».
- *Salida:* El agente no crea tareas directamente; invoca `/story-plan` pasando el contexto de la US. Toda la lógica de creación de `TK-XXX` (stubs, plantilla, work-units) es responsabilidad de ese skill.

**Ejemplo 5 — Draft con cierre asistido**

- *Entrada:* «US nueva: como analista quiero descargar el reporte mensual de ventas en CSV para procesarlo localmente.» Hay actor y valor, pero no se conocen story points, dependencias ni si existen referencias de UI.
- *Comportamiento:* El agente crea `US-0XX-descarga-reporte-mensual-csv/` con `Estado: Draft`, documenta las lagunas en Observaciones, y en el cierre lanza una tanda de preguntas estructuradas:
  - "¿Story points (Fibonacci)?" → opciones `1` / `2` / `3` / `5` (con `8`/`13` accesibles si pide más).
  - "¿Hay dependencias con otra US o sistema?" → opciones `Ninguna` / `Otra US del backlog` / `Sistema externo`.
  - "¿La historia involucra UI propia?" → opciones `Sí, tengo Figma` / `Sí, sin referencias aún` / `No, solo backend`.
- *Resultado:* Con las respuestas, el agente actualiza el `README.md`, revalida INVEST y DoR, y promueve a `Estado: Ready` si los checklists quedan completos. Si el usuario salta una pregunta o queda residual, la US permanece en Draft con la nota correspondiente.

---

## Anti-patterns

- Inventar reglas de negocio o exclusiones que el usuario no dio.
- Poner detalle técnico (clases, endpoints, esquemas) en el `README.md` en lugar de remitirlo a `technical-docs/` o `TK-XXX`.
- Declarar `Estado: Ready` sin Criterios de aceptación completo o sin referencias de diseño cuando la historia involucra UI.
- Declarar `Estado: Ready` con Observaciones que aún listen aclaraciones o pendientes sin resolver.
- Resolver un conflicto entre `TK-XXX` y el `README.md` de la US degradando la US; la US prevalece.
- Crear tareas `TK-XXX` directamente desde este skill sin invocar `/story-plan`; la creación de tareas siempre se delega a ese skill.
- Copiar `assets/user-story-template.md` al repo del producto como artefacto en lugar de usarlo como molde.
- Lanzar preguntas al usuario como prosa libre cuando el cliente expone una herramienta de preguntas estructuradas; o ir descubriendo huecos turno a turno en lugar de agrupar todas las preguntas pendientes en una sola tanda al inicio.

---

## Notas

### Handoffs del ciclo

Posición: **inicio** del pipeline `story-define` → `story-plan` → `story-implement` → `story-integrate`.

| | |
|--|--|
| **Entrada** | Necesidad funcional del usuario. No requiere US previa. |
| **Salida mínima (creación)** | Carpeta `US-XXX-[nombre-corto]/README.md` con actor y valor de negocio; puede quedar en `Estado: Draft` con lagunas en Observaciones. |
| **Salida para continuar** | `Estado: Ready` en el `README.md`; INVEST y DoR completos; al menos un `BR-XX` y un `SC-XX`; Observaciones sin pendientes abiertos. |
| **Siguiente paso** | **`story-plan`** — invocar `/story-plan` (o continuidad explícita del usuario). No crear `TK-XXX` desde este skill. |
| **Si queda en Draft** | No handoff a plan ni implement. Cerrar lagunas con preguntas estructuradas o mantener Draft documentado. |
| **Regreso desde plan** | Conflicto US ↔ TK detectado en `story-plan` → actualizar la US aquí; `story-plan` corrige el TK. La US prevalece sobre el TK. |
| **Regreso desde integrate** | Alcance reducido o `progress.md` incompleto detectado en `story-integrate` → ajustar la US aquí y alinear TKs con `story-plan` antes de reintentar el merge. |

### RFC 2119

Tabla de equivalencias para palabras clave normativas (en MAYÚSCULAS en el idioma de preferencia):


| Nivel (semántica RFC 2119) | Inglés (`en`)                | Español (`es`)                          |
| -------------------------- | ---------------------------- | --------------------------------------- |
| Obligación absoluta        | **MUST** / **REQUIRED**      | **DEBE** / **ES OBLIGATORIO**           |
| Prohibición absoluta       | **MUST NOT** / **SHALL NOT** | **NO DEBE** / **ESTÁ PROHIBIDO**        |
| Recomendación fuerte       | **SHOULD** / **RECOMMENDED** | **DEBERÍA** / **ES RECOMENDABLE**       |
| Desaconsejado salvo causa  | **SHOULD NOT**               | **NO DEBERÍA** / **NO ES RECOMENDABLE** |
| Permiso u opcionalidad     | **MAY** / **OPTIONAL**       | **PUEDE** / **OPCIONAL**                |


Elegir una forma por nivel y mantenerla consistente en toda la US. Si el usuario pide no usar RFC 2119, documentarlo en Observaciones; el formato Gherkin en MAYÚSCULAS se mantiene salvo petición explícita en contra.