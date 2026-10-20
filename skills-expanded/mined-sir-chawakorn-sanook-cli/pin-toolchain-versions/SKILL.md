---
name: pin-toolchain-versions
description: Pins language/runtime/CLI versions for identical toolchains across machines and CI — a version manager (mise/asdf/Volta/nvm), exact .tool-versions/.mise.toml pins, engines + packageManager via corepack, frozen-lockfile installs, auto-switch on cd, and CI reading the same pin file.
when_to_use: Version drift across machines or CI ("wrong node/python version"), painful onboarding, or a "works locally, fails in CI" toolchain mismatch. NOT bumping library deps (dependency-upgrade), a containerized env (setup-devcontainer-env), or workspace task orchestration (setup-monorepo-tooling).
---

## When to Use

Reach for this skill when the problem is **which version of the tool runs**, not which library version is installed:

- "CI uses node 18, my laptop has 20 — build passes locally, fails in CI"
- "New hire spent a day getting the right Python/Ruby/Go installed"
- "`pnpm install` produces a different lockfile on the CI runner"
- "Every machine must resolve the exact same node + package-manager version"
- A flaky build traced to a runtime/CLI version that differs by host

NOT this skill:
- Bumping a library/framework dependency and fixing the breakage → dependency-upgrade
- Reproducibility via a container/devcontainer image → setup-devcontainer-env
- Wiring up workspace task runners / package-manager workspaces → setup-monorepo-tooling
- Publishing the resulting package to a registry → publish-package-registry

## Steps

1. **Pick one manager and commit to it — never run two.** Two managers fighting over `PATH` shims is the #1 cause of "it switched back."

   | Manager | Use when | Notes |
   |---|---|---|
   | **mise** | **Default.** Polyglot (node/python/go/ruby/rust/…), fast Rust shims, reads `.tool-versions` *and* `.mise.toml`, runs tasks + env | One tool for every language; drop-in upgrade path from asdf |
   | asdf | Already standardized on it org-wide | Plugin-per-language, slower; mise reads its files unchanged |
   | Volta | JS/TS-only repo, want the toolchain pinned *in package.json* | Pins node+pm under `"volta"`, no separate file |
   | nvm | Minimal, node-only, can't install other tools | `.nvmrc` only, no pm pin, manual `nvm use` |

   Default to **mise** unless the repo is JS-only and you specifically want package.json-embedded pins (Volta).

2. **Pin EXACT versions — never a range, `latest`, or `lts`.** A range re-introduces drift the moment a new patch ships. `.mise.toml`:

   ```toml
   [tools]
   node   = "20.18.1"
   python = "3.12.7"
   pnpm   = "9.15.0"
   ```
   Or `.tool-versions` (asdf/mise compatible):
   ```
   node 20.18.1
   python 3.12.7
   pnpm 9.15.0
   ```
   Full `MAJOR.MINOR.PATCH`. `node = "20"` or `"lts"` resolves differently on a machine that synced its index yesterday vs today — that defeats the purpose.

3. **Pin the package manager too — runtime alone is not enough.** A pinned node with a floating pnpm still produces different lockfiles. Declare both in `package.json` and let corepack enforce it:

   ```jsonc
   {
     "packageManager": "pnpm@9.15.0",            // corepack pins the exact pm
     "engines": { "node": "20.18.1", "pnpm": "9.15.0" }
   }
   ```
   `corepack enable` makes the `pnpm`/`yarn` shim resolve that exact version. Add `engine-strict=true` to `.npmrc` so an out-of-range node **errors** instead of warning. (Volta users: put `"volta": { "node": "20.18.1", "pnpm": "9.15.0" }` in package.json instead — it owns both.)

4. **Commit the lockfile and install frozen in CI.** Pinned tools are wasted if installs still resolve fresh versions. Commit `pnpm-lock.yaml` / `package-lock.json` / `poetry.lock` / `Cargo.lock`, and in CI use the **frozen** install that fails on any drift, never re-resolves:

   | PM | Local install | CI (must fail on drift) |
   |---|---|---|
   | pnpm | `pnpm install` | `pnpm install --frozen-lockfile` |
   | npm | `npm install` | `npm ci` |
   | yarn (berry) | `yarn install` | `yarn install --immutable` |
   | poetry | `poetry install` | `poetry install` after `poetry lock --check` |
   | cargo | `cargo build` | `cargo build --locked` |

5. **Auto-switch on `cd` so nobody runs the wrong version by hand.** Hook the manager into the shell once: append `mise activate zsh` (or `bash`/`fish`) to the rc file; nvm users add `.nvmrc` auto-use logic. Entering the repo now selects the pinned tools automatically — no `nvm use`, no stale shell. Run `mise install` once to materialize the versions and `mise trust` to allow the repo's config.

6. **Make CI read the SAME pin file — never retype versions in YAML.** A hardcoded `node-version: 20` in the workflow is a second source of truth that silently drifts. GitHub Actions:

   ```yaml
   # Option A: native setup reads the pin file directly
   - uses: actions/setup-node@v4
     with:
       node-version-file: '.tool-versions'   # or .nvmrc / package.json
   - uses: actions/setup-python@v5
     with:
       python-version-file: '.tool-versions'

   # Option B (polyglot, simplest): let mise install everything
   - uses: jdx/mise-action@v2                 # reads .mise.toml / .tool-versions
   ```
   `mise-action` is cleanest when you pin >2 languages — one step, the same file the dev uses.

7. **Go hermetic only when "same versions" isn't enough.** A version manager pins the tool but still links the host's system libraries (openssl, glibc), so two "same node" builds can still differ. For bit-for-bit reproducibility (security/compliance), use **Nix flakes** (`flake.nix` + `flake.lock`, `nix develop`) or **devbox** (`devbox.json`, mise-like UX over Nix). Reserve this for projects that genuinely need it — it's heavier and steeper than mise.

## Common Errors

- **Pinning a range or `latest`/`lts`.** `node = "20"` resolves to different patches over time and across machines. Always full `MAJOR.MINOR.PATCH`.
- **Pinning the runtime but not the package manager.** Floating pnpm/yarn/npm produces divergent lockfiles even on identical node. Pin via `packageManager` + corepack.
- **Two managers installed (nvm + mise, or asdf + Volta).** Their `PATH` shims clash and one wins nondeterministically per shell. Pick one; uninstall the other's shell hook.
- **`engine-strict` not set, so `engines` is just a warning.** npm ignores an `engines` mismatch by default. Set `engine-strict=true` in `.npmrc` to make it a hard error.
- **CI hardcodes the version in YAML.** `node-version: 20` drifts from the repo's pin file the day someone bumps one and not the other. Use `node-version-file:` / `mise-action`.
- **Non-frozen install in CI.** Plain `npm install` / `pnpm install` re-resolves and can pick newer deps than the lockfile. Use `npm ci` / `--frozen-lockfile` / `--immutable` / `--locked`.
- **Forgot `corepack enable`.** Then the `pnpm` on PATH is whatever was globally installed, ignoring `packageManager`. Enable corepack locally and in CI before install.
- **Lockfile not committed (or in `.gitignore`).** Frozen install has nothing to enforce against. Commit every lockfile.
- **`.mise.toml` not trusted on a fresh clone.** mise refuses untrusted config and silently skips it. Run `mise trust` (or set `MISE_TRUSTED_CONFIG_PATHS`) in onboarding/CI.
- **Pinning the tool but using system libs.** A "same node version" build still differs if it links a different openssl. If that bites you, go hermetic (Nix/devbox), not just a version manager.

## Verify

1. **Pin file is exact:** `grep -E '[0-9]+\.[0-9]+\.[0-9]+' .mise.toml .tool-versions package.json` shows full triples — no bare majors, no `latest`/`lts`/`*`.
2. **Single source of truth:** the version in the pin file, `package.json` `engines`/`packageManager`, and the CI workflow all match — no hardcoded version in YAML that diverges from the file.
3. **Clean machine A:** fresh clone → `mise install && corepack enable` → `node -v`, `python -V`, `pnpm -v` print the pinned versions with zero manual selection.
4. **Clean machine B (or container):** repeat step 3 on a second OS/host → identical version strings.
5. **CI parity:** the CI job logs the same `node -v`/`pnpm -v` as the two machines (read the pin file via `setup-*` `version-file` or `mise-action`).
6. **Frozen install holds the line:** bump a dep without updating the lock → `npm ci` / `pnpm install --frozen-lockfile` **fails** (drift is rejected, not silently resolved).
7. **Auto-switch works:** `cd` out of the repo and back → the active `node`/`python` flips to the pinned versions with no manual command.
8. **engine-strict bites:** temporarily set a wrong node in the pin file → install **errors** on the mismatch instead of warning.

Done = two clean machines and CI all print identical tool + package-manager versions resolved from one committed pin file, the frozen install fails on any lockfile drift, and switching is automatic on `cd`.
