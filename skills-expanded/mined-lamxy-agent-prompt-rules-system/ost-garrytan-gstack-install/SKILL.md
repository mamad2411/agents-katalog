---
name: ost-garrytan-gstack-install
description: 'Help users install or update gstack. Primary path: run the support package install script; fallback to repo_readme_summary.md when the script is unavailable or manual control is needed. Scope: install, update, host selection, optional team mode, and verification guidance; excludes uninstall and detailed usage tutorials.'
argument-hint: '[--host=claude|codex|opencode|factory|kiro|auto] [--team=none|required|optional] [--install-dir=DIR]'
---

# gstack Install (skill_for_setup)

> **Installation scope**: global setup plus a CWD-sensitive project team mode. The AI Agent passes `TARGET_DIR` only with `--team=required|optional`; the wrapper enters that directory in a sub-shell before team initialization.

> Reference: [`repo_readme_summary.md`](../../repo_readme_summary.md)  
> Script: [`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> Upstream repository: [garrytan/gstack](https://github.com/garrytan/gstack)

## When to Use

Use this skill when the user wants to install, update, configure, or verify gstack for Claude Code or another supported AI agent host.

This skill is for setup only. It does not provide a full gstack tutorial and does not uninstall gstack.

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) - install methods, prerequisites, platform notes, and verification guidance.
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) - supported flags, host names, platform detection, and script behavior.
3. [`../../.ost-refs/`](../../.ost-refs/) if it exists - local package references.

## Pre-checks

Confirm these from conversation context or ask only when needed:

| Information | Default | Why it matters |
|---|---|---|
| Operating system | None | The script supports macOS, Linux, WSL, and Git Bash/MSYS on Windows 11. |
| Target host | `claude` | Controls whether the script runs `./setup` or `./setup --host HOST`. |
| Team mode | `none` | `required` or `optional` modifies the current project through `gstack-team-init`. |
| Install directory | `~/.local/share/gstack` (setup links `~/.claude/skills/gstack` to it; a legacy real checkout at `~/.claude/skills/gstack` stops the script, update it with `--install-dir=~/.claude/skills/gstack`) | Existing non-git paths cause the script to stop and ask for cleanup or a different directory. |

## Procedure

### Primary path: run the install script

Use this path on supported shell platforms: macOS, Linux, WSL, and Git Bash/MSYS on Windows 11.

From the support package root, run:

```sh
sh scripts_for_install/install.sh
```

Common examples:

```sh
sh scripts_for_install/install.sh
sh scripts_for_install/install.sh --host=codex
sh scripts_for_install/install.sh --host=auto --install-dir="$HOME/gstack"
sh scripts_for_install/install.sh --team=optional /path/to/project
sh scripts_for_install/install.sh --team=required /path/to/project
```

The script:

- checks for `git` and `bun`;
- also checks for `node` on WSL or Git Bash/MSYS because upstream browser fallback support needs it there;
- clones or updates `https://github.com/garrytan/gstack.git`;
- runs upstream `./setup` for Claude Code or `./setup --host HOST` for non-Claude hosts;
- optionally runs `bin/gstack-team-init required|optional`.

The wrapper accepts only `claude`, `codex`, `opencode`, `factory`, `kiro`, and
`auto`, matching upstream setup's actual install capability. Cursor and Slate
are rejected because upstream setup does not install them. OpenClaw, Hermes,
and GBrain require their separate artifact-generation or session workflow.

Git is non-interactive (`GIT_TERMINAL_PROMPT=0`) and uses a `120` second
default wall-clock limit when `timeout` or `gtimeout` is available. Set
`GSTACK_GIT_TIMEOUT_SECONDS` to a positive decimal integer to override it.
Exported proxy variables are passed through to Git and upstream `setup`; Docker
tests need those variables injected explicitly into the container.

### Fallback path: use repo_readme_summary.md

Use the fallback path when:

- the platform is not supported by the script;
- the user wants to execute commands manually;
- the script fails before reaching upstream setup;
- a Windows setup requires manual handling of Git Bash, WSL, Node.js, or copied files after `git pull`;
- the user needs OpenClaw-specific ClawHub installation rather than the host setup script.

Follow `repo_readme_summary.md` **Section 2: Installation and Updates**. Send commands to the user for confirmation before running them one by one.

### Verification

Upstream gstack does not publish a standalone `--version` or `doctor` command in the local summary. Use the smallest relevant confirmation:

```sh
cd ~/.claude/skills/gstack && ./setup
```

For browser capability build failures, use the upstream recovery/build confirmation:

```sh
cd ~/.claude/skills/gstack && bun install && bun run build
```

Then ask the user to restart the target agent and try an appropriate slash command:

```text
/office-hours
/review
/qa https://example.com
```

If Claude Code cannot see gstack skills, follow `repo_readme_summary.md` Section 2 and add the upstream `## gstack` guidance and slash-command list to `CLAUDE.md`.

## Tell the User After Install

```text
gstack is installed or updated. Restart the target agent or start a new session, then try /office-hours, /review, or /qa https://example.com. Updates can also be requested with /gstack-upgrade where supported.
```

## Troubleshooting

| Symptom | Likely cause | Handling |
|---|---|---|
| `missing required command: git` | Git is not on `PATH`. | Install Git, then rerun the script. |
| `missing required command: bun` | Bun v1.0+ is not on `PATH`. | Install Bun, then rerun the script. |
| `missing required command: node` on WSL or Git Bash/MSYS | Windows browser fallback support needs Node.js. | Install Node.js and ensure it is on `PATH`, then rerun the script. |
| Git clone or pull fails | The remote failed, or the configured wall-clock limit expired. | Read the operation, directory, timeout, and exit code in the error. Set `GSTACK_GIT_TIMEOUT_SECONDS` to a positive decimal integer if an override is needed. |
| `--host=cursor` or `--host=slate` | Upstream setup does not install this host. | Use a supported wrapper host or follow that client's own install flow. |
| `--host=openclaw`, `hermes`, or `gbrain` | These use a separate upstream artifact-generation or session workflow. | Follow upstream integration guidance instead of this wrapper. |
| Install directory exists but is not a git checkout | The target path contains unrelated files. | Move it aside or rerun with `--install-dir=DIR`. Do not delete user files automatically. |
| Skills are not visible after install | The agent session has not reloaded or project guidance is missing. | Restart the target agent. For Claude Code, add the upstream gstack section and slash-command list to `CLAUDE.md` if needed. |
| Windows without Developer Mode loses symlink behavior | Upstream setup copies files instead of symlinking. | After future `git pull` updates, rerun `cd ~/.claude/skills/gstack && ./setup`. |
| Browser commands fail after setup | Browser build/dependency state may be incomplete. | Run `cd ~/.claude/skills/gstack && bun install && bun run build`. |
| User asks to uninstall | Uninstall is outside setup scope. | Point to upstream README uninstall guidance or `~/.claude/skills/gstack/bin/gstack-uninstall`; do not run uninstall by default. |
