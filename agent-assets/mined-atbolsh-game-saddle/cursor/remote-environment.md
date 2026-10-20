---
description: Local machine is for editing only — DB and python env live remotely
alwaysApply: true
---

# Remote execution environment

Most real work on this repo happens on a **remote** box. The local machine is
for editing code only. Concretely:

- **Local Neo4j is bare — do not touch it.** Never query, write, seed, wipe,
  or dump the local Neo4j instance. It does not hold the project's memory
  graph; anything you'd learn from it is misleading, and anything you'd write
  to it is lost noise. The real database lives on the remote machine.
- **The local python env is incompatible.** Project dependencies
  (`neo4j_agent_memory`, `torch`, `transformers`, sentence-transformers
  models, ...) are not installed locally. Never run agent code, notebooks, or
  tests locally — they will fail with import errors at best, or "work"
  against the wrong environment at worst.
- **Verification happens remotely, by the user.** Deliver reviewed code;
  do not claim runtime verification you could not perform. Call out anything
  that needs a remote check (e.g. exact NAMS API signatures) explicitly.
- **Don't guess third-party APIs.** When code must call a NAMS / library
  method whose signature cannot be confirmed locally, verify it against the
  installed package on the remote env (e.g. `help(client.short_term)`)
  before relying on it — or write the code to fail loudly if the name is
  wrong (see the no-fuzzy-fallbacks rule).
