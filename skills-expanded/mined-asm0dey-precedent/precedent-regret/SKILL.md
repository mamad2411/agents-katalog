---
name: precedent-regret
description: Mark a choice repeated across projects as a mistake, inverting its precedent. Use when the user says a past choice bit them, was a mistake, or that they would never do it that way again.
---

# Invert a precedent you regret

```bash
uv run <cli> regret \
  --topic "<topic>" --chose "<option that was wrong>" \
  --because "<the lesson>" --instead "<what you prefer now>"
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it. Read that skill first if it is not already loaded.

`--because` is the whole point: without the reason, a future session sees only
that the option is disfavoured and cannot tell whether the condition that made it
wrong applies to the case in front of it.

Show the user which decisions this will mark before running it — the scope is
every project at once. Nothing is deleted: the decisions keep their original
rationales, because a reason that looked good several times is what tells you the
lesson was expensive.
