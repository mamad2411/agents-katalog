---
name: research-knowledge-core
description: "Shared reference for the research-knowledge cluster: the evidence ladder (lightest lane first → escalate on synthesis need), the four provenance tiers every claim carries, source/freshness conventions, and the question-type → spoke matrix. USE WHEN running any research, literature, IP, genomic, codebase, or docs-lookup task — the discipline every spoke in this cluster shares."
cluster: research-knowledge
version: 1.0.0
---

# Research & Knowledge Core

Shared model for the `research-knowledge` cluster. Every research, literature, database,
codebase, and reference spoke depends on these two interlocking ideas — keep them consistent
here so no spoke contradicts another.

## 1. The evidence ladder (this cluster's defining discipline)

Answer with the **lightest lane that actually answers the question**, and escalate only when a
heavier one is justified. Climbing a rung costs time, tokens, and quota — earn it.

```
local context / docs / ck memory   ← cheapest, no network
        │  (not present or stale?)
        ▼
fast discovery (exa-search, single DB query)
        │  (one source not enough? need synthesis?)
        ▼
multi-source synthesis (deep-research, systematic literature review)
        │  (claim needs judging?)
        ▼
evaluation / verification (scholar-evaluation, citation checks)
```

**Rule:** never start a heavyweight pass when a lookup answers it; never stop at one source
when the claim is load-bearing and contested. `research-ops` is the operator that picks the
starting rung — route ambiguous "research this" asks there first.

## 2. The four provenance tiers (every claim carries one)

Each statement you return is labeled by where it came from. Never let one tier bleed into
another unlabeled — that is the single most common way research output misleads.

| Tier | What it is | Source obligation |
|---|---|---|
| **Sourced fact** | From a citable source (paper, page, record, DB) | Name the source + date |
| **Supplied context** | The user gave it to you | Attribute to the user |
| **Inference** | What follows from the evidence | Mark as reasoning, not fact |
| **Recommendation** | Your answer / next move | Flag as a judgment call |

## 3. Conventions

- **Freshness:** date every freshness-sensitive claim; say "as of <date>". Drift-prone MCP
  spokes (`deep-research`, `exa-search`, `documentation-lookup`) — verify configured tool
  names and current API docs before quoting coverage or live counts.
- **Reproducibility:** database spokes (`pubmed`, `uspto`, `gget`) log the exact query,
  parameters, and result IDs so a run can be repeated. Prefer official APIs over scraping.
- **Citations:** carry a stable identifier (DOI / PMID / patent no. / URL) per source; never
  cite a source you did not actually open.
- **Scope before search:** convert the prompt into a searchable question first (PICO for
  clinical/biomedical); pick the review type (narrative → scoping → systematic → meta-analysis)
  to match the rigor the claim needs.
- **Persistence:** when a result should survive the session — onboarding facts, ongoing
  research state — write it to `ck` memory rather than re-deriving it next time.

## 4. Question-type → spoke matrix

| Question type | Spoke | Lightest-lane note |
|---|---|---|
| Ambiguous "research this" / compare / latest | `research-ops` | Picks the lane below |
| Fast web · code · company · people discovery | `exa-search` | Rung 2 |
| Thorough multi-source cited report | `deep-research` | Rung 3 — earn it |
| Systematic literature review & synthesis | `scientific-thinking-literature-review` | Rung 3 |
| Judge a paper / proposal / evidence quality | `scientific-thinking-scholar-evaluation` | Rung 4 |
| Biomedical literature (MeSH / PMID / E-utils) | `scientific-db-pubmed-database` | Rung 2, reproducible |
| Patents & trademarks (official IP records) | `scientific-db-uspto-database` | Rung 2, reproducible |
| Genomic DB / sequence / enrichment | `scientific-pkg-gget` | Rung 2, reproducible |
| Map an unfamiliar repo → onboarding guide | `codebase-onboarding` | Rung 1 (local) |
| Step-by-step `.tour` walkthrough | `code-tour` | Rung 1 (local) |
| Up-to-date library/framework docs | `documentation-lookup` | Rung 1 — before web |
| Persist / resume project context | `ck` | Rung 1 — before re-deriving |

## 5. Conventions for combining spokes

- "Review the literature **and** rate the key paper" → `scientific-thinking-literature-review`
  → `scientific-thinking-scholar-evaluation`.
- "What's the current state of X **and** save it" → `deep-research` → `ck`.
- "Onboard me to this repo **and** leave a tour" → `codebase-onboarding` → `code-tour`.
- A heavyweight web pass that a docs lookup would answer is an anti-pattern — try
  `documentation-lookup` first when the user named a framework.

## 6. Shared guardrails

- **Lightest lane first:** local / docs / `ck` before the web; one source before many;
  scoping before systematic. Escalate only on a real synthesis or verification need.
- **Label every claim** by provenance tier; never fold inference into sourced fact.
- **Date** freshness-sensitive answers; **name** every source; never cite an unopened source.
- **Reproducible** database runs — log query, params, and result IDs.
- **Don't re-derive** what `ck` memory or a prior onboarding already captured.
- Drift-prone MCP spokes: confirm live tool names + quotas before promising coverage.
