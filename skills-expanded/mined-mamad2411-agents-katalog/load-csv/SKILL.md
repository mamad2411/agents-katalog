---
name: load-csv
description: Load CSV or TSV files into a pandas DataFrame. Handles encoding, delimiter detection, type coercion, and missing values. Emits a tabular Dataset Profile.
compatibility: pandas ≥1.5. Works offline.
instruments: Plate Reader (Agilent BioTek, Tecan), Octet/BLI, Nanodrop, Cell Counter
---

# Load CSV / TSV

## When to use

File is `.csv`, `.tsv`, or `.tab` — or content sniff shows a consistent delimiter with a header row.
Instrument sources: Plate Reader, Octet/BLI, Nanodrop, Automated Cell Counter.

---

## Loading

```python
import pandas as pd

def load_csv(path: str) -> tuple[pd.DataFrame, dict]:
    # 1. Try UTF-8, fall back to latin-1
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                engine="python",
                skip_blank_lines=True,
            )
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"LOAD ERROR: could not decode {path} with utf-8 / latin-1 / cp1252")

    return df, {"parser": "pandas.read_csv", "encoding": enc}
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| All encodings fail | `fail` | `"LOAD ERROR: could not decode {path} with utf-8 / latin-1 / cp1252"` |
| Zero rows after load | `warn` | `"LOAD WARN: file loaded but contains 0 data rows — {path}"` |
| No header detected | `warn` | `"LOAD WARN: no header row detected — column names set to positional indices"` |

---

## Profile fields populated

- `format`: `"csv"` or `"tsv"`
- `shape`: `{ rows, cols }`
- `schema`: column names + inferred dtypes + nullable flag
- `missing`: null count + pct per column
- `sample_stats`: min/median/mean/max/std for each numeric column
- `split_info`: check for column named `split`, `fold`, `set`, `partition`
- `label_info`: infer from column named `label`, `target`, `y`, `class`, `score`

---

## Preprocessing defaults

Apply in this order after loading:

1. **Strip whitespace** — strip leading/trailing spaces from all string columns and column names
2. **Lowercase column names** — `df.columns = df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)`
3. **Drop fully empty rows and columns** — `df.dropna(how='all')`
4. **Coerce numeric columns** — `pd.to_numeric(df[col], errors='coerce')` for columns that look numeric (>80% parseable)
5. **Flag duplicates** — report count of exact duplicate rows; do not drop silently
6. **Detect constant columns** — report columns with a single unique value as potential metadata
7. **Plate Reader specifics** — if column names match `A1`–`H12` pattern, flag as well-plate layout and suggest transposing or melting

---

## Output

```python
{
    "df": pd.DataFrame,          # loaded, whitespace-stripped, dtypes coerced
    "profile": {                 # conforms to dataset-profile-schema.md
        "format": "csv",
        "dataset_type": "tabular",
        "shape": { "rows": ..., "cols": ... },
        "schema": [...],
        "missing": {...},
        "sample_stats": {...},
        "split_info": {...},
        "label_info": {...},
        "loadability": { "status": "ok", "parser": "pandas.read_csv", "errors": [] },
        "warnings": [...]
    }
}
```

---

## Production constraints

- **Never** drop rows silently — report counts in `warnings`
- **Never** infer target column from position alone — require a name match
- **Always** try all three encodings before failing
- **Always** report delimiter used in `loadability.parser` (e.g. `"pandas.read_csv(sep=',')"`)
