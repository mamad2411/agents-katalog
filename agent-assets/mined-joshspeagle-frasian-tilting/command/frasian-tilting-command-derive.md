---
description: Run the deriver subagent to produce or verify a method's derivation.
---

Run the `deriver` subagent on `$ARGUMENTS`.

The argument is the method name (e.g. `fisher_rao`). The deriver will:

1. Read `docs/methods/<name>.md` (Definition, Predicted behavior).
2. Read the framework's math primitives at
   `src/frasian/models/normal_normal.py`.
3. Produce a step-by-step Derivation section, with each non-trivial
   step verified by sympy or numerical cross-check on the
   conjugate-Normal sandbox.
4. Output a markdown block ready to paste into the brief's
   "Derivation" section, plus a list of invariants for property
   tests.

Relay the output verbatim. Do *not* paste it into the brief
yourself unless the user explicitly asks — they will review the
derivation first.

If `docs/methods/<name>.md` does not exist yet, tell the user to run
`/propose-method <name>` first to scaffold the brief.
