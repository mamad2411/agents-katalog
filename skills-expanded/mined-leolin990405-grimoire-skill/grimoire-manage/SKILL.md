---
name: grimoire-manage
description: >
  Companion to Grimoire — the OPT-IN layer that takes a produced skill pack,
  asks the user which global agents to configure, installs it across them,
  and then manages it (status / list / sync / uninstall / preflight gate).
  Use after grimoire.sh has produced & you have reviewed a skill pack and the
  user wants it usable in their other agents (Claude Code / Codex / Trae /
  opencode / copilot / qwen / deepseek / stepfun), or wants to re-sync after
  a Trae/stepfun/deepseek app update, check cross-agent parity, remove a
  skill everywhere, or add a confirm-before-running gate. This deliberately
  crosses Grimoire's default "scripts never install skills" boundary by
  explicit user request and records it in the pack manifest. Triggers:
  装 skill 到其它 agent / 把技能打通到所有 agent / 跨 agent 安装技能 /
  skill 没出现在某个 agent / 重新同步技能 / 卸载某个技能 / skill 确认门 /
  install skill across agents / cross-agent skill / sync skills after update /
  skill preflight gate / grimoire-manage.
allowed-tools: Bash
---

# Grimoire-Manage · 跨 agent 安装与管理

Grimoire produces a **candidate** skill pack and never installs it (red line).
`grimoire-manage` is the explicit, user-driven layer that installs and manages
it across agents. Two scripts (repo `scripts/`, mirrored here under `scripts/`):

- `skill-install.sh` — install a reviewed pack into chosen agents
- `skill-manage.sh`  — status / list / sync / uninstall / gate

## When to use

| Need | Command |
|---|---|
| Scan this machine: how many skill-capable agents exist | `skill-manage.sh scan` |
| Check the host has a source skill's config/tools (MinerU server/token, ffmpeg/yt-dlp, Kedou) | `skill-manage.sh doctor [--skill <name>]` |
| See agents + which exist (drive the user choice) | `skill-install.sh --pack <dir> --list` |
| Preview install (no changes) | `skill-install.sh --pack <dir> --agents <csv> --dry-run` |
| Install into chosen agents | `skill-install.sh --pack <dir> --agents <csv\|all>` |
| Cross-agent parity of a skill | `skill-manage.sh status --name <skill>` |
| Per-agent counts + agent-only skills | `skill-manage.sh list` |
| Re-sync after a Trae/stepfun/deepseek update | `skill-manage.sh sync --pack <dir>` |
| Remove a skill everywhere | `skill-manage.sh uninstall --name <skill>` |
| Add the confirm-before-running gate | `skill-manage.sh gate` |

## The flow (produce → choose → install → manage)

1. `grimoire.sh … --only skills --install` (or run grimoire normally) →
   review/promote candidates into `skills/skills/`.
2. **Inventory:** `skill-install.sh --pack <skills-dir> --list`.
3. **Ask the user** which agents to configure — in Claude Code use
   `AskUserQuestion`; otherwise ask in chat. Choose only `present = yes` rows.
   Never pick agents for the user.
4. **Dry-run, confirm, install:** `--dry-run` first, then the same command
   without it. Tell the user to restart each affected agent.
5. **Manage** later via `skill-manage.sh` (status/sync/uninstall/gate).

## Boundary

- Installing crosses the default candidate-only red line **by explicit user
  request**; `skill-install.sh` records this in the pack manifest's
  `red_line_note` / `installed_to`.
- Per-pack only: an agent's own non-shared skills (e.g. Codex `ppt-master`,
  Trae `web-dev`) are never enumerated, moved, or deleted; drifted same-named
  dirs are backed up, never clobbered.
- The Claude `settings.json` preflight hook is printed for **manual** install
  (the agent cannot self-edit startup config); `gate` injects only the
  portable instruction-file paragraph and never touches `settings*.json`.
- Verified agent topology and rules live in `scripts/lib/agent-targets.sh`.
