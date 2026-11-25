---
name: module-scaffold
description: Generate a complete module following the project's declared architecture — entity, repo, service/use-case, DTOs, controller, tests, DI wiring, migration. Use when creating a new feature module from scratch or replacing a prototype with a properly-layered version. Emits structure, not verified behaviour — run `endpoint-test-method` on each scaffolded route once wired.
kind: skill
pack: backend
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# module-scaffold

## Premise

Existing siblings are the truth. Mirror their shape — file names, folder layout, import order, DI token style, barrel exports, test naming — exactly. Do not invent a new layout, do not "improve" the conventions, do not skip steps because the sibling looks "old-fashioned". Refuse to scaffold without naming a specific sibling module (path) you mirrored. A scaffolded module that doesn't match its siblings IS the bug.

Refuse to generate `// TODO` stubs in place of real working code; the smoke spec must compile and pass.

End-to-end module generator. Mirrors a sibling module exactly so layout, imports, DI tokens, and test conventions stay consistent.

## When to use

- Creating a new feature module from scratch.
- Onboarding — generate a known-good module structure to study.
- Replacing an old prototype with a properly-layered version.

## Prerequisites

- The project's architecture doc: `ai/patterns/project-structure.md` or equivalent.
- At least one existing sibling module to mirror — never invent layout from scratch.
- Migration tooling installed (Prisma / TypeORM / Alembic / etc.).
- Test runner configured (Jest / Vitest / pytest / Go test).

## Procedure

1. Gather inputs. **Read what the codebase answers; ask only what it cannot.**
   - From the caller or the user: module name (kebab-case), one-line purpose, and the route set `/add-module`'s aggregate-shape ledger admitted (never a default five).
   - From the sibling and extraction, not from the user: multi-tenant posture, soft-delete convention, translatable/i18n convention. All three are visible in the sibling module; asking is the "ask the user about layout" failure `/add-module`'s premise forbids. Ask only when no sibling exists.
   - From the sibling: whether this project has webhook receivers / queue consumers / scheduled jobs at all — a primitive the project has never used is an escalation, not an input.
2. Read `ai/patterns/project-structure.md` to confirm the declared layout.
3. Read a sibling module — note exactly: file names, folder layout, import order, DI token style (Symbol vs string), barrel exports vs direct imports, test file naming.
4. Consult any framework reference (`.claude/references/<framework>.md`) for idiomatic shape.
5. Generate every file from step "What gets generated" below — each with a real working stub (not a TODO comment).
6. Add the new module to:
   - The app's root module imports.
   - `ai/modules.md` with a one-line row.
   - `ai/status.md` `## Recent Changes` (date + brief).
7. Generate the migration file for the entity (reversible — both `up()` and `down()`).
8. Run the linter + type-checker on generated files; fix any issues before reporting done.

## What gets generated

The exact file tree depends on the project's declared layout (Step 2: read `ai/patterns/project-structure.md`; Step 3: mirror a sibling module). The example below shows ONE plausible layout (Clean / Hexagonal — `core/application/infrastructure/adapters` per module). Adapt to the project's actual layout: a Rails project gets `app/{models,controllers,services}/`; a Django project gets `<app>/{models,views,serializers,urls}.py`; a Go project gets `internal/<feature>/{handler,service,store}.go`; a flat Express app gets `routes/<feature>.js + services/<feature>.js + models/<feature>.js`. Mirror the sibling — don't impose this Clean-Architecture shape on a project that doesn't use it.

```
# Example layout (Clean/Hexagonal — use only if the project's sibling modules look like this)
modules/<name>/
├── core/
│   ├── entities/<name>.<ext>               domain model
│   ├── errors/<name>-not-found.error.<ext> custom exception
│   ├── ports/<name>.repository.<ext>       interface
│   └── ports/<name>.service.<ext>          interface (if applicable)
├── application/
│   └── use-cases/
│       ├── create-<name>.use-case.<ext>
│       ├── get-<name>.use-case.<ext>
│       ├── list-<name>.use-case.<ext>
│       ├── update-<name>.use-case.<ext>
│       └── delete-<name>.use-case.<ext>
├── infrastructure/
│   └── persistence/
│       ├── <name>.orm-entity.<ext>         ORM entity (whatever ORM the project uses)
│       ├── <name>.repository.impl.<ext>    implements port
│       └── <name>.mapper.<ext>             ORM <-> domain
├── adapters/
│   └── http/
│       ├── <name>.controller.<ext>
│       └── dtos/
│           ├── create-<name>.dto.<ext>
│           ├── update-<name>.dto.<ext>
│           └── <name>.response.dto.<ext>
├── tokens.<ext>                            DI tokens (Symbol / string / framework-native — match project)
├── <name>.module.<ext>                     framework module wiring (NestJS @Module / Spring config / Django app / etc.)
├── <name>.module.spec.<ext>                wiring smoke test
└── __tests__/
    ├── create-<name>.use-case.spec.<ext>   unit
    ├── <name>.repository.impl.spec.<ext>   integration
    └── <name>.controller.e2e-spec.<ext>    e2e
```

Plus:
- TypeORM/Prisma migration in `database/migrations/` (or `prisma/migrations/`).
- Row in `ai/modules.md`.
- Entry in `ai/status.md` "Recent Changes".

## Generated-file invariants

- Every DTO is validated **in the sibling's validation library** — every input field carries a validator. The library is read from the sibling at step 3, not chosen from a shortlist: introducing `zod` into a `class-validator` project is the drift `/add-module`'s sibling-shape halt rejects.
- Every query in the repo includes the tenant filter if the project is multi-tenant.
- Every entity extends the project's soft-delete base class (whatever name it uses — detected from extraction) if soft-delete is in use.
- DI tokens defined in `tokens.<ext>` **in the sibling's token style** (Symbol / string / framework-native, as read at step 3) — never inline at the injection site, and never a style the sibling does not use. This invariant used to read "Symbols, never strings", which issued the opposite order to the premise above on any project whose siblings use string tokens — and `/add-module`'s sibling-shape halt then flagged this skill's own output as `drifted`.
- Migration is reversible — both `up()` and `down()` populated, no `// TODO`.
- Test files import from the public surface (the module's barrel or controller), not internal paths.

## Output

```
Module scaffold — orders

Files written: 18
Files updated:  3   (app.module.ts, ai/modules.md, ai/status.md)
Migration:      database/migrations/20260424093000-create-orders.ts (reversible)

Lint:           PASS
Type-check:     PASS
Smoke spec:     orders.module.spec.ts PASS

Next steps:
  1. Run migration: bun run migration:run
  2. Implement business logic in use-cases (currently CRUD-only).
  3. Replace the stub success message in locales/en.json + ar.json.
  4. Add domain-specific endpoints beyond CRUD.
```

## False positives / gotchas

- Don't invent a new file layout — mirror the chosen sibling exactly. Inconsistency is the bug, not "improvement".
- Tests that pass with `// TODO: assertion` are worse than no tests — every spec must have a real assertion or the file is rejected.
- Generated mappers must handle null/undefined relations — don't assume eager loading.
- Migration `down()` that just runs `DROP TABLE` is acceptable; `down()` that's empty or `// not implementable` blocks the scaffold.
- Business logic is NOT scaffolded — only CRUD plumbing. Schema design for non-trivial tables: defer to a `schema-architect` agent.

## Related

- Used by `@api-architect` — that agent designs the module shape, then drives module-scaffold to generate the layered files against a named sibling.
- `.claude/skills/endpoint-test-method/SKILL.md` — verify each scaffolded route end-to-end once the module is wired.
- `.claude/skills/api-snapshot/SKILL.md` — new endpoints surface as additive diffs; snapshot confirms the generated contract.
- `ai/patterns/api-contract.md` — the input/output-DTO + envelope shape every generated DTO must follow.
- `ai/patterns/multi-tenancy.md` — the tenant-filter invariant every generated repository query must include.
- `.claude/rules/backend-principles.md` — the architecture / layering MUSTs the scaffold mirrors from the chosen sibling.

## Halt conditions

- Halt if no sibling module path was named — refuse to scaffold "from the architecture doc alone". Mirror a real, existing module.
- Halt if the generated layout deviates from the named sibling (different folder names, different file names, different DI token style). Inconsistency is the bug.
- Halt if any spec file contains `// TODO: assertion` or no real assertion — empty tests are worse than no tests.
- Halt if the migration `down()` is empty or `// not implementable` — non-reversible migrations are rejected.
- Halt if lint / type-check fails on the generated files — do not declare done with red signals.
