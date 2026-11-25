---
name: project-model
description: When working in a codebase you've touched before, consult and update the persistent project model maintained by presence. The model lives at ~/.claude/presence/projects/<repo-id>/model.md and contains terse notes about architecture, conventions, and verified facts. Use it BEFORE re-deriving things you've already learned, and APPEND to it when you confirm something non-obvious that future sessions will benefit from knowing.
---

# Project model: read and write

`presence` injects the contents of `model.md` into your context at the start of each session. Treat it as a trusted-but-stale set of notes. The previous you wrote them, but the code may have changed since.

## When to read

The model is already in your SessionStart context, so you don't need to re-read it explicitly. If you forgot or need to query a specific slice mid-session:

```bash
PRESENCE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(realpath ~/.claude/plugins/presence 2>/dev/null || echo .)}"
PYTHONPATH="$PRESENCE_ROOT/lib" python3 -c "
from model import read_model
print(read_model('$PWD'))
"
```

## When to write

Append a new observation when **all four** are true:

1. You verified something non-obvious about this codebase (architecture decision, a convention not in CLAUDE.md, the actual command for tests/build, an invariant about data flow).
2. The fact would save a future you 2+ minutes of re-deriving.
3. The fact is unlikely to change in the next month (don't write WIP state).
4. The fact is *project-specific*. General programming knowledge belongs nowhere; you already know it.

To append:

```bash
PRESENCE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(realpath ~/.claude/plugins/presence 2>/dev/null || echo .)}"
PYTHONPATH="$PRESENCE_ROOT/lib" python3 -c "
from model import append_observation
append_observation('''<<<terse multi-line observation here>>>''', '$PWD')
"
```

## Style of entries

Entries should look like:

```
## 2026-04-25 14:32

The `auth/` package uses a custom session middleware that wraps Flask-Login. Token refresh
happens in `auth/refresh.py:42`, NOT in the middleware itself. That's a deliberate split
to keep the middleware reentrant. Don't add refresh logic to the middleware.

Test command: `make test-auth` (NOT `pytest auth/`); the latter misses fixtures.
```

Bad entries (don't write these):
- "Today I fixed the bug." (ephemeral, project state, not a stable fact)
- "Python is dynamically typed." (general knowledge)
- "Files are in src/." (derivable from `ls`)

## Compression

The model is compressed periodically by the `model-curator` subagent (invoke via `/presence-curate`). It will preserve the most recent N entries verbatim and consolidate older ones. Don't worry about file size; write what's worth writing.

## What NOT to put in the model

- Secrets, tokens, API keys. These are redacted by `presence` when logged elsewhere, but in `model.md` you control the content directly: just don't paste them.
- Long code dumps (write the *insight*, not the code).
- Personal opinions about teammates or the codebase.
- Anything that would embarrass you if leaked. The file lives outside the repo by default but is plain text on disk.
