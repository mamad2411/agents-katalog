---
name: arch-audit
description: >
  Auditar el cumplimiento de los estándares de arquitectura (docs/standards/) y de las reglas de
  AGENTS.md contra el estado real del repositorio (Architecture Compliance Checking), citando el ADR
  de origen de cada estándar, y generar un informe priorizado en docs/audits/arch-audit-YYYY-MM-DD.md.
  Activar siempre que el usuario quiera verificar, auditar o comprobar si el código respeta los
  estándares, las decisiones arquitectónicas o las reglas del proyecto — incluso si no dice
  "estándar", "ADR" o "auditoría".
  Frases que activan este skill: "audita el cumplimiento", "¿el código respeta los estándares?",
  "¿el código respeta los ADR?", "verifica que seguimos las reglas de AGENTS.md",
  "revisa si cumplimos la arquitectura", "compliance de arquitectura", "qué normas estamos incumpliendo",
  "chequea las reglas del repo", "arch-audit", "/arch-audit". Usar también cuando el usuario sospeche
  que el repo se desvió de lo documentado y quiera un informe de brechas con acciones.
license: MIT
---

# Skill: arch-audit

Audita el **cumplimiento** de las normas de arquitectura del proyecto contra el estado real del
código, y produce un informe de brechas priorizado. Es la variante de *Architecture Compliance
Checking*: no descubre arquitectura nueva (eso lo hace `arch-discover`) ni la documenta (eso lo hace
`arch-manage`); aquí se toman las normas **ya existentes** como el "deber ser" y se comparan contra
el "ser" del repositorio.

## Qué es normativo aquí: el criterio de cumplimiento (CR), no el ADR

La distinción entre ADR y estándar (ver `arch-manage`) determina qué se audita. **La unidad auditable
es el criterio de cumplimiento** (`CR-XXX`, una fila verificable dentro de un estándar de dominio
técnico o funcional), no el estándar entero, ni el requisito como bloque, ni el ADR:

- **El "deber ser" son los criterios de cumplimiento de los estándares** (`docs/standards/`, en
  estándares `Active`) y las reglas de `AGENTS.md`. Cada criterio (`CR-XXX`) está redactado de forma
  medible, con RFC 2119 cuando es normativa (MUST/SHOULD/MAY…): un `MUST` incumplido es un hallazgo de
  mayor peso que un `SHOULD`. Un estándar de dominio (p. ej. *Testing Standards*) se audita **criterio
  por criterio** (`testing/CR-001`, `testing/CR-002`…), agrupados y contextualizados por su requisito.
- **El requisito es la agrupación legible que da contexto, no la unidad auditada.** Un requisito
  (`## <Nombre>` con `**ID:** <slug>`, referencia `<estándar>/<slug-requisito>` p. ej.
  `testing/unit-testing`) reúne una o varias filas de criterios `CR-XXX` bajo `### Criterios de
  cumplimiento`. Sirve para leer y ubicar los criterios, pero lo que se audita es cada `CR-XXX`.
- **El ADR es contexto, no la norma auditada.** Un ADR registra el *por qué* de una decisión; es
  historia. Se cita como **Origen** de cada criterio (`Origen` de la fila / `source_adrs` del estándar)
  para dar trazabilidad, pero no se audita "el ADR" en abstracto.
- **ADR sin criterio (CR)** = decisión histórica que no fijó ningún criterio (`emits: []`), sin regla
  continua auditable → no genera hallazgo de cumplimiento. Si un ADR `Accepted` contiene una regla
  claramente enforceable pero **no fijó** ningún criterio (repos antiguos, previos a esta separación),
  señalarlo como observación y **sugerir emitir el criterio** vía `arch-manage`, en vez de auditar el
  ADR como si fuera la norma.

> **Peso normativo (RFC 2119).** Al fijar la prioridad de un hallazgo, considerar la fuerza del término:
> incumplir un `MUST`/`REQUIRED`/`SHALL` pesa más que un `SHOULD`/`RECOMMENDED`; un `MAY`/`OPTIONAL` no
> incumplido casi nunca es hallazgo.

**Fuentes normativas (el "deber ser"):**
- `docs/standards/` — todos los estándares de dominio (técnico o funcional) y sus **criterios de cumplimiento** (`CR-XXX`), agrupados por requisito, priorizando los de estándares `Active` (obligatorios). Criterios en estándares `Draft` se listan pero no generan hallazgo con prioridad ni afectan el veredicto; `Deprecated`/`Superseded` no generan hallazgos salvo que el código siga dependiendo de ellos.
- `AGENTS.md` (y `AGENTS.md` anidados por subcarpeta, si existen) — cada regla explícita del documento.
- `docs/adr/` — **solo como trazabilidad**: para cada criterio auditado, citar su ADR de origen; y para detectar ADR `Accepted` con regla enforceable que aún no fijó ningún criterio.
- `.agents/MEMORY.md` (si existe) — contexto de idioma, **no** es fuente de reglas por sí mismo (el stack vive en `AGENTS.md § Stack tecnológico`, no aquí).

**Evidencia (el "ser"):** el código, la estructura de carpetas y los manifiestos de dependencias del repo.

**Método: inspección estática + fitness functions.** La verificación base es leer el repo con `find`,
`grep` y manifiestos. Cuando un criterio (`CR-XXX`) tenga una **fitness function** (chequeo automatizado
de arquitectura, en el sentido de *arquitectura evolutiva*), **ejecutarla**: su resultado es la evidencia
primaria del cumplimiento de ese criterio. No se corre el build ni la suite completa, solo los chequeos
de arquitectura detectados. Si un criterio no puede confirmarse ni por inspección ni por una fitness
function, se marca *No verificable* y se anota qué evidencia haría falta — nunca inventar un veredicto.
Para cada criterio, el skill evalúa si es **apto** para una fitness function (cumplimiento objetivo y
automatizable — normalmente ya declarado en su columna `Automatizable: yes`), comprueba si ya existe y la
ejecuta; si es apto pero no existe (`Verificación: no`), **sugiere crearla**.

**Salida:** un único informe en `docs/audits/arch-audit-YYYY-MM-DD.md`, agrupado por prioridad
(alta / media / baja), donde cada hallazgo referencia el criterio incumplido (`<estándar>/CR-XXX`, con
el requisito que lo agrupa, su estándar de dominio y su ADR de origen) o la regla de AGENTS.md, lista
evidencias y archivos infractores, propone una acción y fija un estado. El informe incluye además una
sección de **fitness functions**: cuáles existen y su resultado al ejecutarlas, y cuáles faltan
(criterios aptos sin fitness function) con la sugerencia de crearlas.

> **`docs/audits/` es compartido y mezcla dos semánticas.** Ahí conviven los informes **históricos** de este
> skill (`arch-audit-YYYY-MM-DD.md`, nunca sobrescritos) con los informes de **estado vigente** de
> `quality-check` y `code-review` (`quality-check.md`, `code-review.md`, sobrescritos en cada corrida) y sus
> copias `<skill>-<YYYYMMDD-HHMMSS>.md` de `save-report`. Los espacios de nombres son disjuntos: al buscar
> auditorías previas usar siempre el glob `arch-audit-*.md`, nunca listar el directorio entero.
>
> Todo `docs/audits/` está **excluido del fingerprint canónico** de la tubería de cierre (ver
> [`quality-check`](../quality-check/SKILL.md#caché-de-corrida-de-pruebas-compartida-con-trace-validate)):
> generar un informe de auditoría **no** invalida la caché de pruebas ni fuerza a regenerar un
> `trace-report.md`.
Este contenido se escribe una sola vez, al crear el informe, y permanece inalterado; cada revalidación
posterior agrega una entrada nueva en la sección `## Revalidaciones` al final del **mismo** archivo
(nunca se crea un archivo por revalidación), con la fecha/hora, el veredicto resultante y solo los
cambios evidenciados.

La plantilla canónica del informe está en `assets/audit-template.md`. **Leerla antes de redactar**
cualquier informe y respetar su estructura.

---

## Resolución de idioma

Decidir el idioma del informe y de los mensajes al usuario en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si hay una preferencia registrada en la memoria del proyecto, usarla.
3. Si no, usar el idioma del mensaje del usuario y preguntar si desea persistir esa preferencia en la memoria del proyecto.
4. Si no se puede inferir, preguntar qué idioma prefiere; no decidir por cuenta propia.

Las rutas de archivo, identificadores (`ADR-XXX`, referencias de criterio `<estándar>/CR-XXX`, referencias de requisito `<estándar>/<slug-requisito>`) y salidas de comandos no se traducen.

---

## Fase 0 — Nueva auditoría o revalidación

Antes de auditar, comprobar si ya existen informes previos:

```bash
ls docs/audits/arch-audit-*.md 2>/dev/null
```

- **Si no hay ninguno:** proceder directamente con una **nueva auditoría desde cero** (Fase 1).
- **Si hay uno o varios:** localizar el **más reciente por la fecha del nombre** del archivo
  (`arch-audit-YYYY-MM-DD.md`; ordenar por esa fecha, no por fecha de sistema) y usar la
  **herramienta de preguntas estructuradas** del cliente para preguntar cómo continuar,
  **mostrando el nombre del archivo detectado**:

  > "Encontré una auditoría previa: **arch-audit-2026-06-30.md**. ¿Cómo quieres continuar?"
  > Opciones:
  > - **Revalidar `arch-audit-2026-06-30.md`** — vuelve a comprobar cada hallazgo previo contra el estado actual y agrega los cambios como una nueva entrada en `## Revalidaciones`, sin tocar el informe original.
  > - **Nueva auditoría desde cero** — audita todas las normas de nuevo, ignorando el informe anterior.

  Una sola pregunta; opciones cortas y mutuamente excluyentes. Si el cliente no expone la
  herramienta, ofrecer las mismas opciones enumeradas en prosa (1 / 2).

### Comportamiento en Revalidación

El informe original (resumen, hallazgos, fitness functions, reglas no verificables) se
preserva **tal cual se creó la primera vez** — una revalidación nunca reescribe,
reordena ni elimina ese contenido. Los cambios de cada revalidación se documentan aparte.

1. Leer el informe previo elegido completo, incluida su sección `## Revalidaciones` si ya existe.
   El **estado de referencia** para comparar no es solo el informe original: es el informe original
   **ajustado** por los cambios acumulados en todas las entradas de `## Revalidaciones` previas (p.
   ej. un hallazgo marcado `✅ Resuelto` en una revalidación anterior ya no cuenta como incumplimiento
   vigente al comparar).
2. Repetir la recopilación y verificación contra el estado actual del repo, reutilizando las mismas
   fases que una auditoría nueva, sin modificar nada de lo ya escrito en el documento:
   - **Fase 1** — detectar criterios de cumplimiento (`CR-XXX`) (o estándares de dominio) o reglas de `AGENTS.md` **nuevos** desde la última verificación.
   - **Fase 2** — reevaluar cada regla/hallazgo ya documentado contra el estado actual.
   - **Fase 2B** — re-ejecutar las fitness functions existentes y las creadas desde la última verificación.
   - **Fase 3.5** — reverificar las dependencias de los estándares/ADR auditados (ver esa fase); su
     resultado se trata como un cambio evidenciado más, no se pregunta ni se escribe por separado.
3. Identificar **solo los cambios evidenciados** en esta corrida frente al estado de referencia (paso 1):
   - Incumplimiento ya no presente → cambio `✅ Resuelto`.
   - Sigue presente pero con evidencia nueva relevante → registrar el cambio de evidencia.
   - Nuevo incumplimiento o regresión (de una regla ya auditada o de una nueva) → registrarlo.
   - Dependencia que faltaba y ya fue instalada, sigue faltando, o aparece una nueva (Fase 3.5) → registrarlo.
   - Si no hubo ningún cambio desde la última verificación, la entrada lo indica explícitamente
     ("Sin cambios respecto a la última verificación.") en vez de listar hallazgos sin novedad.
4. Calcular fecha y hora de esta ejecución:
   ```bash
   date "+%F %H:%M"
   ```
5. Calcular el **veredicto resultante** de esta revalidación, considerando el estado combinado
   (estado de referencia del paso 1 + cambios evidenciados en los pasos 2-3).
6. **Añadir al final del mismo archivo** (nunca crear un archivo nuevo ni sobrescribir lo anterior)
   una **única** entrada nueva en `## Revalidaciones`, con la fecha/hora, el veredicto resultante y
   todos los cambios evidenciados (incluida la verificación de dependencias), siguiendo la estructura
   de `assets/audit-template.md`.
7. Actualizar el campo `Veredicto` de la **cabecera** de ese mismo archivo: conservar el
   veredicto vigente y agregar junto a él `(revalidado YYYY-MM-DD HH:MM)` con la fecha/hora de esta
   revalidación. Es el único dato del contenido original que una revalidación sí actualiza.

En una **Nueva auditoría desde cero** se ignora el histórico para el análisis, se crea un archivo
**nuevo** `arch-audit-<hoy>.md` y se parte de la Fase 1.

---

## Fase 1 — Recopilar las normas (el "deber ser")

1. **Estándares, sus requisitos y sus criterios** — listar y leer:
   ```bash
   ls docs/standards/*.md 2>/dev/null || echo "No hay estándares"
   ```
   De cada estándar de dominio técnico o funcional (identificado por su **nombre**, sin código; su línea
   visible bajo el título es `**Dominio:** <slug>`; archivo `docs/standards/<slug>.md` o carpeta
   `docs/standards/<slug>/README.md`) extraer su `name`, `domain`, `status` y `source_adrs`. **Si el
   estándar no trae la línea `**Dominio:** <slug>`** (formato antiguo o más simple, previo a esta
   convención), usar el nombre del archivo/carpeta como `domain` de facto y señalarlo como observación
   (formato de estándar desactualizado) — no bloquea la auditoría de sus criterios. Dentro del
   documento, cada **requisito** (`## <Nombre>` con `**ID:** <slug-requisito>`; referencia
   `<slug-estándar>/<slug-requisito>`) es una **agrupación legible**; los criterios de todos los
   requisitos viven juntos en la tabla única `## Criterios de cumplimiento`, al final del documento
   (antes de `## Referencias`). Extraer **de cada fila `CR-XXX`** (la unidad auditable; referencia
   global `<slug-estándar>/CR-XXX`): `ID` (`CR-XXX`), `Requisito` (slug del requisito al que
   pertenece), `Descripción` (medible, con su palabra clave RFC 2119 si es normativa), `Origen` (ADR
   que fijó ese criterio), `Automatizable` (yes/no), `Enfoque` (`bloqueante` | `warning`; por defecto
   `bloqueante`) y `Verificación` (`yes` = la verificación existe — el chequeo vive en el archivo de
   checks de su estándar, que se localiza por convención en `scripts/arch/checks/<slug-estándar>.<ext>`,
   o hay evidencia externa registrada en el requisito; `no` = pendiente). **Si el estándar trae el
   formato antiguo** (una tabla `### Criterios de cumplimiento` dentro de cada requisito, sin columna
   `Requisito`, o con rutas/`TODO`/`N/A` en `Verificación` en vez de yes/no), leer esas
   tablas igual y señalarlo como observación (formato de estándar desactualizado) — no bloquea la
   auditoría. **Cada criterio `CR-XXX` es una entrada en la lista de reglas a auditar**,
   contextualizado por el requisito que lo agrupa.

2. **ADRs — solo trazabilidad y huecos.** Listar `docs/adr/*.md`. Para cada criterio auditado, tener a
   mano su ADR de origen para citarlo (el ADR referencia en `emits` los criterios que fija, p. ej.
   `emits: [testing/CR-001]`). Además, detectar **ADR `Accepted` con una regla claramente enforceable
   que no fijó ningún criterio** (`emits: []`): no auditar el ADR como norma, sino anotarlo como
   observación → sugerir emitir el criterio vía `arch-manage`. **Si el ADR no tiene el campo `emits`
   en absoluto** (formato antiguo, previo a esta convención) en vez de `emits: []`, tratarlo igual que
   un ADR sin criterio para esta fase (mismo tratamiento: observación + sugerir emitir vía
   `arch-manage`), pero señalar además que el ADR usa un formato desactualizado (sin `emits`), para no
   confundirlo con una decisión deliberada de no fijar criterios.

3. **AGENTS.md** — leer el/los archivo(s):
   ```bash
   find . -maxdepth 3 -iname "AGENTS.md" -not -path "*/node_modules/*" 2>/dev/null
   ```
   Descomponer el documento en **reglas atómicas y verificables**. Ignorar prosa de contexto sin
   una regla accionable. A cada regla asignarle un identificador estable con el formato
   `AGENTS.md §<sección>` (p. ej. `AGENTS.md §APIs`).

   **Regla duplicada con un criterio existente:** si una regla de `AGENTS.md` repite, en sustancia,
   el mismo contenido normativo que un `CR-XXX` ya extraído en el paso 1 (mismo requisito, mismo
   MUST/SHOULD), **no** crear una entrada separada en la lista de reglas a auditar. Fusionarla bajo
   ese `CR-XXX`: agregar `AGENTS.md §<sección>` como fuente adicional (junto al estándar) en el campo
   `Fuente` del hallazgo, y evaluarla una sola vez. Solo tratarla como regla independiente si añade
   una condición, alcance o matiz que el criterio no cubre. Este criterio de fusión se aplica siempre
   — no queda a discreción de cada corrida, precisamente para que dos auditorías del mismo repo no
   difieran en el conteo de hallazgos por esta razón.

4. **Contexto de stack** — leer `## Stack tecnológico` en `AGENTS.md` si existe, para saber
   lenguajes/frameworks y afinar los patrones de búsqueda (evita falsos negativos por buscar en el
   lenguaje equivocado).

Construir una **lista de reglas a auditar**: cada entrada = un **criterio de cumplimiento**
(`<estándar>/CR-XXX`, con el requisito que lo agrupa) o una regla de AGENTS.md, con su enunciado, su ADR
de origen si aplica, su `Enfoque` (bloqueante/warning) si es un criterio, y su prioridad tentativa (ver
criterios abajo).

### Clasificar aptitud para fitness function

Para cada criterio (y regla), marcar si es **apto** para una fitness function, es decir, si su
cumplimiento es **objetivo y automatizable**. Normalmente el criterio ya lo declara en su columna
`Automatizable` (`yes`); usarla y, si falta o es un ADR sin criterio, evaluarlo:

- **Apto** — se puede escribir un chequeo determinista que pase/falle sin juicio humano. Ejemplos: "las APIs son GraphQL, no REST", "la capa de dominio no importa infraestructura", "ningún módulo excede X dependencias", "cobertura ≥ 80%", "no se usa `any`".
- **No apto** — depende de criterio humano o evidencia externa al repo. Ejemplos: "el código debe ser legible", "las decisiones se toman por consenso", "usar TLS en producción". Estos se auditan por inspección o se marcan *No verificable*; **no** se sugiere fitness function.

Registrar la aptitud de cada criterio — se usa en la Fase 2B y en la sección de fitness functions del informe.

---

## Fase 2 — Verificar contra el repo (el "ser")

Para cada regla, reunir evidencia **a favor y en contra**. Esta fase incluye ejecutar la fitness
function del estándar cuando exista (Fase 2B): su resultado es la evidencia primaria y la inspección
estática lo complementa localizando los archivos infractores. Elegir la técnica de inspección según
el tipo de regla:

| Tipo de regla | Cómo verificar (ejemplos) |
|---|---|
| Tecnología obligatoria/prohibida (p. ej. "usar GraphQL, no REST") | `grep -rn` de patrones de la tecnología permitida y de la prohibida; contar ocurrencias y ubicarlas |
| Estructura / capas (p. ej. "Controller → Service → Repository") | `find` de carpetas esperadas; detectar archivos que saltan capas |
| Convención de nombres/ubicación | `grep`/`find` sobre rutas y nombres de archivo |
| Dependencia permitida/prohibida | Leer manifiestos (`package.json`, `pom.xml`, `pyproject.toml`, `*.csproj`, `go.mod`, `Cargo.toml`) |
| Prohibiciones de código (p. ej. "no usar `any`", "no `console.log`") | `grep -rn` del antipatrón |
| Límites de módulo / imports | `grep -rn` de imports que cruzan fronteras no permitidas |

Guías de verificación:
- **Cuantificar cuando sea posible:** "92% del código usa GraphQL; 3 endpoints REST nuevos". Los porcentajes y conteos hacen el hallazgo accionable.
- **Recolectar rutas exactas** de los archivos infractores — son la parte más útil del informe.
- **No correr el build ni la suite completa.** La única ejecución permitida son las fitness functions detectadas (Fase 2B). Si una regla solo se puede confirmar mirando un entorno externo (p. ej. "TLS en producción"), marcarla **❔ No verificable** y anotar qué evidencia haría falta.
- **No inventar incumplimientos.** Si no hay evidencia en contra, el estado es ✅ Cumplido.

### Estados de cada criterio

- **✅ Cumplido** — sin evidencia en contra (o la fitness function pasa).
- **⚠️ Parcialmente cumplido** — mayoría cumple pero hay excepciones (como el ejemplo de `api/CR-001`, el criterio de protocolo del requisito `api/api-protocol`).
- **❌ Incumplido** — la regla no se respeta o hay infracciones sustanciales (o la fitness function falla).
- **❔ No verificable** — no se puede determinar por inspección estática ni con una fitness function ejecutable.

### Prioridad de cada hallazgo

Asignar prioridad al **incumplimiento** (no al criterio en abstracto):

- **🔴 Alta** — incumple un criterio `MUST`/`REQUIRED`/`SHALL` de un estándar `Active` de amplio impacto, introduce riesgo de seguridad/integridad, o infringe una regla de AGENTS.md obligatoria/bloqueante.
- **🟡 Media** — incumple un criterio relevante de alcance acotado (o un `SHOULD` de peso), o desviación parcial sin riesgo inmediato.
- **⚪ Baja** — convenciones, estilo, un `SHOULD`/`MAY` de bajo impacto; desviaciones tolerables.

El **`Enfoque`** del criterio modula la prioridad, a igualdad de término RFC 2119: un criterio
`bloqueante` incumplido pesa más (tiende a Alta/Media) que un criterio `warning` incumplido (tiende a
Media/Baja), coherente con que un `warning` no cambia el veredicto ejecutable (ver Fase 2B).

Un criterio en estado ✅ Cumplido no genera un **hallazgo** (no lleva su propia entrada bajo
🔴/🟡/⚪ en la Fase 3), pero sí cuenta en la tabla del **Resumen**. Para ubicarlo en una fila de esa
tabla (Alta/Media/Baja), usar la **prioridad potencial** del criterio — la que tendría si estuviera
incumplido, según los mismos criterios de arriba (término RFC 2119, `Enfoque`, alcance e impacto) —
no la prioridad de un hallazgo real, que no existe en este caso. Lo mismo aplica a un criterio
❔ No verificable: se ubica por su prioridad potencial, y además se detalla aparte en la sección
`## Reglas no verificables por inspección estática`.

---

## Fase 2B — Fitness functions

Para cada criterio **apto** (marcado en la Fase 1), determinar si ya existe una fitness function y, si
existe, ejecutarla para validar el cumplimiento. Las fitness functions son **por criterio** (`CR-XXX`).

### 0. Preferir el runner de validaciones de arquitectura

Antes de ejecutar chequeos uno por uno, comprobar si el proyecto tiene un **runner** que corre
todas las validaciones de arquitectura de una vez (lo crea `arch-manage`, escrito en el lenguaje del
stack del repo — Node, Python, PHP…, o shell como último recurso):

```bash
ls scripts/arch/verify.* scripts/arch/checks/* 2>/dev/null
```

- **Si existe**, es la vía preferida: una sola corrida acotada valida todos los criterios con fitness
  function. Ejecutar el runner con el runtime del stack (`node scripts/arch/verify.mjs`,
  `python scripts/arch/verify.py`, etc., o el alias nativo del repo — `npm run arch`, target de
  `Makefile`, etc.) aplicando las mismas cautelas del paso 2 (no correr build/suite completa; si
  requiere instalar dependencias pesadas, preguntar antes). Cada archivo de `checks/` agrupa las
  fitness functions de **un estándar** (`checks/<slug-estándar>.<ext>`, p. ej. `checks/testing.mjs`) e
  imprime una línea de protocolo por criterio — `PASS|FAIL|WARN <estándar>/CR-XXX — detalle`:
  **mapear cada línea a su criterio por esa referencia** y alimentar ese resultado al estado del
  criterio en la Fase 2. Para auditar un solo estándar, el runner acepta su slug como argumento
  (`node scripts/arch/verify.mjs testing`). El resumen final (criterios PASS / WARN / FAIL) y el
  código de salida agregado resumen la salud arquitectónica ejecutable: el runner sale con código ≠ 0
  **solo** si falla algún criterio `bloqueante`; un criterio `warning` que falla se reporta como `WARN`
  pero **no** cambia el código de salida ni el veredicto ejecutable.
- Un criterio con `Verificación: yes` cuyo archivo de checks (`checks/<slug-estándar>.<ext>`) **no**
  existe, o cuya referencia `CR-XXX` no aparece en la salida de la corrida, se ejecuta individualmente
  (pasos 1-2) y además se anota como observación: la fitness function no está registrada en el archivo
  de checks de su estándar (sugerir corregirlo vía `arch-manage`).
- **Si no existe** el runner, continuar con la detección y ejecución individuales (pasos 1-2) y,
  si hay dos o más fitness functions sueltas, **sugerir crear el runner** (`scripts/arch/verify.<ext>`
  en el lenguaje del stack) vía `arch-manage`, para que en adelante todas se ejecuten con un solo
  comando.

### 1. Detectar fitness functions existentes

**Primero, leer la fila del criterio (`CR-XXX`) en la tabla `## Criterios de cumplimiento` de su estándar** (lo escribe
`arch-manage`). Es la fuente más fiable: si `Verificación: yes`, localizar el archivo de checks de su
estándar **por convención** (`scripts/arch/checks/<slug-estándar>.<ext>`, p. ej. `checks/testing.mjs`),
ejecutar ese estándar vía el runner con su slug (`node scripts/arch/verify.mjs testing`) y leer la
línea del `CR-XXX` (salvo que la corrida del paso 0 ya lo haya cubierto); si no hay archivo de checks,
la verificación es evidencia externa — buscarla en el requisito. Si `Automatizable: yes` pero
`Verificación: no`, el criterio es apto pero aún no tiene fitness function → va a las sugerencias
(paso 3). Si `Automatizable: no`, no automatizarlo.

Si la fila no existe o está incompleta (estándares antiguos, o ADR sin criterio), leer
[`references/fitness-function-heuristics.md`](references/fitness-function-heuristics.md) para el
**rastreo heurístico** por señales del stack (tabla de herramientas típicas por ecosistema + comandos
`grep`/`find` genéricos) y mapear lo encontrado al criterio que valida.

### 2. Ejecutar las fitness functions detectadas

Ejecutar **solo** el chequeo de arquitectura, no la suite completa, usando el comando más acotado disponible:

- Preferir el runner (`node scripts/arch/verify.mjs` o el equivalente del stack, con el slug del estándar para acotar; paso 0) cuando exista; si no, el archivo de checks del estándar localizado por convención (`scripts/arch/checks/<slug-estándar>.<ext>`), el `README`, `package.json` (script `arch`/`fitness`/`depcruise`) o `Makefile`.
- Ejemplos: `npx depcruise --config .dependency-cruiser.js src`, `mvn -Dtest=*ArchTest test`, `lint-imports`, `pytest -k arch`.
- Si el comando exacto es ambiguo o requiere instalar dependencias pesadas, **preguntar al usuario** con la herramienta de preguntas estructuradas antes de ejecutarlo, mostrando el comando propuesto. No ejecutar nada destructivo ni que modifique el repo.
- Capturar: comando corrido, resultado (**PASS / FAIL / WARN**), y las líneas relevantes de la salida (violaciones concretas con sus rutas). Un criterio `warning` que falla se reporta como **WARN** (no cambia el veredicto ejecutable). Si falla por entorno (falta un runtime/dependencia), registrar **No ejecutable** con el motivo, no marcarlo como incumplimiento.

Alimentar el resultado al estado del criterio en la Fase 2 (PASS → refuerza ✅; FAIL/WARN → ❌/⚠️ con las violaciones como `Incumplimientos`, ponderando el `Enfoque` en la prioridad).

### 3. Criterios aptos SIN fitness function

Si un criterio es **apto** pero no tiene fitness function (`Verificación: no`), añadirlo a la lista de **sugerencias**. Para cada uno proponer:
- **Qué medir** — la característica arquitectónica a comprobar (la `Descripción` del criterio).
- **Herramienta sugerida** — según el stack (tabla de [`references/fitness-function-heuristics.md`](references/fitness-function-heuristics.md)).
- **Esbozo** — una frase de cómo sería el chequeo (p. ej. "regla dependency-cruiser: prohibir imports desde `src/api/**` que no sean del esquema GraphQL").

Esto no crea la fitness function (eso es otra tarea); solo la **recomienda** en el informe. Sugerir
además dejar constancia en el criterio: mantener su columna `Verificación: no` (vía `arch-manage`), con el esbozo en el informe,
para que la próxima auditoría la descubra sin heurística. Al crearla, `arch-manage` investigará la forma
más común/eficiente de verificarla, instalará lo necesario si hace falta, registrará el chequeo en el
archivo de checks de su estándar (`scripts/arch/checks/<slug-estándar>.<ext>`, con la trazabilidad
`CR-XXX` en comentarios y líneas de salida, y el enfoque `bloqueante`/`warning` implementado dentro del
chequeo) y marcará `Verificación: yes`, quedando incluida en la ejecución del runner
(`scripts/arch/verify.<ext>`).

---

## Fase 3 — Redactar el informe

Esta fase aplica a una **Nueva auditoría desde cero**. Para revalidaciones, seguir en cambio el
flujo de `Comportamiento en Revalidación` descrito en la Fase 0 — no se reescribe el informe.

1. Calcular la fecha de hoy:
   ```bash
   date +%F
   ```
2. Asegurar el directorio: `docs/audits/` (crearlo si no existe).
3. Leer `assets/audit-template.md` y redactar `docs/audits/arch-audit-<hoy>.md` siguiendo su estructura:
   - Encabezado con fecha, repositorio, alcance, método y **veredicto** (`✅ Conforme | ❌ No conforme | ⚠️ Conforme con observaciones`, siguiendo el patrón de `trace-validate`).
     - **Alcance:** ser específico — indicar cuántos criterios se auditaron y sobre cuántos estándares/requisitos de contexto, el desglose por estado de los excluidos, más las fuentes de AGENTS.md consideradas. Ejemplo: `14 criterios en 4 estándares · 1 Draft, 1 Superseded excluidos + AGENTS.md raíz`.
     - **Método:** no es un texto fijo — describir en una frase corta qué se usó realmente en esta auditoría: las técnicas de inspección aplicadas (p. ej. `grep`, lectura de manifiestos) y las fitness functions ejecutadas. Aclarar que no se corre el build ni la suite completa.
   - **Resumen** con la tabla de conteos por prioridad y estado, seguida de 1-3 frases con la lectura global de la salud arquitectónica del repo.
   - Hallazgos **agrupados por prioridad** (alta → media → baja). Por cada hallazgo: el criterio (con su referencia `<estándar>/CR-XXX`, el requisito que lo agrupa, el nombre de su estándar de dominio, su ADR de origen y su `Enfoque` bloqueante/warning) o la regla de AGENTS.md incumplida, `Estado`, `Evidencias` (✔ a favor / ✖ en contra), `Incumplimientos` (rutas de archivos), y `Acción sugerida`. Si el criterio tiene fitness function, incluir en `Evidencias` el resultado de ejecutarla (PASS/FAIL/WARN + comando).
   - **Fitness functions**: indicar si existe el **runner** (`scripts/arch/verify.<ext>`, en el lenguaje del stack del repo) y su resultado conjunto (criterios PASS / WARN / FAIL); una sub-tabla de las **existentes** (criterio `CR-XXX`, enfoque, herramienta, comando, si está registrada en el archivo de checks de su estándar, resultado PASS/FAIL/WARN/No ejecutable) y una lista de las **sugeridas** (criterio apto sin fitness function → qué medir, herramienta y esbozo). Si hay dos o más fitness functions sueltas y no existe el runner, recomendarlo aquí.
   - Sección de reglas **No verificables**.
   - Sección de **Decisiones sin criterio** (opcional): ADR `Accepted` con regla enforceable que no fijó ningún criterio (`emits: []`) → sugerir emitirlo vía `arch-manage`.
   - Sección de **Observaciones** (opcional): notas operativas que no son un hallazgo de incumplimiento (fitness function no registrada en el archivo de checks de su estándar, runner o checks escritos en un lenguaje ajeno al stack del repo, estándar/ADR en formato antiguo, dependencia rechazada en la Fase 3.5, etc.) — es el destino de cualquier "señalar/anotar como observación" mencionado en las fases anteriores.
4. **Nunca sobrescribir** un informe anterior: el nombre lleva la fecha para conservar el histórico. Si ya existe un `arch-audit-<hoy>.md` del mismo día, actualizarlo (no duplicar).

El formato exacto de cada hallazgo (qué campos lleva y en qué orden) es el que ya trae
`assets/audit-template.md` — no se repite aquí; seguir esa plantilla al redactar.

---

## Fase 3.5 — Verificar dependencias de las normas auditadas

Comprobar si las dependencias concretas que implican los estándares/ADR auditados están instaladas y
configuradas en el proyecto.

- **En una nueva auditoría:** se ejecuta después de generar el informe (Fase 3) y antes de
  confirmar (Fase 4); si falta algo y el usuario rechaza instalarlo, se deja constancia editando
  el informe recién escrito (aún no confirmado).
- **En una revalidación:** se ejecuta como parte del paso 2-3 de `Comportamiento en Revalidación`
  (Fase 0), **antes** de escribir la entrada en `## Revalidaciones`; su resultado se incorpora como
  un cambio evidenciado más dentro de esa única entrada — no se escribe ni se pregunta por separado.

Leer [`references/dependency-verification.md`](references/dependency-verification.md) para el flujo
completo: qué contar como dependencia, cómo comprobar si ya existen, la pregunta exacta al usuario, y
qué hacer según acepte o rechace.

---

## Fase 4 — Confirmar

Al terminar, mostrar al usuario:
- Ruta del informe (nuevo `arch-audit-<hoy>.md`, o el mismo archivo si fue revalidación).
- El veredicto vigente (con la fecha/hora de revalidación si aplica) y el conteo de hallazgos por prioridad (p. ej. "🔴 2 · 🟡 3 · ⚪ 1").
- Resumen de fitness functions: cuántas se ejecutaron (PASS/FAIL/WARN) y cuántas se sugiere crear.
- Resultado de la verificación de dependencias (Fase 3.5): cuáles faltaban, si se instalaron o quedaron señaladas en el informe.
- Si fue revalidación: fecha/hora registrada y un resumen de los cambios evidenciados que se añadieron a `## Revalidaciones` (resueltos, nuevos, regresiones, o "sin cambios").

Ofrecer, sin ejecutarlo salvo que el usuario lo pida, el siguiente paso lógico: documentar
excepciones o emitir criterios faltantes con `arch-manage`, crear las fitness functions sugeridas, o
planificar la remediación de los hallazgos de alta prioridad.

---

## Notas de comportamiento

- **Auditar, no arreglar.** Este skill diagnostica y propone; no modifica código de la aplicación ni "corrige" incumplimientos por iniciativa propia. Tampoco crea las fitness functions: las **sugiere**. La única excepción es instalar/configurar dependencias faltantes (Fase 3.5), y solo con aprobación explícita del usuario.
- **El criterio de cumplimiento (CR) es la unidad auditable; el requisito es la agrupación legible y el ADR es contexto.** Se audita el cumplimiento de los criterios (`CR-XXX`) de los estándares de dominio (y reglas de AGENTS.md), criterio por criterio, según su término RFC 2119 y su `Enfoque` (bloqueante/warning), agrupados por su requisito y citando el ADR de origen para trazabilidad. No se audita un ADR como si fuera la norma.
- **Ejecución acotada.** Solo se ejecutan las fitness functions / chequeos de arquitectura detectados, con comandos de solo lectura. Nunca correr scripts de propósito desconocido, ni comandos que desplieguen o modifiquen el repo más allá de la instalación de dependencias aprobada en la Fase 3.5; ante la duda, preguntar antes de ejecutar.
- **Rutas reales, no ejemplos.** Los `src/UserController.php` del ejemplo son ilustrativos; en el informe deben ir siempre rutas verdaderas del repo auditado.
- **No inventar reglas ni veredictos.** Solo se auditan normas que existan en `docs/standards/` o `AGENTS.md`. Ante evidencia ambigua, preferir ⚠️ o ❔ y explicar la duda, en vez de afirmar un incumplimiento.
- **Priorizar señal sobre volumen.** Mejor pocos hallazgos sólidos y bien evidenciados que una lista larga de detalles triviales.
- **Sin estándares ni AGENTS.md:** si no hay ninguna fuente normativa, informarlo y sugerir `arch-init` — bootstrapea `AGENTS.md`, `.agents/MEMORY.md`, `docs/adr/` y `docs/standards/`, e invoca `arch-discover` por su cuenta si el repo ya tiene implementación — en vez de crear un `AGENTS.md` a mano; no fabricar un informe vacío de reglas inventadas. Si solo hay ADR pero ningún criterio, señalar que las decisiones no han emitido reglas auditables y sugerir emitirlas vía `arch-manage`.
- **Informe inmutable, revalidaciones aparte.** El contenido escrito al crear el informe (resumen, hallazgos, fitness functions, reglas no verificables) no se modifica nunca. Cada revalidación se documenta como una entrada nueva en `## Revalidaciones`; el único campo del contenido original que una revalidación actualiza es `Veredicto` en la cabecera.

---

## Archivos del skill (contexto progresivo)

Este `SKILL.md` contiene el flujo completo de las cinco fases. El rastreo heurístico de fitness
functions y el mecanismo de verificación de dependencias viven en `references/`; el formato de cada
hallazgo vive en `assets/`. **Leerlos solo cuando la fase correspondiente lo pida**:

- [`references/fitness-function-heuristics.md`](references/fitness-function-heuristics.md) — tabla de herramientas típicas por ecosistema + comandos de rastreo genérico. Leer en la Fase 2B, paso 1, solo cuando la fila del criterio no exista o esté incompleta.
- [`references/dependency-verification.md`](references/dependency-verification.md) — flujo completo (extraer, comprobar, preguntar, instalar o dejar constancia) para las dependencias que implican las normas auditadas. Leer en la Fase 3.5.
- [`assets/audit-template.md`](assets/audit-template.md) — plantilla del informe, incluido el formato exacto de cada hallazgo. Leer en la Fase 3, al redactar.

---

## Referencias

- [Architecture Decision Records](https://github.com/joelparkerhenderson/architecture-decision-record)
- *Building Evolutionary Architectures* (Ford, Parsons, Kua) — concepto de fitness functions.
- Skills relacionados en este repositorio: `arch-init` (bootstrapear el harness cuando no hay ninguna fuente normativa), `arch-manage` (crear/actualizar ADR y estándares), `arch-discover` (descubrir decisiones y reglas implícitas).
