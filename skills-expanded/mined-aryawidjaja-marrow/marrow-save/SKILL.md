---
description: Save this session's durable knowledge to the Marrow shared brain
---

Review our conversation so far and save what's worth remembering to the Marrow shared brain, so the
next session inherits it.

For each durable decision, fact, or gotcha we reached:

1. Call `mem_recall` first and skip anything already stored — don't duplicate.
2. Save it with `mem_write` (kind `decision` or `fact`, a short `topic` (a label, not a sentence) and an `area` (call `mem_areas` first and reuse an existing one)).

Distill — capture the conclusion and the why, not the transcript. Skip transient chatter, dead ends,
and anything already in Marrow. When you're done, briefly list what you saved.
