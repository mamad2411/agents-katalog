---
name: geospatial-bogota
description: Análisis geoespacial de Bogotá — UPZs, spatial joins con GeoPandas, PostGIS en Supabase, deck.gl layers.
---

# Geospatial Bogotá — SeguroData

Guía para todo el trabajo geoespacial del proyecto: shapefiles de UPZ, spatial joins, PostGIS y visualización en deck.gl.

## Archivos geoespaciales del proyecto

| Archivo | Fuente | Filas | Descripción |
|---------|--------|-------|-------------|
| `datos/raw/f2_upz.geojson` | F2 IDECA | 112 | Polígonos UPZ de Bogotá (EPSG:4326) |
| `datos/raw/f4_cuadrantes.geojson` | F4 MEBOG | 599 | Cuadrantes policiales con nombre del CAI |
| `datos/raw/f7_estratificacion.parquet` | F7 SDP | 44,260 | Manzanas catastrales con estrato + geometría WKT |
| `datos/raw/f8_transmilenio.geojson` | F8 TM | 153 | Estaciones TransMilenio (puntos) |
| `datos/raw/f13_camaras_sdm.geojson` | F13 SDM | 92 | Cámaras Salvavidas (puntos) |

## Spatial joins — patrones del proyecto

```python
import geopandas as gpd
import polars as pl

# Cargar UPZ
upz = gpd.read_file("datos/raw/f2_upz.geojson")
upz = upz.to_crs(epsg=4326)  # Asegurar WGS84

# Spatial join de puntos (ej: cámaras SDM) con UPZ
camaras = gpd.read_file("datos/raw/f13_camaras_sdm.geojson")
camaras_upz = gpd.sjoin(camaras, upz[["upz_cod", "geometry"]], 
                         how="left", predicate="within")
n_camaras_por_upz = camaras_upz.groupby("upz_cod").size().reset_index(name="n_camaras_upz")

# Spatial join de polígonos (ej: cuadrantes) con UPZ — para cuadrantes/km²
cuadrantes = gpd.read_file("datos/raw/f4_cuadrantes.geojson")
cuadrantes_upz = gpd.sjoin(cuadrantes, upz, how="left", predicate="intersects")
```

## F7 (estratificación) — advertencia de memoria

El spatial join de 44K manzanas con 112 UPZs consume **4-5 GB de RAM**.

```python
# ✅ Solo ejecutar una vez (el resultado es casi estático)
python src/transform.py --step f7 --force

# Si falla en Colab gratuito → ejecutar localmente y subir estrato_por_upz.csv
# El archivo resultante: datos/procesados/estrato_por_upz.csv (43 UPZs cubiertas)
```

## Nota sobre la cobertura de F7

F7 solo cubre **43 de 112 UPZs** — el resto no tiene manzanas con estrato mapeado (zonas industriales, aeropuerto, reservas).

```python
# Las UPZs sin estrato reciben NaN → imputar con la media por localidad
silver = silver.with_columns([
    pl.col("estrato_promedio_upz").fill_null(
        pl.col("estrato_promedio_upz").mean().over("cod_localidad")
    )
])
```

## PostGIS en Supabase

```sql
-- Extensiones requeridas (ya configuradas)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla de geometrías UPZ
CREATE TABLE upz_geometrias (
  upz_cod varchar PRIMARY KEY,
  upz_nombre varchar,
  cod_localidad varchar,
  nom_localidad varchar,
  geom geometry(Polygon, 4326)
);

-- Cargar desde GeoJSON
-- usar: python scripts/load_geometrias.py

-- Query PostGIS: encontrar UPZ por lat/lon
SELECT upz_cod, upz_nombre
FROM upz_geometrias
WHERE ST_Contains(geom, ST_SetSRID(ST_MakePoint(-74.072, 4.711), 4326));
```

## Deck.gl layers (frontend React)

```javascript
// Layer 1: coropleta UPZ por nivel de riesgo
new PolygonLayer({
  id: 'upzs-riesgo',
  data: upzsConRiesgo,
  getPolygon: d => d.coordinates,
  getFillColor: d => d.nivel_riesgo === 'ALTO'  ? [239, 68, 68, 180]
                   : d.nivel_riesgo === 'MEDIO' ? [234, 179, 8, 180]
                                                : [34, 197, 94, 180],
  pickable: true,
  onClick: ({ object }) => mostrarModalUPZ(object)
})

// Layer 2: cámaras Salvavidas (toggle)
new ScatterplotLayer({
  id: 'camaras',
  data: camaras,
  getPosition: d => [d.lon, d.lat],
  getRadius: 100,
  getFillColor: [59, 130, 246]
})

// Layer 3: heatmap densidad incidentes
new HeatmapLayer({
  id: 'heatmap-incidentes',
  data: incidentes,
  getPosition: d => [d.lon, d.lat],
  getWeight: d => d.n_delitos
})
```

## EPSG y proyecciones

- Todos los datos: **EPSG:4326 (WGS84)** — latitud/longitud decimal
- Para cálculos de área/distancia precisos: **EPSG:3116 (MAGNA-SIRGAS Colombia)** → convertir con `upz.to_crs(epsg=3116)`
- Bogotá: lat ≈ 4.71, lon ≈ -74.07

## Verificar el shapefile de UPZ

```python
upz = gpd.read_file("datos/raw/f2_upz.geojson")
assert len(upz) == 112, f"Se esperaban 112 UPZs, hay {len(upz)}"
assert upz.crs.to_epsg() == 4326, "CRS incorrecto"
# Columna clave: upz_cod (ej: "044", "099", "104")
```
