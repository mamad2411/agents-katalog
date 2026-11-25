---
name: riskmodels-smart-subheader
description: >
  Generates precise, professional subheader commentary for every Plotly chart
  in R1 snapshots and the visuals gallery. Forces reference to exact time range,
  data_as_of, and lineage. Never hallucinates numbers.
---

# RiskModels Smart Subheader Generator

When building or refining any chart in `sdk/riskmodels/snapshots/` or `sdk/riskmodels/visuals/`
(R1 profile, waterfall, hedge cascade, etc.), generate the **subheader** (the italic explanatory
sentence(s) under each section title) using the `smart_subheader` module.

## Module Location

```
sdk/riskmodels/visuals/smart_subheader.py
```

## Usage

```python
from riskmodels.visuals.smart_subheader import generate_subheader

text = generate_subheader(
    chart_type="er_attribution",       # or "hr_cascade", "peer_table", etc.
    title="L3 Explained-Return Attribution",
    data=metrics_dict,                 # the raw metrics powering the chart
    data_as_of="2026-04-04",           # from RiskLineage.data_as_of
    time_range="past 252 trading days",
    ticker="NVDA",
    benchmark="SOXX",
    use_llm=False,                     # True to enable LLM enhancement
)
```

## Supported Chart Types

| chart_type       | Used by         | Description                              |
|:-----------------|:----------------|:-----------------------------------------|
| `er_attribution` | R1 Panel I      | L3 ER decomposition horizontal bar       |
| `hr_cascade`     | R1 Panel II     | Hedge-ratio cascade grouped bar          |
| `peer_table`     | R1 Panel III    | Peer comparison table                    |
| `waterfall`      | S2, future R3   | Return attribution waterfall             |
| `histogram`      | Future R2/P2    | Cross-sectional distribution             |
| `multi_line`     | Future R2/P2    | Time series overlay                      |
| `stacked_area`   | Future R4       | Factor contribution stacked area         |

## Strict Rules

1. **Always mention the exact time range** (e.g. "over the past 252 trading days ending 2026-04-04")
2. **Always include data_as_of** from lineage
3. **Use only real numbers** from the data dict — never round, estimate, or hallucinate
4. **Never say "outperformance by X%"** without the exact period
5. **Max 2 short sentences**, institutional tone (think Bloomberg PORT commentary)
6. **Rule-based mode is the default** — no LLM dependency for rendering

## LLM Enhancement (Optional)

Set `use_llm=True` to get more nuanced phrasing via OpenAI. Requires:
- `openai` package installed
- `OPENAI_API_KEY` environment variable set

Falls back to rule-based output on any failure (network, auth, timeout).

## LLM Prompt Template

When LLM mode is active, the generator uses this exact prompt:

```
You are a senior quantitative risk analyst at BW Macro.

Generate a single professional subheader (1-2 short sentences) for this chart.

Chart type: {chart_type}
Title: {title}
Ticker: {ticker}
Benchmark: {benchmark}
Data as of: {data_as_of}
Time range: {time_range}
Key metrics: {key_facts_json}

Rules:
- MUST reference the exact time range and data_as_of date
- Use ONLY the real numbers provided above
- Institutional, factual, insightful tone
- Max 2 short sentences
Output ONLY the subheader text.
```
