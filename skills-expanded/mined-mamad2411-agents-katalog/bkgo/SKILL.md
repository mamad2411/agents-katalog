---
name: bkgo
description: Enforces the bkgo CLI workflow for Go backend projects using Hexagonal Architecture. Use this skill whenever working on a bkgo-based project — creating a new project, adding a module, removing a module, generating individual layers (handler, service, repository), writing or editing code in any internal/<module>/ file, or reviewing project structure. Trigger this even if the user just says "add a user module", "create a new service", "remove the payment module", or "scaffold a new Go project" without mentioning bkgo by name — any structural change to a bkgo project must go through the CLI, not manual file creation.
---

# bkgo — Hexagonal Architecture CLI

This project uses `bkgo` as the **only approved tool** for creating, generating, and removing backend project structure. Do not manually create module folders or base files if `bkgo` can handle it. Bypassing the CLI breaks the generated structure that the rest of the codebase depends on.

## Before doing anything structural

Always inspect first — never assume the current state:

```bash
ls
find internal -maxdepth 2 -type f
```

Check whether the target module already exists before generating it:

```bash
ls internal/<module-name>
```

## Verify bkgo is available

Before running any `bkgo` command, confirm the CLI is present:

```bash
which bkgo
bkgo --help
```

If not found:

```bash
go install github.com/BounkhongDev/bkgo/cmd/bkgo@latest
export PATH="$PATH:$(go env GOPATH)/bin"
```

For zsh on macOS, persist the PATH:

```bash
echo 'export PATH="$PATH:$(go env GOPATH)/bin"' >> ~/.zshrc && source ~/.zshrc
```

**Only proceed manually if the user explicitly approves or the CLI cannot support the required operation.** If `bkgo` is missing and can't be installed, say so and wait for approval before touching files by hand.

---

## Operations

### New project

```bash
bkgo new <project-name>
# with custom module name:
bkgo new <project-name> --module github.com/<org>/<project-name>
```

Do not manually create the base folder structure. The generated project is the source of truth.

### Generate a module

```bash
bkgo generate module <module-name>
# alias:
bkgo g module <module-name>
```

Generated structure:

```
internal/<module>/
├── domain.go       ← entity + repository interface (Port)
├── usecase.go      ← business logic
├── handler.go      ← HTTP handler (Fiber)
└── repository.go   ← PostgreSQL implementation (Adapter)
```

Note: `usecase_test.go` is **not** auto-generated — create it manually after generation.

### Generate an individual layer

When a module exists but one layer is missing:

```bash
bkgo g handler <module>
bkgo g service <module>
bkgo g repository <module>
```

### Remove a module

```bash
bkgo remove module <module-name>
# alias:
bkgo rm module <module-name>
```

Remove an individual layer:

```bash
bkgo remove handler <module>
bkgo remove service <module>
bkgo remove repository <module>
```

Do not manually delete generated folders or files unless `bkgo` cannot handle the case.

### Manage the bkgo dependency

```bash
bkgo upgrade                    # bump github.com/BounkhongDev/bkgo + go mod tidy
bkgo upgrade --version v0.2.6   # pin a specific version
bkgo upgrade --cli              # upgrade the installed bkgo CLI binary
bkgo uninstall                  # drop bkgo from go.mod (refuses while code imports it)
bkgo uninstall --cli            # delete the installed CLI binary
```

Use these instead of editing `go.mod` by hand or running `go get github.com/BounkhongDev/bkgo` directly.

---

## Naming

Pass module names to `bkgo` directly — it normalizes casing automatically:

| Input | Package | Struct |
|---|---|---|
| `user` | `user` | `User` |
| `orderItem` | `order_item` | `OrderItem` |
| `order-item` | `order_item` | `OrderItem` |
| `order_item` | `order_item` | `OrderItem` |

Prefer clear domain names: `user`, `shipment`, `payment`, `orderItem`, `trackingEvent`.
Avoid vague names: `data`, `helper`, `common`, `misc`, `test`.

---

## Development workflow

When adding a new feature:

1. Generate the module with `bkgo g module <name>`
2. Review the generated files
3. Add/adjust entity fields in `domain.go`
4. Implement business logic in `usecase.go`
5. Implement database logic in `repository.go`
6. Expose API routes in `handler.go`
7. Add/update tests in `usecase_test.go`
8. Run formatting and tests:

```bash
go fmt ./...
go vet ./...
go test ./...
```

---

## Architecture rules (summary)

See `references/architecture.md` for the full layer-by-layer rules. The cardinal rules are:

- **No HTTP logic in `domain.go`** — entities and interfaces only
- **No database implementation in `domain.go`** — that belongs in `repository.go`
- **No business logic in `handler.go`** — handlers call usecases, nothing more
- **No infrastructure imports in domain logic** — usecases depend on interfaces, not concrete adapters
- **No renaming or deleting generated files** without a clear reason

---

## Agent rules checklist

Before writing or editing any code in this project, confirm:

- [ ] `bkgo` is installed and reachable
- [ ] Current structure has been inspected (`find internal -maxdepth 2 -type f`)
- [ ] Target module existence has been checked before generating
- [ ] New modules are generated via `bkgo g module`, not created manually
- [ ] Each layer's responsibilities match `references/architecture.md`
- [ ] After changes: `go fmt ./...` and `go test ./...` have been run
