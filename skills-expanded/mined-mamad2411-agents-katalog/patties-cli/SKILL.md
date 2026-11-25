---
name: patties-cli
description: Use when running, building, deploying, or managing secrets for a Patties app. Covers `patties dev`, `patties build`, `patties start`, `patties deploy`, and `patties secret`. Trigger phrases include "start the dev server", "build the app", "deploy", "set a secret", "run patties".
---

# patties CLI

`patties` is the project's CLI. It's installed via the `patties` dependency
and exposed through `package.json#scripts` (`bun dev`, `bun run build`,
`bun start`). Reach for these commands directly instead of inventing
ad-hoc Bun invocations.

## Commands

### `patties dev` — start the dev server

```sh
bunx patties dev # the canonical invocation (bun dev runs the same thing via the package.json script)
patties dev --port 4000
patties dev --host 0.0.0.0
```

Starts the dev server with HMR over WebSocket. Reads `patties.config.ts`
for `target`, `port`, env, and secrets. Islands are bundled and hydrated
in dev — the same code path users see in production, minus minification.

### `patties build` — produce a production bundle

```sh
bun run build    # equivalent to `patties build`
patties build --target bun
patties build --target edge --out-dir dist
patties build --compile           # bun target only; single-binary
```

Outputs to `.patties/` by default. The server entry is at
`.patties/server/server-entry.js`. Build also regenerates the agent
manifest section (default `CLAUDE.md`; configurable via
`config.agentsMd.path`).

### `patties start` — run the production bundle

```sh
bun start        # equivalent to `patties start`
```

Runs the last `patties build` output. If no build exists, prints an
error directing you to `patties build` first.

### `patties deploy` — build then dispatch to a deploy plugin

```sh
patties deploy                    # build + dispatch
patties deploy --skip-build       # reuse the existing `.patties/`
```

Requires a deploy plugin declared in `patties.config.ts#plugins`. If no
plugin is installed, prints the command to run the server bundle
manually.

### `patties secret` — manage dev-time secrets

Dev-only. In production, secrets come from the host's secrets surface
(env vars, Cloudflare bindings, Vercel env, etc.) — not from this CLI.

```sh
patties secret set DATABASE_URL   # prompts for value
patties secret set DATABASE_URL "postgres://..."
patties secret get DATABASE_URL
patties secret list
patties secret rm DATABASE_URL
patties secret doctor             # checks OS keychain access
```

Values live in the OS keychain (macOS Keychain, GNOME Keyring, Windows
Credential Manager). They are loaded into `Bun.env` automatically when
the dev server reads `config.secrets`.

## Global flags

- `--cwd <path>` — project root (default `process.cwd()`)
- `--config <path>` — explicit config file (default: discovery in cwd)
- `--verbose` — verbose diagnostics, includes stack traces
- `--version` / `-v` — print version
- `--help` / `-h` — show help

## Common workflows

**First-run sanity check after scaffolding:**
```sh
bun install
bunx patties dev # opens http://localhost:3000 — SSR + island hydration
```

**Verify the production bundle:**
```sh
bun run build
bun start
```

**Iterate on a deploy config:**
```sh
patties build --target edge
patties deploy --skip-build
```

## What this skill does NOT cover

- Authoring framework primitives (routes, islands, agents, tools, jobs).
  See the project's `CLAUDE.md` and `.claude/rules/*.md` for those.
- Bun-the-runtime invocations (`bun add`, `bun upgrade`, `bun pm`).
  Those are upstream Bun commands; check `bun --help` directly.
