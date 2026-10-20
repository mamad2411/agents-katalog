---
name: supabase-segurodata
description: Schema y configuración de Supabase para SeguroData — tablas, RLS, pgvector (HNSW), PostGIS, hook de claims JWT y Realtime. Proyecto `segurodata` (ref pluxaelenhkdaakxdrpm).
---

# Supabase SeguroData — Schema del Proyecto

Referencia completa del schema. Proyecto: `segurodata` (ref `pluxaelenhkdaakxdrpm`, us-east-1). Las migraciones canónicas viven en `supabase/migrations/*.sql` — este documento es el resumen de referencia; ante discrepancia, mandan las migraciones.

## Extensiones requeridas

```sql
CREATE EXTENSION IF NOT EXISTS postgis;    -- geometrías UPZ y cuadrantes
CREATE EXTENSION IF NOT EXISTS vector;     -- pgvector para embeddings GraphRAG
```

## Tablas del sistema

### `silver_upz_mes` — datos del pipeline (cargada desde Silver parquet)
Las 20 columnas de `datos/procesados/silver_upz_mes.parquet` (upz_cod, anio, mes, tipo_crimen, es_crimen, lags, clima, estrato, cuadrantes, TM, F11/F13/F14...). Índice compuesto `(upz_cod, anio, mes)`. Carga bulk con psycopg COPY (`scripts/seed_supabase.py`).

### `predicciones` — niveles de riesgo pre-computados (servidos por POST /predict)
```sql
CREATE TABLE IF NOT EXISTS predicciones (
  upz_cod      varchar NOT NULL,
  anio         int NOT NULL,
  mes          int NOT NULL,
  nivel_riesgo varchar NOT NULL CHECK (nivel_riesgo IN ('CRITICO','ALTO','MEDIO','BAJO')),
  prob_critico float, prob_alto float, prob_medio float, prob_bajo float,
  origen       varchar NOT NULL DEFAULT 'seed_dev',   -- 'seed_dev' | 'notebook_04'
  PRIMARY KEY (upz_cod, anio, mes)
);
```
La columna `origen` permite el switch limpio: `scripts/load_model_artifacts.py` borra `origen='seed_dev'` e inserta lo real de Notebook 04.

### `shap_values` — SHAP pre-computados (formato long, servidos por GET /explain)
```sql
CREATE TABLE IF NOT EXISTS shap_values (
  upz_cod  varchar NOT NULL,
  anio     int NOT NULL,
  mes      int NOT NULL,
  feature  varchar NOT NULL,
  valor    float NOT NULL,
  origen   varchar NOT NULL DEFAULT 'seed_dev',
  PRIMARY KEY (upz_cod, anio, mes, feature)
);
```

### `upz_geometrias` — polígonos UPZ (PostGIS, F2)
```sql
CREATE TABLE IF NOT EXISTS upz_geometrias (
  upz_cod        varchar PRIMARY KEY,
  upz_nombre     varchar,
  cod_localidad  varchar,
  nom_localidad  varchar,
  geom           geometry(MultiPolygon, 4326)
);
CREATE INDEX IF NOT EXISTS idx_upz_geom ON upz_geometrias USING GIST (geom);
```

### `cuadrantes_geom` — cuadrantes de policía (PostGIS, F4) + mapeo a UPZs
```sql
CREATE TABLE IF NOT EXISTS cuadrantes_geom (
  cuadrante_id varchar PRIMARY KEY,
  nom_cai      varchar,
  geom         geometry(MultiPolygon, 4326),
  upz_codes    varchar[]        -- UPZs que intersecta (pre-computado en seed)
);
CREATE INDEX IF NOT EXISTS idx_cuadrantes_geom ON cuadrantes_geom USING GIST (geom);
```
Usado por: filtro comandante-por-cuadrante (backend, D8) y datos del CAI en /prescribe.

### `change_points` — rupturas estructurales (ruptures sobre F1 DAI)
```sql
CREATE TABLE IF NOT EXISTS change_points (
  localidad_cod varchar, localidad_nom varchar,
  fecha_ruptura date, tipo_cambio varchar,  -- 'ALZA' | 'BAJA' | 'INDEFINIDO'
  magnitude float
);
```

### `user_profiles` — roles y cuadrante asignado
```sql
CREATE TABLE IF NOT EXISTS user_profiles (
  user_id            uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email              varchar NOT NULL,
  rol                varchar NOT NULL DEFAULT 'CIUDADANO'
                     CHECK (rol IN ('CIUDADANO','COMANDANTE_CAI','ANALISTA_SDSCJ','ADMIN')),
  cuadrante_asignado varchar REFERENCES cuadrantes_geom(cuadrante_id),
  aprobado           boolean NOT NULL DEFAULT false,
  created_at         timestamptz DEFAULT now()
);
```

**Autoprovisioning por dominio** (trigger `on_auth_user_created` sobre `auth.users`):
- `@policia.gov.co` → COMANDANTE_CAI (cuadrante_asignado NULL hasta que ADMIN lo asigne)
- `@sdscj.gov.co` → ANALISTA_SDSCJ
- resto → CIUDADANO con `aprobado=false`

**Claims JWT** — función `public.custom_access_token_hook(event jsonb)` inyecta `rol` y `cuadrante_asignado` en el access token. ⚠️ El hook se habilita **manualmente**: Dashboard → Auth → Hooks → Custom Access Token.

### `documents_corpus` — corpus GraphRAG (F10, pgvector)
```sql
CREATE TABLE IF NOT EXISTS documents_corpus (
  id           bigserial PRIMARY KEY,
  content      text NOT NULL,
  content_hash varchar UNIQUE,    -- sha256 para dedup en reindexación
  source       varchar,           -- 'RSS_ELTIEMPO' | 'RSS_ESPECTADOR' | 'RSS_INFORMANTE' | 'SEED_DEV'
  titulo       varchar,
  fecha        date,
  url          varchar,
  upz_cod      varchar,           -- nullable — etiquetado por heurística regex
  embedding    vector(384)        -- all-MiniLM-L6-v2 — NUNCA cambiar de modelo sin reindexar todo
);
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents_corpus
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(384),
  match_threshold float,
  match_count int,
  filter_upz varchar DEFAULT NULL
)
RETURNS TABLE (id bigint, content text, source varchar, titulo varchar, fecha date, url varchar, similarity float)
LANGUAGE sql STABLE AS $$
  SELECT id, content, source, titulo, fecha, url,
         1 - (embedding <=> query_embedding) AS similarity
  FROM documents_corpus
  WHERE (filter_upz IS NULL OR upz_cod = filter_upz)
    AND 1 - (embedding <=> query_embedding) > match_threshold
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
```

### `alarmas_ciudadanas` — feature opcional post-concurso (Idea 6)
Sin cambios — ver `docs/HU-Features-Opcionales.md`. Realtime habilitado por cuadrante.

## Scripts de datos

```bash
# Migraciones: supabase/migrations/*.sql — aplicadas vía MCP Supabase (apply_migration)
python scripts/seed_supabase.py         # silver (COPY) + geo F2/F4 + predicciones/shap sintéticos (origen='seed_dev')
python scripts/index_corpus.py          # F10 → chunks → embeddings → documents_corpus
python scripts/load_model_artifacts.py  # SWITCH: borra seed_dev, carga artefactos reales Notebooks 03/04
```

## Row Level Security (RLS)

⚠️ **Regla D8**: el backend usa SERVICE_KEY que **bypasea RLS** — estas políticas protegen al **frontend** (anon key + token de usuario). El backend duplica el filtro por rol en su capa services.

```sql
ALTER TABLE predicciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE shap_values ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents_corpus ENABLE ROW LEVEL SECURITY;

-- Comandante solo ve predicciones de UPZs de su cuadrante
CREATE POLICY "comandante_solo_su_cuadrante" ON predicciones FOR SELECT
  USING (
    (auth.jwt()->>'rol') IN ('ANALISTA_SDSCJ','ADMIN')
    OR (
      (auth.jwt()->>'rol') = 'COMANDANTE_CAI'
      AND upz_cod IN (
        SELECT unnest(upz_codes) FROM cuadrantes_geom
        WHERE cuadrante_id = auth.jwt()->>'cuadrante_asignado'
      )
    )
    OR (auth.jwt()->>'rol') = 'CIUDADANO'   -- ciudadano ve el mapa público completo
  );
-- upz_geometrias: lectura pública (anon) para el mapa base
```

## Conexión desde Python (backend FastAPI)

```python
from supabase import acreate_client   # cliente async (supabase-py v2)

supabase = await acreate_client(settings.supabase_url, settings.supabase_service_key)
resp = await supabase.table("predicciones").select("*") \
    .eq("upz_cod", "044").eq("anio", 2026).eq("mes", 7).execute()
```

## Conexión desde React (frontend)

```typescript
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY   // clave pública — RLS aplica
)
// Realtime para alarmas del cuadrante (feature opcional)
supabase.channel('cuadrante-048')
  .on('postgres_changes', { event: 'INSERT', table: 'alarmas_ciudadanas',
      filter: 'cuadrante_id=eq.048' },
    (payload) => console.log('Nueva alarma:', payload.new))
  .subscribe()
```
