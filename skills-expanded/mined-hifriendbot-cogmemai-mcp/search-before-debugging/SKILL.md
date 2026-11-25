---
name: search-before-debugging
description: Before debugging any new bug, error, or unexpected behavior, search CogmemAi for an existing fix from this or any prior session. Use the moment a bug, error message, stack trace, failed test, or unexpected behavior appears, BEFORE running diagnostic commands or reading code. Eliminates duplicate debugging across the entire team — if someone fixed it before, you find the fix in seconds.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [debugging, search, recall, memory, mcp, bug, incident, developer-tools]
---

# Search Before Debugging with CogmemAi

The single highest-leverage debugging habit: search for an existing fix before debugging from scratch. Most bugs in established codebases are repeats. Someone (you, a teammate, a past version of you) has already solved it. CogmemAi makes those fixes instantly findable.

This skill is the *recall* half of the bugfix loop. Pair it with the `save-bugfix` skill which captures fixes for future sessions to find.

## When to Use

Trigger before any debugging action when you encounter:

- An error message or stack trace
- A failing test (especially flaky or new failures)
- Unexpected behavior or output
- A regression after a recent change
- A user report of "it broke" or "this doesn't work"
- Confusing log output
- A build failure

The rule: **search first, debug second**. Always.

## How to Search

Call `recall_memories` with the most distinctive part of the symptom as the query. Pass `context_type: "debugging"` to bias the ranker toward bug and pattern memories.

```
recall_memories({
  query: "Cannot read properties of undefined Stripe webhook",
  context_type: "debugging",
  limit: 10
})
```

If the literal error string is too generic, also try:

- The component name + the error type ("auth jwt token expired")
- The library name + the symptom ("postgres connection pool exhausted")
- The recent change that may have triggered it ("after migrating to Next 15, hydration mismatch")

Run two or three queries with different phrasings if the first returns nothing relevant. CogmemAi's semantic search will catch reformulations the keyword wouldn't.

## What to Do With Results

### A high-relevance match exists

Stop. Read the memory carefully. It contains the symptom, root cause, fix, and why-it-works that a past debugging session captured. Verify:

1. The symptom in the memory matches your current bug closely
2. The file path or component named in the fix still exists in the codebase
3. The fix is still applicable (the underlying library, version, or architecture hasn't changed in a way that invalidates it)

If all three check out, apply the fix. You just saved an hour of debugging in 30 seconds.

### A partial match exists

The memory describes a *similar* bug, not the same one. Still valuable. Read it for:

- Diagnostic commands the past session used
- Where the previous bug was in the codebase (likely close to yours)
- Patterns the past debugger noticed

Use it as a head start, not the answer.

### No match

No prior fix exists. Debug from scratch. When you find the fix, the `save-bugfix` skill will capture it for next time.

## Filter By Type

When the symptom is unmistakably a known bug class, filter the search:

```
recall_memories({
  query: "race condition login double-submit",
  memory_type: "bug",
  context_type: "debugging"
})
```

Available types relevant to debugging: `bug`, `pattern`, `correction`, `dependency`.

## Search Globally and By Project

By default `recall_memories` searches the current project plus global memories. If the bug feels library-level (a Stripe SDK quirk, a Next.js footgun) and the project is new, also try `scope: "global"` explicitly to surface promoted memories from other projects:

```
recall_memories({
  query: "stripe webhook signature verification fails",
  scope: "global"
})
```

## Why This Matters

A debugging session that starts with `recall_memories` either:

- Returns the fix in seconds (huge win)
- Returns related context that accelerates the new debugging (medium win)
- Returns nothing, costing you one tool call to confirm there's no prior art (minor cost)

The expected value is overwhelmingly positive. The only way it loses is if you skip it.

For teams, the win compounds. Every member's fix becomes every other member's instant lookup. The "we fixed this before" problem disappears.

## Anti-Patterns

- **Skipping the search because "I'll just look at the code"** — searching is faster than reading code. Search first.
- **One vague query then giving up** — try two or three reformulations before concluding nothing exists.
- **Trusting a recalled fix without verification** — file paths, function names, and library versions drift. Confirm before applying.
- **Forgetting to save the new fix** — once you debug it from scratch, use `save-bugfix` so the next person finds it.

## Related Skills

- `save-bugfix` — the partner skill that captures the fix you just discovered
- `cogmemai-memory` — full reference for memory management
- `session-start` — load broader project context at session start
