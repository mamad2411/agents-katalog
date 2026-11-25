---
name: go-version-manager
description: Detect, select, switch, and verify Go toolchains for a repository without mutating global system state. Use when a Go build reports an incompatible GOROOT or standard-library package, when go.mod/go.sum behavior differs across Go versions, when multiple Go versions are installed, when choosing a Go binary for go mod tidy/test/build, or when setting up a repeatable multi-version Go workflow.
---

# Go Version Manager

Choose the project-compatible Go toolchain before changing dependencies. Prefer the machine's existing `goenv` installation for real version switching. Fall back to explicit binary paths when no supported version manager is available.

## Workflow

1. Read `go.mod` completely enough to identify `go`, `toolchain`, and `replace` directives.
2. Run `.agents/skills/go-version-manager/scripts/go-version-manager.sh requirement <project-dir>`, `manager`, and `list`.
3. Run `.agents/skills/go-version-manager/scripts/go-version-manager.sh select <project-dir>` to choose an installed binary.
4. Confirm the selected binary with `<go-binary> version` and `<go-binary> env GOROOT GOTOOLCHAIN GOPATH GOMODCACHE GOCACHE`.
5. Choose the switching scope:
   - For one command, use the script's `exec` command. With `goenv`, it sets `GOENV_VERSION` only for that command.
   - For the current terminal, run the command printed by `shell-command` (normally `goenv shell <version>`).
   - For a repository-persistent selection, use `switch-local`; this runs `goenv local <version>` and writes `.go-version`, so do it only when the user authorizes a repository change.
   - Change `goenv global` only when the user explicitly requests a machine-wide default change.
6. Review `git diff -- go.mod go.sum` after any module command.
7. Report the selected version, commands run, dependency changes, and verification result.

## Selection rules

- Prefer an exact `toolchain goX.Y.Z` installation.
- Otherwise prefer the highest installed patch within the `go X.Y` minor line.
- Treat the `go` directive as the minimum language/toolchain requirement, not permission to upgrade the module directive.
- Use a newer minor only when no compatible same-minor installation exists, and explain the risk before module mutations.
- Do not set `GOROOT` for a normal Go installation; the selected `go` binary determines it.
- Do not rewrite `/usr/local/go`, system symlinks, shell profiles, or global PATH unless explicitly requested.
- Prefer an installed `goenv` and its installed versions. Honor another existing version manager (`mise`, `asdf`, `g`, `gvm`, Homebrew) when the repository already configures one. Do not introduce a second manager without approval.
- Do not automatically install a missing Go version. Report the missing version and ask before downloading or installing tools.

## Module safety

- Never hand-edit `go.sum` to silence missing checksum errors.
- Run `go mod tidy` only with the selected project-compatible toolchain and when the task authorizes dependency-file changes.
- Prefer `go mod download` or the error's narrowly scoped `go get module@version` when only fetching an existing graph is required; inspect resulting diffs.
- Do not upgrade packages merely to compensate for using the wrong local Go version.
- Do not change the `go` or `toolchain` directive unless the user requests a project toolchain upgrade.
- Preserve unrelated user changes in `go.mod` and `go.sum`.

## Diagnose common failures

- `package slices is not in GOROOT`: the active Go binary is older than Go 1.21. Switch toolchains before touching dependencies.
- `missing go.sum entry`: use the correct toolchain, then fetch or tidy the module graph; do not write checksums manually.
- Cache `operation not permitted`: keep the selected toolchain and redirect only writable caches, for example `GOCACHE=<writable-temp-dir>`. Redirect `GOMODCACHE` only when necessary because it can trigger full dependency downloads.
- Mock/test binary requires special flags or external services: distinguish compilation from execution. Use `go test -c -o <temp-file> <package>` for compile-only verification when package initialization prevents local execution.
- A command unexpectedly changes many dependencies: stop, inspect `go version`, `go env GOTOOLCHAIN`, module directives, and the diff before proceeding.

## Verification ladder

Use the lowest sufficient level, then escalate by risk:

1. `<go> version` and `<go> env ...`
2. `<go> mod verify`
3. Targeted `<go> test ./path/to/changed/package`
4. Compile-only `<go> test -c -o <temp-file> ./package`
5. Broader `go test ./...` or project build command

If dependency downloads or writes outside the workspace require approval, request it rather than bypassing sandbox or network controls.

## Script

Use `.agents/skills/go-version-manager/scripts/go-version-manager.sh`:

```bash
# Show go/toolchain requirements
.agents/skills/go-version-manager/scripts/go-version-manager.sh requirement /path/to/project

# List discovered Go binaries
.agents/skills/go-version-manager/scripts/go-version-manager.sh list

# Show which switching backend is available
.agents/skills/go-version-manager/scripts/go-version-manager.sh manager

# Print the selected Go binary
.agents/skills/go-version-manager/scripts/go-version-manager.sh select /path/to/project

# Execute with the selected binary
.agents/skills/go-version-manager/scripts/go-version-manager.sh exec /path/to/project -- test ./...

# Print the command that switches the current terminal
.agents/skills/go-version-manager/scripts/go-version-manager.sh shell-command /path/to/project

# Persist the selection for this repository (writes .go-version)
.agents/skills/go-version-manager/scripts/go-version-manager.sh switch-local /path/to/project
```

The script is read-only except for `switch-local`, which writes `.go-version`, and effects caused by the Go subcommand supplied to `exec`.
