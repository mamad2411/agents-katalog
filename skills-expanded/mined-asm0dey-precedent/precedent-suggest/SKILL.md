---
name: precedent-suggest
description: List decisions this project still owes, based on comparable projects. Use when the user asks what is left to decide, what they have missed, or how this project compares with their others.
---

# Decisions this project still owes

```bash
uv run <cli> suggest --project <path>
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it. The path defaults to the working directory.

Two kinds of output. Coverage gaps are topics settled in comparable projects but
open here — decisions owed, not yet made. Principle candidates are the same
answer reached in three or more projects, which is no longer a per-project
decision.

Present the gaps that matter for the current work rather than the whole list,
and ask before promoting anything to a principle: repetition is evidence, not
consent.
