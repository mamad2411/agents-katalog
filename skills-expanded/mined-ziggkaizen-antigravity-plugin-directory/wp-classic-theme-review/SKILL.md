---
name: wp-classic-theme-review
description: Reviews WordPress classic and hybrid themes for structure, compatibility, security, templates, assets, accessibility, internationalization, performance, parent-update risk, and release packaging. Use for PR review, release readiness, or upgrade validation.
license: MIT
compatibility: "General review guidance; scanner requires Python 3.9 or newer."
---

# WordPress Classic Theme Review

## Use this skill when

- Reviewing a classic or hybrid theme PR.
- Auditing an existing theme.
- Preparing a release package.
- Reviewing a child theme before a parent update.
- Investigating compatibility regressions.

## Review approach

1. Confirm theme type and compatibility baseline.
2. Inspect structure and required files.
3. Review responsibility boundaries.
4. Review templates, queries, output escaping, and hooks.
5. Review assets and editor parity.
6. Review child/parent behavior.
7. Review accessibility and internationalization.
8. Review performance and failure modes.
9. Run available deterministic checks.
10. Report prioritized findings and residual risk.

## Workflows

- [classic-theme-review-workflow.md](workflows/classic-theme-review-workflow.md)
- [parent-theme-upgrade-workflow.md](workflows/parent-theme-upgrade-workflow.md)

## Resources

- [compatibility-matrix.md](resources/compatibility-matrix.md)
- [release-readiness-checklist.md](resources/release-readiness-checklist.md)
- [source-hierarchy.md](resources/source-hierarchy.md)

## Script

Run help first:

```powershell
python scripts\scan-classic-theme.py --help
```

Then scan a theme:

```powershell
python scripts\scan-classic-theme.py C:\path\to\wp-content\themes\theme-slug
```

The script is read-only. Treat heuristic warnings as review prompts, not proof of a defect.

## Finding format

```text
Severity: critical | high | medium | low
File: <path>
Issue: <specific problem>
Impact: <user, security, compatibility, or maintenance impact>
Fix: <concrete change>
Evidence: <test, source, or code reference>
```
