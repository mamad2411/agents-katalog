---
name: qa-engineer-accessibility-test-plan
description: Author a release-grade accessibility test plan covering WCAG 2.2 AA, EN 301 549, automated + manual + AT testing, owners, and exit criteria. Use when planning a11y testing for a feature, release, or VPAT/ACR evidence package.
source: self
date_added: 2026-05-01
---

# Accessibility Test Plan (QA)

A practical, auditable plan that turns "we want it accessible" into a measurable, executable test scope with clear owners, tooling, and exit criteria mapped to WCAG 2.2 / EN 301 549 / ADA Title II.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Standard | WCAG 2.2 AA, EN 301 549 v3.2.1, ADA Title II (effective 2026 for state/local gov), Section 508 |
| Automated | axe-core 4.10 (Pa11y, @axe-core/playwright, Cypress-axe), Lighthouse 12, Accessibility Insights |
| Manual | Tab Stops, color contrast (Stark), zoom 200% / 400%, reflow, reduced motion |
| AT matrix | NVDA + Firefox/Chrome (Win), JAWS + Chrome (Win), VoiceOver + Safari (macOS/iOS), TalkBack + Chrome (Android) |
| Reporting | VPAT 2.5 / Accessibility Conformance Report (ACR), Jira label `a11y`, axe HTML reports artifact |

## When to Use

- New feature reaching beta or GA.
- Release that adds custom widgets, charts, media, or dynamic content.
- Producing or refreshing a VPAT/ACR for procurement.
- Quarterly conformance regression sweep.

## Plan Structure

1. **Scope** — list pages, components, and user flows in/out of scope. Tag by criticality (revenue, sign-up, account, regulatory).
2. **Standards** — WCAG 2.2 AA + which AAA criteria your org commits to (commonly 2.4.12 Focus Not Obscured Enhanced, 1.4.6 Contrast Enhanced).
3. **User scenarios** — 5–10 realistic end-to-end flows (sign-up, checkout, dashboard) executed across 3 personas: keyboard-only, screen-reader, low-vision (zoom + contrast).
4. **Test layers**
   - **Static / unit**: eslint-plugin-jsx-a11y; jest-axe per component.
   - **Component**: Storybook + `@storybook/addon-a11y`; Chromatic snapshots in dark / high-contrast / 200% zoom.
   - **E2E automated**: Playwright/Cypress + axe on every critical page.
   - **Manual**: 12-step keyboard protocol; contrast spot-checks; reflow @ 320 CSS px; 200% & 400% zoom; reduced-motion.
   - **Assistive tech**: AT matrix above × top scenarios.
   - **Forms & errors**: identify, label, instructions, error suggestions (3.3.1–3.3.4, 3.3.7, 3.3.8 cognitive AA).
   - **Media**: captions (1.2.2), audio description (1.2.5), transcripts.
5. **Environments** — dev / staging / accessible-fixtures. Note that prod content (CMS-authored) needs separate sweep.
6. **Tooling matrix** — what runs in CI vs. nightly vs. manual.
7. **Owners & RACI** — engineering owns code defects; design owns visual; content owns alt-text; QA owns coordination.
8. **Defect taxonomy** — severity by user impact, not just WCAG level (Blocker = task impossible with AT; Critical = workaround required).
9. **Exit criteria** — see below.
10. **Evidence pack** — axe JSON, manual checklist, AT session recordings, ACR draft.

## Exit Criteria

- 0 axe `critical` or `serious` violations on in-scope pages.
- 0 Blocker or Critical manual defects.
- All in-scope flows completed end-to-end with NVDA + VoiceOver.
- Keyboard tab order verified; no traps; focus visible meeting 2.4.11.
- WCAG 2.2 new SC verified: 2.4.11 Focus Not Obscured, 2.5.7 Dragging, 2.5.8 Target Size, 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication.
- Reflow at 320 CSS px / 400% zoom: no horizontal scroll, no clipped content (1.4.10).
- Reduced-motion respected (2.3.3 AAA, but treat as AA).
- ACR/VPAT updated and signed off by accessibility lead.

## Coverage Matrix (example excerpt)

| Flow | Automated (axe) | Keyboard | NVDA | JAWS | VoiceOver | TalkBack | Zoom 200% |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Sign-up | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Checkout | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ | ✅ |
| Settings → 2FA | ✅ | ✅ | ✅ | ⏳ | ✅ | — | ✅ |

## CI Snippet

```yaml
# .github/workflows/a11y.yml
name: a11y
on: [pull_request]
jobs:
  axe:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:a11y          # playwright + @axe-core/playwright
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: a11y-report, path: artifacts/a11y/** }
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Treating axe pass as "accessible" | axe catches ~30% of issues; manual + AT mandatory |
| Only Chrome + VoiceOver | Real users use NVDA on Windows; JAWS in enterprise |
| Snapshotting only desktop light mode | Add dark, high contrast, 200% zoom, reduced motion |
| CMS content excluded | Audit author tooling and add author guidelines |
| One-off sweeps before launch | Bake checks into PR + nightly + release gates |
| ACR drafted by marketing | Must be authored from real test evidence |

## Output Format

The plan ships as a single Markdown doc with: scope, standards, scenarios, layered tests, RACI, environments, exit criteria, schedule, risks, evidence list. Pair with the coverage matrix and a defect summary at exit.

## References

- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- EN 301 549 v3.2.1: <https://www.etsi.org/deliver/etsi_en/301500_301599/301549/>
- ADA Title II Web Rule (DOJ 2024, effective 2026): <https://www.ada.gov/resources/2024-03-08-web-rule/>
- ITI VPAT 2.5: <https://www.itic.org/policy/accessibility/vpat>
- W3C — Planning and Managing Accessibility: <https://www.w3.org/WAI/planning-and-managing/>
- Deque axe rules: <https://dequeuniversity.com/rules/axe/>
