---
name: prs
description: List the user's open pull requests (or GitLab merge requests) across all tracked repositories with CI, review and conflict state, plus the ones waiting for their review. Use when the user asks about their open PRs, what is blocking them, or what they need to review.
argument-hint: "[group|repo-path ...]"
allowed-tools: Bash(bash *git-parity.sh*)
---

# git-parity: prs

Report (already generated, nothing was changed):

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/git-parity.sh" prs $ARGUMENTS`

If no report appears above (only Claude Code runs that line), run the script once yourself and use its output: `bash <plugin-root>/scripts/git-parity.sh prs <arguments the user gave>`, where `<plugin-root>` is two directories above this file.

On Windows the script needs a POSIX shell. When the repositories live in WSL, run this (the quoting is deliberate: write the script's Windows path with forward slashes, no backslashes and no inner quotes, because PowerShell strips the quotes and bash eats backslashes):

`wsl.exe -d <distro> -- bash -c 'bash "$(wslpath -u <windows-path-with-forward-slashes>/scripts/git-parity.sh)" prs <arguments>'`

Examples of the path: `C:/Users/me/.codex/plugins/cache/git-parity/git-parity/<version>` or `//wsl.localhost/Ubuntu-24.04/home/me/project/.agents/plugins/git-parity`. Otherwise use Git Bash. Do not reimplement the script in PowerShell, and do not edit line endings: the file already uses LF.

If the output ends with a "Setup" section or a "Note:" about the current repository, no list (or not this repository) is saved yet. After the report, tell the user in one or two sentences which groups were detected, ask about anything listed under "Ask the user about", and ask once whether to save. On a yes, run the printed `add` command(s) exactly; if a command fails, show it so the user can run it. Do not ask again in this session after a no.

## What to do

1. Show the report as is: both lists, "Skipped" and "Next steps". Translate prose to the user's language; keep repo names, numbers, branch names and titles verbatim.
2. Open with one sentence: how many are open, how many need action, how many wait for the user's review.
3. Do not merge, close, approve or comment on anything. If the user asks for one of those afterwards, that is a new, explicit request.

Rows are ordered by urgency: failing checks, conflicts or requested changes first; approved and ready to merge next. `#12` is a GitHub pull request, `!12` a GitLab merge request. "Skipped" lists repositories whose host CLI (`gh` or `glab`) is missing or whose remote is neither.
