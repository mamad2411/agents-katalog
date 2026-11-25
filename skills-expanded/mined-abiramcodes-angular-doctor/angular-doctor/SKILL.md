---
name: angular-doctor
description: Run Angular Doctor after Angular edits. Scan for correctness, performance, security, accessibility, and maintainability regressions; triage angular-doctor-report.md; fix without auto-committing.
license: MIT
compatibility: Requires an Angular CLI or Nx workspace (Angular 15+), Node.js 20.19+, and network access for npx.
metadata:
  project: angular-doctor
  version: "0.3.0"
---

# Angular Doctor (agent skill)

## When to run

After meaningful Angular changes (components, templates, services, routes, forms, DI), run:

```bash
npx @abiramcodes/angular-doctor@latest --verbose --scope changed
```

For a full workspace audit:

```bash
npx @abiramcodes/angular-doctor@latest --verbose
```

## Primary artifact

When score is below 100 or warnings/errors exist, Angular Doctor writes **`angular-doctor-report.md`** at the project root (or the path from `angular-doctor.config.json`). **Read that file first.** It is self-contained. If the `angular-developer` skill is installed, use it as an optional cross-check. The report is enough when that skill is not installed.

The report links the official migration hub [angular.dev/reference/migrations](https://angular.dev/reference/migrations) and a **Recommended migration commands** section with `ng generate @angular/core:*` schematics (run with `--dry-run` first, then `--path` as needed). There is no bundled “all signals” schematic—run signal-input, output, and signal-queries migrations separately when needed.

## Triage workflow (`/doctor`)

Follow `playbooks/triage.md` in this skill folder:

1. Scan (changed scope by default).
2. Open `angular-doctor-report.md` when present.
3. Run **Recommended migration commands** first, then fix [Angular style guide](https://angular.dev/style-guide) findings linked in the report.
4. Group by severity and category.
5. Fix highest-impact errors first (security, correctness, a11y).
6. Re-scan until score stops regressing; do not auto-commit unless the user asks.

## Conventions

- Prefer standalone components, `inject()`, signals/`input()`/`output()`, and built-in control flow (`@if`, `@for` with `track`, `@switch`, `@defer`).
- Respect the project Angular version (OnPush defaults in v22+).
- Hybrid lint stack: Oxlint for TypeScript; a curated set of Angular template rules over standalone and inline templates.
- Image and change-detection findings are static template and decorator checks. LCP `priority`, preconnect, and slow-computation advice stay manual.

## Install this skill locally

```bash
npx @abiramcodes/angular-doctor@latest install
```
