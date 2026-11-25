---
name: etl-open-data
description: Pipeline ETL de las 12 fuentes de datos abiertos de SeguroData — CKAN, Socrata, ArcGIS, Open-Meteo.
---

# ETL Open Data — SeguroData Bogotá

Pipeline de extracción de las 12 fuentes activas del proyecto. Todo vive en `src/pipeline.py` y `src/etl.py`.

## Plataformas — distinción crítica

| Portal | Plataforma | Conector en src/etl.py |
|--------|-----------|----------------------|
| `datosabiertos.bogota.gov.co` | **CKAN** | `ckan_query()`, `ckan_download()` |
| `www.datos.gov.co` | **Socrata** | `socrata_query()` (usa sodapy) |
| `data-movilidadbogota.opendata.arcgis.com` | **ArcGIS Hub** | `arcgis_query()` |
| `serviciosgis.catastrobogota.gov.co` | **ArcGIS REST** | `arcgis_query()` |
| `archive-api.open-meteo.com` | **REST pública** | `open_meteo()` |

## Comandos del pipeline

```bash
python src/pipeline.py --status          # estado de las 12 fuentes
python src/pipeline.py --dry-run         # qué descargaría sin ejecutar
python src/pipeline.py                   # descargar solo lo nuevo (incremental)
python src/pipeline.py --source f3       # una fuente específica
python src/pipeline.py --source f1 --force  # forzar re-descarga
```

## Las 12 fuentes activas

| ID | Fuente | Plataforma | Resource ID / URL | Archivo Bronze |
|----|--------|-----------|------------------|---------------|
| F1 | Delito de Alto Impacto | CKAN | `7b270013-42ca-436b-9c1e-3bcb7d280c6b` | `f1_delito_alto_impacto.parquet` |
| F2 | UPZ Shapefile IDECA | ArcGIS REST | `a5c8c591-0708-420f-8eb7-9f3147e21c40` | `f2_upz.geojson` |
| F3 | Clima Open-Meteo | REST | `archive-api.open-meteo.com` | `f3_clima_bogota.parquet` |
| F4 | Cuadrantes Policía | CKAN | `f0ad2ee3-bfd0-4825-9b31-bff9041649fa` | `f4_cuadrantes.geojson` |
| F5 | NUSE 123 C4 | CKAN | `30d65a8b-d0ed-4e95-977e-0d7cc2ea89ef` | `f5_nuse_123.parquet` |
| F6 | Hurto PN | Socrata | `4rxi-8m8d` (datos.gov.co) | `f6_hurto_pn.parquet` |
| F7 | Estratificación SDP | CKAN | `29f2d770-bd5d-4450-9e95-8737167ba12f` | `f7_estratificacion.parquet` |
| F8 | TransMilenio | ArcGIS | `9be8b6fb-8059-492f-a866-4a1ac031c502` | `f8_transmilenio.geojson` |
| F10 | Noticias RSS | RSS | El Tiempo + Espectador + El Informante | `noticias_rss.jsonl` |
| F11 | Obras IDU | CKAN | datosabiertos.bogota.gov.co/organization/idu | `f11_idu_calzada/` |
| F13 | Cámaras SDM | ArcGIS Hub | data-movilidadbogota.opendata.arcgis.com | `f13_camaras_sdm.geojson` |
| F14 | Alumbrado UAESP | CKAN | `luminarias_upz-bogota-d-c` | `f14_alumbrado_upz.csv` |

> F12 (Plan Desarrollo 2024-2027) — Planificada para Fase 3 (corpus GraphRAG)

## Estrategias incrementales

```python
# F1, F2, F4, F7, F8 → HTTP Last-Modified (solo descarga si cambió)
# F3 Clima → append desde max(fecha) hasta ayer
# F5 NUSE → descarga por año + deduplicación
# F6 Hurto PN → Socrata $where fecha_hecho > 'max_fecha'
# F10 RSS → feedparser, solo artículos nuevos

# Uso desde notebook:
from src.pipeline import run_pipeline
resultados = run_pipeline(sources=["f3", "f5"], verbose=True)
```

## Variables de entorno requeridas

```bash
# .env del proyecto (no commitear)
SOCRATA_APP_TOKEN=<token gratuito de dev.socrata.com>
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
```

## App Token Socrata

Sin token el límite es 1,000 filas/request. Registrar gratis en dev.socrata.com.
F5 NUSE tiene 128K registros → sin token tarda mucho. Con token sube a 50K filas/request.

## Nota sobre SIEDCO

El ID `2bxu-b96f` da 404 — no existe como dataset tabular. Usar F1 (Delito de Alto Impacto) para crimen por localidad y F5 (NUSE) para crimen por UPZ.
