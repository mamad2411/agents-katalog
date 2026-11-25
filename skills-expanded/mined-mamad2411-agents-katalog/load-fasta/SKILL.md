---
name: load-fasta
description: Load FASTA files into a pandas DataFrame using BioPython. Detects sequence alphabet and emits dataset_type as protein_sequence or nucleotide_sequence. Computes length stats and ESM2 compatibility flags.
compatibility: biopython ≥1.80, pandas ≥1.5. Works offline.
instruments: Sequencer (NGS), UniProt exports, reference databases
---

# Load FASTA

## When to use

File is `.fasta`, `.fa`, `.faa`, `.fna` — or first line starts with `>`.
Sources: NGS assemblers, UniProt/NCBI exports, reference proteomes, designed sequences.

---

## Loading

```python
from Bio import SeqIO
import pandas as pd

def load_fasta(path: str) -> tuple[pd.DataFrame, dict]:
    records = []
    try:
        for rec in SeqIO.parse(path, "fasta"):
            records.append({
                "seq_id":   rec.id,
                "header":   rec.description,
                "sequence": str(rec.seq).upper().strip(),
                "length":   len(rec.seq),
            })
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse FASTA — {e}")

    if not records:
        raise ValueError(f"LOAD ERROR: no sequences found in {path}")

    df = pd.DataFrame(records)
    alphabet = _detect_alphabet(df["sequence"].tolist())
    dataset_type = "protein_sequence" if alphabet == "protein" else "nucleotide_sequence"

    return df, {
        "parser": "biopython.SeqIO(fasta)",
        "alphabet": alphabet,
        "dataset_type": dataset_type,
    }


PROTEIN_CHARS = set("ACDEFGHIKLMNPQRSTVWYBZXUO*-")
NUCLEOTIDE_CHARS = set("ACGTURYSWKMBDHVN-")

def _detect_alphabet(sequences: list[str]) -> str:
    sample = "".join(sequences[:200]).upper()
    total = len(sample)
    if total == 0:
        return "unknown"
    pct_aa = sum(1 for c in sample if c in PROTEIN_CHARS) / total
    pct_nt = sum(1 for c in sample if c in NUCLEOTIDE_CHARS) / total
    if pct_aa > 0.90 and pct_nt < 0.70:
        return "protein"
    elif pct_nt > 0.90:
        return "dna"
    else:
        return "mixed"
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid FASTA format | `fail` | `"LOAD ERROR: could not parse FASTA — {detail}"` |
| Zero sequences | `fail` | `"LOAD ERROR: no sequences found in {path}"` |
| Duplicate IDs present | `warn` | `"LOAD WARN: {n} duplicate seq_id values detected"` |
| Non-standard characters found | `warn` | `"LOAD WARN: non-standard characters in sequences — {chars}"` |
| Alphabet is `mixed` | `warn` | `"LOAD WARN: mixed alphabet detected — verify sequence type before PLM use"` |

---

## Profile fields populated

- `format`: `"fasta"`
- `dataset_type`: `"protein_sequence"` or `"nucleotide_sequence"` (determined by alphabet)
- `shape`: `{ sequences: N }`
- `schema`: `[{name: seq_id}, {name: sequence}, {name: length}]`
- `sequence_stats`: `length_min`, `length_median`, `length_max`, `read_type`, `is_plm_ready`, `pct_over_512`, `pct_over_1024`
- `missing`: null counts for `seq_id` and `sequence`

---

## Preprocessing defaults

1. **Uppercase all sequences** — `seq.upper()`
2. **Strip whitespace and line breaks** from sequence strings
3. **Detect alphabet** — runs `_detect_alphabet()` on first 200 sequences; sets `dataset_type` and `read_type`
4. **Set `is_plm_ready`** — `true` if `protein_sequence`, `false` if `nucleotide_sequence`
5. **Remove gap characters** (`-`, `.`) only if explicitly instructed; otherwise flag and report count
6. **Flag non-standard chars** — any char outside standard alphabet → list in `warnings`
7. **Deduplicate check** — report duplicate `seq_id` count; do not drop silently
8. **Compute ESM2 length flags** — `pct_over_512`, `pct_over_1024` (only meaningful for `protein_sequence`)

---

## Output

```python
{
    "df": pd.DataFrame,   # columns: seq_id, header, sequence, length
    "profile": {
        "format": "fasta",
        "dataset_type": "protein_sequence",  # or "nucleotide_sequence"
        "shape": { "sequences": N },
        "sequence_stats": {
            "length_min": ..., "length_median": ..., "length_max": ...,
            "read_type": "protein | dna | rna | mixed | unknown",
            "is_plm_ready": True,   # False if nucleotide_sequence
            "pct_over_512": ..., "pct_over_1024": ...
        },
        "loadability": { "status": "ok", "parser": "biopython.SeqIO(fasta)", "errors": [] },
        "warnings": [...]
    }
}
```

---

## Production constraints

- **Always** run alphabet detection and set `dataset_type` before returning
- **Always** set `is_plm_ready = false` for `nucleotide_sequence`
- **Never** modify sequences without reporting the transformation
- **Never** drop sequences with non-standard characters — flag them and keep
- **Always** compute `pct_over_512` and `pct_over_1024` for `protein_sequence`
- **Always** deduplicate check before returning
