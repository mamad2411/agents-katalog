---
name: design-qa
description: Check a prototype against its original design direction and requirements before shipping. Compares implementation to the mockup/spec/context, flags drift in layout, spacing, type, color, states, and behavior, and reports a pass/fix list. Use when the user says "design QA", "does it match the design", "check against the spec", "conformance check", or before sharing/handing off a prototype. Part of the Product Design set. Uses a browser tool for visual comparison.
---

# Design — Design QA

Verify the built prototype actually matches the intended design + requirements. Catch drift before it ships. Unlike `design-audit` (open-ended critique of any UI), QA is a *conformance check against a known source of truth* — it answers "does this match what we agreed to build?"

## When to use
- A prototype is built and you need to confirm it matches the mockup/spec before review.
- Final gate before `design-share` or dev handoff.
- "Does it match the design?", "conformance check".

## When NOT to use
- No spec/reference to compare against → that's open critique → `design-audit`.
- Nothing built yet → build it first.

## Inputs
- The **built prototype** (local URL or path).
- The **source of truth**: reference image/mockup, `./design/context.md`, `./design/ideate/*`.
- **Acceptance/success criteria** (from context).

## Workflow
1. **Capture** the implementation via a browser-automation tool — screenshots of key screens *and* states (loading/empty/error/success).
2. **Visual conformance** — compare to the reference: layout, type scale, spacing rhythm, palette, radii/shadows, iconography. Note every drift with the expected vs actual value.
3. **Behavioral conformance** — walk the flow: do interactions, states, and navigation match the intended UX?
4. **Requirements conformance** — does it satisfy the goal + success criteria from context? Any scope item missing?
5. **Accessibility sanity** — contrast, focus order, target size, keyboard reachability (flag what needs manual AT testing — automated checks aren't full WCAG).
6. Write `./design/qa.md`: PASS items + prioritized fix list (severity × effort) + a verdict.

## Output: ./design/qa.md
```
prototype: http://localhost:5173   source: ./mocks/onboarding.png + context.md
visual:
 ✓ layout matches  ✗ body type 14px (spec 16px)  ✗ accent #7C3 (spec #6366F1)
behavior:
 ✓ happy path  ✗ no error state on empty name (spec requires inline error)
requirements (vs success criteria):
 ✓ 3-step wizard  ✓ progress saved  ✗ missing "skip" affordance (scope v1)
a11y:
 ✗ CTA contrast 3.1:1 (<4.5)   manual: screen-reader pass still required
verdict: NOT READY — 4 fixes (2 HIGH: error state, contrast). Loop to design-prototype.
```

## Quality bar
- Compared against the **locked source of truth**, not personal taste.
- Every miss cites which source it violates (mock / context / success criteria) + expected vs actual.
- A11y findings distinguish automated checks from what needs manual AT validation.
- A clear verdict: READY, or NOT READY with the blocking items named.

## Common pitfalls
- **QA by opinion** — drifting into "I'd prefer..." instead of "spec says X, build shows Y".
- **Skipping states** — only checking the happy path; error/empty/loading are where drift hides.
- **Passing HIGH drift** — don't green-light something with blocking visual/behavioral mismatches.
- **Overclaiming a11y** — automated contrast/focus ≠ full WCAG conformance; say so.

## Handoff
PASS → `design-share`. FAIL → loop the fix list back to `design-prototype` (or `design-image-to-code` for visual drift), then re-QA. Don't share stakeholder-facing prototypes with unresolved HIGH items without explicitly flagging them.

## Tooling
Needs a **browser-automation tool** to capture screens/states for comparison. Without one, do a code-level + manual review and flag that visual conformance is unverified.
