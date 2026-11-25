---
name: status
description: Read-only report of every tracked git repository - which branches are behind, ahead, diverged, dirty or never pushed, with next steps. Use when the user asks whether their repos or branches are in sync, up to date, or what is unpushed.
argument-hint: "[repo-path ...]"
allowed-tools: Bash(bash *git-parity.sh*)
---

# git-parity: status

Report (already generated, nothing was changed; only `git fetch` ran):

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/git-parity.sh" status $ARGUMENTS`

If no report appears above (only Claude Code runs that line), run the script once yourself and use its output: `bash <plugin-root>/scripts/git-parity.sh status <arguments the user gave>`, where `<plugin-root>` is two directories above this file.

On Windows the script needs a POSIX shell. When the repositories live in WSL, run this (the quoting is deliberate: write the script's Windows path with forward slashes, no backslashes and no inner quotes, because PowerShell strips the quotes and bash eats backslashes):

`wsl.exe -d <distro> -- bash -c 'bash "$(wslpath -u <windows-path-with-forward-slashes>/scripts/git-parity.sh)" status <arguments>'`

Examples of the path: `C:/Users/me/.codex/plugins/cache/git-parity/git-parity/<version>` or `//wsl.localhost/Ubuntu-24.04/home/me/project/.agents/plugins/git-parity`. Otherwise use Git Bash. Do not reimplement the script in PowerShell, and do not edit line endings: the file already uses LF.

If the output ends with a "Setup" section or a "Note:" about the current repository, no list (or not this repository) is saved yet. After the report, tell the user in one or two sentences which groups were detected, ask about anything listed under "Ask the user about", and ask once whether to save. On a yes, run the printed `add` command(s) exactly; if a command fails, show it so the user can run it. Do not ask again in this session after a no.

## What to do

1. Show the report to the user as is: keep the table, the "Clean" line and "Next steps". Translate labels and prose to the user's language; keep repo names, branch names, states and commands verbatim.
2. Add at most two sentences of summary on top. Do not re-explain rows.
3. Do not run any other command. This skill never changes anything.

States: DIVERGED (local and remote both have new commits), IN-PROGRESS (rebase/merge unfinished), STALE (fetch failed), DIRTY n (n uncommitted files), AHEAD n (not pushed), BEHIND n (can fast-forward), DETACHED, NO-UPSTREAM (never pushed), GONE (remote branch deleted, usually merged), BRANCHES (current branch fine, another branch needs attention), OK (clean, something was updated or noted).
