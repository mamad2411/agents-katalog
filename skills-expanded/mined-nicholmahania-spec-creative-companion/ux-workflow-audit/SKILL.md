---
name: ux-workflow-audit
description: End-to-end UX audit of a web app from a brand-new user's perspective. Use this skill whenever the user asks to review, audit, test, critique, or improve the usability, UX, flow, or onboarding of an app, site, or prototype — including requests like "look this over," "does this make sense," "find what's confusing," or "test my app." Trigger even for partial reviews of a single page or flow; the same method applies at any scale.
---

# End-to-End UX Workflow Audit

Audit an application the way a confused first-time user experiences it — then hand back a prioritized, non-destructive punch-list.

## Perspective (hold this the entire time)

You are an entirely new, uninitiated user. You have never seen this platform. You find it confusing and over-complicated until proven otherwise. You do not get credit for prior knowledge:

- If a label only makes sense once you know how the system works, it fails.
- If a step requires guessing, external research, or reading documentation, it fails.
- If you hesitate even briefly about what to click next, log it — hesitation is data.

Actively resist the builder's curse: knowing how it's *supposed* to work. When in doubt, ask "would my least technical relative get past this screen?"

## Mechanical Sequence

Evaluate page by page, in the order a real user meets them:

1. **Start at the login/entry screen.** First impressions count: is it obvious what this app is and what to do first?
2. **Follow the onboarding path** exactly as a new account would experience it.
3. **Proceed to the core action** — the single most important thing a user comes here to do.
4. **Then sweep remaining pages** (settings, secondary features, edge screens) in navigation order.

Do not skip ahead to interesting pages. The sequence *is* the finding — broken order is itself a defect.

**If browser automation (e.g., Playwright) is available:** actually load each route, click each element, submit each form with both valid and invalid input, and screenshot anything questionable. **If not:** walk the code route-by-route and simulate the same sequence, stating clearly that findings are from code review rather than live interaction.

## Granular Checklist (per page)

Systematically inspect every single one of:

- **Buttons** — label clarity, does it do what it says, disabled states explained, destructive actions guarded
- **Form fields** — labels present, formats indicated, validation messages helpful, errors recoverable without data loss
- **Modals** — escapable (X, Esc, click-outside), purpose obvious, no dead-ends
- **Settings & configuration options** — every option understandable without documentation; defaults sensible; consequences of changes clear
- **Navigation** — current location always visible; a way back always exists
- **Empty, loading, and error states** — each tells the user what's happening and what to do next

Nothing is too small. "The button says Submit but the toast says Saved" is a real finding.

## Logical Flow Verification

For each key journey (onboarding → core action at minimum), verify:

- The path is **linear and seamless** — no forks where the user must guess, no steps that dump them somewhere unexpected.
- **Zero external research required** — no step depends on knowledge the app didn't provide.
- Each step's completion visibly leads to the next — the app pulls the user forward rather than stranding them.
- Progress is never silently lost.

**Intuitive architecture standard:** Flag any feature that requires excessive explanation to use. For over-complicated settings and configuration layouts, recommend simplifications that follow clear, modern SaaS conventions (grouped sections, plain-language labels, sensible defaults, progressive disclosure of advanced options) rather than inventing novel patterns.

## Output: Prioritized Punch-List

Group all findings into a single punch-list, ordered by severity:

- **P1 – Blockers:** A new user cannot proceed (broken flow, dead-end, incomprehensible required step)
- **P2 – Friction:** User can proceed but with confusion, hesitation, or error-prone guessing
- **P3 – Polish:** Inconsistencies, wording, minor visual issues

Each item: **where** (page/element), **what** a new user experiences, **why** it fails, and **the fix**.

## Non-Destructive Fixes

- Fixes must not break existing feature logic or lock up working code. Prefer the smallest change that resolves the confusion: relabeling, reordering, adding a hint, adjusting a default.
- If a proper fix requires structural change, say so — but still offer the minimal interim fix alongside it.
- Never silently refactor working code as part of an audit. Auditing and rebuilding are separate jobs; deliver the punch-list first and let the user choose what to act on.
