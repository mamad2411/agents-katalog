---
name: local
description: Find local work that is not on the remote yet across all tracked repositories and offer to push it and open a pull request, one confirmation per repository. Run only when the user explicitly asks to push or publish their local work.
argument-hint: "[repo-path ...]"
disable-model-invocation: true
allowed-tools: Bash(bash *git-parity.sh*)
---

# git-parity: local

Report (already generated, nothing was changed):

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/git-parity.sh" local $ARGUMENTS`

If no report appears above (only Claude Code runs that line), run the script once yourself and use its output: `bash <plugin-root>/scripts/git-parity.sh local <arguments the user gave>`, where `<plugin-root>` is two directories above this file.

On Windows the script needs a POSIX shell. When the repositories live in WSL, run this (the quoting is deliberate: write the script's Windows path with forward slashes, no backslashes and no inner quotes, because PowerShell strips the quotes and bash eats backslashes):

`wsl.exe -d <distro> -- bash -c 'bash "$(wslpath -u <windows-path-with-forward-slashes>/scripts/git-parity.sh)" local <arguments>'`

Examples of the path: `C:/Users/me/.codex/plugins/cache/git-parity/git-parity/<version>` or `//wsl.localhost/Ubuntu-24.04/home/me/project/.agents/plugins/git-parity`. Otherwise use Git Bash. Do not reimplement the script in PowerShell, and do not edit line endings: the file already uses LF.

If the output ends with a "Setup" section or a "Note:" about the current repository, no list (or not this repository) is saved yet. After the report, tell the user in one or two sentences which groups were detected, ask about anything listed under "Ask the user about", and ask once whether to save. On a yes, run the printed `add` command(s) exactly; if a command fails, show it so the user can run it. Do not ask again in this session after a no.

## What to do

1. Show the report as is. Translate prose to the user's language; keep names, states and commands verbatim.
2. If there is a "Push candidates" section, ask which ones to push. One decision per repository/branch; "all" is acceptable only if the user says so explicitly. When asking with a choice widget, every question needs at least two options: for a repository with a single candidate, offer "push" and "skip".
3. For each approved candidate, run exactly the command printed for it. Never add `--force`, `--force-with-lease` or `--no-verify`.
4. After a successful push of a non-base branch, offer a pull request. If the user agrees: `gh pr create --fill` in that repo for a GitHub remote, `glab mr create --fill` for a GitLab remote, when that CLI is installed; otherwise print the URL that `git push` showed. Ask for title/body changes before creating.
5. End with a short list: pushed, PR opened (with URL), skipped.

## Hard rules

- Nothing reaches the remote without a yes for that specific repo and branch.
- Never push a branch that is not listed under "Push candidates" (base branches and `never-push` entries are excluded on purpose).
- Never commit for the user. For DIRTY repos, show what is pending and let the user decide.
- DIVERGED branches are not pushed: explain and stop.
