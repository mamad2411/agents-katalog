---
name: load-fcs
description: Load Flow Cytometry Standard (.fcs) files into a pandas DataFrame using fcsparser. Extracts channel measurements, applies compensation matrix if present, and emits a flow-cytometry Dataset Profile.
compatibility: fcsparser ≥0.2.4, pandas ≥1.5. Works offline.
instruments: Flow Cytometry Analyzer/Sorter — BD LSRFortessa, Cytek Aurora, CytoFLEX, Sony ID7000C, BD FACSAria, Sony MA900
---

# Load FCS (Flow Cytometry Standard)

## When to use

File is `.fcs` — per-cell fluorescence and scatter measurement from a flow cytometer or cell sorter.
Sources: BD, Cytek, Sony, Beckman Coulter instruments. Analyzed further in FlowJo, R (flowCore), or Python.

---

## Loading

```python
import fcsparser
import pandas as pd

def load_fcs(path: str) -> tuple[pd.DataFrame, dict]:
    try:
        meta, df = fcsparser.parse(path, reformat_meta=True)
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse FCS file — {e}")

    if df.empty:
        raise ValueError(f"LOAD ERROR: no events found in FCS file — {path}")

    return df, {
        "parser": "fcsparser",
        "fcs_version": meta.get("FCS version", "unknown"),
        "cytometer": meta.get("$CYT", "unknown"),
        "num_parameters": meta.get("$PAR", "unknown"),
        "num_events": meta.get("$TOT", len(df)),
        "has_compensation": "$COMP" in meta or "SPILL" in meta,
    }
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid FCS format | `fail` | `"LOAD ERROR: could not parse FCS file — {detail}"` |
| Zero events | `fail` | `"LOAD ERROR: no events found in FCS file — {path}"` |
| No compensation matrix | `warn` | `"LOAD WARN: no compensation matrix in FCS file — fluorescence channels may be uncorrected"` |
| FCS version < 3.0 | `warn` | `"LOAD WARN: FCS version {v} — older format, some metadata fields may be missing"` |

---

## Profile fields populated

- `format`: `"fcs"`
- `dataset_type`: `"flow-cytometry"`
- `shape`: `{ rows: N_events, cols: N_channels }`
- `schema`: channel names + dtypes (FSC-A, SSC-A, FITC-A, PE-A, etc.)
- `sample_stats`: min/median/mean/max/std per channel
- `missing`: null counts (FCS rarely has nulls — flag if any)

---

## Preprocessing defaults

1. **Extract channel names** from FCS metadata (`$PnN`, `$PnS` parameters)
2. **Apply compensation matrix** if `SPILL` or `$COMP` key present in metadata — `fcsparser` does not apply automatically
3. **Log-transform fluorescence channels** — apply `arcsinh(x / 5)` (cofactor=5 standard for flow) for visualization-ready data; report transformation
4. **Leave scatter channels raw** — FSC, SSC should not be log-transformed
5. **Flag negative values** — common after compensation; report pct negative per channel
6. **Report event count** and note if gated population or full ungated export

---

## Output

```python
{
    "df": pd.DataFrame,   # columns: FSC-A, SSC-A, FITC-A, PE-A, ... (per-cell events)
    "profile": {
        "format": "fcs",
        "dataset_type": "flow-cytometry",
        "shape": { "rows": N_events, "cols": N_channels },
        "schema": [...],
        "sample_stats": {...},
        "loadability": { "status": "ok", "parser": "fcsparser", "errors": [] },
        "warnings": [...]
    }
}
```

---

## Production constraints

- **Never** apply compensation or log-transform without reporting in `warnings`
- **Always** report whether a compensation matrix was found
- **Always** distinguish scatter (FSC/SSC) from fluorescence channels in `schema`
