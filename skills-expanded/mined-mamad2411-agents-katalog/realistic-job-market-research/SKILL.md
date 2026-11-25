---
name: realistic-job-market-research
description: "Collect and audit public job postings, build a lossless filterable ledger, and realistically evaluate a shortlist against a local candidate profile, exact JD, company identity, current finance, commute or work policy, compensation, and hiring effort. Use for 'collect all openings', 'research these jobs realistically', 'which roles are worth the effort', or 'separate new, reposted, stale, and misleading openings'. Never submits applications or mutates profiles."
license: MIT
compatibility: "Codex and Claude Code. Requires Node.js 20+, Python 3.10+, network access for live public collection, and an optional local browser for authenticated review and browser QA."
---

# Realistic Job Market Research

## Purpose

Reproduce a complete two-stage workflow: declared-source census and artifact audit first, personalized realistic review second. Distinguish low-cost application preparation from the stricter decision to join an employer.

For personalized review, read and validate the private profile described in [references/personalization.md](references/personalization.md). Default path: `~/.config/realistic-job-market-research/profile.json`. A raw census does not require a profile.

Resolve supporting scripts from this skill directory, never from the user's project cwd. Claude Code can use `${CLAUDE_SKILL_DIR}`; in Codex, use the absolute directory containing this `SKILL.md`.

## Workflow

1. Freeze the candidate contract from the local profile and verify referenced resume hashes. Do not paraphrase a mutable resume from memory.
2. Choose a mode. `census` owns declared public collection and the filterable ledger. `review` starts from an audited ledger or named shortlist. `update` compares prior IDs and bodies with current pages.
3. For `census`, read [references/census-runbook.md](references/census-runbook.md), initialize a new immutable run, and preserve the registry capability split: 13 implemented adapters, 15 access probes, and one authenticated handoff. Attempt every declared source without describing probe-only channels as collected, preserve blocked or failed zero-row artifacts, sync terminal states, build the manifest and dashboard, then run both executable gates.
4. For `review`, recheck every selected role on its current detail page. The exact body and source ID outrank title, tags, and search snippets.
5. Extract mandatory and preferred requirements, duties, employment, exact location, work policy, compensation, deadline, and hiring steps. Use `UNKNOWN` when absent.
6. Resolve employer identity before finance. Match every mandatory requirement to profile evidence as `confirmed`, `transferable`, `missing`, or `unknown`.
7. Read [references/scoring-model.md](references/scoring-model.md), then calculate `JD Match Score`, `Opportunity Score`, `Evidence Coverage`, and `Evidence Quality` with `scripts/score_review.py`. Calculate raw weighted values at full precision, apply non-compensatory ceilings before bands and ranking, and report sensitivity profiles.
8. Make two decisions: `PREPARE | CONDITIONAL | DROP` for application effort and `PASS | HOLD | NO_GO` for the employer or offer. Scores inform these states but never replace them.
9. Adversarially recheck leaders using [references/pitfalls.md](references/pitfalls.md), including degree floors, customer-facing work, language, mandatory frameworks, scale, hidden tests, stale finance, and founder-commitment signals.
10. Produce coverage, scored shortlist, component scores, sensitivity changes, hard exclusions, corrections, claim-level sources, unknowns, and resume actions. Validate machine-readable output.

## Modes

- **Census:** after reviewing the source policy, run `<skill-dir>/scripts/run-census.mjs --run-dir /absolute/run/path --acknowledge-source-policy` with Node.js.
- **Named shortlist:** deeply verify roles supplied by the user.
- **Audited ledger:** select a small review set; unreviewed rows are not exclusions.
- **Update correction:** label genuinely new, reposted, previously missed, closed, and materially changed roles separately.

## Rules

- Prefer official career pages and exact job details. A search result is discovery evidence, not proof that a role is active.
- Never call a query-limited, blocked, or failed source complete. Never synthesize rows from provider totals.
- Preserve conflicting facts with both sources; do not average them.
- Do not infer salary, work policy, degree requirements, finance, or hiring steps.
- Do not express unsupported hiring probabilities as percentages. Use reasoned `high`, `medium`, or `low` fit labels.
- Never present a score without its components, numeric calculation trail, evidence coverage and quality, model version, weights, and active caps.
- Do not store recruiter names, emails, phone numbers, private messages, credentials, or confidential employer data.
- Do not apply, save, message, edit a profile, or contact anyone without explicit authorization for that action.
- Keep the final shortlist small. More rows are not a better result.

## References

- [references/census-runbook.md](references/census-runbook.md) — read for collection, resume, and artifact transitions.
- [references/source-registry.md](references/source-registry.md) — 29-source scope and completeness contract.
- [references/source-governance.md](references/source-governance.md) — collection authorization, retention, rate, and redistribution boundary.
- [references/raw-schema.md](references/raw-schema.md) and [references/verification-gates.md](references/verification-gates.md) — read before build or audit claims.
- [references/evidence-contract.md](references/evidence-contract.md) — read before finance, identity, status, or decision classification.
- [references/review-schema.md](references/review-schema.md) — read when producing or validating machine-readable review JSON.
- [references/scoring-model.md](references/scoring-model.md) — research basis, formulas, weights, caps, and sensitivity analysis.
- [references/decision-validation.md](references/decision-validation.md) — owner swing weighting and prospective outcome validation.
- [references/personalization.md](references/personalization.md) — local profile and public/private boundary.
- [references/authenticated-sources.md](references/authenticated-sources.md) — read before any personalized browser source.
- [references/pitfalls.md](references/pitfalls.md) — adversarial checks learned from failed scans.
- [references/reproducibility.md](references/reproducibility.md) — frozen reference-run parity evidence.
