# Agent Eval Test-Set Curation

## Summary

**One-sentence:** Produces a curated agent-eval golden set: trajectory cases + capability tags + provenance + version-control conventions — partitioned into fast-subset and full-suite buckets.

**One-paragraph:** RAG eval test-set methodologies exist but no agent-eval-specific guide covers trajectory cases, capability tags, and version control of the golden set. This produces a spec for sourcing, labelling, partitioning, and version-controlling the golden set; the harness consumes its output verbatim.

**Ефективно для:** first-time eval setup for a new agent; quarterly review of an existing golden set; replacing 'eyeballed 10 random examples' with a versioned set; turning real production failures into permanent regression cases.

## Applies If (ALL must hold)

- Building an eval harness AND need ≥30 representative trajectories
- Production has ≥100 traces to sample from OR a domain expert can hand-author cases
- Tagging schema decided (capability, persona, difficulty)
- Version control system exists for the set

## Skip If (ANY kills it)

- No traces and no domain expert — defer until either exists
- Tags would not affect any decision — premature taxonomy
- Existing test set already passes the 4 rules below

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Trace history OR domain expert | trace store OR person | observability OR SME |
| Capability taxonomy | list of tags | domain expert |
| Version-controlled location | git repo | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-observability-stack-blueprint]]` | Trace history source |
| `[[agent-failure-taxonomy]]` | Labels for tagging failure-derived cases |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Sample real traces | sonnet | Stratified sampling. |
| Author tag taxonomy | opus | Domain reasoning. |
| Tag trajectories | sonnet | Pattern matching. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-eval-test-set-curation.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-eval-harness-bootstrap-recipe]]`
- `[[agent-eval-cost-budget-policy]]`
- `[[agent-drift-detection-statistical]]`
- `[[agent-failure-taxonomy]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-eval-test-set-curation applies: root question — "Does the team have ≥30 trajectories OR can source them?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
