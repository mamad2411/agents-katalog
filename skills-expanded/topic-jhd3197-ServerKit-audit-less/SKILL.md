---
name: audit-less
description: Scan LESS stylesheets for variable errors — undefined variables, CSS custom properties passed to compile-time functions (fade, darken, lighten, etc.), and incorrect variable name patterns. Reports issues with file, line, and fix.
argument-hint: "[file-or-directory]"
---

Audit LESS stylesheets in ServerKit for recurring build-breaking patterns.
Scope: **${ARGUMENTS:-frontend/src/styles/}**

## What to Scan For

### Pattern 1: CSS custom properties in LESS compile-time functions

LESS functions like `fade()`, `darken()`, `lighten()`, `saturate()`, `spin()`, `mix()` require **real color values** at compile time. Variables defined as `var(--something)` will fail.

Search for calls to these functions and check if any argument is a variable that resolves to a CSS custom property.

**Broken** — these variables use `var(--...)` and cannot be evaluated by LESS:
- `@bg-body`, `@bg-sidebar`, `@bg-card`, `@bg-hover`, `@bg-elevated`, `@bg-secondary`, `@bg-tertiary`
- `@border-default`, `@border-subtle`, `@border-active`, `@border-hover`
- `@text-primary`, `@text-secondary`, `@text-tertiary`
- `@accent-primary`, `@accent-hover`, `@accent-glow`, `@accent-shadow`
- `@shadow-sm`, `@shadow-md`, `@shadow-lg`
- `@color-primary`

**Fix**: Use the corresponding `*-raw` variant instead (e.g., `@bg-hover` → `@bg-hover-raw`, `@text-tertiary` → `@text-tertiary-raw`, `@accent-primary` → `@accent-primary-raw`).

### Pattern 2: Undefined or misspelled variables

Check for variables that don't exist in `_variables.less`. Common mistakes:
- `@card-bg` → should be `@bg-card`
- `@accent-success` → should be `@success`
- `@accent-danger` → should be `@danger`
- `@accent-info` → should be `@info`
- `@accent-warning` → should be `@warning`
- `@primary-color` → should be `@accent-primary` or `@accent-primary-raw`
- `@spacing-*` → should be `@space-*`

### Pattern 3: Non-raw variables in theme-sensitive contexts

For any LESS function that manipulates color values (fade, darken, lighten, contrast, saturate, desaturate, spin, mix, tint, shade), the argument MUST be a raw hex/rgb value or a `*-raw` variable.

## Reference: Valid Variable Names

Read `frontend/src/styles/_variables.less` to get the authoritative list of defined variables. Any `@variable` used in a `.less` file that is not in `_variables.less` (and is not a local variable or LESS built-in) is a bug.

## Output Format

For each issue found, report:
```
[FILE]:[LINE] — [ISSUE]
  Found:    [problematic code]
  Fix:      [corrected code]
```

At the end, provide a summary count: `X issues found across Y files`.
If no issues are found, report: `No LESS variable issues found.`
