---
name: load-jsonl
description: Load JSONL / NDJSON files into a pandas DataFrame. Flattens one level of nesting, infers types, and emits a tabular or text Dataset Profile.
compatibility: pandas ≥1.5. Works offline.
instruments: ML pipelines, HuggingFace dataset exports
---

# Load JSONL / NDJSON

## When to use

File is `.jsonl` or `.ndjson` — each line is a valid JSON object.
Common sources: HuggingFace dataset exports, ML pipeline outputs, annotation files.

---

## Loading

```python
import pandas as pd
import json

def load_jsonl(path: str) -> tuple[pd.DataFrame, dict]:
    try:
        df = pd.read_json(path, lines=True)
    except ValueError as e:
        # Fallback: parse line by line, skip malformed lines
        records, errors = [], []
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as je:
                    errors.append(f"line {i+1}: {je}")
        if not records:
            raise ValueError(f"LOAD ERROR: no valid JSON objects found in {path}")
        df = pd.DataFrame(records)
        if errors:
            # warn but continue
            pass

    return df, {"parser": "pandas.read_json(lines=True)", "parse_errors": errors if 'errors' in dir() else []}
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| No valid JSON lines | `fail` | `"LOAD ERROR: no valid JSON objects found in {path}"` |
| Some lines malformed | `warn` | `"LOAD WARN: {n} malformed lines skipped in {path}"` |
| All values are dicts/lists (deeply nested) | `warn` | `"LOAD WARN: deeply nested JSON — only top-level keys flattened"` |

---

## Profile fields populated

- `format`: `"jsonl"`
- `dataset_type`: `"tabular"` if values are short scalars; `"text"` if any string column has median length > 200 chars
- `shape`: `{ rows, cols }` after flattening
- `schema`: column names + inferred dtypes
- `missing`: null count + pct per column
- `sample_stats`: numeric columns only
- `label_info`: infer from `label`, `target`, `score`, `y`, `class`

---

## Preprocessing defaults

1. **Flatten one level** — for columns containing dicts, expand with `pd.json_normalize` prefix
2. **Explode list columns** — if a column contains lists of scalars, report and ask user whether to explode or stringify
3. **Lowercase and normalize column names** — strip, lowercase, replace spaces with `_`
4. **Coerce numeric strings** — `pd.to_numeric(errors='coerce')` for columns that look numeric
5. **Flag sequence column** — if a column contains strings matching protein/DNA alphabet (>80% amino acid chars), annotate as potential `bio-sequence` and suggest re-routing to `load-fasta` logic

---

## Output

```python
{
    "df": pd.DataFrame,
    "profile": {
        "format": "jsonl",
        "dataset_type": "tabular | text",
        ...   # conforms to dataset-profile-schema.md
    }
}
```

---

## Production constraints

- **Never** silently discard malformed lines — count them and report in `warnings`
- **Never** explode list columns without reporting the operation
- **Always** check for sequence-like columns and flag for bio-sequence re-routing
