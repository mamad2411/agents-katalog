---
name: quality-control
description: >-
  Sample-stratified quality control for single-cell data with every exclusion
  recorded. Use when filtering cells or genes, setting QC thresholds, handling
  mitochondrial fraction or doublets, or when cellimo check reports C008
  (unstratified QC) or C010 (exclusions not recorded).
allowed-tools: Bash(cellimo *), Read, Skill
---

Quality control removes data. Every removal is a scientific claim that those
cells were not measuring what you wanted, so every removal is grounded,
sample-stratified, inspected, and recorded.

## Ground every scientific code cell

A scientific code cell reads, transforms, filters, summarises, or plots the
single-cell data. Before creating **each** such cell:

1. Call `ground` with one concrete objective, the modality, and likely native
   API names. For example: `quality control per sample
   sc.pp.calculate_qc_metrics sc.pl.violin sc.pp.filter_cells mitochondrial`.
   Use `analysis_mode="exploratory"`.
2. If `needs_user_decision` is true, stop. Show the user the note and relevant
   rejected findings. Do not replace missing or rejected precedent with code
   from memory.
3. Read both `api_usage` and `in_practice`. Tutorials establish the native API;
   paper companions show how it is used on real data. Adapt one bounded cell in
   working memory and keep every applicable `# cellimo:source ... section=...
   sha=...` line exactly as returned.
4. Call `ground` again with the same objective and the **exact proposed cell**
   as `candidate_code`. Do not create the cell unless
   `candidate_reviewed=true` and `needs_user_decision=false`.
5. If the preflight names a native alternative, ask the user whether to use it
   or retain the custom implementation. The agent may explain the trade-off;
   it may not override the finding.
6. Only now load marimo-pair, call `create_cell`, then `run_cell`, and inspect
   the cell status and output. One grounding result authorises one cell, not a
   whole QC section.

Calls that only write Cellimo provenance are bookkeeping, not scientific code
cells. A cell that both filters data and records it is scientific and still
needs the source header and candidate preflight.

## Look before thresholding

Plot these distributions per sample, never only pooled:

- genes per cell;
- counts per cell;
- percentage of mitochondrial counts.

Pooling hides the thing you are looking for. A sample sequenced half as deeply
as the others has a legitimately lower count distribution; a global threshold
deletes most of it and keeps the rest, creating a batch effect.

Prefer a grounded package-native plot when it expresses the required grouping.
Do not build a Matplotlib or seaborn equivalent merely for styling convenience.
Ground the plotting cell separately from the filtering cell.

## Set thresholds within samples

A fixed technical floor plus a within-sample robust outlier rule is a
defensible starting point, not an automatic truth. Tissue changes the
mitochondrial cut-off: heart and kidney cells legitimately carry more
mitochondrial RNA than PBMCs. Show the distributions, state the proposed rule,
and let the user settle any material threshold choice.

If there is only one sample, a global threshold can be correct. Record a
`pooling_justification` so C008 can distinguish that design from an oversight.

## Preserve counts first

Before normalisation changes `X`, identify and preserve the unmodified counts in
the declared counts layer. Put that operation in a grounded cell. Normalising in
place with no counts layer is unrecoverable; if counts are unavailable upstream,
stop and route back to project-audit.

## Record exclusions from observed numbers

After the grounded filtering cell has run, record the object sizes it actually
produced:

```python
with project.stage("post_qc", summary="Sample-stratified QC",
                   params={"min_genes": 200, "max_pct_mt": 15, "mad": 5}) as stage:
    filtered.write_h5ad(stage.output("artifacts/post_qc.h5ad"))
    stage.add_exclusion(
        "low gene count / high mitochondrial fraction / within-sample outlier",
        axis="obs", n_before=n0, n_removed=n0 - n1, n_remaining=n1,
        by_sample={sample: int(count) for sample, count in removed.items()},
        stratified_by=sample_key,
        criteria={"min_genes": 200, "max_pct_mt": 15, "mad_threshold": 5},
    )
    stage.add_exclusion("genes in fewer than 3 cells", axis="var",
                        n_before=g0, n_removed=g0 - g1, n_remaining=g1)
    stage.set_matrix_facts(representation="raw_counts", counts_layer="counts",
                           n_obs=n1, n_vars=g1)
```

`n_before - n_removed` must equal `n_remaining`; the validator checks it. Never
substitute arithmetic remembered from an earlier run for the live object.

## Inspect what was removed

Report per-sample loss. A sample that lost 60% of its cells while others lost
5% is not a QC success; it may be a failed library, and dropping it entirely is
a user decision.

Doublet detection is a separate grounded stage and normally runs per sample
because doublet rate scales with loading density. Record the expected and
observed rates.

## Stop conditions

- Stop before writing if either `ground` call requires a user decision.
- Stop after execution if QC removes more than half the cells, and explain.
- If a condition drops below two donors, say immediately that confirmatory
  comparison of that group is no longer supportable.
