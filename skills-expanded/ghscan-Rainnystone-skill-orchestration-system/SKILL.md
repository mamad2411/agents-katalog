---
name: sos
description: "Use when helping a user inspect, organize, plan, apply, activate, back up, or restore SOS-managed agent skill packs on Codex or Claude Code without assuming global installation."
---
# SOS Skill Orchestration

Use this skill for workflows around Skill Orchestration System (SOS) on Codex or Claude Code: inspecting active skills, proposing packs, creating reviewable plans, applying approved plans, activating packs, checking status, and restoring backups.

Default stance:
- Start in no-global-install mode.
- Use `scripts/sos_doctor.py` to detect whether SOS can run and which hosts are visible.
- Resolve the host (`--host codex` or `--host claude`) before any write command.
- Prefer read-only or dry-run commands before any write.
- Keep deterministic writes in the SOS CLI.
- Do not edit Codex config, Claude `.sos-archive/`, SOS vaults, manifests, registry files, backups, or generated pointer skills by hand.

Progressive disclosure:
1. Read `references/execution-modes.md` when local capability is uncertain.
2. Read `references/workflows.md` for the specific operation the user requested.
3. Read `references/safety-model.md` before any write, restore, cleanup, sync apply, or source deletion.
4. Read `references/codex.md` for Codex-specific config or skill-root behavior.
5. Read `references/claude-code.md` for Claude-specific archive and skill-root behavior.

Do not load every reference up front. Do not paste the full CLI reference unless the user asks for command details or the selected workflow needs exact commands.

Keep `README.md` and `README_CN.md` aligned when user-facing install, usage, or workflow entry points change.
