---
description: Prefer clean, loud failures over fuzzy fallbacks that "sometimes work"
alwaysApply: true
---

# No fuzzy fallbacks — fail cleanly

Never do the "wrong but easy" thing if it can produce plausible-but-wrong
results. Fuzzy bugs that sometimes work are the worst kind to debug,
especially in AI-agent code where outputs are nondeterministic to begin with.
A clean failure (exception, empty result, loud warning) is always preferable
to silently degraded behavior.

Concretely:

- **Exact queries over similarity search.** When data can be fetched by an
  exact key (session id, node label, property match), do that. Do not use a
  semantic/vector search API as a substitute for an exact lookup — it returns
  the *nearest* thing, not the *right* thing, and non-empty garbage masks
  broken primary paths. (Real example from this repo: passing a session id as
  the free-text query to NAMS `search_traces` could return other sessions'
  traces; the exact `MATCH (t:ReasoningTrace {session_id: $sid})` Cypher is
  the primary path.)
- **Fallbacks must be visible.** If a fallback path exists at all, it should
  fire only when the primary path *errors* (not merely returns something
  unexpected), and it must log at WARNING or higher so degradation is never
  silent.
- **Don't guess schemas.** Verify node labels / property names against a real
  DB dump or live query before writing Cypher. A query ordered by a
  nonexistent property "works" (no error, undefined order) — that is exactly
  the failure mode to avoid.
- **No defensive `except: pass`.** Swallowing an exception to keep going
  converts a clean failure into a fuzzy one. Catch only what you can handle
  meaningfully, and log what you catch.
