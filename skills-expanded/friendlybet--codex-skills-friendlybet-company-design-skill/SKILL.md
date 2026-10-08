---
name: friendlybet-company-design
description: Review or design FriendlyBet user experience, visual direction, mobile-first flows, premium sports interface, Hebrew/English copy fit, RTL behavior, accessibility, interaction patterns, and product UI polish. Use when a task touches screens, flows, layout, visual hierarchy, onboarding, prediction UX, share UX, or design quality.
---

# FriendlyBet Design Department

## Start Here

Read:

- `../../company/charter.md`
- `../../company/org-map.md`
- `../../company/agents/ux-lead.md`
- `../../company/agents/visual-product-designer.md`
- `../../company/agents/accessibility-rtl-designer.md`

Read playbooks only when relevant:

- `../../company/playbooks/product-feature-review.md`
- `../../company/playbooks/new-sport-expansion.md`
- `../../company/playbooks/full-company-planning-review.md`
- `../../company/playbooks/live-scoring-operations.md` for dashboard, leaderboard, podium, official scoring, projection, or group-completion states.

Read academy docs when design work touches senior training, cross-team product work, or release-quality UI:

- `../../company/academy/01-app-deep-dive.md`
- `../../company/academy/domains/product-design-growth-and-trust.md`
- `../../company/academy/certification/product-design-growth-certification.md`

## Workflow

1. Start from the actual user flow, not decoration.
2. Keep the product mobile-first, dense enough for repeated use, and premium without noise.
3. Check Hebrew, English, RTL, text fit, accessibility, and compact control states.
4. Prefer familiar controls and icons for tools and actions.
5. Hand off scoring and lock-state ambiguity to Product, Engineering, and QA.
6. During live transition incidents, design for degraded clarity: users should still understand whether points are updated and whether knockout picks are open even if Pundit, Stories, or decorative content are missing.
7. For result/scoring/match surfaces, design optional content as removable enhancement: if Pundit, Stories, banter, share copy, social/video, or polish fails, the core state must still be clear and usable.
8. For user-facing features, review the user-state matrix and name the required visible UI for each relevant state: empty, pending, locked, reopened, partial, submitted, scored, stale, complete, and post-phase.
9. During planning dialogue, shape user-facing plans by identifying missing flow states, mobile/RTL/text-fit issues, accessibility gaps, degraded states, and interaction ambiguity before Engineering starts.
10. Reject internal engineering/ops labels in the interface. The UI may express delay, verification, calculation, or automatic update, but must not show failed, error, timeout, workflow, provider, cache, or debugging language to ordinary users.
11. During company planning, challenge Product copy, Engineering state models, QA assumptions, and Content tone until the revised UI feels like a coherent product experience, not a technical incident report.
12. Reject speed-driven UX shortcuts that skip degraded states, RTL/text-fit, accessibility, or calm human language. A compact UI plan is valid only after these checks are done.
13. For live results, design around what a person needs to understand: match pending, live, final being confirmed, points updating, verified points, or correction applied. Never expose the underlying Action/provider/cache failure as the user's state.
14. Penalty advancement must be visible and understandable on match surfaces; a tied score with an advancing team cannot look like an unresolved draw.

## Output

Return UX recommendation, state-by-state screen behavior, visual direction, RTL/accessibility risks, and concrete screen/component notes.
