---
name: designer-accessibility-test-plan
description: Plan accessibility validation across automated, manual, and assistive-tech layers, mapped to WCAG 2.2 AA and EAA (Jun 28 2025) obligations.
---
# Accessibility Test Plan
A layered plan that catches issues automated tools miss and produces evidence of conformance, not just a green dashboard.

## When to Use
- Pre-release of any user-facing flow shipping to EU/UK markets (EAA).
- Adding new components to a design system.
- Major redesign of forms, navigation, media, or data tables.
- VPAT/ACR refresh or procurement response.
- Remediation sprint following an audit.

## Stack Baseline (2026)
- **Standards:** WCAG 2.2 AA, EN 301 549 v3.2.1, ATAG 2.0 (for authoring tools), EAA enforcement (Jun 28 2025).
- **Automated:** axe DevTools (browser + Linter), Lighthouse, ANDI, Storybook a11y addon, Pa11y CI.
- **Assistive tech matrix:** NVDA + Firefox/Chrome (Win), JAWS + Chrome (Win), VoiceOver + Safari (macOS/iOS), TalkBack + Chrome (Android).
- **Visual & input:** zoom 200% / 400%, Windows High Contrast / `forced-colors`, `prefers-reduced-motion`, keyboard-only, switch control, voice control.
- **Design source:** Figma with Variables for tokens, contrast plugins (Stark, Able), Dev Mode for spec hand-off.

## Prerequisites
- Component inventory and target screens identified.
- Design tokens for color/typography/focus available.
- Test environment with seeded data covering empty/error/long-content states.
- Recruited participants with disabilities for at least one round (paid, consented).

## Instructions
1. **Build a WCAG 2.2 AA conformance matrix** (rows = success criteria; columns = screen/component; cells = Pass/Fail/N-A + evidence link). Include new 2.2 criteria: 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (Min), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication.
2. **Layer the test plan:**
   | Layer | Coverage | Tools | Catches |
   |---|---|---|---|
   | Automated | ~30–40% of issues | axe, Lighthouse, Storybook a11y | Contrast, missing alt, ARIA misuse |
   | Manual structural | Headings, landmarks, name/role/value | DevTools accessibility tree, ANDI | Semantic gaps |
   | Keyboard | Tab order, focus visible, traps, skip links | Keyboard only | Operability |
   | Screen reader | NVDA, JAWS, VoiceOver, TalkBack | Per matrix above | Announce correctness |
   | Visual | Zoom 200/400%, forced-colors, dark mode | Browser, OS settings | Reflow, color reliance |
   | Motion | `prefers-reduced-motion` | OS toggle | Vestibular safety |
   | User testing | Participants with disabilities | Moderated remote | Real-world friction |
3. **Write test scripts per component** — preconditions, steps, expected announcement/behavior, WCAG SC reference.
4. **Recruit participants** across screen reader, low vision, motor, and cognitive profiles. Compensate fairly. Plan accessible session logistics (captions, extended time, async option).
5. **Triage findings** by severity (Blocker/Major/Minor/Cosmetic) and WCAG SC. Tag owner and target release.
6. **Re-test on fix** with the same script; close only when assistive-tech evidence is captured (recording or note).
7. **Produce an ACR/VPAT-style summary** referencing EN 301 549 for EU procurement.

## Common Pitfalls
| Pitfall | Why it hurts | Fix |
|---|---|---|
| "Axe passed, ship it" | Catches ~30–40% of issues | Always add manual + AT layers |
| Testing only Chrome + VoiceOver | Misses NVDA/JAWS-specific bugs | Run full AT matrix |
| Skipping zoom and forced-colors | Reflow and contrast bugs slip through | Add to every component checklist |
| No users with disabilities | Lived-experience issues invisible | Recruit ≥3 per round, compensate |
| Treating 2.2 as optional | EAA enforcement risk in EU | Include all new 2.2 SCs in matrix |
| Focus indicator removed for "polish" | Fails 2.4.7 / 2.4.11 | Token-driven, never `outline:none` alone |
| Decorative motion without reduced-motion path | Vestibular harm + 2.3.3 fail | Honor `prefers-reduced-motion` globally |

## Output Format
Accessibility test plan: scope, conformance target, WCAG 2.2 matrix, AT/browser matrix, test scripts per component, participant plan, severity rubric, and a remediation tracker linked to issues.

## Authoritative References
- https://www.w3.org/TR/WCAG22/
- https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
- https://www.deque.com/axe/devtools/
- https://www.w3.org/WAI/ARIA/apg/practices/
- https://webaim.org/projects/screenreadersurvey/
