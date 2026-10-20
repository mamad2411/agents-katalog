---
name: agent-resource-control
description: Control de concurrencia y recursos cuando un agente trabaja en una máquina de desarrollo — qué se serializa (builds, test runners, navegadores Playwright con un solo worker), cuántos subagentes y cuándo, procesos en background sin huérfanos, puertos ocupados y límite de carriles activos. Usar antes de lanzar un build, una suite, un E2E, un servidor de desarrollo o un subagente; cuando la máquina se pone lenta o hay fallos intermitentes; y al cerrar un turno para limpiar lo que quedó corriendo.
effort: medium
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Control de recursos del agente

Una máquina de desarrollo no es un runner de CI. Comparte CPU, memoria, disco y puertos
entre el editor, el stack local (API, base, front), el navegador de la persona y lo que
vos lances. Saturarla no acelera nada: produce timeouts, tests que fallan "porque sí" y
diagnósticos falsos. **Un fallo intermitente bajo carga es, hasta que se demuestre lo
contrario, un fallo de recursos — no del producto.**

Los límites concretos (números, comandos, scripts) los fija el `CLAUDE.md` del proyecto.
Esta skill da los valores por defecto cuando el proyecto no dice nada.

## 1. Regla base: un proceso pesado a la vez

Son pesados: compilación/build, typecheck de un repo grande, test runner, E2E con
navegador, rebuild de la base o carga de seeds, instalación de dependencias, emulador
móvil.

1. No lances dos pesados en paralelo, ni en el mismo repo ni en repos hermanos.
2. No encadenes el siguiente hasta que el anterior **terminó** (no "parece que terminó").
3. Lecturas, greps y ediciones sí van en paralelo: no compiten por nada relevante.

## 2. Tabla tarea → paralelismo permitido

| Tarea | En máquina de desarrollo | Nota |
|---|---|---|
| Read / Grep / Glob / ediciones independientes | Paralelo libre | — |
| Lint o typecheck acotado a archivos tocados | 1 por vez | Liviano si está bien acotado |
| Build / typecheck de repo completo | **Serial, 1** | Nunca junto a una suite |
| Tests unitarios | **1 runner**; workers internos: el default del proyecto | Bajá workers si hay timeouts |
| Tests de integración con base real | **Serial, 1 runner** | Comparten la base: además de recursos, hay colisión de datos |
| E2E Playwright — diagnóstico/fix | **`--workers=1`**, un solo proyecto (navegador), `--max-failures=1`, sin reintentos | Test afectado, no la suite |
| E2E Playwright — regresión del módulo | `--workers=1`, serial | Después de estabilizar |
| E2E cross-browser final | Un proyecto por comando, **secuencial** | Nunca todos los navegadores a la vez |
| Rebuild de base / seeds / generadores | **Serial, exclusivo** | Nada más contra esa base mientras corre |
| Servidores de desarrollo | Una instancia por servicio | Reusá la que ya está levantada |
| Subagente de solo lectura | 1 por defecto (ver §4) | — |
| Subagentes que **escriben** | Solo con archivos disjuntos y aislamiento | Ver §4 |
| CI | Paralelismo y sharding según el pipeline | Esta tabla no aplica a CI (`ci-cd-pipeline`) |

`--fully-parallel` y `--workers>1` en E2E local: no, salvo que el proyecto lo declare
seguro. La estabilidad del diagnóstico vale más que los minutos ahorrados.

## 3. Procesos en background

Un proceso en background es una deuda que contraés: la pagás antes de cerrar el turno.

1. Antes de levantar un servidor, **fijate si ya está arriba** (puerto en escucha, health). Reusalo.
2. Usá background solo para lo que debe seguir vivo mientras trabajás (servidor de desarrollo, watcher). Un comando que termina se corre en primer plano.
3. Anotá lo que lanzaste: qué, en qué puerto, cómo se detiene.
4. No uses esperas fijas para "darle tiempo": sondeá la condición real (puerto abierto, health OK, línea de "listo" en el log).
5. Al terminar —o al fallar— **detené lo que vos levantaste**. No mates procesos que no lanzaste: pueden ser de la persona.
6. Watchers y modos `--watch` en una sesión de agente casi nunca hacen falta: corré la versión de una sola pasada.

## 4. Subagentes

Un subagente cuesta contexto, tokens y coordinación. Se justifica cuando se cumplen **todas**:

1. La tarea es aislable y su enunciado se entiende sin tu contexto.
2. No va a editar los mismos archivos que vos ni que otro subagente.
3. El resultado **reduce** tu contexto (te quedás con la conclusión, no con los dumps).
4. Anunciás por qué lo necesitás.
5. No excede el límite de subagentes activos del proyecto.

Valores por defecto:

- **Un carril activo por vez.** No abras el siguiente con el actual en QA rojo.
- **Un subagente activo por vez** en trabajo de implementación; el agente principal implementa.
- Discovery e investigación: subagente de **solo lectura**.
- Fan-out mayor (varios en paralelo) solo para trabajo **independiente y sin estado compartido** —por ejemplo redactar documentos separados— y con pedido explícito de quien dirige el trabajo. Varios subagentes lanzando builds o suites en la misma máquina violan §1 aunque cada uno cumpla las reglas.
- Subagentes que escriben en paralelo sobre el mismo repo: solo con aislamiento (worktree o equivalente) y archivos disjuntos.

Roles, contratos de entrada/salida y patrones de fan-out: `agent-orchestration`.

## 5. Puertos

- Puerto ocupado ≠ "matar lo que esté ahí". Primero identificá **qué** proceso lo tiene.
- Si es el servicio que necesitás y está sano: usalo.
- Si es un huérfano **tuyo** de un intento anterior: detenelo y anotalo.
- Si no es tuyo: no lo toques; preguntá o usá otro puerto si el proyecto lo permite.
- No cambies puertos en la config versionada para esquivar un conflicto local.

Cómo mirar quién escucha (los comandos dependen del SO; en Windows ver
`windows-dev-environment`): `netstat -ano` filtrando el puerto y luego el PID, o
`Get-NetTCPConnection -LocalPort <n>` en PowerShell.

## 6. Señales de saturación y qué hacer

| Señal | Lectura | Acción |
|---|---|---|
| Timeouts en tests que antes pasaban | Carga, no regresión | Bajá workers, corré el test solo, re-evaluá |
| Un E2E pasa solo y falla en la suite | Estado compartido o recursos | Serial + aislar datos (`test-data-management`) |
| Builds cada vez más lentos | Procesos acumulados | Revisá huérfanos y watchers |
| `EADDRINUSE` / puerto en uso | Instancia previa viva | §5 |
| Memoria agotada en build o runner | Dos pesados a la vez, o workers de más | §1 y bajar workers |

Antes de clasificar un fallo como bug de producto, re-ejecutalo **solo y con la máquina
tranquila**. Nunca subas reintentos ni timeouts para tapar saturación.

## 7. Candados automáticos

Si el proyecto impone estos límites con hooks (veto a background, tope de subagentes,
gate de cierre), respetalos: son la política, no un obstáculo. Conocé sus límites —un
guard puede quedar inerte en un SO donde la métrica que usa no existe— y no dependas de él
para portarte bien. Desactivar un guard exige autorización explícita y queda dicho en el
reporte. Diseño de esos candados: `hooks-and-guardrails`.

## Anti-patrones

- ❌ Build + suite + E2E al mismo tiempo "para ganar tiempo".
- ❌ E2E local con todos los navegadores y todos los workers.
- ❌ Levantar una segunda instancia del servidor porque no miraste si ya había una.
- ❌ Matar por nombre todos los procesos `node`/`python` de la máquina.
- ❌ Esperas fijas en vez de sondear la condición.
- ❌ Subir timeouts o reintentos para que un test saturado pase.
- ❌ Cerrar el turno con un servidor o un watcher tuyo todavía corriendo.
- ❌ Cinco subagentes corriendo tests sobre la misma base.

## Checklist

- [ ] Hay a lo sumo un proceso pesado corriendo, y esperé a que el anterior terminara.
- [ ] E2E local con `--workers=1`, un navegador, y en diagnóstico `--max-failures=1`.
- [ ] Cross-browser: un proyecto por comando, en secuencia.
- [ ] Verifiqué si el servidor ya estaba arriba antes de levantar otro.
- [ ] Cada proceso en background que lancé está anotado y lo detuve al terminar.
- [ ] No maté procesos ajenos ni cambié puertos en config versionada.
- [ ] Los subagentes cumplen las cinco condiciones de §4 y el límite del proyecto.
- [ ] Un carril activo; ninguno nuevo con QA en rojo.
- [ ] Los fallos intermitentes se re-ejecutaron solos antes de clasificarlos.
- [ ] No desactivé ningún candado sin autorización explícita.
