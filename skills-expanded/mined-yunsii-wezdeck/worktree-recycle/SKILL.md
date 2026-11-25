---
name: worktree-recycle
description: >
  Fast reset of a primary checkout or linked dev-* workstation onto
  origin/HEAD: soft preflight, then worktree-task recycle (fetch + dirty
  check + hard-reset + remote sync). Skips delivery gate and project init
  by default. Use when the user says 重置开发分支 / 重置工作站 / recycle
  this worktree / 收尾换下一轮, optionally with a next-task brief.
---

# Worktree recycle (platform skill — single source)

**Who runs:** the coding agent, **not** the human.  
**Never** tell the user to copy-paste `worktree-task recycle` as the primary path — load this skill and run the co-located runner.

Hard git ops stay in **`worktree-task recycle`** (dirty check, optional delivered gate, allowlisted clean, branch align to slug, `reset --hard origin/HEAD`, sync `origin/<branch>`).  
This skill owns soft preflight and readiness hints. **Project bootstrap is not part of recycle** — the next task initializes what it needs.

## When to load / run

| User intent (examples) | You do |
| --- | --- |
| 重置开发分支 / 重置工作站 / recycle / 收尾换下一轮 | `preflight` (optional glance) → `recycle -y` |
| 重置并开始做 X / recycle with task X | same, pass `--task "X"` |
| 只要看看能不能重置 | `preflight` or `recycle --dry-run` only |
| 主 worktree / primary / master 对齐最新主分支 | same recycle path on the primary checkout |
| **wezdeck standing close-out:** worktree round delivered onto `origin/HEAD` / 「合入主分支后收尾」 | same recycle path — **default**, not optional |

**Skip / redirect:**

- Short-lived `task-*` / `hotfix-*` end-of-life → **`worktree-task reclaim`** / `Ctrl+k g r` (not this skill)
- Pure `git reset` without this skill → do not bypass; still use the runner

**wezdeck policy:** worktrees = **isolation**; delivery = **direct mainline** (no PR).  
**Invariant:** idle `dev/*` tip **must equal** `origin/HEAD`. After landing on mainline (or when mainline moved while the workstation sat idle), **immediately** recycle — do not leave `dev/*` behind. See `docs/workspaces.md` → Maintenance loop.

## Resolve TOOL_HOME (first hit wins)

```text
1. $WORKTREE_RECYCLE_HOME
2. directory of this SKILL.md if run.sh is co-located
3. $HOME/.agents/skills/worktree-recycle
4. $WEZDECK_ROOT/skills/worktree-recycle
5. $HOME/github/wezterm-config/skills/worktree-recycle
```

```bash
TOOL_HOME=…   # dir that contains run.sh
R="$TOOL_HOME/run.sh"
```

Install / refresh discovery (idempotent, from wezdeck):

```bash
./scripts/dev/link-platform-skills.sh
```

## Who runs what

| Layer | Duty |
| --- | --- |
| **Skill + `run.sh`** | Soft preflight, orchestrate recycle; init only with `--with-init` |
| **`worktree-task recycle`** | Fetch, dirty gate, branch align, hard-reset, remote sync |
| **Agent (you)** | After git is clean, start the next task; bootstrap the stack only if that task needs it |
| **Human** | Intent; confirm only when preflight shows **real** blockers (wrong lifecycle slug, dirty outside allowlist) |

## Agent procedure

1. **Resolve** TOOL_HOME; confirm `"$R"` is executable. Cwd may be a linked `dev-*` worktree **or** the primary checkout (or pass `--cwd`).
2. **Preflight** (optional glance; recycle also runs it):
   ```bash
   "$R" preflight --cwd "$PWD"
   ```
   Soft signals only. `task-*` / `hotfix-*` are real blockers (use reclaim). Dirty trees need `--force` or a clean tree.
3. If the user already named the next task, keep it for `--task`.
4. **When the user already said 重置 / recycle:** do **not** re-ask about squash / push / init. Proceed:
   ```bash
   "$R" recycle --cwd "$PWD" -y [--task "…"] [--fresh-agent] [--dry-run]
   ```
   Prefer `-y` when the user explicitly asked to reset. Do **not** invent a “先 push / 手动 reset / 先 bootstrap” fork.
   Pass **`--fresh-agent`** when the user wants a blank next round (收尾换下一轮 / 重置并开始做 X / “别接着旧会话”). That flag **unpins typed resume and cold-respawns** the worktree’s agent pane (same end state as manual `Ctrl+Shift+n`). Expect the current agent pane to die after the tool returns — do not plan follow-up turns in the same conversation.
5. **Do not run init** unless the user asked or you pass `--with-init`. Leave deps/codegen/services to the follow-up task.
6. **Report** briefly: new HEAD, branch (after slug align), remote sync result, fresh-agent outcome (respawned / skipped / failed hint).

## Preflight covers (skill layer)

| Check | Hard / soft | Notes |
| --- | --- | --- |
| Primary **or** linked `dev-*` | hard | `task-*` / `hotfix-*` → reclaim |
| Dirty outside recycle allowlist | hard (CLI) | Fix or explicit `--force` from user |
| Delivery / content-absorbed | **off by default** | Opt in with `--require-delivered` |
| `.ticket/` leftovers | soft | Allowlisted clean on linked trees |
| Next-task text from user | passthrough | Becomes `--task` (stdout/log only; no worktree file) |

## Desired end state

After a successful recycle:

- Local tip == `origin/HEAD` (default branch tip)
- Branch name matches the worktree slug mapping (`dev-agent` → `dev/agent`); primary uses the default branch (`master` / `main`)
- `origin/<same branch>` tip == that same commit (unless `--no-sync-remote`)
- Upstream is `origin/<branch>` (linked never tracks the default branch)
- Project bootstrap **not** required by recycle itself

## Fast path defaults

| Behavior | Default | Opt-in / opt-out |
| --- | --- | --- |
| Delivery gate | skip | `--require-delivered` / `WT_RECYCLE_REQUIRE_DELIVERED=1` |
| Branch align to slug | on | `--keep-branch-name` / `WT_RECYCLE_KEEP_BRANCH_NAME=1` |
| Remote sync | on | `--no-sync-remote` / `WT_RECYCLE_SYNC_REMOTE=0` |
| Project init | skip | `--with-init` or `run.sh init` |

## Don't

- Don't ask the human to run CLI as the main path
- Don't re-ask squash / push / manual-reset questions after the user already said 重置开发分支
- Don't use recycle for short-lived `task-*` / `hotfix-*` (use reclaim)
- Don't `--force` away dirty trees without an explicit user override
- Don't treat attention / ledger / ticket `shipped` as proof of merge
- Don't run `sync-runtime` or package installs just because recycle finished
- Don't auto-bootstrap the project inside the skill runner
- Don't delete Claude transcripts; use `--fresh-agent` (unpin + cold respawn) when a blank session is wanted — do not ask the human to press `Ctrl+Shift+n`
- Don't maintain a second SKILL.md body outside this directory (link only)

## Related

- Runner: `run.sh`, `lib/preflight.sh`, `lib/init.sh` (opt-in)
- Hard ops: `scripts/runtime/worktree/worktree-task recycle`
- Docs: `docs/workspaces.md` (Recycle), `docs/daily-workflow.md` (closing a round)
- Link: `scripts/dev/link-platform-skills.sh`
- Offline: `"$TOOL_HOME/test.sh"`
