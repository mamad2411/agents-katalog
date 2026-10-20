---
name: load-fastq
description: Load FASTQ files into a pandas DataFrame using BioPython. Parses sequences and Phred quality scores, computes per-read quality stats, and emits a raw_reads Dataset Profile. FASTQ is raw sequencing data — it is NOT a PLM input.
compatibility: biopython ≥1.80, pandas ≥1.5, numpy ≥1.23. Works offline.
instruments: Sequencer — Illumina MiSeq, MiSeq i100, Element Biosciences Aviti, PromethION 2
---

# Load FASTQ

> **Not a PLM input.** FASTQ files contain raw unaligned sequencing reads with quality scores. They are not directly usable for protein language model fine-tuning. Route to `analyze-fastq-reads` for quality assessment, then quality-filter and align before any downstream use.

## When to use

File is `.fastq` or `.fq` — or first line starts with `@` followed by a read identifier.
Sources: NGS sequencers (short-read Illumina, long-read Oxford Nanopore PromethION).

---

## Loading

```python
from Bio import SeqIO
import pandas as pd
import numpy as np

def load_fastq(path: str) -> tuple[pd.DataFrame, dict]:
    records = []
    try:
        for rec in SeqIO.parse(path, "fastq"):
            quals = rec.letter_annotations["phred_quality"]
            records.append({
                "read_id":    rec.id,
                "sequence":   str(rec.seq).upper(),
                "length":     len(rec.seq),
                "mean_q":     float(np.mean(quals)),
                "min_q":      int(np.min(quals)),
                "qual_string": "".join(chr(q + 33) for q in quals),  # ASCII Phred
            })
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse FASTQ — {e}")

    if not records:
        raise ValueError(f"LOAD ERROR: no reads found in {path}")

    df = pd.DataFrame(records)
    return df, {"parser": "biopython.SeqIO(fastq)", "dataset_type": "raw_reads"}
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid FASTQ format | `fail` | `"LOAD ERROR: could not parse FASTQ — {detail}"` |
| Zero reads | `fail` | `"LOAD ERROR: no reads found in {path}"` |
| >10% reads with mean Q < 20 | `warn` | `"LOAD WARN: {pct}% of reads have mean Phred Q < 20 — low quality"` |
| Duplicate read IDs | `warn` | `"LOAD WARN: {n} duplicate read_id values detected"` |

---

## Profile fields populated

- `format`: `"fastq"`
- `dataset_type`: `"raw_reads"` (always — FASTQ is never a direct PLM input)
- `shape`: `{ sequences: N }`
- `sequence_stats`: `length_min`, `length_median`, `length_max`, `read_type`, `is_plm_ready: false`
- `sample_stats`: `mean_q` distribution (min/median/mean/max/std)
- `missing`: null counts

---

## Preprocessing defaults

1. **Uppercase sequences** — `seq.upper()`
2. **Detect alphabet** — DNA expected; flag if non-ACGTN chars > 1%
3. **Set `is_plm_ready = false`** — FASTQ is always raw_reads, never a PLM input
4. **Flag low-quality reads** — reads with mean Q < 20 flagged in `warnings`; do not filter silently
5. **Compute quality distribution** — mean Q per read; report pct below Q20 and Q30 thresholds
6. **Report read length distribution** — FASTQ from long-read sequencers (PromethION) will have variable lengths; flag if std > 200

---

## Output

```python
{
    "df": pd.DataFrame,   # columns: read_id, sequence, length, mean_q, min_q, qual_string
    "profile": {
        "format": "fastq",
        "dataset_type": "raw_reads",
        "shape": { "sequences": N },
        "sequence_stats": {
            "length_min": ..., "length_median": ..., "length_max": ...,
            "read_type": "dna",
            "is_plm_ready": False,
            "pct_over_512": None,   # not applicable for raw reads
            "pct_over_1024": None
        },
        "sample_stats": { "mean_q": { "min": ..., "median": ..., "mean": ..., "max": ..., "std": ... } },
        "loadability": { "status": "ok", "parser": "biopython.SeqIO(fastq)", "errors": [] },
        "warnings": ["FASTQ is raw sequencing data — not a PLM input; quality-filter and align first"]
    }
}
```

---

## Production constraints

- **Always** set `dataset_type = "raw_reads"` — never `bio-sequence` or `protein_sequence`
- **Always** set `is_plm_ready = false` and add the non-PLM warning
- **Never** filter reads by quality without explicit instruction — flag only
- **Always** report pct reads below Q20 in `warnings`
- **Never** compute `pct_over_512` / `pct_over_1024` for FASTQ reads — set to null
