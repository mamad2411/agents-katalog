---
name: mikroorm-patterns
description: Persistencia con MikroORM sobre PostgreSQL — Unit of Work e identity map, un EntityManager por request o job, `em.transactional`, flush explícito, locking optimista con propiedad de versión y `OptimisticLockError`, populate sin N+1, referencias vs entidades cargadas, filtros de tenant y soft delete, esquema gestionado fuera del ORM. Usar al escribir o revisar un repositorio, caso de uso transaccional, entidad, job o test que toque el EntityManager, o ante datos viejos, flushes inesperados o errores de contexto global.
---

# MikroORM — patrones de la casa

MikroORM es Data Mapper + **Unit of Work** + **Identity Map**. Casi todos los bugs
vienen de tratarlo como Active Record. Para NestJS ver `nestjs-development`; para
bloqueos y carreras, `concurrency-and-locking`; para SQL fino, `postgresql-advanced`.
APIs verificadas contra mikro-orm.io; ante duda de versión, verificá en la doc oficial.

## 1. Modelo mental

- El `EntityManager` (EM) rastrea entidades **gestionadas** y, en `flush()`, calcula el
  diff contra la copia original y emite los `INSERT/UPDATE/DELETE` en una transacción.
- Identity map: dentro de un EM, la misma fila es **la misma instancia**. Dos `findOne`
  del mismo id no hacen dos lecturas frescas: el segundo devuelve lo que ya tenés.
- `em.persist(e)` solo marca; `em.flush()` escribe. Una entidad ya gestionada (vino de
  un `find`) no necesita `persist` para que sus cambios se guarden en el próximo flush.
- Consecuencia: un EM **no es thread-safe ni compartible entre requests**.

## 2. Un EM por contexto

| Contexto | Cómo se obtiene el EM |
|---|---|
| Request HTTP | contexto por request (`RequestContext` / integración de Nest) |
| Job, cron, consumer de cola, script | `@CreateRequestContext()` en el método, o `orm.em.fork()` |
| Test | `orm.em.fork()` por caso |

```typescript
// ❌ EM global compartido: identity map contaminado entre requests y fuga de memoria
const user = await orm.em.findOne(User, id);

// ✅ fork: identity map limpio, aislado
const em = orm.em.fork();
const user = await em.findOneOrFail(User, id);
```

- El ORM valida por defecto el uso del EM global sin contexto y lanza error: no
  desactives esa validación para "arreglarlo"; creá el contexto.
- Un fork nace con identity map vacío. Si necesitás releer una fila dentro del mismo EM,
  usá `em.refresh(entity)` o un fork nuevo; no esperes que `findOne` vaya a la base.

## 3. Transacciones

```typescript
await em.transactional(async (tx) => {
  const appt = await tx.findOneOrFail(Appointment, id, { populate: ['slot'] });
  appt.confirm(actor);          // la regla vive en la entidad/dominio
  tx.persist(new AppointmentEvent(appt, 'confirmed', actor));
}); // flush + commit automáticos; cualquier throw hace rollback
```

- `em.transactional()` crea un contexto interno (fork) que **hereda** el identity map del
  externo (`clear: false` por defecto) y hace flush antes del commit.
- Usá **el EM que te pasa el callback** (`tx`), o un EM que respete el contexto. Mezclar
  otro EM ajeno adentro saca esas escrituras de la transacción.
- Nivel de aislamiento por transacción: opción `isolationLevel`
  (`IsolationLevel.SERIALIZABLE`, etc.). El decorador `@Transactional()` envuelve el
  método con la misma semántica y propagación `REQUIRED` por defecto.
- **Nada externo adentro**: ni HTTP, ni email, ni publicar a una cola. Los efectos van
  después del commit (outbox — ver `async-messaging-events`).
- Una transacción = un caso de uso. No abras transacciones en repositorios.

## 4. Flush explícito

- Modos: `FlushMode.AUTO` (default: flushea antes de una query solo si hace falta),
  `COMMIT` (demora hasta el commit), `ALWAYS` (antes de cada query).
- Regla de la casa: **el caso de uso decide cuándo se escribe**. Un flush al final de la
  unidad de trabajo, no `flush()` salpicado después de cada cambio. Varios flush en un
  mismo caso de uso fuera de una transacción = varias transacciones = atomicidad rota.
- En `AUTO`, los cambios sobre entidades gestionadas no disparan auto-flush por sí solos;
  si dependés de leer lo que acabás de cambiar vía query, hacé flush explícito.
- Para lotes grandes: flush cada N y `em.clear()` para que el identity map no crezca sin
  techo.

## 5. Locking optimista

```typescript
@Property({ version: true })
version!: number; // entero preferido a timestamp
```

- En cada `UPDATE` el ORM agrega `WHERE version = ?` e incrementa. Si otra transacción
  ganó, lanza **`OptimisticLockError`**.
- El flujo es de **punta a punta**: el cliente recibe `version`, la devuelve en la
  mutación, y el servidor la verifica al cargar:

```typescript
const rec = await em.findOneOrFail(ClinicalNote, id, {
  lockMode: LockMode.OPTIMISTIC,
  lockVersion: dto.version,     // versión que el cliente leyó
});
```

- ❌ Cargar, asignar y flushear **sin** `lockVersion`: solo protege la ventana de
  milisegundos del request, no la edición del usuario (lost update entre dos pestañas).
- `OptimisticLockError` se traduce en un único lugar a **409/412** con código estable
  (ver `error-handling-contract`). **No se reintenta a ciegas**: reintentar es pisar al otro.
- Pesimista (requiere transacción abierta): `lockMode: LockMode.PESSIMISTIC_WRITE`
  (`for update`), `PESSIMISTIC_PARTIAL_WRITE` (`for update skip locked`),
  `PESSIMISTIC_WRITE_OR_FAIL` (`for update nowait`), y las variantes `_READ` (`for share`).
  También vía `em.lock()` o `qb.setLockMode()`.

## 6. Relaciones: referencias, populate y N+1

- Una relación no populada es una **referencia**: solo tiene la PK. Con `{ ref: true }`
  se tipa `Ref<T>` y el compilador impide leer propiedades no cargadas; tras
  `populate`, accedés con `.$`.
- Para setear una FK sin leer la fila: `em.getReference(Doctor, doctorId)`. No hagas un
  `findOne` solo para asignar una relación.
- N+1 típico: iterar una lista y tocar una relación lazy. Declará `populate` en la query.

```typescript
// ❌ 1 + N
const appts = await em.find(Appointment, { day });
for (const a of appts) names.push((await a.patient.load())!.fullName);

// ✅ populate declarado; estrategia explícita si el join explota filas
const appts = await em.find(Appointment, { day }, {
  populate: ['patient', 'slot.doctor'],
  strategy: LoadStrategy.SELECT_IN,
});
```

- Estrategias: `JOINED` (un query con joins), `SELECT_IN` (un query por relación),
  `BALANCED` (join en to-one, select-in en to-many). Con varias colecciones to-many,
  `JOINED` multiplica filas: medí con el log de queries.
- Proyectá con `fields` en listados; no traigas columnas pesadas (texto clínico, blobs)
  para pintar una tabla.
- `em.populate(entities, [...])` para entidades ya cargadas.

## 7. `em.find` vs QueryBuilder vs SQL

| Necesidad | Herramienta |
|---|---|
| CRUD, filtros, populate, paginación por cursor | `em.find` / `findByCursor` |
| Agregados, joins con condición, subqueries, `setLockMode` | `em.createQueryBuilder` |
| Reportes, CTEs, funciones de ventana, `pg_trgm` | SQL parametrizado, en un repositorio |

- Nunca interpoles input en SQL: parámetros siempre (ver `security-guardrails`).
- Lo que devuelve SQL crudo **no** está gestionado: no esperes que un cambio se flushee.

## 8. Filtros: tenant y soft delete

```typescript
@Filter({ name: 'tenant', cond: (args) => ({ tenant: args.tenantId }), default: true })
@Filter({ name: 'notDeleted', cond: { deletedAt: null }, default: true })
```

- Los parámetros se fijan una vez por contexto: `em.setFilterParams('tenant', { tenantId })`
  en el interceptor/middleware que resuelve el tenant. Globales: `em.addFilter(...)`.
- Apagar un filtro es una decisión explícita y auditada: `{ filters: { tenant: false } }`
  solo en código marcado como agnóstico de tenant. Ver `multi-tenancy`.
- Los filtros **no** aplican a SQL crudo ni a todo QueryBuilder manual: ahí el `tenant_id`
  va a mano, y RLS es la red de abajo (ver `postgresql-advanced`).

## 9. Esquema fuera del ORM

- En entornos reales el ORM **no** crea ni altera tablas: schema sync apagado. La fuente
  de verdad del esquema es el modelo (ver `model-driven-schema`); las entidades lo
  **reflejan**.
- Nombres de tabla/columna explícitos en la entidad cuando difieren de la convención; no
  renombres en el ORM algo que el modelo llama distinto.
- Verificá la fidelidad entidad ↔ base al arrancar o en CI (columna ausente, nulabilidad
  divergente). Un mapeo que compila no prueba que la columna exista.

## 10. Testing

- Unitario con EM mockeado: prueba **la regla**, no la persistencia. No demuestra que la
  query funcione, ni las constraints, ni el locking.
- Todo lo que dependa de SQL real (filtros, populate, versión, exclusion constraints,
  transacciones) se prueba contra PostgreSQL real (ver `integrity-testing`).
- ESM: corré los tests por el script del proyecto (ver `typescript-standards` §7).

## Anti-patrones

- EM global en un job o consumer; desactivar la validación de contexto global.
- `flush()` después de cada línea; transacciones dentro de repositorios.
- Optimista sin `lockVersion` del cliente; reintentar un `OptimisticLockError`.
- `findOne` solo para asignar una FK; lazy loading dentro de un loop.
- `filters: false` para "que ande"; SQL crudo sin `tenant_id`.
- Schema sync encendido contra una base compartida.

## Checklist

- [ ] Cada request/job/test tiene su propio contexto de EM (fork o `@CreateRequestContext`).
- [ ] Un caso de uso = una `em.transactional`; sin I/O externo adentro.
- [ ] Un flush por unidad de trabajo; lotes con flush + `clear` periódico.
- [ ] Entidades editables por usuarios con `@Property({ version: true })` y `lockVersion` verificado.
- [ ] `OptimisticLockError` mapeado a 409/412 en un solo lugar, sin reintento ciego.
- [ ] `populate` declarado; sin relaciones lazy en loops; `fields` en listados.
- [ ] Filtros de tenant/soft delete activos por defecto; cada desactivación justificada.
- [ ] SQL crudo parametrizado y con `tenant_id` explícito.
- [ ] Schema sync apagado; fidelidad entidad ↔ base verificada.
- [ ] Lo que depende de SQL real tiene test contra PostgreSQL real.
