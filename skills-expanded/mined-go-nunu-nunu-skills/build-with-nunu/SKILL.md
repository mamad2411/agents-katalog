---
name: build-with-nunu
description: Build and evolve production Go applications with go-nunu. Use when choosing or scaffolding a Nunu layout; implementing or refactoring features across api/v1, handlers, services, repositories, models, routers/servers, config, migrations, jobs, tasks, MCP tools, or Wire; testing and debugging Nunu projects; or maintaining the Nunu CLI and templates. Trigger on go-nunu, Nunu layouts, `nunu new/create/run/wire`, or clear Nunu conventions. Do not use for generic Go work without Nunu context.
---

# Build with Nunu

Deliver a working vertical slice that fits the repository's actual Nunu layout. Treat nearby code, local instructions, `go.mod`, and existing build targets as stronger evidence than remembered examples.

## Start with reconnaissance

1. Read `AGENTS.md`, `CLAUDE.md`, and other repository instructions in scope.
2. Run `scripts/inspect-nunu-project.sh [path]` from this skill directory.
3. Read [references/layouts.md](references/layouts.md) and classify the project from evidence. Do not assume every Nunu repository uses the same folders.
4. Trace one neighboring feature end to end, including tests and generated-code boundaries.
5. Check `git status` and preserve unrelated user changes.

If the directory is not a Nunu project, say what evidence is missing and use ordinary Go conventions instead of forcing this architecture.

## Shape the change

Resolve only decisions that materially affect the implementation: behavior, transport, auth, persistence, compatibility, and target app in a monorepo. Infer the rest from the closest complete feature.

For feature work, read [references/vertical-slices.md](references/vertical-slices.md). Write a compact artifact map before editing:

```text
contract -> model/migration -> repository -> service -> handler -> router/server -> Wire -> tests/docs
```

Omit layers the feature genuinely does not need. Keep dependency flow inward: transports depend on services, services depend on repository interfaces, and repositories own persistence details.

## Implement the vertical slice

1. Define request, response, and domain error behavior before transport code.
2. Add or adjust persistence models and migration behavior without hiding schema changes.
3. Put repository interfaces at the consumer boundary used by the local layout. Pass `context.Context`; use the repository's transaction-aware database accessor when one exists.
4. Keep business rules, authorization decisions, and transaction orchestration in services.
5. Keep handlers thin: bind and validate input, call a service, log with request context, and translate errors through the project's response helpers.
6. Register HTTP routes, MCP capabilities, jobs, or tasks in the layout's established composition point.
7. Add constructors to every relevant Wire provider set. Edit `wire.go`; never hand-edit `wire_gen.go`.
8. Update Swagger/OpenAPI or other generated artifacts only when the repository tracks them and the contract changed.

Use `nunu create all <feature>` only as an optional seed when the CLI is installed and the target files do not exist. Inspect its output immediately: modern layouts may require additional API, router, transaction, or Wire work. Never overwrite a customized feature with generated stubs.

## Regenerate and verify

Read [references/testing.md](references/testing.md), then use the narrowest relevant commands discovered in the repository.

1. Format changed Go files with `gofmt` or the repository formatter.
2. Regenerate Wire after constructor signatures or provider sets change. Prefer an explicit target such as `nunu wire cmd/server/wire`; use `nunu wire all` only when multiple injectors are affected.
3. Regenerate mocks only after interfaces stabilize. Treat mock files and `wire_gen.go` as generated output.
4. Run focused tests first, then broader package or repository tests.
5. Run the repository's build, vet, lint, race, Swagger, or integration targets when relevant and available.
6. Inspect the diff for accidental generated churn, secrets, missing providers, error-code drift, and unrelated edits.

Do not start Docker, databases, migrations against non-test data, or long-running servers unless the task requires it and the target environment is known.

## Handle specialized variants

- For MCP servers or changes to the Nunu CLI/templates, read [references/mcp-and-cli.md](references/mcp-and-cli.md).
- For monorepos, scope discovery, generation, Wire, and tests to the selected app while preserving shared-package boundaries.
- For legacy/base layouts, follow their flatter server registration and provider-set style rather than backporting Advanced-layout structure without a reason.

## Finish with evidence

Report the user-visible behavior delivered, the layers touched, generated artifacts refreshed, and exact checks run. Distinguish passing checks from checks skipped because an external service or tool was unavailable.
