---
name: squad-file
description: File a new item. Runs squad new with type and title, then injects the standard item template body for you to fill in.
argument-hint: "<type> \"<title>\""
allowed-tools:
  - Bash
  - Edit
paths:
  - ".squad/items/**"
disable-model-invocation: true
---

You are filing a new item. Run:

```bash
squad new $ARGS
```

This creates a new item file under `.squad/items/` with frontmatter populated. Open the file and fill in the body using this template:

```markdown
## Problem
<What is wrong / what does not exist. 1–3 sentences.>

## Context
<Why this matters. Where in the codebase it lives. What has been tried. Link to upstream specs if relevant.>

## Acceptance criteria
- [ ] Specific, testable thing 1
- [ ] Specific, testable thing 2
- [ ] (For bugs) A failing test exists; it now passes.

## Notes
<Optional design notes. Trade-offs considered. Pointers to related items.>
```

Risk classification reminder: bump `risk:` from `low` if the change touches sensitive paths defined in `.squad/config.yaml`. For `risk: high` items where rollback is non-trivial (schema migrations, multi-tier cutovers, anything `git revert` alone does not fully reverse), add a `## Rollback plan` section before coding.

If this item is P0 or P1, add it to the "Ready" section of STATUS.md.

Commit:

```bash
git add .squad/items/<new-file>.md
git commit -m "docs: add <ID> <title>"
```

(No PM-trace IDs in the commit message body — the filename carries the ID.)
