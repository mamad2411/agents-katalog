---
name: ux-build
description: "Design, implement, or refactor frontend UI/UX flows, components, forms, dashboards, and interactions with evidence-based usability patterns. Use during actual UI creation or UX fixes, not only after a review."
---

# Build or refactor UI with UX evidence

## Scope

This skill applies to frontend implementation and redesign. Preserve the user's requirements, project conventions, design system and scope. You may design and code only actions permitted by the current task.

When implementing complex states or widgets, read `references/implementation-contracts.md` for practical behavior contracts and acceptance checks.

## Procedure

1. Determine user goal, audience, critical path, current components/design system and constraints. Identify risky states (loading, errors, empty, success, mobile, permissions, interruption).
2. Use `ux-diagnose` taxonomy or the specific specialist playbook(s) to choose patterns. Map each decision to a *user problem*, not a superficial law-name citation. Use progressive disclosure; load only relevant specialist guidance.
3. When a general pattern is not enough, inspect the matched category in `../ux-diagnose/references/remediation-recipes.json` and its counterexample/acceptance test; check `cross-law-conflicts.json` before making a tradeoff. Prefer existing accessible components, design tokens, routing and state infrastructure. Avoid adding dependencies or inventing new patterns without compelling benefit. Keep native control semantics.
4. Implement complete behavior: affordances, focus, labels, loading/cancellation, validation, persistence, responsive layout, keyboard access, error recovery and truthful confirmations appropriate to the task.
5. Inspect the real UI when runtime tools are available. Test at least one happy path and one failure/recovery path, plus keyboard and narrow viewport when relevant; add focused automated tests appropriate to repo conventions.
6. Summarize the user-facing change, the key principle(s) and what was actually tested. Explicitly list unverified behaviors if browser/user testing was unavailable.

Do not optimize aesthetics while leaving core task breakage; do not fabricate progress; do not simplify away choices/consent; do not deploy or publish merely because UI changed. For validation guidance use `ux-validate`.
