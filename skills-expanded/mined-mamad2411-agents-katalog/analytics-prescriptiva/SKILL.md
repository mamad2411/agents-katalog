---
name: analytics-prescriptiva
description: Capa prescriptiva del sistema — tabla ontológica SHAP → diagnóstico → entidad → acción para el Módulo 3.
---

# Analytics Prescriptiva — SeguroData Bogotá

Genera recomendaciones operacionales basadas en SHAP values y detección de cambios estructurales (ruptures). Corresponde al **Módulo 3 ("¿Qué hacer?")** del dashboard.

## Flujo del Módulo 3

```
1. Usuario selecciona UPZ en el mapa
2. Sistema obtiene: SHAP top-3 features (Supabase tabla shap_values)
                  + ¿hay breakpoint reciente? (Supabase tabla change_points)
3. Tabla ontológica mapea: feature → diagnóstico → tipo → entidad → acción
4. FastAPI /prescribe → OpenRouter (LLM_MODEL) → texto operacional en lenguaje del comandante
```

## La tabla ontológica (17 filas — Notebook 03)

| SHAP top feature | Diagnóstico | Tipo | Entidad | Acción operacional |
|---|---|---|---|---|
| `cuadrantes_por_km2` bajo | Baja cobertura policial | Seguridad | MEBOG / SIJIN | Refuerzo cuadrante + CAI nombre + dirección + tel |
| `estrato_promedio_upz` bajo | Vulnerabilidad socioeconómica | Social | SDIS + SDDE | Programa Jóvenes en Paz + cupos empleo |
| `luminarias_led_upz` bajo | Baja iluminación nocturna | Urbanístico | UAESP | Reposición luminarias en franja madrugada |
| `n_camaras_upz` bajo | Sin disuasión tecnológica | Seguridad | SDSCJ | Solicitud cámaras Salvavidas SDM |
| `km_via_intervenida_upz` alto | Obra activa → puntos ciegos | Obras | IDU + MEBOG | Coordinación obra-seguridad |
| `n_delitos_upz_4sem` alto | Autoexcitación reciente | Operacional | MEBOG | Saturación patrullaje 48h |
| `temperatura_c` alto | Activador climático | Monitoreo | Policía + IDIGER | Alerta preventiva franja tarde/noche |
| `ratio_nuse_delitos_upz` alto | Alto subregistro | Datos | SDSCJ / C4 | Campaña denuncia ciudadana |
| `dist_tm_metros` alto | Zona aislada | Movilidad | TransMilenio S.A. | Factor de contexto — sin acción directa |
| `franja_dominante_mes` madrugada | Crimen nocturno | Seguridad | MEBOG turno noche | Operativo nocturno focalizado |
| `n_delitos_upz_8sem` alto + breakpoint | Problema estructural | Estratégico | SIJIN + SDIS | Intervención integral 30 días |

## Uso de ruptures para diagnóstico diferencial

```python
import ruptures as rpt

# Para cada localidad (F1 DAI histórico 2018-2026)
algo = rpt.Pelt(model="rbf").fit(serie_mensual)
breakpoints = algo.predict(pen=10)

# Si hay breakpoint reciente (< 6 meses) + tendencia sostenida → diagnóstico ESTRUCTURAL
# Si no hay breakpoint → diagnóstico TEMPORAL (pico coyuntural)
```

**Diferencia en la recomendación:**
- PICO TEMPORAL → saturación patrullaje 48h (MEBOG)
- PROBLEMA ESTRUCTURAL → intervención SIJIN + SDIS + seguimiento 30 días

## Formato de output (texto para el comandante)

```
**UPZ {nombre} — {localidad}** lleva {N} meses con {tipo_crimen} 
{estructuralmente elevado / en pico temporal}.

El factor dominante es {diagnóstico_shap_1} (SHAP +{valor}).
{Si hay obra IDU: agravado por obra activa en {vía}}.

Intervención recomendada:
• **{ENTIDAD_1}**: {acción_1}
• **{ENTIDAD_2}**: {acción_2}
• **CAI responsable**: {nombre_cai}, {dirección}, tel {telefono}
```

## Advertencias

- Los SHAP values deben ser **pre-computados** en `scripts/train_model.py` y cargados en Supabase tabla `shap_values` — NUNCA calcular on-demand en la app (crash de RAM)
- El nombre del CAI viene de F4 cuadrantes → campo incluido en Silver como `cai_nombre` + `cai_direccion`
- El texto lo genera OpenRouter (variable `LLM_MODEL=google/gemini-2.5-flash-lite` por defecto — los `:free` de OpenRouter no fueron confiables, ver `docs/chatbot_test_battery.md`)
- La `OPENROUTER_API_KEY` se configura en Cloud Run — NUNCA en el frontend

## Archivos relacionados

- `backend/routers/prescribe.py` — endpoint FastAPI /prescribe
- `datos/modelos/tabla_ontologica.json` — tabla de 17 filas (generada en Notebook 03)
- `datos/modelos/shap_values_upz.parquet` — SHAP pre-computados (Notebook 04)
