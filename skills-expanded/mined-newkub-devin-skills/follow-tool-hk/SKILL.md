---
name: follow-tool-hk
description: Set up and use hk for Git hooks instead of Lefthook/pre-commit
argument-hint: "[scope]"
related:
  - follow-tool-mise
  - run-verify
  - fix

---

## Goal

Set up hk as the Git hook manager replacing Lefthook, with a type-safe and fast Pkl config

## Scope

Use hk for pre-commit, pre-push, pre-merge-commit and the `check`/`fix` commands

- Boundary: if the repo already uses moonrepo → moon's `vcs.hooks` (v1.9+) is enough for general hooks (`moon run :lint --affected --status=staged`) — use hk when you want parallel staged-file linting, non-moon hook steps, or one hook config across repos

- General git hooks patterns: see `references/apis.md`
- Latest: `hk@2.2.0` (verified 2026-09-24) — v2 breaking: config is Pkl-only (removed `hk.toml`/`hk.yaml`/`.hkrc.pkl`), builtin variants (`gitleaks_staged`, `knip_strict`, `pinact_v3`) replaced by typed options such as `(Builtins.gitleaks) { scan = "staged" }`, `hk generate` → `hk init`, pre-commit fix+stage automatic — migration guide: `https://hk.jdx.dev/migration-v2`
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Install hk

> Goal: have the hk CLI ready

1. Recommended: install via mise — `mise use -g hk` or `mise use hk` in the project
2. Alternatives: `cargo install hk`, `brew install hk`, `mise use hk`
3. If the project has no mise, run `/follow-tool-mise` first
4. Confirm with `hk --version`

### 2. Install Git Hooks

> Goal: git calls hk automatically

1. Recommended per-repo install: `hk install` or `mise x -- hk install`
2. Global install alternative: `hk install --global` (requires Git 2.54+)
3. Confirm with `git config --get hook.hk-pre-commit.command`
4. If using mise, set `HK_MISE=1` in `mise.toml` or `mise = true` in `hk.pkl`

### 3. Create mise.toml

> Goal: manage the tools hk uses

1. Run `mise use bun gitleaks hk` to add the tools to the project
2. Define `HK_MISE = "1"` in `[env]`
3. Use versions that match `packageManager`, e.g. `bun = "1.4.2"`
4. Don't commit secrets or user-specific paths

### 4. Create hk.pkl

> Goal: configure hooks for the project

1. Run `hk init` to create a template `hk.pkl` (v2: `hk generate` was renamed to `hk init`)
2. Edit `hk.pkl` using `amends` and `import Builtins.pkl` per the latest version — v2 pins to `v2.2.0`/`hk@2.2.0`
3. Set `mise = true` if using mise tools
4. Define the main hooks: `pre-commit`, `pre-push`, `pre-merge-commit`, `check`, `fix` — or use the top-level `steps` map (v2) to create implicit `check`/`fix`/`pre-commit` at once
5. Use `hk.local.pkl` for local overrides without committing
6. v2: config is Pkl only — `hk.toml`/`hk.yaml`/`hk.json`/`.hkrc.pkl` are removed

### 5. Configure Steps

> Goal: define the linters/tests hk runs

1. Use `Builtins.<name>` for supported tools, e.g. `Builtins.gitleaks` — v2: no variant names (`gitleaks_staged`, `knip_strict`, `pinact_v3`); use typed options such as `(Builtins.gitleaks) { scan = "staged" }`, `(Builtins.knip) { strict = true }`, `(Builtins.pinact) { version = "3" }`
2. Create custom steps with `glob`, `exclude`, `check`, `fix`
3. Use `fix = true` in `pre-commit` to edit files automatically
4. Use `stash = "git"` in `pre-commit` to stash unstaged changes
5. For large working trees or Windows long paths, use `stash = "patch-file"` or `stash = "none"`
6. Use `stomp = true` for typecheck/test/scan steps that don't need a file lock
7. Use `batch = true` for tools that support batching
8. Use `effect = "destructive"` for steps that delete/overwrite files — hk forces confirm in agent/MCP contexts (v1.55+)
9. For monorepos, use `subprojects` in `hk.pkl` for nested configs + per-directory mise env (v1.52+)
10. Use `dir` with Tera templates, e.g. `dir = "{{workspace}}"` for workspace-aware steps instead of `cd {{workspace}} && ...` (v1.57+)
11. Use `check_diff` + `check_after_diff = true` for partial fixers (e.g. ShellCheck) — apply the fixed diff then re-run checks so unfixed findings still show (v1.57+)

### 6. Run and Validate

> Goal: verify the hooks work

1. Run `hk run pre-commit` to test
2. Run `hk run pre-push`
3. Run `hk run pre-merge-commit`
4. Run `hk check --all` for CI
5. Run `hk fix` to edit files
6. For agent use, run `hk agent` to print integration snippets (instructions, hooks, MCP) — read-only, touches no config
7. Run `/run-verify` to check lint/typecheck/scan after setup

### 7. Migrate from Lefthook

> Goal: move from lefthook to hk

Migrating from the `pre-commit` framework → use `hk migrate pre-commit --output hk.migrated.pkl` then `HK_FILE=./hk.migrated.pkl hk validate` (lefthook has no auto-migrate yet)

1. Remove `lefthook.yml` and `lefthook-local.yml` from the repo
2. Take `bunx lefthook install` out of `package.json` `prepare`
3. Change `prepare` to `mise x -- hk install`
4. Update lefthook references in `AGENTS.md` to `hk`
5. Delete the ast-grep rule `follow-lefthook.yml` in `rules/` if present

## Rules

### 1. Configuration Structure

- Use `hk.pkl` at the root or `.config/hk.pkl`
- Use `hk.local.pkl` for local overrides (not committed)
- Always use `amends` with the release package URL
- Use `import Builtins.pkl` to access builtin linters
- Use the latest version tag, e.g. `v2.2.0` — v2 no longer supports `hk.toml`/`hk.yaml`/`hk.json`/`.hkrc.pkl`

### 2. mise Integration

- Set `mise = true` in `hk.pkl` when tools come from mise
- Set `HK_MISE = "1"` in `mise.toml` `[env]`
- Use `mise x -- hk install` in `package.json` `prepare`
- List the tools in `mise.toml`, e.g. `bun`, `gitleaks`, `hk`

### 3. Hook Behavior

- `pre-commit` should set `fix = true`
- `pre-push` runs check-only (no fix)
- `pre-merge-commit` runs typecheck alone
- Use the correct hook names: `pre-commit`, `pre-push`, `pre-merge-commit`
- Never use `pre-merge` (not a valid Git hook name)
- Don't bypass hooks with `HK=0 git commit` without good reason

### 4. Step Standards

- Specify `glob` for linters that operate on files
- Use `exclude` as a `List(...)`
- Use `check` for read-only, `fix` for modify
- Use `stomp = true` for workspace-wide checks
- Use `batch = true` for tools that support it
- Use `depends` for ordering between steps
- Use `exclusive = true` for steps that must run alone
- hk v1.57+ embeds its own version's Pkl package — config pinned to the same version validates offline on a cold cache; disable with `HK_PKL_EMBEDDED=0`

### 5. Example mise.toml

```toml
[tools]
bun = "1.4.2"
gitleaks = "8.30.1"
hk = "2.2.0"

[env]
HK_MISE = "1"

[hooks]
postinstall = "hk install"
```

### 6. Example hk.pkl

```pkl
amends "package://github.com/jdx/hk/releases/download/v2.2.0/hk@2.2.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v2.2.0/hk@2.2.0#/Builtins.pkl"

mise = true

local linters = new Mapping<String, Step> {
  ["biome"] {
    glob = List("*.{ts,tsx,js,jsx,vue,json,jsonc,md}")
    exclude = List("/.agents/", "/.devin/")
    check = "bunx biome check --no-errors-on-unmatched {{files}}"
    fix = "bunx biome check --write --no-errors-on-unmatched {{files}}"
    batch = true
  }
  ["gitleaks"] {
    check = "gitleaks protect --no-banner --redact --config .gitleaks.toml --staged"
  }
}

local checks = new Mapping<String, Step> {
  ["scan"] {
    check = "bun run scan"
    stomp = true
  }
  ["typecheck"] {
    check = "bun run typecheck"
    stomp = true
  }
  ["test"] {
    check = "bun run test:run"
    stomp = true
  }
}

hooks {
  ["pre-commit"] {
    fix = true
    steps {
      ...linters
    }
  }
  ["pre-push"] {
    steps {
      ...checks
    }
  }
  ["pre-merge-commit"] {
    steps {
      ["typecheck"] = checks["typecheck"]
    }
  }
  ["check"] {
    steps {
      ...linters
      ...checks
    }
  }
  ["fix"] {
    fix = true
    steps {
      ...linters
    }
  }
}
```

### 7. Common Commands

- `hk run pre-commit` - test pre-commit
- `hk run pre-push` - test pre-push
- `hk check --all` - check the whole repo
- `hk check --unstaged` - check only unstaged/untracked files (v1.52+, suits agent stop hooks)
- `hk fix` - fix files
- `hk agent` - print agent integration snippets (Codex, Claude Code, VS Code) — read-only (v1.55+)
- `hk mcp` - run the MCP server with an interactive dashboard (v1.55+)
- `hk migrate pre-commit` - convert `.pre-commit-config.yaml` to `hk.pkl`
- `hk config dump` - show the effective config
- `hk builtins` - list builtin linters

- Use /follow-tool-mise to install and manage tools
- Use /run-verify to check lint/typecheck/scan after setup
- Use /fix when hooks find issues that need fixing
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- hk installed and working through mise
- `mise.toml` defines the tools and `HK_MISE=1`
- `hk.pkl` defines pre-commit, pre-push, pre-merge-commit
- `hk run` passes every hook
- `hk check --all` ready for CI
- Lefthook config removed or replaced
