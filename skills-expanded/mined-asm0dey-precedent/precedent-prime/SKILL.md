---
name: precedent-prime
description: Load this project's recorded decisions and precedent into context. Use when starting work in a project you have not been briefed on, or when the user asks what has already been decided here.
---

# Load this project's decisions

The path defaults to the working directory; use another when the user names one.

```bash
uv run <cli> brief --project <path>
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it.

Report what it returns, leading with whatever bears on the work at hand rather
than reciting the whole brief. If the project is untagged, say so and offer tags
based on what you can see in the directory — do not pin them without agreement.

Then hold these for the rest of the session: check the graph before recommending
a technology, and offer to record a decision in the message where it gets
settled. Guidance for both is in the `precedent` skill; read it if it is not
already loaded.
