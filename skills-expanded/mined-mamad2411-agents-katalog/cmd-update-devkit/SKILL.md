---
name: cmd-update-devkit
description: Command — Force a fresh load of devkit after pushing changes — refresh the bb-plugins marketplace and reinstall
---

# /update-devkit

Forces Claude Code to re-read devkit by refreshing its marketplace and reinstalling. Use after pushing changes to the devkit repo, or whenever you suspect CC has cached an older version.

The marketplace/uninstall/install steps are Claude Code meta-commands (slash commands typed in the chat) — they are NOT shell commands. Only the verification step shells out (`/help | grep`).

## Prerequisite

devkit installs from the **`bb-plugins`** marketplace, which sources `github.com/lettland/bb-plugins`. Your changes must already be **pushed to GitHub** (e.g. `git push origin master` from the dev clone) — the steps below fetch from the marketplace, not from any local working tree.

## Steps

1. **Refresh the marketplace** (CC slash command) so the latest pushed commit becomes available:
   ```
   /plugin marketplace update bb-plugins
   ```
2. **Uninstall** (CC slash command):
   ```
   /plugin uninstall devkit
   ```
3. **Reinstall from the marketplace** (CC slash command):
   ```
   /plugin install devkit@bb-plugins
   ```
4. **Verify** (this one is a shell command — `/help` here means CC's help output piped to grep):
   ```bash
   # Run inside Claude Code:
   /help | grep -i devkit
   ```
   You should see the devkit commands listed. If you don't, the install didn't take — re-run step 1 and confirm the marketplace name with `/plugin marketplace list`.

## Resolution policy

Installs from **`@bb-plugins`** (the GitHub marketplace for `lettland/bb-plugins`). Step 1 is what actually pulls new commits — without it, an uninstall/reinstall just restores the previously cached version. There is no `@local` marketplace in this setup.
