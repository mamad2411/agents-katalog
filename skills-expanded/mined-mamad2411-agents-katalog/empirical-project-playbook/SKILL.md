---
name: empirical-project-playbook
description: "Use when starting, building, or auditing an empirical/data-driven project with AI agents - anything that measures something (edge, conversion, performance, a business hypothesis) and decides with data. Covers pre-registration and kill criteria, anti-mining defenses, presence-vs-utility acceptance, shadow-mode rollout, mechanized build-failing checks, the 'treacherous silence' bug family, verification standards, and security/systems rules."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [empirical, methodology, agent-built, pre-registration, anti-mining, business-analysis, mcp, performance]
    related_skills: [test-driven-development, systematic-debugging, requesting-code-review, hermes-agent]
---

# Empirical Project Playbook

Playbook para construir y operar **proyectos empíricos** (trading, ML, growth,
analytics, automatización con riesgo) usando agentes de IA. Destila el método
que un proyecto real de prediction-markets construyó contra sus propios
errores: 25+ patrones de incidente mecanizados, un registry de findings con
lifecycle, y un norte de decisión único.

**Origen:** polymarket-trading-bot (2026). Los axiomas de mercado (familia X)
NO se extrapolan; el MÉTODO sí. Este playbook es la capa portable.

## Cuándo usar esta skill

- Arrancar un proyecto nuevo que va a medir algo (edge, conversión, rendimiento,
  hipótesis de negocio) y decidir con datos.
- Construir con agentes de IA (Claude Code, Hermes, OpenCode, Codex) y querer
  que hereden el método sin re-derivar los errores.
- Agregar una capa de análisis empresarial / integración (MCP, servidores
  externos, pruebas de rendimiento de sistema) sobre un proyecto existente.
- Auditar un proyecto que ya acumula datos y no sabe si son útiles.

## Relación con el arnés de construcción

Este playbook es el MÉTODO (qué medir, cómo no engañarse, cuándo matar una
hipótesis). El **arnés** que hace que el código escrito por agentes sea confiable
—loop de validación, guards en todas las superficies, baselines con trinquete,
doc que verifica sus números, modos de falla propios del agente— vive en la skill
`agent-ready-project`, y aplica aunque el proyecto no mida nada. Cargar las dos
cuando un proyecto empírico se construye con agentes.

## Los 3 mandamientos del método

1. **Un juez, un norte.** Una sola métrica de veredicto final por la que se
   promociona o descarta todo (ej. `EDGE_CONFIRMED` usable-only). Todo lo demás
   es medio. Si hay muchas métricas tentadoras, elegir UNA explícitamente.
2. **Presence ≠ utility.** Un feature no está listo cuando corre sin error:
   está listo cuando una query/log de PRODUCCIÓN responde la pregunta que lo
   motivó, con valores plausibles en filas post-deploy. "Hay filas" no es "sirve".
3. **Si es mecanizable, es check que falla el build, no párrafo.** La prosa no
   frenó un bug que recurrió 6 veces; el script que bloquea el build, sí.

## Flujo de trabajo (cadencia)

1. **Memo ANTES de implementar** trabajo estratégico: claim, evidencia,
   no-goals, métrica post-deploy, kill criteria. Sin memo no es strategic work.
   → `docs/analysis/YYYY-MM-DD-<tema>.md` o `docs/plans/`.
2. **Registry con lifecycle formal**: `PROPOSED → TESTING → SUPPORTED →
   CONFIRMED` (o `INSUFFICIENT / RETRACTED / SUPERSEDED`). Un guard en código
   bloquea usar findings `RETRACTED` y redirige los `SUPERSEDED`.
3. **Shadow → observación → enforce.** Nunca live ni hard gate desde datos de
   paper. Un flag en observación calcula y loguea "habría hecho X" sin ejecutar.
4. **Build solo con query de aceptación pre-escrita.** Antes de escribir código,
   escribir la consulta/log que va a demostrar que el feature sirve.
5. **Cierre:** memoria de sesión, status del plan, tree limpio o rama pusheada.

## Anti-minería (defensa contra tus propios datos)

- **Pre-registro**: fijar criterios de éxito/fracaso ANTES de ver los datos.
  Ej: "kill si EV<0 a n≥80; success si EV≥0.05 a n≥80". Un sweet spot minado
  post-hoc es una hipótesis, no un hallazgo.
- **Réplica en muestra fresca**: un hallazgo de una sesión se re-mide sobre
  datos que no participaron en descubrirlo, con corte de frescura estricto.
- **CI gate anti-drift**: falla el build si un PR toca `docs/analysis/` sin
  actualizar el registry. Impide que la doc y el estado diverjan.
- **NULL ≠ 0**: "nunca lo medimos" (NULL) es un defecto; "lo medí y dio cero"
  (0) es un dato legítimo. Contar el segundo como defecto convierte un sistema
  honesto en un FAIL permanente → fatiga de alertas.

## Capa de invariantes y veredictos (self-attesting)

La confianza de un sistema empírico NO es "no encontré bug esta semana" — es que cada
etapa prueba, por ciclo, que pobló lo que promete. Sin esa capa, "¿funciona?" depende de
la memoria del operador y de sesiones de debug que encuentran el próximo fallo por suerte.

- **La batería por ciclo precede a cualquier métrica de producto.** Un feed de datos no se
  puede vender ni un edge se puede confiar si el sistema no puede probar que mide lo que
  dice. Instrumenta la batería ANTES de construir producto encima. Si los datos alimentan
  una decisión, un contrato (etapa fuente → consumidor → campo prometido → condición → query
  de prod → NULL≠0) debe atestiguarlo. Ver skill `empirical-system-invariants` (batería
  + guard `empirical-system-invariants/scripts/invariant_guard.py`, agnóstico).
- **Engram como memoria de VEREDICTOS, no de logs.** Persistir los RESULTADOS de checks y
  findings (veredicto, n, EV, kill/success, dataset_version) como observaciones con
  `topic_key` estable — nunca el ruido de progreso. Un check nuevo aprendido tras un
  incidente se registra para que cualquier agente futuro lo cargue. El silo que guarda cada
  cosa es decisión explícita (Hermes no escribe al engram del proyecto; convención ya
  documentada).
- **Hermes MCP como fuente única del estado.** Exponer health/checks/veredictos como
  recursos MCP para que agentes y dashboards lean el MISMO dato que el sistema usa — nunca
  una copia que drifta entre capas. (El patrón "MCP como capa de integración" del playbook;
  acá pasa a ser parte del contrato de datos.)
- **Auditorías atómicas delegadas** (claude/codex/opencode) con verificación de handle real
  (query de prod, SHA, valores plausibles) hecha UNO MISMO — nunca self-report. Esto corta el
  ciclo "sesión de debug que encuentra el próximo phantom wiring": la auditoría corre como
  tarea acotada y su salida se verifica contra la batería.
- **Deuda medida, no sospechada.** Una snapshot de prod y una query COUNT convierten una
  sospecha en un número. Ejemplo real medido: `edge_elo/form/casino/h2h/residual` estaban
  0/1384 no-null en `rejected_signals` — confirmado por SQL, y el guard lo marca ROJO con
  exit 1. NUNCA afirmar deuda sin reproducirla uno mismo sobre la DB.

## Capa de data-engineering y lakehouse (para entrenar IA / conectar agentes)

Cuando los datos operativos deben volverse un activo reutilizable para ML y agentes, la
capa es un **lakehouse Delta**: almacenado de estructurado + no estructurado, historial de
operaciones, time-travel, y lectura directa por engines y modelos.

El detalle operativo (stack validado, flujo extract → Delta → consumo, upsert, particionado,
vacuum/compaction, orígenes conectables) NO se duplica acá: vive en la skill
**`delta-lakehouse`**, y el diseño punta a punta de la arquitectura (fuente → medallion
bronze/silver/gold → consumo y dashboards) en **`data-medallion-architecture`**.

Lo que el playbook aporta sobre esa capa son sus propias reglas aplicadas al lakehouse:

- **Presence ≠ utility:** una tabla Delta "anda" no es aceptación — lo es que una query DE
  PRODUCCIÓN la lea con valores plausibles post-deploy.
- **Fuente única, nunca una copia que drifta:** un agente consume la MISMA tabla que el
  sistema escribe (mismo principio que MCP-fuente-única).
- **Tests herméticos** para el ingesta (`tmp_path`, nada de archivos reales del host).
- **Medir al punto de operación real:** un lake a 1K filas y uno a 1M/día son problemas
  distintos; el costo se decide midiendo, no por preferencia.
- **NULL ≠ 0 aplicado a la retención:** no vacuar en caliente lo que un agente puede
  necesitar reproducir; fijar retención explícita.

## La familia de "silencios traidores" (patrones que no rompen nada)

Todos nacieron de bugs reales. Buscarlos en cualquier proyecto:

- Getter que devuelve vacío ante un error sin dejar rastro visible.
- Writer de DB que escribe y nunca commitea.
- Gate que no distingue "falló" de "NO CORRIÓ" (ej. `pytest | grep passed || fail`
  con el intérprete inexistente).
- Métrica que cuenta solo éxitos usada como denominador → "success: -5046%".
- Rama de severidad inalcanzable por orden de guardas (todo `>50` es también `>10`).
- Check cuyo umbral describe el deseo, no el defecto → FAIL permanente.
- Prune que loguea "N eliminadas" mientras un filtro sin techo temporal
  protege el 100% de las filas vencidas. Log verde, efecto nulo.
- Wiring fantasma: `getattr(obj, "x", {})` que nadie asigna. El default
  "seguro" oculta el bug: nada crashea, nada loguea, el caller opera sobre
  estado vacío para siempre.
- Doc que drifta respecto al estado real (flags declarados ON que el .env no
  tiene; código deployado atrasado respecto a main).

## Estándar de verificación

- **Un fix no está verificado hasta que su test FALLA contra el código previo.**
  Un test que pasa antes y después no probó nada. Verificar revirtiendo el
  archivo (`git show HEAD:<f> > <f>`), correr la suite, restaurar.
- **Gemelos de frontera**: si un test afirma una cota, hace falta un gemelo que
  pruebe que el fixture efectivamente la roza — si no, pasa por accidente.
- **Medir al punto de operación real**: todo veredicto es al tamaño/escala en
  que se midió. Un "sí se puede" a $1 no es una afirmación sobre tamaño operable.
- **Tests herméticos**: nada de archivos reales del host, red, ni hora del
  reloj. Todo por `tmp_path` + patch. Un timestamp ISO hardcodeado en una
  fixture es una bomba de tiempo.
- **Paths anclados a `__file__`**, nunca al cwd. "Funciona desde la raíz del
  repo" no es funcionar bajo systemd/ssh.

## Capa de análisis empresarial e integración

Para proyectos que quieren una capa de negocio/analytics encima:

- **MCP como capa de integración**: exponer el estado del sistema como
  recursos/prompts MCP (ej. health, métricas, veredictos) para que agentes y
  dashboards lean el MISMO dato que el sistema usa — no una copia que drifta.
  Ver skill `hermes-agent` → `hermes-agent/references/native-mcp.md`.
- **Servidor externo vs local**: decidir por medición, no por preferencia.
  Medir latencia, cuota, costo y disponibilidad del proveedor externo contra
  el costo de operar local. Un proveedor externo que falla en silencio
  devolviendo datos cacheados es peor que uno local lento pero honesto.
  Toda decisión de infraestructura se registra con sus números en
  `templates/infra-decision.md` (mismo espíritu que el pre-registro: criterio
  antes de ver los datos de rendimiento).
- **Pruebas de rendimiento de sistema**: medir con números reales por ciclo/
  por día/cantidad procesada, nunca estimaciones. Detectar costos in-cycle vs
  CLI: una función de análisis manual y la misma llamada in-cycle NO pueden
  compartir el default caro (un bootstrap de 5000 réplicas bloquea el loop 348s).
  Señal de costo in-cycle: los ciclos más lentos caen en múltiplos exactos
  (200, 400, 600…) = un `_EVERY_N_CYCLES` caro.
- **Monitoreo con línea base propia**: comparar cada métrica contra SU propia
  línea base, nunca contra un absoluto. Un canal que colapsa de 8 filas/día a 1
  no cruza un umbral absoluto pero sí su propia línea base.

## Aprendizajes transversales por área (destilados del playbook fuente)

### CI / programación y test

- **Un gate que no distingue "falló" de "NO CORRIÓ" culpa a lo primero.**
  `pytest | grep "passed" || fail` da el mismo resultado con tests rojos que con
  el intérprete inexistente. Verificar el intérprete ANTES de interpretar la
  salida. Firmas hermanas: step de CI con `|| true` / `continue-on-error`,
  `# noqa` varado en la línea de cierre, `mypy` en `stages:[manual]`.
- **Nunca mergear con CI en rojo.** CI ve bugs que un dry-run en prod no ve
  (NameError, regresión de versión). Los checks existen por esto.
- **Versiones de lint pineadas a un solo lugar.** `.pre-commit-config.yaml`
  pinea `black==25` mientras `requirements-dev.txt` dice `black>=23` → CI y el
  hook local nunca convergen, reformateos en bucle. Un pin = una fuente.
- **Characterization tests (golden) ANTES de refactorar un módulo crítico.**
  Congelar el comportamiento actual (15 tests / 87 casos golden en el fuente),
  verificado por mutación (alterar un valor lo hace fallar). Un refactor sin
  esto es ruleta.
- **El test tiene que cubrir el código que tocaste, no uno viejo.** Un test
  que no llama a la función refactorizada da cobertura de la versión vieja.
  Confirmar que el test está en ROJO contra el código ANTES del fix (gemelo de
  frontera, P8).
- **No concluir un patrón con 2 muestras cuando la instrumentación puede
  juntar más en minutos.** Un bug dominante se maldiagnosticó como timeout de
  red con 2 muestras tempranas; con 351, el 95% era tamaño de frame. Esperar la
  ventana antes de escribir la conclusión.
- **Verificar el protocolo real contra el servidor, no contra el mock.** Un WS
  mal desde el origen no lo agarró ningún test porque los tests mockeaban el
  protocolo viejo. Probar en vivo con un script chico.

### Estructura y método

- **Doc raíz única, corta (~300 líneas), con reglas por directorio lazy-load.**
  Cada línea del raíz carga en TODA sesión → bloat = menos precisión + más
  tokens. Reglas "nunca X / siempre Y" con ejemplos, en orden de prioridad.
- **Revisión de reglas muertas al tocar la doc:** una regla que ya no describe
  el sistema real es peor que no tenerla (el agente la obedece y hace daño
  silencioso). Al editar, verificar que las rutas referenciadas existen y que
  los verificadores que la prosa declara siguen en CI.
- **Subagentes solo para tareas atómicas; nunca confiar en su self-report**
  sin verificar el handle (URL/path/estado) uno mismo.
- **Worktrees para paralelismo real**; `git add <paths>` nunca `-A`; merge no
  rebase; recovery por reflog.
- **Doc fechada** (`docs/analysis/YYYY-MM-DD-*.md`) + INDEX como puerta.
- **Skills = workflows versionados.** "Salvá lo que hiciste" tras cada tarea
  no trivial → skill en el repo, no en la cabeza.

### Recolección de datos

- **El recolector debe funcionar SIN depender de ejecutar la acción que mide.**
  El que-ve-señales tenía que recolectar datos aunque Guard0Cap bloqueara las
  órdenes → shadow-ledger PRE-GATE (enganche antes de la ejecución), que crece
  aunque `ordenes=0`.
- **Un canal de datos sin pipeline de resolución acumula filas que nadie puede
  juzgar nunca.** El feedback loop (`would_have_won`) se rompe si no hay
  resolución in-cycle + timer backstop. "¿Quién llama a update_*_outcome()?"
  desde el día 1.
- **Etiqueta de dedup ÚNICA por fuente** (`profile_tag`): dos fuentes con el
  mismo tag se pisan sin avisar; una fuente gemela escribe una fila por tag,
  inflando `n` ~4x salvo dedupe explícito por entidad. Las queries ad-hoc NO
  deduplican — usar la herramienta canónica (el `edge_verdict`).
- **Distinguir 3 estados de un dato:** no-medido (NULL, defecto a corregir),
  medido-con-valor (dato), medido-y-cero (dato legítimo). Y el veredicto es al
  TAMAÑO en que se midió.
- **Un getter de DB que traga excepciones devuelve `[]` en silencio** (converter
  de tipos, columnas `TIMESTAMP` con ISO). Leer con una conexión NUEVA, no la
  del pool — la del pool ve su propia transacción sin commit y oculta el bug.
- **Freshness ≠ retención.** Dos relojes (segundos "¿es seguro usarlo?" vs
  horas "¿vale la pena tenerlo?"). Confundirlos purga datos legítimos o nunca
  libera nada. Límite duro LRU + grace period para entradas recién creadas.

### Know-how operativo (transferible)

- **Estado que se lee pero nadie asigna = wiring fantasma** (getattr con
  default "seguro"): nada crashea, nada loguea, el caller opera sobre vacío
  para siempre. El trailing-stop NUNCA se activó en prod porque un método
  portado perdió su atributo interno. Un `grep` del nombre no prueba que la
  instancia lo tenga — verificar `hasattr` / a qué módulo apunta el import.
- **Un escalar donde el dominio tiene N entidades** (dict keyed por posición)
  es la misma clase de error. Si el vecino está keyed y este no, sospechar.
- **Contador que se computa en el ciclo debe persistir, no vivir solo en un
  log que rota** — los consumidores concluyen lo contrario de la realidad.
- **Estructura en memoria keyed por entidad externa necesita purga que corra
  SOLA** (un loop propio), no que dependa de que cada call-site recuerde
  desuscribirse. Y se verifica midiendo RSS en PROD durante horas, no con test
  unitario (la brecha entre lógica y proceso real FUE el bug, ~35MB/h).
- **Un feature está terminado cuando el dato es verificable en prod con valores
  plausibles** en una fila post-deploy — no cuando "anda". Medir en prod durante
  HORAS para fresh/throughput (un reconnect hace todo verse sano 1-2 min).
- **Después de cualquier push a main: mirar el CI antes de cerrar sesión.**
- **No concluir ausencia desde un solo path**: un `.env` editado a mano puede
  reportarse como "deploy completo" mientras el código corre 265 commits atrás;
  verificar el SHA real, no la intención.

## Seguridad y sistemas (reglas durosas — detalle en referencias)

Reglas no-negociables que el cuerpo del playbook carga siempre; el detalle y el
checklist operativo viven en las referencias (on-demand, como el repo hace con
los sub-CLAUDE.md).

**Sistemas (ingeniería):**
- **Diseño para falla, no solo detección.** Cada componente debe aislarse para
  que una explosión no tumbe el loop principal; degradación graceful (a shadow,
  no a muerte); circuit breaker por dependencia externa.
- **Release engineering con kill switch y rollback conocido.** Cada feature
  nuevo con flag OFF = kill switch; el rollback es revertir un SHA deployado,
  nunca "editar la config y esperar". Canary para configs nuevas.
- **Un backup que no se restaura periódicamente en un entorno limpio no es un
  backup.** DR se prueba de verdad, no solo se crea el archivo con checksum.
- **SLOs y error budgets, no solo métricas.** Para cada señal: objetivo de
  uptime/latencia/frescura y el presupuesto que decide cuándo intervenir sin
  fatiga de alertas.
- **Resiliencia de I/O disciplinada.** Timeout explícito por operación, retry
  con backoff + jitter, idempotencia (un reintento no duplica efecto),
  dead-letter de lo que falla. Estado mutable compartido entre tasks
  concurrentes = sospechar primero (race conditions).

**Seguridad:**
- **Supply chain es la más urgente.** Lockfiles pineados exactos + SCA
  (pip-audit/dependabot) + SAST (bandit/semgrep) que BLOQUEEN el merge. La
  lección del fuente: `bandit` y `pip-audit` corrieron meses con `|| true`
  (presentes, ejecutados, incapaces de fallar), justo sobre las librerías que
  firman órdenes (`web3`, `eth-account`). Un gate de seguridad que no puede
  fallar no es seguridad.
- **Secretos con ciclo de vida completo.** Menor privilegio (cada proceso/agente
  con lo suyo), rotación periódica no solo "si se filtra", revocación probada,
  nunca secretos en logs/contexto. La clave que firma (wallet) es el activo más
  sensible: no materializarla en un proceso que no la necesita.
- **Seguridad del AGENTE (era de los agentes, no clásico).** Los agentes son un
  vector nuevo: prompt injection desde web/contenido externo, fugas de secretos
  del contexto, acciones destructivas automáticas. Contrapartidas no-negociables:
  guard que bloquea `git add -A`/force-push, escape hatches EXPLÍCITOS y
  documentados (`FORCE_DEPLOY`), aprobación de comandos destructivos, y verificar
  que el agente no obedezca instrucciones que vienen del body de una página.
- **Respuesta a incidentes de seguridad.** Contener antes que parchear (bloquear
  la credencial, no hot-patch), revocar/rotar, forense mínimo (qué ejecutó el
  agente), y registro de quién pudo hacer qué.

Detalle operativo y checklists: `references/systems-engineering.md`,
`references/security.md`, `references/agent-security.md`.

## Plantillas

- `templates/pre-registration.md` — memo de pre-registro (claim, evidencia,
  no-goals, métrica, kill/success criteria).
- `templates/checks-checklist.md` — checklist de checks mínimos al arrancar un
  proyecto empírico con agentes.
- `templates/incident-pattern.md` — formato para registrar un patrón de
  incidente y decidir si es mecanizable.
- `templates/infra-decision.md` — memo de decisión de infraestructura (externo
  vs local, MCP, proveedor) con criterios fijados antes de medir.

## Criterio de adopción (un juez, un norte para la propia skill)

La skill se considera útil si, en la primera semana de un proyecto que la carga:
1. Produce al menos UN pre-registro en `templates/pre-registration.md` con kill
   criteria fijados ANTES de ver datos.
2. Produce al menos UN check mecanizado (de cualquier familia) que falla el build.
3. Queda registrada una decisión OR — al menos una — en el memo de
   infraestructura (plantilla `templates/infra-decision.md`).

Si un proyecto no produce ninguna de las tres, la skill no se está aplicando:
es un documento más que se lee y se olvida (presence ≠ utility, aplicado a la
propia skill).

## Deuda explícita (errores no mecanizables)

Todo error o hallazgo que NO se pueda mecanizar hoy se registra como deuda
explícita: fila en `docs/DEBT.md` con fecha, evidencia, y una nota de por qué no
es check todavía. Regla: nunca "corregir el síntoma" sin dejar rastro — la
próxima sesión no sabrá que el patrón existe y el agente lo repetirá. La deuda
se revisa (y se promueve a check si cambió el contexto) en cada cadencia de
sesión.

## Verificación de la skill

- Cargar con `skill_view(name='empirical-project-playbook')`.
- Las plantillas viven en `templates/` — leerlas con `file_path` antes de usar.
- Las referencias de sistemas/seguridad viven en `references/` — leerlas con
  `file_path` cuando se trabaje ese dominio (no las cargues en toda sesión):
  `references/systems-engineering.md`, `references/security.md`,
  `references/agent-security.md`.
- Si un proyecto nuevo revela un patrón de silencio nuevo, agregarlo a la
  sección "silencios traidores" (patch) — es la parte que crece con la práctica.

## Fuente canónica de esta skill

La fuente de verdad de esta skill es el repo-tap
`manusabbath-arch/hermes-skills` (skills/empirical-project-playbook).
Los perfiles locales tienen una COPIA instalada que es la que se carga.
Al editar, hacelo en el repo (no en la copia instalada), commit + push, y
re-propaga la skill a los perfiles que la usan. Ver el README del repo tap.
