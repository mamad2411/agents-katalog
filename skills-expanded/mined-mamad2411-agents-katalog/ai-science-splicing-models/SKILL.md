---
name: ai-science-splicing-models
description: "Score splicing variant effects with SpliceAI/Pangolin delta scores (DS_AG/DS_AL/DS_DG/DS_DL) and AlphaGenome. Use when scoring a VCF for splice disruption, interpreting DS thresholds, or ranking cryptic splice-site variants."
tool_type: python
primary_tool: spliceai
---

# Splicing Models: SpliceAI and AlphaGenome

## When to Use

- Scoring a VCF of candidate SNVs/indels for splice-disrupting potential (rare disease, exome/genome triage)
- Interpreting or thresholding SpliceAI delta scores (DS_AG, DS_AL, DS_DG, DS_DL) for clinical flagging
- Deciding between SpliceAI, Pangolin (tissue-specific splicing), or AlphaGenome (multi-modal: expression + chromatin + contact + splicing)
- Prioritizing a shortlist of variants by combining splice deltas with expression/chromatin evidence
- Explaining why a variant creates a cryptic donor/acceptor site rather than just weakening a canonical one

## Version Compatibility

- `spliceai` ≥1.3.1 (Illumina), requires TensorFlow ≥2.x, Python 3.8–3.10 per upstream pins
- `pangolin` ≥1.0.5 (tissue-specific splicing predictor, same input contract as SpliceAI)
- `pysam` ≥0.22 for VCF iteration; reference build must match training genome (GRCh37 or GRCh38)
- AlphaGenome: accessed via Google DeepMind's hosted API/research repo (no local weights as of 2026)

## Prerequisites

- `pip install spliceai tensorflow pysam` (SpliceAI ships its own Keras models; first run downloads ~200MB of weights)
- A reference FASTA (indexed with `.fai`) and a gene annotation (`grch37`/`grch38` built-in, or custom GTF-derived annotation file)
- Familiarity with VCF format (see `bio-applied-variant-calling-and-snp-analysis`) and GT/AG splice-site biology

## Splice Signal Refresher

- **Donor (5' splice site)**: exon–intron boundary, canonical dinucleotide `GT`
- **Acceptor (3' splice site)**: intron–exon boundary, canonical dinucleotide `AG`
- Delta scores range 0–1: **≥0.2** is a common clinical-flagging threshold, **≥0.8** is high confidence
- Gain scores (`DS_DG`/`DS_AG`) mean the variant creates a **new** site — harder to interpret than losses, since you must evaluate the resulting exon/intron structure

**Run real SpliceAI on a VCF**

**Goal:** Get production delta scores for variants in a VCF using the actual SpliceAI model (not a toy heuristic).
**Approach:** Use the `spliceai` CLI for batch scoring, or the `Annotator`/`get_delta_scores` Python API for programmatic control per-record.

```bash
## CLI: annotate a VCF, writing SpliceAI INFO fields (ALLELE|SYMBOL|DS_AG|DS_AL|DS_DG|DS_DL|DP_AG|DP_AL|DP_DG|DP_DL)
spliceai -I input.vcf -O output.vcf -R hg38.fa -A grch38 -D 500 -M 1
```

```python
import pysam
from spliceai.utils import Annotator, get_delta_scores

def annotate_vcf(vcf_path: str, fasta_path: str, annotation: str = "grch38", dist: int = 500):
    """Yield (record, [delta_score_str, ...]) for each variant in a VCF.

    delta_score_str fields are '|'-delimited: ALLELE|SYMBOL|DS_AG|DS_AL|DS_DG|DS_DL|DP_AG|DP_AL|DP_DG|DP_DL
    """
    ann = Annotator(fasta_path, annotation)
    for record in pysam.VariantFile(vcf_path):
        scores = get_delta_scores(record, ann, dist, mask=0)
        yield record, scores

for record, scores in annotate_vcf("input.vcf", "hg38.fa"):
    print(record.chrom, record.pos, record.ref, record.alts, scores)
```

**Toy delta-score model (build intuition before trusting the real network)**

**Goal:** Understand what a delta score measures — the change in donor/acceptor "site-ness" caused by a single-base substitution.
**Approach:** Score a small window around a variant with a crude motif+GC heuristic, comparing reference vs. mutant windows. This is pedagogical only; use the real `spliceai`/`pangolin` models for anything clinical.

```python
def donor_score(window: str) -> float:
    """Toy donor-site score: rewards a GT dinucleotide at the window center, plus G-richness."""
    center = window[len(window) // 2 - 1: len(window) // 2 + 1]
    score = 0.7 if center == "GT" else 0.1
    score += 0.03 * window.count("G")
    return min(score, 1.0)

def acceptor_score(window: str) -> float:
    """Toy acceptor-site score: rewards an AG dinucleotide at the window center, plus T-richness."""
    center = window[len(window) // 2 - 1: len(window) // 2 + 1]
    score = 0.7 if center == "AG" else 0.1
    score += 0.02 * window.count("T")
    return min(score, 1.0)

def mutate(seq: str, pos: int, alt: str) -> str:
    """Return seq with the base at pos replaced by alt."""
    return seq[:pos] + alt + seq[pos + 1:]

def splice_deltas(seq: str, pos: int, alt: str, w: int = 9) -> dict:
    """Compute toy DS_DG/DS_DL/DS_AG/DS_AL deltas for a substitution at pos."""
    half = w // 2
    start, end = max(0, pos - half), min(len(seq), pos + half + 1)
    ref_window = seq[start:end]
    alt_window = mutate(seq, pos, alt)[start:end]

    d_ref, d_alt = donor_score(ref_window), donor_score(alt_window)
    a_ref, a_alt = acceptor_score(ref_window), acceptor_score(alt_window)
    return {
        "DS_DG": max(0.0, d_alt - d_ref),
        "DS_DL": max(0.0, d_ref - d_alt),
        "DS_AG": max(0.0, a_alt - a_ref),
        "DS_AL": max(0.0, a_ref - a_alt),
    }

example = "CCTGACTGGTGAGTCTCAGGTTAC"
for alt in "ACGT":
    if alt != example[9]:
        print(example[9], ">", alt, splice_deltas(example, 9, alt))
```

**Rank and integrate candidate variants**

**Goal:** Turn per-variant delta scores into a prioritized shortlist, optionally combined with expression/chromatin evidence (AlphaGenome-style multi-task output).
**Approach:** Sort by `max(DS_*)` as a first-pass filter, then blend with other modalities using a weighted score.

```python
def rank_by_max_delta(example: str, candidates: list) -> list:
    """Rank (pos, alt) candidates by their maximum splice delta score, descending."""
    ranked = []
    for p, alt in candidates:
        if alt == example[p]:
            continue
        ds = splice_deltas(example, p, alt)
        ranked.append((p, example[p], alt, max(ds.values()), ds))
    ranked.sort(key=lambda x: x[3], reverse=True)
    return ranked

def integrated_priority(max_ds: float, expr_delta: float, chrom_delta: float) -> float:
    """Weighted blend of splice, expression, and chromatin deltas (AlphaGenome-style triage)."""
    return 0.6 * max_ds + 0.25 * abs(expr_delta) + 0.15 * abs(chrom_delta)

candidates = [(8, "A"), (8, "C"), (9, "A"), (10, "T"), (14, "G"), (17, "A")]
for pos, ref, alt, max_ds, ds in rank_by_max_delta(example, candidates):
    print(f"pos={pos} {ref}>{alt} maxDS={max_ds:.3f} details={ds}")
```

## Pitfalls

- **Toy code ≠ SpliceAI**: the illustrative `donor_score`/`acceptor_score` functions are for intuition only — they will not match real SpliceAI/Pangolin output; always use the real model for actual variant interpretation.
- **Reference build mismatch**: SpliceAI predictions depend on the annotation (`grch37`/`grch38`) matching the FASTA build — mixing builds silently produces wrong gene contexts.
- **Coordinate systems**: BED is 0-based half-open; VCF/GFF are 1-based inclusive — mixing them causes off-by-one errors in window extraction.
- **Gain vs loss asymmetry**: DS_DG/DS_AG (gain) require checking the resulting exon/intron structure — a high gain score without a plausible new transcript is often a false positive.
- **Multiple testing**: apply FDR correction (Benjamini-Hochberg) when scoring thousands of variants and thresholding for significance.

## See Also

- `bio-applied-variant-calling-and-snp-analysis` — VCF structure, calling, and iteration with pysam/cyvcf2
- `bio-applied-clinical-genomics` — downstream clinical triage of prioritized variants
- `ai-science-enformer-regulatory` — related sequence-to-function model (Enformer/Borzoi) for regulatory and expression tracks
- `ai-science-variant-to-structure-models` — complementary variant-effect prediction at the protein-structure level
