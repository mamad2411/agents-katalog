---
name: squad-blocked
description: Mark an item blocked and inject the standard ## Blocker section template into the item file.
argument-hint: "<ITEM-ID>"
allowed-tools:
  - Bash
  - Edit
paths:
  - ".squad/items/**"
disable-model-invocation: true
---

You are marking item `$ARGS` as blocked. Run:

```bash
squad blocked $ARGS --reason "<one-line reason>"
```

Then add a `## Blocker` section to the item file (`.squad/items/$ARGS-*.md`) using this template:

```markdown
## Blocker

**What blocks:** <concrete description of what is preventing progress>

**What is needed to unblock:** <specific action, decision, dependency, or external answer>

**Who/what could unblock:** <agent, user, external party, or "waiting on <event>">
```

Then:
- Move the item out of "In Progress" → "Blocked" in STATUS.md if it was on the board.
- Pick the next item and continue. Do not sit on a blocked item.
- If the block is on an external dependency with no clear resolver, escalate to the user.
