---
name: mise
description: Use when working with mise — installing/activating it, or writing mise.toml tool versions, [env] vars, and [tasks].
---

# mise

Docs: https://mise.jdx.dev — fetch the relevant page when you need detail beyond this file.

## Install & activate

```bash
curl https://mise.run | sh          # or: brew/apt/dnf/pacman/scoop install mise
eval "$(mise activate zsh)"         # bash|zsh|fish|pwsh — add to shell rc
```

Homebrew and some package managers activate automatically. `mise doctor` diagnoses setup.

## Commands

```bash
mise use node@22          # add to ./mise.toml and install
mise use -g node@22       # add to ~/.config/mise/config.toml
mise install              # install everything in config
mise exec python@3 -- python   # one-off, no config change
mise ls / mise ls-remote node  # installed / available versions
mise run <task> / mise tasks   # run / list tasks
mise trust                # required before mise runs a new config's code
```

## mise.toml

```toml
[tools]
node = "22.11.0"            # pin exact for reproducibility
python = { file = ".python-version" }
"github:owner/repo" = "latest"   # explicit backend

[env]
NODE_ENV = "development"
_.file = ".env"             # load gitignored secrets

[tasks.build]
description = "Build the bundle"
depends = ["clean"]         # depends entries run in parallel
sources = ["src/**/*"]      # sources+outputs enable caching
outputs = ["dist/**/*"]
run = "npm run build"
```

Namespace related tasks (`db:migrate`, `test:unit`). `run` as an array runs steps sequentially.

## Backends

Prefer in order: **core** (bare `node`, `python`, `go`) > **aqua** (`aqua:owner/repo`, verifies signatures) > **github** (`github:owner/repo`) > language-native (`npm:`, `pipx:`, `cargo:`, `go:`, `gem:`) > `asdf:` (runs arbitrary plugin code).

`ubi:` is deprecated — replace with `github:`.

## Gotchas

- aqua verification failures: `mise self-update` first, then disable only the failing method (`MISE_AQUA_GITHUB_ATTESTATIONS=0`, `MISE_AQUA_COSIGN=0`, `MISE_AQUA_SLSA=0`) — not all of them. Some releases genuinely lack attestations; try another version or the `github:` backend.
- Never commit secrets to mise.toml; use `_.file = ".env"`.
- Windows: add `run_windows` overrides for shell-specific commands.
