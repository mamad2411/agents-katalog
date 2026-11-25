---
name: install
description: Install the harness-kit pipeline into the current project. Copies agents, slash commands, skills, and hooks into the project's .claude/, plus AGENTS.md and CLAUDE.md at the repo root. Run after adding the harness-kit plugin from the marketplace.
user_invocable: true
---

Install harness-kit into the user's project. Plugin ships full harness; this skill lays it down via bundled installer.

## What it writes

Installer copies into the **target project** (`${CLAUDE_PROJECT_DIR}`):

- `.claude/agents/`, product-manager + staff-software-engineer (sensors, evals, guides, skills)
- `.claude/commands/`, `/product-manager:*`, `/sse:*`, `/pipeline:*`, `/context:*`
- `.claude/runtime/`, per-agent hooks + scripts (outputs/ stay target-side state)
- `.claude/hooks/` + `.claude/scripts/`, pipeline tracking, token accounting, opt-in pipeline status bar
- `.claude/shared/`, cross-agent guides
- `.claude/conventions/`, scaffold for project overrides
- `.claude/settings.json`, wires hooks (existing one backed up first). No statusLine: user keeps own global one. Pipeline bar only with `HK_STATUSLINE=1`
- `AGENTS.md` at repo root; `CLAUDE.md` if absent

This modifies files in the user's repo. Tell user what runs before running. Existing `.claude/settings.json` backed up to `.claude/settings.json.bak.<stamp>`.

## Run

Requires `git` + `python3` (installer checks, exits if missing).

```bash
bash "${CLAUDE_PLUGIN_ROOT}/setup/install.sh" "${CLAUDE_PROJECT_DIR}"
```

Relay installer output verbatim. On `missing agents` / `git not found` / `python3 not found`, surface exact line.

## Eval judge

Installer runs non-interactive here, so it defaults judge to `local` on first install (reinstall keeps existing `.claude/hk-config.json`). First install only: ask user (AskUserQuestion) which eval judge:

- **local (default)**: fresh Claude evaluator scores rubrics. No extra cost. Nothing to do.
- **jev**: Jev by TypeSafe AI scores weighted rubrics. Different model family (reduces self-preference bias), typed scores. Paid API, needs key from https://console.typesafe.ai/keys.

On `jev`: follow `.claude/commands/hk/eval.md` `jev` section in target project (env var name or key via stdin, never echoed). Mention switch later with `/hk:eval jev | local`.

## Graph engineering

First install only: ask (AskUserQuestion) graph mode, default **off**:
- **off**: plain pipeline, nothing extra.
- **manifest**: REQ ids, `trace/{feature_id}.yml`, scope gate that blocks out-of-scope files, link status PROPOSED/VALIDATED/STALE. No infra, no key.
- **full**: manifest + embedded FalkorDB graph: Graphiti (free NVIDIA build key) + Joern CPG. Python 3.12+.

Apply with `.claude/commands/hk/graph.md` in target project.

## After

Tell user: **restart Claude Code** to load agents, commands, hooks. Then:

- `/golden-path`, the golden path: idea → merged PR in one command
- `/product-manager:prd | :prp | :run`
- `/sse:plan | :dev | :test | :pr | :run | :sdd`
- `/pipeline:continue | :reset`
- `/context:pack | :graph` (optional, need repomix / graphify)
- `/hk:eval jev | local` (eval judge, default local)
- `/hk:graph off | manifest | full` (graph engineering, default off)

Update later: `/plugin update harness-kit` then `/harness-kit:update`.
