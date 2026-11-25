---
name: precedent-diverge
description: Record that this project knowingly departs from precedent, and why. Use when the user says they usually do X but are doing something else here, or when they accept a CONFLICT or DIVERGENCE warning deliberately.
---

# Record a deliberate exception

Use when the precedent is sound but this project is genuinely an exception. Not
when the precedent is stale — that is `--supersedes`. Not when it was wrong
everywhere — that is the `precedent-regret` skill.

```bash
uv run <cli> record --project . \
  --title "..." --topic "..." --chose "..." --rationale "..." \
  --despite "<what makes this project different>"
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it. Read that skill first if it is not already loaded.

`--despite` is what stops `check` repeating an unanswerable DIVERGENCE warning in
this project forever. State what is different about *this* project, not why the
option is good in general — the reason has to be checkable by a future session
deciding whether the exception still holds.
