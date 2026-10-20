---
tags: [backend, version, specific, sql, map, selection]
name: version-specific-sql-map-selection
description: Select MyBatis-style SQL maps at runtime by DBMS + version with graceful fallback to a default supported version
category: backend
version: 1.0.0
trigger: multi-version RDBMS query routing, versioned SQL XML maps, per-DBMS query dispatch
source_project: lucida-domain-dpm
---

# Version-specific SQL map selection

When monitoring or querying many RDBMS products across many versions (Oracle 9i–23c, MySQL 5.7–9.6, MariaDB 10.6–12.2, PostgreSQL 9.6–18, MSSQL 2012–2022, Tibero 4–6, CUBRID 9.1–11.3), maintain one SQL map XML per `(DBMS, majorVersion)` tuple and resolve the correct map at runtime.

## Shape
- File naming: `sql_map_<DBMS>_<VERSION>.xml` in a single resources folder.
- Registry: boot-time scan loads every matching file into `Map<(dbms,version), Map<queryId, sql>>`.
- Lookup: `getQuery(dbms, rawVersion, queryId)` runs `rawVersion` through a per-DBMS version normalizer, then falls back to a known-good default when the normalizer rejects it.
- Fallback rationale: unknown target version is better served by the closest supported version than a hard failure — collection keeps running.

## Steps
1. Define a `DbmsVersionResolver` interface: `String resolve(String rawVersion)`; one impl per DBMS.
2. In each impl, map raw version strings to the nearest supported bucket (e.g. `10.x, 11.x, 12.x` → `12c`; unknown → documented default).
3. Register impls in a `Map<Dbms, DbmsVersionResolver>`.
4. At startup, glob `sql_map_*.xml` and parse `(dbms, version)` from the filename; store in a two-level map.
5. Expose `QueryTextMapper.get(dbms, rawVersion, queryId)` that resolves version, looks up, and throws only when the query id is missing for every known version of that DBMS.
6. Log the resolved `(dbms→version)` once per target on first use so operators can see which bucket a target was routed to.
