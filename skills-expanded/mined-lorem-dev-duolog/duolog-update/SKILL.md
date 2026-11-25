---
name: duolog-update
description: >-
  Use when the person asks to update duolog on this computer or in the
  current project.
metadata:
  duolog-version: "1.11.1"
---

# Update duolog

Run every command yourself, in this order. Leave every permission prompt to
the person. Stop at the first command that fails and show its error.
Check each part of an installer pipeline for failure too.

1. Run `duolog version` and say the current version.
2. Run the installer again for this OS, with `DUOLOG_VERSION` set to
   `latest`, so that a version pinned earlier does not hold it back. On
   macOS, Linux or WSL:

   ```sh
   curl -fsSL https://github.com/lorem-dev/duolog/releases/latest/download/install.sh | DUOLOG_VERSION=latest sh
   ```

   In Windows PowerShell:

   ```powershell
   $env:DUOLOG_VERSION = 'latest'; irm https://github.com/lorem-dev/duolog/releases/latest/download/install.ps1 | iex
   ```

   Run `duolog version` again. If it did not change, say this was
   already the newest release and go on.
3. Run `codex plugin marketplace list`. If no marketplace is named
   `duolog`, run `codex plugin marketplace add lorem-dev/duolog`, then
   `codex plugin add duolog@duolog`.
   If `duolog` is already listed, update it and the plugin instead:

   ```sh
   codex plugin marketplace upgrade duolog
   codex plugin add duolog@duolog
   ```

4. If this project has `.duolog/config.yaml`, run
   `duolog install --scope project`.
   Do not install into a project that does not have duolog yet. Instead,
   say that `duolog install --scope project` sets up a project when wanted.
   Read the user hook files: `~/.claude/settings.json` and
   `~/.codex/hooks.json`. Use `settings.json` under `CLAUDE_CONFIG_DIR`
   and `hooks.json` under `CODEX_HOME` when those variables are set.
   If either file has duolog hook entries, also run
   `duolog install --scope user`. Missing files mean no hooks there;
   user skills alone do not mean an all-projects install.
5. Read what each install printed. If it changed a Codex hook, tell the
   person to approve the hooks again in `/hooks` in Codex.
   Codex skips a changed hook until then. Never write trust or approvals.
6. Run `duolog doctor` and report what it asks the person to do.
7. Tell the person to start new Claude Code and Codex sessions.
   Running sessions keep the old hooks and skills.
