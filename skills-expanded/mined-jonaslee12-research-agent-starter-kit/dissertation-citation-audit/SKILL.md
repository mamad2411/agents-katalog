---
name: dissertation-citation-audit
description: Audit dissertation citations, bibliography entries, source metadata, quote accuracy, and whether cited sources actually support the attached claims.
---

# Dissertation Citation Audit

Use when checking references, citations, literature review drafts, theoretical claims, methodology citations, or final dissertation readiness.

## Workflow

1. Identify the files to audit.
2. Extract claims with citations.
3. Check whether each citation supports the exact claim.
4. Flag missing page numbers for direct quotes if required by the style guide.
5. Flag unverifiable or suspicious references.
6. Check consistency between in-text citations and bibliography.

## Status Labels

- `VERIFIED`: citation exists and supports the claim.
- `WEAK SUPPORT`: source is relevant but does not fully support the claim.
- `MISMATCH`: source does not support the claim.
- `MISSING`: citation key or bibliography entry missing.
- `NEEDS VERIFICATION`: source details are incomplete or not locally verifiable.

## Output

Create or update `audit-reports/CITATION_AUDIT.md`.

## Claim Ledger Lite

Use `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md` when the task audits or revises formal proposal, thesis/dissertation, manuscript, report, grant, stakeholder-facing argument claims, chapter/section-level claim support, or source-readiness upgrades.

For those tasks, create or check a Claim Ledger Lite table before treating claim support as usable:

```bash
python3 scripts/claim_ledger_lite_check.py <ledger.md>
```

The ledger must record the claim, output location, source anchor, evidence status, what the evidence cannot prove, concept contract, allowed wording, and review action. It does not make metadata-only sources citation-ready and it does not replace source-section verification.

## Guardrails

Read `../dissertation-shared/references/citation-discipline.md`.
Do not invent source metadata. If internet access is needed for verification, say so clearly.
