# Agent Context Engineering Corpus Standard

## Summary

**One-sentence:** Spec for the canonical corpus an agent assembles per task — sources, chunking, ranking, citation, freshness — so two agents on the same task produce comparable contexts.

**One-paragraph:** Spec for the canonical corpus an agent assembles per task — sources, chunking, ranking, citation, freshness — so two agents on the same task produce comparable contexts. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying agent context engineering corpus standard. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for agent context engineering corpus standard across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- the agent assembles a per-task corpus from multiple sources (docs, code, chats, tickets)
- two agents on the same task must produce comparable corpora (reproducibility matters)
- the corpus feeds an LLM call whose output downstream consumers depend on

## Skip If (ANY kills it)

- agent uses a single source verbatim (no chunking, no ranking) — corpus standard is overkill
- agent is a one-shot prototype with no second consumer — wait until reproducibility matters
- the corpus is itself the deliverable to a human reviewer — use research-synthesis methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source inventory (allowed sources + access policy) | list | ml-engineering |
| Chunking + embedding model | config | ml-engineering |
| Ranking policy | ranker + tie-break rules | ml-engineering |
| Freshness policy | max age per source class | ml-engineering |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval gate for corpus quality |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `source_inventory` | sonnet | Lift allowed sources + access policy from team docs. |
| `policy_compose` | opus | Compose corpus policy (chunking + ranking + freshness + citation). |
| `citation_audit` | sonnet | Audit citations in sample runs against policy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/corpus-policy.md.j2` | Spec skeleton for corpus policy |
| `templates/corpus-policy.md` | Spec skeleton for corpus policy Generated from `templates/corpus-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/output-schema.json` | Corpus envelope schema (sources + chunks + ranks + citations) |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in corpus policy |
| `templates/_smoke-test.md` | Minimum viable filled-in corpus policy Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-context-engineering-corpus-standard.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[eval-driven-development-tdd-for-ai]]
- [[ai-call-site-inventory]]
- [[ai-feature-observability-four-pillars]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
