---
name: product-development
description: The four-phase product development workflow this repository is built for — discover, prototype, build, ship — what each phase produces, and the gates between them. Use when planning or running product work, when asked how long something will take, when deciding what to cut, or when a phase's slash command needs the method behind it.
license: MIT
---

# Product development, in four phases

From a sentence to a deployed multi-tenant SaaS with auth, organizations, roles,
a public API and whatever the product actually is.

It works because most of it is already built. This repository ships the things
every B2B product needs and nobody demos — identity, tenancy, access control, an
audit trail, API keys, a versioned public API — so the work goes on the part that
is specific to the product.

## The four phases

| Phase     | Produces                                             | Gate                                    |
| --------- | ---------------------------------------------------- | --------------------------------------- |
| Discover  | A written riskiest assumption and a cut feature list | The assumption is written down          |
| Prototype | Real screens against the real shell                  | No migrations were needed               |
| Build     | Vertical slices, each green                          | Every slice passes the full gate        |
| Ship      | Deployed, with the isolation tests still passing     | Nothing on the ship checklist is untrue |

Each has a slash command — `/product-discover`, `/product-prototype`,
`/product-build`, `/product-ship` — and a file under `docs/workflow/` that the
command reads.

## What makes it survive contact

**The riskiest assumption is written before anything is built.** Skipping it
builds the wrong thing on schedule, which is worse than building nothing slowly.

**The prototype phase may not add a migration.** That single constraint is what
keeps the phase short. If a screen needs a schema, it is a build, and it goes in
the list rather than in this phase.

**A slice is not done until the whole gate passes**, including the browser tests.
Not the compiler — the gate. On this repository that has already caught a Node
subpath import the compiler resolved and Node could not, and a lint fix that
satisfied the linter while breaking Playwright at run time.

**`docs/workflow/STATE.md` is the memory.** Product work outlives any session's
context. Each command writes where it got to; `SessionStart` reads it back.
Without that the loop restarts every time a context window does.

## What to cut first

In order, when the build phase will not fit:

1. A second frontend, an admin panel, anything cross-tenant
2. Configurability — one hard-coded value beats a settings screen nobody asked for
3. Integrations beyond the first
4. The dashboard. Almost nothing needs it at the start

What never gets cut: tenant isolation, the audit trail, and the tests that prove
both. Those are the things a security review asks about, and retrofitting them
costs more than building them did.
