---
name: architecture-guard
description: Keep a long-running project's architecture coherent across rounds so it doesn't drift into spaghetti. Maintains a durable architecture map and audits for drift (dependency cycles, god-objects, oversized files, duplication, layering violations). Use on Review rounds and whenever a round adds a new module or a cross-module dependency.
---

# architecture-guard — fight architectural drift across a long loop

Cold-start ORIENT preserves *progress* but not the *holistic architecture* — over many rounds a system drifts into tangled spaghetti. This keeps a durable architectural memory and audits coherence.

## 1. Maintain the durable architecture map
Keep an `ARCHITECTURE.md` (or a `## Architecture` section) current — make it part of the cold-read stack ORIENT reads every round:
- the module / dependency graph (who depends on whom; the intended layering)
- key invariants & boundaries ("perception never imports control"; "X has exactly one writer")
- a "where does X live" index, so new code lands in the right module instead of a new dumping ground

## 2. Audit for drift (every Review round + on cross-module changes)
- dependency **cycles** — generate the import graph; cycles are forbidden
- **oversized files** (>800 lines) and **god-objects** → split
- **duplication** — the same logic in N places → consolidate
- **layering violations** — a lower layer importing an upper one, leaked internals
- **public-surface bloat** — is the API growing without anything being pruned?

## 3. If drift is found: refactor BEFORE adding more
Stop feature work; restore the boundaries first (spike-then-migrate, tests green throughout), then update the map. A round that piles features on top of drift only makes it worse.

Honest scope: this keeps a project in the "human-graspable, modular" regime far longer — it does not make a 100k-line monolith coherent. Bias hard toward many small, well-bounded modules.
