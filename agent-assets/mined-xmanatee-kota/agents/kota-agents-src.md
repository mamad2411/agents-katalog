# Source Tree

`src/` has two layers:

- `src/core/` is the small runtime kernel: protocols, lifecycle, daemon,
  workflow execution, eventing, sessions, and shared contracts.
- `src/modules/` contains scope-owned modules that contribute tools,
  workflows, agents, skills, channels, routes, commands, and services.

Root `src/*.ts` files should stay rare and act only as public entrypoints or
thin repo-wide glue.

Guidelines:

- Keep `src/core/` protocol-oriented.
- Put swappable features in modules.
- Avoid aliases, compatibility wrappers, and parallel surfaces between core and
  modules.
- Read the local `AGENTS.md` before changing a subtree.

## Root Layout

Keep public entrypoints and genuinely cross-subsystem integration scenarios at
the `src/` root. Unit tests and component fixtures belong beside their owning
core area or module. Cross-cutting fixtures are exceptional: prefer an owned
typed builder or semantic scenario over a root-level data catalog.

- Entrypoint sources (`cli.ts`, `init.ts`, `module-api.ts`,
  `validate-queue.ts`) and their paired unit tests (`cli.test.ts`,
  `init.test.ts`).
- Cross-subsystem integration and repo-wide journeys: `*.integration.test.ts`.
  Each retained journey identifies the real composition failure it catches;
  single-owner checks remain beside their owner in the owner portfolio.
- Shared fixtures co-located with cross-cutting integration tests when
  they span multiple subsystems and have no single owning module
  (e.g. `conversational-cross-store-fixture.integration.ts`).

Every other unit test lives next to the code it exercises under
`src/core/<area>/` or `src/modules/<module>/`. If a test legitimately spans
multiple subsystems, name it `*.integration.test.ts`; otherwise move it to
the owning subsystem. Standards owns verification admission and portfolio
membership; directory layout follows the behavior's production owner.

Core tests may not use `#modules/*` imports. A test that genuinely needs to
load or reference product modules belongs at the root integration tier, not
under `src/core/`; package boundaries are the authority, not a copied source
catalog.

## Strict Types Policy

Production TypeScript stays strict. Decode untrusted boundary values into
precise domain types before use; test decoder rejection and propagation rather
than source syntax or per-file type-token counts. See `src/core/AGENTS.md`.
