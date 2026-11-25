# scikit-bio Tree Comparison Starter

Use this skill to parse two small Newick trees with `scikit-bio` and summarize a compact topology-comparison result.

## What it does

- Parses two deterministic toy phylogenies from Newick strings.
- Summarizes tip labels, total branch lengths, and both unweighted and weighted Robinson-Foulds distances.
- Returns a small JSON payload suitable for smoke tests and future phylogenetic workflow extensions.

## When to use it

- You need a runnable starter for `Phylogenetic comparative workflows`.
- You want a lightweight verified tree-comparison example before larger comparative biology analyses.

## Example

```bash
slurm/envs/ecology/bin/python skills/ecology-evolution-and-biodiversity/scikitbio-tree-comparison-starter/scripts/run_scikitbio_tree_comparison.py \
  --out scratch/ecology/tree_comparison_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/ecology-evolution-and-biodiversity/scikitbio-tree-comparison-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase31_frontier_leaf_conversion_skills -v`
