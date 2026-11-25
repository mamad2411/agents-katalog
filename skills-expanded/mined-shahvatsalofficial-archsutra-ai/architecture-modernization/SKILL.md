---
name: architecture-modernization
description: Plan a safe, incremental modernization or migration of an existing system. Covers baseline, target state, seams, strangler slices with interop, data migration, rollback, exit criteria and measurable outcomes. Use this skill whenever the user mentions breaking up a monolith, rewriting, replatforming, cloud migration, a framework or database upgrade, "legacy", or asks for the safest order in which to change a running system, even if they never say "modernization". Do not use it for greenfield design (use architecture-design) or for a pure assessment (use architecture-audit).
license: Apache-2.0
compatibility: Works with file read and search tools. Uses architecture-audit output when available; the archsutra CLI is optional.
---
# Architecture Modernization

Plan change to a system that must keep running. The goal is a sequence of small, reversible steps, each of which leaves the system better and shippable.

## Why this skill is built the way it is

- Rewrites fail most often because they stop delivering value for months while the old system keeps changing. Incremental slices keep value flowing and risk small.
- Migrations hurt at the data layer and at the edges (consumers you cannot see). So data movement and interop get their own plan, not a footnote.
- "Modern" is not a goal. A migration is justified only by a measurable outcome, so you define the outcome first.

## Workflow

1. **Baseline.** Use an architecture-audit report (or run that skill first) for the current state, risks and blind spots. If none exists, map the system enough to name its parts and dependencies.
2. **Define why and how success is measured.** Pick 2 to 4 outcomes with numbers (lead time, incident rate, cost per request, the scale limit you will hit). If the user cannot name any, say the migration is not yet justified and ask.
3. **Define the target state** only as far as the outcomes require. Avoid a perfect end-state diagram nobody can reach.
4. **Find seams.** Look for modules with few inbound dependencies, stable interfaces and owned data. Use [references/seam-finding.md](references/seam-finding.md).
5. **Cut slices.** Prefer strangler-style slices. For each slice write scope, interop, data migration, rollback, verification and exit criteria using [references/slice-template.md](references/slice-template.md).
6. **Build the safety net first.** Characterization tests, contract tests and fitness functions before the first change. If none exist, the first tasks are tests, not changes.
7. **Sequence by risk removed per effort and by dependencies.** Put the riskiest unknown early as a cheap experiment.
8. **Keep a risk register** ([references/risk-register.md](references/risk-register.md)): what could stall the program (people, data quality, vendor limits) and the cheapest early test of each.

## Rules that keep migrations survivable

- **Every slice has a rollback** that was tested, or the slice is not ready. Say when rollback stops being possible (the point of no return) and gate that step.
- **Expand, migrate, contract** for data: add the new structure, move data while both work, remove the old only after verification.
- **Reject big-bang rewrites** unless the user states a constraint that forces one; then record the reason and shrink the blast radius anyway.
- **Do not break consumers you cannot see.** Treat unknown consumers as present; version and deprecate with dates.
- **Label claims** `observed`, `inferred`, `proposed` or `unknown`. Most of the plan is `proposed`; the current state must be `observed`.

## Files the reader gets

Write the plan as both `docs/architecture/modernization.md` and `docs/architecture/modernization.html`. Save the Markdown, then run `archsutra html docs/architecture/modernization.md`. Do not hand-write HTML. Do not leave the plan only in chat.

## Hand-offs

Use architecture-design for a component that is genuinely new. Use threat-modeling when a slice changes a trust boundary. Run architecture-verification before presenting the plan.
