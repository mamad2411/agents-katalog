---
name: hci-web-accessibility
description: Makes web interfaces usable and accessible, applying HCI principles and WCAG 2.2 AA. Use whenever the user builds or reviews HTML, CSS, React, Vue or other web UI and cares about accessibility, keyboard use, screen readers, forms, focus, color contrast, zoom, responsive layout or legal compliance, asks whether colors pass contrast, or wants an accessibility audit, even if they only say "check my page for problems". Lints HTML, calculates contrast ratios, and explains each fix with the user impact.
---

# hci-web-accessibility

Build web pages that work for keyboard users, screen reader users, people with low vision, motor limits and cognitive load. Builds on `hci-foundations`.

```
hci-web-accessibility/
├── SKILL.md
├── scripts/
│   ├── lint_html_a11y.py       static WCAG checks on HTML files (alt, labels, names, headings, ARIA refs, zoom)
│   └── contrast_ratio.py       WCAG contrast ratio with pass or fail and a passing suggestion
└── references/
    └── wcag-checklist.md       structure, text alternatives, color, keyboard, forms, targets, motion, testing
```

## When to use

- Writing or reviewing a page, component, form or design system
- An accessibility audit, a complaint, or a compliance requirement
- Choosing colors, and checking whether text and controls are readable
- Fixing keyboard traps, missing labels, focus styles or zoom problems

## Workflow

1. **Know the context**: users, key tasks, framework (plain HTML, React, Vue), and the target level (usually WCAG 2.2 AA).
2. **Lint the markup**: `python3 scripts/lint_html_a11y.py site/` (a file or a folder). For component frameworks, lint the rendered HTML (build output or saved page); templates with JSX or directives are not plain HTML.
3. **Check colors**: `python3 scripts/contrast_ratio.py "#777" "#fff" --suggest`. Need 4.5:1 for normal text, 3:1 for large text and for UI components and focus indicators. Use `--suggest` to get the nearest passing color.
4. **Fix in priority order**: things that block use (no names, labels, keyboard access, zoom blocked), then structure (headings, landmarks, lang, title), then comfort (contrast, motion, target size).
5. **Prefer native HTML** over ARIA. Add ARIA only for what native elements cannot express, and then add the keyboard behavior as well.
6. **Explain each fix** with who it helps ("screen reader users hear nothing for this button") and the WCAG criterion.
7. **Verify by hand** and say what remains: keyboard-only pass of the key task, zoom 200 and 400 percent, 320 px width, screen reader (NVDA, VoiceOver), reduced motion. A clean linter does not mean the page is accessible; tools find about a third of problems.

## Rules

- Every control has an accessible name, a role and its state; every image has the right alt
- Placeholders are not labels; color alone never carries meaning
- Never remove the focus outline without a visible replacement
- Never disable zoom; never trap keyboard focus; never use positive `tabindex`
- Make dynamic changes perceivable: live regions, focus management after navigation, error messages tied to fields
- Be honest about conformance: say what was tested and what was not
- Fix the cause in the design system, not each instance, when a pattern repeats

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, line, severity, WCAG criterion, who is affected |
| Fixes | code changes, grouped by pattern |
| Contrast results | each pair with its ratio and the criterion |
| Manual checks left | keyboard, zoom, screen reader, reduced motion |
| Follow ups | automated checks in CI, a real user test with assistive technology |

## Related skills

- `hci-foundations`: principles and evaluation reports
- `hci-rtl-localization`: right-to-left layout and multilingual pages
- `hci-microcopy`: error messages, labels and link text
- `hci-usability-testing`: test with real users, including assistive technology users
