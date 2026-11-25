---
name: story-plan
description: Crea o actualiza tareas técnicas (TK-XXX) asociadas a una historia de usuario existente. Activar cuando el usuario solicite planificar implementación, descomponer trabajo, definir alcance técnico, estructurar subtareas o documentar especificaciones técnicas sin generar código ni pruebas. Activar también — por defecto — cuando el usuario solo entregue una referencia a una historia (p. ej. «US-004», «planifica US-007», «tareas para esta historia») — en ese caso el propósito es proponer stubs agrupados por unidad de trabajo que cubran los escenarios (SC-XX) y consideren las reglas de negocio (BR-XX) de la US, sin redactar TKs completas.
license: MIT
---

# Skill: Planificar tarea de historia de usuario
 
Guía para **crear o actualizar** tareas `TK-XXX` bajo una historia de usuario existente.
 
> **Alcance de un TK:** La tarea es un documento de **especificación técnica**. Describe qué lograr, cómo implementarlo y sus dependencias dentro de la unidad de trabajo. No implementa código, no ejecuta pruebas, no crea ADRs. Lo que no está acordado va en **Observaciones** o se pregunta al usuario — nunca se inventa.
 
La plantilla canónica está en `assets/task-template.md` (léela antes de escribir cualquier TK).
 
---
 
## Subagente requerido
 
**Este skill debe ejecutarse bajo el agente/subagente `docs-specialist`** (`agents/docs-specialist.md`; en el proyecto destino instalar como `.cursor/agents/docs-specialist.md`). No ejecutar el flujo normativo de TK sin ese contexto.
 
---

## Cómo preguntar al usuario

Cuando este skill indique **preguntar, pedir, confirmar, validar o sugerir** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** que ofrezca el cliente (la que renderiza opciones tappables o un selector de respuesta) en lugar de redactar la pregunta como prosa libre. Reglas:

- **Opciones cortas y mutuamente excluyentes** (2–4 por pregunta) cuando la respuesta admita categorías; usar entrada libre solo si no hay forma razonable de enumerar opciones (p. ej. el objetivo breve de un stub).
- **No repreguntar** lo que ya está respondido en el contexto, en `.agents/MEMORY.md`, en el `README.md` de la US o en las `TK-*.md` existentes de su carpeta.
- **Recopilación inicial (modo A, antes de redactar):** una sola tanda con hasta **tres preguntas por bloque**; no ir descubriendo huecos turno a turno.
- **Modo B — confirmación de stubs (paso 6):** **una pregunta por turno** con opciones `Confirmar stubs` / `Ajustar alcance` / `Cancelar`; no crear archivos antes de confirmación.
- **Fallback**: si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3…).

Cada sección posterior que diga *preguntar al usuario*, *validar con el usuario*, *confirmar* o *sugerir al usuario* asume este mecanismo; no se vuelve a repetir.

---

## Resolución de idioma

Orden canónico compartido con el resto del ciclo de historias. Detenerse en el primer paso que aplique:

1. **`.agents/MEMORY.md`** (raíz del repo) → línea `preferred language: <ISO 639-1>` (p. ej. `es`, `en`). Si no existe esa línea pero hay claves legacy (`language:`, `idioma:`, `Project language:`), usarlas solo como fallback al leer MEMORY antiguo.
2. **Idioma del turno del usuario** (mensaje actual).
3. **Preguntar al usuario** qué idioma prefiere y persistir la respuesta en `.agents/MEMORY.md` con `preferred language: <código>`.

---

## Modos de invocación

El skill reconoce **dos modos** según lo que entregue el usuario. El modo determina el flujo a aplicar.

| Modo | Disparador | Flujo a aplicar |
|------|------------|-----------------|
| **A. Tarea específica** | El usuario describe una tarea concreta (objetivo, unidad, alcance) o pide editar una `TK-XXX` existente. | *Flujo: Crear stub*, *Flujo: Crear TK completa* o *Flujo: Actualizar una TK existente* según corresponda. |
| **B. Stubs desde US** | El usuario entrega **solo una referencia a una historia** (p. ej. «US-004», «crea las tareas para US-007», «planifica esta historia») sin describir tareas específicas. | *Flujo: Sugerir stubs desde una US* — propósito por defecto: proponer un conjunto de stubs agrupados por unidad de trabajo que cubra los SC y considere las BR de la US. |

En caso de duda entre A y B: preguntar al usuario antes de continuar. No combinar ambos modos en una misma ejecución.

---
 
## Ubicación de archivos
 
| Artefacto | Ruta |
|-----------|------|
| Tarea | `docs/specs/user-stories/US-XXX-[nombre-corto]/TK-XXX-[kebab-case].md` |
| Unidades de trabajo | `docs/specs/work-units.md` |
| ADR | `docs/adr/` |
| Documentación técnica | `docs/specs/technical-docs/` |
| Glosario | `docs/specs/glossary.md` |
 
---
 
## Convenciones del nombre de archivo
 
- Formato: `TK-XXX-[nombre-descriptivo].md` con `TK-XXX` en mayúsculas.
- `XXX`: número secuencial **por historia** (no global); tres dígitos con cero a la izquierda.
- Nombre descriptivo: minúsculas, kebab-case, corto y descriptivo.
- Ejemplos: `TK-001-modelo-dominio-receta.md`, `TK-002-endpoint-crear-receta.md`.
---
 
## Información requerida antes de redactar
 
Antes de crear o editar cualquier TK, el agente debe tener clara la siguiente información. **No inventar nada** — si algún dato no es explícito, preguntar al usuario.
 
| Dato | Cómo obtenerlo | Si no está disponible |
|------|----------------|-----------------------|
| **US padre** | Indicada por el usuario | Sin `README.md` de US existente no se puede crear el TK |
| **Modo de invocación** | Inferir del mensaje: ¿tarea específica (A) o solo referencia a US (B)? | Si es ambiguo, preguntar al usuario |
| **Intención** (solo modo A) | Del mensaje del usuario | Preguntar: ¿solo anclaje (stub) o TK completa lista para Ready? |
| **Objetivo del TK** (solo modo A) | Del mensaje del usuario | Para stub: basta un objetivo breve. Para TK completa: preguntar hasta tener contexto suficiente |
| **BR y SC de la US** (solo modo B) | Leer la sección **Criterios de aceptación** del `README.md` de la US padre (subsecciones *Reglas de negocio* y *Escenarios*) | Si faltan BR-XX o SC-XX explícitos: bloquear modo B y reportar — no crear stubs |
| **Unidad de trabajo** | Inferir del repo o indicada por el usuario | Stub: puede quedar `Por definir`. TK completa: obligatoria; sin ella el estado no puede ser `Ready` |
| **Contexto técnico** (solo TK completa) | ADRs existentes, technical-docs, descripción del usuario | Si falta decisión técnica relevante: sugerir ADR al usuario, no crearlo |
| **Referencia de UI** (solo TK de interfaz) | Figma, wireframe o imagen de alta fidelidad aportados por el usuario | Obligatoria para `Ready`; sin ella el TK de UI no puede salir de `Draft` |
| **Idioma de preferencia** | Ver [Resolución de idioma](#resolución-de-idioma) | Preguntar y persistir en `.agents/MEMORY.md` con `preferred language: <código>` |
 
> Leer siempre el `README.md` de la US y **todas** las `TK-*.md` existentes en la carpeta antes de crear o editar cualquier tarea. Detectar solapamientos y resolverlos con el usuario antes de continuar.
 
---
 
## Validación antes de crear
 
Antes de crear archivos, verificar las siguientes condiciones. Si alguna falla, **no crear** — informar al usuario y resolver primero.
 
**¿Qué verificar?**
- **US padre existe y está Ready:** la carpeta `US-XXX-[nombre-corto]/` tiene `README.md` con `Estado: Ready`. No se pueden crear TKs sobre una US en Draft.
- **ID disponible:** el número `TK-XXX` propuesto no existe ya en la carpeta.
- **Solapamiento de alcance:** leer todas las `TK-*.md` de la carpeta de la US padre y comparar su objetivo con el de la nueva tarea. Si alguna ya cubre el mismo alcance: informar al usuario indicando cuál es el conflicto y preguntar si prefiere actualizar la existente o ajustar el alcance de la nueva.
- **Unidad definida (solo TK completa):** si la unidad sigue siendo `Por definir` tras preguntar, publicar como stub en Draft, no como TK completa.
**Si hay conflicto:**
```
⚠️ No es posible crear la tarea todavía:
- <razón concreta>
- [TK-XXX: Título](TK-XXX-nombre.md) — <razón del solapamiento, si aplica>
```
 
---
 
## Flujo: Crear stub (anclaje de ID)
 
Un stub reserva el ID y el vínculo a la US. No requiere contexto técnico completo.
 
1. Inferir el siguiente `TK-XXX` libre listando archivos `TK-*.md` en la carpeta de la US.
2. Crear `TK-XXX-[nombre-descriptivo].md` con:
   - `Estado: Draft`
   - `Historia`: enlace a la US `[US-XXX](./README.md)`.
   - `Unidad de trabajo`: la conocida o `Por definir`.
   - `Asignado a`: indicado por el usuario; si no, inferir con `git config user.name`; omitir la línea si no aplica.
   - **Descripción**: objetivo breve acordado — el *qué*, sin el cómo.
   - **Plan de implementación**: vacío o ausente si no hay pasos definidos.
   - **Observaciones**: pendientes reales; no rellenar con texto genérico.
3. Actualizar `work-units.md` **solo si** la unidad del stub no es `Por definir` (ver paso 2 del flujo de TK completa).
4. **Parar aquí.** No continuar con los pasos de TK completa.
5. **Handoff:** stub en `Draft` — completar a `Ready` con *Flujo: Crear TK completa* (modo A) antes de **`story-implement`**.
---
 
## Flujo: Crear TK completa
 
Una TK completa puede alcanzar `Estado: Ready` si cumple todas las condiciones del checklist.
 
1. **Inferir el siguiente `TK-XXX`** libre en la carpeta de la US.
2. **Gestionar `work-units.md`:**
   - Crear desde `assets/work-units-template.md` si el archivo no existe.
   - Si la unidad es nueva: añadir sección `## <nombre-unidad>` con párrafo de alcance. Si el alcance no está claro, preguntar antes de añadirla.
   - No listar TKs, DTOs ni technical-docs dentro de `work-units.md`; solo nombre de unidad y párrafo de alcance.
3. **Redactar el TK** siguiendo `assets/task-template.md`:
   - **Metadatos**: `Historia` con enlace `[US-XXX](./README.md)`; `Asignado a` indicado por el usuario, o inferido con `git config user.name`, u omitido si no aplica.
   - **Descripción**: qué lograr — objetivo claro, tono imperativo y verificable; sin «podría», «quizá», «tal vez».
   - **Dependencias**: solo piezas *dentro de la unidad de trabajo* — componentes, servicios, modelos, librerías. No incluir aquí ADRs, technical-docs, contratos ni referencias de diseño; esos van exclusivamente en **Referencias**.
   - **Referencias**: ADRs existentes, technical-docs, diseño. No crear ADRs; si falta una decisión, sugerirlo al usuario en Observaciones.
   - **Plan de implementación**: pasos concretos acordados o derivados de fuentes citadas en Referencias. Si los pasos no se conocen aún, **no inventar** — indicar en Observaciones qué información falta para poder redactarlos.
   - **Observaciones**: solo si hay pendientes reales (prerrequisitos no cumplidos, información pendiente, decisiones por tomar). Si no hay nada pendiente, **omitir la sección**. Si el equipo lo exige, una línea *Sin pendientes documentados*. Con pendientes reales: `Estado: Draft`.
4. **Actualizar** technical-docs y glossary si aplica (entradas breves; glossary no es sustituto de ADR ni technical-doc).
5. **Verificar el checklist** antes de asignar `Estado: Ready`.
6. **Handoff:** si todas las TK del alcance acordado están `Ready`, sugerir **`story-implement`**. Si otras TK siguen en `Draft`, listar cuáles completar antes de implementar.
---
 
## Flujo: Actualizar una TK existente
 
1. **Identificar el archivo** — por número, nombre o título.
2. **Leer el contenido actual** completo antes de editar.
3. **Leer el `README.md` de la US y las demás TKs** para detectar solapamientos con los cambios propuestos.
4. **Aplicar los cambios** solicitados por el usuario. Reglas invariantes:
   - Si hay conflicto entre el TK y el `README.md` de la US: **la US prevalece**. Corregir el TK, no la historia.
   - Si el usuario cambia el estado a **Ready**: verificar todas las condiciones del checklist antes de guardar.
   - Si se añaden pasos al Plan: mantener tono imperativo y verificable; sin supuestos no acordados.
5. **Confirmar** mostrando las secciones modificadas.
---
 
## Flujo: Sugerir stubs desde una US
 
Aplica cuando el input es **solo una referencia a una historia** (modo B). El propósito es proponer un conjunto coherente de stubs que cubra los SC y considere las BR, sin redactar TKs completas.
 
**Precondiciones de bloqueo** — si alguna falla, **no crear archivos** e informar al usuario indicando la condición incumplida:
- La carpeta `US-XXX-[nombre-corto]/` existe y su `README.md` tiene `Estado: Ready`.
- El `README.md` contiene la sección **Criterios de aceptación** con al menos **una regla de negocio** (`BR-XX`) en la subsección *Reglas de negocio*.
- El mismo bloque contiene al menos **un escenario** (`SC-XX`) en la subsección *Escenarios*.
 
**Pasos:**
 
1. **Leer el `README.md` de la US completo** y todas las `TK-*.md` existentes en su carpeta.
2. **Verificar las precondiciones de bloqueo.** Si alguna falla, no continuar: reportar al usuario qué falta y sugerir el skill correspondiente (`story-define` para alinear la US, etc.).
3. **Identificar unidades de trabajo** a partir del alcance de la US, los SC y las BR. Una unidad puede ser un módulo, servicio, paquete, componente UI, etc. **No inventar** unidades no soportadas por la US; lo no claro queda `Por definir` o se pregunta.
4. **Cubrir los SC y considerar las BR.** Asegurar que cada `SC-XX` queda cubierto por al menos un stub propuesto. Las `BR-XX` se consideran como restricciones que condicionan el alcance de los stubs (validaciones, invariantes, autorizaciones); no se replican literalmente en el TK.
5. **Presentar la propuesta de stubs** al usuario, agrupada por unidad de trabajo. Por cada stub incluir: `TK-XXX` tentativo (siguiente libre en secuencia), nombre de archivo, unidad de trabajo (o `Por definir`), objetivo breve y qué `SC-XX` cubre. No es 1 stub por SC: varios SC pueden caer en un mismo stub si comparten unidad y alcance; un SC amplio puede dividirse si abarca varias unidades. **No crear archivos en este turno** — dejar explícito al final del mensaje.
6. **Confirmar con el usuario** mediante la herramienta de preguntas estructuradas: `Confirmar stubs` / `Ajustar alcance` / `Cancelar`. Si elige ajustar, revisar la propuesta y repetir pasos 5–6. **No continuar sin confirmación explícita**, salvo que el mensaje inicial ya describiera la descomposición con detalle suficiente para considerarla aprobada.
7. **Crear cada stub** de la propuesta confirmada siguiendo el *Flujo: Crear stub* (Estado: Draft, descripción breve sin referenciar identificadores `SC-XX` / `BR-XX` en el documento, plan vacío).
8. **Reportar al usuario** la lista de stubs creados, agrupados por unidad de trabajo, indicando brevemente qué `SC-XX` cubre cada uno.
9. **Handoff:** si los stubs quedaron en `Draft`, indicar al usuario que debe completar cada TK a `Estado: Ready` con **`story-plan`** (modo A) antes de invocar **`story-implement`**. No sugerir implementación mientras las TK del alcance sigan en Draft.
 
**Reglas invariantes:**
- No redactar Plan de implementación, ni Dependencias detalladas, ni Referencias técnicas: son **stubs**, no TKs completas.
- No incluir identificadores `SC-XX` / `BR-XX` dentro de los archivos `TK-XXX.md`. La consideración es del agente, no del documento.
- **No crear archivos `TK-*.md` antes de la confirmación del paso 6.** La traza SC/BR → stub vive en la propuesta (paso 5) y en el reporte (paso 8), no dentro de los archivos.
- Si la US es ambigua respecto a unidades de trabajo: preguntar al usuario antes de crear stubs; no inferir unidades por cuenta propia.
- Si dos stubs se solapan: consolidarlos en la propuesta (paso 5) o preguntar al usuario antes de confirmar.
---
 
## Checklist antes de redactar
 
**Información:**
- [ ] `README.md` de la US leído
- [ ] Todas las `TK-*.md` de la carpeta leídas; solapamientos resueltos
- [ ] Modo de invocación identificado (A o B)
- [ ] Modo A: intención clara: stub vs TK completa
- [ ] Modo B: BR-XX y SC-XX identificados en **Criterios de aceptación** del `README.md`; US en `Estado: Ready`
- [ ] Modo B: propuesta presentada al usuario (paso 5) sin archivos creados
- [ ] Modo B: confirmación estructurada recibida (paso 6) antes del primer `TK-*.md`
- [ ] Idioma de preferencia determinado y `.agents/MEMORY.md` actualizado si fue necesario
**Validación:**
- [ ] Carpeta de la US existe con `README.md`
- [ ] ID `TK-XXX` libre en la carpeta
- [ ] Sin solapamiento de alcance con TKs existentes
**Condiciones para `Estado: Ready`:**
- [ ] Unidad de trabajo definida (no `Por definir`) y sección en `work-units.md`
- [ ] **Descripción** con objetivo claro y verificable
- [ ] Si es TK de UI: referencia a Figma, wireframe o imagen de alta fidelidad presente en **Referencias**
- [ ] **Dependencias** listadas dentro del alcance de la unidad
- [ ] **Plan de implementación** con pasos concretos
- [ ] **Observaciones** sin pendientes abiertos — sección omitida o con *Sin pendientes documentados*
- [ ] Referencias a ADRs y technical-docs con rutas relativas válidas
**Formato:**
- [ ] Plantilla `assets/task-template.md` leída
- [ ] Nombre de archivo en kebab-case, secuencial por historia
- [ ] Sin código de aplicación en el archivo
- [ ] Sin párrafos instructivos de plantilla en el TK publicado
---
 
## Ejemplos
 
**Ejemplo 1 — Stub**
 
- *Entrada:* «Solo quiero reservar TK-003, sin diseño técnico todavía.»
- *Salida:* `TK-003-[nombre-corto].md` en Draft, unidad `Por definir`, descripción mínima del objetivo, Plan vacío, Observaciones con los pendientes reales. `work-units.md` sin cambios.

**Ejemplo 2 — TK completa**
 
- *Entrada:* «TK para el diálogo de selección de ítem usando Material; la US tiene criterios; el ADR de UI está en `docs/adr/`.»
- *Salida:* TK con unidad concreta, Plan con pasos verificables, referencias al ADR con ruta relativa, `work-units.md` actualizado si la unidad es nueva. `Estado: Ready` si Observaciones está limpia; `Draft` si quedan pendientes.

**Ejemplo 3 — Información incompleta**
 
- *Entrada:* «TK-005 para la API Z.»
- *Comportamiento:* El agente identifica que faltan contratos, endpoints y DTOs para redactar una TK completa. Pregunta al usuario antes de continuar. Si el usuario solo quiere reservar el ID: crea un stub en Draft. No redacta TK completa con supuestos.

**Ejemplo 4 — Stubs desde una US (modo B)**
 
- *Entrada:* «Crea las tareas necesarias para implementar US-004.» (sin describir tareas específicas).
- *Comportamiento — turno 1:* El agente activa el *Flujo: Sugerir stubs desde una US*. Verifica que `US-004/README.md` está en `Ready` y contiene BR y SC en **Criterios de aceptación**. Lee la US completa, identifica unidades de trabajo, y presenta la propuesta agrupada por unidad (paso 5) con `TK-XXX` tentativo, nombre de archivo, objetivo breve y cobertura de SC por stub. Pregunta con opciones `Confirmar stubs` / `Ajustar alcance` / `Cancelar`. **No crea archivos.**
- *Comportamiento — turno 2:* Tras confirmación, crea cada stub en `Estado: Draft` sin referencias a `SC-XX` / `BR-XX` en el archivo (paso 7) y reporta rutas creadas con cobertura SC (paso 8).
- *Salida:* Stubs `TK-001-...md` a `TK-NNN-...md` en Draft; `work-units.md` actualizado solo si alguna unidad es nueva y su alcance está claro. Handoff: completar cada TK a `Ready` con `story-plan` antes de `/story-implement`.
 
**Ejemplo 5 — US no Ready o sin BR/SC**
 
- *Entrada:* «Tareas para US-009.» — pero `US-009/README.md` está en `Draft` o no tiene SC documentados en **Criterios de aceptación**.
- *Comportamiento:* El agente bloquea, no crea ningún stub. Reporta al usuario qué falta (estado, BR, SC) y sugiere usar `story-define` para alinear la US antes de planificar tareas.
---
 
## Anti-patterns
 
- Implementar features, migraciones o tests mientras se redacta el TK.
- Crear ADRs sin pedido explícito del usuario; solo referenciar existentes o sugerir su creación.
- Publicar `Estado: Ready` en un stub sin criterios ni contexto técnico.
- Publicar `Estado: Ready` con pendientes en Observaciones.
- Ignorar las TKs existentes en la carpeta; duplicar o contradecir su alcance.
- Meter listas de TKs, DTOs o technical-docs largos en `work-units.md`.
- Inventar flujos, entidades o integraciones en lugar de preguntar.
- Usar `glossary.md` como especificación técnica o sustituto de ADR.
- Rellenar secciones con supuestos o ejemplos genéricos; dejar pendientes reales sin listar en Observaciones.
- Narrar el trabajo realizado en el mensaje al usuario («leí la US», «creé el TK», «actualicé work-units»); solo reportar resultados y pendientes.
- **Modo B**: crear stubs desde una US en `Draft`, o sin `BR-XX` / `SC-XX` explícitos en **Criterios de aceptación** de su `README.md` — debe bloquear y reportar.
- **Modo B**: incluir identificadores `SC-XX` / `BR-XX` dentro del archivo `TK-XXX.md`; la cobertura se reporta al usuario, no se documenta en el TK.
- **Modo B**: forzar un mapeo 1 stub = 1 SC; los stubs se agrupan por unidad de trabajo, no por escenario.
- **Modo B**: redactar Plan de implementación, Dependencias o Referencias detalladas en stubs propuestos desde una US — son stubs, no TKs completas.
- **Modo B**: crear stubs sin haber presentado la propuesta (paso 5) y recibido confirmación (paso 6).
- Lanzar preguntas al usuario como prosa libre cuando el cliente expone una herramienta de preguntas estructuradas; o ir descubriendo huecos turno a turno en lugar de agrupar las preguntas pendientes en una sola tanda al inicio.
---
 
## Notas

### Handoffs del ciclo

Posición: **planificación** — entre `story-define` e `story-implement`.

| | |
|--|--|
| **Entrada** | US con `Estado: Ready` y **Criterios de aceptación** (`BR-XX`, `SC-XX`) en su `README.md`. Si la US está en Draft o faltan BR/SC: **bloquear** y devolver handoff a **`story-define`**. |
| **Salida mínima (modo B)** | Stubs `TK-XXX-*.md` en `Draft` + cobertura SC reportada al usuario. |
| **Salida para implementar** | Cada TK del alcance acordado en **`Estado: Ready`** (Plan, Dependencias y Referencias según checklist). Stubs en Draft **no** habilitan `story-implement`. |
| **Siguiente paso** | **`story-implement`** — solo cuando US Ready **y** las TK a ejecutar están Ready. Sugerir `/story-implement` al cerrar la última TK Ready del alcance. |
| **Regreso desde define** | Cambio funcional en la US → releer `README.md` y actualizar TKs afectadas antes de continuar. |
| **Regreso desde implement** | TK fuera de alcance o ambigüedad técnica → ajustar el TK aquí; no modificar el `README.md` de la US. Si el conflicto es funcional, escalar a **`story-define`**. |

### work-units.md
 
Cada sección `## <nombre-unidad>` contiene solo el nombre de la unidad y una descripción **corta** — lo estrictamente necesario para entender su alcance: qué cubre y, si reduce ambigüedad, qué queda fuera. No es un índice de tareas ni un inventario de artefactos técnicos. Cuando la unidad de un stub es `Por definir`, no es obligatorio crear la sección hasta que se concrete.
 
### Mensaje al usuario
 
Solo resultados y lo que el usuario debe saber o decidir. No incluir razonamiento interno, cadenas de pensamiento ni narración del trabajo en curso. Si hay pendientes o aclaraciones, listarlos en viñetas agrupadas por TK.