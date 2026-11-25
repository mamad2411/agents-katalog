---
name: agent-ready-project
description: "Use when setting up or hardening a project that AI agents will build and modify - any codebase, not just data or trading. Covers the non-eludible validation loop (pre-commit, CI, pre-push), turning a check on over a dirty codebase with a ratchet baseline, docs that verify their own numbers, measuring lint debt instead of sweeping it, guards on every surface that can run the action, and the failure modes specific to agent-written code: invented API signatures, unverified self-reports, phantom wiring, silent-green tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [agents, ci, pre-commit, validation-loop, guards, doc-drift, lint-debt, testing, agent-security, bootstrap]
    related_skills: [empirical-project-playbook, empirical-system-invariants]
---

# Agent-Ready Project

Cómo dejar un proyecto listo para que agentes de IA lo construyan y lo modifiquen
sin que la calidad dependa de que alguien se acuerde de revisar. Es el **arnés de
construcción**, no el método de investigación: aplica igual a un CRUD, una API o
un pipeline.

**Origen:** polymarket-trading-bot (2026), ~500 commits construidos con agentes
(Claude Code, Hermes, OpenCode, Codex). Cada regla de acá nació de un fallo real
que costó tiempo o plata; la evidencia va con la regla.

**Diferencia con `empirical-project-playbook`:** ese dispara cuando el proyecto
MIDE algo y decide con datos (pre-registro, anti-minería, kill criteria). Este
dispara siempre que un agente escriba código. Un proyecto que no mide nada
necesita el arnés igual.

## Cuándo usar esta skill

- Arrancar un proyecto que va a construirse mayormente con agentes.
- Endurecer uno existente que ya acumuló código de agente sin red de seguridad.
- Prender un check nuevo sobre un codebase que ya viola la regla.
- Diagnosticar por qué "los tests pasan" y aun así llegan bugs a producción.

## La tesis

Un agente produce código a una velocidad que la revisión humana no sigue. Lo que
decide la calidad del resultado NO es el prompt: es **el loop de validación**.
La prosa —CLAUDE.md, comentarios, docs— no frena nada. El patrón "wiring
fantasma" se escribió en la doc después de cada una de sus primeras apariciones
y recurrió **seis veces igual**. Dejó de recurrir el día que alguien escribió el
script que falla el build.

Corolario operativo: **cada fallo del agente se mecaniza en la MISMA sesión.**
Un check nuevo, o una fila fechada en un registro de deuda si hoy no es
mecanizable. Nunca "corregir el síntoma" y seguir — la próxima sesión no va a
saber que el patrón existe y el agente lo va a repetir.

## El loop de validación (la pieza central)

Tres capas, cada una más cara y más lenta que la anterior, ninguna eludible:

1. **Pre-commit** — estático, segundos. Formato, lint, y los checks propios del
   proyecto (patrones de incidente, wiring fantasma, doc drift).
2. **CI bloqueante** — en el PR. Ve cosas que un dry-run local no ve:
   `NameError` por un import que existe solo en tu venv, regresión de versión de
   una dependencia. **Nunca mergear con CI en rojo.**
3. **Pre-push / suite completa** — tests reales antes de que salga de la máquina.

Reglas que hacen que el loop sirva de verdad:

- **Un gate que no distingue "falló" de "NO CORRIÓ" culpa a lo primero.**
  `pytest | grep passed || fail` da idéntico resultado con tests rojos que con el
  intérprete inexistente. Verificar el intérprete ANTES de interpretar la salida
  (`python -m pytest --version` como paso propio).
- **Un gate que no puede fallar no es un gate.** Firmas a buscar: `|| true`,
  `continue-on-error`, `stages: [manual]`, un `# noqa` varado en la línea de
  cierre. En el proyecto fuente, `bandit` y `pip-audit` corrieron **meses** con
  `|| true` — presentes, ejecutados, incapaces de fallar — justo sobre las
  librerías que firmaban órdenes con dinero real.
- **Versiones de lint pineadas en UN solo lugar.** Si `.pre-commit-config.yaml`
  dice `black==25` y `requirements-dev.txt` dice `black>=23`, el hook local y el
  CI nunca convergen: reformateos en bucle para siempre.
- **Escape hatches explícitos, nombrados y documentados** (`ALLOW_MAIN_COMMIT`,
  `FORCE_DEPLOY`, `ALLOW_DRIFT`). Un gate sin escape se termina desactivando
  entero; uno con escape nombrado deja rastro de quién lo usó y por qué.

## Prender un check sobre código que ya lo viola: baseline con trinquete

El motivo #1 por el que un check útil nunca se prende es que el codebase ya tiene
200 violaciones y nadie va a parar todo para limpiarlas. La salida no es
suprimir el check: es **congelar la deuda conocida y fallar solo si crece**.

```
.incident_baseline.json
{ "acknowledged": [ {"file": "src/foo.py", "attr": "cached_book"}, ... ] }
```

- El check reporta `nuevos` (falla el build) y `conocidos` (informa).
- **Indexar la baseline por identidad estable, NO por línea.** Si la clave
  incluye el número de línea, editar cualquier cosa arriba inventa un hallazgo
  "nuevo" y el equipo aprende a ignorar el check. El proyecto fuente usa
  `file + attribute`.
- Reportar también las claves **stale** (en la baseline pero ya inexistentes):
  es deuda que se pagó y hay que sacar del archivo, o el trinquete afloja.

Esto convierte "algún día lo limpiamos" en una curva que solo puede bajar.

## La doc que verifica sus propios números

Un doc de arquitectura abría con `main.py` = 4541 líneas. Tres días después eran
1317. **Nadie mintió**: la extracción se mergeó y el doc no se tocó. El daño no
es un bug — es que el próximo agente decide arquitectura sobre un mapa viejo.

La regla: **la doc puede afirmar números; el número tiene que ser generado y
chequeado, no tipeado y confiado.**

```markdown
<!-- verify
id: main-py-loc
kind: loc
target: src/main.py
expect: 1317
tolerance: 2%
-->
```

Un script recorre los bloques, recalcula, y falla el build si el valor real se
fue de la tolerancia. Ver `scripts/doc_verify.py` (stdlib, agnóstico, exit code)
y la especificación completa en `templates/verify-block.md`.

Gemelos del mismo problema, que valen tanto como el de arriba:

- **Drift entre el default del código y la config REAL de producción.** Un
  `MAX_POSITIONS` que el código default-ea en 6 y el `.env` de prod tiene en 2
  bloqueaba todas las operaciones — y cualquier análisis que leyera el código
  razonaba sobre un sistema que no existe.
- **Drift entre el SHA deployado y `origin/main`.** Una sesión editó el `.env`
  por SSH y reportó "deploy completo"; producción corría **265 commits atrás**.
  Verificar el SHA real, nunca la intención.
- **Revisión de reglas muertas al tocar la doc.** Una regla que ya no describe el
  sistema real es PEOR que no tenerla: el agente la obedece y hace daño
  silencioso. Al editar, verificar que las rutas citadas existen y que los
  verificadores que la prosa declara siguen en CI.

## Deuda de lint: medir, nunca barrer

Si un linter tira 186 hallazgos, la reacción por default es suprimir la familia
entera en la config. Es el error caro: **entre los que barrés hay bugs reales.**

El caso que lo prueba: `F841` (variable asignada que nadie usa) es **el detector
más barato del wiring fantasma** — el bug que el proyecto persiguió seis veces
escribiendo scripts a medida durante meses. Estaba apagado en la config del
linter todo ese tiempo.

Método correcto, aplicado a `B905` (`zip()` sin `strict=`), 53 casos vivos:

1. **Clasificar uno por uno.** 46 tenían los largos garantizados iguales por
   construcción → `strict=True`, que no cambia comportamiento y convierte una
   futura ruptura de esa invariante en un error ruidoso.
2. 3 truncaban a propósito → `strict=False` **con el motivo al lado**.
3. **4 eran defectos REALES** — largos que difieren de verdad. Se habrían barrido
   con la familia entera.
4. Lo que queda ignorado se ignora **por deuda medida y contada**, no en bloque:
   `B907 (72), B007 (19)` con el número al lado, para que se vea si crece.

Regla de cierre: **las supresiones que sobreviven llevan el motivo al lado.
Visibles, no aprobadas.** Un `# noqa` pelado es deuda que nadie va a encontrar.

## Guards: todas las superficies, no solo la del agente

Una acción destructiva se puede ejecutar por varios caminos. Un guard que cubre
uno solo no es un guard: es una sugerencia. En el proyecto fuente el git-guard
está **triplicado a propósito**: hook de `pre-commit`, plugin del agente, y hook
`PreToolUse` del CLI — *"para el caso en que el commit lo haga una persona o una
herramienta sin plugin"*.

Lo mínimo que un proyecto construido por agentes bloquea:

- `git add -A` / `git add .` → paths explícitos siempre (un agente comitea
  secretos y artefactos sin querer).
- Commit directo a `main` y `force-push`.
- Deploy sin `DRY_RUN` / sin confirmación.
- Comandos destructivos (`rm -rf`, `DROP`, `truncate`) fuera de un directorio
  temporal.

Y la contrapartida específica de la era de los agentes: **verificar que el agente
no obedezca instrucciones que vienen del contenido que está leyendo** (prompt
injection desde una página web, un issue, un README de dependencia).

## Modos de falla propios del código escrito por agentes

Esto no aparece en una checklist de code review clásica. Son formas que el agente
produce sistemáticamente:

- **Firmas de API inventadas.** El agente completa la firma desde lo que el modelo
  recuerda, no desde el código real. Costó **~15 iteraciones de corrección** en un
  solo tramo. Regla: verificar contra la definición y el schema REALES —
  `rg` la firma, abrir el módulo. Nunca contra la memoria del modelo.
- **Self-report de subagente sin verificar.** Un subagente reporta "PR creado,
  tests verdes". Verificar el handle real uno mismo: la URL, el SHA, la query de
  producción, el valor plausible. Usar subagentes solo para tareas **atómicas**;
  el contexto de diseño queda en la sesión principal.
- **Wiring fantasma.** `getattr(obj, "attr", {})` donde ninguna clase asigna
  `attr`. El default "seguro" ES el bug: nada crashea, nada loguea, el caller
  opera sobre estado vacío para siempre. En un caso había un comentario y un log
  **afirmando que el wiring estaba conectado**, porque el código se escribió con
  esa intención — la intención nunca se ejercitó end-to-end. Un `grep` del nombre
  no prueba que la instancia lo tenga: verificar `hasattr` sobre la instancia
  real, o a qué módulo apunta el import del call-site.
- **Tarea periódica silencio-verde.** La función solo loguea en la rama con datos:
  `if count > 0: log(...)`. Puede pasar días sin procesar nada y nadie se entera.
  **Log incondicional con el conteo, siempre.**
- **Test que cubre la versión vieja.** Un test que no llama a la función que
  refactorizaste da cobertura del código anterior. Confirmar que el test está en
  ROJO contra el código previo antes del fix.

## Disciplina de diagnóstico

- **Ante un check en rojo, leer su METADATA antes que su mensaje.** El mensaje
  resume; la metadata dice cuál sumando se movió, que es lo único que separa
  "defecto real" de "umbral mal calibrado". `Trade success: 11.2%` no distinguía
  nada; `failures=421` vs `rejections=11397` señaló la causa en un paso.
- **Mirar el `timestamp` antes de razonar sobre cualquier snapshot de salud.** Un
  `/health` cacheado describe otro instante. En un mismo día, dos conclusiones
  salieron falsas por razonar sobre un snapshot viejo.
- **Un sentinel "nunca pasó" va FUERA del dominio, no en su borde.** `0` como
  "nunca ocurrió" contra un reloj monotónico puede ser MENOR que el TTL en un
  proceso recién arrancado → el primer intento tras un restart se sirve de cache
  vacío o se saltea. Mordió dos veces en un día. El sentinel correcto es
  `float("-inf")` (o `None` con rama explícita).
- **No concluir un patrón con 2 muestras si la instrumentación junta más en
  minutos.** Un bug dominante se maldiagnosticó como timeout de red con 2
  muestras; con 351, el 95% era tamaño de frame.
- **Verificar el protocolo real contra el servidor, no contra el mock.** Los mocks
  congelan el protocolo viejo y ningún test agarra la ruptura.

## Operar sin romper producción

- **La DB de producción sirve al sistema en vivo: una query ad-hoc pesada es una
  interrupción, no una lectura.** Un `EXISTS` correlacionado o un join por `LIKE`
  con comodines de los dos lados no tienen índice que los salve. Una query propia
  quedó al **97% de CPU durante 1h21m** y dejó el health en `unhealthy`. Acotar
  por índice y por fecha; para exploración cara, copiar un backup.
- **Proceso huérfano (`PPID=1`) = nadie va a recibir su resultado. Matalo.**
- **Commits sin push no se deployan.** Un bugfix editado directo en el servidor no
  existe para nadie más.
- **Stash no es backup de trabajo multi-sesión.** Rama pusheada, o descarte
  consciente.
- **Producción = una unidad canónica.** Dos unidades de systemd con nombres
  parecidos = doble instancia y un debug de horas.
- **Después de cualquier push a main: mirar el CI antes de cerrar la sesión.**

## Doc raíz para agentes

- **Corta (~300 líneas) y con reglas por directorio lazy-load.** Cada línea del
  raíz carga en TODA sesión: bloat = menos precisión y más tokens. El detalle vive
  en `<dir>/CLAUDE.md` que se carga solo cuando se toca ese directorio.
- **Reglas "nunca X / siempre Y", con ejemplo, en orden de prioridad.**
- **El piso realista no es un número.** Recortar por debajo del contenido
  operativo vivo (runbook, reglas no negociables, tablas que un script parsea)
  degrada la red de seguridad. El objetivo es sacar historia y estado superseded
  a docs fechados con un puntero — no llegar a 300.
- **Versionar la doc del agente en el repo.** Es el activo que hace que la próxima
  sesión no re-derive los errores.

## Orden de adopción (un proyecto existente, sin parar todo)

1. **Guards destructivos** (git add -A, main, force-push). Barato, evita el daño
   irreversible desde el día 1.
2. **Loop de validación mínimo**: pre-commit con formato + lint, CI que corra los
   tests y que pueda fallar de verdad.
3. **Medir la deuda de lint** y prender las familias que hoy dan cero — atrapan
   bugs futuros a costo cero.
4. **Un check propio** del patrón que más te mordió, con **baseline con
   trinquete** para no bloquear el trabajo.
5. **Verify blocks** en los 3 números que la doc afirma y que más rápido envejecen.
6. **Characterization tests** antes del primer refactor de un módulo crítico:
   congelar el comportamiento actual, verificado por mutación (alterar un valor
   golden tiene que hacer fallar el test). Un refactor sin esto es ruleta.

## Criterio de adopción

La skill se está aplicando si, en la primera semana:

1. Existe un check propio del proyecto que **falla el build** y que se verificó
   por mutación (romperlo a propósito lo pone en rojo).
2. Al menos un fallo del agente se mecanizó en la misma sesión en que ocurrió.
3. La deuda que no se mecanizó quedó **contada** (baseline o registro fechado),
   no barrida.

Si no pasó ninguna de las tres, es un documento más que se lee y se olvida.

## Plantillas y scripts

- `templates/validation-loop-checklist.md` — checklist de arranque del arnés.
- `templates/verify-block.md` — especificación del bloque `<!-- verify -->`.
- `scripts/doc_verify.py` — verificador de bloques `verify` (stdlib, agnóstico,
  exit code). Uso: `python3 doc_verify.py --root . --docs README.md docs/`.
- `scripts/tests/` — tests herméticos del verificador.

## Fuente canónica

Repo-tap `manusabbath-arch/hermes-skills` (`skills/agent-ready-project`). Editar
acá, nunca la copia instalada.
