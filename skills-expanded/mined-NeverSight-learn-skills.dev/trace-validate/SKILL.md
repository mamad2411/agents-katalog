---
name: trace-validate
description: >-
  Generar un reporte de trazabilidad que cruza los criterios de aceptación de un artefacto —una historia de usuario (US-XXX), una tarea de mantenimiento (WI-XXX), un feature ya implementado (FT-XXX) o cualquier documento cuyos criterios tengan identificador codificado (AC-001, 1.1, R-3…)— contra los casos y artefactos de prueba del repositorio. Por cada criterio indica qué lo cubre, su estado (Cubierto / Parcial / No cubierto), si la prueba se ejecutó y con qué resultado, y cierra con un veredicto de cobertura. No corre la suite: delega la ejecución en quality-check. Activar siempre que el usuario pida validar cobertura, generar una matriz o reporte de trazabilidad, verificar que los criterios de aceptación están probados, comprobar si un trabajo o un feature está cubierto por pruebas, o mencione "trazabilidad", "matriz de cobertura" o "validar criterios de aceptación", aunque no nombre el formato exacto.
license: MIT
---

# Skill: Validar trazabilidad de un trabajo

Genera un **reporte de trazabilidad** que cruza los **criterios de aceptación** de un trabajo contra los **casos de prueba** y los **artefactos de prueba automatizada** (unit, integración, e2e) presentes en el repositorio, y emite un **veredicto** sobre si el trabajo queda cubierto.

El trazado primario es para **historias de usuario** (`US-XXX`) con sus **criterios de aceptación**. Sirve igual para cualquier otro artefacto que tenga criterios con **identificador codificado** — el formato es indiferente (`AC-001`, `1.1`, `R-3`…) y se usa **verbatim**, sin normalizar (ver [Tipos de trabajo y criterios](#tipos-de-trabajo-y-criterios)). Es el mismo contrato que produce `test-define`.

> **Qué hace:** lee, mapea, **obtiene los resultados de pruebas delegando en `quality-check`** y reporta. Es una actividad de **verificación**, no de desarrollo.
>
> **No ejecuta pruebas por sí mismo.** La ejecución de la batería de pruebas se **delega en `quality-check`**: si existe una corrida previa fresca de `quality-check` (sin cambios en el código desde entonces), se **reutilizan** sus resultados; si no, se invoca `quality-check` en modo `tests-only` para producirlos. Ver [Resultados de pruebas: delegación en quality-check](#resultados-de-pruebas-delegación-en-quality-check).
>
> **Reporte idempotente.** Si no hubo **cambios en los archivos** (código, criterios ni pruebas) desde la última vez que se generó el `trace-report.md`, **no se genera un documento nuevo**: se devuelven los mismos resultados del reporte existente. Ver [Reutilización del reporte (idempotencia)](#reutilización-del-reporte-idempotencia).
>
> **Qué NO hace:** no escribe ni modifica código de aplicación, no escribe nuevos tests (eso es de `quality-specialist` vía `work-implement`), no edita la especificación de producto (README de la US, `TK-XXX`, `WI-XXX`, `FT-XXX`, `validation.md`, ADRs), **ni corre la suite de pruebas directamente**. Lo único que produce es el **reporte de trazabilidad**. Lo que no se puede determinar de las fuentes va a **Observaciones** o se pregunta al usuario — nunca se inventa cobertura ni resultados.

---

## Alcance del informe

El informe de este skill cubre **un artefacto concreto y sus criterios de aceptación**. La pregunta es «¿cada criterio de *este* trabajo está probado?», así que el universo lo definen los criterios del artefacto, no los archivos que cambiaron ni el repositorio completo.

Consecuencias prácticas:

- **Se validan todos los criterios del artefacto**, aunque en esta rama no se haya tocado el código de alguno de ellos: un criterio cuya prueba nunca se escribió sigue siendo un hueco.
- **No se reportan pruebas ni código ajenos al artefacto.** Tests de otros trabajos, cobertura global o fallos en módulos que no mapean a ningún criterio de este artefacto no entran en la matriz — a lo sumo van a «Observaciones y pendientes».
- **Si la rama abarca varios trabajos**, se valida uno por corrida, con su propio `trace-report.md` junto a su artefacto. Los resultados de pruebas sí son compartidos (vienen de la corrida de `quality-check`), pero el **mapeo** es por artefacto.
- **La clave de frescura es de rama, no de artefacto.** El fingerprint de la idempotencia cubre todo el árbol, así que un cambio en *otro* trabajo de la misma rama invalida también este `trace-report.md` y fuerza a regenerarlo. Es conservador a propósito: prefiere revalidar de más antes que devolver un reporte que ya no corresponde al código.

---

## Subagente

**Si el proyecto define el subagente `quality-specialist`, ejecutar este skill bajo ese subagente** (es el mismo agente que escribe los tests en el cierre de `work-implement`, por lo que es el contexto natural para validarlos). Si no existe en el proyecto, ejecutar el flujo normalmente.

---

## Tipos de trabajo y criterios

El tipo se determina por el identificador que indique el usuario o por la ruta de trabajo. Cada tipo fija de dónde se leen los criterios de aceptación y con qué códigos se traza.

| Tipo | Identificador | Dónde viven los criterios | Códigos a trazar |
|------|---------------|---------------------------|------------------|
| **Historia de usuario** | `US-XXX` | Sección **Criterios de aceptación** del `README.md` de la US (lista plana, habitualmente `AC-XXX`) | El identificador de cada criterio, en el orden en que aparecen |
| **Tarea de mantenimiento** | `WI-XXX` | Sección **## Criterios de aceptación** del `README.md` del WI (`WI-XXX-[kebab]/README.md`) | El identificador de cada criterio, en el orden en que aparecen |
| **Feature (funcionalidad ya implementada)** | `FT-XXX` | Sección **## Criterios de aceptación** del `README.md` del feature (`docs/specs/features/FT-XXX-[slug]/README.md`) | El identificador de cada criterio, en el orden en que aparecen |
| **Cualquier otro artefacto de especificación** | Ruta o nombre que indique el usuario | La sección de criterios del documento (puede llamarse «Criterios de aceptación», «Requisitos», «Acceptance Criteria»…) | El identificador de cada criterio, tal como aparece |

> **El requisito no es el formato, es que exista identificador.** En todo el flujo, «criterio» se refiere al identificador **tal como está escrito en el artefacto** — `AC-012`, `1.3`, `R-3`, `CA-07` son todos válidos. **Nunca normalizar ni renombrar**: el vínculo de trazabilidad debe ser buscable literalmente tanto en el artefacto como en los TCs que produjo `test-define`. Si el trabajo **no tiene criterios**, o los tiene sin identificador, no hay nada que trazar → **bloquear** (ver «Cuándo bloquear»).

> **FT — validar cobertura de funcionalidad ya implementada.** Un `FT-XXX` es el
> registro de una funcionalidad **ya implementada** (inferida de código legacy por el
> análisis de `work-research`, o simplemente el registro de funcionalidad existente),
> no trabajo por construir. Validarlo responde: *¿esa funcionalidad ya existente está
> cubierta por pruebas?* Un criterio **No cubierto** significa que ese comportamiento
> **carece de pruebas** (un hueco a cerrar escribiendo tests), **no** que falte código
> funcional. Sus casos de prueba documentados viven en
> `docs/specs/features/FT-XXX-[slug]/test-cases/`, igual que en una US o un WI.

---

## Cómo preguntar al usuario

Cuando este skill indique **preguntar, pedir, confirmar o validar** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** del cliente (opciones tappables o selector) en lugar de prosa libre. Reglas:

- **Opciones cortas y mutuamente excluyentes** (2-4 por pregunta) cuando la respuesta admita categorías.
- **No repreguntar** lo que ya esté respondido en el contexto de la sesión o en los documentos del repo.
- **Fallback:** si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3...).

---

## Resolución de idioma

El idioma del reporte se decide en este orden; detenerse en el primer paso que aplique:

1. Si en el contexto de la sesión existe una preferencia de idioma del usuario, usarla.
2. Si no, usar el idioma del mensaje del usuario y **preguntar al usuario si desea persistir su preferencia de idioma en la memoria**.
3. Si no se puede inferir, **preguntar al usuario** qué idioma prefiere y, tras su respuesta, **preguntar si desea persistir su preferencia de idioma en la memoria**; no decidir el idioma por cuenta propia.

La salida y los mensajes de error de las herramientas de prueba no se traducen.

---

## Información requerida antes de generar el reporte

No inventar nada. Si un dato no es explícito, obtenerlo del repo o preguntar al usuario.

| Dato | Cómo obtenerlo | Si no está disponible |
|------|----------------|-----------------------|
| **Trabajo a validar** | Indicado por el usuario o inferido de la ruta de trabajo; determinar el tipo (`US-XXX` / `WI-XXX` / `FT-XXX` / otro artefacto) | Preguntar qué trabajo validar; sin él no se puede generar el reporte |
| **Criterios de aceptación** | Según el tipo (ver [Tipos de trabajo y criterios](#tipos-de-trabajo-y-criterios)) | Si el trabajo no tiene criterios de aceptación: **bloquear** y reportar — sin criterios no hay nada que trazar |
| **Casos de prueba** | **Fuente primaria:** la carpeta `test-cases/` **junto al artefacto** y su índice `test-cases/README.md`, más la línea `Casos de prueba:` que `test-define` deja bajo cada criterio. **Fallback:** inferir desde los tests del repo | Si no hay casos documentados, derivar la cobertura desde los artefactos de prueba del repo |
| **Artefactos de prueba** | Buscar en el repo archivos de test unit / integración / e2e relacionados con el trabajo (ver el Paso 2 en `references/flow.md`) | Si no se encuentran, marcar criterios sin artefacto como `No cubierto` y dejar Observación |
| **Resultados de pruebas** | **Delegados en `quality-check`**: caché fresca `test-run.json` o invocación `tests-only` (ver [Resultados de pruebas: delegación en quality-check](#resultados-de-pruebas-delegación-en-quality-check)) | Si `quality-check` no puede ejecutarlas (sin stack, entorno sin correr, no disponible en la sesión) o el usuario declina la delegación: las filas **con artefacto** van con `Ejecución = —` y `Resultado = No ejecutado`, y el motivo a «Observaciones y pendientes» |
| **Alcance** | Todo el trabajo por defecto; el usuario puede acotar a ciertos criterios | Si es ambiguo, preguntar |

> Leer **siempre** el documento de criterios completo (el `README.md` del trabajo, o el archivo del artefacto externo) antes de generar el reporte. No asumir criterios que no estén escritos.

---

## Flujo

Resumen de los pasos. El detalle íntegro de cada paso está en **`references/flow.md`** (leerlo antes de ejecutar el flujo).

0. **Comprobar frescura del reporte** — si ya existe `trace-report.md` con un fingerprint guardado y no hubo cambios en los archivos desde entonces, **devolver el reporte existente sin regenerarlo** (ver [Reutilización del reporte (idempotencia)](#reutilización-del-reporte-idempotencia)). Solo si hay cambios (o el usuario pide revalidar) continuar con los pasos siguientes.
1. **Localizar y leer el trabajo** — resolver tipo y ubicación; extraer todos los criterios con su identificador **verbatim**. Sin criterios (o sin identificador) → bloquear (ver «Cuándo bloquear»).
2. **Inventariar casos y artefactos** — leer la carpeta `test-cases/` del artefacto y su índice como fuente primaria, y clasificar los tests del repo por tipo, con ruta y criterio.
3. **Mapear cobertura fila a fila** — expandir cada criterio en sus filas (criterio × TC × tipo declarado), rellenar `Evidencia` y derivar el estado del criterio (ver «Estados de cobertura») con sus observaciones. No forzar mapeos inciertos.
4. **Obtener resultados de pruebas (delegando en `quality-check`)** — reutilizar la caché `test-run.json` si está fresca, o invocar `quality-check` en modo `tests-only`; mapear por suite a las filas y rellenar `Ejecución` (`quality-check` / `Manual` / `—`) y `Resultado` (`Paso` / `Fallo` / `No ejecutado` / `No cubierto` / `N/A`). **No** correr pruebas directamente. Nunca fabricar resultados (ver [Resultados de pruebas: delegación en quality-check](#resultados-de-pruebas-delegación-en-quality-check) y `references/flow.md`).
5. **Redactar el reporte** desde `assets/trace-report-template.md` (leerla antes de redactar): cabecera, Resumen (prosa con la procedencia + tabla de indicadores), **cobertura por criterio** (una fila por criterio, con su Estado), **matriz de trazabilidad** (una fila por criterio × TC × tipo declarado, con Evidencia, Ejecución y Resultado) y, si los hay, los caveats globales en «Observaciones y pendientes». Ver [Vistas del reporte](#vistas-del-reporte-cobertura-por-criterio-y-matriz).
6. **Emitir el veredicto** (ver «Veredicto») respondiendo si todos los criterios quedan cubiertos.
7. **Entregar y guardar** el reporte en la ubicación del tipo (ver «Ubicación de archivos»), **grabando el fingerprint** del estado actual para la próxima comprobación de frescura; no modificar otros artefactos.

---

## Estados de cobertura

| Estado | Cuándo aplicarlo |
|--------|------------------|
| **Cubierto** | El criterio tiene al menos un caso de prueba **y** el artefacto que le corresponde, y lo valida de forma completa. Si se ejecutó automáticamente, pasó. **Un criterio cuyos TCs son `Manual` por diseño también es Cubierto** si esos TCs lo validan por entero — ver la nota de abajo. |
| **Parcial** | El criterio está cubierto solo en parte: hay prueba pero no abarca todo el criterio, el artefacto existe pero no se pudo ejecutar, el resultado fue parcial, existe solo validación manual **no declarada como tal** (TC automatizable aún sin automatizar), o la suite que agrupa su test dio `FAIL` pero no se pudo aislar si el test específico del criterio fue el que falló (ver «Mapeo a la matriz» más abajo). Detallar el límite en Observaciones. |
| **No cubierto** | No existe caso de prueba ni artefacto que valide el criterio, o la prueba asociada **falló** y se pudo aislar que fue la suya. |

> **Cobertura ≠ ejecución.** Que exista prueba que valida el criterio es una cosa; que haya corrido y con qué resultado, otra. Un criterio cuya prueba **falló** —y se pudo aislar que fue la suya— se reporta **No cubierto** con el fallo en Observaciones; si la suite falló pero no se puede aislar el test, es **Parcial** (ver «Mapeo a la matriz»).
>
> **El `Estado` del TC filtra la cobertura.** `test-define` guarda cada TC con `Estado: Draft | Ready | Obsolete`. Un TC **`Obsolete`** no cuenta como cobertura (dejar Observación); uno **`Draft`** cuenta como cobertura **Parcial** (aún no está listo para respaldar el criterio); solo los **`Ready`** cuentan como cobertura plena. Si el TC no trae el campo, tratarlo como `Ready`. Esto es distinto del `Estado:` del **artefacto**, que este skill no exige (ver «Cuándo bloquear»).
>
> **Manual por diseño vs. pendiente de automatizar.** `test-define` distingue los dos casos en el campo **Tipo de prueba** del TC: `Manual` significa *no se automatiza por decisión de diseño*; cualquier otro valor (`Unit`, `Integration`, `API Test`, `Visual Test`, `E2E`) significa *debería existir artefacto automatizado*. Respetar esa declaración: un criterio con TCs `Manual` que lo cubren por completo es **Cubierto** (sus filas van con `Ejecución = Manual` y `Resultado = N/A`), no una deuda; un criterio con TCs automatizables **sin** artefacto es **Parcial** o **No cubierto**. No penalizar una decisión de diseño ni disimular una automatización pendiente.
>
> **Un TC con varios tipos declarados se cubre por tipo.** Si un TC declara `Unit, E2E` y solo existe el test unitario, el criterio **no** es `Cubierto`: la fila `E2E` de la matriz queda en `No cubierto` y el criterio baja a **Parcial**, con el tipo faltante nombrado en Observaciones. La matriz muestra esa asimetría fila a fila (ver [Vistas del reporte](#vistas-del-reporte-cobertura-por-criterio-y-matriz)).

---

## Vistas del reporte: cobertura por criterio y matriz

El reporte tiene **dos tablas complementarias**, no una. Separarlas evita el problema de meter en una sola fila
información de granularidades distintas (un criterio puede tener varios TCs, y un TC varios tipos de prueba).

El **Resumen** las precede con una tabla de indicadores de **cuatro** filas —criterios de aceptación,
cubiertos, parciales, no cubiertos— cuyos tres últimos valores deben sumar el total. No lleva indicadores de
pruebas (fallidas, no ejecutadas): esa granularidad ya está en la matriz y mezclar los dos ejes confunde.
La **procedencia** de los resultados y el `result` **por suite** van en la línea «Pruebas» del Resumen;
`test-run.json` no trae un agregado global, así que no se inventa uno.

**1. Cobertura por criterio** — la vista de veredicto. Una fila por criterio:

| Criterio | Descripción | Estado | Observaciones |
|----------|-------------|--------|---------------|
| AC-2.1 | El usuario recibe confirmación por correo | Parcial | E2E declarado en TC-001 sin automatizar |
| AC-2.2 | La plantilla del correo respeta la identidad visual | Cubierto | Validación manual por diseño (TC-004) |

**2. Matriz de trazabilidad** — la vista auditable. **Una fila por cada combinación criterio × TC × tipo de
prueba declarado**: si un TC declara `Unit, E2E`, produce dos filas.

| Criterio | TC | Tipo | Evidencia | Ejecución | Resultado |
|----------|-----|------|-----------|-----------|-----------|
| AC-2.1 | TC-001 | Unit | `tests/unit/notify.test.ts` | quality-check | Paso |
| AC-2.1 | TC-001 | E2E | — | — | No cubierto |
| AC-2.2 | TC-004 | Manual | `test-cases/TC-004-revision-visual.md` | Manual | N/A |

Semántica de las columnas:

| Columna | Qué contiene | Valores |
|---------|--------------|---------|
| **Criterio** | Identificador **verbatim** del artefacto, repetido en cada fila suya | `AC-012`, `1.3`, `R-3`… |
| **TC** | Caso de prueba que produjo `test-define` | `TC-XXX` · `—` si el criterio no tiene TC documentado (fila **derivada** de un test hallado, o hueco total) |
| **Tipo** | El `Tipo de prueba` **declarado en el TC**; en filas derivadas, el tipo del artefacto hallado | `Manual` · `Unit` · `Integration` · `API Test` · `Visual Test` · `E2E` · `—` (sin TC y sin artefacto) |
| **Evidencia** | La prueba concreta que respalda la fila | Ruta del artefacto automatizado · ruta del TC para filas `Manual` · `—` si esa intención no está materializada |
| **Ejecución** | **Quién** produjo el resultado | `quality-check` · `Manual` · `—` (no se ejecutó) |
| **Resultado** | Qué dio esa prueba | `Paso` · `Fallo` · `No ejecutado` (hay artefacto, no corrió) · `No cubierto` (no hay evidencia para ese tipo) · `N/A` (manual por diseño) |

> **Por qué se eliminó la columna `Automática`.** Un `Sí` no decía nada útil: no revelaba qué tipo de prueba
> respaldaba el criterio, dónde vivía, ni quién produjo el resultado. `Tipo` + `Evidencia` + `Ejecución` dan
> esa información sin ambigüedad, y la granularidad por tipo hace **visible el hueco** (la fila `E2E` sin
> evidencia) en lugar de esconderlo tras un `Sí` que solo hablaba del test unitario.

> **`Evidencia = —` implica `Ejecución = —` y `Resultado = No cubierto`.** No hay excepción: si no hay
> artefacto, no hubo ejecución ni puede haber resultado. Al revés no: puede haber evidencia con
> `Ejecución = —` y `Resultado = No ejecutado` (el artefacto existe pero `quality-check` no pudo correrlo;
> la razón va a «Observaciones y pendientes»).

> **Criterio sin TC documentado pero con test hallado.** Si el mapeo se infirió desde el repo (fallback del
> Paso 2), la fila se escribe igual con `TC = —` y el **tipo del artefacto hallado**, y se anota en
> Observaciones que el mapeo es inferido, no declarado. Solo el criterio **sin TC y sin artefacto** produce
> la fila vacía `— | — | — | — | No cubierto`.

**Derivación del `Estado` del criterio** a partir de sus filas. Evaluar **en orden** y detenerse en la primera que aplique:

| # | Filas del criterio | Estado |
|---|--------------------|--------|
| 1 | **Ninguna** fila aporta cobertura — todas en `No cubierto`, o el criterio no tiene TC ni artefacto, o sus únicos TCs son `Obsolete` — **o** alguna fila dio `Fallo` **aislado a su test** | **No cubierto** |
| 2 | **Alguna** fila en `No cubierto`/`No ejecutado`, algún TC en `Draft` u `Obsolete` conviviendo con cobertura válida, o un `Fallo` de suite **no aislable** | **Parcial** |
| 3 | **Todas** con `Resultado` ∈ {`Paso`, `N/A`} y todos los TCs en `Ready` (o sin campo `Estado`) | **Cubierto** |

> **Dos destinos de observación, no intercambiables.** La prueba para elegir: *¿se puede atribuir a un
> criterio concreto?* Si sí, va en la **columna `Observaciones`** de la tabla 1; si no, en la **sección
> «Observaciones y pendientes»**. La matriz no lleva columna de observaciones.
>
> | Destino | Qué recibe |
> |---------|------------|
> | **Columna `Observaciones`** (tabla 1) | Tipo declarado sin automatizar · TC en `Draft`/`Obsolete` · `Fallo` no aislable · suite efectiva distinta del tipo declarado · mapeo inferido en vez de declarado · **cobertura apoyada en TCs `Manual`** (aunque sea por diseño: es el caveat que justifica el `⚠️`) · límite de la cobertura |
> | **Sección «Observaciones y pendientes»** | Suite `coverage` en `FAIL` · `workingTreeClean: false` (árbol sucio) · clases de prueba ausentes en el repo · ejecución no delegable y su motivo · tests que no se pudieron vincular con certeza a ningún criterio · tests o fallos ajenos al artefacto |
>
> La sección global **se omite entera** si no hay ninguno. Cuando el skill diga «dejar Observación» sin más,
> aplicar esta prueba.

> **La derivación no es cerrada sobre la matriz: dos datos viven fuera de ella.** (a) el `Estado` del TC
> (`Draft`/`Obsolete`/`Ready`, que viene del propio TC) y (b) si un `Fallo` pudo **aislarse** al test del
> criterio. Ambos se anotan siempre en la columna **Observaciones de la tabla 1** — sin esa anotación, dos
> criterios con filas idénticas quedarían con estados distintos sin explicación. Un `Fallo` no aislable se
> escribe igual (`Resultado = Fallo`) en la matriz; lo que lo distingue es la Observación «suite `X` en
> `FAIL`, no se pudo aislar el test» y el `Estado = Parcial` resultante.
>
> **TCs `Obsolete`.** Sus filas se conservan en la matriz por trazabilidad con su valor real, pero **no
> cuentan como cobertura** al derivar el estado: si son los únicos TCs del criterio, este cae en la fila 1
> aunque sus filas digan `Paso`; si conviven con TCs `Ready` que sí lo cubren, el criterio es como máximo
> **Parcial** (fila 2). En ambos casos, Observación explicando que el TC está obsoleto.

---

## Reutilización del reporte (idempotencia)

Mismo principio de caché que `quality-check`: **si no hubo cambios en los archivos desde la última
generación, no se produce un reporte nuevo** — se devuelven los mismos resultados del `trace-report.md`
existente. Esto evita rehacer el mapeo y volver a delegar la ejecución de pruebas cuando nada cambió.

> **Contexto de ejecución.** Como `quality-check`, este skill es una **compuerta de cierre** (al integrar o
> antes del PR), no corre por tarea ni durante la implementación. La frescura se evalúa sobre la rama
> **consolidada** del cierre. En el pipeline típico de cierre `pr-create` corre `quality-check` **primero**
> (produce `test-run.json` fresco) y luego `trace-validate`, que reutiliza esa corrida — sin doble
> ejecución de pruebas; y si el código tampoco cambió desde el último `trace-report.md`, este Paso 0 lo
> devuelve sin regenerarlo.

**Clave de frescura — el fingerprint canónico de la tubería** (idéntico al de `quality-check`; excluye los
artefactos generados —todo `docs/audits/`, todo `.sdd-devkit/` y los `trace-report.md`— para que escribirlos no
invalide la caché). Recipe exacto en `quality-check` → [Caché de corrida de pruebas](../quality-check/SKILL.md#caché-de-corrida-de-pruebas-compartida-con-trace-validate).
Cubre el README de criterios de la US/WI, los tests y el código fuente: si no cambia, el reporte sería
idéntico → se reutiliza.

> **Un solo fingerprint por corrida.** Calcularlo una vez y usarlo para las **dos** comprobaciones:
> la frescura del `trace-report.md` (este Paso 0) y la del `test-run.json` (Paso 4, delegación).

**Comportamiento (Paso 0 del flujo):**

1. Resolver la ubicación del trabajo y buscar su `trace-report.md`. Si no existe → generar normal (no hay caché).
2. Si existe, leer el **fingerprint guardado** en su marca de pie
   (`<!-- trace-validate:fingerprint=<hash> · generado=YYYY-MM-DD -->`) y recalcular el `FINGERPRINT`:
   - **Coinciden** → **no regenerar**: devolver el veredicto y el resumen del reporte existente tal cual,
     e indicar al usuario que no hubo cambios desde la última validación ({{fecha guardada}}). No reescribir
     el archivo, no delegar en `quality-check`.
   - **Difieren, no hay fingerprint guardado (reportes antiguos), o el usuario pide revalidar/forzar** →
     ejecutar el flujo completo (Pasos 1-7) y **regrabar** el fingerprint al guardar (Paso 7).
3. La marca de pie con el fingerprint **se conserva** en el documento publicado (no se elimina como el
   bloque de instrucciones de la plantilla).

> Un cambio solo en `docs/audits/`, en `.sdd-devkit/` o en un `trace-report.md` **no** cuenta como cambio de
> archivos (están excluidos): el reporte depende del código, los criterios y las pruebas, no de los
> artefactos que él mismo o `quality-check` generan.

---

## Resultados de pruebas: delegación en quality-check

`trace-validate` **no ejecuta la suite de pruebas**. La ejecución es responsabilidad de `quality-check`,
que la persiste en un artefacto reutilizable `test-run.json` (esquema `test-run/v1`). Como el review es
una **corrida completa** de la rama, este artefacto vive en una **ubicación fija**, no por unidad:
**`.sdd-devkit/test-run.json`**, en la raíz del repositorio.

**Cómo obtener los resultados (Paso 4 del flujo):**

1. **Reusar el fingerprint canónico** ya calculado en el Paso 0 (mismo valor; no recalcular).
2. **Si existe `test-run.json` y su `git.fingerprint` coincide** → caché **fresca**: no hubo cambios
   desde la corrida de `quality-check`. **Reutilizar** los resultados por suite (`unit`/`integration`/`e2e`)
   sin ejecutar nada. Anotar la procedencia en la línea «Pruebas» del **Resumen**: «resultados tomados de
   la corrida de `quality-check` del {{commit/fecha}}».
3. **Si no existe o el fingerprint difiere** (hubo cambios, o nunca corrió) → **delegar en `quality-check`
   en modo `tests-only`**, que ejecuta solo los checks de pruebas, escribe `test-run.json` y devuelve los
   resultados. Luego consumir esa caché ya fresca.
4. **Si `quality-check` no puede ejecutarlas** (stack no detectable, entorno sin poder correr, dependencias
   ausentes, o el usuario declina la delegación) → las filas con artefacto van con `Ejecución = —` y
   `Resultado = No ejecutado`, con la razón en «Observaciones y pendientes», y se entrega igualmente la matriz con los
   artefactos hallados. **Nunca fabricar resultados.**

**Mapeo a la matriz.** Cada entrada `suites[]` de `test-run.json` trae `type` (`unit`/`coverage`/
`integration`/`e2e`) y `result` (`PASS`/`FAIL`/`SKIPPED`/`N/A`). La suite **`coverage` no se mapea a ningún
criterio**: es cobertura de líneas/ramas, una métrica del repo que juzga `quality-check`, no cobertura
funcional; si viene en `FAIL`, mencionarlo en «Observaciones y pendientes» y nada más. Traducir al reporte: `PASS`→`Paso`,
`FAIL`→`Fallo`, `SKIPPED`→`No ejecutado`, `N/A` (el repo no tiene esa suite)→`No ejecutado`, dejando en
«Observaciones y pendientes» que esa clase de prueba no existe en el repo. Un criterio cuya prueba asociada dio `FAIL` **y
se pudo aislar que fue la suya** se reporta **No cubierto** con el fallo en Observaciones; si la suite falló
sin poder aislar el test, es **Parcial** (ver «Estados de cobertura» y la nota de granularidad más abajo).

**La traducción es por fila, no por criterio.** Cada fila de la matriz (criterio × TC × tipo) se resuelve así:

| Situación de la fila | Evidencia | Ejecución | Resultado |
|----------------------|-----------|-----------|-----------|
| Tipo declarado sin artefacto en el repo | `—` | `—` | `No cubierto` |
| Artefacto hallado y la suite que lo corre dio `PASS` | ruta | `quality-check` | `Paso` |
| Artefacto hallado y su test dio `FAIL` (aislable) | ruta | `quality-check` | `Fallo` |
| Artefacto hallado, suite en `FAIL` **sin** poder aislar el test | ruta | `quality-check` | `Fallo` (+ Observación «no aislable» → criterio `Parcial`) |
| Artefacto hallado, suite `SKIPPED` / ausente / no ejecutable | ruta | `—` | `No ejecutado` |
| TC `Manual` por diseño | ruta del TC | `Manual` | `N/A` |

`Ejecución` dice **quién** produjo el resultado, no de qué clase es la prueba: eso ya lo dice la columna
`Tipo` y la ruta de `Evidencia`. La **suite efectiva** que corrió el test (dónde vive realmente en el repo)
solo se menciona cuando **no** coincide con el tipo declarado —un `API Test` que corre en `unit`, por
ejemplo—, y va en Observaciones, no en la matriz.

> **Granularidad suite vs. criterio:** `result` es por **suite completa**, no por test individual. Si
> varios criterios mapean a tests dentro de la misma suite y esa suite da `FAIL`, no propagar `Fallo`/`No
> cubierto` a todos ellos sin más: si el `summary` u otro detalle de `quality-check` permite aislar qué test
> falló, marcar solo ese criterio; si no hay forma de aislarlo, marcar los criterios afectados como
> `Parcial` (no `No cubierto`) con la ambigüedad explicada en Observaciones. Detalle completo en
> `references/flow.md` (Paso 4).

> Si el proyecto no usa `quality-check` (no está disponible en la sesión), degradar con elegancia: reportar
> las filas **con artefacto** en `Ejecución = —` / `Resultado = No ejecutado` («ejecución delegada no disponible») —las que no tienen artefacto siguen en `No cubierto`— y entregar la cobertura estática. No
> reintroducir un runner propio en `trace-validate`.

---

## Cuándo bloquear

Parar y reportar (sin generar reporte parcial) cuando:

- El trabajo no existe o no se encuentra su documento de criterios.
- No hay sección de criterios de aceptación, está vacía, o los criterios **no tienen identificador codificado** (el formato es indiferente; lo que no puede faltar es el identificador): no hay nada que trazar de forma trazable; sugerir alinear el trabajo con su skill de definición/planificación antes de validar (para un `FT-XXX`, completar su especificación con el flujo «Analizar legado» de `work-research`).

> **No bloquear** por que el artefacto no siga las convenciones del plugin: identificadores fuera del formato `AC-XXX`, ubicación fuera de `docs/specs/` o ausencia de campo `Estado:` **no** son motivos de bloqueo.

```
WARNING No es posible generar el reporte de trazabilidad:
- <razón concreta>
- <acción sugerida: p. ej. definir los criterios de aceptación del trabajo antes de validar>
```

---

## Ubicación de archivos

| Artefacto | Ruta |
|-----------|------|
| Historia de usuario | `docs/specs/user-stories/US-XXX-[nombre-corto]/README.md` |
| Work item | `docs/specs/work-items/WI-XXX-[kebab]/README.md` |
| Feature (funcionalidad ya implementada) | `docs/specs/features/FT-XXX-[slug]/README.md` |
| Cualquier otro artefacto | La ruta que indique el usuario |
| Casos de prueba documentados (entrada, los produce `test-define`) | `test-cases/` **dentro de la carpeta del artefacto**, con su índice `test-cases/README.md` |
| Caché de corrida de pruebas (entrada, la produce `quality-check`) | `.sdd-devkit/test-run.json` (ubicación fija, no por unidad) |
| Reporte de trazabilidad (salida) | US: `…/US-XXX-[nombre-corto]/trace-report.md` · WI: `docs/specs/work-items/WI-XXX-[kebab]/trace-report.md` · FT: `docs/specs/features/FT-XXX-[slug]/trace-report.md` · otro artefacto: `trace-report.md` **junto al artefacto** (confirmar la ruta con el usuario antes de escribir) |

---

## Mensaje al usuario

Solo el veredicto, el resumen de cobertura y lo que el usuario debe saber o decidir (criterios `No cubierto`/`Parcial`, pruebas que fallaron, si no se pudo ejecutar y por qué). No narrar el trabajo en curso («leí el README», «creé el archivo») ni el razonamiento interno. Listar pendientes en viñetas agrupadas por criterio.

---

## Veredicto

| Veredicto | Cuándo aplicarlo |
|-----------|------------------|
| **✅ Aprobado** | **Todos** los criterios del trabajo en estado **Cubierto** y, si se ejecutaron pruebas automáticas, **todas pasaron**. |
| **⚠️ Aprobado con observaciones** | **Ningún** criterio en `No cubierto`, pero hay caveats que el usuario debe conocer: algún criterio en **Parcial**, cobertura apoyada en TCs `Manual` (aunque sea por diseño), o pruebas que **no se pudieron ejecutar** y por tanto no confirman nada. Enumerar cada caveat. |
| **❌ Rechazado** | Al menos un criterio en **No cubierto**, o una prueba asociada **falló** de forma aislable. Listar los criterios faltantes/fallidos. |

Precedencia: `❌ Rechazado` > `⚠️ Aprobado con observaciones` > `✅ Aprobado`. Es decir, `✅ Aprobado` exige **cero caveats**: si hay alguno (criterio `Parcial`, cobertura apoyada en TCs `Manual`, pruebas no ejecutadas), el veredicto es `⚠️`, no `✅`.

> **En el cierre, este `⚠️` no bloquea** (a diferencia del `⚠️ Incompleto` de `quality-check` y `code-review`, que sí): `work-integrate` y `pr-create` continúan mostrando las observaciones al usuario. Por eso cada caveat debe quedar enumerado y ser legible por sí solo — es lo único que el usuario verá antes de integrar.

---

## Handoffs del ciclo

Posición: **validación / cierre de calidad** — después de `work-implement`.

| | |
|--|--|
| **Entrada** | Trabajo (`US-XXX` / `WI-XXX`, u otro artefacto) con **criterios de aceptación identificados**; código implementado; idealmente tests escritos por `quality-specialist` en el cierre de `work-implement`. Resultados de pruebas **vía `quality-check`** (caché `test-run.json` o delegación `tests-only`). **O** un `FT-XXX` (registro de funcionalidad ya implementada — inferida de código legacy o documentada como existente) para comprobar si está cubierta por pruebas. |
| **Salida** | `trace-report.md` en la ubicación del tipo + veredicto sobre la cobertura. |
| **Veredicto ❌ Rechazado (US/WI)** | Volver a `work-implement` (fase de pruebas con `quality-specialist`) para cubrir los criterios faltantes; revalidar después. |
| **Veredicto ❌ Rechazado (FT)** | Hay comportamiento ya implementado **sin pruebas**: escribir los tests faltantes sobre el código existente (no código funcional) con `work-implement` en su tipo **feature** —que automatiza los `TC-XXX` del `FT-XXX`— y revalidar. Formalizar ese trabajo como una tarea de mantenimiento (`WI-XXX`) es opcional y lo decide el usuario. |
| **Falta funcional en el trabajo** | Si la matriz revela que un criterio no es testeable o está mal definido, escalar a la definición/planificación del trabajo — para un `FT`, a quien lo registró (el flujo «Analizar legado» de `work-research` u otra fuente de la funcionalidad); no editar la especificación desde aquí. |

---

## Mapa de referencias

| Archivo | Cuándo leerlo |
|---------|---------------|
| `references/flow.md` | Flujo paso a paso (Pasos 0-7), delegación de la ejecución de pruebas en `quality-check` (caché `test-run.json` / `tests-only`) y checklist completo. Leer antes de ejecutar el flujo. |
| `references/examples.md` | Ejemplos por tipo (US / WI, sin criterios, sin runner, criterio sin prueba) y anti-patrones. Leer ante dudas de comportamiento. |
| `assets/trace-report-template.md` | Plantilla canónica del reporte de trazabilidad. Leer antes de redactar el reporte. |
