---
name: analyze
description: "Full agentic analysis pipeline — ingest, clean, analyze, visualize, report, and dashboard from any data"
argument-hint: "[dataset-name] [optional-question]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Agent
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# 10x Analyst — Full Analysis Pipeline

Run the complete 5-agent analysis pipeline on any CSV, Excel, or JSON dataset.

## Overview

This command orchestrates all 5 specialist agents in sequence: Data Engineer (ingest/clean) → Statistician (EDA/stats) → Visualizer (charts/dashboard) → Reporter (Markdown report) → Strategist (business recommendations). Reads from `input/<dataset>/`, writes everything to `output/<dataset>/`.

## When to Use

- User provides data files and wants a complete analysis with report and dashboard
- User says "analyze this data", "give me insights", or "what does this data tell us"
- User points to a dataset folder and wants the full treatment

## Path Resolution

Parse `$ARGUMENTS` to get the dataset name (e.g., `shopify-data`).
- **Input path:** `input/<dataset-name>/` — where data files are read from
- **Output path:** `output/<dataset-name>/` — where all artifacts are written
- All paths are relative to the `10x-analyst/` plugin root directory

Example: `/10x-analyst:analyze shopify-data` reads from `input/shopify-data/` and writes to `output/shopify-data/`.

## Instructions

Follow these phases **exactly in order**. Each phase produces files that the next phase depends on.

### PHASE 1 — Data Engineering

**Goal:** Load, profile, and clean all data files.

1. Resolve paths from `$ARGUMENTS`:
   ```python
   dataset_name = "$ARGUMENTS".split()[0].strip("/")  # e.g. "shopify-data"
   input_dir = f"input/{dataset_name}"
   output_dir = f"output/{dataset_name}"
   ```
2. Find all data files at `input/<dataset>/` using Glob:
   - Patterns: `input/<dataset>/**/*.csv`, `input/<dataset>/**/*.xlsx`, `input/<dataset>/**/*.xls`, `input/<dataset>/**/*.json`
3. Create output directories:
   ```bash
   mkdir -p output/<dataset>/charts output/<dataset>/cleaned-data
   ```
4. For each file, run this Python profiling script:
   ```python
   import pandas as pd
   import json
   import os

   def profile_file(filepath):
       ext = os.path.splitext(filepath)[1].lower()
       if ext == '.csv':
           df = pd.read_csv(filepath)
       elif ext in ['.xlsx', '.xls']:
           df = pd.read_excel(filepath)
       elif ext == '.json':
           df = pd.read_json(filepath)
       else:
           return None

       profile = {
           'file': os.path.basename(filepath),
           'rows': len(df),
           'columns': len(df.columns),
           'column_names': list(df.columns),
           'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
           'missing': {col: int(df[col].isna().sum()) for col in df.columns},
           'missing_pct': {col: round(df[col].isna().mean() * 100, 1) for col in df.columns},
           'duplicates': int(df.duplicated().sum()),
           'numeric_stats': {}
       }
       for col in df.select_dtypes(include='number').columns:
           profile['numeric_stats'][col] = {
               'min': float(df[col].min()) if not df[col].isna().all() else None,
               'max': float(df[col].max()) if not df[col].isna().all() else None,
               'mean': round(float(df[col].mean()), 2) if not df[col].isna().all() else None,
               'median': round(float(df[col].median()), 2) if not df[col].isna().all() else None,
               'std': round(float(df[col].std()), 2) if not df[col].isna().all() else None
           }
       return profile
   ```
5. Write data profile to `output/<dataset>/data-profile.md`
6. Clean each file:
   - Parse date columns with `pd.to_datetime(errors='coerce')`
   - Strip `$` and `,` from currency columns, convert to float
   - Standardize column names: `df.columns = df.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True)`
   - Drop exact duplicates: `df.drop_duplicates(inplace=True)`
   - Save cleaned files to `output/<dataset>/cleaned-data/`
7. Present data inventory table to the user

### PHASE 2 — Statistical Analysis

**Goal:** Compute all metrics, KPIs, segments, and insights.

8. Load cleaned data from `output/<dataset>/cleaned-data/`
9. Join related tables if multiple files present (match on common column names like `id`, `customer_id`, `order_id`, `product_id`)
10. Detect data domain:
    - If columns contain `order`, `revenue`, `price`, `product`, `customer` → **E-Commerce**
    - Otherwise → **General Tabular**
11. Run domain-specific analysis:

**E-Commerce:**
```python
# Revenue over time
revenue_by_month = df.groupby(pd.Grouper(key='date_col', freq='M'))['revenue_col'].sum()

# Top products
top_products = df.groupby('product_col')['revenue_col'].sum().nlargest(10)

# AOV
aov = df.groupby('order_id_col')['revenue_col'].sum().mean()

# RFM Segmentation
rfm = df.groupby('customer_id_col').agg(
    recency=('date_col', lambda x: (df['date_col'].max() - x.max()).days),
    frequency=('order_id_col', 'nunique'),
    monetary=('revenue_col', 'sum')
)
```

**General Tabular:**
```python
# Correlation matrix
corr = df.select_dtypes(include='number').corr()

# Distribution stats
desc = df.describe(include='all')

# Top categories
for col in df.select_dtypes(include='object').columns:
    value_counts = df[col].value_counts().head(10)
```

12. Save structured insights to `output/<dataset>/insights.json`:
```json
[
  {
    "id": "insight-001",
    "headline": "Revenue grew 23% month-over-month",
    "category": "revenue",
    "value": 45230.50,
    "change_pct": 23.0,
    "implication": "Growth is accelerating"
  }
]
```

### PHASE 3 — Visualization

**Goal:** Generate charts and interactive dashboard.

13. Read `output/<dataset>/insights.json` and cleaned data
14. Generate PNG charts using matplotlib/seaborn:
```python
import matplotlib.pyplot as plt
import seaborn as sns

COLORS = ['#FF6B35', '#004E89', '#00A878', '#FFD166', '#EF476F', '#118AB2', '#073B4C']
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette(COLORS)
plt.rcParams.update({'figure.figsize': (12, 6), 'figure.dpi': 150, 'font.size': 11})

# Save each chart to output/<dataset>/charts/
plt.savefig('output/<dataset>/charts/chart_name.png', bbox_inches='tight')
plt.close()
```

15. Generate charts based on insight types:
    - Trend → line chart
    - Top-N → horizontal bar chart
    - Proportion → donut chart
    - Correlation → heatmap
    - Distribution → histogram

16. Build `output/<dataset>/dashboard.html`:
    - Standalone HTML with Chart.js from CDN
    - KPI cards row at top
    - 2x2 chart grid (trend, top-N, segments, heatmap)
    - Data table section
    - 10x.in branding and responsive CSS
    - All data embedded as inline `const data = {...}` JavaScript

### PHASE 4 — Report

**Goal:** Compile everything into a Markdown report.

17. Read all artifacts: `data-profile.md`, `insights.json`, chart file list from `output/<dataset>/charts/`
18. Write `output/<dataset>/report.md` with:
    - Executive Summary (top 3-5 bullet points)
    - Data Overview (files, rows, quality)
    - Key Findings (each with chart embed and implication)
    - Detailed Analysis sections
    - Methodology
    - Appendix with full stats

### PHASE 5 — Strategy

**Goal:** Add business recommendations and executive brief.

19. Read `insights.json` and draft report
20. Prioritize insights: P0 (critical) → P3 (low)
21. Generate actionable recommendations with expected impact
22. Append to report: Recommendations section and Executive Brief
23. Present final summary to user:
    - List all files created in `output/<dataset>/`
    - Top 3 insights
    - How to open the dashboard: `start output/<dataset>/dashboard.html`
    - Suggested follow-up analyses

## Examples

```bash
# Full Shopify dataset analysis (reads input/shopify-data/, writes output/shopify-data/)
/10x-analyst:analyze shopify-data

# Analysis with a specific question
/10x-analyst:analyze shopify-data "Which customer segments are most profitable?"
```

## Best Practices

- Place your data folder inside `input/` before running (e.g., `input/my-sales-data/`)
- Run `:profile` first if you want to inspect data quality before committing to the full pipeline
- For large datasets (>100K rows), the pipeline samples for visualization but uses full data for statistics
- Each phase is independent — if Phase 3 fails, Phases 1-2 outputs are still valid in `output/<dataset>/`
- The dashboard works offline once generated (Chart.js is the only CDN dependency)

## Limitations

- Max recommended file size: 500MB per file (pandas memory constraint)
- Excel files with macros/formulas may not load — export to CSV first
- Chart.js CDN required for dashboard interactivity
- RFM segmentation uses quartile thresholds — not custom scoring
- The pipeline generates static outputs, not live-updating dashboards

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
