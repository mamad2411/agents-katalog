---
name: expand-references
description: On explicit user request, expand one to three seed papers into nearby, bridge, foundational, methodological, recent, and survey follow-ups.
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Expand References

Turn one to three seed papers into a structured follow-up reading list.
Use this when the human already has anchor papers and wants the next papers to read.

## Arguments

- Positional arguments are the seed papers. Quote multi-word titles.
- `--negative <paper>` may be repeated to push the workflow away from an unwanted cluster.
- `--pool all-cs|recent` selects the Semantic Scholar recommendation pool.
- `--limit <n>` controls how many raw recommendations are requested before reranking.
- `--per-bucket-limit <n>` caps each curated bucket after scoring.

## Workflow

Use this workflow only when the user explicitly requests reference expansion.
Run it in the current agent; no platform-specific worker or fork is required.
Resolve `<skill-dir>` from this `SKILL.md`, following installation symlinks.
The runner uses the Semantic Scholar API; prefer `SEMANTIC_SCHOLAR_API_KEY`
in the environment over a command-line credential.

1. Run `python3 "<skill-dir>/scripts/run.py" ...`.
2. Read `result.closest_neighbors` for the immediate next reads.
3. Read `result.bridge_papers` for papers that connect multiple seeds.
4. Read `result.foundational`, `result.methodological`, `result.recent`, and `result.surveys_or_benchmarks` for curated slices of the neighborhood.
5. If the result is sparse or off-topic, adjust the seed set or add `--negative` papers and rerun.

## Output

- The script prints the unified JSON envelope described in `output_contract.md`.
- The underlying workflow result is `ExpandReferencesResult.to_dict()`.
- `result.notes` captures dropped records and other execution notes.

## When To Escalate

- Fewer than one clear seed paper is available.
- The resolved seeds are obviously duplicates or wrong papers.
- The output is empty even after trying better seeds or a different recommendation pool.
