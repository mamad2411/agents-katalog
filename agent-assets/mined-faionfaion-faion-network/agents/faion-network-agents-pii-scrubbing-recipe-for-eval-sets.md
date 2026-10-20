# PII Scrubbing Recipe for Eval Sets

## Summary

**One-sentence:** Codified recipe to convert raw production traffic into a safe evaluation set — PII scrub rules, consent labels, retention window, audit trail.

**One-paragraph:** Building an eval harness from real user traffic exposes the team to PII, consent, and retention risk. This methodology produces a versioned spec that names the scrub strategy (regex + ML detector + human review), the consent label per row, the retention window, and the audit trail. Output is a `pii-scrub-spec.json` artefact that downstream eval-harness builds consume; without it the eval set is GDPR-noncompliant and untraceable.

**Ефективно для:**

- Production eval harness, що споживає реальний user traffic.
- GDPR / CCPA-regulated context з vague legal guidance.
- Долі consent labels + retention window треба зафіксувати перед індексацією.
- Audit trail для downstream reviewers (security, legal, ML-ops).
- Версіонування scrub-recipe — щоб updates були diff-able and reversible.

## Applies If (ALL must hold)

- Eval harness will draw from production traffic (not synthetic).
- Team has a named accountable owner (handle / role-with-rotation).
- Repository / wiki space хранить the versioned artefact.
- Tier ≥ geek (manifest enforces).

## Skip If (ANY kills it)

- All eval data is synthetic — no PII risk, no scrub recipe needed.
- Working eval-set spec already exists — update in place, do not duplicate.
- Regulator mandates a different template — defer to legal.
- Greenfield prototype без real users.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Sample of production traffic (≥100 rows, redactable copy) | JSONL | data warehouse |
| Consent dictionary (user_id → consent flags) | YAML | consent service |
| Retention policy (days, per-row class) | YAML | legal repo |
| PII regex catalog (emails / phones / addresses / IDs) | YAML | platform security |
| Named accountable owner | string (handle) | ownership log |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides ML-engineer operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 hard rules + run-checklist + skip terminal | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for pii-scrub-spec + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: sample → classify → scrub → consent → audit | ~800 |
| `content/05-examples.xml` | essential | Worked example: 500-row sample → final spec | ~700 |
| `content/06-decision-tree.xml` | essential | Routes traffic-class + consent state to scrub strategy | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-spec` | haiku | Template fill, bounded. |
| `pick-scrub-strategy` | sonnet | Per-row judgment: regex enough vs ML detector. |
| `legal-review-synthesis` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pii-scrub-spec.json` | JSON skeleton matching 02-output-contract schema. |
| `templates/pii-scrub-spec.md.j2` | Markdown skeleton for narrative review draft. |
| `templates/pii-scrub-spec.md` | Markdown skeleton for narrative review draft. Generated from `templates/pii-scrub-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pii-scrubbing-recipe-for-eval-sets.py` | Validate pii-scrub-spec against 02-output-contract schema | Pre-commit + before downstream eval-harness build |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[production-trace-mining-for-training-data]]
- [[rag-corpus-discovery-interview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides between regex-only scrub (low PII density, well-known formats) vs ML-detector + human review (high PII density or free-form). It also routes consent-missing rows out of the eval set entirely. Walk it before drafting the spec; choosing regex on free-form text leaks PII.
