---
name: pericles-compliance-audit
version: 2026.05.0
description: >
  How Pericles stays doctrine-compliant over time — the §11 compliance cadence and the
  §12 ADR process. Use this WHENEVER you run a PR doctrine check, prepare an architecture
  review, conduct the quarterly audit, set audit-log retention, pin versions, or author
  an ADR / file a carve-out exception. Encodes the three compliance checkpoints, the
  immutable-log + retention rules, and the ADR template.
doctrine_refs: [§11, §12; Ops §1–§3, §6; Manifest Spec §5]
depends_on: [pericles-doctrine, pericles-observability, pericles-skill-registry]
last_reconciled: 2026-05-28
---

# Pericles Compliance & Audit (build skill)

The doctrine only holds if it's checked against real work (§11) and changes only through
a disciplined process (§12). This skill is how compliance becomes routine rather than
aspirational.

## When to use this skill

Reviewing a PR's doctrine checklist; preparing or running an architecture review; doing the
quarterly audit; setting retention; pinning versions; authoring an ADR or filing a §12
carve-out exception.

## The three compliance checkpoints (§11)

1. **PR doctrine check** — every PR touching a manifest, runtime, or data integration
   carries the "Doctrine touched" checklist (`pericles-doctrine`); reviewers reject if
   missing/inaccurate.
2. **Architecture review** — required for any new **Functional Skill** (its
   `data_access.pattern`, dependencies, Execution-Node usage); linked from the manifest
   `provenance` (`pericles-skill-authoring`).
3. **Quarterly doctrine audit** — sample the live codebase + registry against the
   doctrine: pipeline-position correctness (§4), Execution-Node commits (§3), MCP for new
   sources (§5), tenant isolation, eval drift watchlist (`pericles-evals-scorers`), and
   the carve-out exception register.

## Immutable logs & retention

Audit/lineage logs are append-only with no app edit/delete path
(`pericles-data-model`, `pericles-observability`). Retention follows the manifest
`governance.audit_retention_days` (365–2555; default 365). Hot 90 days in Postgres, cold
beyond; customer deletion purges hot within 30 days (the `data-retention-cleanup` job).
Audit access scope is per deployment shape (`pericles-deployment-shapes`).

## Version pinning & lifecycle compliance

Tenants pin exact Skill/pack versions (`pericles-skill-registry`,
`pericles-industry-pack`); a `published` Skill needs `eval_criteria` and the Manifest
Spec §5 gate; `retired` forces migration within 7 days; a post-promotion version tamper
is P0 (`pericles-tenant-isolation`).

## The ADR process (§12)

The doctrine evolves only through ADRs. To change a principle: write an ADR
(`templates/adr.template.md`), get joint product + engineering sign-off; until approved,
the existing principle holds. **Emergency carve-out:** ship under §12, file an exception
immediately with a remediation date ≤30 days, and log it in the carve-out register. A
growing exception list is itself a signal a principle needs revision — review the
register at the quarterly audit.

## What this forbids

Merging a doctrine-touching PR without the checklist; a new Functional Skill without an
architecture review; editable/deletable audit logs; retention below the manifest
minimum; changing a principle by writing code instead of an ADR; an unremediated
carve-out past its date.

## Verification

PRs carry an accurate checklist; new Functional Skills link an architecture review; the
quarterly audit runs against the live codebase and the carve-out register; logs are
immutable and retained per policy; ADRs gate principle changes.

## Existing standards (read alongside)

Doctrine §11/§12 + ADR framework (Notion); Ops §1–§3/§6; `.claude/rules/12-testing.md`,
`200-quality/202-git-workflow` and `003-code-review-standards`.

## Open questions

- Where the ADR register and carve-out exception register live (Notion ADR framework vs
  repo `docs/adr/`) — confirm; keep one canonical home.
- Whether the quarterly audit is tooling-assisted (a script over the registry + logs) —
  build one if manual sampling misses drift.

## Changelog

- 2026.05.0 — Initial draft from Doctrine §11/§12 + the ADR framework; retention/pinning
  reconciled with Ops and the data model. ADR template added.
