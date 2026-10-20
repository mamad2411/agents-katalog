# Training Data Sourcing Policy

## Summary

**One-sentence:** Produces a versioned training-data-sourcing policy: allowed sources, prohibited classes, licence + consent gating, PII handling, audit trail and approval owners for fine-tuning runs.

**Ефективно для:** ML engineers preparing a fine-tune corpus; data leads gating customer-data usage for training; legal / compliance reviewers on AI training pipelines.

**One-paragraph:** This methodology pins the recurring decision around "training-data-sourcing-policy" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Team is fine-tuning OR pre-training on data not provided by the foundation-model vendor.
- Data includes user content (PII or customer corpus).
- Regulatory regime applies (GDPR / CCPA / HIPAA / EU AI Act).
- Owner exists to sign the policy.

## Skip If (ANY kills it)

- Team is prompt-only (no fine-tuning) — pivot to prompt-data policy.
- Corpus is fully public-domain with no PII — overhead unjustified.
- Vendor handles all training; team only operates inference.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus inventory | CSV / Parquet manifest | data engineering |
| Source licence table | CSV / Markdown | legal |
| Consent register | CSV / DB extract | trust + safety |
| PII classifier output | JSONL | data engineering |
| Policy owner + approver | handle / email | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[fine-tune-vs-prompt-decision-tree]]` | team has confirmed fine-tune is the right axis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_sources` | sonnet | Per-source licence + consent classification. |
| `draft_policy` | sonnet | Cross-source synthesis. |
| `escalate_legal` | opus | Cross-regime conflict triage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/training-data-sourcing-policy.json` | JSON Schema for the Training Data Sourcing Policy output contract |
| `templates/training-data-sourcing-policy.md.j2` | Markdown skeleton with the required fields |
| `templates/training-data-sourcing-policy.md` | Markdown skeleton with the required fields Generated from `templates/training-data-sourcing-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-training-data-sourcing-policy.py` | Enforce the Training Data Sourcing Policy output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[fine-tune-vs-prompt-decision-tree]] — gates whether to fine-tune at all.
- [[data-exfiltration-canary-tokens]] — adjacent leakage detection.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
