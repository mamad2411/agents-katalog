---
name: paper-triage
description: On explicit user request, triage an ambiguous paper query into likely interpretations, a ranked shortlist, and recommended follow-up workflows.
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Paper Triage

Turn an ambiguous paper query into a ranked shortlist and clear next steps.
Use this when the human starts with a fuzzy title fragment, overloaded term, or vague memory of a paper.

## Arguments

- The positional argument is the paper query. Quote multi-word titles when running from a shell.
- `--shortlist-size <n>` controls the final shortlist size returned to the human.
- `--relevance-limit <n>` controls the first relevance-search pass.
- `--bulk-candidate-limit <n>` controls the wider recall pass.
- `--snippet-candidate-limit <n>` controls how many preliminary candidates get snippet search.
- `--snippet-limit-per-paper <n>` caps snippet evidence gathered for each snippet target.

## Workflow

Use this workflow only when the user explicitly requests paper triage. Run it
in the current agent; no platform-specific worker or fork is required. Resolve
`<skill-dir>` from this `SKILL.md`, following installation symlinks. The runner
uses the Semantic Scholar API; prefer `SEMANTIC_SCHOLAR_API_KEY` in the
environment over a command-line credential.

1. Run `python3 "<skill-dir>/scripts/run.py" ...`.
2. Read `result.possible_interpretations` to see how the query was resolved.
3. Read `result.shortlist` for the ranked candidate papers.
4. Read `result.follow_up_actions` to know which workflow to run next once the right paper is identified.
5. If the shortlist still looks wrong, rerun with a more specific query string.

## Output

- The script prints the unified JSON envelope described in `output_contract.md`.
- The underlying workflow result is `TriageResult.to_dict()`.
- `result.notes` captures extra execution notes, and `result.considered_candidates` shows the rerank breadth.

## When To Escalate

- The query is too vague to resolve into a useful shortlist.
- The top interpretation is clearly wrong even after adding specificity.
- The human really wants author lookup or direct paper details instead of title disambiguation.
