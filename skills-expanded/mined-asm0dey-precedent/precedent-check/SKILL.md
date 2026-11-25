---
name: precedent-check
description: Show what was decided before on a topic, and flag conflicts with a proposed choice. Use when the user weighs an option, asks what they picked last time, or is about to settle a technology, framework, provider or process choice.
---

# Check precedent on a topic

Take the topic and the option from the user's own words: "should I use Postgres
here" is topic `persistence`, option `postgres`. Ask only when the topic is
genuinely unclear.

```bash
uv run <cli> check --topic "<topic>" --chose "<option>"
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it, and the session brief prints its full path.

Lead with what it returns before offering your own opinion.

`CONFLICT` means this option was explicitly rejected before — quote the recorded
reason. `DIVERGENCE` means the user chose differently in comparable projects.

Both are information, not vetoes. Test whether the recorded reason still applies
to *this* case: a rationale about concurrent writers says nothing about a
single-user tool. Say which way you read it and leave the decision with them.
