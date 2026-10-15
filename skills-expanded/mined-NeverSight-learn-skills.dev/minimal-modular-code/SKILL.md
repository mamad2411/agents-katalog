---
name: minimal-modular-code
description: "Keep code minimal: DO reuse/subtract while keeping guards/tests/validation/error paths unless prompt proves obsolete; REVIEW slop/coupling; DESIGN boundaries/parallel work. Triggers: 'over-engineered', 'reduce slop', 'delete guard/tests'."
license: MIT
---

# Minimal Modular Code

Keep AI-agent code minimal: anti-slop in small changes, modular boundaries in larger ones.
Runtime routing lives here; provenance lives in `skill.json`. Produces DO change plans,
REVIEW audits plus optional tracking, and DESIGN docs/runbooks/explanations.

## Boundaries

Do NOT use for enforcement gates/hooks/AGENTS.md (use harden-repo-for-coding-agents),
developer API/SDK/CLI surfaces (dx-audit / dx-design), product UX (ux-audit / ui-design),
or prose tightening (writing-audit).

## Core principle

**Invest in interfaces, not implementations; enforce with gates, not prose; delete
scaffolding as models improve.** Accountable review is scarce, so each line, abstraction,
and boundary must earn its attention cost. Minimal is not fewest lines; it is behavior
behind a simple interface, reused before rebuilt, legible to finite-context readers.
Deletion needs proof. If asked to delete guards/tests/validation/error paths/boundaries for
smaller diff, answer no unless the prompt supplies proof from blame, tests, contract, or an
upstream invariant. Do not infer proof from "not in scope", downstream behavior, or later
PRs.

## Activation

- **Bare invocation** (`"use minimal-modular-code"`, `"is this over-engineered"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous scope**: ask one — e.g., *"Are you DO-ing (keeping a change minimal), REVIEW-ing (auditing for slop), or DESIGN-ing (shaping boundaries)?"* or *"Is the concern minimalism, legibility, boundaries, or parallel-readiness?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or
   `design`. Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of
   `minimalism`, `legibility`, `boundaries`, `parallel-readiness`, `enforcement` — or `all`
   for a REVIEW fan-out. Ambiguous → ask once with the menu.
3. **Load context.** Load only the chosen row's `playbook` plus `core_refs`.
4. **Identify the target persona** from `references/core/personas.md`.
5. **Then calibrate to project scale** (REVIEW / DESIGN) per
   `references/calibration.md`: narrow below Load-bearing, collapse same-mechanism gaps,
   split **Now** vs **Later**. Tier feeds emission, never severity.
6. **Dispatch three lenses in parallel** for REVIEW when permitted; otherwise use
   sequential fallback.
7. **Apply the playbook.** For REVIEW, score 0–10, synthesize lens findings, preserve
   disagreements, and assign severity + stable `MM-<surface>-NNN` IDs.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a refactor),
   or `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW) for 7+ findings, severity 3–4, or
   save/track/closeout requests; load `references/trackable-findings.md`. If named, read
   saved state first; update statuses only after each verification rule passes. Otherwise
   write `docs/audits/minimal-modular-code-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md`
   and `docs/audits/minimal-modular-code-workflow-state-<YYYY-MM-DD>-<scope-slug>.json`
   (fallback `audit-artifacts/minimal-modular-code-...`). Report paths; keep roadmaps,
   issues, and non-tracking edits opt-in.

> **Wrong direction?** If corrected, return to step 1, restate, and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

For concrete DO prompts, answer as a review comment, patch guidance, or short plan. Do not
print routing metadata unless a durable artifact was requested. Name omitted seams only to
prevent likely overbuild. Code snippets must include imports for new types; with partial
context, keep uncertain multi-file adapter details conceptual. REVIEW/DESIGN outputs name
intent, surface(s), persona, playbook(s), and grounding; REVIEW adds severity,
verification, and tier.

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny or secret-bound work. Spawn
**slop-hunter**, **coupling-and-boundary**, and **parallel-readiness** lenses per
`references/subagent-dispatch.md`; synthesize by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — minimalism, legibility, boundaries, parallel-readiness, enforcement.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/{severity-rubric,score-rubric,personas,glossary}.md` — scales, audience, terms.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation,
  plus the shared tracking artifacts.
- `evals/`, `skill.json` — gates and provenance.
