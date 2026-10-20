---
name: analytics-predictiva
description: Capa predictiva de SeguroData — inferencia XGBoost, evaluación, backtesting, tendencias y Módulo 2 del dashboard.
---

# Analytics Predictiva — SeguroData Bogotá

Cubre todo el ciclo de predicción: desde la tabla Silver hasta las probabilidades por UPZ que alimentan el **Módulo 2 ("¿Qué va a pasar?")** del dashboard.

## Flujo completo de predicción

```
Silver (111,606 filas)
  → Gold: tabla maestra con 18 features + nivel_riesgo (scripts/train_model.py)
  → Entrenamiento XGBoost — TRAIN: ene–oct 2025 (Notebook 04)
  → SHAP pre-computados → Supabase tabla shap_values
  → FastAPI /predict → {upz_cod, mes} → {nivel_riesgo, probabilidades}
  → React Módulo 2: mapa coropleta ALTO/MEDIO/BAJO + panel SHAP
```

## Inferencia con el modelo entrenado

```python
import joblib
import polars as pl
import pandas as pd

# Cargar modelo serializado (generado en Notebook 04)
bundle = joblib.load("datos/modelos/xgboost_segurodata.joblib")
model, le = bundle["model"], bundle["label_encoder"]

FEATURES = [
    "n_delitos_upz_4sem", "n_delitos_upz_8sem", "tipo_delito_dominante",
    "dia_semana", "franja_horaria", "mes", "es_fin_semana",
    "temperatura_c", "precipitacion_mm",
    "estrato_promedio_upz", "cuadrantes_por_km2", "n_estaciones_tm", "dist_tm_metros",
    "ratio_nuse_criminal_upz",
    "km_via_intervenida_upz", "n_camaras_upz", "luminarias_led_upz"
]

def predecir_upz(df_features: pd.DataFrame):
    """
    Devuelve nivel de riesgo + probabilidades para cada fila.
    """
    probs = model.predict_proba(df_features[FEATURES])
    clases = le.classes_  # ['ALTO', 'BAJO', 'MEDIO'] — orden alfabético
    return pd.DataFrame(probs, columns=[f"prob_{c}" for c in clases])
```

## Backtesting — evaluación en el conjunto de test

```python
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns, matplotlib.pyplot as plt

# Cargar Silver y separar test
silver = pl.read_parquet("datos/procesados/silver_upz_mes.parquet")
crimenes = silver.filter(pl.col("es_crimen") == True)
test = crimenes.filter(
    ((pl.col("anio") == 2025) & (pl.col("mes") >= 11)) |
    (pl.col("anio") == 2026)
).to_pandas()

y_pred = le.inverse_transform(model.predict(test[FEATURES]))
y_true = test["nivel_riesgo"]

# Reporte completo (no usar accuracy solo — clases desbalanceadas)
print(classification_report(y_true, y_pred, target_names=["BAJO","MEDIO","ALTO"]))

# Matriz de confusión
cm = confusion_matrix(y_true, y_pred, labels=["ALTO","MEDIO","BAJO"])
sns.heatmap(cm, annot=True, fmt="d", xticklabels=["ALTO","MEDIO","BAJO"],
            yticklabels=["ALTO","MEDIO","BAJO"])
plt.title("Matriz de confusión — Test nov2025–abr2026")
plt.savefig("graficas/V8_confusion_matrix.png")
```

## Predicción para todas las UPZs (mapa completo)

```python
# Generar predicciones para todas las UPZs en el mes actual
# Este resultado se carga en Supabase tabla shap_values (pre-computado en Notebook 04)

gold = pl.read_parquet("datos/features/gold_upz_mes.parquet")
mes_actual = gold.filter(
    (pl.col("anio") == 2026) & (pl.col("mes") == pl.col("mes").max())
)

predicciones = predecir_upz(mes_actual.to_pandas())
mes_actual = mes_actual.with_columns([
    pl.Series("nivel_riesgo_pred", le.inverse_transform(model.predict(mes_actual.to_pandas()[FEATURES]))),
    pl.Series("prob_alto", predicciones["prob_ALTO"])
])

# Guardar para Supabase
mes_actual.select(["upz_cod", "anio", "mes", "nivel_riesgo_pred", "prob_alto"]) \
          .write_parquet("datos/modelos/predicciones_mes_actual.parquet")
```

## Tendencias predictivas (Módulo 2 extendido)

```python
# Proyección a +4 semanas usando los lags existentes
# Para responder: "si no se actúa, ¿hacia dónde va esta UPZ?"

def proyectar_tendencia(upz_cod: str, silver: pl.DataFrame):
    """
    Extrapola la tendencia de los últimos 2 meses para proyectar el siguiente.
    Devuelve el nivel de riesgo proyectado + probabilidad de escalar.
    """
    serie = (
        silver
        .filter((pl.col("upz_cod") == upz_cod) & (pl.col("es_crimen") == True))
        .sort(["anio", "mes"])
        .select(["anio", "mes", "n_delitos", "n_delitos_upz_4sem", "n_delitos_upz_8sem"])
        .tail(3)  # últimos 3 meses
    )
    
    # Extrapolación lineal simple (suficiente para el concurso)
    delta = serie["n_delitos_upz_4sem"][-1] - serie["n_delitos_upz_4sem"][-2]
    proyectado = serie["n_delitos_upz_4sem"][-1] + delta
    
    # Calcular percentil proyectado (usando los umbrales del training)
    return {
        "n_delitos_proyectado": proyectado,
        "tendencia": "ALZA" if delta > 0 else "BAJA",
        "magnitud_delta": abs(delta)
    }
```

## Endpoint FastAPI /predict (uso desde el backend)

```python
# backend/routers/predict.py
from fastapi import APIRouter
import joblib

router = APIRouter()
bundle = joblib.load("datos/modelos/xgboost_segurodata.joblib")
model, le = bundle["model"], bundle["label_encoder"]

@router.post("/predict")
async def predict(upz_cod: str, mes: int, anio: int):
    # 1. Obtener features de Supabase para esa UPZ+mes
    features = await get_features_from_supabase(upz_cod, mes, anio)
    # 2. Inferencia
    probs = model.predict_proba([features])[0]
    nivel = le.inverse_transform([model.predict([features])[0]])[0]
    return {
        "nivel_riesgo": nivel,
        "probabilidades": {c: float(p) for c, p in zip(le.classes_, probs)}
    }
```

## Métricas objetivo para el concurso

| Métrica | Objetivo realista | Por qué |
|---------|------------------|---------|
| F1 macro | > 0.55 | Clases desbalanceadas — F1 macro es la métrica honesta |
| Recall ALTO | > 0.65 | El costo de un falso negativo (no detectar ALTO) es mayor |
| Precision ALTO | > 0.60 | Minimizar falsas alarmas que desgastan al comandante |

> Referencia: Riascos & Mateo (2019) — CAP-AUC=0.8 en Bogotá con Hawkes Process. El estado del arte académico (ST-GNN Chicago) alcanza F1=0.71 con 320K registros. Con 111K registros de entrenamiento, F1 macro > 0.55 es un resultado sólido y honesto.

## Visualizaciones del Módulo 2 (Notebook 05 → React)

```javascript
// Mapa coropleta: todas las UPZs coloreadas por predicción del mes
new PolygonLayer({
  id: 'predicciones',
  data: upzsConPredicciones,
  getFillColor: d => d.nivel_riesgo_pred === 'ALTO'  ? [239, 68, 68, 200]
                   : d.nivel_riesgo_pred === 'MEDIO' ? [234, 179, 8, 200]
                                                     : [34, 197, 94, 200],
  pickable: true
})
```

## Advertencias

- **NUNCA calcular SHAP on-demand** — pre-computar en Notebook 04 y servir desde Supabase
- **NUNCA usar train_test_split aleatorio** — usar corte temporal (ene–oct 2025 TRAIN)
- El modelo `xgboost_segurodata.joblib` se carga UNA SOLA VEZ al iniciar FastAPI, no por request
- Si `n_camaras_upz` o `luminarias_led_upz` tienen NaN (F13/F14 no cubren todas las UPZs): imputar con 0 antes de predecir
