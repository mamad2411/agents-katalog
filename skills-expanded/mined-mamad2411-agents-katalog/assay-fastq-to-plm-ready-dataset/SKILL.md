---
name: assay-fastq-to-plm-ready-dataset
description: Convert paired-end FASTQ reads from a yeast-display RBD binding screen into a PLM-ready labeled CSV. Handles Aviti NGS data from FACS-sorted binder/non-binder pools across lib1/lib2 sub-libraries and one or more sort gates. Runs QC and paired-end merge via fastp (subprocess, no Java required), adapter trimming and variable-region extraction in pure Python, SARS-CoV-2 RBD constant-sequence reconstruction, DNA-to-AA translation, wild-type removal, per-pool deduplication, cross-pool overlap exclusion and binder/non-binder labeling. Outputs <species>_<date>.csv (columns: species, Sequence, Library, aa_sequence, count, binding, sort) ready for PLM fine-tuning, embedding, or variant-effect scoring.
user-invokable: true
compatibility: python ≥3.9, biopython ≥1.79, pandas ≥1.5. Step 1 requires fastp (no Java; install with conda install -c bioconda fastp or download from github.com/OpenGene/fastp). Steps 2–4 run offline with biopython + pandas only.
---

# Assay FASTQ to PLM-Ready Dataset

> **Invoke this skill whenever the user has paired-end FASTQ reads from an RBD yeast-display binding screen and needs a labeled amino acid CSV for PLM training.** Execute all steps in order; do not skip any. All code blocks are self-contained — copy and run directly in a Python interpreter.

## When to use

Use when:
- Input is raw paired-end Aviti or Illumina FASTQ files (`*_R1.fastq.gz` / `*_R2.fastq.gz`)
- Samples come from a combinatorial SARS-CoV-2 RBD yeast-display library with lib1 and lib2 sub-libraries
- Data was FACS-sorted into binder and non-binder pools across one or more sort gates
- Goal is a PLM-ready CSV with per-sequence `binding` labels and `sort` metadata
- User says any of: "preprocess the binding screen data", "run the NGS pipeline", "I have FASTQ files from the assay", "process the yeast display reads", "prepare the dataset for fine-tuning"

## When not to use

| Want… | Use instead |
|---|---|
| Profile or inspect the output labeled CSV | `profiling-datasets` |
| Fine-tune a PLM on the output CSV | `huggingface-jobs` |
| Quality metrics only, no labeling | `analysis/analyze-fastq-reads` |
| Already have amino acid sequences in a CSV | `data-processing/protein-sequence-data` |

---

## Input contract

```python
config = {
    "input_dir":   str,   # directory containing all *_R1.fastq.gz / *_R2.fastq.gz pairs
    "output_dir":  str,   # working dir for merged .fastq.gz and trimmed .csv intermediates
    "species":     str,   # e.g. "mouse" — used in output filename
    "date":        str,   # e.g. "250624" (YYMMDD) — used in output filename
    "sorts": [
        {
            "sort_id":     int,  # 1, 2, 3, …
            "binder_lib1": str,  # sample basename (no _R1/_R2.fastq.gz suffix)
            "binder_lib2": str,
            "non_lib1":    str,
            "non_lib2":    str,
        }
    ]
}
```

**Example**

```python
config = {
    "input_dir":  "./input",
    "output_dir": "./output",
    "species":    "mouse",
    "date":       "250624",
    "sorts": [
        {
            "sort_id":     1,
            "binder_lib1": "250624_mouse_bind_s1_lib1",
            "binder_lib2": "250624_mouse_bind_s1_lib2",
            "non_lib1":    "250624_mouse_non_s1_lib1",
            "non_lib2":    "250624_mouse_non_s1_lib2",
        },
        {
            "sort_id":     2,
            "binder_lib1": "250624_mouse_bind_s2_lib1",
            "binder_lib2": "250624_mouse_bind_s2_lib2",
            "non_lib1":    "250624_mouse_non_s2_lib1",
            "non_lib2":    "250624_mouse_non_s2_lib2",
        },
    ]
}
```

---

## Biological constants

Define these once at the top of your script before running any step.

```python
from Bio.Seq import Seq

# Constant flanking sequences that reconstruct full-length RBD from the variable region.
# lib1: append LIB1_CONSTANT AFTER the variable region (3′ constant).
# lib2: prepend LIB2_CONSTANT BEFORE the variable region (5′ constant).
LIB1_CONSTANT = "GGGAATAAACCGTGCAACGGCGTAGCTGGCTTTAACTGTTATTTCCCATTAAGATCTTATTCTTTCAGACCTACGTATGGAGTCGGGCATCAGCCGTACAGGGTTGTGGTTCTTTCATTTGAACTGCTGCACGCGCCCGCAACCGTATGCGGGCCGAAGAAATCAACG"
LIB2_CONSTANT = "AATATCACGAACCTTTGTCCTTTCGATGAGGTCTTCAATGCTACTAGATTCGCATCCGTGTATGCATGGAATAGAAAGAGAATTAGTAATTGTGTAGCGGACTACTCTGTACTTTATAACTTGGCCCCATTCTTTACATTCAAGTGTTACGGTGTATCTCCCACC"

# Wild-type SARS-CoV-2 RBD amino acid sequence — removed from all outputs.
WT_AA = "NITNLCPFDEVFNATRFASVYAWNRKRISNCVADYSVLYNLAPFFTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGNIADYNYKLPDDFTGCVIAWNSNKLDSKVSGNYNYLYRLFRKSNLKPFERDISTEIYQAGNKPCNGVAGFNCYFPLRSYSFRPTYGVGHQPYRVVVLSFELLHAPATVCGPKKST"

# Library-specific adapter sequences and expected variable-region lengths (bp).
# Both 435 and 438 are exact multiples of 3 — no partial-codon issues at translation.
LIB_CONFIG = {
    1: {"adapter": "GCGGGCTCC", "length": 435},
    2: {"adapter": "TCTCCCACC", "length": 438},
}

# Step 1 QC thresholds
QUALITY_THRESHOLD  = 20   # fastp --qualified_quality_phred: trim to Q20
PRE_MERGE_MIN_LEN  = 150  # min R1/R2 read length before merge (bp)
POST_MERGE_MIN_LEN = 435  # min merged read length to keep (bp)
```

---

## Step 1 — QC, quality trim and paired-end merge

Uses `fastp` (no Java required) via `subprocess`: quality-trims both reads to Q20, discards R1/R2 pairs shorter than 150 bp, merges overlapping pairs and discards unmerged reads. A second pure-Python pass filters the merged output to ≥435 bp. Samples run concurrently via `ThreadPoolExecutor`. The intermediate merged file is deleted after each sample succeeds.

Install fastp: `conda install -c bioconda fastp` or download from github.com/OpenGene/fastp.

```python
import gzip
import os
import shutil
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def _filter_merged(src_gz, dst_gz, min_len):
    kept = 0
    with gzip.open(src_gz, "rt") as src, gzip.open(dst_gz, "wt") as dst:
        while True:
            header = src.readline()
            if not header:
                break
            seq  = src.readline()
            plus = src.readline()
            qual = src.readline()
            if len(seq.rstrip()) >= min_len:
                dst.write(header + seq + plus + qual)
                kept += 1
    return kept

def _process_sample(sample, input_dir, output_dir):
    i, o = Path(input_dir), Path(output_dir)
    o.mkdir(parents=True, exist_ok=True)
    r1         = i / f"{sample}_R1.fastq.gz"
    r2         = i / f"{sample}_R2.fastq.gz"
    merged_all = o / f"{sample}_merged_all.fastq.gz"
    filtered   = o / f"{sample}_filtered_merged.fastq.gz"
    try:
        # Q20 trim + discard short pairs + merge overlapping reads
        # --disable_adapter_trimming: adapter removal is handled by Step 2
        subprocess.run([
            "fastp",
            "--in1", str(r1), "--in2", str(r2),
            "--merged_out", str(merged_all),
            "--out1", os.devnull, "--out2", os.devnull,
            "--failed_out", os.devnull,
            "--merge",
            "--qualified_quality_phred", str(QUALITY_THRESHOLD),
            "--unqualified_percent_limit", "40",
            "--length_required", str(PRE_MERGE_MIN_LEN),
            "--disable_adapter_trimming",
            "--thread", str(min(4, os.cpu_count() or 1)),
            "--json", str(o / f"{sample}_fastp.json"),
            "--html", os.devnull,
        ], check=True, capture_output=True, text=True)
        # Keep only merged reads >= 435 bp
        kept = _filter_merged(merged_all, filtered, POST_MERGE_MIN_LEN)
        print(f"[Step 1] {sample}: {kept} merged reads ≥{POST_MERGE_MIN_LEN}bp → {filtered.name}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"fastp failed on {sample}:\n{e.stderr}") from e
    finally:
        merged_all.unlink(missing_ok=True)
    return filtered

def run_step1(config):
    if shutil.which("fastp") is None:
        raise FileNotFoundError(
            "fastp not found on PATH. Install with: conda install -c bioconda fastp"
        )
    samples = [f.name.replace("_R1.fastq.gz", "")
               for f in Path(config["input_dir"]).glob("*_R1.fastq.gz")]
    print(f"[Step 1] {len(samples)} samples, {max(1, os.cpu_count()-1)} workers")
    with ThreadPoolExecutor(max_workers=max(1, os.cpu_count() - 1)) as pool:
        futures = [pool.submit(_process_sample, s, config["input_dir"], config["output_dir"])
                   for s in samples]
        for f in futures:
            f.result()  # re-raise worker exceptions

def check_step1(config):
    import json
    out_dir = Path(config["output_dir"])
    samples = [f.name.replace("_R1.fastq.gz", "")
               for f in Path(config["input_dir"]).glob("*_R1.fastq.gz")]
    for sample in samples:
        out = out_dir / f"{sample}_filtered_merged.fastq.gz"
        if not out.exists() or out.stat().st_size == 0:
            raise RuntimeError(
                f"[Step 1] {out.name} missing or empty — check fastp stderr above."
            )
        jsf = out_dir / f"{sample}_fastp.json"
        if jsf.exists():
            d        = json.loads(jsf.read_text())
            n_pairs  = d.get("summary", {}).get("before_filtering", {}).get("total_reads", 0) // 2
            n_merged = d.get("merge_result", {}).get("total_merged", 0)
            rate     = n_merged / n_pairs if n_pairs > 0 else 0
            print(f"  {sample}: {n_merged:,} merged reads ({rate:.1%} merge rate)")
            if rate < 0.10:
                print(f"  WARNING: merge rate <10% for {sample} — verify overlapping library design or FASTQ integrity")
    print("[Step 1] ✓ All filtered_merged.fastq.gz present and non-empty")
```

---

## Step 2 — Adapter trimming and variable-region extraction

Library identity inferred from filename: `"lib2"` anywhere in the name (case-insensitive) → lib2; otherwise lib1. Reads the merged FASTQ in 50 000-read chunks. For each read, searches for the forward adapter and extracts the downstream sequence at the expected fixed length. Falls back to the reverse-complement adapter if the forward is not found. Reads without a recognizable adapter or of incorrect length are discarded.

```python
import gzip
import re
from Bio import SeqIO
from Bio.Seq import Seq
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

def _trim_chunk(sequences, lib):
    fwd = LIB_CONFIG[lib]["adapter"]
    exp = LIB_CONFIG[lib]["length"]
    rc  = str(Seq(fwd).reverse_complement())
    trimmed, rev_count = [], 0
    for seq in sequences:
        if fwd in seq:
            candidate = re.sub(f".*{fwd}", "", seq)[:exp]
        elif rc in seq:
            seq = str(Seq(seq).reverse_complement())
            candidate = re.sub(f".*{fwd}", "", seq)[:exp]
            rev_count += 1
        else:
            continue
        if len(candidate) == exp:
            trimmed.append(candidate)
    return trimmed, rev_count

def _trim_file(args):
    input_gz, output_csv = args
    name = Path(input_gz).name
    lib  = 2 if "lib2" in name.lower() else 1
    total_rev = 0
    with gzip.open(input_gz, "rt") as handle, open(output_csv, "w") as out:
        out.write("Sequence\n")
        batch = []
        for record in SeqIO.parse(handle, "fastq"):
            batch.append(str(record.seq))
            if len(batch) == 50_000:
                seqs, rev = _trim_chunk(batch, lib)
                total_rev += rev
                out.writelines(s + "\n" for s in seqs)
                batch = []
        if batch:
            seqs, rev = _trim_chunk(batch, lib)
            total_rev += rev
            out.writelines(s + "\n" for s in seqs)
    print(f"[Step 2] {name}: {total_rev} rev-comp reads trimmed → {Path(output_csv).name}")

def run_step2(config):
    out_dir = Path(config["output_dir"])
    tasks = [
        (str(gz), str(out_dir / ("trimmed_" + gz.name.replace(".fastq.gz", ".csv"))))
        for gz in out_dir.glob("*_filtered_merged.fastq.gz")
    ]
    print(f"[Step 2] Trimming {len(tasks)} files")
    with ProcessPoolExecutor(max_workers=max(1, os.cpu_count() - 1)) as pool:
        list(pool.map(_trim_file, tasks))

def check_step2(config):
    out_dir = Path(config["output_dir"])
    issues  = []
    for gz in sorted(out_dir.glob("*_filtered_merged.fastq.gz")):
        csv     = out_dir / ("trimmed_" + gz.name.replace(".fastq.gz", ".csv"))
        lib     = 2 if "lib2" in gz.name.lower() else 1
        exp_len = LIB_CONFIG[lib]["length"]
        if not csv.exists():
            issues.append(f"MISSING: {csv.name}"); continue
        df = pd.read_csv(csv)
        if len(df) == 0:
            issues.append(
                f"EMPTY: {csv.name} — adapter '{LIB_CONFIG[lib]['adapter']}' not found "
                f"in any read. Verify lib{'2' if lib == 2 else '1'} identity in filename."
            ); continue
        wrong = (df["Sequence"].str.len() != exp_len).sum()
        if wrong:
            issues.append(f"{csv.name}: {wrong} sequences not {exp_len}bp — trimming logic error")
        print(f"  {csv.name}: {len(df):,} sequences ({exp_len}bp each)")
    if issues:
        raise RuntimeError("[Step 2] failures:\n" + "\n".join(issues))
    print("[Step 2] ✓ All trimmed CSVs present, non-empty, correct sequence length")
```

---

## Step 3 — Constant-sequence reconstruction, translation, WT removal, deduplication

Reconstructs full-length RBD by attaching the constant flanking region to each library's variable sequences, translates to amino acids, removes sequences with premature stop codons, computes read-depth counts per unique AA sequence, logs and removes WT, then deduplicates (keeping first occurrence so the `count` column reflects total read depth before deduplication).

```python
import pandas as pd
from Bio.Seq import Seq

def preprocess_rbd(lib1_csv, lib2_csv, verbose=True):
    lib1 = pd.read_csv(lib1_csv)
    lib2 = pd.read_csv(lib2_csv)

    # Reconstruct full-length RBD: lib1 carries 3′ constant, lib2 carries 5′ constant
    lib1["Sequence"] = lib1["Sequence"] + LIB1_CONSTANT
    lib2["Sequence"] = LIB2_CONSTANT + lib2["Sequence"]
    lib1["Library"], lib2["Library"] = 1, 2

    df = pd.concat([lib1, lib2], ignore_index=True)

    # Remove any sequence with non-ATCG characters
    df = df[df["Sequence"].str.match(r"^[ATCG]+$")].copy()

    # Translate — biopython Seq.translate() uses standard genetic code (table 1),
    # identical to Biostrings::translate() for pure-ATCG sequences of length % 3 == 0
    df["aa_sequence"] = df["Sequence"].apply(lambda s: str(Seq(s).translate()))

    # Guard: >50% stop codons almost always means lib1/lib2 constant-direction swap
    n_stops   = df["aa_sequence"].str.contains("*", regex=False).sum()
    stop_rate = n_stops / max(len(df), 1)
    if stop_rate > 0.5:
        raise RuntimeError(
            f"[Step 3] Stop codon rate {stop_rate:.1%} exceeds 50% — almost certainly a "
            f"lib1/lib2 constant-direction swap. Verify lib1 appends LIB1_CONSTANT AFTER "
            f"and lib2 prepends LIB2_CONSTANT BEFORE."
        )
    if verbose:
        print(f"  {stop_rate:.1%} premature stop codons removed ({n_stops:,} sequences)")

    # Remove sequences with premature stop codons (internal '*')
    df = df[~df["aa_sequence"].str.contains("*", regex=False)].copy()

    # Count reads per unique AA sequence before deduplication
    df["count"] = df["aa_sequence"].map(df["aa_sequence"].value_counts())

    # Log WT percentage — high value indicates library quality issues
    wt_pct = (df["aa_sequence"] == WT_AA).sum() / max(len(df), 1) * 100
    if verbose:
        print(f"  WT%: {wt_pct:.2f}  (lib1={Path(lib1_csv).name})")

    # Remove wild-type sequences
    df = df[df["aa_sequence"] != WT_AA].copy()

    # Deduplicate by AA sequence; first occurrence carries the correct count
    df = df.drop_duplicates(subset="aa_sequence", keep="first").reset_index(drop=True)

    if len(df) == 0:
        raise RuntimeError(
            f"[Step 3] 0 sequences survived all filters — check lib1/lib2 CSV assignments "
            f"and constant-sequence direction."
        )
    if verbose:
        print(f"  {len(df):,} unique AA sequences retained")
    return df
```

---

## Step 4 — Binder/non-binder labeling and overlap exclusion

For each sort gate, sequences appearing in both the binder and non-binder pools are excluded from both (ambiguous label, cannot be reliably used for training). The remaining sequences receive a `binding` label and a `sort` identifier. Results from all sort gates are concatenated into the final DataFrame.

```python
def label_sort(sort_cfg, output_dir):
    d = Path(output_dir)

    def csv_path(sample):
        return d / f"trimmed_{sample}_filtered_merged.csv"

    bind = preprocess_rbd(csv_path(sort_cfg["binder_lib1"]), csv_path(sort_cfg["binder_lib2"]))
    non  = preprocess_rbd(csv_path(sort_cfg["non_lib1"]),    csv_path(sort_cfg["non_lib2"]))

    overlap = set(bind["aa_sequence"]) & set(non["aa_sequence"])
    if overlap:
        print(f"  [sort {sort_cfg['sort_id']}] {len(overlap)} overlapping sequences removed")
    bind = bind[~bind["aa_sequence"].isin(overlap)].copy()
    non  = non[~non["aa_sequence"].isin(overlap)].copy()

    bind["binding"], non["binding"] = "bind", "non"
    combined = pd.concat([bind, non], ignore_index=True)
    combined["sort"] = sort_cfg["sort_id"]
    return combined

def run_step4(config):
    frames = []
    for sort_cfg in config["sorts"]:
        print(f"[Steps 3–4] Sort {sort_cfg['sort_id']}")
        frames.append(label_sort(sort_cfg, config["output_dir"]))
    return pd.concat(frames, ignore_index=True)

def check_step4(df, config):
    for sort_cfg in config["sorts"]:
        sid = sort_cfg["sort_id"]
        sub = df[df["sort"] == sid]
        n_b = (sub["binding"] == "bind").sum()
        n_n = (sub["binding"] == "non").sum()
        if n_b == 0:
            raise RuntimeError(
                f"[Step 4] Sort {sid}: binder pool is empty after overlap removal — "
                f"check binder_lib1/binder_lib2 assignments."
            )
        if n_n == 0:
            raise RuntimeError(
                f"[Step 4] Sort {sid}: non-binder pool is empty after overlap removal — "
                f"check non_lib1/non_lib2 assignments."
            )
        print(f"  sort {sid}: {n_b:,} bind + {n_n:,} non = {len(sub):,} sequences")
    print(f"[Step 4] ✓ {len(df):,} total labeled sequences across {df['sort'].nunique()} sort(s)")
```

---

## Full pipeline

```python
import time
from pathlib import Path

def main(config):
    t0 = time.time()

    print("=== Step 1: QC and paired-end merge ===")
    run_step1(config)
    check_step1(config)
    print(f"  done in {time.time()-t0:.0f}s\n")

    t1 = time.time()
    print("=== Step 2: Adapter trimming ===")
    run_step2(config)
    check_step2(config)
    print(f"  done in {time.time()-t1:.0f}s\n")

    t2 = time.time()
    print("=== Steps 3–4: Translation, filtering, labeling ===")
    df = run_step4(config)
    check_step4(df, config)
    print(f"  done in {time.time()-t2:.0f}s\n")

    out_csv = Path(config["output_dir"]) / f"{config['species']}_{config['date']}.csv"
    # `species` column is required by the downstream evaluation harness — every
    # row carries the species so the candidate dataset is self-describing and
    # the join key does not depend on filename parsing.
    df["species"] = config["species"]
    df[["species", "Sequence", "Library", "aa_sequence", "count", "binding", "sort"]].to_csv(
        out_csv, index=False
    )
    print(f"Wrote {len(df):,} sequences → {out_csv}")
    print(f"  bind: {(df['binding']=='bind').sum():,}  non: {(df['binding']=='non').sum():,}")
    print(f"  total: {time.time()-t0:.0f}s")

# Install dependencies if needed:
#   pip install biopython pandas
main(config)
```

---

## Output contract

```
<species>_<date>.csv  (index=False, UTF-8)

Column       Type    Description
species      str     Species/ortholog (e.g. "possum", "human_new") — same value on every row
Sequence     str     Full-length RBD DNA (variable + constant flanking, ~600 bp)
Library      int     Sub-library of origin: 1 (3′-constant) or 2 (5′-constant)
aa_sequence  str     Translated amino acid sequence (no stop codon, not WT)
count        int     Total read depth for this aa_sequence before deduplication
binding      str     "bind" (binder pool) or "non" (non-binder pool)
sort         int     FACS sort gate identifier (from config)
```

`species` is required by the downstream evaluation. The amino-acid column is
named `aa_sequence` (not `aa_seq`) — the CandidateAdapter recognises both, but
the canonical name is `aa_sequence`.

---

## Failure modes

**fastp not found** — `FileNotFoundError` at start of Step 1. Install with `conda install -c bioconda fastp` or download a precompiled binary from github.com/OpenGene/fastp. No Java required.

**fastp subprocess fails** — `RuntimeError` with full stderr. Common causes: corrupt or truncated FASTQ input, mismatched R1/R2 read counts, or insufficient disk space for the intermediate merged file.

**Empty CSV after Step 2** — adapter not found in any read. Verify library identity is encoded in the sample basename: the string `"lib2"` (case-insensitive) must appear for lib2 samples; everything else defaults to lib1. Check that `binder_lib1` / `binder_lib2` are correctly assigned.

**All sequences filtered in Step 3** — constant-sequence direction error. Confirm `binder_lib1` maps to a lib1 sample and `binder_lib2` to a lib2 sample. Swapping the two within a pool produces every sequence being out-of-frame and failing the stop-codon filter.

---

## Hard constraints

- **Never** swap `LIB1_CONSTANT` and `LIB2_CONSTANT` — direction is biological, not arbitrary
- **Never** prepend LIB1_CONSTANT or append LIB2_CONSTANT — lib1 appends after, lib2 prepends before
- **Never** write the output CSV with `index=True` — the R pipeline produced an unnamed index column; the Python pipeline must not
- **Never** assign `binding` labels before overlap removal — label only after filtering common sequences
- **Always** compute `count` with `value_counts().map()` before `drop_duplicates` — post-dedup counts will all be 1
- **Always** log WT percentage before removing WT — it is a library quality diagnostic
- **Always** verify `fastp` is on PATH before any subprocess call — fail early with an actionable message
