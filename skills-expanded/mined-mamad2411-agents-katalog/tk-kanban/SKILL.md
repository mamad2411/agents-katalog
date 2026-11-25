---
name: tk-kanban
description: Build a portable static HTML dashboard from cross-border e-commerce CSV or XLSX exports by inspecting and normalizing product data, computing transparent metrics and opportunity indicators, adding evidence-based agent insights, and rendering the bundled offline template. Use when an agent needs to create or refresh a TikTok Shop, FastMoss, Amazon, Shopee, or similar product dashboard; adapt changed export columns; diagnose an unreadable table; compare available product performance; or replace a Streamlit dashboard with directly shareable web files.
---

# TK Kanban

Generate a complete cross-border e-commerce dashboard. Treat table adaptation as an internal step; the default deliverable is a validated static webpage.

## Core workflow

1. Locate the requested CSV/XLSX file. When the user supplies a directory, select the newest supported source file case-insensitively and exclude generated outputs.
2. Run `scripts/inspect_source.py` and review its JSON result. Do not continue when `status` is `blocked`.
3. Run `scripts/normalize_products.py`. Preserve the source file and write a new normalized CSV.
4. Run `scripts/build_dashboard_metrics.py` to create `dashboard-model.json`.
5. Read `dashboard-model.json`, then write a concise `insights.json` that follows `references/dashboard-contract.md` and `references/analysis-guidelines.md`.
6. Run `scripts/render_dashboard.py` with the model and insights. Always render the bundled static HTML template unless the user explicitly requests another output format.
7. Run `scripts/validate_dashboard.py`. If validation fails, repair the bundled template or scripts and re-render the dashboard.
8. Return a link to the generated `index.html` and summarize the strongest evidence, data limitations, and files created.

## Command pattern

Use the active Python interpreter. Pass explicit paths; do not rely on the current working directory.

```text
python scripts/inspect_source.py INPUT --output INSPECTION_JSON
python scripts/normalize_products.py INPUT --output NORMALIZED_CSV --report NORMALIZATION_JSON
python scripts/build_dashboard_metrics.py NORMALIZED_CSV --output DASHBOARD_MODEL_JSON
python scripts/render_dashboard.py --model DASHBOARD_MODEL_JSON --insights INSIGHTS_JSON --output-dir DASHBOARD_DIR
python scripts/validate_dashboard.py DASHBOARD_DIR
```

All scripts emit machine-readable JSON to stdout. Treat a nonzero exit code as a failed stage.

## Agent analysis

Generate insights with the current agent by default. If subagents are available and the dataset or comparison is complex, delegate only the interpretive analysis stage:

- Give the subagent `dashboard-model.json`, `references/analysis-guidelines.md`, and the user's decision goal.
- Ask for an `insights.json` matching the documented contract.
- Do not provide expected conclusions.
- Validate every returned claim against the model before rendering.
- Continue locally when subagents are unavailable.

Never call DeepSeek, OpenAI, or another model API from bundled scripts. The executing agent supplies the reasoning layer.

## Progressive references

- Read `references/dashboard-contract.md` before creating or repairing `insights.json` or changing dashboard sections.
- Read `references/analysis-guidelines.md` before writing business conclusions or delegating analysis.
- Read `references/opportunity-score.md` when explaining, changing, or auditing the opportunity ranking.
- Read `references/fastmoss-format.md` only for FastMoss/TikTok exports, column-mapping failures, encoding issues, or unexpected blank columns.
- Read `references/historical-comparison.md` only when two or more dated snapshots are available and the user requests trend analysis.

## Safety and quality rules

- Never overwrite a source spreadsheet.
- Never patch generated dashboard files (`index.html`, `app.js`, or `styles.css`) to make validation pass. Fix the bundled source template and re-render. If the installed skill is not writable, stop and report the package defect.
- Preserve product IDs as strings; never convert them through floating point.
- Do not invent missing metrics, causal explanations, market-wide claims, or historical trends.
- Label deterministic ranking as `机会指数`, not `AI评分`.
- Surface missing fields and data-quality limitations in the dashboard.
- Do not expose API keys, tokens, credentials, or unrelated local files.
- Keep the final dashboard offline-capable: no CDN, remote script, package installation, `fetch()` call, or running server.
- Use UTF-8 for JSON/HTML and UTF-8 with BOM for generated CSV files.

## Output contract

Produce a dashboard directory containing:

```text
dashboard/
├── index.html
├── app.js
└── styles.css
```

The renderer embeds the dashboard JSON inside `index.html`, so opening the file directly must work. Keep intermediate inspection, normalized CSV, model, and insight files beside the dashboard or in a clearly named work directory.
