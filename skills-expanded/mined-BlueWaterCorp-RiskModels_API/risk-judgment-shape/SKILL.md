---
name: risk-judgment-shape
description: >-
  Boundary spec for the Risk Interpretation Engine. Use when adding
  qualifier wording, headline copy, residual-quality phrases, peer-rank
  language, or any "is this stock good/bad?" judgment to RiskModels_API
  code. Editorial vocabulary lives in BWMACRO; this repo only exposes
  the public Judgment shape and a bland numeric stub.
---

# Risk Judgment — public boundary

## What this skill protects

The bwmacro/RiskModels stack centralizes *risk interpretation* (turning
raw ERM3 outputs into qualified, PM-readable language) into a single
engine that lives **privately** in BWMACRO. RiskModels_API is the
public layer — data, math, chart primitives — and must not contain the
editorial vocabulary that the engine produces.

If you are about to write a string like:

- `"Strong Residual Alpha"`, `"Solid Residual Quality"`, `"Muted"`, …
- `"performance is beta-driven"`, `"returns are driven by idiosyncratic exposure"`, …
- `"ranks near the top of the cohort"`, `"sits near the cohort median"`, …
- `"High Systematic Exposure"`, `"Underperforming SMH"`, …

… STOP. That is editorial vocabulary. It belongs in BWMACRO, not here.

## When this skill applies

- Any change to a snapshot renderer (`sdk/riskmodels/snapshots/*.py`).
- Any change to API route handlers under `app/api/` that surface
  natural-language descriptions of risk.
- Any change to MCP tools that return "interpreted" output.
- Any new feature that classifies a stock or portfolio into a state
  (driver = systematic / balanced / idiosyncratic, quality = strong /
  solid / muted, etc.).

## The contract — public side (this repo)

The single public surface for interpretation in this repo is
[`sdk/riskmodels/interpretation.py`](../../../sdk/riskmodels/interpretation.py).
It exports:

| Symbol | Purpose |
|---|---|
| `Judgment` | Frozen dataclass — the contract every consumer reads. Fields: `version`, `as_of`, `ticker`, `features`, `text`, `states`, `flags`. |
| `INTERPRETER_VERSION` | Schema version. Bumped when the public feature dictionary changes shape. |
| `compute_features(data) -> dict` | Pure numeric extraction from a `DDData`. No qualifiers, no thresholds. Both the bland stub and the BWMACRO engine consume this. |
| `derive_default_judgment(data) -> Judgment` | Bland public stub. `text` fields are raw numerics only ("AAPL — systematic 39%, residual +1.9%, peer rank 78") — no qualifiers, no editorial. |

Snapshot render entry points accept an optional `judgment` parameter:

```python
def render_dd_to_pdf(data, output_path, *, judgment: Judgment | None = None): ...
def render_dd_to_png(data, output_path, *, judgment: Judgment | None = None): ...
def render_dd_to_png_bytes(data, *, judgment: Judgment | None = None): ...
```

When `judgment is None`, the legacy in-SDK editorial generator runs
(temporarily, until Phase 1B replaces it with a BWMACRO call site).
When provided, the renderer reads `judgment.text` for headline + insight
strings.

## The contract — private side (BWMACRO)

The editorial engine lives at:

```
BWMACRO/bwmacro/risk_interpretation/
  ├── dd.py              # derive_judgment(data) for DD snapshots
  ├── states.py          # threshold tables → discrete states
  ├── flags.py           # predicate flags
  ├── renderers.py       # qualifier vocabulary + PM phrasing
  └── tests/             # eval cases
```

It imports `Judgment`, `compute_features`, and `INTERPRETER_VERSION`
from `riskmodels.interpretation` and produces a fully-populated
`Judgment` (with `states`, `flags`, and editorial `text`) that the API
route layer injects into `render_dd_to_*` calls.

## Rules (non-negotiable)

1. **No qualifier vocabulary in this repo.** "Strong", "Solid",
   "Muted", "beta-driven", "ranks above the median" — all of those go
   to BWMACRO.

2. **No threshold tables in this repo.** If you find yourself writing
   `if residual_share > 0.5:` to decide on language, that logic
   belongs in `BWMACRO/bwmacro/risk_interpretation/states.py`.

3. **No flag predicates in this repo.** "high_residual_negative",
   "industry_tailwind", etc. live in BWMACRO.

4. **`compute_features` is the canonical feature extractor.** Do not
   re-implement feature extraction inside snapshot renderers. Call
   `compute_features(data)` and read from the returned dict.

5. **`Judgment` is the canonical interpretation object.** API
   responses, chat agents, snapshot renderers — all consume the same
   shape. Do not invent parallel structures.

6. **Color = identity, sign = pattern.** A negative residual is
   green-with-stripes, not red. (See the v9 waterfall fix for context.)

## Migration phases (current state: Phase 1A landed)

- **Phase 1A** (✅ landed): `Judgment` shape, `compute_features`, bland
  stub, render-entry-point seam. Behavior preserved when `judgment=None`
  via the legacy `_generate_dd_insights` function in
  `sdk/riskmodels/snapshots/stock_deep_dive.py`.

- **Phase 1B** (BWMACRO PR, blocked on 1A): port the body of
  `_generate_dd_insights` to `bwmacro/risk_interpretation/dd.py`. Add
  the engine-owner SKILL in BWMACRO. Wire API route handlers to call
  BWMACRO and inject the result.

- **Phase 1C** (BWMACRO PR, blocked on 1B): Dagster job — monthly
  full-deployment render of top-N tickers, push to GCS at
  `gs://rm_api_data/snapshots/dd/{YYYY-MM}/{ticker}.pdf`. API serves
  from GCS with on-demand fallback for tickers not in the latest batch.

- **Phase 2** (RiskModels_API, after 1B): flip the `judgment=None`
  default path to call `derive_default_judgment` (the bland stub)
  instead of `_generate_dd_insights`. Delete the legacy function. SDK
  community gets bland numeric output; BWMACRO callers get the rich
  editorial version.

## No mock data — paired rule

When real data is missing for a chart panel, API response, or chat
output: look in `Funds_DAG/data/sync/funds/*.json`, the per-fund
`ds_*.zarr` stores, and the RiskModels SDK / API endpoints (use
`riskmodels-api-discovery` first). If the fetcher genuinely isn't
wired yet, render an explicit "data unavailable" placeholder and
add a backlog entry. Do not synthesize plausible values — even with
a watermark; screenshots crop watermarks. Cross-repo full directive:
[`BWMACRO/.cursor/skills/no-mock-data/SKILL.md`](../../../BWMACRO/.cursor/skills/no-mock-data/SKILL.md).

## Tracking

The MASTER_BACKLOG entry for this initiative is at
`BWMACRO/docs/ceo/MASTER_BACKLOG.md` under
"Risk Interpretation Engine".

## Sister boundary — Snapshot composition (PR 3, 2026-05)

A second cross-repo split governs which **snapshot layouts** ship public
vs private. Same shape as the interpretation boundary above, different axis:

| Public (this repo) | Private (BWMACRO) |
|---|---|
| `riskmodels.snapshots.canonical.CanonicalStockSnapshot` — semantic schema | `bwmacro.snapshots.stock.r1_risk_profile` |
| `riskmodels.snapshots.canonical.from_components(p1, peer_comparison=…)` | `bwmacro.snapshots.stock.p1_stock_performance` |
| `riskmodels.snapshots.canonical.from_dd_data(dd)` (structurally typed) | `bwmacro.snapshots.stock.stock_deep_dive` (DDData class) |
| `riskmodels.snapshots.reference_renderer` — clean, less-opinionated PDF/PNG | `bwmacro.snapshots.stock.{s1_forensic,s2_waterfall,product_tear_sheet}` |
| `riskmodels.snapshots._stock_data.P1Data` — data dataclass | All curated layout / chart composition for the institutional 1-page PDFs |
| `riskmodels.visuals.{cascade,l3_decomposition,waterfall,components}` | `riskmodels.visuals._mag7`, `gallery`, `mag7_l3_*`, `smart_subheader` |

**Hard rule:** the `rm_api_public` GCS bucket pipeline (`bulk_dd_render.py`
+ `app/api/snapshot/[ticker]`) **never imports `bwmacro.*`**. It must stay
self-sufficient on the public canonical pipeline. User confirmed this directly
during PR 2 and PR 3.

If you need to add a new institutional renderer, put it in BWMACRO and
write an adapter in `bwmacro/snapshots/stock/adapters.py` that maps the
private data class onto `CanonicalStockSnapshot` via
`riskmodels.snapshots.canonical.from_components`.
