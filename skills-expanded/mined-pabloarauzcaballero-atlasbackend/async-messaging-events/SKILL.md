---
name: async-messaging-events
description: Mensajería asíncrona y eventos en la API NestJS — outbox transaccional, entrega at-least-once y consumidores idempotentes, orden, reintentos con backoff y dead-letter, eventos de dominio vs de integración, sagas con compensación y observabilidad de colas. Usar al publicar un evento, escribir un consumidor, sacar trabajo del request (emails, notificaciones, integraciones), coordinar un flujo que cruza módulos o servicios, o diagnosticar mensajes duplicados, perdidos o fuera de orden — incluido el aviso que se duplica o nunca sale cuando falla el guardado (outbox).
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Mensajería asíncrona y eventos

`backend-development` establece que el trabajo no sincrónico va a una cola y que no se llama a
un externo dentro de una transacción. Esta skill es el **cómo**: garantías de entrega, outbox,
idempotencia, orden, versionado y sagas. Jobs programados y cron: `background-jobs-scheduling`.

## 1. ¿Async o no?

| Señal | Decisión |
|---|---|
| El usuario necesita el resultado para seguir | **sincrónico** |
| Efecto secundario que puede tardar o fallar sin invalidar la operación (email, push, webhook, indexar) | async |
| Dependencia externa lenta o inestable | async + reintentos |
| Varios módulos reaccionan al mismo hecho | evento |
| Invariante que debe valer **ya** (saldo, cupo de agenda, unicidad) | sincrónico, en la misma transacción |

Async no es gratis: introduce consistencia eventual, duplicados, desorden y un estado
"en proceso" que la UI tiene que mostrar (`frontend-ux-states`). Si el flujo entero cabe en una
transacción local, no lo partas.

## 2. Vocabulario

- **Comando**: pedido dirigido a un dueño ("enviar recordatorio"). Un solo consumidor. Puede rechazarse.
- **Evento**: hecho ya ocurrido, en pasado ("CitaConfirmada"). Cero o N consumidores. No se rechaza.
- **Evento de dominio**: interno al módulo/servicio; puede ser rico y cambiar con el modelo.
- **Evento de integración**: contrato público entre módulos/servicios; estable, versionado,
  mínimo. Nunca publiques la entidad del ORM: mapeá a un payload propio.
- Un evento **no lleva datos sensibles de más**: identificadores y lo mínimo; el consumidor autorizado
  consulta el resto (`data-privacy-sensitive`).

## 3. Outbox transaccional

El problema: `commit` en la base **y** `publish` en el broker son dos sistemas. Si publicás
antes del commit, anunciás algo que puede no haber pasado; si publicás después y el proceso
muere en el medio, el evento se pierde. No hay orden correcto: hay outbox.

1. En la **misma transacción** que el cambio de negocio, insertá una fila en `outbox`
   (`id`, `aggregate_id`, `type`, `version`, `payload`, `tenant_id`, `occurred_at`, `published_at NULL`).
2. Un *relay* (proceso aparte) lee las filas pendientes en orden, publica al broker y marca
   `published_at`. Si muere entre publicar y marcar, **republica** ⇒ at-least-once.
3. Varias instancias del relay: tomá filas con `SELECT … FOR UPDATE SKIP LOCKED` para no
   pisarse (`concurrency-and-locking`).
4. Purga periódica de filas publicadas viejas; alerta si la antigüedad de la pendiente más
   vieja crece.

```ts
// ✅ cambio + evento en una sola unidad atómica (MikroORM)
await em.transactional(async (tx) => {
  appointment.confirm();
  tx.persist(new OutboxMessage({ type: 'appointment.confirmed', version: 1,
    aggregateId: appointment.id, tenantId, payload: { appointmentId: appointment.id } }));
});
// ❌ await queue.add(...) dentro o inmediatamente después, sin outbox: evento fantasma o perdido
```

Excepción pragmática: si el efecto es descartable (métrica, invalidación de caché que tiene
TTL igual), publicar post-commit sin outbox es aceptable. Decidilo explícitamente.

## 4. At-least-once ⇒ consumidores idempotentes

Exactly-once de punta a punta no existe en la práctica; asumí duplicados **siempre**.

| Técnica | Cómo | Cuándo |
|---|---|---|
| Tabla de mensajes procesados | `INSERT (consumer, message_id)` con `UNIQUE` en la **misma transacción** que el efecto; violación ⇒ ya procesado, ack | default |
| Operación naturalmente idempotente | `UPSERT`, "setear estado X", no "sumar 1" | cuando el modelo lo permite |
| Guarda de estado/versión | aplicar solo si el agregado está en el estado esperado (`state-machines-workflows`) | transiciones |
| Clave de idempotencia hacia el externo | pasar `message_id` al proveedor (email, pago) | efectos fuera de tu base |

- El `message_id` lo genera el **productor** una vez; un reintento reusa el mismo id.
- Efecto externo no idempotente (mandar un SMS) + proveedor sin clave de idempotencia ⇒
  registrá "intentado" antes y "enviado" después, y aceptá por diseño cuál es el mal menor
  (duplicar o perder) — ver `notifications-delivery`.
- BullMQ: un `jobId` propio evita encolar el duplicado mientras el job exista; ojo que
  `removeOnComplete`/`removeOnFail` borran el job y con él esa protección. No reemplaza la
  idempotencia del consumidor.

## 5. Orden

- No asumas orden global. Si importa, importa **por agregado** (todas las cosas de *esta* cita).
- Opciones: particionar/agrupar por `aggregate_id` con un solo consumidor activo por clave;
  o llevar `sequence`/versión del agregado en el evento y que el consumidor descarte lo viejo
  y reencole lo adelantado.
- Reintentos con backoff **rompen el orden**: un mensaje reintentado llega después de su sucesor.
  Diseñá consumidores que toleren eso (guarda de versión) en vez de pelear contra el broker.
- Preferí eventos que llevan el **estado resultante** a eventos delta cuando el orden es frágil.

## 6. Reintentos, backoff y dead-letter

1. Clasificá el error: **transitorio** (timeout, 5xx, lock, conexión) ⇒ reintentar;
   **permanente** (payload inválido, entidad inexistente, regla de negocio) ⇒ no reintentar.
2. BullMQ: `attempts` + `backoff: { type: 'exponential' | 'fixed', delay }`. Para cortar los
   reintentos ante un error permanente, lanzá `UnrecoverableError`: el job va directo a failed.
3. Tope de intentos siempre. Agotados ⇒ **dead-letter** (en BullMQ, el conjunto *failed*, o
   una cola DLQ propia) con alerta. Nunca reintento infinito ni descarte silencioso.
4. La DLQ tiene dueño, runbook y herramienta de **re-drive** (reencolar tras el fix). Una DLQ
   que nadie mira es un `catch {}` distribuido.
5. *Poison message*: si un mensaje tumba al worker, el tope de intentos + DLQ lo aísla; sin
   tope bloquea la cola entera.
6. Retención: `removeOnComplete`/`removeOnFail` con un número o edad, para que Redis no crezca
   sin límite pero conserves lo suficiente para diagnosticar.
7. Timeout por mensaje menor que el tiempo de visibilidad/lock del broker; si no, otro worker
   lo toma mientras el primero sigue, y tenés procesamiento concurrente del mismo mensaje.

## 7. Sobre (envelope) y versionado

```ts
interface EventEnvelope<T> {
  id: string;            // único, generado por el productor
  type: string;          // 'appointment.confirmed' — pasado, dominio.hecho
  version: number;       // versión del esquema del payload
  occurredAt: string;    // ISO-8601 UTC
  tenantId: string;      // ver multi-tenancy
  correlationId: string; // traza de punta a punta
  causationId?: string;  // id del mensaje que lo causó
  actorId?: string;      // quién originó la acción
  payload: T;
}
```

- Cambios **compatibles**: agregar campos opcionales. Consumidores tolerantes: ignoran lo
  desconocido, no fallan por campos nuevos.
- Cambio **incompatible** (quitar/renombrar/cambiar tipo o semántica) ⇒ `version` nueva,
  publicación en paralelo de ambas hasta migrar todos los consumidores, y fecha de retiro.
- Validá el payload con esquema al **consumir** (es input externo) y al producir en tests.
- Catálogo de eventos versionado en el repo: tipo, versión, productor, consumidores, esquema.

## 8. Sagas y compensación

Un flujo que cruza transacciones (reservar turno → cobrar → notificar) no tiene rollback:
tiene **compensaciones**.

- **Coreografía** (cada paso reacciona a eventos): simple con 2–3 pasos; se vuelve ilegible
  después. **Orquestación** (un coordinador con estado persistido): preferible cuando hay
  más pasos, timeouts o decisiones.
- Cada paso define su compensación (*liberar turno*, *reembolsar*) y ambas son idempotentes.
- Ordená los pasos: primero los compensables, al final los irreversibles (enviar el email).
- El estado de la saga es una máquina de estados persistida (`state-machines-workflows`), con
  **timeout por paso**: una saga colgada es peor que una fallida.
- Una compensación puede fallar: reintento + DLQ + intervención manual documentada.

## 9. Contexto en el consumidor

No hay request: reconstruí el contexto desde el sobre — tenant (abrir contexto y fijarlo en la
transacción, `multi-tenancy`), actor y permisos ya resueltos (`authz-access-control`),
`correlationId` en logs y trazas (`backend-observability`). Un EntityManager **nuevo por
mensaje** (fork), nunca uno compartido entre mensajes.

## 10. Observabilidad de colas

Medí y alertá por: profundidad de cola, **antigüedad del mensaje más viejo** (mejor señal que
la profundidad), tasa de procesamiento y de error, duración por tipo, reintentos, tamaño de
DLQ, lag del relay del outbox. Propagá el contexto de traza en el sobre para ver productor y
consumidor en un mismo trace.

## Anti-patrones

- `emit` en memoria (event emitter del proceso) tratado como entrega garantizada: muere con el proceso.
- Publicar dentro de la transacción, o después sin outbox, en un flujo que no tolera pérdida.
- Consumidor que asume "llega una sola vez y en orden".
- Evento con la entidad completa serializada; evento usado como RPC disfrazado esperando respuesta.
- Reintentar errores de validación. DLQ sin alerta ni dueño.
- Cadena de eventos imposible de seguir sin `correlationId`.

## Checklist

- [ ] La decisión async está justificada; los invariantes inmediatos siguen siendo sincrónicos.
- [ ] Outbox en la misma transacción que el cambio; relay con `SKIP LOCKED` y alerta de lag.
- [ ] Consumidor idempotente con deduplicación transaccional por `message_id`.
- [ ] Sin dependencia de orden global; guarda de versión donde el orden importa.
- [ ] Errores clasificados; `attempts` + backoff; `UnrecoverableError` para los permanentes.
- [ ] DLQ con alerta, dueño, runbook y re-drive.
- [ ] Sobre estándar con `id`, `type`, `version`, `tenantId`, `correlationId`.
- [ ] Payload mínimo, sin datos sensibles de más, validado con esquema al consumir.
- [ ] Cambios incompatibles con versión nueva y convivencia.
- [ ] Sagas con compensaciones idempotentes, estado persistido y timeouts.
- [ ] Contexto de tenant/actor/traza reconstruido por mensaje; EM nuevo por mensaje.
- [ ] Métricas de cola, antigüedad, errores y DLQ en dashboard.
