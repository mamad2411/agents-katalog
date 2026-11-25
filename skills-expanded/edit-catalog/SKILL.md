---
name: edit-catalog
description: Catalog edits in YAML or Go. Use for any task that adds an App, changes an App's image, port, Compose, env, notes or StandaloneGuide (even a one-line image bump), changes a Recipe, or hides or unhides an App. Each of these changes generated site and DCM data and the generated e2e inventory. DCM-only Containers go to add-container; Homarr wiring goes to docs/agents/homarr-integrations.md.
---

# Edit the Catalog

Read `CONTEXT.md` for App, Recipe and Catalog, and `docs/agents/generated-data.md` for what is derived from what. For a new App, copy the shape of the last one: `git show --stat ca78641b` (Cleanuparr).

Pick the branch, then run its steps in order:

- **New App**: steps 1 to 8.
- **Change an App**: steps 1, 2, 6 and 8, plus 5 when its repository or icon changes. If `internal/catalog/specs/<id>.yaml` exists, edit that file. Otherwise edit the App's package under `internal/apps/`; its directory is the id without hyphens or a shorter name (`paperless-ngx` lives in `paperlessngx`), so find it with `grep -rl 'ID: "<id>"' internal/apps`.
- **Change a Recipe**: edit `defaultRecipes` in `internal/catalog/recipes.go`, then steps 6, 7 and 8.
- **Hide or unhide an App**: edit `unavailable` in `internal/catalog/catalog.go` with the reason and the issue that tracks the way back, then steps 6, 7 and 8.

## 1. Resolve upstream facts

Take the image, tag, ports, volumes and env from the project's own docs or registry page, not from memory or an aggregator.

**Done:** each fact has a source URL you can put in the PR body.

## 2. Find an existing home

Search `internal/apps/`, `internal/catalog/`, `dcm/src/tools/` and `ALIASES` in `dcm/src/lib/selfhost.ts` for the product under every spelling (`actualbudget` against `actual-budget`).

**Done:** no hit, so you add one App, or you edit the existing App and add none. Every Container for the same product in `dcm/src/tools` has the App's id or an `ALIASES` key for it; otherwise DCM lists the product twice. Add the missing `ALIASES` entry in the same change.

## 3. Write the App

Write `docs/catalog/traps/<id>.md` (it keeps the hyphens) and then the App. The description is at most 100 characters in plain words (`internal/catalog/descriptions_test.go` enforces it). Extra services are named `<id>-...`.

- **YAML, the default.** When Setup only proves the web page answers (`setup.kind: no-account`), write `internal/catalog/specs/<id>.yaml`: copy `specs/ollama.yaml` and read "Declarative spec" in `docs/catalog/adding-apps.md` for the keys. No Go, no test and no registration; `<id>.yaml` is the file name and its first line is `# Traps: docs/catalog/traps/<id>.md`.
- **Go.** For extra Setup steps, a first administrator, Links or deferred services, add `internal/apps/<name>/<name>.go` and its test, where `<name>` is the id without hyphens. `Info().ID` is the id itself. Setup follows `internal/helpers/` and the Protected invariants in `AGENTS.md`: credentials stay in the private Project `.env`, and public Host settings are filtered before output.

**Done:** `go test ./internal/appspec/ ./internal/catalog/` passes for a spec, `go test ./internal/apps/<name>/` for Go.

## 4. Register

A spec is embedded and needs no registration; skip to step 5. For a Go App, run `go run ./tools/registrygen`. It scans `internal/apps/` and rewrites `internal/catalog/apps_gen.go`; never edit that file by hand.

**Done:** `git diff internal/catalog/apps_gen.go` shows your App's import and registration, and `go test ./internal/catalog/` passes. A `parity_test.go` failure on a ported App means a legacy fact changed: add a `deviations` entry with the reason; leave `legacy-facts.json` as it is.

## 5. Declare site metadata

Usually nothing. The icon defaults to `svg/<id>.svg` on Dashboard Icons, and sitegen checks that a new path exists. Add the id to `iconOverrides` in `tools/sitegen/icons.go` only when the icon lives at another path (`""` for none). The star repository comes from `Docs` when it is a `github.com/<owner>/<repo>` URL; otherwise add the upstream repository to `starRepoOverrides` in `tools/sitegen/stars.go` (`""` for none). Nothing fails when an App has no repository; its star count never appears.

**Done:** `go run ./tools/sitegen` passes, and `Docs` is the GitHub repository or the id is in `starRepoOverrides`.

## 6. Regenerate

```bash
go run ./tools/sitegen
```

Add `standalone_guide` (or `StandaloneGuide()` in Go) only when its standalone Compose needs a sentence of guidance; sitegen fails when the guide names a variable or folder the converted Compose lacks.

**Done:** a second run changes nothing, and `git status` shows only your files plus `site/src/data/catalog.json` and `dcm/src/data/selfhost.json`.

## 7. Refresh the goldens and inventory

App and Recipe counts are computed, so no README or `e2e/acceptance.md` number moves. Regenerate the two files that record the Catalog:

```bash
go test ./internal/tui -update
go test ./e2e -run TestAcceptanceInventory -update
```

Read both diffs: in the goldens only the `N more` line moves, and `e2e/testdata/inventory.json` gains or loses the App.

**Done:** `go test ./e2e/ ./internal/tui` passes and `git status` shows no `README.md` change.

## 8. Gate

Run the Go gate from `AGENTS.md`, then the web gate: generated data changed. Never run Docker, `e2e` or the installer.

**Done:** both exit 0 and `git status` shows only files that belong to this change.
