---
name: modelo-xgboost
description: Modelo XGBoost + SHAP + ruptures para SeguroData — entrenamiento, evaluación, pre-cómputo y análisis de sesgo.
---

# Modelo XGBoost — SeguroData Bogotá

El modelo predictivo principal. Corresponde al **Módulo 2 ("¿Qué va a pasar?")** y alimenta el Módulo 3.

## Las 18 variables de entrada

> Lista real y autoritativa en `scripts/train_model.py` (constante `FEATURES`). Granularidad UPZ × mes.

```python
FEATURES = [
    # Históricas / lag temporal
    "n_delitos_upz_4sem", "n_delitos_upz_8sem", "n_delitos_upz_12sem", "tendencia_upz",
    # Lag espacial (delitos de UPZs vecinas en t-1, adyacencia F2)
    "n_delitos_vecinos_lag",
    # Temporales cíclicas (reemplazan el `mes` crudo)
    "mes_sin", "mes_cos",
    # Climáticas
    "temperatura_c", "precipitacion_mm_mes",
    # Espaciales
    "estrato_promedio_upz", "cuadrantes_por_km2", "n_estaciones_tm", "dist_tm_metros",
    # Subregistro
    "ratio_nuse_criminal_upz",
    # Infraestructura (n_camaras_upz/luminarias_led_upz reales desde 10-jul;
    # km_via_intervenida_upz = F11, sigue placeholder 0, sin extractor)
    "km_via_intervenida_upz", "n_camaras_upz", "luminarias_led_upz",
    # Tipo de delito dominante (codificado)
    "tipo_crimen_cod",
]
TARGET = "nivel_riesgo"  # CRÍTICO / ALTO / MEDIO / BAJO (4 clases ordinales, percentiles q40/q75/q95)
```

## Validación temporal — REGLA CRÍTICA

```python
# NUNCA usar train_test_split aleatorio — data leakage temporal
silver = pl.read_parquet("datos/procesados/silver_upz_mes.parquet")
crimenes = silver.filter(pl.col("es_crimen") == True)

train = crimenes.filter(
    (pl.col("anio") == 2025) & (pl.col("mes") <= 10)  # ene-oct 2025
)
test = crimenes.filter(
    ((pl.col("anio") == 2025) & (pl.col("mes") >= 11)) |
    (pl.col("anio") == 2026)                           # nov 2025 – abr 2026
)
```

## Entrenamiento

```python
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_train = le.fit_transform(train[TARGET])  # BAJO=0, MEDIO=1, ALTO=2, CRÍTICO=3

model = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric="mlogloss",
    random_state=42
)
model.fit(
    train[FEATURES].to_pandas(),
    y_train,
    eval_set=[(test[FEATURES].to_pandas(), le.transform(test[TARGET]))],
    verbose=False
)

# Guardar modelo
import joblib
joblib.dump({"model": model, "label_encoder": le}, "datos/modelos/xgboost_segurodata.joblib")
```

## SHAP values — pre-computar en Notebook 04

```python
import shap
import polars as pl

# NUNCA calcular on-demand en la app — pre-computar y guardar en Supabase
explainer = shap.TreeExplainer(model)
X_all = silver.filter(pl.col("es_crimen") == True)[FEATURES].to_pandas()
shap_values = explainer.shap_values(X_all)

# Guardar como tabla plana (una fila por UPZ × mes × clase)
shap_df = pl.DataFrame({
    "upz_cod": silver["upz_cod"],
    "anio": silver["anio"],
    "mes": silver["mes"],
    **{f"shap_{feat}": shap_values[clase_alto][:, i] 
       for i, feat in enumerate(FEATURES)}
})
shap_df.write_parquet("datos/modelos/shap_values_upz.parquet")
# Luego: python scripts/load_shap.py → carga en Supabase tabla shap_values
```

## Métricas — reportar SIEMPRE

```python
from sklearn.metrics import classification_report

y_pred = le.inverse_transform(model.predict(test[FEATURES].to_pandas()))
print(classification_report(test[TARGET], y_pred, target_names=["BAJO","MEDIO","ALTO","CRÍTICO"]))
# Reportar: precision, recall, F1 por clase + macro average + accuracy dentro de ±1 banda
# NUNCA solo accuracy exact-match (clases desbalanceadas + objetivo ordinal)
```

## Análisis de sesgo por estrato — OBLIGATORIO

```python
# Para responder al jurado: "¿el modelo discrimina por estrato?"
import shap

# 1. SHAP dependence plot: ¿cómo afecta el estrato a la predicción?
shap.dependence_plot("estrato_promedio_upz", shap_values[clase_alto], X_all)

# 2. Tasa de falsos negativos por estrato
test_df = test.to_pandas()
test_df["pred"] = y_pred
test_df["falso_negativo"] = (test_df[TARGET] == "ALTO") & (test_df["pred"] != "ALTO")
sesgo = test_df.groupby("estrato_promedio_upz_bin")["falso_negativo"].mean()
print(sesgo)
# Resultado esperado: distribución similar en todos los estratos
```

## Detección de cambios estructurales (ruptures)

```python
import ruptures as rpt

# Para cada localidad (F1 DAI 2018-2026):
def detectar_cambios(serie_mensual, pen=10):
    algo = rpt.Pelt(model="rbf").fit(serie_mensual.values)
    return algo.predict(pen=pen)

# Guardar en Supabase tabla change_points para el Módulo 3 (Prescriptivo)
```

## Archivos generados en Notebook 04

```
datos/modelos/
├── xgboost_segurodata.joblib     ← modelo + label encoder
├── shap_values_upz.parquet       ← SHAP pre-computados
├── tabla_ontologica.json         ← 17 filas (generado en Notebook 03)
└── change_points_localidades.csv ← breakpoints ruptures por localidad
```
