---
name: background-jobs-scheduling
description: Jobs en background y tareas programadas en la API NestJS — idempotencia, un solo ejecutor entre varias instancias (lock distribuido o scheduler central), timeouts, reintentos, jobs largos reanudables por lotes con checkpoint, contexto de tenant y actor dentro del job, zona horaria de los cron, apagado limpio, visibilidad (último éxito, duración, fallos) y recordatorios programados. Usar al escribir un cron, un worker, un proceso por lotes, un recordatorio de cita o un reproceso masivo, y al diagnosticar un job que corrió dos veces, no corrió o quedó colgado.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Jobs en background y tareas programadas

`backend-development` dice *que* el trabajo no sincrónico va a una cola. `async-messaging-events`
cubre eventos, outbox y consumidores. Acá: trabajo **disparado por el reloj** o **por lotes**,
que corre sin usuario mirando — por eso falla en silencio si no lo diseñás para que se note.

## 1. Elegir el mecanismo

| Necesidad | Mecanismo |
|---|---|
| Tarea periódica liviana, una sola instancia de la app | `@Cron` de `@nestjs/schedule` |
| Tarea periódica con **varias instancias** | scheduler central de la cola (BullMQ Job Schedulers) o `@Cron` + lock distribuido |
| Trabajo diferido a una hora concreta (recordatorio) | tabla de pendientes + barrido, o job con `delay` |
| Trabajo pesado o por lotes | cola + worker dedicado, separado del proceso HTTP |
| Mantenimiento de base (purgas, vacuum) | preferí herramientas de la base/infra antes que la app |

**Trampa central**: `@Cron` se registra en **cada instancia** del proceso. Con tres réplicas, el
cron corre tres veces. Desarrollás con una instancia y el bug aparece en producción.

## 2. Un solo ejecutor

1. **Scheduler en la cola**: BullMQ `queue.upsertJobScheduler(id, { pattern, tz }, { name, data })`
   es idempotente por `id` — todas las instancias pueden llamarlo al arrancar y existe un solo
   scheduler; el job resultante lo toma un solo worker.
2. **Lock distribuido** alrededor del cuerpo del cron:
   - Postgres: `pg_try_advisory_lock(key)` (de sesión) o `pg_try_advisory_xact_lock(key)`
     (se libera al terminar la transacción). Si devuelve `false`, otra instancia lo tiene: **salí
     sin error**. Ver `concurrency-and-locking`.
   - Redis: `SET clave valor NX PX <ms>` con valor único y liberación que verifica ese valor.
     El TTL debe superar la duración máxima del job, o renovarse.
3. **Proceso worker único** dedicado a cron: simple, pero es un punto único de falla — necesita
   alerta de "no corrió".
4. Aun con lock, el cuerpo **debe ser idempotente** (§3): los locks expiran, los relojes derivan
   y los reinicios pasan a mitad de ejecución.

```ts
// ❌ corre una vez por réplica
@Cron(CronExpression.EVERY_HOUR)
async sendReminders() { await this.reminders.sendDue(); }

// ✅ un solo ejecutor, sin solaparse consigo mismo, con zona horaria explícita
@Cron('0 0 * * * *', { name: 'reminders', timeZone: 'America/La_Paz', waitForCompletion: true })
async sendReminders() {
  await this.locks.withTryLock('cron:reminders', () => this.reminders.sendDue());
}
```

`waitForCompletion: true` evita que una corrida nueva arranque mientras la anterior sigue **en
esa instancia** (las ejecuciones que caen en el medio se saltean). No coordina entre instancias.

## 3. Idempotencia del job

- Diseñá como **barrido de estado**, no como "hacer X ahora": *"enviar todo recordatorio con
  `due_at <= now()` y `sent_at IS NULL`"*. Correrlo dos veces, tarde o tras un crash da el mismo
  resultado.
- Reclamá cada ítem atómicamente antes de procesarlo: `UPDATE … SET claimed_at = now() WHERE id = $1 AND claimed_at IS NULL`
  o `SELECT … FOR UPDATE SKIP LOCKED`. Filas afectadas = 0 ⇒ otro lo tomó.
- Marcá el resultado en la **misma transacción** que el efecto local. Para efectos externos
  (email, push), clave de idempotencia hacia el proveedor (`notifications-delivery`).
- Un reclamo puede quedar huérfano si el worker muere: `claimed_at` viejo sin `sent_at` se
  libera tras un umbral.
- Nunca dependas de "corre exactamente a las 03:00 una vez". Dependé del estado.

## 4. Timeouts, reintentos y fallos

1. **Timeout por job y por ítem**. Un job sin timeout retiene el lock para siempre y bloquea
   las corridas siguientes. BullMQ no mata un job por tiempo: implementalo en el handler
   (`AbortSignal`, timeouts en las llamadas de red).
2. Reintentos con `attempts` + `backoff` para errores transitorios; `UnrecoverableError` para
   los permanentes; agotados ⇒ failed/DLQ con alerta (`async-messaging-events` §6).
3. **Aislá el fallo por ítem**: un registro roto no debe abortar el lote. `try/catch` por ítem,
   registrá el fallo con su id, seguí, y reportá `procesados / fallidos` al final. Si fallan
   *todos*, eso sí es error del job.
4. `@Cron` e `@Interval` de NestJS envuelven el método en un try-catch: **una excepción no
   tumba la app pero tampoco avisa a nadie**. Capturá, logueá con contexto y emití métrica vos.
5. *Stalled jobs* (BullMQ): si el worker bloquea el event loop o muere, el job vuelve a la cola
   y otro lo toma ⇒ doble ejecución. Otra razón para §3. No hagas trabajo CPU-intensivo
   sincrónico en el handler.

## 5. Jobs largos: lotes con checkpoint

- Procesá en **lotes acotados** (cientos/miles, medí), cada uno en su transacción corta. Una
  transacción de horas retiene locks, infla el WAL y pierde todo si falla al final.
- **Paginá por clave** (`WHERE id > :ultimo ORDER BY id LIMIT :n`), no por `OFFSET`: el offset
  se corre si el conjunto cambia mientras procesás (`code-efficiency`).
- **Checkpoint persistido** (último id procesado, contadores) tras cada lote ⇒ el job es
  **reanudable**: tras un reinicio sigue donde quedó.
- Con MikroORM: `em.clear()` o un fork nuevo por lote; si no, el identity map crece sin límite
  y la memoria explota (`code-efficiency`).
- Limitá el ritmo (pausa entre lotes, concurrencia acotada) para no ahogar a los usuarios
  interactivos ni a un proveedor externo con rate limit.
- Reprocesos masivos y backfills: modo *dry-run* que cuenta y muestra qué haría, y corrida
  acotada (`--limit`, por tenant) antes de la total (`data-quality-validation`).

## 6. Contexto dentro del job

No hay request ⇒ no hay tenant, ni actor, ni traza implícitos.
- **Tenant**: o el payload trae `tenantId`, o el job itera tenants y abre **contexto y
  transacción por tenant**. Un job que corre "sin tenant" con el filtro desactivado es la fuga
  clásica (`multi-tenancy`).
- **Actor**: los jobs de sistema usan una identidad de servicio explícita y auditable; los que
  actúan por un usuario llevan su id y no amplían sus permisos (`authz-access-control`).
- **Traza**: `correlationId` en el payload y en cada log; nombre del job, intento y duración
  como atributos estructurados (`backend-observability`).
- **EntityManager**: uno nuevo por job (y por lote en jobs largos). Nunca el global.

## 7. Tiempo y zonas horarias

1. Guardá instantes en UTC (`timestamptz`). La zona horaria es dato de **presentación y de
   regla de negocio**, y pertenece al usuario u organización, no al servidor.
2. Todo cron declara su zona: `timeZone` en `@Cron`, `tz` en el scheduler de BullMQ. Sin
   declararla corre en la zona del contenedor, que suele ser UTC y distinta a la de tu máquina.
3. "Todos los días a las 08:00" para usuarios en varias zonas **no** es un cron: es un barrido
   frecuente que busca quién tiene `due_at <= now()`, con `due_at` calculado en la zona de cada uno.
4. Zonas con horario de verano: una hora local puede no existir o repetirse. Calculá con una
   librería con base tz, nunca sumando offsets a mano.
5. Los relojes de las instancias derivan: usá `now()` de la base como referencia única dentro
   de una transacción cuando la comparación decide quién procesa.

## 8. Recordatorios programados

Patrón preferido — **tabla de pendientes + barrido**:
1. Al crear/modificar la cita, `UPSERT` del recordatorio: `(appointment_id, kind, due_at, sent_at NULL)`.
2. Un barrido frecuente envía lo vencido y no enviado, con reclamo atómico (§3).
3. **Revalidá al disparar**: la cita pudo cancelarse, moverse, o el usuario desactivar el canal.
   Releé el estado actual; no confíes en el payload de cuando se programó.
4. Reprogramar = actualizar `due_at`; cancelar = borrar o marcar. No hay job huérfano que cazar.
5. Ventana de cortesía: un recordatorio vencido hace demasiado **no se envía**, se marca
   `skipped` (nadie quiere a las 3 AM el aviso de la cita de ayer). Respetá horas de silencio.

Alternativa: job con `delay` por recordatorio. Sirve para volúmenes bajos, pero reprogramar
exige encontrar y quitar el job anterior, y el estado vive en Redis en vez de en tu base.

## 9. Apagado limpio

- `app.enableShutdownHooks()` y cerrar workers en `onModuleDestroy`/`onApplicationShutdown`.
- BullMQ `await worker.close()` deja de tomar jobs y **espera a los activos, sin timeout
  propio**: asegurate de que tus jobs terminan, y que el período de gracia del orquestador
  (tiempo entre `SIGTERM` y `SIGKILL`) supera tu job más largo — o que el job es reanudable.
- Lo que no alcanza a terminar queda como *stalled* y lo retoma otro worker ⇒ §3 otra vez.
- Workers en un **proceso/despliegue separado** del HTTP: escalan distinto y un deploy de la
  API no corta un lote.

## 10. Visibilidad

El fallo típico de un cron no es que rompa: es que **deja de correr y nadie se entera**.
- Por job: `last_started_at`, `last_success_at`, duración, ítems procesados/fallidos, intento.
- **Alertá por ausencia**: "sin éxito en más de N períodos" (heartbeat / dead man's switch).
  Una alerta solo por error no detecta el job que nunca arrancó.
- Alertá por duración creciente (se acerca al período) y por backlog de pendientes vencidos.
- Registro de ejecuciones consultable (tabla `job_run`) — sirve de evidencia y de diagnóstico.
- Disparo manual controlado (endpoint admin o CLI, autorizado y auditado) para re-correr sin
  esperar al reloj.

## Anti-patrones

- `@Cron` a secas en una app con réplicas. `setInterval` en un servicio.
- Job "hacer X a las 03:00" no idempotente; reintento que duplica cobros o notificaciones.
- Una transacción gigante para todo el lote; `OFFSET` sobre un conjunto que muta.
- Desactivar el filtro de tenant "porque es un job". Zona horaria implícita del servidor.
- Excepción tragada por el wrapper del scheduler, sin log ni métrica.
- Alertar solo por error, nunca por ausencia de éxito.

## Checklist

- [ ] Mecanismo elegido sabiendo cuántas instancias corren; un solo ejecutor garantizado.
- [ ] Cuerpo idempotente: barrido de estado + reclamo atómico + marcado transaccional.
- [ ] Timeout por job e ítem; reintentos solo para transitorios; DLQ/failed con alerta.
- [ ] Fallo de un ítem no aborta el lote; se reporta procesados/fallidos.
- [ ] Jobs largos por lotes, paginados por clave, con checkpoint y `em.clear()`/fork por lote.
- [ ] Contexto de tenant, actor y traza reconstruido explícitamente; EM nuevo por job.
- [ ] Zona horaria declarada en cada cron; instantes en UTC; horarios por usuario como barrido.
- [ ] Recordatorios revalidan el estado actual al disparar; ventana de cortesía definida.
- [ ] Apagado limpio: shutdown hooks, `worker.close()`, gracia ≥ job más largo o job reanudable.
- [ ] `last_success_at` y alerta por **ausencia**; registro de ejecuciones; disparo manual auditado.
