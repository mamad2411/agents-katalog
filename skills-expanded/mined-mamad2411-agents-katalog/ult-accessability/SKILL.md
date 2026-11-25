---
name: ult-accessability
description: Default router for the ult-accessability plugin. Routes accessibility audits, WCAG 2.2 AA/AAA guidance, contrast checks, fixes, and verification to the matching specialist skill(s). Use when asked to audit accessibility, check WCAG conformance, fix a11y issues, verify contrast, test keyboard or screen reader support, or when the request spans more than one accessibility area. Also use for /ult-accessability.
license: MIT
metadata:
  author: ult-accessability
  version: "1.0.0"
---

# Ult Accessability router

Load this skill first. Then load only the specialist skills the table names. Do not stay in the router after routing.

## Default: the full run

A broad request ("audit this", "make this accessible", "check then fix") runs the whole pipeline, in order:

1. **Audit** — load `audit`, check the target, produce findings.
2. **Initial report** — file per [REPORT-TEMPLATE.md](../../references/REPORT-TEMPLATE.md).
3. **Fix** — load `fix`, one fix per finding with `file:line` refs.
4. **Re-verify** — load `testing`, re-run the exact checks that failed.
5. **Final before/after report** — file per [REPORT-TEMPLATE.md](../../references/REPORT-TEMPLATE.md); every initial finding appears exactly once.

Narrow requests skip to the matching step; the hard rules below still apply.

## Route

Match the user request. Load every matching specialist.

| Request | Load | Then |
|---------|------|------|
| Full run: audit, fix, verify ("audit this", "make it accessible") | `audit`, then `fix`, then `testing` | Follow the pipeline above |
| Audit / review / "is this accessible" (no fix yet) | `audit` | File the initial report; offer `fix` next |
| WCAG AA rules, A/AA criteria, "does this meet AA" | `wcag-aa` | Apply its POUR rules; route failures to `fix` |
| WCAG AAA rules, enhanced criteria, "does this meet AAA" | `wcag-aaa` | Apply its enhanced rules; route failures to `fix` |
| Contrast ratio, color contrast, "does this pair pass" | `contrast-color` | Measure, never eyeball |
| Fix audit findings / remediate issues | `fix` | Consume findings; verify each fix with `testing` |
| Test / verify / keyboard / screen reader / zoom / reflow | `testing` | Run its automated + manual protocols |
| Live page / URL walkthrough | `audit` + live checks | See Live pages below |

If two specialists disagree, live evidence wins; the criterion text in [WCAG.md](../../references/WCAG.md) wins on interpretation.

## Hard rules

1. **Evidence-led, always.** Label every claim: live (real page in a browser) > markup (DOM/code read) > screenshot (pixels only) > hypothesis (unverified). Never mix them in one claim.
2. **Measure before fixing.** Ratios come from real colors, sizes from real dimensions — never invented, never eyeballed. Contrast goes through `contrast-color`.
3. **Every criterion lands in exactly one home:** a finding, checked-and-clean, suppressed (with owner + revisit date), or not verifiable from this input. Silence is a false pass.
4. **Re-verify after every fix** with the same check that failed. Nothing closes without passing evidence.
5. **Cite criteria** as `WCAG 2.2 SC x.x.x (Name, Level)` — full table in [WCAG.md](../../references/WCAG.md).
6. **Scope honesty.** This is expert review, not legal certification: findings do not certify ADA/Section 508 conformance and do not substitute for testing with people who use assistive technology.

## Live pages (BrowserOS neo)

When a URL can run, drive the real page: snapshot → act → verify. Work in your own tab, call `name_session` early, and follow [BROWSEROS-NEO.md](../../references/BROWSEROS-NEO.md) for the keyboard walk, focus, target-size, contrast, zoom/reflow, and forced-colors checks. A live page widens what is verifiable but never relaxes the four-homes accounting.

## Output

```markdown
## Evidence
| Signal | Input/conditions | Result | Evidence |
|--------|------------------|--------|----------|
| Contrast 1.4.3 | Hero text, computed colors | 3.2:1 fail | markup |

## Findings
- **[skill]** Issue. Location: `path:line` or page region
  - Observed:
  - Evidence: live | markup | screenshot | hypothesis
  - WCAG: `WCAG 2.2 SC x.x.x (Name, Level)`
  - Fix:

## Next specialist
- skill-name — why
```

## Specialists

| Skill | Path |
|-------|------|
| audit | `../audit/SKILL.md` |
| wcag-aa | `../wcag-aa/SKILL.md` |
| wcag-aaa | `../wcag-aaa/SKILL.md` |
| contrast-color | `../contrast-color/SKILL.md` |
| fix | `../fix/SKILL.md` |
| testing | `../testing/SKILL.md` |
