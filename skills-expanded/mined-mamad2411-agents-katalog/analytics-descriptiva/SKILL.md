---
name: analytics-descriptiva
description: Análisis exploratorio de datos (EDA) del proyecto SeguroData Bogotá — NUSE, DAI, clima y features por UPZ.
---

# Analytics Descriptiva — SeguroData Bogotá

Realiza EDA sobre los datos de crimen, incidentes y contexto urbano de Bogotá a nivel UPZ (112 zonas).

## Datos disponibles

| Dataset | Ruta | Descripción |
|---------|------|-------------|
| Silver principal | `datos/procesados/silver_upz_mes.parquet` | 111,606 filas × 20 cols: UPZ × mes × tipo_incidente |
| DAI histórico | `datos/procesados/delitos_localidad_anio.parquet` | 2018–2026 por localidad (para ruptures) |
| Clima diario | `datos/procesados/clima_diario.parquet` | temperatura_c, precipitacion_mm por día |
| UPZ shapefile | `datos/raw/f2_upz.geojson` | 112 polígonos, base de mapas |

## Tipos de análisis

### 1. Distribución espacial
- Top-10 UPZs con más incidentes criminales (filtrar `es_crimen=True`)
- Mapa de coropleta por nivel de riesgo (usar `f2_upz.geojson` + geopandas)
- Comparar densidad de delitos vs densidad de cuadrantes por UPZ

### 2. Distribución temporal
- Serie mensual 2025–2026 por UPZ (agrupar por `anio`, `mes`)
- Distribución por `franja_dominante_mes` (madrugada/mañana/tarde/noche)
- Identificar picos: fin de año, Semana Santa, inicio de año escolar

### 3. Tipos de crimen
- Frecuencia de `tipo_crimen` (Top-20 de los 86 tipos NUSE)
- Comparar tipos de crimen criminal (`es_crimen=True`) vs desorden urbano (`es_crimen=False`)
- Correlación entre tipos de crimen en la misma UPZ

### 4. Calidad de datos
- % nulos por columna en Silver
- UPZs sin cobertura de estrato (F7 solo cubre 43/112 UPZs)
- Detectar outliers en `ratio_nuse_delitos_upz` (proxy de subregistro)

### 5. Análisis de correlaciones (para el Notebook 02)
- Correlación entre features espaciales y `n_delitos` (scatterplot + heatmap)
- SHAP correlation proxy: ¿cuál feature varía más con el nivel de riesgo?

## Código base (Polars)

```python
import polars as pl
import geopandas as gpd
import matplotlib.pyplot as plt

silver = pl.read_parquet("datos/procesados/silver_upz_mes.parquet")

# Solo crimen de alto impacto
crimenes = silver.filter(pl.col("es_crimen") == True)

# Top-10 UPZs
top_upz = crimenes.group_by("upz_cod").agg(
    pl.col("n_delitos").sum().alias("total")
).sort("total", descending=True).head(10)
```

## Advertencias del proyecto

- **F1 (DAI)** tiene granularidad de LOCALIDAD (no UPZ) — usar solo para tendencias históricas 2018–2026
- **F6 (Hurto PN)** tiene granularidad MUNICIPIO — solo benchmarking nacional
- La tabla Silver tiene 86 tipos NUSE. Filtrar siempre por `es_crimen=True` para el análisis criminológico
- **F7 (estratificación)** cubre solo 43 de 112 UPZs — mencionar en el análisis de cobertura
- Guardar figuras en `graficas/` con nombres descriptivos (V1-V7 para el EDA del Notebook 02)

## Output esperado

- Código Python ejecutable en Notebook 02
- 7 visualizaciones guardadas en `graficas/`
- Tabla resumen de calidad de datos
- Conclusiones en lenguaje del concurso: mencionar UPZs por nombre (Kennedy, Suba, etc.)
