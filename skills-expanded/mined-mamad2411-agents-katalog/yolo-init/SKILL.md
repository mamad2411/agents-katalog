---
name: yolo-init
description: Use when setting up YOLO in a project for the first time, or repairing the setup. Scaffolds workspace/config.yaml and the features/, decisions/, and debug/ dirs (plus docs/ for the docs engine), and installs the CLAUDE.md routing block. Triggers on "set up YOLO here", "init yolo", "yolo init".
---

# yolo-init

Make a repo YOLO-ready. Idempotent — safe to re-run (repair mode).

**Resolve template sources via the plugin root.** When YOLO is installed as a plugin
(`${CLAUDE_PLUGIN_ROOT}` is set), read `.claude/yolo/templates/*` from
`${CLAUDE_PLUGIN_ROOT}/.claude/yolo/templates/*`; when the framework was copied into the project, read
them project-relative (see `conventions.md` *Where YOLO's files live*). Either way, `yolo-init` writes
**only project state** — `workspace/`, `workspace/config.yaml`, and the `CLAUDE.md` routing block. In
plugin mode do **not** copy the framework (skills/conventions) into the project; it stays in the plugin
and resolves via `${CLAUDE_PLUGIN_ROOT}`.

## Procedure
1. Create `workspace/`, `workspace/features/`, `workspace/decisions/`, `workspace/debug/` if missing (each tracked; add a `.gitkeep` where empty). Ensure `docs/` exists too — the single doc folder the docs engine indexes and where persisted intake lives; yolo keeps **no** `workspace/intake/` shelf.
2. If `workspace/config.yaml` is missing, copy `.claude/yolo/templates/config.yaml` to it; set `project.name` to the repo directory name and `project.base_branch` via the detection rule in `.claude/yolo/conventions.md` (`git symbolic-ref --short refs/remotes/origin/HEAD` minus `origin/`, else first existing of `main`/`master`). If it exists, repair only: fill missing keys, never overwrite a user-set value.
3. Install the routing block: ensure the project `CLAUDE.md` contains the content of `.claude/yolo/templates/claude-routing-block.md`. If the `<!-- YOLO:routing-block start -->`/`end` markers already exist, replace the block between them; otherwise append it. (Idempotent.)
4. Commit (`yolo: init`).

## Constraints
- Never git-ignore `workspace/` — it is the durable spine and must survive branches/worktrees.
- Repair mode preserves existing config values; it only fills gaps.
