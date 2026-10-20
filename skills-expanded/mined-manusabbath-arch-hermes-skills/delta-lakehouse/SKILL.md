---
name: delta-lakehouse
description: "Use when building an ETL or data pipeline, or storing structured and unstructured data in a Delta lakehouse for ML training or AI agent consumption. Covers extraction from heterogeneous sources, Delta tables with operation history and time travel, upsert patterns, partitioning, vacuum and compaction, using deltalake + duckdb + pyarrow."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [deltalake, duckdb, pyarrow, lakehouse, etl, data-engineering, ml, agents]
    related_skills: [empirical-project-playbook, empirical-system-invariants]
---

# Delta Lakehouse (ETL → tablas Delta → ML/agentes)

Convierte datos operativos en un activo versionado y reutilizable: un **lakehouse Delta**
resuelve el almacenado de estructurado + no estructurado, el historial de operaciones
(writes/updates), time-travel y la lectura directa por engines, modelos y agentes de IA.

**Origen:** polymarket-trading-bot (2026). Datos de predicción/mercados que hoy viven en
SQLite/JSON/logs no versionados, imposibles de reproducir para entrenar un modelo o
auditar qué estado vio un agente.

## Stack (validado end-to-end 2026)

- `deltalake` (delta-rs, Python puro) — tablas Delta con `history()`/time-travel.
- `duckdb` — SQL sobre Delta (`delta_scan`), ETL/analytics, escribe parquet.
- `pyarrow` — conversión formato ↔ Arrow; `pa.Table.from_pylist` para ingesta.
- Sin pandas para el ingesta (pyarrow basta); pandas solo si el proyecto ya lo usa.

Instalar (PEP 668 obliga venv en Debian/Ubuntu):

```bash
python3 -m venv .lhenv && .lhenv/bin/pip install deltalake duckdb pyarrow
```

Confirmar stack antes de interpretar salida:

```bash
.lhenv/bin/python -c "import deltalake,duckdb,pyarrow; print(deltalake.__version__,duckdb.__version__,pyarrow.__version__)"
```

## Flujo canónico (extract → lake → tablas delta → agentes/ML)

1. **Extract de orígenes heterogéneos** (JSONL, CSV, API/WS, DB) → normalizar a `pa.Table`.
   No estructurado (eventos JSON, payloads API, texto) viaja como columna list/struct
   (Arrow) o `VARIANT` (DuckDB) — no forzar a columnas planas.
2. **Escritura a tabla Delta** — `write_deltalake(path, arrow_table)` → version 0; cada
   escritura nueva crea OTRA versión.
3. **Historial de operaciones** — `DeltaTable(path).history()` registra `operation`
   (WRITE/OVERWRITE/...), timestamp, `operationMetrics` (rows, num_files). Es el rastro
   auditable de todo cambio.
4. **Time-travel** — `DeltaTable(path, version=N)` revierte a una versión histórica:
   reproduce el dataset exacto que entrenó un modelo o el estado que vio un agente.
5. **Consumo por ML/agentes** — DuckDB conecta a Delta en memoria (barata, sin servidor);
   la misma tabla la leen `deltalake`/`duckdb`/`polars`/Spark. Un agente consume la MISMA
   tabla que el sistema escribe — nunca una copia que drifta.

## Código validado (copia-pega)

```python
import os, pyarrow as pa, duckdb
from deltalake import write_deltalake, DeltaTable

# 1) EXTRACT no estructurado (JSONL) -> Arrow
events = [{"market": "m0", "edge_elo": None, "ts": 0},
          {"market": "m1", "edge_elo": 0.5, "ts": 1}]
arrow = pa.Table.from_pylist(events)

# 2) Escritura inicial -> tabla Delta version 0
tbl = os.path.join(base, "events")
write_deltalake(tbl, arrow)
print(DeltaTable(tbl).version())               # 0

# 3) Update (upsert) -> nueva version + historial
new = pa.Table.from_pylist([{"market": "m1", "edge_elo": 0.9, "ts": 2}])
merged = pa.concat_tables([DeltaTable(tbl).to_pyarrow_table(), new])   # read + union
seen = {}
for row in merged.to_pylist():
    seen[row["market"]] = row                   # dedup por PK, ultimo gana
write_deltalake(tbl, pa.Table.from_pylist(list(seen.values())), mode="overwrite")

print(DeltaTable(tbl).history()[0]["operation"])   # commit visible
print(DeltaTable(tbl, version=0).to_pyarrow_table().num_rows)  # time-travel

# 4) DuckDB lee Delta nativo
con = duckdb.connect()
print(con.execute(f"SELECT * FROM delta_scan('{tbl}') ORDER BY market").fetchall())
```

## Optimización de almacenado/lectura

- **Particionar por la columna de corte** (día/liga): `write_deltalake(..., partition_by=["day"])`
  → lecturas tocan solo los partfiles relevantes.
- **Tipos Arrow compactos** (int64, bool, double) desde el ingesta, evita objetos/str.
- **VACUUM + compaction** para tablas con muchas versiones: `DeltaTable.vacuum()` borra
  partfiles viejos (cuidado: NULL≠0, no vacuar en caliente lo que un agente necesita
  reproducir — fijar retención explícita).
- **Medir tamaño/costo de lectura en prod durante HORAS**, no en unit tests.

## Orígenes de extracción

- WS/API en vivo → normalizar a Arrow en el ingesta.
- SQLite/Postgres/CSV/JSONL → DuckDB (`delta_scan`/`COPY`) o pyarrow directo.
- Objetos remotos (S3/GCS/Azure): `write_deltalake`/`DeltaTable` aceptan URIs de object
  storage (credenciales vía storage_options) — no es local-only.

## Prácticas (herederas del playbook empírico)

- **Presence ≠ utility:** la tabla "anda" no basta — que una query DE PRODUCCIÓN la lea con
  valores plausibles post-deploy es la aceptación.
- **Conexión única de lectura** para agentes/analistas; nunca copias que driften.
- **Tests herméticos** para el ingesta: `tmp_path` + delta/pyarrow en disco temporal; nunca
  archivos reales del host.
- **Medir al punto de operación real:** un lake de 1K filas y uno de 1M/día son problemas
  distintos; el costo se decide midiendo, no por preferencia.
- **Contratos de datos** (ver `empirical-system-invariants`): declarar qué tabla promete qué
  columnas y el guard verifica por ciclo — el lakehouse versiona el dato, el invariant
  atestigua que se pobló.

## Cómo verificar esta skill

1. `skill_view(name='delta-lakehouse')` — linked_files muestra templates/ si las agregás.
2. Correr el código validado arriba contra `tmp_path`: debe crear tabla con version 0,
   hacer update a version >0, y DuckDB debe hacer `delta_scan` y devolver filas.
3. Agregar una plantilla `templates/ingesta-plantilla.md` por cada fuente nueva y
   referenciarla acá.

## Fuente canónica

Repo-tap `manusabbath-arch/hermes-skills` (skills/delta-lakehouse). Los perfiles locales
tienen una COPIA instalada que es la que se carga. Al editar, hacerlo en el repo, commit +
push, re-propagar. Ver README del repo tap.
