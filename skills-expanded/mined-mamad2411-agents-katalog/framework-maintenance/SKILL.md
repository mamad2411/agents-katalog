---
name: framework-maintenance
description: Authority declaration for framework self-build (target=Framework): owns the framework surface so guard passes framework writes, never product (I11). Use on a target=Framework wave.
---

# framework-maintenance

The authority that lets the agent build **the framework itself**. When a task targets the Framework
(this rebuild, a ref-adopt, foundation hardening), its waves write to `engine/` and `library/` — paths
no kernel/support/system module owns. Without a declared authority, guard Layer 4 (I5) blocks those
writes. This module **is that declaration**: its `authority.owns` covers the framework surface, so guard
passes framework writes — and **only** framework writes (I11: never product space).

It is a **declaration, not an orchestrator**. It does no work and produces no receipts of its own — the
building agent does the work and writes the milestone receipts (I10) *under* this authority.

## What this does / does not do

Does: declare authority over the framework surface (`engine/*`, `library/*`, the registry/config/version
files) in `skill-rules.json` so `guard-check.py authority --module framework-maintenance` authorizes a
framework wave's write targets; carry the one-time bootstrap-attestation exception (Wave 1). Does **not**:
execute or transform anything (it is an authority grant), write to **product space** (I11 — that is a
hard boundary, not a default), or write its own receipts (the building agent's milestone receipts cover
the work).

## When NOT to use

- The task is **product-space** work — framework-maintenance never authorizes product writes (I11). The
  active domain/module owns those, scoped by `scope.md`.
- The task card does **not** declare `target: Framework` — there is no framework authority to grant.
- A **read-only** analysis of framework files — reads need no write authority; do not activate.

## Inputs

- The locked task card (must declare `target: Framework`).
- `registry.yaml` (guard resolves this module's path → `skill-rules.json`).
- `engine/shared/references/invariants.md` (I5 authority, I11 space boundary).

## How it works

1. A `target: Framework` task routes its waves through guard with `--module framework-maintenance`.
2. guard Layer 4 loads this module's `skill-rules.json` `authority.owns` and `fnmatch`es every declared
   write target against it (`guard-check.py authority`). All within `owns` → AUTHORIZED; any target
   outside → UNAUTHORIZED (HARD error) — that target is either product space (forbidden, I11) or a new
   framework path that must be added to `owns` deliberately, never silently passed.
3. **Bootstrap attestation (Wave 1 only):** before the receipt chain exists, the first framework wave is
   human-attested once; every subsequent wave runs guard normally under this authority.

## Output

Produces **no receipts itself** — it is an authority declaration. It *enables* guard to authorize the
building agent's framework writes; the agent writes the milestone receipts (`module: framework-maintenance`,
e.g. these rebuild receipts) under this authority (I10). The contract is `skill-rules.json` `authority.owns`
+ `schemas/framework-authority.schema.json` (authority-scope + bootstrap-attestation record shape).

## Proactive Triggers

- **A framework wave declares a write target outside `authority.owns`**: do not widen `owns` reflexively —
  first decide whether the target is product space (then it is an I11 violation, not an authority gap) or
  a genuinely new framework path (then add it to `owns` as a deliberate, reviewed change).
- **A product-space path appears under `target: Framework`**: HARD stop (I11). Framework and product are
  separate spaces; a task that needs both is two tasks.

## Completion Criteria

**Done when:** a `target: Framework` wave's write targets all fall within `authority.owns` and guard
Layer 4 returns AUTHORIZED (or Wave-1 bootstrap attestation is recorded). The building agent then
proceeds and writes its own receipt.

**Not done if:** a product-space write was authorized under this module (I11 breach); `owns` was widened
to pass a wave without deciding framework-vs-product; the module tried to do work or write a receipt
itself.

**Next step:** executor runs the authorized framework wave; the building agent writes the milestone receipt.

## Related Skills

- **guard**: reads this module's `authority.owns` at Layer 4. framework-maintenance *declares*; guard *enforces*.
- **archive**: bumps the **product** version; framework-maintenance governs writes to the **framework** (never product) — the two never overlap (the four-identities separation, doc 07).
