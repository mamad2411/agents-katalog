---
name: design-audit
description: Audit an existing UI for usability, hierarchy, accessibility, and conversion problems. Reviews a live URL, screenshot, or codebase against heuristics and reports prioritized issues with fixes. Use when the user says "audit this UI", "what's wrong with this screen", "UX review", "find the problems", "why is this confusing", or has existing interface to critique. Part of the Product Design set. Can drive a browser for live audits.
---

# Design — Audit

Find what's broken in an EXISTING interface and prioritize fixes by impact. The output is a ranked, actionable issue list — not a vibe check. Every issue ties back to the user's goal, so you're fixing what matters, not nitpicking pixels.

## When to use
- An existing screen/flow/site needs critique before iterating.
- "Why is conversion/completion low here?"
- Pre-redesign baseline: what to keep, what to fix.

## When NOT to use
- Nothing's built yet → `design-ideate` / `design-get-context`.
- You want competitor benchmarks → `design-research`.
- Final conformance check on a prototype you just built → `design-qa` (compares to a spec; audit is open-ended).

## Inputs
- **Target**: live URL, screenshot/image, or component path.
- `./design/context.md` (goal, user, success) if it exists — anchors severity.

## Workflow
1. **Capture the UI**: for a URL, use a browser-automation tool (snapshot + screenshot) or a web-fetch tool; for an image, use a vision/read tool; for code, read the components.
2. **Run heuristic passes**:
   - **Hierarchy**: is the primary action obvious within ~2 seconds? One clear focal point?
   - **Clarity**: labels, microcopy, empty/error/loading states present and understandable?
   - **Flow**: step count, friction, dead ends, unnecessary choices.
   - **Accessibility**: contrast ratios, focus order, target sizes (≥44px), alt text, keyboard reachability. (Note: full WCAG conformance needs manual assistive-tech testing — flag it.)
   - **Consistency**: spacing rhythm, type scale, component reuse vs one-offs.
   - **Conversion**: distractions competing with the CTA, trust cues, friction before value.
3. **Score each issue**: severity (high/med/low) × effort (S/M/L). Propose a concrete fix per issue.
4. Write `./design/audit.md`, sorted by severity. Hand fixes to `design-ideate`/`design-prototype`.

## Output: ./design/audit.md
```
target: https://app.example.com/signup   goal: ↑ signup completion
| # | area       | issue                              | sev  | fix                              | eff |
|---|------------|------------------------------------|------|----------------------------------|-----|
| 1 | hierarchy  | 3 CTAs same weight above the fold  | HIGH | one primary, demote 2 to links   | S   |
| 2 | clarity    | no error state on failed submit    | HIGH | inline field errors + summary    | M   |
| 3 | a11y       | CTA contrast 3.1:1 (<4.5 req)      | HIGH | darken accent to #1A6FؚE         | S   |
| 4 | flow       | asks company size before email     | MED  | move optional fields after signup| M   |
| 5 | a11y       | keyboard focus not visible         | MED  | add focus ring                   | S   |
notes: full screen-reader pass still required (manual AT).
verdict: 3 HIGH issues likely suppressing completion; fix 1-3 first.
```

## Quality bar
- Every issue ties to the user goal/success criteria — no taste nitpicks.
- Severity reflects user impact, not personal preference.
- Each issue has a concrete, implementable fix (not "improve hierarchy").
- Accessibility findings state what was checked vs what needs manual AT validation.
- Confirmed problems are separated from hypotheses ("likely" vs "is").

## Common pitfalls
- **Nitpicking** — listing 30 cosmetic issues buries the 3 that matter. Prioritize ruthlessly.
- **Overclaiming a11y** — automated contrast/focus checks ≠ full WCAG. Be honest about the gap.
- **Vague fixes** — "make it clearer" isn't actionable; "merge the two CTAs, primary = Sign up" is.
- **Ignoring the goal** — an audit untethered from the goal optimizes the wrong things.

## Handoff
`audit.md` → `design-ideate` (if fixes need new directions) or `design-prototype` (if fixes are direct edits). HIGH issues are the priority backlog.

## Tooling
Live URL audit needs a browser-automation tool (snapshot/screenshot) or web-fetch; image audit needs a vision/read tool; code audit needs file reads. Degrades to a heuristic review of whatever can be captured; state what couldn't be verified.
