---
name: environment-doctor
description: Checks the health of a Claude Code dev environment (git, Node.js, VS Code + extensions, Docker, claude-mem, other installed plugins) and suggests exact fix commands.
when_to_use: Use when the user types "check my setup", "is my install broken", "setup isn't working", or asks why claude/docker/git isn't working.
allowed-tools:
  - Bash(git --version)
  - Bash(node --version)
  - Bash(npm --version)
  - Bash(bun --version)
  - Bash(code --version)
  - Bash(code --list-extensions)
  - Bash(docker --version)
  - Bash(docker info)
  - Bash(claude --version)
  - Bash(claude plugin list)
  - Bash(claude plugin marketplace list)
  - Bash(test -d ~/.claude-mem)
---

Every check below is read-only and pre-approved in `allowed-tools`, so run them
without stopping to ask. Never assume a result — always run the real command.

## 1. Run these checks (via the Bash tool, one at a time)

- `git --version`
- `node --version` (needs ≥ 18, ≥ 20 recommended since claude-mem requires Node ≥ 20)
- `bun --version` (claude-mem's hooks and worker daemon run on Bun — without it claude-mem installs but silently does nothing)
- `code --version`
- `docker --version` and `docker info` (confirms the engine is actually running, not just installed)
- `claude --version`
- `test -d ~/.claude-mem` (indicates claude-mem is installed)
- `claude plugin list` to see which plugins are installed, and `claude plugin marketplace list` to see which marketplaces are registered
- `code --list-extensions` and check for the recommended set: `anthropic.claude-code`, `ms-azuretools.vscode-docker`

Summarize the results as a ✅/❌ table before suggesting any fixes.

## 2. Fix commands by OS (ask which OS if unknown)

**Windows (PowerShell, via winget):**
- Missing Git → `winget install --id Git.Git -e`
- Missing Node → `winget install --id OpenJS.NodeJS.LTS -e`
- Missing Bun → `irm https://bun.sh/install.ps1 | iex` (installs to `%USERPROFILE%\.bun\bin` and only updates the persisted PATH — a terminal that was already open still won't see it)
- Missing VS Code → `winget install --id Microsoft.VisualStudioCode -e`
- Missing Docker → `winget install --id Docker.DockerDesktop -e`, then note it needs a restart + first manual launch (and `wsl --install` first if WSL2 isn't set up yet)
- Missing Claude Code CLI → `irm https://claude.ai/install.ps1 | iex`

**macOS (via Homebrew):**
- Missing Git/Node/Bun → `brew install git` / `brew install node` / `brew install bun`
- Missing VS Code → `brew install --cask visual-studio-code`
- Missing Docker → `brew install --cask docker`, then note it needs to be opened manually once
- Missing Claude Code CLI → `curl -fsSL https://claude.ai/install.sh | bash`

**Both OSes:**
- Claude Code CLI installed but not found in the terminal → almost always a PATH-not-refreshed issue; tell the user to close and reopen their terminal first
- claude-mem not installed → recommend `npx claude-mem install` (the officially recommended method — it auto-detects Claude Code, no need for the manual `/plugin marketplace add` flow). It does **not** install Bun for you: check Bun first, or claude-mem installs cleanly and then does nothing, logging "Bun runtime not found" from its worker.
- Missing VS Code extension → suggest `code --install-extension <id> --force`

## 3. Plugin problems specifically

A plugin that "installed fine" but does nothing is nearly always one of these two:

- **Installed into the wrong scope.** `--scope project` writes `.claude/settings.json` into the folder it was run from, so the plugin only loads inside that folder. If they ran the bootstrap script from a downloads folder, that's the bug. Check `claude plugin list`, then reinstall with `--scope user` to make it available everywhere.
- **The marketplace was never added.** `claude plugin install <name>@<marketplace>` can only resolve `@<marketplace>` if that marketplace is registered. Check `claude plugin marketplace list` first. For plugins from this repo: `claude plugin marketplace add ./` (run from the repo root — the folder holding `.claude-plugin/marketplace.json`; a bare `.` is rejected as "Invalid marketplace source format"), then `claude plugin install devenv-doctor --scope user`.

Note: the CLI command is `claude plugin install` (singular "plugin"); a common typo is `claude plugins install` (plural), which fails.

## 4. Always close with

One summary line: "You're ready ✅" or, if not fully passing, how many checks remain and the right order to fix them in (runtimes first, then VS Code extensions, then Docker last since it's the slowest / may need a restart).

Don't teach git/Docker theory in this skill — stay focused on "what's broken, how to fix it," not concepts.
