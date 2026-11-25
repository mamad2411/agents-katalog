---
name: add
description: Save, list or remove the git repositories that git-parity tracks, optionally in named groups (one group per project). Use when the user wants to track a repository that was not detected automatically, asks which repositories are tracked, or agrees to save the groups a git-parity report suggested.
argument-hint: "[--group name] <repo-path ...> | --remove <repo-path ...> | --list"
allowed-tools: Bash(bash *git-parity.sh*)
---

# git-parity: add

git-parity finds repositories on its own: inside a repository it takes the ones beside it with the same remote owner; in a folder of projects it takes every repository up to two levels below. This skill saves that choice, or adds what detection cannot see (a repository somewhere else on disk).

Result of the request (the saved list is the only file this ever changes; repositories are never touched):

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/git-parity.sh" add $ARGUMENTS`

If no result appears above (only Claude Code runs that line), run it yourself: `bash <plugin-root>/scripts/git-parity.sh add <arguments>`, where `<plugin-root>` is two directories above this file. On Windows with repositories in WSL: `wsl.exe -d <distro> -- bash -c 'bash "$(wslpath -u <windows-path-with-forward-slashes>/scripts/git-parity.sh)" add <arguments>'`.

## What to do

1. If the user gave paths, the result above already shows what was added, skipped or already listed. Show the "Saved list" and say in one sentence what changed.
2. If no path was given, do not guess one. Run `bash <plugin-root>/scripts/git-parity.sh detect`, show the proposed groups, and ask the user which to save. Ask about every line under "Ask the user about".
3. When you decide on your own that a repository should be tracked (for example the user mentions a project outside the current folder), ask first, then run `add`. If the command fails, show it so the user can run it.
4. One group per project. Suggest a group name from the folder names; let the user rename it.

Other forms: `add --list` shows the saved list; `add --remove <path>` stops tracking a repository (it deletes nothing on disk). A copy of the previous list is kept as `repos.bak`.
