---
name: slopbuster-rules
license: Apache-2.0
description: Architecture guardrails to follow WHILE implementing backend or frontend code, so AI-generated code does not drift into slop. Use when scaffolding a project, adding a feature module, or writing implementation code and you want it to respect layering, module boundaries, typing, and async/resource safety. Stack packs for Python, Rust, and frontend (client/server separation).
---

# SlopBuster — Rules

These are the guardrails for the *building* phase. The goal is not style policing — it's
keeping responsibility in the layer where it's most stable so the codebase stays
maintainable, extensible, and safe as it grows and as agents extend it.

Load the pack for the stack you're writing:

- **Python backend** (FastAPI / Flask / Django / Litestar / Quart) → [references/python.md](references/python.md)
- **Rust backend** → [references/rust.md](references/rust.md)
- **Frontend (any SaaS/service; client/server separation core, Next.js/React instantiation)** → [references/frontend.md](references/frontend.md)

The packs scale to the system you're building — a small service follows the same principles
without the heavy machinery. Reach for jobs/workers, queues, streaming, or agent crates only
when you actually need them.

## Principles that hold across stacks

- **Place by stable responsibility.** Transport concerns near the edge, domain logic in
  modules, infra isolated, external calls behind clients. When unsure where code goes, put
  it where its responsibility changes least.
- **Thin edge, thick core.** Routers/handlers/components validate and delegate; they don't
  hold business logic. Logic lives in services/modules/hooks.
- **One direction of dependency.** No layer reaches sideways or upward. No circular imports.
  A module talks to another module only through its public service, never its internals.
- **Make invalid states unrepresentable.** Model state explicitly (union/enum state machines,
  typed contracts). No boolean explosion, no untyped boundaries, no `any` to buy speed.
- **Safety by default.** Every external call has a timeout and bounded retry. Long work goes
  to a job/worker, not the request path. Auth, validation, and rate limits are defaults.
- **Prompts/personas/configs are data, not code.** Versioned and editable, never hardcoded
  into source.

## How to use this while coding

1. Detect the stack, load its pack.
2. Before adding a feature, confirm where each piece belongs (layer/module) — don't freestyle
   structure.
3. Write to the contracts: typed input/output and explicit error types on every public unit.
4. When tempted to add an abstraction or wrapper, require a concrete reason it earns its keep.
   No abstraction without a reference need.

## Keep the boundaries explicit

The dependency directions and layer boundaries you adopt here aren't decoration — state them
plainly: which folders belong to which layer, and which dependency directions are forbidden
(no layer reaches sideways or upward, modules talk only through public services). Keep that
map in the project's docs and aligned to the actual tree, and revisit it whenever the layout
moves, so drift is caught by review instead of slipping in unnoticed.

The point of the building phase is that there's nothing for the audit phase to find.
