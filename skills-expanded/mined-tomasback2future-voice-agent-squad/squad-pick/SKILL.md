---
name: squad-pick
description: Atomically claim an item by ID. Verifies references, applies RED-first if AC names concrete failures.
argument-hint: "<ITEM-ID>"
allowed-tools:
  - Bash
  - Read
paths:
  - ".squad/items/**"
disable-model-invocation: true
---

You are claiming item `$ARGS`. Run:

```bash
squad claim $ARGS --intent "<one sentence describing what you intend to ship>"
```

If the command exits non-zero, the item is already claimed by someone else — pick another and tell the user.

If the claim succeeds:

1. Read the item file end-to-end (`.squad/items/$ARGS-*.md`). The `## Acceptance criteria` section is the contract.
2. **Verify every `file:line` reference** in the item body against current code. Items rot — line numbers shift, files get renamed, constants change. Open each reference and confirm the described condition is still true. If the item is stale, correct the body before starting.
3. **If the AC names concrete failing scenarios** ("returns wrong value for X", "breaks when Y happens"): invoke `squad-premise-validation` and write the RED test FIRST against current code. If the test passes unmodified, the bug does not reproduce — stop and reclassify per the skill.
4. Otherwise, invoke `squad-loop` and proceed with TDD.

Announce the claim in one line: *"Claimed $ARGS: <title>. Starting with <plan>."*
