---
name: bootstrap-monorepo
description: Autonomous polyglot monorepo bootstrap meta-prompt on the moon + proto + Bun stack (Nx-convergent). TRIGGERS - new monorepo, new repository, polyglot setup, scaffold repo, moon proto bootstrap, monorepo from scratch.
allowed-tools: Read
disable-model-invocation: false
---

# Bootstrap Polyglot Monorepo (moon + proto + Bun, Nx-convergent)

Canonical reference lives in THIS skill:

→ **See**: [references/bootstrap-monorepo.md](references/bootstrap-monorepo.md)
→ **Cross-language boundaries**: [references/cross-language-interop.md](references/cross-language-interop.md) — boundary decision ladder + verified tool status (research-verified 2026-06)

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Starting ANY new repository — single-language or polyglot (the structure scales down)
- Setting up a moon-orchestrated, proto-pinned, Bun/TypeScript-wired monorepo
- Wiring engines (Rust/Python/Go) behind contracts under a TS control plane
- You want the repo Nx-convergent from day one (later `nx init` is mechanical, not a restructure)

## Stack

| Tool           | Responsibility                                                                     |
| -------------- | ---------------------------------------------------------------------------------- |
| **proto**      | Toolchain versions (bun, python, rust, node, …) pinned in repo-local `.prototools` |
| **moon**       | Project graph + task orchestration + caching + affected detection (`moon ci`)      |
| **Bun**        | TS runtime for every script, CLI, glue tool, and test; root workspaces             |
| **uv / cargo** | Python / Rust engines invoked natively from moon `script:` tasks                   |
| **TypeScript** | Type-safe control plane (7.0.2+); see **TypeScript Configuration** below           |

TypeScript is the control plane; other languages are engines behind language-neutral contracts (JSON Schema 2020-12 / proto) with drift gates and parity tests.

## TypeScript Configuration

This skill scaffolds **`tsconfig.base.json`** as the canonical reference implementation for all new repositories. Boilerplate path: `[templates/tsconfig.base.json](templates/tsconfig.base.json)` — the single source of truth for TS7 config shape.

Each new monorepo receives a root `tsconfig.base.json` with:

- `moduleResolution: bundler`, `target: ESNext`, `strict: true`, `noEmit`, `skipLibCheck`
- `allowImportingTsExtensions`, `lib: ["ESNext"]`, `verbatimModuleSyntax`, `noUncheckedIndexedAccess`, `noImplicitOverride`, `exactOptionalPropertyTypes`
- **`types` is deliberately omitted from the base** — TS7 defaults it to `[]` (stopping resolution of `@types/*`, `process`, JSX globals). Every package declares its own via `"types": ["bun"]` or `["node"]` etc. — bare name only, never `@types/bun` or `bun-types`.

Package-level `tsconfig.json` files extend the base and add their own `types` array + any legitimate package-specific overrides.

**Reference**: `~/.claude/typescript-latest-CLAUDE.md` (applies estate-wide). Package.json declares `"typescript": "latest"` (TS7.0.2+).

For TS 7 migration details and per-repo adoption: consult the bootstrapped skill docstrings and the upstream reference.

## Language-Selection Default (greenfield tiebreaker)

Choose _which language owns the code_ before choosing how to cross between them. This is a **tiebreaker, not a mandate** — a SOTA-native ecosystem and existing repo convention override it.

- **TypeScript by default** for the control plane: app logic, orchestration, CLIs, APIs, config, validation, agent/workflow automation, and anything future agents must refactor. (TS is structurally typed by default — the most agent-navigable surface.)
- **An engine language only where its ecosystem is SOTA-native**: Python for ML/data/science/quant or Python-only libraries; Rust/Go for hot kernels and systems work (Go > Rust as the tiebreaker).
- **Never let an engine language leak across the repo.** A Python-only library does NOT make the project Python — wrap it behind ONE typed boundary (ladder below) and keep TS as the public interface. Validate at the boundary: TS types are compile-time only and Python hints are not runtime-enforced.

## Crossing a Language Boundary (decision ladder)

When work must cross languages, climb from cheapest to most coupled — **stop at the first rung that satisfies the need** (full doctrine + verified tool status: [references/cross-language-interop.md](references/cross-language-interop.md)):

1. **Process boundary** — CLI + JSON/NDJSON on stdio (moon `script:` task). Default.
2. **Schema-typed RPC** — protobuf + buf / ConnectRPC, when a long-lived service or stream exists.
3. **Data-plane** — Apache Arrow IPC/Flight/ADBC, the moment two languages exchange _tables_.
4. **In-process FFI** — PyO3/maturin, napi-rs, Bun FFI, when call frequency makes 1–3 too slow.
5. **One WASM component core** — WIT + Component Model, ONLY if the kernel needs no threads (WASI threading still unshipped as of mid-2026).

Pattern B gate amendment: after the 8-float-op test selects Pattern B, ask "does the kernel need threads?" → if yes, native core (cdylib/PyO3), not WASM.

**TypeScript ↔ Python** (the most common pair) verified picks, June 2026: rung 1 = `Bun.spawn`/`child_process` running Python via `uv run --python 3.14` (NOT `bun:ffi` — C-ABI only); rung 2 = FastAPI + `@hey-api/openapi-ts` (HTTP) or `buf`-generated `protobuf-es` + `protocolbuffers/python` stubs (RPC); schema SSoT = Pydantic v2 → JSON Schema 2020-12 → TS, with a CI drift gate. Full table in the reference.

## Quick Commands

```bash
# After bootstrap:
moon ci                          # affected quality pipeline
moon run <project>:check         # one project's full gate (lint+test+drift)
moon query projects              # machine-readable project graph (agents read this)
moon query tasks                 # machine-readable task surface
proto use                        # install all .prototools pins on a fresh machine
```

## Legacy Path

Pre-2026-06 repos on **Pants + mise**: the old reference remains at
[../mise-tasks/references/bootstrap-monorepo.md](../mise-tasks/references/bootstrap-monorepo.md).
Migrate per-repo (parity-first, cut tasks over one at a time), never big-bang.

## Releases (local-first)

Two cases (full recipes in [references/bootstrap-monorepo.md](references/bootstrap-monorepo.md) Phase 9):

- **One releasable unit** → stock `semantic-release`, one `.releaserc.yml`, tag `v${version}`.
- **Multiple independently-versioned projects** (the monorepo standard) → per-project **namespaced tags**
  (`<project>/v${version}`) via **`@rimac-technology/semantic-release-monorepo`** (stock semantic-release ignores
  `commitPaths` — upstream #1279/#1212), selected by a `RELEASE_PROFILE`-keyed `.releaserc.cjs` dispatcher that
  derives each stream's `processCommits` from its `commitPaths`, plus a repo-wide umbrella on stock semantic-release.
  Install the fork with `npm i -D --ignore-scripts`. Reference impl: `claude-sys`.

## Related Skills

- `itp:semantic-release` - Release automation (local-first; Actions only for release/CodeQL/Dependabot/deploy)
- `itp:mise-tasks` / `itp:mise-configuration` - legacy mise-era orchestration (still valid for unmigrated repos)

---

## Troubleshooting

| Issue                                                | Cause                                                  | Solution                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- |
| `proto::detect::failed` for moon                     | tool installed but no version pinned                   | `proto pin --to global moon <version>` (or add to `.prototools`)          |
| `moon` not found over ssh                            | shims not on non-interactive PATH                      | export `PROTO_HOME` + shims PATH in `~/.zshenv` (NOT only `.zshrc`)       |
| Python tests "No module named pytest"                | `uv run` prunes dev extras                             | `uv run --extra dev -p <version> pytest <path>` from repo root            |
| PyO3 crate `cargo test` link errors (`_PyBool_Type`) | tests reference `#[pyfunction]` under extension-module | keep logic in pure-Rust core fns; tests call the core, wrapper stays thin |
| Task runs in wrong cwd                               | script assumes repo root                               | `options: { runFromWorkspaceRoot: true }` in the task                     |
| Guard task wrongly cached                            | moon caches by default                                 | `options: { cache: false }` on guards/parity/network tasks                |
| Commit "passed" but didn't land                      | a hook auto-fixed files and aborted                    | re-stage and retry; ALWAYS verify `git log --oneline -1` after commit     |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
