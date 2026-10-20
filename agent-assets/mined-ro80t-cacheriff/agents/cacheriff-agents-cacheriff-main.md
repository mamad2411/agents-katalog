# AGENTS.md

Instructions for AI coding agents working in this repository.

## What this is

cacheriff is a lazygit-inspired terminal UI (Bubble Tea) for inspecting and
cleaning up package-manager caches, globally installed packages, and
per-project install artifacts across npm, pnpm, yarn, bun, deno, cargo, and
Go.

## Build, test, run

```sh
go build ./...               # build
go vet ./...                  # static analysis
go test ./... -race -cover    # tests
gofmt -l .                     # formatting check (fix with gofmt -w .)
go run .                       # run the TUI
```

These are the same checks CI runs (`.github/workflows/ci.yml`). Run them
before considering a change done.

## Code layout

- `internal/driver` — one file per package manager, each implementing the
  `Driver` interface (`driver.go`). Concrete drivers embed `base` (`base.go`)
  for common plumbing (ID/Name/Available/SupportedOS/LocalArtifactDirNames/
  LocalInstallDir) and shared helpers (`runOutput`, `runCombined`,
  `singleDirCacheEntries`, `sizeCacheDirs`, `unsupportedKindErr`, `dirSize`).
  Only implement what genuinely differs per package manager: `CacheDir`,
  `CacheEntries`, `GlobalInstallDir`, `GlobalPackages`, `LocalPackages`, and
  `Remove`.
- `internal/ui` — the Bubble Tea model/view/keys/commands/messages/styles.
- `internal/theme` — color roles as plain hex strings, with no dependency on
  the rendering library (so the same definitions could back a future Neovim
  port directly via `guifg`/`guibg`).
- `internal/config` — user config file loading, lazygit-inspired: an
  optional YAML file with a `gui.theme` section, location overridable via
  `CCF_CONFIG_FILE` (like lazygit's `LG_CONFIG_FILE`).
- `internal/platform` — OS detection for drivers that are OS-specific.
- `internal/textwrap` — TUI text wrapping and argv-safety helpers.

## Comment style

Comments in this codebase are intentionally minimal: default to none: only
add one when the *why* isn't derivable from the code itself (a hidden
constraint, a workaround, a non-obvious invariant). Don't restate what a
well-named function or type already says. Keep new code consistent with
this — see `git log` for the commit that trimmed the codebase to this style
if you want a before/after reference.

Because of that, some non-obvious reasoning that used to live inline no
longer does. The sections below preserve it for agents that need the
context but shouldn't be re-added as comments unless something changes.

## Design invariants worth knowing

### Driver interface & `base`

- `localDir == ""` in `base` means "no per-project install directory":
  cargo, Go, and Deno resolve dependencies into a single shared,
  machine-wide cache (CARGO_HOME's registry, GOMODCACHE, DENO_DIR) rather
  than copying them into the project the way npm copies into
  `node_modules`. `LocalInstallDir` returns `("", false)` in that case.
- `EntryKind` (`KindCache`/`KindGlobalPackage`/`KindLocalPackage`)
  distinguishes what an `Entry` represents; `Remove` switches on it.
- `Entry.Size == -1` means "unknown/not computed"; `Entry.Version == ""`
  means "not applicable" (e.g. a cache directory has no version).

### Performance

- Cache directories are sized concurrently (`sizeCacheDirs`, cargo's and
  Go's `CacheEntries`, Deno's `denoCacheEntriesFromInfo`) because some
  caches — npm/bun/pnpm/yarn's content-addressable stores, cargo's
  `registry/src`, GOMODCACHE — hold huge numbers of small files, and
  walking them one after another would be slow.
- `dirSize` checks `ctx` on every filesystem entry so a large walk aborts
  promptly when the caller's timeout fires (`loadTimeout` = 2 min, in
  `internal/ui/model.go`).

### CLI quirks drivers work around

- `npm ls -g --json` / `npm ls --json` exit non-zero on any
  dependency-tree problem (e.g. one extraneous package) even though they
  still print valid JSON — only bail if the output can't be parsed.
- `go version -m` has the same non-zero-exit-but-valid-output behavior when
  scanning binaries it can't read build info from.
- Yarn Classic 1.22's `yarn global list --json` only emits progress events,
  never the actual package list — `GlobalPackages` reads the global
  `package.json`'s declared dependencies directly instead.
- `bun pm ls -g`'s global install root is read from its own output (first
  line) rather than assumed to be `$BUN_INSTALL/install/global`, since
  `bunfig.toml` can redirect it elsewhere.
- Deno has no command that lists `deno install -g` tools with resolved
  versions — `GlobalPackages` scans the bin directory's generated shim
  scripts and reports each one's target specifier (e.g. `npm:cowsay`) as
  the Version.
- On Windows, `cargo install --list` doesn't include the `.exe` suffix on
  binary names — `cargoBinSize` falls back to trying it.
- Go's module cache path escaping (`escapeModulePath`) replaces each
  uppercase letter with `!` + its lowercase form, matching
  `golang.org/x/mod/module.EscapePath`, since GOMODCACHE must work on
  case-insensitive filesystems too.
- rustup toolchains aren't listed via `rustup toolchain list` —
  `cargoToolchainEntries` reads `RUSTUP_HOME/toolchains` directly, since
  the directory can exist (and be worth reporting) even when rustup
  itself isn't on PATH. Removal still shells out to `rustup toolchain
  uninstall`, since `cargo` has no equivalent subcommand.

### Security

- `textwrap.EscapeArg` validates package names before they're passed to a
  driver's uninstall command. Every arg reaches the OS as a discrete argv
  element via `exec.CommandContext` (never a shell string), so classic
  shell-metacharacter injection can't happen regardless of input. What it
  actually guards against is **argument injection**: a name starting with
  `-` could be misread as a flag (e.g. a package literally named
  `--force`), and control characters have no legitimate place in a name
  either. It rejects such values rather than rewriting them — silently
  stripping characters would just make the name stop matching anything
  real, which is worse than failing loudly.

### UI (Bubble Tea)

- `driverDataMsg`/`packageRemovedMsg` carry a `gen` field so a stale async
  result (from a load or remove the user has since abandoned by selecting
  something else) is discarded instead of overwriting newer state.
- Only global packages support uninstall today — no driver's `Remove`
  implements `KindLocalPackage` yet.
- `ui.SetTheme` must be called once, before the program starts (see
  `main.go`), to apply a user-configured color scheme from
  `internal/config`.
- Panels use lipgloss `Border` + `Padding(0, 1)` with manual text wrapping
  (`textwrap.ContentLine`) to their real usable width before rendering:
  lipgloss's `Height()` doesn't clip overflow, so an unwrapped long line
  would grow the box past its declared height and misalign it against its
  neighbor.

## Adding a new package manager driver

1. Create `internal/driver/<name>.go`, embed `base`, implement `Driver`.
   Use an existing driver (`npm.go`, `cargo.go`, etc.) as a reference.
2. Register the constructor in `All()` in `driver.go`.
3. Add `<name>_test.go`.
4. Make sure `Available()` can be called safely even when the CLI isn't
   installed.

See also `.github/CONTRIBUTING.md` for the human-facing version of this.
