# Prompt Portability Across Providers

## Summary

**One-sentence:** Spec to rewrite a prompt suite for cross-provider portability — Anthropic + OpenAI + Gemini — without breaking users on the next model upgrade.

**One-paragraph:** Production AI features need provider redundancy (Anthropic primary + OpenAI fallback, Gemini Pro for vision). Prompts encode provider-specific structure: Claude's XML tags, OpenAI's developer/user roles, Gemini's safety blocks, refusal styles. This methodology produces a `portability-spec.json` artefact pinning the abstraction layer (system prompt placement, tool-call schema, reasoning-block strategy, refusal handler) so the same prompt suite runs on any of N providers. Output is versioned + owned + reviewed.

**Ефективно для:**

- AI features з multi-provider redundancy (Anthropic + OpenAI + Gemini).
- Migrate AI feature across model upgrade without breaking users.
- Strip provider-specific tags from existing prompts.
- Abstract tool-call schemas через a common adapter.
- Refusal-style normalisation across providers.

## Applies If (ALL must hold)

- Recurring need to migrate prompts across providers / model generations.
- ≥2 provider runtimes in production OR planned within the quarter.
- Named accountable owner.
- Repository hosts the versioned spec.

## Skip If (ANY kills it)

- Single-provider product without redundancy plans.
- One-shot migration with no recurrence.
- Fewer than 3 instances per year.
- No named owner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current prompt suite | Markdown / YAML | git |
| Provider matrix (which providers + which features) | YAML | platform |
| Tool catalog (functions + schemas) | YAML | service repo |
| Refusal-style policy | Markdown | safety repo |
| Named accountable owner | string | ownership log |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[prompt-portability-audit]]` | Pre-migration audit. |
| `[[prompt-pr-review-checklist]]` | Downstream review gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for portability-spec + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: pick providers → audit → abstract → test → commit | ~800 |
| `content/05-examples.xml` | essential | Worked example: Claude+OpenAI dual stack | ~700 |
| `content/06-decision-tree.xml` | essential | Routes provider matrix to abstraction strategy | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-current` | sonnet | Per-prompt judgment. |
| `abstract-tool-schemas` | opus | Multi-provider abstraction reasoning. |
| `refusal-normalize` | sonnet | Per-style rewrite. |

## Templates

| File | Purpose |
|------|---------|
| `templates/portability-spec.json` | JSON skeleton matching 02-output-contract. |
| `templates/portability-spec.md.j2` | Narrative review draft. |
| `templates/portability-spec.md` | Narrative review draft. Generated from `templates/portability-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-portability-across-providers.py` | Validate portability-spec | Pre-commit + before migration job |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-portability-audit]]
- [[provider-deprecation-runbook]]
- [[prompt-pr-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to a single-provider exit if no redundancy is planned; otherwise picks the abstraction layer (tool-schema adapter vs system-prompt rewrite vs both) based on the provider matrix. Walk it before opening the migration PR.
