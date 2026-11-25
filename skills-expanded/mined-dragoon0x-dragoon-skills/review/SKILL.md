---
name: review
description: Unified code + design review in a single pass. Runs slop detection, design critique, and engineering signals (TODO/FIXME, any types, large files) at once. On any UI files in scope (jsx/tsx/vue/svelte/css/scss/html), /critique and /slop run automatically - engineering review and design review in one read. Use when the user wants to review a PR, diff, file, or folder. Supports `--diff` to review only files changed in git working tree. Run as `node ~/.claude/skills/dragoon/skills/review/scripts/review.js [path]`.
version: 1.0.0
---

# /review

Unified review. The integration that no other skill pack ships.

When you run /review on a diff, it scans every file:
- runs slop detection (all 12 rules)
- runs lightweight engineering checks (TODO/FIXME, any types, large files)
- if any UI files are present, automatically runs /critique on the project

One report. Both lanes. The thing teams actually need.

## When to use

Run /review when:
- The user wants to review a PR or diff
- Before opening a pull request
- The user says "review my changes", "look at this diff", "audit this branch"
- As a CI step on every PR

## Run it

```
# review the working directory
node ~/.claude/skills/dragoon/skills/review/scripts/review.js

# review only changed files in git
node ~/.claude/skills/dragoon/skills/review/scripts/review.js --diff

# review a specific file or folder
node ~/.claude/skills/dragoon/skills/review/scripts/review.js src/Card.tsx

# CI gate: fail if design score < 80 or any high-severity findings
node ~/.claude/skills/dragoon/skills/review/scripts/review.js --diff --threshold 80
```

Flags:
- `--diff` only review files in git diff (uses `git diff --name-only HEAD`)
- `--manifest <p>` use a specific manifest
- `--json` machine-readable
- `--threshold <n>` CI gate
- `--no-design` skip design critique (slop only)
- `--no-slop` skip slop (critique only)
- `--help` full usage

## Exit codes

- `0` clean (or threshold met)
- `1` high-severity findings, or threshold not met
- `2` bad usage

## What's checked

Engineering signals:
- `eng-001` unresolved TODO / FIXME / HACK / XXX markers
- `eng-002` use of `any` type in TypeScript
- `eng-003` files over 600 lines

Design signals: all 12 slop rules. See `node ~/.claude/skills/dragoon/skills/slop/scripts/slop.js --rules`.

Design quality: full /critique scoring on the project's manifest.
