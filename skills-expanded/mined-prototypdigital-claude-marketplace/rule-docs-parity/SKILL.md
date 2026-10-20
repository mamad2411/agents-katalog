---
name: docs-parity
description: Keep documentation in sync with every user-facing change.
---

# Docs parity

A PR that changes behavior without updating docs is not done.

**Why:** Docs that lag behind behavior mislead users into using flags, defaults, or APIs that no longer work, and the drift compounds with every unsynced change. Best enforced by a CI check that fails when source under a watched path changes without a matching docs diff; this rule explains why that gate exists.

## What counts as user-facing

- New or removed CLI flags, commands, or options
- Changes to user-facing workflows (new prompts, removed choices, changed defaults)
- New or removed public APIs, config options, or schema fields
- Changes to output behavior or generated artifacts

## Required behavior

When any of the above change:

1. Update `README.md` if the change affects setup, usage, or the feature overview.
2. Update the relevant documentation page if one covers the changed area.
3. Include the doc update in the same commit as the code change — not a follow-up.

## Examples

```text
// BAD — new CLI flag added with no README update
src/cli.ts: added --output-format flag (json | table)
README.md: still documents only --output flag
→ Users have no idea the flag exists or how to use it

// GOOD — README updated in the same commit
src/cli.ts: added --output-format flag (json | table)
README.md: "## Flags" section updated with --output-format usage
```

## When NOT required

- Internal refactors with no behavior change (renaming a variable, extracting a function)
- Test-only changes
- Dependency bumps with no API change
