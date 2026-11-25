---
name: wcag-audit
description: Conduct a WCAG 2.2 AA conformance audit combining automated tooling (axe, Pa11y, Lighthouse), manual checks, and assistive-tech testing - producing a remediation-ready findings report. Use before launches, procurement, accessibility statements, or compliance deadlines.
source: self
date_added: 2026-04-30
---

# WCAG Audit

A conformance audit is a structured assessment of a digital product against WCAG 2.2 (and where required, EN 301 549, ADA, EAA-2025). Automation finds ~30–40% of issues; the rest require human judgement and AT.

## Stack Baseline (2026)

| Layer | Tool |
| --- | --- |
| Automated rules | axe-core 4.10+, Pa11y 8, Lighthouse 12, IBM Equal Access |
| Browser DevTools | Chrome DevTools Issues + a11y panel, Firefox Accessibility Inspector |
| Manual + AT | NVDA, JAWS, VoiceOver (macOS/iOS), TalkBack, Narrator, Dragon |
| Color / contrast | TPGi Colour Contrast Analyser, browser DevTools |
| Mobile | Accessibility Scanner (Android), Accessibility Inspector (iOS) |
| Reporting | ARC Toolkit, Accessibility Cloud, custom Markdown templates |

## Scope Definition

1. Pages/components/flows in scope (sample to cover unique templates + critical user journeys).
2. WCAG version + level (default 2.2 AA).
3. Browsers, OS, and AT pairings (e.g., NVDA + Firefox/Chrome on Windows; VoiceOver + Safari on macOS/iOS).
4. Authenticated vs anonymous coverage.
5. Out-of-scope items declared.

## Test Method (per page/component)

1. **Automated scan** — `axe-core` via Playwright/Cypress; capture violations with selectors and rule ID.
2. **Manual checks** — keyboard-only, focus order, focus visibility (2.4.13), reflow at 320 CSS px (1.4.10), 200% zoom (1.4.4), animations (2.3.3), error identification (3.3.1–3).
3. **AT walkthrough** — screen reader linearization, headings, landmarks, names/roles/values, live regions, dialog focus management.
4. **Color/contrast** — text 4.5:1, large text 3:1, non-text UI 3:1.
5. **Forms** — labels, autocomplete, error association, required indication.
6. **Media** — captions, transcripts, audio description, autoplay control.
7. **Mobile** — touch target 24×24 (2.2 AA SC 2.5.8), gesture alternatives.

## WCAG 2.2 New Criteria to Verify

- 2.4.11 Focus Not Obscured (Min) AA, 2.4.12 (AAA), 2.4.13 Focus Appearance (AAA).
- 2.5.7 Dragging Movements AA.
- 2.5.8 Target Size (Minimum) AA.
- 3.2.6 Consistent Help A.
- 3.3.7 Redundant Entry A, 3.3.8 Accessible Authentication (Min) AA, 3.3.9 (AAA).

## Findings Report (per issue)

- ID, page/component, screenshot.
- WCAG SC + level.
- Severity (Blocker / Critical / Serious / Moderate / Minor).
- User impact + AT impact.
- Steps to reproduce, including AT setup.
- Recommended fix with code example.
- Owner + target date.

## Severity Heuristic

| Severity | Definition |
| --- | --- |
| Blocker | Prevents task completion for AT users |
| Critical | Major barrier; common path |
| Serious | Significant barrier; less common path |
| Moderate | Workaround exists |
| Minor | Cosmetic / minor inconvenience |

## Common Pitfalls

- Relying on automated scans alone — misses ~60–70% of real issues.
- Testing only on desktop — mobile AT differs significantly.
- No AT testing — "passes axe" ≠ "usable with screen reader".
- Reports without code-level fixes — nothing changes.
- Auditing once, never again — regressions reintroduce issues.

## Output

- Findings spreadsheet/JSON + Markdown summary.
- VPAT/ACR for procurement when required.
- Remediation roadmap with milestones.
- Re-audit plan post-fix.

## References

- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- EN 301 549 v3.2.1
- WAI-ARIA 1.2 / APG — https://www.w3.org/WAI/ARIA/apg/
- axe-core rules — https://dequeuniversity.com/rules/axe/
- Deque University, TPGi Knowledgebase
