---
name: data-science-crisp
description: Metodología CRISP-ML aplicada al proyecto — estructura de notebooks, validación temporal, análisis de sesgo.
---

# Data Science CRISP-ML — SeguroData Bogotá

El proyecto sigue CRISP-ML (Cross-Industry Standard Process for Machine Learning). Cada fase tiene un notebook dedicado.

## Estructura de notebooks

| Notebook | Fase CRISP-ML | Contenido | Estado |
|----------|--------------|-----------|--------|
| `SeguroData_01_Plan_y_Fuentes.ipynb` | Business Understanding | Catálogo 12 fuentes activas + F12 planificada, arquitectura, diferenciador | ✅ |
| `SeguroData_02_EDA.ipynb` | Data Understanding | EDA + change points ruptures F1 DAI | ✅ |
| `scripts/train_model.py` | Data Preparation | 18 variables, tabla ontológica prescriptiva, Supabase | ✅ |
| `SeguroData_04_Modelo.ipynb` | Modeling + Evaluation | XGBoost + SHAP pre-computados + análisis sesgo | ⏳ |
| `SeguroData_05_Dashboard.ipynb` | Deployment (desc.) | Arquitectura React+FastAPI+Supabase + screenshots | ⏳ |
| `SeguroData_06_Deployment.ipynb` | Deployment (impl.) | Deploy Vercel+Cloud Run + registro datos.gov.co | ⏳ |

## Regla CRÍTICA — Validación temporal (no aleatoria)

```
NUNCA usar train_test_split() aleatorio en series temporales — data leakage temporal.

CORRECTO:
  TRAIN: enero – octubre 2025  (10 meses de F5 NUSE)
  TEST:  noviembre 2025 – abril 2026  (6 meses — el modelo nunca los "vio")

INCORRECTO:
  from sklearn.model_selection import train_test_split
  X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)  # ❌ PROHIBIDO
```

```python
# ✅ Forma correcta
silver = pl.read_parquet("datos/procesados/silver_upz_mes.parquet")
train = silver.filter(
    (pl.col("anio") == 2025) & (pl.col("mes") <= 10)
)
test = silver.filter(
    ((pl.col("anio") == 2025) & (pl.col("mes") >= 11)) |
    (pl.col("anio") == 2026)
)
```

## Variable objetivo — definición

```python
# nivel_riesgo se define en Notebook 03 ANTES de entrenar
# Percentiles de n_delitos por upz_cod × anio × mes (solo es_crimen=True)
crimenes_agg = silver.filter(pl.col("es_crimen") == True)
    .group_by(["upz_cod", "anio", "mes"])
    .agg(pl.col("n_delitos").sum())

p75 = crimenes_agg["n_delitos"].quantile(0.75)
p40 = crimenes_agg["n_delitos"].quantile(0.40)

# top 25% → ALTO, 25–60% → MEDIO, resto → BAJO
```

## Las 18 variables del modelo (scripts/train_model.py)

```
HISTÓRICAS / LAG:    n_delitos_upz_4sem, n_delitos_upz_8sem, n_delitos_upz_12sem, tendencia_upz
LAG ESPACIAL:        n_delitos_vecinos_lag
TEMPORALES CÍCLICAS: mes_sin, mes_cos
CLIMÁTICAS:          temperatura_c, precipitacion_mm_mes
ESPACIALES:          estrato_promedio_upz, cuadrantes_por_km2, n_estaciones_tm, dist_tm_metros
SUBREGISTRO:         ratio_nuse_criminal_upz
INFRAESTRUCTURA:     km_via_intervenida_upz, n_camaras_upz, luminarias_led_upz
TIPO DELITO:         tipo_crimen_cod
OBJETIVO (Y):        nivel_riesgo (CRÍTICO/ALTO/MEDIO/BAJO — ordinal, percentiles q40/q75/q95)
```

## Análisis de sesgo por estrato — OBLIGATORIO en Notebook 04

El jurado siempre pregunta esto. Incluir:

1. **Distribución de predicciones por estrato** (1-6): ¿el modelo predice más ALTO en estratos bajos?
2. **Tasa de falsos negativos por estrato**: ¿las zonas de estrato bajo tienen más falsos negativos?
3. **SHAP interaction plots**: `shap.dependence_plot("estrato_promedio_upz", shap_values, X)`
4. **Conclusión esperada**: el estrato entra como feature causal legítima, no como proxy discriminatorio

## Métricas de evaluación (reporte mínimo)

```python
from sklearn.metrics import classification_report, confusion_matrix

# NUNCA reportar solo accuracy — las clases están desbalanceadas
print(classification_report(y_test, y_pred, target_names=["BAJO","MEDIO","ALTO","CRÍTICO"]))
# Reportar: precision, recall, F1 por clase + macro average
```

## Ruptures — change points (F1 DAI histórico)

```python
import ruptures as rpt

# Para cada localidad: detectar cuándo cambió el patrón de crimen
algo = rpt.Pelt(model="rbf").fit(serie_mensual_localidad)
breakpoints = algo.predict(pen=10)
# Guardar en Supabase tabla change_points para el Módulo 3
```

## Checklist por notebook

**Notebook 03 (Features):**
- [ ] Tabla ontológica prescriptiva (17 filas) — documentar ANTES del código
- [ ] 18 variables definidas con justificación causal
- [ ] Silver 20 cols cargado → Gold con variable objetivo agregada
- [ ] `tabla_ontologica.json` generado y guardado en `datos/modelos/`

**Notebook 04 (Modelo):**
- [ ] Validación temporal (no aleatoria)
- [ ] XGBoost entrenado + métricas completas (precision/recall/F1)
- [ ] SHAP values pre-computados y guardados como parquet
- [ ] Análisis de sesgo por estrato incluido
- [ ] Modelo serializado como `.joblib` en `datos/modelos/`
