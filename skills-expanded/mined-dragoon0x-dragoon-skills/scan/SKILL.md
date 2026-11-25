---
name: scan
description: Fingerprint a codebase's design DNA and write dragoon.json. Use when the user wants to set up dragoon in a project, or asks to "scan", "fingerprint", or "analyze" the design system. Always run this first before /critique, /slop, or /review on a project that hasn't been scanned yet. Outputs detected stack, palette, type scale, spacing grid, motion curves, and accessibility metrics. Run as `node ~/.claude/skills/dragoon/skills/scan/scripts/scan.js [root]`.
version: 1.0.0
---

# /scan

Generates `dragoon.json`, the canonical fingerprint of a codebase's design DNA. Every other dragoon skill reads or writes against this file.

## When to use

Run /scan when:
- The user is setting up dragoon in a new project for the first time
- The user asks to "scan", "fingerprint", "audit the design system", "analyze the codebase"
- Another dragoon command (/critique, /slop, /review) needs a manifest and one doesn't exist
- The codebase has changed significantly and the existing manifest is stale

## What it produces

A `dragoon.json` file at the project root with:
- **stack**: framework (react/next/vue/svelte/etc), styling layer (tailwind/css/styled-components/etc), language, package manager
- **tokens.color**: top distinct colors with usage counts and inferred roles
- **tokens.spacing**: distinct spacing values, inferred grid (4/6/8/12/16px), confidence score
- **tokens.type**: font families, font sizes, inferred scale ratio (golden, perfect-fourth, etc), confidence
- **tokens.radius / shadow / motion / breakpoints**: top values with counts
- **metrics**: file counts, component count estimate, accessibility signals (alt rate, button label rate, semantic tag use)
- **rules**: derived defaults (grid size, type ratio, max variants per token, allowed colors). Edit by hand if needed.

## Run it

```
node ~/.claude/skills/dragoon/skills/scan/scripts/scan.js [root]
```

Flags:
- `--out <path>` write to a custom path
- `--json` print manifest to stdout
- `--dry-run` compute but don't write
- `--quiet` no terminal output beyond errors
- `--help` full usage

## Notes

- Pure regex scanning. No AST parser dependency. No network calls.
- Skips node_modules, dist, build, .git automatically (gitignore-aware).
- Caps at 5,000 files per scan and 2MB per file. Larger codebases get a representative sample.
- Re-run /scan after major design changes to keep rules current.
