---
name: bigdata-python
description: Optimización Python para datasets grandes en este proyecto — Polars, memoria Colab, procesamiento incremental.
---

# Big Data Python — SeguroData Bogotá

Guía para trabajar eficientemente con los datasets del proyecto, especialmente en Google Colab gratuito.

## Tamaños de datasets

| Dataset | Filas | Peso estimado | Notas |
|---------|-------|--------------|-------|
| F5 NUSE (Bronze) | 128,314 | ~50 MB | Fuente principal — Polars nativo |
| F6 Hurto PN (Bronze) | 638,569 | ~200 MB | Solo benchmarking — cargar por chunks |
| F7 Estratificación (Bronze) | 44,260 polígonos | ~100 MB | **Pesado** — spatial join consume 4-5 GB RAM |
| Silver final | 111,606 × 20 cols | ~80 MB | Resultado del pipeline — Polars |
| F3 Clima horario | 56,112 filas | ~15 MB | Ligero |

## Polars vs Pandas — reglas del proyecto

```python
# ✅ USAR Polars para todos los datasets > 10K filas
import polars as pl

silver = pl.read_parquet("datos/procesados/silver_upz_mes.parquet")

# Lazy evaluation para queries complejas (no carga todo en RAM)
resultado = (
    silver.lazy()
    .filter(pl.col("es_crimen") == True)
    .group_by(["upz_cod", "anio", "mes"])
    .agg(pl.col("n_delitos").sum())
    .collect()
)

# ✅ USAR Pandas solo para spatial joins con GeoPandas (requiere .to_pandas())
import geopandas as gpd
upz = gpd.read_file("datos/raw/f2_upz.geojson")
df_pd = silver_subset.to_pandas()
gdf = gpd.GeoDataFrame(df_pd, geometry=gpd.points_from_xy(df_pd.lon, df_pd.lat))
```

## Paso F7 (estratificación) — advertencia crítica

El spatial join de 44K manzanas contra 112 UPZs consume 4-5 GB de RAM.

```python
# ❌ NO hacer esto en Colab gratuito (8 GB RAM disponibles, el join los agota)
gdf_join = gpd.sjoin(estratificacion, upz, how="left", predicate="within")

# ✅ Opciones seguras:
# Opción A — Ejecutar solo una vez localmente y subir el CSV resultante
python src/transform.py --step f7 --verbose
# Luego subir datos/procesados/estrato_por_upz.csv

# Opción B — Colab Pro (más RAM)
# Opción C — Procesar en chunks de 5K manzanas
chunk_size = 5000
for i in range(0, len(estratificacion), chunk_size):
    chunk = estratificacion.iloc[i:i+chunk_size]
    resultado = gpd.sjoin(chunk, upz, how="left", predicate="within")
```

## Lectura incremental (F6 Hurto PN — 638K filas)

```python
# Cargar por chunks para benchmarking (no en entrenamiento)
import polars as pl

# Con Polars: leer en streaming
df = pl.scan_parquet("datos/raw/f6_hurto_pn.parquet").collect()

# O filtrar en la descarga Socrata (solo Bogotá, últimos 2 años)
from src.etl import socrata_query
df_hurto = socrata_query("4rxi-8m8d",
    where="municipio='BOGOTA D.C.' AND fecha_hecho >= '2024-01-01'")
```

## Formatos de archivo — reglas del proyecto

| Tipo de dato | Formato | Por qué |
|-------------|---------|---------|
| Datasets tabulares > 10K filas | `.parquet` | Columnar, compresión, compatible Polars |
| Tablas estáticas pequeñas | `.csv` | Legible, versionable en git |
| Datos geoespaciales | `.geojson` | Compatible geopandas + Supabase PostGIS |
| Modelos entrenados | `.joblib` | XGBoost serializado, ligero |
| SHAP values | `.parquet` | 1,918 filas Gold × 18 features = 34,524 filas |

## Optimización memoria en notebooks

```python
# Después de un paso pesado: liberar memoria explícitamente
import gc
del df_estratificacion_raw
gc.collect()

# Verificar memoria disponible
import psutil
print(f"RAM disponible: {psutil.virtual_memory().available / 1e9:.1f} GB")

# En Colab: monitorear durante el pipeline
!free -h
```

## Pipeline de datos — comandos

```bash
python src/pipeline.py --status          # estado de las 12 fuentes
python src/pipeline.py                   # descargar todo (solo lo nuevo)
python src/transform.py --dry-run        # ver qué haría sin ejecutar
python src/transform.py                  # Bronze → Silver (111,606 × 20 cols)
python src/transform.py --step f7 --force  # forzar recálculo estratificación
```
