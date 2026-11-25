---
name: marketing-meta-ads-analyzer
description: "Analiza y diagnostica campañas de Meta Ads a partir de datos exportados, capturas o métricas del Ads Manager. Identifica causas raíz, interpreta CPA/ROAS/CPM/CTR con la mecánica real de subasta y pacing, evita errores del Breakdown Effect y produce recomendaciones accionables. Úsala cuando el usuario pida análisis de campañas, diagnóstico de rendimiento, CPA, ROAS, audiencias, creatividades o datos de Meta Ads."
---

# Análisis y Diagnóstico de Meta Ads

## Cuándo usar esta skill

Úsala para analizar rendimiento de campañas, conjuntos de anuncios o anuncios de Meta Ads:

- Interpretar exportaciones CSV, capturas o datos pegados desde Ads Manager.
- Detectar causas raíz de caída de rendimiento, CPA alto, bajo ROAS o fatiga creativa.
- Explicar por qué Meta asigna presupuesto de cierta forma.
- Proponer optimizaciones verificables sin romper el aprendizaje del sistema.

No asumas ninguna cuenta, campaña o benchmark privado. Trabaja solo con los datos que aporte el usuario y, si faltan métricas críticas, pide el mínimo necesario.

## Reglas obligatorias para informes finales

- **Nunca recomiendes pausar o bajar presupuesto de un segmento solo porque su CPA/CPM medio sea mayor en un desglose.** Un coste medio más alto no implica peor rendimiento; puede reflejar oportunidades marginales que el sistema captura después.
- **Justifica toda recomendación con evidencia, mecánica de Meta y efecto esperado sobre el rendimiento global.**
- **Formula cambios como hipótesis testeables**, no como órdenes absolutas.
- **Consulta primero recomendaciones oficiales de Meta si están disponibles**. Si discrepas, explícalo.
- **Desambigua clicks**: usa "Clicks (all)" o "Link Clicks"; nunca "clicks" a secas.
- **Audiencia**: usa "Accounts Center accounts" o solo el número; no digas "personas" al reportar reach/audience size.

## Nombres de métricas

Normaliza los nombres en todos los informes:

| Métrica cruda | Nombre en informe |
|---|---|
| `impressions` | Impressions |
| `video_thruplay_watched_actions` | ThruPlays |
| `clicks` | Clicks (all) |
| `purchase_roas` | Purchase ROAS |
| `cpm` | CPM |
| `cpc` | CPC (all) |
| `ctr` | CTR (all) |
| `cost_per_action_type:link_click` | CPC (Link Click) |
| `outbound_clicks_ctr` | Outbound CTR |
| `cost_per_action_type:purchase` | Cost per Purchase |
| `actions:purchase` | Purchases |
| `action_values:purchase` | Purchase Value |
| `frequency` | Frequency |
| `reach` | Reach (Accounts Center accounts) |
| `spend` | Amount Spent |

## Principios de análisis

- **Primero agregado, luego detalle**: Meta optimiza el conjunto, no cada desglose aislado.
- **Dinámico antes que estático**: analiza tendencias y ventanas de tiempo, no snapshots sueltos.
- **Marginal antes que promedio**: el sistema decide por el coste de la siguiente conversión probable, no solo por CPA medio histórico.
- **Aprendizaje importa**: cambios recientes, learning limited o bajo volumen invalidan conclusiones fuertes.

## Documentos de referencia

Carga desde `references/` según necesidad:

- `breakdown_effect.md` — leer primero si hay desgloses por edad, placement, país, creatividad o audiencia.
- `core_concepts.md` — subasta, pacing y aprendizaje.
- `learning_phase.md` — mecánica de fase de aprendizaje.
- `ad_relevance_diagnostics.md` — ranking de calidad, engagement y conversión.
- `auction_overlap.md` — solapamiento de subasta.
- `pacing.md` — distribución de presupuesto.
- `bid_strategies.md` — estrategias de puja.
- `ad_auctions.md` — cómo se decide la subasta.
- `performance_fluctuations.md` — variación normal vs señal preocupante.

## Workflow

### Paso 1 — Elegir nivel correcto

| Setup | Nivel correcto |
|---|---|
| Advantage+ Campaign Budget / CBO | Campaña |
| Placements automáticos sin CBO | Ad set |
| Varios anuncios dentro de un ad set | Ad set |

Explica el nivel elegido. Muchos errores de optimización vienen de evaluar un desglose como si fuera una unidad de decisión independiente.

### Paso 2 — Revisar fase de aprendizaje

Antes de diagnosticar:

- ¿El ad set sigue en learning?
- ¿Hubo ediciones recientes?
- ¿Hay volumen suficiente de eventos?

Si está en aprendizaje, marca las conclusiones como preliminares.

### Paso 3 — Analizar con lente Meta

Revisa:

1. **Eficiencia marginal**: tendencia temporal de CPA, no solo promedio.
2. **Ad relevance diagnostics**: calidad, engagement y conversion rate ranking.
3. **Auction overlap**: campañas o ad sets compitiendo entre sí.
4. **Pacing**: si Meta está reservando presupuesto para oportunidades mejores.
5. **Fluctuaciones**: 20-30% día a día puede ser normal; >50% sostenido requiere análisis.

### Paso 4 — Sintetizar con Breakdown Effect

Cuando haya desgloses, explica cómo puede aparecer una lectura engañosa:

> Un placement con CPA medio bajo puede estar agotando oportunidades baratas y subiendo en CPA marginal. Meta puede mover presupuesto a otro placement con CPA medio mayor si la siguiente conversión esperada es más barata.

### Paso 5 — Informe

Estructura:

1. **Resumen ejecutivo** — 2-3 hallazgos clave.
2. **Nivel de evaluación** — cuál y por qué.
3. **Fase de aprendizaje** — estado y caveats.
4. **Análisis de rendimiento** — métricas normalizadas.
5. **Diagnóstico** — causas raíz con evidencia.
6. **Recomendaciones** — hipótesis accionables, impacto esperado y cómo verificar.
7. **Notas de Breakdown Effect** — callouts explícitos donde aplique.

Skill original de Angel Aparicio (IA Masters Academy), adaptada para iamasters-os.
