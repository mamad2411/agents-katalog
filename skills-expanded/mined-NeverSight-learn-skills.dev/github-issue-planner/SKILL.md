---
name: github-issue-planner
description: Fetch open GitHub issues, use the local checkout as the implementation source of truth, and write decision-complete local Markdown plans. Use when the user asks to plan GitHub issue fixes, prepare an implementation backlog from GitHub issues, inspect open issues before coding, produce read-only issue-resolution plans, or explicitly asks to execute one planned issue through a branch, commit, PR, and post-merge follow-up.
---

# GitHub Issue Planner

Fetch open non-PR GitHub issues, inspect the local checkout, and write one resolution plan per issue. GitHub is read-only by default.

The branch, commit, PR, and post-merge issue-comment lifecycle is opt-in only. Use it only when the user explicitly asks to `execute`, `implement`, `open PR`, or `run issue lifecycle` for a single planned issue.

## Default Planning Workflow

1. **Resolve inputs**
   - Set `$skillDir` to this skill folder and use it for every bundled script path.
   - Use the current working directory as the codebase unless the user provides a local path.
   - Use the user's GitHub URL or `owner/repo` when provided.
   - If no GitHub target is provided, infer `owner/repo` from the local checkout's GitHub remote. Ask only when inference fails or multiple GitHub remotes conflict.
   - Do not clone or inspect GitHub repository files. GitHub provides issue metadata only.

2. **Preflight**
   - Use `.env` in the current directory or this skill folder, or an explicit `--env` path.
   - Validate token and optional config without exposing secrets:
     ```powershell
     $skillDir = 'C:\Users\Akshay Diwadkar\.agents\skills\github-issue-planner'
     python "$skillDir\scripts\check_github_env.py" --env .env --github-repo-url owner/repo
     ```
   - If preflight fails, report the missing or invalid configuration and stop.

3. **Fetch open issues**
   - Fetch all open non-PR issues and comments:
     ```powershell
     $skillDir = 'C:\Users\Akshay Diwadkar\.agents\skills\github-issue-planner'
     python "$skillDir\scripts\fetch_github_issues.py" --env .env --github-repo-url owner/repo --output .scratch/github-issue-plans/issues.json
     ```
   - Treat the JSON output as the only GitHub issue context. Do not write labels, comments, or state changes back to GitHub.

4. **Explore local code**
   - For each issue, inspect the local codebase, tests, docs, config, and nearby patterns relevant to the issue.
   - Cite local files and commands where they support implementation decisions.
   - Mark the issue `blocked` when required local code, credentials, generated artifacts, or external dependencies are unavailable.

5. **Plan with the rubric**
   - Read `references/planning-rubric.md` before writing the report.
   - Use the built-in rubric by default. Use `plan-with-senior-dev` only when the user explicitly asks for senior planning.
   - Mark an issue `needs-info` when the issue or local evidence lacks enough detail to plan safely.

6. **Quality-gate and report**
   - Write a Markdown report under `.scratch/github-issue-plans/<owner-repo>/<timestamp>.md`.
   - Quality-gate each issue section against `references/planning-rubric.md`.
   - A `ready-to-plan` issue must cite local evidence, implementation steps, relevant API/config/data impacts, tests, risks, and assumptions. Otherwise mark it `needs-info` or `blocked`.
   - End by summarizing the report path and top priorities in chat.

## Opt-In Execution Workflow

Use this workflow only when explicitly requested. It handles exactly one `ready-to-plan` issue per branch and PR.

1. **Select one issue**
   - Confirm exactly one issue number and its `ready-to-plan` section from the latest report.
   - Do not batch multiple issues into one execution PR.
   - If the issue is `needs-info` or `blocked`, stop and report the missing decision or blocker.

2. **Prepare the branch before editing**
   - Run `git status -sb` and inspect relevant diffs before creating a branch.
   - If the worktree contains unrelated changes, do not stage or overwrite them; ask which files belong to the issue.
   - Resolve the default branch from the remote, using `main` when the remote does not provide a clear answer.
   - Checkout and update the default branch, then create `codex/issue-<number>-<slug>` before making code changes.

3. **Implement and verify**
   - Use the issue plan as the implementation source of truth.
   - Keep changes limited to the selected issue.
   - Run the exact verification commands from the plan, plus any focused checks needed for touched code.

4. **Commit, push, and open PR**
   - Stage only files belonging to the selected issue.
   - Commit as `Fix issue #<number>: <short title>`.
   - Push the branch with upstream tracking.
   - Open a ready-for-review PR titled `[codex] Issue #<number>: <title>`.
   - The PR body must use `Refs #<number>`, not `Fixes #<number>`, and must include the validation run, assumptions, and this post-merge follow-up command:
     ```powershell
     $skillDir = 'C:\Users\Akshay Diwadkar\.agents\skills\github-issue-planner'
     python "$skillDir\scripts\post_merge_issue_followup.py" --env .env --github-repo-url owner/repo --issue-number <number> --pr-number <pr> --base main --verification-summary-file .scratch/github-issue-plans/verification-issue-<number>-pr-<pr>.md
     ```

5. **Stop after PR creation**
   - Do not wait in-session for approval and merge.
   - Do not close, label, or comment on the issue during execution mode.
   - End with the branch, commit, PR URL, validation result, and the resumable post-merge follow-up command.

## Post-Merge Follow-Up Workflow

Use this workflow after the PR has been approved and merged into `main`.

1. **Verify on updated main**
   - Checkout `main` and pull the latest remote state.
   - Rerun the verification commands recorded in the issue plan or PR body.
   - Write a short Markdown verification summary file, normally `.scratch/github-issue-plans/verification-issue-<number>-pr-<pr>.md`.

2. **Post the issue comment**
   - Run the bundled script:
     ```powershell
     $skillDir = 'C:\Users\Akshay Diwadkar\.agents\skills\github-issue-planner'
     python "$skillDir\scripts\post_merge_issue_followup.py" --env .env --github-repo-url owner/repo --issue-number <number> --pr-number <pr> --base main --verification-summary-file .scratch/github-issue-plans/verification-issue-<number>-pr-<pr>.md
     ```
   - The script confirms the PR is merged into the expected base branch, has approval evidence, references the requested issue, and that the issue number is still an issue rather than a PR.
   - The script avoids duplicate comments by using a hidden marker: `github-issue-planner:issue=<number>:pr=<pr>`.

3. **Do not mutate issue state**
   - Do not close the issue.
   - Do not apply or remove labels.
   - Do not use GitHub auto-close keywords in PR bodies.

## GitHub Configuration

Create `.env` from `.env.example` or export equivalent variables:

```dotenv
GITHUB_TOKEN=
GITHUB_ISSUE_FETCH_LABELS=
GITHUB_ISSUE_FETCH_LIMIT=
# Optional. Defaults to https://api.github.com.
GITHUB_API_URL=
```

Safe env handling:

- `.env.example` is safe to read.
- `.env` is sensitive and must be treated as a secret-bearing file.
- Never directly read `.env` in the agent context: do not run `cat .env`, `Get-Content .env`, `type .env`, `rg ... .env`, `Select-String ... .env`, or equivalent commands.
- Never inspect `.env` contents to debug authentication. If debugging is needed, inspect only existence, size, or path metadata.
- Pass `.env` paths only to trusted bundled scripts via `--env`; checker output must mask tokens.

`GITHUB_TOKEN` is required. Labels and limits are optional defaults only. Pass the repository target per run with `--github-repo-url`. Trusted bundled scripts may parse `.env` internally when passed `--env`; the agent must not read the file directly.

`GITHUB_API_URL` is optional and defaults to `https://api.github.com`.

Read-only planning mode needs issue read access. Opt-in execution and post-merge follow-up need token permissions for pull requests and issue comments, plus local `git`/`gh` authentication for branch, push, and PR creation.

## Safety Rules

- In default planning mode, do not comment on GitHub issues.
- In opt-in execution mode, do not comment on GitHub issues.
- In post-merge follow-up mode, comment only with the bundled `post_merge_issue_followup.py` script after verification passes on updated `main`.
- Do not apply or remove labels.
- Do not close issues.
- Do not implement code fixes unless opt-in execution mode was explicitly requested for exactly one `ready-to-plan` issue.
- Do not treat GitHub repository contents as the codebase; only the local checkout is the code source.
