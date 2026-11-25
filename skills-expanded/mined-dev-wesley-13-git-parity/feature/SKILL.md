---
name: feature
description: Show where the branches of one feature stand across all tracked repositories - commits ahead of the base, pushed or not, pull request state, and merge order for stacked branches. Use when the user asks about the state of a feature that spans several repos.
argument-hint: "<branch-name-or-pattern> [group|repo-path ...]"
allowed-tools: Bash(bash *git-parity.sh*)
---

# git-parity: feature

Report (already generated, nothing was changed; only `git fetch` ran):

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/git-parity.sh" feature $ARGUMENTS`

If no report appears above (only Claude Code runs that line), run the script once yourself and use its output: `bash <plugin-root>/scripts/git-parity.sh feature <arguments the user gave>`, where `<plugin-root>` is two directories above this file. If the report says a pattern is needed, ask the user for the feature's branch name or a part of it.

On Windows the script needs a POSIX shell. When the repositories live in WSL, run this (the quoting is deliberate: write the script's Windows path with forward slashes, no backslashes and no inner quotes, because PowerShell strips the quotes and bash eats backslashes):

`wsl.exe -d <distro> -- bash -c 'bash "$(wslpath -u <windows-path-with-forward-slashes>/scripts/git-parity.sh)" feature <arguments>'`

Examples of the path: `C:/Users/me/.codex/plugins/cache/git-parity/git-parity/<version>` or `//wsl.localhost/Ubuntu-24.04/home/me/project/.agents/plugins/git-parity`. Otherwise use Git Bash. Do not reimplement the script in PowerShell, and do not edit line endings: the file already uses LF.

If the output ends with a "Setup" section or a "Note:" about the current repository, no list (or not this repository) is saved yet. After the report, tell the user in one or two sentences which groups were detected, ask about anything listed under "Ask the user about", and ask once whether to save. On a yes, run the printed `add` command(s) exactly; if a command fails, show it so the user can run it. Do not ask again in this session after a no.

## What to do

1. Show the table as is, translating prose to the user's language; keep repo names, branch names and commands verbatim.
2. Open with one or two sentences: how many branches in how many repos, and what blocks the feature from being merged (unpushed work, missing pull requests, stacked order).
3. Keep "Next steps". Rows are already in merge order inside each repository; if the feature needs a cross-repository order (for example backend before frontend), say that this is the user's call and suggest one only if the branch names make it obvious.
4. Do not run any other command. This skill never changes anything.

Columns: "vs base" is commits ahead / behind the base branch ("merged" = nothing left to merge). "Remote" is pushed, N unpushed, never pushed, behind remote, or remote only. "PR" is the pull request number and state, "none", or "-" when the branch is not on the remote or `gh` is not installed.
