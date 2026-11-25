---
name: ost-phuryn-pm-skills-install
description: 'Install and update PM Skills Marketplace for Claude Code, Codex CLI, Claude Cowork, or skills-only clients. Primary path: run the support-package install script. Fallback: follow repo_readme_summary.md Part 2. Scope includes setup, update, copy-mode install, and verification; excludes slash-command conversion and workflow tutorials.'
argument-hint: '--client=codex|claude-code|cowork|gemini|opencode|cursor|kiro [--plugins=all|pm-toolkit,pm-execution] [--location=local|global] [--repo-dir=PATH] [--verify-only]'
---

# PM Skills Marketplace Install

> **Installation scope**: mode D. Local skills-only clients are CWD-sensitive; the AI Agent must pass `TARGET_DIR` last (or `--project-dir`) so the wrapper can enter it in a sub-shell. `--client=claude-code` defaults to user scope like the official command; with an explicit `--location=local` it enters `TARGET_DIR` in a sub-shell and installs with `--scope project`, writing that project's `.claude/settings.json`. Codex, default Claude Code, and `--global` paths do not take a project directory.

> Reference: [`repo_readme_summary.md`](../../repo_readme_summary.md)  
> Script: [`scripts_for_install/install.sh`](../../scripts_for_install/install.sh)  
> Official repository: [phuryn/pm-skills](https://github.com/phuryn/pm-skills)

## When to Use

Use this skill when the user wants to install, update, copy, or verify PM Skills Marketplace from `phuryn/pm-skills` for:

- Claude Code plugin usage.
- Codex CLI plugin usage.
- Claude Cowork GUI usage.
- Skills-only clients: Gemini CLI, OpenCode, Cursor, or Kiro.

The PM Skills Marketplace contains nine plugins. Claude Code and Claude Cowork can use Claude slash commands and skills. Codex CLI installs the same plugin files and can use the skills, but Claude slash commands do not become Codex slash commands. Skills-only clients receive copied skill folders only.

## Pre-read

1. [`../../repo_readme_summary.md`](../../repo_readme_summary.md) - install and update behavior.
2. [`../../scripts_for_install/install.sh`](../../scripts_for_install/install.sh) - supported clients, flags, platform limits, and verification.

## Pre-checks

Confirm the target from context. Use the defaults only when the user has not specified a preference.

| Information | Default | Notes |
|-------------|---------|-------|
| Client | `codex` | Supported values: `codex`, `claude-code`, `cowork`, `gemini`, `opencode`, `cursor`, `kiro`. |
| Plugins | `all` | Or a comma-separated subset from the nine PM plugins. |
| Skills-only location | `local` | Applies only to `gemini`, `opencode`, `cursor`, and `kiro`. |
| Existing repo checkout | none | Optional `--repo-dir=PATH`; without it the script clones `phuryn/pm-skills` for copy clients. |
| Verification only | no | Use `--verify-only` when the user only wants to inspect current state. |

Before running any command that modifies local CLI, plugin, or assistant configuration, show the exact command and get user confirmation. This includes plugin marketplace add/update/install commands and skills-only copy commands that write into project or user skills directories.

## Procedure

### Primary Path: Run the Install Script

Use this path on macOS, Linux, and WSL. From the support-package root, which is two directories above this `SKILL.md`, run:

```sh
sh scripts_for_install/install.sh [flags] [TARGET_DIR]
```

Common examples:

```sh
sh scripts_for_install/install.sh --client=codex
sh scripts_for_install/install.sh --client=claude-code --plugins=pm-toolkit,pm-execution
sh scripts_for_install/install.sh --client=claude-code --location=local --plugins=pm-execution /path/to/project
sh scripts_for_install/install.sh --client=cowork
sh scripts_for_install/install.sh --client=opencode --location=local --repo-dir=/path/to/pm-skills /path/to/project
sh scripts_for_install/install.sh --client=gemini --location=global --repo-dir=/path/to/pm-skills
sh scripts_for_install/install.sh --client=codex --verify-only
```

Supported script flags:

| Flag | Purpose |
|------|---------|
| `--client=codex` | Install or verify through Codex CLI plugin commands. |
| `--client=claude-code` | Install or update through Claude Code plugin commands; user scope unless `--location=local` is given. |
| `--client=cowork` | Print Claude Cowork GUI install steps. |
| `--client=gemini` | Copy skills to Gemini CLI skills directory. |
| `--client=opencode` | Copy skills to OpenCode skills directory. |
| `--client=cursor` | Copy skills to Cursor skills directory. |
| `--client=kiro` | Copy skills to Kiro skills directory. |
| `--plugins=all` | Install or copy all nine PM plugins. |
| `--plugins=a,b,c` | Install or copy selected PM plugin names. |
| `--location=local` | Project-level skills directory for skills-only clients. |
| `--location=global` | User-level skills directory for skills-only clients. |
| `--repo-dir=PATH` | Use an existing `phuryn/pm-skills` checkout for skills-only copy mode. |
| `--verify-only` | Skip install/copy and run verification checks only. |

The valid plugin names are:

```text
pm-toolkit
pm-product-strategy
pm-product-discovery
pm-market-research
pm-data-analytics
pm-marketing-growth
pm-go-to-market
pm-execution
pm-ai-shipping
```

For Claude Code, the script adds or refreshes the `pm-skills` marketplace, installs missing plugins, and updates existing plugins when detected. For Codex CLI, the script adds or upgrades the marketplace snapshot and installs missing plugins. For skills-only clients, the script copies skill folders into the selected local or global target directory.

### Fallback Path: Use repo_readme_summary.md

Switch to the fallback path when:

- The platform is native Windows outside WSL.
- The script fails because required commands such as `claude`, `codex`, or `git` are unavailable.
- The user wants manual control over each command.
- Claude Cowork must be installed through the GUI.
- A skills-only client needs a target directory or copy behavior not covered by the script.

Follow [`../../repo_readme_summary.md`](../../repo_readme_summary.md) Part 2, "Installation and update", step by step. Present each command that writes local CLI or assistant configuration and wait for user confirmation before running it.

### Verification

Use the script verification mode when possible:

```sh
sh scripts_for_install/install.sh --client=codex --verify-only
sh scripts_for_install/install.sh --client=claude-code --verify-only
sh scripts_for_install/install.sh --client=opencode --location=local --verify-only /path/to/project
```

Manual verification commands from the summary:

```sh
claude plugin list
claude plugin list --json --available
codex plugin list
codex plugin list --marketplace pm-skills
codex plugin list --available --json
```

For skills-only clients, verify that the target skills directory contains one or more copied `SKILL.md` files.

## After Installation

Tell the user:

```text
PM Skills Marketplace is installed or copied for the selected client. In Claude Code or Claude Cowork, use the installed PM slash commands and skills. In Codex, invoke the workflows by natural language because Claude slash commands are installed as files but are not Codex slash commands. In Gemini, OpenCode, Cursor, or Kiro, only copied skills are expected to work.
```

## Troubleshooting

| Symptom | Cause | Handling |
|---------|-------|----------|
| `unsupported platform` | The script supports macOS, Linux, and WSL only. | Use the fallback path in `repo_readme_summary.md` Part 2, or use Claude Cowork GUI setup on Windows. |
| `required command not found: claude` | Claude Code CLI is not installed or not on `PATH`. | Install or expose Claude Code CLI before rerunning `--client=claude-code`, or use another supported client. |
| `required command not found: codex` | Codex CLI is not installed or not on `PATH`. | Install or expose Codex CLI before rerunning `--client=codex`, or use another supported client. |
| `required command not found: git` | Skills-only copy mode needs `git` when `--repo-dir` is not supplied. | Provide `--repo-dir=/path/to/pm-skills` or install `git`. |
| Plugin commands installed but unavailable in Codex | Claude slash commands do not run as Codex slash commands. | Use natural language to invoke equivalent PM workflows, or ask separately to convert command files into Codex skills. |
| No skills found for skills-only client | The selected target directory does not contain copied `SKILL.md` files. | Rerun the script with the intended `--client`, `--location`, and optional `--repo-dir`; then verify again. |
