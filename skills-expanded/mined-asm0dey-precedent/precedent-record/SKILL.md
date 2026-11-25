---
name: precedent-record
description: Record a decision that was just settled, with its rationale and rejected alternatives. Use the moment the user commits to a database, framework, provider, deployment target, pricing model or process — including when they say "let's go with X".
---

# Record a settled decision

Use what the user just settled. When they gave no detail, take it from the
conversation. The `precedent` skill covers what is worth recording and what is
not; read it if it is not already loaded.

Draft the command, show the user the one-line summary, and run it only once they
confirm. An explicit "decided" or "settled" is that confirmation: record in the
same turn and say so in one line. A wrong entry is worse than a missing one, because it gets quoted back
later as their own precedent.

```bash
uv run <cli> record --project . \
  --title "..." --rationale "..." --scope architecture \
  --topic "..." --chose "..." --rejected "..."
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it.

`--topic` is the question the decision answers (`persistence`,
`backend-framework`), never a project tag like `java` or `telegram-bot`,
and never a bare noun plus a qualifier (`framework,java`). Put the
qualifier inside one topic.

`--rationale` is the field that matters: in two years the *what* is recoverable
from the code and the *why* is not. `--rejected` is what lets a future session
warn about reviving something already turned down. In a monorepo, record against
the module the decision is about, not the repository root.
