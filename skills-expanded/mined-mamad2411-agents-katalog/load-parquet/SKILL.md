---
name: load-parquet
description: Load Parquet or Arrow files into a pandas DataFrame. Inspects schema, flattens struct columns, detects partitions, and emits a tabular Dataset Profile.
compatibility: pandas ≥1.5, pyarrow ≥10.0. Works offline.
instruments: HuggingFace dataset exports, ML pipeline outputs, large-scale tabular datasets
---

# Load Parquet / Arrow

## When to use

File is `.parquet` or `.arrow` — or magic bytes `PAR1` detected.
Sources: HuggingFace Hub dataset downloads, ML pipeline outputs, large biology tabular datasets.

---

## Loading

```python
import pandas as pd
import pyarrow.parquet as pq

def load_parquet(path: str) -> tuple[pd.DataFrame, dict]:
    try:
        pf = pq.ParquetFile(path)
        schema = pf.schema_arrow
        df = pf.read().to_pandas()
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse Parquet file — {e}")

    if df.empty:
        raise ValueError(f"LOAD ERROR: Parquet file loaded but is empty — {path}")

    return df, {
        "parser": "pyarrow.parquet",
        "arrow_schema": str(schema),
        "num_row_groups": pf.num_row_groups,
    }
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid Parquet | `fail` | `"LOAD ERROR: could not parse Parquet file — {detail}"` |
| Empty after load | `fail` | `"LOAD ERROR: Parquet file loaded but is empty"` |
| Struct/nested columns present | `warn` | `"LOAD WARN: {n} nested struct columns detected — may need flattening"` |
| List-type columns present | `warn` | `"LOAD WARN: {n} list-type columns detected — embeddings or token arrays?"` |

---

## Profile fields populated

- `format`: `"parquet"`
- `shape`, `schema`, `missing`, `sample_stats`, `split_info`, `label_info` — same as `load-csv`

---

## Preprocessing defaults

1. **Inspect Arrow schema** — report column names, types, and nullable flags from schema before loading
2. **Flatten top-level structs** — use `pd.json_normalize` on struct columns; report which were flattened
3. **Flag list/array columns** — could be embeddings (fixed-length) or token arrays (variable); report shape
4. **Detect partition columns** — if file is part of a Hive-partitioned dataset, report partition keys
5. **Detect embedding columns** — if a list column has fixed length ≥64, flag as potential embedding vector (sequence representation)
6. **Coerce numeric string columns** — same as `load-csv`

---

## Output

```python
{
    "df": pd.DataFrame,
    "profile": {
        "format": "parquet",
        "dataset_type": "tabular",
        ...
        "loadability": { "status": "ok", "parser": "pyarrow.parquet", "errors": [] },
        "warnings": [...]
    }
}
```

---

## Production constraints

- **Always** report Arrow schema before flattening — never lose type information silently
- **Always** flag fixed-length list columns as potential embeddings
- **Never** flatten nested columns without reporting the operation
