---
name: load-excel
description: Load Excel files (.xlsx, .xls) into a pandas DataFrame. Handles multi-sheet workbooks, merged cells, empty rows, and common plate reader / BLI / Nanodrop layouts.
compatibility: pandas ≥1.5, openpyxl ≥3.0 (for .xlsx), xlrd ≥2.0 (for legacy .xls). Works offline.
instruments: Plate Reader (Agilent BioTek, Tecan Infinite), Octet/BLI (ForteBio, GATOR), Nanodrop, Cell Counter
---

# Load Excel

## When to use

File is `.xlsx` or `.xls`.
Instrument sources: Plate Reader, Octet/BLI binding kinetics exports, Nanodrop concentration tables, automated cell counters.

---

## Loading

```python
import pandas as pd

def load_excel(path: str, sheet_name=0) -> tuple[pd.DataFrame, dict]:
    try:
        xl = pd.ExcelFile(path)
        sheet_names = xl.sheet_names

        if len(sheet_names) > 1:
            # Multi-sheet: load the first by default, warn about others
            pass  # caller should be notified via warnings

        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            header=0,
            engine="openpyxl" if path.endswith(".xlsx") else "xlrd",
        )
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse Excel file — {e}")

    if df.empty:
        raise ValueError(f"LOAD ERROR: sheet '{sheet_name}' is empty in {path}")

    return df, {"parser": f"pandas.read_excel(sheet={sheet_name})", "all_sheets": sheet_names}
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Corrupt or unreadable | `fail` | `"LOAD ERROR: could not parse Excel file — {detail}"` |
| Selected sheet empty | `fail` | `"LOAD ERROR: sheet '{name}' is empty"` |
| Multiple sheets detected | `warn` | `"LOAD WARN: workbook has {n} sheets — loaded sheet '{name}'; others ignored"` |
| Merged cells detected | `warn` | `"LOAD WARN: merged cells detected — forward-filled during load"` |

---

## Profile fields populated

Same as `load-csv`: `format`, `shape`, `schema`, `missing`, `sample_stats`, `split_info`, `label_info`.

- `format`: `"excel"`

---

## Preprocessing defaults

1. **Drop fully empty rows and columns** — common in plate reader exports with decorative blank rows
2. **Forward-fill merged cells** — Excel merged cells read as NaN after first cell; `df.ffill()`
3. **Strip whitespace** from string columns and headers
4. **Detect well-plate layout** — if column names match `A1`–`H12` / `1`–`12` patterns, flag as 96-well plate layout and suggest melting with `pd.melt`
5. **Detect Octet/BLI layout** — if columns contain `Association`, `Dissociation`, `Baseline`, flag as binding kinetics time-series
6. **Coerce numeric columns** — `pd.to_numeric(errors='coerce')`
7. **Report all sheet names** — list in `warnings` if >1 sheet

---

## Output

```python
{
    "df": pd.DataFrame,
    "profile": {
        "format": "excel",
        "dataset_type": "tabular",
        ...   # conforms to dataset-profile-schema.md
        "loadability": { "status": "ok", "parser": "pandas.read_excel", "errors": [] },
        "warnings": ["workbook has 3 sheets — loaded 'Sheet1'; others ignored"]
    }
}
```

---

## Production constraints

- **Never** silently load all sheets — load sheet 0 and report others in `warnings`
- **Always** forward-fill merged cells and report it
- **Always** flag well-plate column layouts for potential melting
