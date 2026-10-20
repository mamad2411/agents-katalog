---
name: concurrency-and-locking
description: Control de concurrencia en escrituras — locking optimista con versión de fila (409/412) vs pesimista (`FOR UPDATE`, `SKIP LOCKED`), advisory locks, claves de idempotencia, reintento solo ante errores reintentables, doble submit y las carreras típicas (doble reserva de turno, doble asiento contable, contadores). Usar al diseñar o revisar una mutación que lee-y-luego-escribe, un endpoint que el cliente reintenta, un worker de cola, un contador, o ante datos duplicados o pisados de forma intermitente.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Concurrencia y locking

Toda secuencia **leer → decidir → escribir** es una carrera hasta que se demuestre lo
contrario. Con más de una instancia de la API, un mutex en memoria no protege nada: la
coordinación vive en la **base**. Mecánica de Postgres en `postgresql-advanced`; API del
ORM: el que fije el `CLAUDE.md` del repo; cómo probarlo, `integrity-testing`.

## 1. Primero: ¿puede la base garantizarlo sola?

Antes de elegir un lock, intentá que la invariante sea una **constraint** o una
**sentencia atómica**. Es más simple y no se puede saltear.

| Invariante | Mecanismo |
|---|---|
| No duplicar (un like por usuario, un asiento por operación) | `UNIQUE` + manejar `23505` |
| No solapar rangos (turnos, bloqueos de agenda) | `EXCLUDE USING gist` + manejar `23P01` |
| Contador | `UPDATE ... SET n = n + 1` (atómico), nunca leer-sumar-escribir |
| Transición de estado | `UPDATE ... WHERE id = $1 AND status = $esperado` y mirar filas afectadas |
| Saldo/stock no negativo | `CHECK (balance >= 0)` + `UPDATE` atómico |

```typescript
// ❌ lost update: dos requests leen 41 y ambos escriben 42
post.likes = post.likes + 1;

// ✅ atómico en la base; la fila de like con UNIQUE(post_id, user_id) evita el doble like
await em.nativeUpdate(Post, { id }, { likes: raw('likes + 1') }); // verificar API en la doc del ORM
```

## 2. Optimista vs pesimista

| | Optimista (versión de fila) | Pesimista (`FOR UPDATE`) |
|---|---|---|
| Cuándo | Conflictos raros; ediciones de usuario que duran minutos (formularios, ficha clínica) | Conflictos frecuentes sobre la misma fila; sección crítica corta dentro de una transacción |
| Costo | El perdedor rehace su trabajo | Los demás esperan; riesgo de deadlock |
| Cruza requests | Sí: la versión viaja al cliente y vuelve | No: el lock muere con la transacción |
| Falla como | `OptimisticLockError` → 409/412 | espera, `lock_timeout` (`55P03`) o deadlock (`40P01`) |

**Optimista, de punta a punta**: el `GET` devuelve `version` (o `ETag`); la mutación la
exige (`If-Match` o campo en el body); el `UPDATE` lleva `WHERE version = $leída`. Si el
servidor recarga la entidad y compara contra lo que **él** acaba de leer, no protege la
edición del usuario. Sin versión en la mutación → **428**; versión vieja → **412** (con
`If-Match`) o **409** (en el body). Elegí una convención por API y documentala
(ver `error-handling-contract`).

**Pesimista**: siempre dentro de una transacción corta, sin I/O externo adentro.

- `FOR UPDATE`: bloquea la fila hasta el commit. Bloqueá la **fila padre** que serializa
  el recurso (la agenda del profesional, la cuenta contable), no cada hijo.
- `FOR UPDATE NOWAIT`: falla ya si está tomada — para acciones de usuario donde esperar
  no tiene sentido.
- `FOR UPDATE SKIP LOCKED`: saltea filas tomadas — **solo** para colas de trabajo, donde
  cualquier fila libre sirve. Nunca para lógica de negocio: ignora datos que existen.
- Orden de locks fijo (ids ascendentes) para no generar deadlocks.

```sql
-- worker de cola: N workers concurrentes sin pisarse
UPDATE job SET status = 'running', locked_at = now()
WHERE id = (SELECT id FROM job WHERE status = 'pending'
            ORDER BY run_at FOR UPDATE SKIP LOCKED LIMIT 1)
RETURNING *;
```

## 3. Advisory locks

Lock por **clave arbitraria**, para serializar algo que no es una fila (o todavía no
existe): "generar el próximo número de comprobante del tenant", "un solo cierre contable
a la vez", "un cron que no debe correr duplicado".

- Preferí `pg_advisory_xact_lock(key)` (se libera solo al terminar la transacción) a la
  variante de sesión, que se filtra con pools en modo transacción.
- `pg_try_advisory_xact_lock(key)` para "si ya hay otro, salgo".
- La clave es un `bigint` (o dos `int`): derivala de forma determinista y documentada
  (namespace + hash del recurso). Colisión de claves = serialización innecesaria, no corrupción.
- No reemplaza una constraint: protege solo a quien se acuerda de pedirlo.

## 4. Idempotencia: el cliente va a reintentar

Timeout del lado del cliente ≠ la operación no ocurrió. Todo `POST` con efecto (crear
cita, registrar pago, emitir asiento, enviar solicitud) acepta `Idempotency-Key`.

1. Tabla `idempotency_key(tenant_id, key, request_hash, status, response, expires_at)`
   con `UNIQUE(tenant_id, key)`.
2. `INSERT` de la clave **en la misma transacción** que el efecto. Si choca con `23505`:
   misma `request_hash` → devolvé la respuesta guardada; hash distinto → **422** (clave
   reutilizada con otro payload); todavía en curso → **409**.
3. La clave la genera el cliente por **intención de usuario** (un UUID por apertura del
   formulario), no por request HTTP.
4. Expiración explícita. La key no sustituye la `UNIQUE` de negocio: son dos redes.

**Doble submit en UI**: deshabilitar el botón es UX (ver `frontend-ux-states`), no
protección. La protección es la key + la constraint.

**Consumers de cola**: entrega *at-least-once* → el handler deduplica por id de mensaje
en una tabla con `UNIQUE`, en la misma transacción que el efecto. Ver `async-messaging-events`.

## 5. Reintentos

| Error | ¿Reintentar? |
|---|---|
| `40001` serialization_failure, `40P01` deadlock | Sí: **la transacción entera**, backoff + jitter, tope (3–5) |
| Timeout de red hacia un tercero | Solo si la operación es idempotente o lleva key |
| `OptimisticLockError` / 409 / 412 | **No** automático: el usuario debe ver el dato nuevo y decidir |
| `23505`, `23P01`, `23514`, `23503` | No: es un resultado de negocio |
| `55P03` lock_not_available | Depende: en DDL sí; en acción de usuario, informar "ocupado" |

- El reintento vuelve a **leer**: jamás reuses entidades cargadas en el intento fallido
  (contexto de ORM nuevo por intento).
- Reintentar a ciegas un conflicto optimista es exactamente el lost update que el lock evitaba.

## 6. Carreras típicas de la casa

- **Doble reserva de turno**: dos pacientes toman el mismo hueco. → `EXCLUDE` sobre
  `(doctor_id, rango)`; el perdedor recibe 409 con código estable y la UI recarga huecos.
  Un `SELECT` de disponibilidad previo es solo cortesía.
- **Bloqueo de agenda vs cita existente**: el bloqueo y la cita se crean a la vez. →
  misma constraint de exclusión cubriendo ambos tipos, o lock de la fila de agenda.
- **Doble asiento contable**: reintento del cliente o del job. → idempotency key +
  `UNIQUE(tenant_id, source_type, source_id)` en el asiento. Los asientos no se editan:
  se revierten (ver `accounting-double-entry`).
- **Numeración correlativa sin huecos**: `SEQUENCE` deja huecos. → fila contador por
  tenant con `FOR UPDATE`, o advisory lock transaccional.
- **Contadores (likes, comentarios)**: `UPDATE n = n + 1` + fila única por actor; o
  recalcular desde la tabla de hechos y tratar el contador como caché.
- **Transición doble** (dos operadores aprueban/rechazan a la vez): `UPDATE ... WHERE
  status = $esperado`; 0 filas = perdió (ver `state-machines-workflows`).
- **Check-then-insert** ("si no existe, crear"): `INSERT ... ON CONFLICT DO NOTHING/UPDATE`.

## 7. Cómo se prueba

- Un test unitario con mocks **no puede** probar concurrencia. Hace falta PostgreSQL real.
- Patrón: lanzar N operaciones con `Promise.all`, cada una con **su propia conexión/
  contexto**, y afirmar el estado final: exactamente 1 éxito, N−1 conflictos con el código
  esperado, y el invariante intacto en la base (`count(*)`, suma, sin solapes).
- Para ventanas chicas, forzá el intercalado: transacción A toma el lock y espera una
  señal; B intenta; se afirma que B espera o falla; A confirma.
- Corré el test varias veces: uno que pasa 1 de cada 20 es un bug de concurrencia, no un
  flaky (ver `e2e-failure-triage`).

## Anti-patrones

- `SELECT` de verificación + `INSERT` sin constraint ("igual chequeamos antes").
- Mutex/flag en memoria del proceso en un servicio con más de una instancia.
- Versión que no viaja al cliente; `If-Match` opcional.
- `SKIP LOCKED` en lógica de negocio; transacción con `FOR UPDATE` que llama a un tercero.
- Reintento genérico de "cualquier error de base".
- Deshabilitar el botón como única defensa contra el doble submit.

## Checklist

- [ ] Cada leer→decidir→escribir identificado y resuelto con constraint, sentencia atómica o lock.
- [ ] Invariantes de unicidad/no-solape en la base, con su SQLSTATE mapeado a un error estable.
- [ ] Recursos editables por usuarios con versión de punta a punta (428 sin versión, 409/412 vieja).
- [ ] Locks pesimistas en transacción corta, orden fijo, sin I/O externo.
- [ ] `POST` con efecto aceptan `Idempotency-Key`; clave y efecto en la misma transacción.
- [ ] Consumers deduplican por id de mensaje.
- [ ] Solo `40001`/`40P01` se reintentan automáticamente, con contexto de ORM nuevo y tope.
- [ ] Test de concurrencia contra PostgreSQL real, con N paralelos y aserción del invariante.
