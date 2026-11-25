---
name: better-interface
description: "Holistic interface review that routes a screen, flow or repo through the better-* skills and returns one ranked verdict. Use for a whole-interface \"review this\" request."
---

# Interface review

A thin router. It owns scope, severity, consolidation and the verdict. The rules live in the domain skills; don't restate or override them here.

## Route

Load each domain skill and review in this order, so foundational failures aren't hidden by polish:

1. `better-accessibility`
2. `better-layout`
3. `better-writing`
4. `better-typography`
5. `better-colors`
6. `better-ui`

Take each skill's principles and checks, not its standalone report format. If one is missing, mark that domain `Not reviewed` and move on; don't rebuild its rules from memory. An issue two skills touch is reported once, under the skill that owns the underlying rule.

A request about a branch, PR, commit range or uncommitted changes is a change review: tell the user to run `interface-review` (user-invoked). When it hands a review back, apply the severity, cap and verdict below to `Introduced` and `Regression` findings only.

## Before judging

- State the scope (screen, flow, feature, repo). Include empty, loading, error and narrow-width states. If it's too big to inspect credibly, narrow to one complete flow and say what was excluded.
- Recon the stack, tokens, component library and any design docs (DESIGN.md, CLAUDE.md, Storybook, Figma). Write fixes in the project's idiom. Deliberate project choices (density, radius, voice) are not findings; taste is not evidence. When a shared token or guideline causes a problem, report it once against that source.
- Review is read-only unless the user also asks for fixes.

## Severity

- `HIGH`: blocks a task, misleads, hides content or controls, risks data loss, or is a repeated systemic failure.
- `MEDIUM`: meaningfully hurts comprehension, efficiency, adaptability or consistency.
- `LOW`: isolated polish.

Within a level, rank by reach: a token or shared-component fix beats the same symptom in one leaf.

These are `HIGH` on sight once the owning skill confirms them: control with no accessible name; no visible focus; pointer-only path; motion ignoring `prefers-reduced-motion`; content clipped or unreachable at 320px or 200% zoom; text failing its contrast ratio; meaning by color alone; destructive action with no confirm, undo or distinct style; truncated value with no way to reach it; hidden content with no cue; an error with no recovery; a semantic color used against its meaning; a state change carried only by motion.

## Choosing the fix

Prefer the cheapest fix that works: delete, then use the platform (native element, native focus ring), then reuse an existing token, then correct the value, and only then add something new.

## Report

1. **Scope and coverage**: scope, stack, docs found, and a table of each domain with evidence inspected and result (`N findings`, `Clear`, or `Not reviewed: reason`).
2. **Findings**: one table, at most 15 rows, ordered by severity then reach. Columns: Severity, Domain, Location (`path:line`), Before, After, Why. One row per root cause, listing every location. Triggers go first; if the cap cuts any, say how many. Never pad. With none, write "No actionable interface findings."
3. **Verification**: each check or interaction run and its result. Anything not run is `Not verified`, not a finding. Don't infer a runtime or visual claim from source alone.
4. **Verdict**: `Block` if any `HIGH` remains, else `Approve`. Never approve a domain you didn't inspect.
