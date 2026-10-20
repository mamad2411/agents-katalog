---
name: data-medallion-architecture
description: "Use when designing an end-to-end data architecture: choosing a source (API, database, SFTP), building a medallion bronze-silver-gold lakehouse pipeline, and turning it into hypothetical-scenario dashboards and AI/ML/MCP consumption. Covers source-selection tradeoffs and layer design patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [medallion, architecture, bronze-silver-gold, lakehouse, delta, duckdb, dashboard, scenarios, data-engineering]
    related_skills: [delta-lakehouse, empirical-project-playbook]
---

# Data Medallion Architecture (fuente → bronze → silver → gold → consumo)

Diseño punta a punta para un pipeline de datos: elegir la FUENTE, armar la arquitectura
**medallion** (Bronze/Silver/Gold), y alimentar consumo (AI, ML, MCP, dashboards). El
objetivo es que cada capa tenga un rol único y auditable — no una pila de pipelines
ad-hoc.

**Origen:** extensión del stack `delta-lakehouse` (2026). El lakehouse resuelve el
almacenado; esta skill resuelve el DISEÑO: qué va en cada capa, cómo elegir fuente, y cómo
llegar de una fuente cruda a un dashboard de escenarios hipotéticos.

## Stack (validado end-to-end sobre deltalake 1.6 + duckdb 1.5 + pyarrow)

`deltalake` (tablas Delta + history/time-travel) · `duckdb` (SQL `delta_scan`) ·
`pyarrow` (ingesta a `pa.Table`). Instalar en venv (PEP 668): `pip install deltalake duckdb pyarrow`.

## La capa medallion — roles (cada capa SÓLO hace lo suyo)

```
FUENTE → BRONZE → SILVER → GOLD → CONSUMO
(API/DB/SFTP)  (raw)   (clean)  (agregado)
```

**BRONZE (raw, append-only, fuente de verdad):**
- Ingestiona el dato TAL COMO llega (JSON, CSV, XML). NO se limpia, NO se dedupe.
- Append-only: una fila = un evento recibido; el historial es inmutable.
- Es la capa de auditoría / re-procesamiento: si silver/gold se rompen, se re-deduce desde
  bronze.

**SILVER (limpia, dedup, tipos, NULL gestionado):**
- Dedup por PK, coerce tipos (string → float/int), filtra/rellena.
- NULL se DECLARA: malo→sentinel documentado (ej. 0.0), borde→conservado como NULL. NUNCA
  silencio. Regla NULL≠0 del playbook: NULL=defecto a corregir, 0=medido legítimo.
- Es lo que consumen los análisis por defecto (gold se materializa desde acá).

**GOLD (agregada, pregunta de negocio, dashboard-ready):**
- Agrega a la dimensión de corte (market/día/liga). Es la capa que responde la pregunta.
- Se materializa como tabla Delta (para consumo) o como query DuckDB (para dashboards en
  vivo).

**CONSUMO (AI / ML / MCP / análisis):**
- La misma tabla que consume un modelo, agente o dashboard es la que el sistema escribe —
  nunca una copia que drifte (mismo principio que MCP-fuente-única).
- DuckDB conecta en memoria (barata, sin servidor) a silver/gold.

## Código validado (medallion completo, copia-pega)

```python
import os, pyarrow as pa, duckdb
from deltalake import write_deltalake, DeltaTable

# BRONZE: raw append-only
raw_events = pa.Table.from_pylist([{"market":"m0","price":"0.55","edge_raw":0.12,"ts":10}])
write_deltalake(bronze, raw_events)          # append-only (mode default create)

# SILVER: dedup PK + coerce tipo + NULL gestionado
cleaned = []  # dedup por (market, ts); float(price) en try/except -> sentinel 0.0 si malo
write_deltalake(silver, pa.Table.from_pylist(cleaned))

# GOLD: agregada materializada / query
con = duckdb.connect()
print(con.execute(f"SELECT market, MAX(price) last_price FROM delta_scan('{silver}') GROUP BY market").fetchall())
```

## Elegir la FUENTE (decisión, no reflejo)

Antes de construir: comparar orígenes (API/DB/SFTP) con criterios explícitos y números, no
preferencia:
- **Confiabilidad / freshness:** ¿la API falla en silencio devolviendo datos cacheados?
  (proveedor externo que falla en silencio es peor que local lento pero honesto).
- **Latencia, cuota, costo, disponibilidad.**
- **Formato:** estructurado (DB/CSV) vs no estructurado (JSONL/payloads). Ambos entran — el
  no estructurado viaja como columna list/struct/variante, no forzado a plano.
- Registrar la decisión en `empirical-project-playbook/templates/infra-decision.md`
  (mismo espíritu que el playbook:
  criterio antes de ver los datos).

## De una fuente a escenarios hipotéticos → dashboard

Flujo para llegar de la arquitectura al dashboard:

1. **Fijar la pregunta de negocio GOLD ANTES de construir** (ej. "¿qué mercados con edge
   >x sobreviven el fill?"). La capa GOLD responde esto.
2. **Definir escenarios hipotéticos** = variaciones de la agregación/segmentación sobre
   GOLD (ej. cambiar el umbral de edge, el horizonte, el parámetro de riesgo). No son
   queries sueltas: son la MISMA pregunta con parámetros.
3. **Materializar/consultar** con DuckDB + `delta_scan` sobre GOLD, con la query parametrizada
   por el escenario.
4. **Ponerlo en el dashboard** — un dashboard es la vista agendada de los escenarios sobre
   GOLD. La query/valor que usa el dashboard debe ser la MISMA del GOLD, nunca una copia.
5. **Medir al punto de operación real:** el dashboard muestra números sobre el tamaño real
   de datos que produce el sistema, no un sample de juguete.

## Prácticas (heredadas)

- **Presence ≠ utility:** una capa "anda" no basta — que una query de PRODUCCIÓN sobre GOLD
  responda la pregunta con valores plausibles post-deploy es la aceptación.
- **Contratos de datos** por capa (ver `empirical-system-invariants`): declarar qué columna
  promete cada capa y el guard verifica. Bronze es append-only y su contrato es "recibí el
  evento"; silver "dedup + tipo"; gold "responde la pregunta".
- **Tests herméticos** para transformaciones: `tmp_path` + delta; nunca archivos reales.
- **Un escalar donde el dominio tiene N entidades** (dict keyed por posición) es un smell —
  el medallion es una jerarquía de capas, no un solo dict.

## Plantillas

- `templates/scenario-dashboard.md` — cómo pasar de GOLD a escenarios hipotéticos → dashboard
  (parametrización de la query, cómo presentar).

## Cómo verificar esta skill

1. `skill_view(name='data-medallion-architecture')` — linked_files muestra templates/.
2. Correr el código validado: bronze append-only, silver dedup, gold agregada; DuckDB lee
   silver y responde la pregunta.
3. Rellenar `templates/scenario-dashboard.md` con un escenario real del proyecto y referenciarlo acá.

## Fuente canónica

Repo-tap `manusabbath-arch/hermes-skills` (skills/data-medallion-architecture). Los perfiles
locales tienen una COPIA instalada que es la que se carga. Al editar, hacerlo en el repo,
commit + push, re-propagar. Ver README del repo tap.
