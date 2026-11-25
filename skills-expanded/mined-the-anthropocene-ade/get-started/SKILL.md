---
name: get-started
description: Use when the person asks to install, set up or try Atlas ADE (the ade command) in a project that has no ade.toml yet
---

# Get started with Atlas ADE

Atlas ADE is a small meta-harness: it runs the person's own Claude Code, Codex, OpenCode or Pi on their repo one card (a small task) at a time, and records what each card cost. Free, MIT, no account.

This skill only gets ADE into a project. It needs a shell there. With no shell, give the person the commands below to run themselves, and stop.

1. Run `ade --version`. If the command is missing, ask the person before installing anything, then run `uv tool install atlas-ade` (or `pipx install atlas-ade`).
2. If the project already has `ade.toml`, ADE is set up here: use the project's own `ade` skill and stop.
3. In a new, empty folder, run `ade init`.
4. In a repository the person already has, work on a clean checkout of the main branch. Run `ade init --dry-run` first and write nothing yet. Show the person every rule it says it would remove from `.claude/settings.json`, and ask which to keep. Once they have answered, run `ade init`. For each rule they keep, name the line to add under `[permissions.allow]` or `[permissions.deny]` in the `ade.toml` it wrote; that file is protected, so the person adds them, then run `ade init` again to put them back.
5. Read the `ade` skill that `ade init` installed (`.claude/skills/ade/SKILL.md`). Walk the person through the setup choices, one at a time: which model each role uses, which parts of the kit to keep, and the test command. From here on, that skill is the guide.

To see a full loop without spending any usage, offer `ade rehearse`.

When `ade` refuses a step, it prints the fix. Show the person that line, and do not work around it.

Install page, for the person: https://atlas-ade.dev/docs/install/
