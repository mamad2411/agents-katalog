---
name: repo-tooling-architect
version: 1.6.0
description: Repo-root developer tooling — .editorconfig, .gitignore, version pinning (mise default, proto alt), task runner (Task default, just alt), CI (GitHub Actions default, act for local/free runs), minimal pre-commit, env vars via dotenv + external secret manager, Renovate, AGENTS.md / CLAUDE.md agent-instruction files. Use when scaffolding or auditing a repo's tooling layer, or naming/renaming Taskfile tasks.
---

# Repo Tooling Architecture

Productivity files that live at the repo root, are language-agnostic, and shape how every contributor and CI step interacts with the code. Pairs with every language and framework architect skill. See [STACK.md](STACK.md) for pinned tool versions.

## Decision model

Add a tool when **all three** are true:

1. **It pays back on day one.** Not "useful eventually" — useful from the first PR.
2. **The cost of installing it is smaller than the cost of going without it.** A 30-second install is fine; a 30-minute setup that breaks once per OS is not.
3. **There's no language-native option that already covers it.** `go test` doesn't need a Makefile wrapper. `uv run` doesn't need `task` for one-language projects.

When in doubt, skip. Tools you add later are easy; tools you remove are political.

## 1. `.editorconfig`

Always include. Universal editor support, zero ceremony, ends the indent-style wars before they start.

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{go,Makefile}]
indent_style = tab

[*.{yml,yaml,json}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false  # Markdown uses trailing spaces for hard breaks
```

## 2. `.gitignore`

Always include. Curate per language; never copy a 500-line GitHub default that contains entries for languages you don't use.

- **Use [github.com/github/gitignore](https://github.com/github/gitignore)** as the source for the base section per language.
- **Trim aggressively.** A clean `.gitignore` is documentation; a noisy one is noise.
- **Local-only exclusions** (`.idea/`, `.vscode/settings.json`) go in `.git/info/exclude` per-developer or `~/.gitignore_global`, not the repo's `.gitignore`.

## 3. Tool version pinning — mise (default), proto (alternative)

The problem: "works on my machine" because each dev has different Go / Python / Node versions. CI uses yet another version. Fix: pin every tool the repo needs in a file, install with one command.

### Default: `mise` with `mise.toml`

```toml
# mise.toml
[tools]
go = "1.27"
python = "3.14"
node = "22"
task = "3.51"
golangci-lint = "2.12"
buf = "1.69"
trivy = "0.70"
```

```bash
mise install                     # installs everything pinned
```

- **Why mise as default:** broadest tool coverage via asdf-legacy plugins, available through `winget`/`brew`/`scoop`.
- **Shell activation required:** `eval "$(mise activate bash)"` (or zsh/fish/pwsh equivalent).

### Alternative: `proto` with `.prototools`

Same key-value shape, file named `.prototools`, install with `proto install`. Pick proto when you want strict separation (proto manages only binary versions; `task` handles env + tasks) and no shell-activation step (PATH-shim based). Trade-off: smaller plugin ecosystem; obscure tools may need a custom WASM plugin.

**Either way:** the pinned-versions file is committed; CI installs the same versions; nobody runs "whatever's on their machine."

## 4. Task runner — Task (default) or just (alternative)

The problem: every project has 5–15 commands a contributor needs to know (`go build`, `go test --race`, `docker compose up -d db`, `task generate-contracts`, etc.). Without a runner, they live in stale README sections.

**Default: skip a task runner for single-language projects.** `go build`, `uv run`, `npm` are enough. Don't wrap them in `task build:` aliases — that's ceremony.

**Add a task runner when:** multi-language repo, multi-service compose stack, or a meaningful number of multi-step commands.

### Default: Task with `Taskfile.yml`

Sample `Taskfile.yml`: [RECIPES.md](RECIPES.md#4-sample-taskfileyml).

- **Why Task as default:** built-in `sources:` / `generates:` for incremental builds, `--watch` mode, first-class Windows support (ships its own POSIX-sh interpreter), built-in `dotenv:` loading.
- **Discoverability:** `task --list` shows every task with its `desc`.

**Naming: `module[:submodule…]:verb[:target|mode]`.** Name tasks after the thing they act on, then the action — `proto:generate`, `git:update:recursive`, `docker:up:dev` — not the reverse (`generate-proto`, `run-tests`). Environment and service are **targets after the verb** (`docker:up:dev`, not `docker:dev:up`). Cross-cutting actions use the inverse family, `verb:target` (`test:backend`, `scan:fs`). Reserve unprefixed names (`default`, `build`, `lint`) for repo-wide entry points that don't belong to a single module.

**The full grammar, the canonical verb/module vocabulary, the aggregate/atomic rule, include rules, and the standard Go-library task set are in [TASKFILE.md](TASKFILE.md).** Read it before adding or renaming a task — the audit of the active repos found the same drift (git submodule names, env ordering, `gen`/`generate`, `cover`/`coverage`, `be`/`fe`) everywhere, and TASKFILE.md is the single answer to it.

For a large enough module to warrant its own file, promote the prefix to a real namespace with `includes:` — Task auto-prefixes every task in the included file, so `docker:up` becomes `task docker:up` whether it's a flat key or defined in `Taskfile.docker.yml`:

Example: [RECIPES.md](RECIPES.md#4-includes-example).

Stay flat until a module earns its own file — see [TASKFILE.md](TASKFILE.md) §6.

### Alternative: just with `justfile`

Makefile-style brevity over YAML; recipes look like shell. Add `set windows-shell := [...]` and `set dotenv-load` at the top. Pick `just` when you prefer terseness, don't need incremental builds, and all collaborators are on macOS/Linux. Trade-off: no native incremental builds, no `--watch` mode.

**Settle on one per repo.** Don't mix `Taskfile.yml` and `justfile`.

## 5. Pre-commit hooks — minimal, opt-in

The problem: minor issues (trailing whitespace, committed secrets, large files) reach CI when they could have been blocked locally. Fix: a tiny pre-commit hook set that catches *only* what can't be caught later or that's genuinely fast.

**Strong opinions exist.** Some teams love pre-commit; some find it slows commits / blocks WIP commits. The minimal-hook stance is the compromise: catch real risks, never run language-specific linters or formatters in commit hooks (those run in editor-on-save and again in CI).

### `.pre-commit-config.yaml` — minimal set

Sample config: [RECIPES.md](RECIPES.md).

- **Install:** `pre-commit install` once per clone.
- **Run on demand:** `pre-commit run --all-files` (or wire into a Task: `task lint:precommit`).
- **No language-specific linters.** `ruff`, `golangci-lint`, etc. run in editor (on save) and again in CI. Running them in a pre-commit hook duplicates work and slows commits.
- **Skip on a single commit:** `git commit --no-verify` is fine; over-policing pre-commit erodes trust.

## 6. Environment variables

The problem: secrets and config diverge across machines, leak into git, or get exported globally and bleed across projects.

### Pattern

- **Non-secret config: `.env` + `.env.local`**, loaded by Task's `dotenv:` directive.
  - `.env` is committed (defaults safe for any contributor — `LOG_LEVEL=info`, `DB_HOST=localhost`).
  - `.env.local` is git-ignored (per-developer overrides — `LOG_LEVEL=debug`).
- **Real secrets: external secret manager.** Never in `.env`, never committed:
  - **1Password CLI** (`op run --env-file=.env.template -- task up`) — solo / small team
  - **doppler** (`doppler run -- task up`) — team
  - **Cloud secret manager** (AWS Secrets Manager, GCP Secret Manager) — production injection at runtime
- **No `direnv`** unless you need automatic activation when you `cd` into a directory. Task's `dotenv:` covers the common case without a second tool.

### `.env` shape

```
# .env — committed, safe defaults
LOG_LEVEL=info
APP_PORT=8080
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
```

```
# .env.local — git-ignored, per-developer overrides + dev secrets
LOG_LEVEL=debug
DB_PASSWORD=dev-only-not-a-real-secret
```

**`.gitignore` must include `.env.local`.** Audit any `.env*` pattern: only ignore variants that hold secrets; commit the safe ones.

## 7. Dependency updates — Renovate (default), Dependabot (acceptable)

The problem: dependency updates accumulate until they hit a security advisory or a breaking version, then a week of catch-up is needed. Automate it.

### Default: Renovate

`renovate.json` at the repo root:

Sample `renovate.json`: [RECIPES.md](RECIPES.md#7-renovatejson).

- **Why Renovate:** grouping rules, scheduled batches, broader ecosystem coverage (Go modules, Python, npm, Docker tags, GitHub Actions, Terraform).
- **Group minor + patch updates** into one weekly PR — review-bandwidth-friendly.
- **Security updates land immediately** — never queued.
- **Major bumps stay separate, labeled, never auto-merged** — they deserve a human read.

### Acceptable: Dependabot

For tiny single-language repos where Renovate's flexibility is overkill, GitHub's built-in Dependabot is fine. Same pattern (security immediate, minor grouped, major labeled).

## 8. CI — GitHub Actions (default), act for local/free runs

The problem: GitHub Actions minutes aren't free once the included allowance
is exceeded (or a payment/spending-limit issue blocks the account) —
Docker-heavy jobs (multi-platform builds, image scans) burn through them
fastest.

**Default: GitHub Actions**, workflow files under `.github/workflows/`,
triggered on `push`/`pull_request` as normal.

**When Actions billing becomes a blocker** (spending limit hit, no card on
file, or a deliberate "don't pay for CI" stance): run the *same* workflow
file locally via [`act`](https://github.com/nektos/act) instead of writing
a second pipeline. `act` reads `.github/workflows/*.yml` and runs each job
as a sibling Docker container, using a runner image
(`catthehacker/ubuntu:act-latest` covers most `ubuntu-latest` jobs) that
closely mirrors GitHub's actual runner — including Docker-in-Docker-style
builds, since that image ships the Docker CLI against the host daemon.

Config (`.actrc`, `.secrets.example`), the `ci:local` task and the act gotchas (artifact server, secrets, tag events, same-host registry push) are in [RECIPES.md](RECIPES.md#8-act-config-task-wiring-and-gotchas).
- **Trade-off, accept it deliberately:** no automatic gate on push anymore
  if triggers move to `workflow_dispatch`-only. Running the local task
  before pushing is on the developer, not enforced (a pre-push git hook
  can close this gap if it becomes a real problem in practice).
- **Don't reimplement the pipeline as shell scripts instead.** `act` runs
  the *actual* workflow file — no second definition to drift out of sync
  with the first.

## 9. Agent instructions — `AGENTS.md` (source), `CLAUDE.md` (thin)

Files that brief coding agents on the repo. Add them once the repo has commands or conventions an agent cannot infer from the code.

- **`AGENTS.md` is the single source.** Tool-neutral (Codex, OpenCode, Cursor, Claude Code via import). Lives at the repo root.
- **`CLAUDE.md` stays thin:** `@AGENTS.md` plus only Claude-specific lines (hooks, slash commands, memory notes). Never duplicate content between the two.
- **Nested `AGENTS.md`** in a subdirectory only when that package has its own commands or rules; the closest file wins.
- **Generated blocks** (e.g. skill imports from a tool like `rsk`) go in their own file or a delimited section, never hand-edited.

What belongs, in this order:

1. One-paragraph purpose of the repo.
2. **Commands** — build, test, lint, run, using the task runner names from section 4.
3. **Layout** — top-level directories and what each owns.
4. **Conventions that are non-obvious** — what a good engineer would still get wrong.
5. **Boundaries** — always / ask first / never (publishing, migrations, secrets, generated files).
6. **Pointers** to `docs/` (ADRs, backlog) instead of copying them; see `docs-architect` for the snippet.

What does not belong: anything derivable from the code or `git log`, tutorials, full API docs, secrets, private details of other projects.

Keep it short (aim under ~150 lines). Every line should prevent a mistake; when an instruction stops earning its place, delete it. Treat it as code: review changes, and fix it when an agent gets something wrong because of it.

## 10. When to skip the whole thing

This skill is opinionated about *adding* tools, but the strongest opinion is **don't add what you don't need.**

- **Single-language single-service project:** skip the task runner (use native tooling), keep `mise`/`proto` for version pinning if more than one dev exists.
- **Solo throwaway project:** `.editorconfig` and `.gitignore`. That's it.
- **Documentation-only repo:** `.editorconfig`, `.gitignore`, optional pre-commit for trailing whitespace.
- **Library / SDK with one entry point:** language-native tooling + Renovate. No Task, no mise needed.
- **Multi-language monorepo / multi-service compose stack:** the full stack — `.editorconfig`, `.gitignore`, `mise.toml` (or `.prototools`), `Taskfile.yml`, `pre-commit-config.yaml`, `renovate.json`, `docker-compose.yaml`, `AGENTS.md`.

Default to less. Add when the friction is real.
