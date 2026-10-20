# Llm Judge Rubric Evidence First

## Summary

**One-sentence:** Builds an LLM-as-judge rubric (JSON output, evidence cited before scores, per-criterion, bias mitigations) and emits a judge-spec + sample rubric.

**One-paragraph:** Rating prompts ('rate 1-10') are noise. A real LLM judge demands a structured rubric, JSON output, evidence cited BEFORE the score, per-criterion scoring, and explicit bias mitigation (position, verbosity, self-preference, authority). This methodology converts an eval task profile into a deterministic judge-spec.

**Ефективно для:** solopreneur evaluating open-ended outputs (summaries, code reviews, agent transcripts) who refuses to ship hope.

## Applies If (ALL must hold)

- Output is open-ended (summary, code review, plan, transcript).
- Exact-match / unit tests don't apply.
- ≥1 stronger judge model available than the system under test.
- Eval cost is bounded.
- Labeled examples exist OR can be co-authored with the judge.

## Skip If (ANY kills it)

- Output is structured and exact-matchable.
- Judge model is weaker than SUT.
- Compliance forbids LLM-generated scores.
- Sample size <5 — write manual reviews.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `eval-task-profile.yaml` | criteria, judge_model, sample_count, bias_targets | author |
| `SUT output sample` | JSONL or md | from system |
| `Optional ground-truth` | if available | labeling |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for rubric structure, evidence-first, per-criterion, JSON, bias mitigations. | ~1750 |
| `content/02-output-contract.xml` | essential | judge-spec + rubric schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | 1-10 prompt, no JSON, position bias, verbosity bias, self-preference. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step build procedure. | ~800 |
| `content/05-examples.xml` | recommended | Worked example: code-review judge. | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/eval-task-profile.yaml` | Input. |
| `templates/judge-spec.md.j2` | Output. |
| `templates/judge-spec.md` | Output. Generated from `templates/judge-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llm-judge-rubric-evidence-first.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-agents-eval]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on criteria_count (1 → single-criterion focused; 2-5 → per-criterion structured; >5 → split into multiple judges), then on bias_targets (position → swap order; verbosity → length-penalty; self-preference → judge != SUT model). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
