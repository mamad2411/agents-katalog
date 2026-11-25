---
name: prek-migrate
description: >
  Migrate a repo from pre-commit to prek (the fast Rust Git hook manager).
  Use this skill whenever the user mentions prek, pre-commit to prek migration,
  prek.toml, converting .pre-commit-config.yaml to TOML, Rust builtin hooks,
  repo: builtin, prek util yaml-to-toml, prek update cooldown-days supply-chain
  hardening, or cleaning up legacy pre-commit artifacts (mise tasks, CI workflows,
  AGENTS.md docs, old shims) — even if they only say "speed up hooks" or "replace
  pre-commit" without naming prek explicitly.
license: MIT
---

# prek-migrate — pre-commit → prek

prek (https://github.com/j178/prek, docs https://prek.j178.dev/) is a Rust drop-in replacement for pre-commit: one binary, no Python runtime for prek itself, parallel setup, Rust-native builtin hooks. `repo: builtin` is prek-only — if the repo must keep running under stock pre-commit (users or CI still install it), stop and keep the YAML.

## Scope — minimal by default

| Scope | Trigger | Deliverable |
|---|---|---|
| **Minimal** (default) | any migration request | `prek.toml`, `prek install -f`, green validate/run, 3 commits |
| **Full sweep** | "remove all traces", "consolidate", "docs", "badge", "CI", "full migration" | minimal + `references/cleanup.md` |
| **Hardening** | "harden", "supply chain", "cooldown", "pin updates", "freeze" | minimal + `references/hardening.md` |

Never auto-adopt opt-ins; "migrate to prek" alone means minimal. Full sweep and hardening are independent: "full migration" means cleanup, not hardening.

## Rules

- **Convert, don't translate** — `prek util yaml-to-toml` writes the config; hand-edit only comments and preflight fixes.
- **Installed prek is truth** — builtins and flags come from `prek util list-builtins`, never a static list.
- **Three commits, never squash** — `chore(prek)` ×3, in order; commit only when validate + run are green.
- **Commit 1 is a no-op** — keep YAML unchanged; stage only `prek.toml` (YAML preflight edits stay unstaged).
- **One config after commit 2** — YAML dies in commit 2; no long-lived dual config.

## 1. Inventory — one read-only block

```bash
cat .pre-commit-config.yaml .pre-commit-config.yml prek.toml mise.toml .mise.toml 2>/dev/null
grep -rn "pre-commit" mise.toml .mise.toml pyproject.toml package.json tox.ini AGENTS.md README.md CONTRIBUTING.md docs/ .github/ 2>/dev/null
ls .github/workflows/ 2>/dev/null
prek --version && prek util list-builtins
```

Record every `repo` + `rev` + hook `id` + `args` / `files` / `exclude` / `types` / `stages`, every `default_*`, and every caller (mise tasks, CI, docs, package.json). Set `CONFIG` to whichever exists: `.pre-commit-config.yaml` or `.pre-commit-config.yml`.

## 2. Convert

Two kinds of preflight fixes — different files, different commits:

| Fix | Where | Why |
|---|---|---|
| Local YAML parse errors (invalid YAML, duplicate key in the local file) | YAML, before conversion | the converter can't read it; leave this edit unstaged |
| Deprecated stage aliases (`commit`→`pre-commit`, `push`→`pre-push`) and remote rev bumps (duplicate key in a remote hook manifest) | `prek.toml`, after conversion | keeps commit 1 a no-op for stock pre-commit users |

```bash
prek validate-config "$CONFIG"          # parse errors → fix YAML first
prek util yaml-to-toml "$CONFIG" -o prek.toml
# edit prek.toml: stage aliases, rev bumps, comments
prek validate-config prek.toml
prek run --all-files
```

`CONFIG` may be omitted from `yaml-to-toml`; it auto-discovers `.yaml`/`.yml`. Re-add comments the converter dropped. `prek.toml` now wins; on older prek pass `-c prek.toml` explicitly. Run `prek install -f` (honors `default_install_hook_types`; shims are not committed). Then commit 1 — see §4; stage only `prek.toml`. Details: `references/toml.md`.

## 3. Builtins

Baseline first, before touching `prek.toml`, so the remote pinned implementation runs:

```bash
PREK_NO_FAST_PATH=1 prek run <hook-id> --all-files   # before: remote impl
```

Run `prek util list-builtins` — ids + flags are ground truth. Move every hook whose id is listed and whose repo is `https://github.com/pre-commit/pre-commit-hooks` into one `[[repos]] repo = "builtin"` block, preserving `args`, `files`, `exclude`, `types`, `stages`. Drop `entry` (forbidden); `language` may stay only as `system`. Everything else stays as-is — remote (ruff, `mirrors-*`, shellcheck, conventional hooks) or local — except local `pygrep` one-liners, which map to `deny-pattern`/`require-pattern` (mapping 4).

```bash
prek run <hook-id> --all-files                       # after: builtin
prek validate-config prek.toml && prek run --all-files
git rm -f --ignore-unmatch .pre-commit-config.yaml .pre-commit-config.yml
prek cache gc
```

Mappings and edge cases: `references/builtins.md`. Then commit 2 — see §4.

## 4. Validate and commit

Verify `prek validate-config prek.toml`, `prek run --all-files`, and `prek list` before staging.

| # | `chore(prek)` commit | Contains | Gate |
|---|---|---|---|
| 1 | `convert pre-commit config to prek.toml` | `prek.toml` only (converter output + comments); YAML kept and unchanged | validate + green run |
| 2 | `switch eligible hooks to builtin and drop pre-commit config` | builtin block; YAML removed with `git rm -f --ignore-unmatch`; `prek cache gc` | validate + green run |
| 3 | `migrate settings to native format and add hardening` (drop `and add hardening` if not requested) | always `minimum_prek_version = "<installed prek>"`, replacing the legacy `minimum_pre_commit_version` when present; `[update]`/mise/docs/CI/badge deltas **only when requested** | validate + green run |

Stage only files that changed: commit 1 stages `prek.toml` only and leaves YAML preflight edits unstaged. Commit 3 is mandatory: it always lands the native `minimum_prek_version`, and carries opt-in hardening/cleanup. Never fold commit 3 work into 1–2, never commit red, never squash.

## References

- `references/builtins.md` (ground truth, mappings, caveats) · `references/toml.md` (converter, shape, gotchas) · `references/hardening.md` (opt-in `[update]` cooldown/freeze/tag filters) · `references/cleanup.md` (opt-in full sweep: mise, docs, badge, CI, shims)
- Upstream: https://prek.j178.dev/ · https://github.com/j178/prek · https://github.com/j178/prek-action
