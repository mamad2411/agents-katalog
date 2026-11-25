---
name: scoped-tests
description: >-
  Use after changing code, before claiming work is done — run the test command
  scoped to what you changed instead of the whole suite, to avoid the timeout
  and context waste of full-suite runs on a small change.
---

# Scoped test runner

The article's rule: running the full suite when you changed one part of the
codebase wastes context and time. Pick the narrowest command that still covers
the change.

1. **Changed one service / package / app?** Run only that area's test command.
   The exact command lives in that area's `CLAUDE.md` — subdirectory `CLAUDE.md`
   files should specify the test command that applies to that part of the repo.
2. **Changed shared / core code that other areas import?** Run the full suite —
   a change there ripples everywhere, so a scoped run would miss regressions.
3. **Not sure what a change reaches?** Trace its importers first (the
   codebase-search MCP's `find_references` does this), then scope accordingly.

This skill is repo-agnostic on purpose: it carries the *principle*. The exact
commands belong in each repo's own `CLAUDE.md` hierarchy, not bundled here.
