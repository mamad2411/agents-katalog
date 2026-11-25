---
name: a11y-deep
description: Formal WCAG 2.2 AA accessibility discipline for Astro 7 sites, beyond the Lighthouse 0.95 floor — a zero-violations axe scan over every built page in CI via @axe-core/playwright, a codified manual smoke per release, and a WCAG-EM 2.0 sample audit for public conformance claims. Use when a client requires WCAG compliance or an audit, when fixing screen reader, keyboard navigation, or focus issues, when wiring axe into CI, when the Lighthouse score is green but users report barriers, or when writing a conformance statement. Trigger on accessibility audit, WCAG compliance, WCAG 2.2 AA, axe scan, screen reader issues, keyboard navigation, target size, or accessible authentication. Explains why a 0.95 Lighthouse score is not zero violations, why even a full axe pass finds roughly half of real issues, and which WCAG 2.2 criteria only humans can verify. Not for the Lighthouse CI floor and workflow file (perf-ci-gates), per-engine reduced-motion wiring (motion-system), or WebGL pause controls (webgl-atmosfera).
---

# a11y-deep

> Accessibility on this stack has three layers, and the automated one is the SMALLEST: an axe scan at zero violations over every built page (in CI, next to the Lighthouse gate but strictly stronger), a manual smoke pass codified per release (because five of WCAG 2.2's six new A/AA criteria have zero automation), and a WCAG-EM 2.0 audit reserved for the day a site claims conformance in public. A green Lighthouse a11y score is a tripwire, not a verdict.

## Reference materials — load when relevant

This SKILL.md is the verdict, the evidence, and the three-layer structure. Load references only when their content is needed:

- `references/axe-ci-job.md` — load when wiring the CI scan: the scan script, the workflow job, tag policy with target-size enabled, the zero-violations posture, and the documented-exclusion mechanism.
- `references/manual-checklist.md` — load when running the per-release manual smoke or scoping a full WCAG-EM audit: the codified checklist including the six WCAG 2.2 A/AA deltas as literal lines.
- `references/astro-seams.md` — load when the site uses ClientRouter, islands, or the catalog's motion/visual skills: the Astro-specific seams (route announcer, hydration windows, focus) and the composition boundaries.

## Verdict

Automated scanning uses `@axe-core/playwright` at ZERO violations across every built page, with tags `wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa` plus the `target-size` rule enabled explicitly (axe ships it disabled). The scan lives in the same CI workflow as the Lighthouse gate — perf-ci-gates owns the workflow file and keeps its 0.95 floor as the cheap early tripwire; this skill contributes the axe job and owns everything above it. Above the scan sit the two human layers: a per-release manual smoke (keyboard, screen reader, 400% reflow, form error semantics, the WCAG 2.2 deltas) and, only when a public conformance or accessibility statement is on the table, a WCAG-EM 2.0 structured sample audit. Conformance is never tool-determined.

## The evidence (verified) — why the floor is not enough

- Lighthouse's a11y category runs axe-core under the hood, but only ~66 audits from axe's 125-rule catalog — and the score is a WEIGHTED average, so a page can hold 0.95+ while failing low-weight audits outright. The floor catches collapses, not violations.
- Even a full axe pass is a minority instrument: Deque's own large-scale study puts automated detection at 57% of accessibility issues BY VOLUME (per-criterion coverage is far lower). The remaining ~43% is the manual layers' territory; W3C/WAI states plainly that some checks cannot be automated.
- WCAG 2.2 added six A/AA criteria (consistent help, redundant entry, focus not obscured, dragging movements, target size, accessible authentication). axe-core 4.13 automates exactly ONE of them — `target-size` — and ships it disabled by default. Five of six are judgment calls no gate parameter reaches. (4.1.1 Parsing is removed in 2.2 — stop chasing it.)
- WCAG-EM 2.0 (W3C Group Note, 2026-07-23) is the current canonical evaluation methodology — define scope, explore, sample representative + random pages, evaluate, report. It is newer than most tooling folklore; use it, not blog checklists, when an audit must stand up.

## The three layers

| Layer | Cadence | Instrument | Posture |
|---|---|---|---|
| 1 — axe scan | Every push (CI) | `@axe-core/playwright` over every built HTML page | Zero violations; exclusions only per-rule/per-selector, documented in the repo |
| 2 — manual smoke | Every release | Codified checklist (keyboard, NVDA + VoiceOver, 400% reflow, error semantics, 2.2 deltas) | Findings filed and fixed before release |
| 3 — WCAG-EM audit | Only for a public conformance claim | WCAG-EM 2.0 sample methodology | The claim quotes the audit, not the CI badge |

## Honest framing for es-MX briefs

Mexican law today binds GOVERNMENT portals to WCAG 2.0 AA (SFP accord, 2015); NMX-R-099-SCFI-2018 is a voluntary procurement norm; there is no private-sector mandate, though legislative initiatives point that direction. Sell this skill's discipline as direction-of-travel, brand ethics, and real usability — never as a compliance obligation a private MX client legally has. Do not oversell; overselling compliance is its own credibility bug.

## Pins (verified 2026-08-17) and review-gates

| Pin | Value | Review-gate |
|---|---|---|
| `@axe-core/playwright` | 4.13.0 (bundles axe-core ~4.13.0) | Bump with axe-core minors; re-check the disabled-rules list each bump — target-size will flip to enabled-by-default someday |
| `axe-core` | 4.13.0 (via the wrapper — no separate install needed) | New WCAG 2.2 rules may appear; re-read rule-descriptions on each minor |
| playwright | already in the stack's CI toolchain; wrapper peer is `playwright-core >= 1.0.0` (laxest peer in the catalog) | If a repo's CI drops Playwright, the flip is pa11y-ci with `runners: ['axe']` — never @axe-core/cli (Selenium + chromedriver@latest version-matching brittleness) |
| WCAG-EM | 2.0 (Group Note 2026-07-23) | Methodology document — re-check for updates when an audit is commissioned |

## Limitations and out-of-scope

- The Lighthouse floor, the workflow file, and every CI threshold belong to perf-ci-gates; this skill adds a job to that workflow, it does not fork the gate.
- Reduced-motion implementation is owned per engine by motion-system, and the WebGL pause control by webgl-atmosfera; this skill audits that they hold, it does not re-implement them.
- Color contrast pairs on brand sites are constrained by the ingested canon — the composition precedent (large-text roles, muted-copy rules) lives with brand-canon-ingest; this skill flags contrast findings but palette changes are owner decisions.
- Manual layers require a human with assistive tech; the skill codifies WHAT to test and HOW to record it, it cannot replace the tester.
