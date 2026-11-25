---
name: arch-init
description: >-
  Identifica el punto de partida de un proyecto (sin código / con código base / con implementación) e inicializa lo que falte de su harness multi-agente: repo git, placeholders `AGENTS.md`/`CLAUDE.md`/`.agents/MEMORY.md`/`docs/adr/README.md`/`docs/standards/README.md`, el stack tecnológico (capturando qué se quiere desarrollar y, si hace falta, investigando con `work-research`), candidatos de ADR/estándares (vía `arch-discover` si ya hay implementación) y la compuerta de calidad (consultando `quality-check` para saber qué se suele validar por stack). Cierra actualizando el stack y sugiriendo continuar con `work-define` o `work-plan`. Activar al pedir inicializar, bootstrapear o preparar un proyecto para agentes, configurar su harness, crear `AGENTS.md`/`CLAUDE.md`/`MEMORY.md` desde cero, o mencionar "arch-init", "/arch-init", "inicializa el harness".
license: MIT
---

# Skill: Inicialización del harness de agentes (arch-init)

Inicializa, en un proyecto **en cualquier punto de partida**, las primeras instrucciones persistentes y compatibles con múltiples agentes: repositorio git, los archivos base del harness (`AGENTS.md`, `CLAUDE.md`, `.agents/MEMORY.md`, `docs/adr/README.md`, `docs/standards/README.md`), un stack tecnológico definido, una compuerta de calidad mínima y las decisiones relevantes documentadas como ADR/estándares.

> **Completa siempre lo que falta.** El punto de partida que identifica el Paso 1 — sin código, con código base, o con implementación — solo decide **cómo** se llega a cada pieza (p. ej. un stack ya detectado salta el Paso 2). El resultado al cerrar es siempre el mismo checklist completo, sin importar de dónde partió.
>
> **Alcance:** este skill **bootstrapea** el harness — es el primer paso de SDD Devkit, antes de que exista nada que `arch-discover`, `arch-manage`, `arch-audit` o `quality-check` puedan leer, auditar o revisar. No reemplaza a `work-define` / `work-plan` / `work-implement` (historias y tareas) ni reimplementa la lógica de esos skills — los invoca cuando corresponde. Se ejecuta normalmente **una vez** por proyecto; volver a ejecutarlo sobre uno ya inicializado solo completa lo que falte (ver [Idempotencia](#idempotencia--reejecución)).
>
> **Orden con compuertas:** no se avanza de paso mientras el anterior no esté resuelto. La sección `## Stack tecnológico` de `AGENTS.md` se deja **vacía** hasta el cierre (Paso 5) — no se rellena antes, aunque el stack ya se conozca desde el Paso 1 o el Paso 2.

## Relación con el resto de SDD Devkit

`arch-init` es el único punto de entrada que **crea** `AGENTS.md`, `.agents/MEMORY.md`, `docs/adr/README.md` y `docs/standards/README.md` desde cero — el resto de skills de arquitectura los dan por existentes (o toleran que estén vacíos):

| Skill | Qué asume/hace, y cómo se relaciona con `arch-init` |
| ----- | ----------------------------------------------------- |
| `arch-manage` | Crea/actualiza ADRs y estándares de dominio. `arch-init` lo invoca en el Paso 5 con los candidatos que se aceptaron en el Paso 4 — nunca redacta un ADR/estándar por su cuenta. |
| `arch-discover` | Infiere ADR/estándares candidatos **del código ya existente** y los crea por su cuenta (su Fase 5 invoca `arch-manage`). `arch-init` lo invoca **completo** en el Paso 4.1 cuando el punto de partida es "con implementación" — no reimplementa esa inspección ni repite su creación de artefactos. |
| `arch-audit` | Audita `docs/standards/` y `AGENTS.md` contra el repo — de `AGENTS.md` toma también el contexto de stack (`## Stack tecnológico`) — y lee `.agents/MEMORY.md` para el idioma. `arch-init` es lo que le da a `arch-audit` algo que auditar la primera vez. |
| `quality-check` | Sabe qué se suele validar por stack — tipado, linter, unit tests, coverage, integración, build, e2e, sonar (`quality-check/references/stacks.md`). `arch-init` lo **consulta** en el Paso 4 para saber qué le falta a la compuerta de calidad; no ejecuta la corrida completa (esa corre sobre código ya implementado, no aplica en una inicialización). |
| `work-define` / `work-plan` | Reciben el handoff que `arch-init` ofrece al cerrar (Paso 5). |

---

## Cómo preguntar al usuario

Cuando este skill indique **preguntar, pedir, confirmar o sugerir** algo al usuario, hacerlo mediante la **herramienta de preguntas estructuradas** del cliente (la que renderiza opciones tappables o un selector) en lugar de redactar la pregunta como prosa libre. Reglas:

- **Opciones cortas y mutuamente excluyentes** (2-4 por pregunta) cuando la respuesta admita categorías; selección múltiple solo donde el propio paso lo indique explícitamente (p. ej. capas de testing, candidatos de ADR); texto libre cuando la respuesta no se preste a opciones cerradas.
- **No repreguntar** lo que ya esté resuelto en el contexto de la sesión, en `.agents/MEMORY.md` o en los manifiestos del repo.
- **Una tanda por paso**: agrupar las preguntas de un mismo paso en un solo bloque en vez de ir descubriendo huecos turno a turno.
- **Fallback:** si el cliente no expone esta herramienta, formular la pregunta en prosa con opciones enumeradas (1, 2, 3…).

Cada vez que una sección posterior diga *preguntar*, *confirmar* o *sugerir* al usuario, asume este mecanismo; no se repite allí.

---

## Resolución de idioma

1. Si `.agents/MEMORY.md` **ya existe** (reejecución sobre un harness parcialmente inicializado), leer su línea `preferred language: <código>` y usar ese idioma.
2. Si no existe, usar el **idioma del turno del usuario**.
3. Persistir el idioma resuelto en `.agents/MEMORY.md` como `preferred language: <código>` al crearlo (Paso 3) — no hace falta preguntarlo aparte salvo que el idioma del turno sea ambiguo.

---

## Mapa del harness

| Archivo | Contenido | Se crea en |
| ------- | --------- | ---------- |
| `AGENTS.md` | Reglas operativas/arquitectónicas + sección `Stack tecnológico` | Paso 3 (stub) → Paso 5 (stack definitivo) |
| `CLAUDE.md` | Solo `@AGENTS.md`, por compatibilidad | Paso 3 |
| `.agents/MEMORY.md` | Memoria persistente (idioma, preferencias, reglas operativas — **no** el stack, eso vive solo en `AGENTS.md`) | Paso 3 (stub, con idioma) |
| `docs/adr/README.md` | Índice de ADRs vigentes | Paso 3 (stub) → Paso 5 (poblado por `arch-manage`) |
| `docs/standards/README.md` | Índice de estándares vigentes | Paso 3 (stub) → Paso 5 (poblado por `arch-manage`) |

---

## Paso 1 — Identificar el punto de partida

Leer `references/stack-detection.md` completo antes de este paso.

### 1.1 Repositorio git

- `git rev-parse --is-inside-work-tree`. Si falla, ejecutar `git init` e informar que se creó el repositorio (sin hacer commit todavía — el primer commit queda a criterio del usuario, p. ej. vía `git-commit` después del Paso 3).
- Si ya es un repo git, no tocar la configuración existente (remoto, ramas, hooks).

### 1.2 Clasificar la situación

Aplicar las señales de `references/stack-detection.md § 2` para ubicar el proyecto en **una** de tres situaciones:

| Situación | Qué implica |
| --------- | ------------ |
| **Sin código** | No hay manifiestos de ningún stack ni código fuente propio. |
| **Con código base** | Hay un stack detectable (manifiestos / resultado de un scaffold) pero sin lógica de negocio propia todavía. |
| **Con implementación** | Hay características de negocio ya implementadas (módulos, rutas, componentes o tests con lógica propia; `docs/specs/` con contenido). |

Si el resultado es ambiguo, preguntar al usuario en vez de asumir. Esta clasificación decide si el Paso 2 hace falta (solo **Sin código**) y cómo se identifican los candidatos de arquitectura en el Paso 4.

### 1.3 Detectar el stack tecnológico

Buscar los manifiestos de `references/stack-detection.md § 1`. **Con código base** y **Con implementación** siempre tienen stack detectable — registrar internamente lenguaje(s), framework(s) y versiones (se usan en el cierre, Paso 5). **Sin código** no tiene nada que detectar: el Paso 2 es obligatorio.

---

## Paso 2 — Conseguir el stack

**Solo si el Paso 1.2 clasificó "Sin código".** En cualquier otro caso, saltar directo al Paso 3.

### 2.1 Preguntar qué se quiere desarrollar

No arrancar con una categoría cerrada de "tipo de proyecto" ni con una pregunta de preferencia de stack por separado. Preguntar primero, en lenguaje abierto: *"¿Qué quieres desarrollar?"* — pedir que describa la necesidad: qué problema resuelve, para quién, y cualquier restricción o preferencia que ya tenga en mente (integraciones con algo existente, rendimiento esperado, quién lo va a mantener, plazos). Es una respuesta de **texto libre**; si el cliente expone la herramienta de preguntas estructuradas, usarla igual con una opción de entrada libre en vez de forzar categorías.

De la respuesta, extraer (sin volver a preguntar por separado): el **tipo de proyecto** (se infiere, no se pregunta aparte), cualquier **preferencia de stack** ya mencionada, y las **restricciones** relevantes (integraciones, rendimiento, equipo, plazos, licenciamiento).

Si la respuesta es demasiado vaga para decidir nada (p. ej. "una app"), repreguntar **una sola vez** pidiendo más detalle — no avanzar con una necesidad ambigua.

### 2.2 Sugerir directo o investigar primero

Con la necesidad ya capturada, decidir cómo se llega al stack:

- **El usuario ya mencionó una preferencia de stack explícita** en el 2.1 → usarla directamente. Saltar a 2.3.
- **No hay preferencia, pero la necesidad es común y el criterio es claro** (stack bien establecido para ese tipo de proyecto, sin restricciones inusuales) → sugerir directamente 1-2 opciones con una justificación breve (1-2 líneas, atada a la necesidad descrita) y presentarlas con la herramienta de preguntas estructuradas: opciones = cada stack sugerido, más `Quiero que investigues más opciones` y `Tengo otra preferencia` (texto libre). No hace falta un subagente para este caso.
- **Hay trade-offs no triviales, restricciones específicas que cambian la respuesta obvia, o el usuario pide explícitamente que se investigue** → delegar en un **subagente** que ejecute el skill **`work-research`** (dominio **Técnica**, investigación **independiente** — no hay `US`/`WI`/`MG` todavía) con una pregunta construida a partir de la necesidad capturada (el problema y sus restricciones, no una categoría genérica), p. ej. *"¿Qué stack tecnológico es más adecuado para <necesidad descrita, con sus restricciones>?"*. Pedirle explícitamente que, para **cada opción**, incluya los **comandos exactos de instalación/scaffolding** — no solo la comparación teórica. `work-research` guarda su informe en `docs/specs/research/RS-XXX-{slug}.md`; esperar su resultado y presentar las opciones al usuario (una por stack, más `Ninguna, decido yo`).

Ante la duda entre sugerir directo o investigar, preferir investigar: una sugerencia sin respaldo en un stack con opciones reñidas cuesta más corregir después que un `RS-XXX` de más.

Si durante 2.1 o 2.2 hace falta alguna aclaración adicional del usuario para poder decidir, preguntarla en el momento — no acumular ambigüedades para más adelante.

### 2.3 Instalar el stack elegido

1. Ejecutar los comandos de scaffolding/instalación de la opción elegida (de la investigación del 2.2, o indicados por el usuario si dio su propia preferencia).
2. Verificar que la instalación quedó operativa (p. ej. `npm run build`, un comando de arranque en modo check, o el equivalente del stack) antes de continuar.
3. Registrar internamente el stack definitivo (lenguaje, framework, versión, herramientas de build) — **todavía no se escribe en `AGENTS.md`**, eso ocurre en el Paso 5.

---

## Paso 3 — Placeholders del harness

Antes de escribir cualquier archivo, aplicar la regla de [Idempotencia](#idempotencia--reejecución).

1. **`AGENTS.md`** — copiar `assets/agents-template.md` tal cual (el bloque de reglas operativas/arquitectónicas y la sección `## Stack tecnológico` **vacía**).
2. **`CLAUDE.md`** — copiar `assets/claude-template.md` tal cual.
3. **`.agents/MEMORY.md`** — copiar `assets/memory-template.md`, reemplazando `<código>` en `preferred language:` por el idioma resuelto en [Resolución de idioma](#resolución-de-idioma).
4. **`docs/adr/README.md`** — copiar `assets/adr-index-template.md` tal cual.
5. **`docs/standards/README.md`** — copiar `assets/standards-index-template.md` tal cual.

### Idempotencia / reejecución

- Si un archivo del harness **ya existe**:
  - Si su contenido coincide con el patrón gestionado por este skill (p. ej. `AGENTS.md` ya tiene el bloque de "Reglas operativas y arquitectónicas"), **no sobrescribir** — continuar como si ya estuviera creado.
  - Si existe pero con contenido **distinto** (el usuario ya tenía su propio `AGENTS.md`/`CLAUDE.md`/etc.), **no sobrescribir automáticamente**: mostrar el contenido actual y preguntar si se debe fusionar, reemplazar o dejar como está. Nunca perder contenido del usuario sin su autorización explícita.
- Si el harness **ya está completo** (los cinco archivos existen y gestionados), informar que el proyecto ya está inicializado y preguntar si se desea continuar igualmente para revisar/completar el resto (Paso 4 en adelante) o terminar aquí.

---

## Paso 4 — Candidatos de arquitectura y compuerta de calidad

### 4.1 Identificar candidatos de ADR/estándares

Leer `references/adr-candidates.md` completo antes de este paso.

- **Con implementación** (Paso 1.2) → delegar en un **subagente** que ejecute el skill **`arch-discover`** **completo** sobre el repo — sus cinco fases, incluida la Fase 5, en la que `arch-discover` mismo crea los artefactos aprobados invocando `/arch-manage` por su cuenta. `arch-discover` presenta sus candidatos al usuario, los agrupa por dominio funcional y los delega en `arch-manage` sin intervención de `arch-init` — **no** repetir esa presentación aquí, ni volver a delegarlos en `arch-manage` en el Paso 5.1: `arch-discover` ya es dueño de esa lista de principio a fin. Lo único que se retiene de esta ejecución es un resumen (cuántos ADR/estándares creó, con sus rutas) para reportarlo en el cierre (Paso 5.3) — **no** se agrega nada de esto a la lista consolidada del Paso 4.1/5.1.
- **Con código base** o **Sin código** (tras el Paso 2) → no hay nada que "descubrir" en código que todavía no existe: el candidato es la **decisión de stack** tomada en el Paso 1.3 o el Paso 2 (con sus alternativas, si vinieron de una investigación), clasificada por dominio funcional según `adr-candidates.md § 1`.

La lista consolidada que llega al Paso 5.1 se arma solo con la rama "con código base"/"sin código" de arriba (cuando aplica) más lo que aporte el 4.2 — nunca con los candidatos de `arch-discover`, que ya quedaron resueltos por su propia Fase 5. No delegar nada en `arch-manage` todavía desde aquí; eso ocurre en el Paso 5.1.

### 4.2 Compuerta de calidad

Leer `references/quality-gate.md` completo antes de este paso.

1. **Diagnóstico:** revisar si ya existe configuración de pruebas (config, carpetas, scripts de test).
2. **Qué se suele validar:** consultar el skill **`quality-check`** — específicamente su `references/stacks.md`, tabla "Aplicabilidad por stack" — para saber qué checks son **Bloqueantes** (típicamente tipado si aplica, linter, unit tests, coverage, build) y cuáles **Condicionales** (típicamente integración y E2E, y linter/tipado en algunos stacks) para el stack de este proyecto. `arch-init` no ejecuta la corrida completa — esa corre sobre código ya implementado, no aplica en una inicialización —, solo usa esa tabla como checklist de qué falta configurar.
3. **Completar lo que falte:** para cada check **Bloqueante** ausente, y cada **Condicional** relevante según el tipo de proyecto (`quality-gate.md § 3` — nunca sugerir una capa que no ayude a validar este proyecto en particular, p. ej. E2E a una librería sin UI ni endpoints), preguntar al usuario y, si acepta, instalar/configurar lo necesario: dependencias, config mínima, un test de ejemplo real (no un placeholder vacío), y el script de ejecución.
4. **Validar:** ejecutar la suite configurada y confirmar que corre sin errores de configuración antes de avanzar. Si falla por algo fuera del alcance de este skill, informar y preguntar cómo proceder.
5. El framework y las capas configuradas se suman como candidato de dominio `testing` a la lista del 4.1 (un requisito por capa aceptada, igual que el ejemplo canónico de `arch-discover`).

---

## Paso 5 — Cierre

### 5.1 Documentar las decisiones aceptadas

Presentar la lista consolidada de candidatos agrupada por dominio funcional, con la herramienta de preguntas estructuradas en **selección múltiple** (incluir siempre `Ninguno por ahora`). Esta lista es la decisión de stack del 4.1 (**solo** si la situación fue "con código base" o "sin código" — si fue "con implementación", esos candidatos ya los gestionó `arch-discover` en su propia Fase 5 y **no** se repiten aquí) más lo añadido en el 4.2. Si la lista queda vacía (p. ej. situación "con implementación" y la compuerta de calidad ya estaba completa), saltar directo al 5.2 sin preguntar. Si el usuario acepta algo: resolver **decisores** e **idioma** una sola vez para todo el lote (`adr-candidates.md § 3`) y delegar en un **subagente** que ejecute **`/arch-manage`**, agrupando los candidatos aceptados **por dominio** en la misma invocación. `arch-manage` crea los ADR y, cuando corresponda, los requisitos en el estándar de dominio, actualizando ambos índices por su cuenta. Esperar su respuesta antes de continuar.

### 5.2 Actualizar el stack

Reemplazar el contenido (vacío) bajo `## Stack tecnológico` en `AGENTS.md` con el stack definitivo — lenguaje(s), framework(s) y versión, gestor de paquetes/build, y las capas de testing configuradas en el 4.2. **`AGENTS.md` es la única fuente del stack** — no se repite en `.agents/MEMORY.md` (ese archivo no lleva sección de stack; ver plantilla). Este es el **único** momento del flujo en que se escribe esa sección.

### 5.3 Confirmar y sugerir el siguiente paso

Confirmar al usuario que el harness inicial quedó listo, resumiendo: punto de partida (situación del Paso 1.2), repositorio git (creado o ya existía), archivos del harness creados, stack definitivo, compuerta de calidad configurada, y — si aplica — los ADR/estándares creados con sus rutas: los del Paso 5.1 y, si la situación fue "con implementación", también los que creó `arch-discover` en su propia Fase 5 (retenidos del Paso 4.1).

Después, ofrecer el siguiente paso natural con la herramienta de preguntas estructuradas — **es una sugerencia, no un paso bloqueante**: *"¿Quieres continuar con...?"* opciones: `Escribir la primera historia de usuario (work-define)` / `Planificar tareas técnicas o de mantenimiento (work-plan)` / `Nada por ahora`.

No confirmar el cierre antes de que `AGENTS.md` tenga el stack ya escrito.

---

## Mapa de referencias

| Archivo | Cuándo leerlo |
| ------- | -------------- |
| `references/stack-detection.md` | Paso 1 — manifiestos por ecosistema y la clasificación en las tres situaciones (sin código / con código base / con implementación). |
| `references/quality-gate.md` | Paso 4.2 — cómo interpretar la tabla de `quality-check` por stack, y cuándo sugerir E2E/API testing según el tipo de proyecto. |
| `references/adr-candidates.md` | Paso 4.1 y 5.1 — cómo convertir la decisión de stack (o los candidatos de `arch-discover`) y la compuerta de calidad en candidatos por dominio funcional, y cómo delegarlos en `arch-manage`. |
| `assets/agents-template.md` | Paso 3 — plantilla de `AGENTS.md`. |
| `assets/claude-template.md` | Paso 3 — plantilla de `CLAUDE.md`. |
| `assets/memory-template.md` | Paso 3 — plantilla de `.agents/MEMORY.md`. |
| `assets/adr-index-template.md` | Paso 3 — plantilla de `docs/adr/README.md`. |
| `assets/standards-index-template.md` | Paso 3 — plantilla de `docs/standards/README.md`. |

---

## Anti-patterns

- Rellenar `## Stack tecnológico` en `AGENTS.md` antes del Paso 5, aunque el stack ya se conozca desde el Paso 1 o el Paso 2.
- Escribir el stack (o duplicarlo) en `.agents/MEMORY.md` — ese archivo no lleva sección de stack; `AGENTS.md` es la única fuente.
- Sobrescribir un `AGENTS.md`/`CLAUDE.md`/etc. existente con contenido propio del usuario sin preguntar primero.
- Ejecutar el Paso 2 (conseguir el stack) cuando el Paso 1.2 ya clasificó "con código base" o "con implementación".
- Clasificar la situación del Paso 1.2 sin evidencia clara, en vez de preguntar ante la ambigüedad.
- Preguntar "tipo de proyecto" como categoría cerrada o "¿tienes preferencia de stack?" como pregunta aparte, en vez de capturar la necesidad en el 2.1 y extraer de ahí tipo/preferencia/restricciones.
- Sugerir o investigar un stack sin haber capturado antes la necesidad real (2.1) — avanzar con una descripción vaga ("una app") sin repreguntar.
- Investigar el stack (2.2) sin pedirle al subagente los comandos de instalación de cada opción.
- Reimplementar en el Paso 4.1 la inspección de código que ya hace `arch-discover`, en vez de delegarle esa identificación cuando el punto de partida es "con implementación".
- Volver a presentar o delegar en `/arch-manage` los candidatos que `arch-discover` ya creó por su cuenta en su propia Fase 5 — es trabajo duplicado y puede generar un ADR casi-idéntico; el Paso 5.1 solo agrupa lo que **no** pasó por `arch-discover`.
- Reinventar en el Paso 4.2 un catálogo propio de qué validar por stack en vez de consultar `quality-check/references/stacks.md`.
- Ejecutar la corrida completa de `quality-check` sobre el repo — ese skill corre sobre código ya implementado, no en una inicialización sin nada que verificar.
- Sugerir E2E, API testing u otras capas que no aportan valor de validación al tipo de proyecto.
- Cerrar el Paso 4.2 sin ejecutar la suite de pruebas al menos una vez para confirmar que corre.
- Delegar en `/arch-manage` sin que el usuario haya aceptado explícitamente al menos un candidato, o sin agrupar por dominio los candidatos que comparten estándar.
- Confirmar el cierre antes de actualizar el stack definitivo en `AGENTS.md`.
- Forzar el handoff a `work-define`/`work-plan` en el 5.3 en vez de ofrecerlo como sugerencia que el usuario puede declinar.
- Hacer commit automático del harness sin que el usuario lo pida (queda para `git-commit`, fuera de este skill).
- Lanzar preguntas como prosa libre cuando el cliente expone la herramienta de preguntas estructuradas.

---

## Ejemplos

**Ejemplo 1 — Sin código, necesidad con restricciones que ameritan investigar**

Carpeta vacía salvo un `README.md`. Paso 1: no hay repo git → `git init`; sin manifiestos → situación "sin código". Paso 2.1: a "¿qué quieres desarrollar?" el usuario responde "una API para gestionar pedidos de un e-commerce, con picos fuertes de tráfico en fechas de descuentos" — sin preferencia de stack. Paso 2.2: la restricción de picos de tráfico no es trivial → se decide investigar; el subagente de `work-research` compara Node/Fastify, Python/FastAPI y Go con foco en throughput, con comandos de instalación para cada uno; el usuario elige Fastify + TypeScript. Paso 2.3: se ejecuta el scaffold. Paso 3: se crean los cinco archivos del harness. Paso 4.1: como no hay implementación todavía, el único candidato es "Fastify + TypeScript" (dominio `api`, con las alternativas del `RS-XXX`). Paso 4.2: se consulta `quality-check/references/stacks.md` para Node+TS (tipado, linter, unit, coverage y build son bloqueantes); no hay nada configurado → se sugiere Vitest (unit) y, por tratarse de una API, Supertest (API testing); el usuario acepta ambos y se configuran. Se suma "Vitest + Supertest" (dominio `testing`) a la lista. Paso 5.1: el usuario acepta documentar ambos candidatos → subagente `/arch-manage` crea los ADR y los estándares de dominio `api` y `testing`. Paso 5.2: se escribe el stack en `AGENTS.md`. Paso 5.3: se confirma el cierre y se ofrece continuar con `work-define`; el usuario acepta.

**Ejemplo 2 — Con implementación, delegando en arch-discover**

Repo git con historial de dos años, `package.json` con NestJS + Prisma, `docs/specs/user-stories/` con 40 historias. Paso 1: repo ya existe; stack detectado (NestJS/Prisma); situación "con implementación" → se salta el Paso 2. Paso 3: `AGENTS.md` y `.agents/MEMORY.md` no existían → se crean con stub. Paso 4.1: se delega en un subagente que corre `arch-discover` **completo**; encuentra y presenta candidatos como "por qué Prisma" y "arquitectura en capas", el usuario acepta 3, y el propio `arch-discover` los crea invocando `arch-manage` en su Fase 5 — `arch-init` no vuelve a presentarlos ni a delegarlos. Paso 4.2: ya hay Jest configurado con buena cobertura de unit (bloqueantes cubiertos según `quality-check/references/stacks.md`); falta E2E para los flujos de checkout → se sugiere y el usuario acepta agregar Playwright, que se suma como candidato de dominio `testing`. Paso 5.1: la lista consolidada tiene solo el candidato de Playwright (los 3 de `arch-discover` ya quedaron creados) → se documenta y `/arch-manage` lo crea. Paso 5.2: stack definitivo (NestJS x.y, Prisma x.y, Jest + Playwright) se escribe en `AGENTS.md`. Paso 5.3: se confirma el cierre reportando los 3 ADR/estándares que creó `arch-discover` más el de Playwright, y se ofrece continuar con `work-plan` (hay deuda técnica pendiente); el usuario prefiere `Nada por ahora`.

**Ejemplo 3 — Con código base, sugerencia directa sin investigar**

Carpeta con un scaffold de Astro recién generado (`npm create astro@latest`), sin posts ni contenido propio. Paso 1: repo existe; `package.json` detecta Astro → situación "con código base" → se salta el Paso 2 (el stack ya está decidido por el scaffold). Paso 3: se crean los cinco archivos del harness. Paso 4.1: el candidato es "Astro" (dominio `frontend`), sin alternativas registradas porque no hubo Paso 2. Paso 4.2: `quality-check/references/stacks.md` para Node+TS marca unit/build como bloqueantes; se sugiere Vitest; el usuario acepta. Paso 5: se documenta lo aceptado, se escribe el stack, se confirma el cierre y se ofrece `work-define`.

**Ejemplo 4 — Reejecución sobre un harness ya inicializado**

El usuario vuelve a pedir `arch-init` sobre un proyecto donde ya corrió antes. Paso 3 detecta que los cinco archivos ya existen y están gestionados por este skill → informa que el harness ya está inicializado y pregunta si continuar para revisar/completar. El usuario confirma porque quiere agregar la compuerta E2E que no se configuró la primera vez → el skill retoma directamente en el Paso 4.2, sin tocar los archivos ya creados.

---

## Handoffs

| Después de `arch-init`... | Skill natural siguiente | Contexto que pasa |
| -------------------------- | ------------------------ | -------------------- |
| Harness inicializado, listo para escribir requisitos | `work-define` | El stack y las convenciones ya viven en `AGENTS.md`/`docs/standards/`. Ofrecido explícitamente en el Paso 5.3. |
| Harness inicializado, hay trabajo técnico que planificar | `work-plan` | Ofrecido explícitamente en el Paso 5.3. |
| Se necesita investigar algo más allá del stack inicial | `work-research` | Puede referenciar el `RS-XXX` generado en el Paso 2.2. |
| Se quieren agregar más ADR/estándares después del cierre | `arch-manage` | Los índices `docs/adr/README.md` y `docs/standards/README.md` ya existen y se amplían, no se recrean. |
| Verificar cumplimiento de lo documentado | `arch-audit` | Lee `AGENTS.md` (incluido el stack) y `docs/standards/`; `.agents/MEMORY.md` ya tiene el idioma que necesita. |
| Primer commit del harness | `git-commit` | El working tree recién creado por este skill. |
