---
name: algo-sequence-alignment
description: "Implement Needleman-Wunsch global and Smith-Waterman local sequence alignment: fill/traceback DP matrices, match/mismatch or BLOSUM62 scoring. Use when coding alignment from scratch or explaining DP traceback algorithms."
tool_type: python
primary_tool: numpy
---

# Sequence Alignment with Dynamic Programming

## When to Use

- Implementing Needleman-Wunsch or Smith-Waterman from scratch (interview prep, teaching DP, or custom scoring not supported by library aligners)
- Explaining/visualizing how a DP alignment matrix and traceback pointers are built
- Comparing global vs. local vs. affine-gap alignment behavior on short test sequences
- Aligning two full-length homologous sequences (global) or finding the best matching sub-region (local, e.g. domain search, adapter/primer location)
- Need production-grade protein/DNA alignment with real substitution matrices — use Biopython's `PairwiseAligner` (C-accelerated) rather than pure-Python DP for anything beyond toy-sized sequences

## Version Compatibility

Biopython ≥1.80 (`Bio.Align.PairwiseAligner` replaced the deprecated `Bio.pairwise2` in 1.80), NumPy ≥1.24, Python ≥3.10.

## Prerequisites

`pip install biopython numpy`. Concepts: basic dynamic programming (overlapping subproblems, memoized tables), FASTA/`Seq` objects (see `biopython` skill), substitution matrix concepts (BLOSUM/PAM).

## Global vs Local

| | Needleman-Wunsch (Global) | Smith-Waterman (Local) |
|---|---|---|
| Aligns | Full sequences end-to-end | Best matching sub-region |
| Init | First row/col = cumulative gap penalty | First row/col = 0 |
| Cell floor | No floor (can go negative) | Floor at 0 |
| Traceback from | Bottom-right corner | Maximum-scoring cell |
| Use when | Same-length homologs, full divergence | Domain search, read mapping, local motifs |

For each cell `dp[i][j]`, take the max of three predecessors: diagonal `dp[i-1][j-1] + score(seq1[i-1], seq2[j-1])` (match/mismatch), up `dp[i-1][j] + gap` (gap in seq2), left `dp[i][j-1] + gap` (gap in seq1).

**Goal:** compute the optimal global alignment score and one optimal alignment (score + traceback).
**Approach:** build an `(m+1) x (n+1)` DP matrix, initialize the border with cumulative gap penalties, fill by max-of-three-predecessors, then trace back from `dp[m][n]` to `dp[0][0]`.

```python
import numpy as np

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    """Global alignment (Needleman-Wunsch). Returns (score, aligned_seq1, aligned_seq2)."""
    m, n = len(seq1), len(seq2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    for i in range(m + 1):
        dp[i][0] = i * gap
    for j in range(n + 1):
        dp[0][j] = j * gap

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            dp[i][j] = max(dp[i - 1][j - 1] + s, dp[i - 1][j] + gap, dp[i][j - 1] + gap)

    # Traceback from bottom-right corner
    align1, align2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            if dp[i][j] == dp[i - 1][j - 1] + s:
                align1.append(seq1[i - 1]); align2.append(seq2[j - 1])
                i -= 1; j -= 1
                continue
        if i > 0 and dp[i][j] == dp[i - 1][j] + gap:
            align1.append(seq1[i - 1]); align2.append('-'); i -= 1
        else:
            align1.append('-'); align2.append(seq2[j - 1]); j -= 1

    return dp[m][n], ''.join(reversed(align1)), ''.join(reversed(align2))

score, a1, a2 = needleman_wunsch("ATCGTAC", "ATGTTAT")
assert (a1, a2) == ("ATCGTAC", "ATGTTA-") or len(a1) == len(a2)
```

**Goal:** find the best-scoring local sub-alignment (e.g. a conserved domain shared between two otherwise divergent sequences).
**Approach:** same recurrence as NW but floor every cell at 0 and start/stop traceback at the global-max cell instead of a fixed corner.

```python
import numpy as np

def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-1):
    """Local alignment (Smith-Waterman). Returns (score, aligned_seq1, aligned_seq2)."""
    m, n = len(seq1), len(seq2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    max_score, max_pos = 0, (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = match if seq1[i - 1] == seq2[j - 1] else mismatch
            dp[i][j] = max(0, dp[i - 1][j - 1] + s, dp[i - 1][j] + gap, dp[i][j - 1] + gap)
            if dp[i][j] > max_score:
                max_score, max_pos = dp[i][j], (i, j)

    align1, align2 = [], []
    i, j = max_pos
    while dp[i][j] > 0:
        s = match if seq1[i - 1] == seq2[j - 1] else mismatch
        if dp[i][j] == dp[i - 1][j - 1] + s:
            align1.append(seq1[i - 1]); align2.append(seq2[j - 1]); i -= 1; j -= 1
        elif dp[i][j] == dp[i - 1][j] + gap:
            align1.append(seq1[i - 1]); align2.append('-'); i -= 1
        else:
            align1.append('-'); align2.append(seq2[j - 1]); j -= 1

    return max_score, ''.join(reversed(align1)), ''.join(reversed(align2))

score, a1, a2 = smith_waterman("AAATCGTACGGG", "CCATGTTATCC")
assert score >= 0 and len(a1) == len(a2)
```

**Goal:** align real protein sequences with a biologically meaningful substitution matrix and affine gap costs (short gaps cost more per-residue than long ones) — the production path instead of hand-rolled DP.
**Approach:** use Biopython's C-accelerated `PairwiseAligner`, loading a standard matrix (`BLOSUM62` for typical protein similarity, `PAM250`/`BLOSUM45` for distant homologs) and separate open/extend gap scores.

```python
from Bio.Align import PairwiseAligner, substitution_matrices
from Bio.Seq import Seq

def align_proteins(seq1, seq2, mode="global", matrix="BLOSUM62", open_gap=-10, extend_gap=-0.5):
    """Align two protein sequences with a real substitution matrix and affine gaps."""
    aligner = PairwiseAligner()
    aligner.mode = mode  # "global" (NW) or "local" (SW)
    aligner.substitution_matrix = substitution_matrices.load(matrix)
    aligner.open_gap_score = open_gap
    aligner.extend_gap_score = extend_gap
    alignments = aligner.align(Seq(seq1), Seq(seq2))
    best = alignments[0]
    return best.score, best

hba = "MVLSPADKTNVKAAWGKVGAHAG"  # human hemoglobin alpha N-term
hbb = "MVHLTPEEKSAVTALWGKVNVDE"  # human hemoglobin beta N-term
score, aln = align_proteins(hba, hbb)
assert score > 0
```

## Complexity

O(mn) time and space for both NW and SW. Space can be reduced to O(min(m,n)) with rolling arrays (Hirschberg's algorithm recovers full traceback in O(mn) time / O(m+n) space if needed).

## Pitfalls

- Traceback ties (multiple predecessors with the same score) yield different, equally-optimal alignments — pick a consistent tie-break order (e.g. diagonal > up > left) for reproducibility
- Linear gap penalties treat one 10-residue gap the same as ten 1-residue gaps; affine penalties (open + extend, as in the Biopython example) are more biologically realistic and require three DP matrices (M/X/Y) instead of one
- NW forces alignment across the entire length of both sequences — if lengths differ a lot, use SW or semi-global (free end gaps) alignment instead
- BLOSUM62 is the default for protein BLAST/general use; use higher-number BLOSUM (BLOSUM80) for close homologs and PAM250/BLOSUM45 for distant ones
- `Bio.pairwise2` is deprecated (removed in recent Biopython) — use `Bio.Align.PairwiseAligner`
- Pure-Python DP is O(mn) per call and becomes impractically slow above a few thousand residues; use `PairwiseAligner` (C-accelerated) or BLAST/minimap2 for real genome-scale search

## See Also

- `bio-alignment-pairwise-alignment` — Biopython PairwiseAligner in depth, alignment scoring/formatting
- `biopython` — Seq objects, FASTA I/O, general Biopython usage
- `bio-alignment-msa-parsing` — multiple sequence alignment (beyond pairwise)
- `bio-database-access-blast-searches` — heuristic (non-DP) large-scale sequence search with BLAST
