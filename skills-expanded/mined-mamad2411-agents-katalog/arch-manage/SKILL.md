---
name: arch-manage
description: >
  Crear o actualizar la arquitectura documentada del proyecto: Architecture Decision Records
  (ADR, en docs/adr/) y estándares de arquitectura por dominio técnico/funcional (en docs/standards/). Un ADR
  registra el "por qué" de una decisión (histórico, inmutable); un estándar (p. ej. "Testing Standards")
  agrupa los requisitos verificables de un dominio — el "qué hay que cumplir hoy". Cada decisión que fija
  una regla añade o actualiza un requisito del estándar de dominio (no crea un estándar por decisión).
  Activar para documentar, registrar o cambiar el estado de una decisión arquitectónica o norma del
  proyecto, aunque no use las palabras "ADR" o "estándar".
  Frases que activan este skill: "registrar decisión", "documentar por qué usamos X", "decision record",
  "cambiar ADR a Accepted", "marcar como Superseded", "crear/actualizar ADR", "ADR-XXX", "definir un
  estándar", "añadir un requisito".
  Usar también ante una tensión arquitectónica que deba quedar documentada.
license: MIT
---

# Skill: arch-manage

Crea y actualiza los dos artefactos de arquitectura del proyecto — **ADRs** y **estándares de dominio** —
siguiendo el flujo de este documento.

> **Este SKILL.md es el router.** El detalle de consulta puntual (catálogo de dominios, convenciones de
> frontmatter, fitness functions/runner, instalación de dependencias) vive en `references/` y se lee
> **solo cuando aplica** — ver [Archivos del skill](#archivos-del-skill-contexto-progresivo) al final.

## Concepto: ADR ≠ estándar (y el estándar es más amplio)

Este skill mantiene separados dos artefactos que suelen confundirse. La distinción es la razón de ser
de esta versión: **el ADR es la decisión; el estándar es la norma de dominio que la decisión alimenta.**

| | **ADR** (`docs/adr/`) | **Estándar** (`docs/standards/`) |
|---|---|---|
| Qué es | El registro de **una decisión** arquitectónica en un punto del tiempo | Un documento normativo de **dominio** (p. ej. *Testing Standards*) que **agrupa varios requisitos** |
| Granularidad | Fino: una decisión | **Amplio: un dominio** entero, alimentado por muchas decisiones |
| Pregunta que responde | *¿Por qué* elegimos X sobre Y? | *¿Qué* debe cumplir el proyecto hoy en este dominio, y *cómo* se verifica |
| Naturaleza | Histórico, narrativo, **inmutable** una vez `Accepted` | **Vivo y prescriptivo**; crece y se actualiza a medida que llegan nuevas decisiones |
| Contenido | Contexto, drivers, decisión, alternativas, consecuencias | Requisitos redactados con **RFC 2119 / RFC 8174** (MUST/SHOULD/MAY…), cada uno con su descripción normativa y excepciones, y sus **criterios de cumplimiento** (`CR-XXX`) verificables, agrupados en una tabla única al final del documento |
| Verificación | No se audita en sí mismo (es historia) | **Es lo que audita `arch-audit`**: cada **criterio de cumplimiento** (CR) con su fitness function |
| Relación | **Emite/actualiza** criterios de cumplimiento (`emits`) dentro de un estándar de dominio | **Nace de** los ADR que aportaron sus criterios (`source_adrs`) |

### El estándar es de dominio, no de decisión

> **Qué es "dominio" aquí.** Un **dominio técnico o funcional** del proyecto: un área o aspecto
> transversal (testing, architecture, api, security, coding-style, frontend, persistence, devops, observability — ver [`references/functional-domains.md`](references/functional-domains.md)). **No** es
> un dominio de negocio/DDD (bounded context) ni un dominio de internet. Se agrupa por *aspecto de
> arquitectura*, no por feature de negocio.

La clave de esta versión: **un estándar no es "usar PHPUnit para unit tests".** Ese es un *requisito*.
El estándar es **"Testing Standards"**, el documento de dominio (identificado por su **nombre**, sin
código) que contiene ese requisito («Unit testing») y todos los demás del mismo dominio.

- Decides *"unit tests con PHPUnit"* → no creas el estándar "usar PHPUnit"; creas (o actualizas) el
  estándar de dominio **`Testing Standards`** (`docs/standards/testing.md`) y añades dentro el requisito
  **Unit testing**: *"Las pruebas unitarias **DEBEN** implementarse con PHPUnit."* (en un estándar en
  inglés sería *"Unit tests **MUST** be implemented with PHPUnit."* — ver sección
  "Resolución de idioma" más abajo)
- Después decides *"e2e con Playwright"* → **no** creas un estándar nuevo: **añades** al mismo
  `Testing Standards` el requisito **E2E testing**: *"Las pruebas end-to-end **DEBEN** implementarse con
  Playwright."*

Así el estándar de dominio va agregando requisitos. Dentro de cada requisito, la unidad **verificable
y trazable** es el **criterio de cumplimiento** (`CR-XXX`): cada CR mide algo concreto (p. ej. cobertura
≥ 80%), traza a su ADR de origen y —si es automatizable— tiene su propia fitness function. Un requisito
agrupa uno o varios CR.

> **Requisitos en lenguaje normativo (RFC 2119 / RFC 8174).** Cada requisito del estándar se redacta
> con la palabra clave normativa correspondiente, **en MAYÚSCULAS** (solo en mayúsculas tienen el
> significado normativo, según RFC 8174) **y en el idioma de preferencia** (ver sección
> "Resolución de idioma" más abajo):
>
> | Inglés | Español |
> |---|---|
> | MUST | DEBE |
> | MUST NOT | NO DEBE |
> | REQUIRED | REQUERIDO |
> | SHALL | DEBERÁ |
> | SHALL NOT | NO DEBERÁ |
> | SHOULD | DEBERÍA |
> | SHOULD NOT | NO DEBERÍA |
> | RECOMMENDED | RECOMENDADO |
> | MAY | PUEDE |
> | OPTIONAL | OPCIONAL |

> **Regla práctica:** toda decisión se registra como **ADR**. Si además establece una regla continua,
> esa regla entra como **un requisito** en el estándar de su dominio (creándolo si el dominio aún no
> tiene estándar, o ampliándolo si ya existe). Una decisión puntual e histórica (p. ej. "en 2026
> migramos de MySQL a Postgres") es un ADR sin requisito: no hay norma continua que cumplir.

Las plantillas canónicas están en `assets/adr-template.md` y `assets/standard-template.md`.
**Leer la que corresponda antes de redactar.**

---

## Clasificar el input antes de redactar: ¿ADR, estándar, o ambos?

**Primer paso, siempre.** Antes de recopilar información o tocar cualquier archivo, clasificar qué pide
el input para saber **qué documento(s)** se producen y **con qué alcance**. No asumir que todo input
crea un ADR *y* un estándar: cada uno tiene su propio alcance y pueden existir de forma independiente.

Preguntarse dos cosas, en este orden:

1. **¿Hay una *decisión* nueva que documentar** (una elección técnica y su porqué)?
2. **¿Hay una *regla continua y verificable*** que el equipo deba cumplir de aquí en adelante?

Según las respuestas, el input cae en uno de tres casos:

| Caso | El input es… | Qué se produce | Ruta |
|---|---|---|---|
| **A. Solo ADR** | Una decisión puntual/histórica **sin** regla continua que cumplir (p. ej. "en 2026 migramos de MySQL a Postgres", "adoptamos Vite como bundler") | Un **ADR** con `emits: []`. **No** toca `docs/standards/` | [Crear una decisión (ADR)](#flujo-crear-una-decisión-adr-y-su-requisito-de-estándar), deteniéndose en el paso 4 (rama "No") |
| **B. ADR + estándar** | Una decisión **que además** fija una regla continua y verificable (p. ej. "las APIs son GraphQL", "unit tests con PHPUnit y cobertura ≥ 80%") | Un **ADR** (el porqué) **y** su(s) **criterio(s) de cumplimiento** emitido(s) al estándar del dominio (el qué verificable) | [Crear una decisión (ADR) y su requisito de estándar](#flujo-crear-una-decisión-adr-y-su-requisito-de-estándar), completo |
| **C. Solo estándar / requisito** | Una regla o convención verificable **sin decisión nueva** que documentar: refinar un umbral, aclarar una excepción, o añadir/editar un requisito o criterio en un dominio existente | Un **requisito/criterio** en un estándar. Idealmente traza a un ADR; si no existe, ofrecer crearlo, pero **se permite** dejar constancia de que su decisión de origen está pendiente | [Crear o actualizar un estándar / requisito directamente](#flujo-crear-o-actualizar-un-estándar--requisito-directamente) |

> **Independencia de los dos documentos.** Un ADR **puede no tener estándar** (`emits: []`, caso A) y un
> requisito/criterio **puede no tener ADR** registrado (caso C). No forzar la creación del otro documento
> solo por simetría: se crea el que el alcance del input justifique.

### Regla de oro: no mezclar el alcance de cada documento

El ADR y el estándar se enlazan **por referencia**, nunca duplicando contenido:

- **El ADR contiene solo el *porqué*** — contexto, drivers, decisión, alternativas, consecuencias — y
  `emits` (las referencias `<estándar>/CR-XXX` que fija). **Nunca** aloja el enunciado normativo
  (MUST/SHOULD…) ni los criterios verificables: el ADR **emite** la regla, no la **contiene**.
- **El estándar contiene solo el *qué hay que cumplir hoy*** — requisitos con su descripción normativa
  (RFC 2119) y sus criterios de cumplimiento (`CR-XXX`) verificables — y `source_adrs`. **Nunca** aloja el porqué,
  los drivers ni las alternativas: eso es historia y vive en el ADR.
- **El enlace es cruzado, no copiado:** `emits` (ADR) ↔ `source_adrs` / columna `Origen` (estándar). Si
  te descubres copiando el enunciado normativo dentro del ADR, o el contexto/alternativas dentro del
  estándar, estás mezclando alcances: mueve cada parte a su documento y deja solo la referencia.

> Si el input es ambiguo sobre si fija o no una regla continua (caso A vs B), **confirmarlo con el
> usuario** en la tanda de preguntas inicial (ver "Información requerida"), no decidirlo por cuenta propia.

---

## Resolución de idioma

El idioma de los artefactos y de los mensajes al usuario se decide en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si hay una preferencia registrada en la memoria del proyecto, usarla.
3. Si no, usar el idioma del mensaje del usuario y **preguntar si desea persistir esa preferencia en la memoria del proyecto**.
4. Si no se puede inferir, **preguntar** qué idioma prefiere; no decidir el idioma por cuenta propia.

Las claves de frontmatter, los identificadores (`ADR-XXX`, referencias de requisito `<estándar>/<requisito>` y de criterio `<estándar>/CR-XXX`), las rutas y las salidas de comandos **no se traducen**.

Las palabras clave normativas de RFC 2119 / RFC 8174 (MUST/DEBE, SHOULD/DEBERÍA, MAY/PUEDE… — tabla completa en la sección "Concepto: ADR ≠ estándar" más arriba) **sí se redactan en el idioma de preferencia**, siempre en MAYÚSCULAS: un estándar en español usa DEBE/DEBERÍA/PUEDE…, uno en inglés usa MUST/SHOULD/MAY…

---

## Información requerida antes de redactar

Recopilar en **una sola tanda de preguntas** al inicio usando la herramienta de preguntas estructuradas del cliente (máx. 3 preguntas por bloque; opciones cortas y mutuamente excluyentes). No inventar datos — si no están en contexto, preguntar.

| Dato | Fuente preferida | Si no está |
|------|-----------------|------------|
| Problema / tensión arquitectónica | Descripción del usuario | Preguntar |
| Decisión concreta | Descripción del usuario | Preguntar |
| ¿Establece una regla continua? (→ requisito de estándar) y ¿de qué **dominio**? (ver [`references/functional-domains.md`](references/functional-domains.md)) | Inferir del alcance; confirmar con el usuario | Preguntar si es ambiguo |
| Decisores | Indicado por el usuario | Preguntar siempre |
| Stack tecnológico | `package.json`, `pom.xml`, etc. | Preguntar |
| Alternativas consideradas | Solo si el usuario las mencionó | Omitir la sección si no las mencionó |
| ADRs / estándares relacionados | `docs/adr/` + `docs/standards/` + contexto | Preguntar si hay referencias a citar |

> ADRs en estado **Draft** o **Proposed** también requieren problema y decisión tentativa.

---

## Validación de conflictos (solo al crear)

Antes de redactar un ADR nuevo o de añadir un requisito:

1. Leer títulos y la sección clave (`## Decisión` de los ADR; los requisitos de los estándares de `docs/standards/`).
2. Si hay conflicto (misma tecnología/componente ya cubierto por un ADR `Accepted` o por un requisito `Active`, contradicción directa, o duplicación):
   - **No redactar**; informar al usuario con enlace(s) al artefacto en conflicto.
   - Sugerir: (a) actualizar el existente, (b) crear ADR nuevo marcando el anterior como `Superseded`, o (c) ajustar el alcance/requisito.

---

## Flujo: Crear una decisión (ADR) y su requisito de estándar

> Aplica a los casos **A** (solo ADR) y **B** (ADR + estándar) de la [clasificación del input](#clasificar-el-input-antes-de-redactar-adr-estándar-o-ambos). El paso 4 bifurca entre ambos. Mantener separado el alcance: el ADR solo registra el porqué y `emits`; el enunciado normativo y los criterios viven en el estándar.

1. **Número y archivo del ADR** — correlativo en `docs/adr/`; archivo `docs/adr/ADR-XXX-<slug>.md`. Convenciones de identidad/numeración y frontmatter: [`references/conventions.md`](references/conventions.md).
2. **Recopilar información faltante** (ver tabla anterior).
3. **Escribir el ADR** desde `assets/adr-template.md`:
   - Frontmatter YAML: `id: ADR-XXX`, `status` (ver regla de default abajo), `last_update` = hoy, `deciders`, `tags`, `supersedes: null`, `superseded_by: null`, `emits: []` (campos completos en [`references/conventions.md`](references/conventions.md)).
   - **Default de `status`:**
     - **Por defecto, `Draft`** — la decisión todavía no está en vigor o sigue en discusión.
     - **`Accepted`** si la decisión ya está vigente y el código la implementa y cumple **hoy** — típicamente al venir de `arch-discover` documentando retroactivamente algo que el repo ya hace (no una decisión nueva a futuro). No usar `Draft` para una decisión que ya rige: `Draft`/`Proposed` implican que aún no aplica, lo cual sería falso en ese caso.
   - Cuerpo: `## Contexto`, `## Decisión`, `## Alternativas consideradas` (opcional), `## Consecuencias`, `## Referencias`. **Solo el porqué** — sin enunciados normativos ni criterios (eso va al estándar).
4. **Decidir si la decisión establece una regla continua.** Preguntarse: *¿esta decisión fija una regla
   que el equipo deberá cumplir de forma continua?*
   - **No** (decisión puntual o histórica) → `emits: []`. No toca estándares. Fin del bloque de estándares.
   - **Sí** → identificar el **dominio técnico/funcional** clasificándolo con [`references/functional-domains.md`](references/functional-domains.md) (proponer otro solo si no encaja en ninguno) y continuar al paso 5.
5. **Ubicar o crear el estándar de dominio** en `docs/standards/` (identificado por su **nombre**, sin código):
   - **Si ya existe** un estándar para ese dominio (p. ej. `docs/standards/testing.md` o `docs/standards/testing/README.md`) → **actualizarlo**: añadir (o modificar) el **requisito** correspondiente, sin reescribir los requisitos existentes.
   - **Si no existe** → **crearlo** desde `assets/standard-template.md` con `name` (p. ej. `Testing Standards`), `domain` (slug), `status: Draft` (o `Active` si ya rige), `last_update` = hoy y `source_adrs`.
     - **Forma simple:** `docs/standards/<slug>.md`.
     - **Forma con documentos adicionales:** si el estándar necesita archivos de apoyo (guías, ejemplos, matrices), crear la carpeta `docs/standards/<slug>/`, escribir el estándar en `docs/standards/<slug>/README.md` y colocar los documentos adicionales dentro de esa carpeta (enlazados con rutas relativas desde el estándar). Si un estándar simple pasa a necesitar extras, migrarlo de `<slug>.md` a `<slug>/README.md`.
6. **Redactar el requisito y proponer sus criterios de cumplimiento** (campos exactos en [`references/conventions.md`](references/conventions.md)):
   - Un bloque `## <Nombre del requisito>` con: `**ID:** <slug-requisito>`, el párrafo de qué es / cómo se usa / cómo se implementa, que **debe incluir el enunciado normativo con RFC 2119** (MUST/SHOULD/MAY… en mayúsculas), y `### Excepciones`. **No** incluir aquí los criterios de cumplimiento: van todos juntos en la tabla única `## Criterios de cumplimiento`, al final del documento (antes de `## Referencias`). El **origen y la verificación se registran por criterio (CR)**, no a nivel de requisito.
   - **Los CR no se escriben directamente: se proponen y el usuario elige.** Derivar los criterios candidatos del requisito, investigar el **mecanismo de verificación** de cada uno, presentarlos en una **tabla de propuesta simplificada** (`#`, criterio, enfoque y la herramienta con la que se verificaría — sin comandos ni código, que aún no existen) y preguntar al usuario **cuáles quiere crear** y **para cuáles quiere la fitness function ahora** — flujo completo en [`references/fitness-functions.md`](references/fitness-functions.md). Solo lo seleccionado se escribe.
   - Añadir a la tabla única `## Criterios de cumplimiento` la fila (o filas) `CR-XXX` **seleccionadas**: `ID` (`CR-XXX`, correlativo único en el estándar), `Requisito` (el `ID` del requisito al que pertenece), `Descripción` (medible, con RFC 2119 si es normativa), `Origen` (`ADR-XXX`), `Automatizable` (yes/no), `Enfoque` (`bloqueante`/`warning`; por defecto `bloqueante`) y `Verificación` (yes/no: si la verificación ya existe; la ruta del chequeo no se escribe — se resuelve por convención).
   - **Enlazar en ambos sentidos:** añadir la referencia global de cada CR (`<slug-estándar>/CR-XXX`, p. ej. `testing/CR-001`) al `emits` del ADR, y el `ADR-XXX` a `source_adrs` del estándar (a nivel de documento) además de en la columna `Origen` del CR.
7. **Crear las fitness functions que el usuario seleccionó en el paso 6** — flujo completo en [`references/fitness-functions.md`](references/fitness-functions.md): **instalar y configurar** la herramienta ya decidida en la propuesta si hace falta, y registrar el chequeo en el **archivo de checks de su estándar** (`scripts/arch/checks/<slug-estándar>.<ext>`, un archivo por estándar, con la trazabilidad `CR-XXX` en comentarios y líneas de salida), asegurando el **runner** `scripts/arch/verify.<ext>` — ambos escritos en el **lenguaje del stack del repo** (p. ej. Node en un proyecto Angular/React/Vue). Al quedar registrado el chequeo, **volver a la fila del CR** y poner `Verificación: yes` (los CR seleccionados sin fitness function se quedan en `no`, pendientes). La verificación cuelga de **cada criterio de cumplimiento**, no del requisito, del ADR ni del estándar entero.
8. **Ofrecer instalar dependencias referenciadas ausentes** — flujo en [`references/dependencies.md`](references/dependencies.md) (no repite las herramientas de fitness function ya resueltas en el paso 7).
9. **Actualizar los índices `README.md`**:
   - `docs/adr/README.md`: añadir `- [ADR-XXX: Título](ADR-XXX-slug.md)` en orden ascendente.
   - `docs/standards/README.md`: si el estándar de dominio es nuevo, añadir `- [Nombre del estándar](<slug>.md)` (forma simple) o `- [Nombre del estándar](<slug>/README.md)` (forma carpeta); si ya existía, no duplicar.
   - **Si el índice no existe todavía y la carpeta ya tenía artefactos previos** (p. ej. `docs/adr/ADR-001-*.md` y `ADR-002-*.md` ya existían pero nunca hubo `docs/adr/README.md`): al crear el índice por primera vez, listar **todos** los artefactos existentes en la carpeta (`ls docs/adr/*.md` / `docs/standards/*.md` o `*/README.md`), no solo el que se acaba de crear — el índice debe reflejar el estado real de la carpeta desde su primera versión, en el mismo orden ascendente que usaría en adelante. Si la carpeta no tenía nada más, el índice arranca con la única entrada nueva.
   - Crearlos con encabezado y lista si no existen. Nunca reordenar ni eliminar entradas.
10. **Confirmar** mostrando: ruta del ADR, estándar de dominio y requisito(s) añadido(s)/actualizado(s), líneas de índice, y —si aplica— la fitness function creada (en qué archivo de checks quedó), el comando del runner (`node scripts/arch/verify.mjs` en un repo Node, o el equivalente del stack; con el slug del estándar para correr solo ese) y las dependencias instaladas.

---

## Flujo: Actualizar un ADR existente

Recordar que un ADR es **histórico**: se actualiza su estado o se corrigen datos, pero no se reescribe
la decisión ya tomada — para cambiar de rumbo se crea un ADR nuevo que supersede al anterior.

1. Identificar el archivo por número, slug o título.
2. Leer el contenido completo antes de editar.
3. Aplicar los cambios; actualizar `last_update` a hoy si el cambio es sustantivo. **Nunca** reescribir una decisión `Accepted`; para eso, superseder.
4. Si el nuevo estado es `Superseded`:
   - Marcar `status: Superseded` y `superseded_by: ADR-XXX`. Si el usuario no lo indicó, preguntar antes de guardar.
   - En el ADR reemplazante, fijar `supersedes: ADR-<anterior>`.
   - **Revisar los criterios emitidos** (`emits`): si la decisión superseded había fijado criterios de cumplimiento (CR) que ya no rigen, actualizarlos o retirarlos de su estándar de dominio (marcando el requisito o el estándar `Deprecated`/`Superseded` según alcance), y enlazar el CR reemplazante si lo hay. Un ADR obsoleto no debe dejar criterios vivos huérfanos.
   Si el nuevo estado es `Deprecated`: `status: Deprecated`, actualizar `last_update`, registrar el motivo en `## Referencias` y aplicar el mismo repaso a sus criterios.
5. Actualizar `docs/adr/README.md` si el título cambió.
6. **Confirmar** mostrando los campos modificados y el impacto en criterios emitidos.

---

## Flujo: Crear o actualizar un estándar / requisito directamente

> Aplica al caso **C** de la [clasificación del input](#clasificar-el-input-antes-de-redactar-adr-estándar-o-ambos): una regla verificable sin decisión nueva. No arrastrar aquí el porqué/drivers/alternativas — eso, si hace falta documentarlo, es un ADR aparte.

A veces se refina una regla sin una decisión nueva (afinar un umbral, ampliar el alcance, aclarar una
excepción, añadir un requisito a un dominio existente). El estándar es **vivo**: se edita.

1. **Todo criterio de cumplimiento (CR) debería trazar a un ADR** (columna `Origen` + `source_adrs`). Si se pide añadir un criterio
   sin decisión registrada, ofrecer crear primero el ADR de origen (flujo de arriba). Si el usuario
   prefiere no crearlo, permitir el CR dejando constancia de que su decisión de origen está
   pendiente de documentar (lo señalará `arch-audit`).
2. Identificar el estándar de dominio (o crearlo, `docs/standards/<slug>.md` o `docs/standards/<slug>/README.md` si lleva documentos adicionales; dominio según [`references/functional-domains.md`](references/functional-domains.md)).
3. Añadir o editar el bloque de requisito (`ID`, descripción con el enunciado normativo en RFC 2119, `Excepciones`). Si el cambio implica **CR nuevos**, pasar antes por la **propuesta y selección** de [`references/fitness-functions.md`](references/fitness-functions.md) (tabla simplificada de criterios candidatos → el usuario elige cuáles crear), y escribir solo los seleccionados como filas `CR-XXX` en la tabla única `## Criterios de cumplimiento`, al final del documento (`Requisito`, `Descripción`, `Origen`, `Automatizable`, `Enfoque`, `Verificación`; ver [`references/conventions.md`](references/conventions.md)). Actualizar `last_update` a hoy.
4. Reevaluar la fitness function de cada CR afectado: si cambió su descripción, ajustar su chequeo en el archivo de checks de su estándar (`scripts/arch/checks/<slug-estándar>.<ext>`; ver [`references/fitness-functions.md`](references/fitness-functions.md)).
5. Si el nuevo estado del estándar o de un requisito es `Deprecated`/`Superseded`, enlazar el reemplazo y actualizar `docs/standards/README.md`.
6. **Confirmar** los cambios.

---

## Anti-patterns

- Mezclar el alcance de ADR y estándar: meter el enunciado normativo (RFC 2119) o los criterios de cumplimiento dentro del ADR, o el contexto/alternativas/consecuencias dentro del estándar. Cada uno contiene solo lo suyo y se enlazan por referencia (`emits` ↔ `source_adrs`/`Origen`).
- Crear un estándar nuevo por cada decisión en vez de añadir un requisito al estándar de dominio existente — el estándar es de **dominio**, no de decisión.
- Redactar un ADR o un requisito sin pasar primero por la [Validación de conflictos](#validación-de-conflictos-solo-al-crear): duplicar o contradecir un ADR `Accepted` o un requisito `Active` ya existente.
- Reescribir la decisión de un ADR `Accepted` en vez de crear uno nuevo que lo supersede — un ADR es histórico e inmutable una vez aceptado.
- Marcar un ADR `Superseded`/`Deprecated` sin revisar los criterios (`emits`) que fijó: dejar CR huérfanos vigentes en un estándar cuando la decisión que los originó ya no rige.
- Escribir los `CR-XXX` en el estándar sin presentar antes la **tabla de propuesta** y dejar que el usuario elija cuáles crear — los criterios se proponen, no se imponen (`references/fitness-functions.md`).
- Escribir en la tabla del estándar filas de criterios que el usuario **no seleccionó** (aunque se hayan propuesto, aunque parezcan buena idea, aunque sea «para dejarlos pendientes») — solo lo seleccionado se crea y se registra.
- Preguntar «¿creo la fitness function?» sin haber investigado ni mostrado la **herramienta concreta** con la que se verificaría (y si hay que instalarla): el usuario no puede decidir sobre un chequeo que no sabe cómo se hará. El comando y el código no se muestran aquí — todavía no existen.
- Crear una fitness function sin la aprobación explícita del usuario, o sin investigar primero si ya existe una herramienta/convención establecida para ese chequeo en el stack — un script propio a medida es el último recurso, no el primero (`references/fitness-functions.md`).
- Quemar números `CR-XXX` en criterios que el usuario aún no ha seleccionado — los candidatos se numeran `C1`, `C2`… solo para la conversación; el `CR-XXX` se asigna al escribir.
- Dejar la herramienta de verificación de una fitness function sin instalar cuando el usuario aceptó instalarla, o repreguntar por ella en el paso de dependencias generales (`references/dependencies.md`) después de ya haberla resuelto en `references/fitness-functions.md`.
- Escribir el runner o los checks en un lenguaje ajeno al stack del repo (p. ej. shell en un proyecto Node) — se escriben con el runtime que el proyecto ya usa; el shell POSIX es solo el último recurso cuando el repo no tiene ningún runtime de stack.
- Crear un archivo de chequeo por criterio de cumplimiento — el archivo de checks es **por estándar** (`scripts/arch/checks/<slug-estándar>.<ext>`); la trazabilidad por CR va dentro, en comentarios y en las líneas de salida de cada chequeo.
- Instalar o configurar dependencias sin la aprobación explícita del usuario, o correr build/suites completas por iniciativa propia.
- Al invocarse en lote (p. ej. desde `arch-discover`), volver a preguntar decisores/idioma o la instalación de dependencias por cada artefacto en vez de resolverlo una sola vez para todo el lote.
- Pedirle al usuario el número del próximo ADR o CR — siempre se calcula releyendo `docs/adr/` o la tabla del estándar, nunca se pregunta.

---

## Archivos del skill (contexto progresivo)

Este SKILL.md contiene el concepto, la clasificación del input y los flujos. El detalle de consulta
puntual está en archivos aparte; **leer cada uno solo cuando la tarea lo pida** (así el contexto se
mantiene ligero):

**Plantillas y activos (`assets/` — copiar/rellenar al redactar):**

- `assets/adr-template.md` — plantilla del ADR. Leer antes de escribir un ADR.
- `assets/standard-template.md` — plantilla del estándar (requisitos + tabla de `CR-XXX`). Leer antes de crear/editar un estándar.
- `assets/arch-fitness/` — implementación de referencia del runner, en Node (`verify.mjs`, `checks/example.mjs.template`, `README.md` con el contrato). En un repo Node se copia al crear el runner; en otro stack se genera el equivalente en ese lenguaje con el mismo contrato.

**Referencias de consulta (`references/` — leer bajo demanda):**

- [`references/functional-domains.md`](references/functional-domains.md) — catálogo de los 9 dominios funcionales canónicos. Leer al **clasificar el dominio** de un estándar (casos B/C).
- [`references/conventions.md`](references/conventions.md) — convenciones de identidad, numeración y **frontmatter** de ADR / estándar / requisito / CR. Leer al escribir frontmatter o identificadores.
- [`references/fitness-functions.md`](references/fitness-functions.md) — cómo **proponer los criterios (CR) con su mecanismo de verificación** para que el usuario elija cuáles crear, cómo crear la **fitness function** de los seleccionados, registrarla en el archivo de checks de su estándar y mantener el **runner** `scripts/arch/verify.<ext>`. Leer **antes de escribir CR nuevos**, al automatizar un CR o al tocar el runner.
- [`references/dependencies.md`](references/dependencies.md) — flujo para ofrecer **instalar dependencias** ausentes que referencia la decisión. Leer tras crear los artefactos si referencian una tecnología concreta.

---

## Referencias

- [Architecture Decision Records](https://github.com/joelparkerhenderson/architecture-decision-record)
- [Documenting Architecture Decisions — Cognitect](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) · [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) (BCP 14) — palabras clave normativas.
- *Building Evolutionary Architectures* (Ford, Parsons, Kua) — concepto de fitness functions.
