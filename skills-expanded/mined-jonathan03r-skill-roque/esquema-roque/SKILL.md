---
name: esquema-roque
description: Use when the user invokes /esquema_roque or asks to design, diagram, esquematizar, or create Postgres/Supabase database tables in Roque/Sunapp SQL style.
---

# Esquema Roque

## Purpose

Design Postgres/Supabase schemas using Roque/Sunapp conventions: domain schemas, Spanish entity names, entity-prefixed columns, `bigserial` operational IDs, audit fields, active flags, explicit indexes, checks, RLS, grants, and fixed function `search_path`.

## Trigger

Use this skill when user says:

- `/esquema_roque`
- `esquematiza mi base de datos`
- `crea diagrama entidad relacion`
- `haz SQL en mi formato`
- `usa mi arquitectura de tablas`

## Workflow

1. If inside a repo, inspect existing `db/*.sql` first with `rg`/file reads. Prefer local pattern over this generic guide.
2. Ask only if missing business-critical info. For idea-only requests, proceed with assumptions.
3. Produce one or more of:
   - Mermaid ERD for quick visual review.
   - DBML for dbdiagram.io.
   - PostgreSQL SQL draft in Roque/Sunapp style.
4. Choose the correct schema before creating any table. Do not default to `public`.
5. For concurrent jobs, always include status, attempts, availability time, worker lock fields, dedupe key, and indexes for queue pickup.
6. For Supabase tables, include RLS/grants posture. Never leave `public` tables without RLS.
7. For SQL functions, include fixed `search_path`.
8. Warn if user pasted DB credentials or secrets.

## Schema Placement

Default to domain schemas, not `public`. Pick schema by business meaning:

| Domain | Schema | Examples |
| --- | --- | --- |
| Credits, billing, balances | `creditos` | `creditos.cargos_api`, `creditos.reservas`, `creditos.consumos_detalles` |
| SIRE/libros/propuestas | `sire` | `sire.propuestas_ventas`, `sire.propuestas_compras`, `sire.paquetes` |
| SUNAT integrations/cache | `sunat` | `sunat.sesiones`, `sunat.tokens`, `sunat.diccionarios` |
| Mailbox | `buzon` | `buzon.mensajes`, `buzon.sync_jobs` |
| Notifications | `notificaciones` | `notificaciones.envios`, `notificaciones.lecturas` |
| Audit/logs | `auditoria` | `auditoria.consultas_api`, `auditoria.errores_sunat` |
| Scheduling/workers | `programacion` | `programacion.tareas`, `programacion.ejecuciones` |
| Catalog/master data | `catalogos` | `catalogos.tipo_cambio`, `catalogos.sunat_tributos` |
| Accounting domain | `contabilidad` | `contabilidad.asientos`, `contabilidad.cuentas` |

Use `public` only for objects intentionally exposed to Supabase Data API clients, usually thin views or frontend-owned tables with explicit RLS policies.

Schema setup pattern:

```sql
create schema if not exists <schema>;
revoke all on schema <schema> from anon, authenticated;
grant usage on schema <schema> to service_role;
```

If frontend must read a domain schema directly, grant minimally and add policies:

```sql
grant usage on schema catalogos to authenticated;
grant select on catalogos.<tabla> to authenticated;
alter table catalogos.<tabla> enable row level security;
create policy "<tabla>_select_authenticated"
  on catalogos.<tabla>
  for select
  to authenticated
  using (activo = true);
```

Alternative: expose a controlled `public` view instead of granting table access:

```sql
create or replace view public.<vista>
with (security_invoker = true)
as
select ...
from catalogos.<tabla>
where activo = true;
```

Decision rule:

- Frontend reads/writes directly: `public` table/view + RLS + minimal grants.
- Backend/service only: domain schema + `revoke all from anon, authenticated` + `grant usage to service_role`.
- Sensitive RPC: domain schema + `security definer` only if needed + fixed `search_path` + execute only to `service_role`.

## Roque SQL Style

Default backend-owned table shape:

```sql
create table if not exists <schema>.<tabla_plural> (
  <entidad_singular>_id bigserial primary key,
  usuario_uuid uuid references auth.users(id) on delete cascade,

  <entidad_singular>_estado text not null default 'ACTIVO',
  <entidad_singular>_metadata jsonb not null default '{}'::jsonb,

  creado_por uuid,
  actualizado_por uuid,
  fecha_creacion timestamptz not null default now(),
  fecha_actualizacion timestamptz not null default now(),
  activo boolean not null default true
);

alter table <schema>.<tabla_plural> enable row level security;
revoke all on table <schema>.<tabla_plural> from anon, authenticated;
grant select, insert, update, delete on table <schema>.<tabla_plural> to service_role;
```

Naming rules:

- Schemas: Spanish/domain singular or plural by business clarity: `creditos`, `sire`, `buzon`, `auditoria`, `contabilidad`.
- Tables: Spanish plural, snake_case: `programaciones`, `programacion_ventanas`, `programacion_ejecuciones`.
- Primary key: singular table/entity prefix + `_id`: `programacion_id`.
- Columns: prefix with singular entity where useful: `programacion_estado`, `programacion_nombre`.
- User owner: `usuario_uuid uuid references auth.users(id)`.
- Audit: prefer `creado_por`, `actualizado_por`, `fecha_creacion`, `fecha_actualizacion`, `activo`.
- Index names: `idx_<tabla>_<campos>`.
- Unique indexes: `uq_<tabla>_<campos>`.
- Check constraints: `<tabla>_<campo>_check`.

Catalog rules:

- Use catalog tables for extensible types: channels, statuses, providers, categories.
- Operational tables must reference catalog primary keys (`bigint`/`bigserial`), not compare by text code.
- Catalog `codigo` can exist for seed/admin lookup, but app inserts/updates should pass `<catalogo>_id`.
- Avoid examples that depend on `where <catalogo>_codigo = 'EMAIL'` unless explicitly showing seed/backoffice lookup.

Catalog shape:

```sql
create table if not exists catalogos.<catalogo_plural> (
  <catalogo_singular>_id bigserial primary key,
  <catalogo_singular>_codigo text not null unique,
  <catalogo_singular>_nombre text not null,
  <catalogo_singular>_descripcion text,
  creado_por bigint,
  actualizado_por bigint,
  fecha_creacion timestamptz not null default now(),
  fecha_actualizacion timestamptz not null default now(),
  activo boolean not null default true
);

alter table catalogos.<catalogo_plural> enable row level security;
```

Operational FK shape:

```sql
<catalogo_singular>_id bigint not null
  references catalogos.<catalogo_plural>(<catalogo_singular>_id)
```

## Functions and RPC

All functions must fix `search_path`. For sensitive writes, prefer a domain schema and grant only `service_role`.

```sql
create or replace function creditos.<funcion>(...)
returns jsonb
language plpgsql
security definer
set search_path = creditos, public, pg_temp
as $$
begin
  ...
end;
$$;

revoke execute on function creditos.<funcion>(...) from public, anon, authenticated;
grant execute on function creditos.<funcion>(...) to service_role;
```

For non-sensitive SQL helpers:

```sql
create or replace function sire.<funcion>(...)
returns table (...)
language sql
stable
set search_path = sire, public, pg_temp
as $$
  ...
$$;
```

Never create mutable-search-path functions.

## Concurrency Pattern

For queued execution tables:

```sql
<entidad>_estado text not null default 'PENDIENTE',
<entidad>_clave text not null,
<entidad>_prioridad integer not null default 100,
<entidad>_intentos integer not null default 0,
<entidad>_max_intentos integer not null default 4,
<entidad>_disponible_en timestamptz not null default now(),
<entidad>_bloqueado_por text,
<entidad>_bloqueado_en timestamptz,
<entidad>_iniciado_en timestamptz,
<entidad>_finalizado_en timestamptz,
<entidad>_ultimo_error text
```

Queue pickup index:

```sql
create index if not exists idx_<tabla>_estado_prioridad
  on <schema>.<tabla> (
    <entidad>_estado,
    <entidad>_prioridad,
    <entidad>_disponible_en,
    fecha_creacion
  )
  where activo = true;
```

Deduplication:

```sql
create unique index if not exists uq_<tabla>_<dedupe>
  on <schema>.<tabla> (<owner>, <clave>);
```

Worker code should claim rows with `for update skip locked`, not app-only locking.

## Output Format

Keep response practical:

1. Short architecture summary.
2. Mermaid ERD or DBML when user asks to visualize.
3. SQL draft only if user asks for code.
4. Notes: indexes, constraints, RLS, concurrency risks.

If user asks "ideas nada mas", avoid full SQL unless helpful.
