---
name: verasic-github-cli-init
description: GitHub CLI auth for local AI agent harnesses — fine-grained PAT in gitignored .github-agent.local, direnv, gh verify. Use when setting up gh for agents, creating GH_TOKEN, wiring GitHub PR/issue/CI workflows per repo, or before any gh command when auth may be missing.
disable-model-invocation: true
---

Security: see `references/scanner-notes.md` and upstream [SECURITY.md](https://github.com/Milkywayrules/verasic-skills/blob/main/SECURITY.md) for expected scanner signals and trust model.

# Verasic GitHub CLI Init — Local Agent Harness Auth

## Workflows

All paths below assume the Cursor install root; installed elsewhere (e.g. `.agents/skills/`), adjust the prefix — the scripts themselves are install-root-agnostic. `/verasic-init` runs the bootstrap for you.

## Orchestration (Cursor)

Wire GitHub CLI auth for the local AI agent harness on this repo.

Read `.cursor/skills/verasic-github-cli-init/references/setup-protocol.md` (or `.agents/skills/verasic-github-cli-init/references/setup-protocol.md` for cursor-hybrid installs), then run from the repository root:

```bash
bash .cursor/skills/verasic-github-cli-init/scripts/bootstrap.sh
```

After bootstrap, tell the user clearly:

1. Create a fine-grained PAT scoped to this repo (link: https://github.com/settings/tokens?type=beta) — recommended permissions are in the setup protocol.
2. Copy `.github-agent.local.example` → `.github-agent.local`, set `GH_TOKEN`, run `chmod 600 .github-agent.local` (never commit).
3. Run `direnv allow` if they use direnv.
4. Verify with `bash .cursor/skills/verasic-github-cli-init/scripts/check-gh.sh`.

Do not run `gh auth login` device-flow loops. Do not print or commit token values. Do not run bare `gh auth status` in chat — use `check-gh.sh`.

**Bootstrap path — wire a repo once:**

1. Read `references/setup-protocol.md` (in this skill's directory) for secrets tiers and PAT permissions.
2. From the repo root: `bash .cursor/skills/verasic-github-cli-init/scripts/bootstrap.sh` (or `/verasic-github-cli-init` in Cursor, or let `/verasic-init` do it).
3. User creates `.github-agent.local` with `GH_TOKEN` (never commit).
4. Verify: `bash .cursor/skills/verasic-github-cli-init/scripts/check-gh.sh`

**Runtime path — before any `gh` command:**

1. If `GH_TOKEN` is unset, load credentials without executing env files:

```bash
source .cursor/skills/verasic-github-cli-init/scripts/load-gh-env.sh
```

2. Use `gh` with `-R "${GH_REPO}"` when auto-detection fails.
3. Never log or commit tokens. Do not run bare `gh auth status` in agent logs — use `check-gh.sh`.

## Source of truth

The full spec lives in `references/setup-protocol.md`. The Cursor rule is a thin digest; never duplicate the spec elsewhere.

## Hard rules

- Local agents → `.github-agent.local`; CI → GitHub Actions; production → secrets manager — never mix tiers.
- One fine-grained PAT per repo, scoped to that repo only.
- Never use `gh auth login` device-flow polling loops for harness setup — use `GH_TOKEN`.
