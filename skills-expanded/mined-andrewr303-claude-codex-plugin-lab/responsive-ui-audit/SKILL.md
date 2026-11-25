---
name: responsive-ui-audit
description: "Use to find, rank, and fix mobile/responsive formatting defects including overflow, clipping, fixed widths, broken navigation, bad forms, inaccessible controls, and missing responsive states."
---

# Responsive UI Audit

Use this skill when the user asks to audit, fix, debug, or improve mobile
and responsive formatting on an existing page, component, or app.

## Required References

Read `../../references/responsive-audit-checklist.md`,
`../../references/mobile-repair-playbook.md`, and
`../../references/verification-matrix.md`. If accessibility or touch issues
are involved, also read `../../references/accessibility-touch.md`.

## Audit Procedure

1. Inspect the active stack, route, component tree, styling system, tokens,
   and existing responsive conventions.
2. Check for parallel mobile components or mobile-specific routes before
   changing a desktop component.
3. Form at least two plausible root-cause hypotheses for non-obvious
   breakage, then falsify them with file reads, screenshots, DOM inspection,
   computed styles, or tests.
4. Run `scripts/audit_responsive_static.py` when local files are available.
5. Verify at a practical viewport matrix: 320, 360, 390, 414, 768, 1024,
   1280, and an embedded/container width if the component can be nested.
6. Fix the smallest source-level problem, not only the visible symptom.

## Finding Format

For reviews, lead with findings:

```md
### [Severity] [Issue]
- Confidence:
- Evidence:
- Impact:
- Fix:
- Verification:
```

For implementation, hand off changed files and verification commands. Do
not claim visual success from build or typecheck alone.
