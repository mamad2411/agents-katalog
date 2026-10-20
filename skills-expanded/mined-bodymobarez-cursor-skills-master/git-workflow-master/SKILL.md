---
name: git-workflow-master
description: Master hub for Git, PRs & CI triage. Use for commits, branches, pull requests, and CI triage. Bundles 14 specialized skills (in skills/<name>/GUIDE.md). Use this for any git workflow task.
---

# Git, PRs & CI triage — Master Hub

Use for commits, branches, pull requests, and CI triage.

## How to use this hub

This single skill bundles **all 14 git workflow skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **babysitting-pr** — Monitor a pull request for CI failures, review comments, and merge conflicts — then fix them automatically. Use when a PR is open and you want the agent to keep it merge-ready.  
  → `skills/babysitting-pr/GUIDE.md`
- **blastum-github-cli** — GitHub CLI (gh) comprehensive reference for repositories, issues, pull requests, Actions, projects, releases, gists, codespaces, organizations, extensions, and all GitHub operations from the comman...  
  → `skills/blastum-github-cli/GUIDE.md`
- **creating-pr** — Create a clean, review-ready pull request with a good title, structured description, linked issues, and appropriate reviewers.  
  → `skills/creating-pr/GUIDE.md`
- **mattpocock-git-guardrails-claude-code** — Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety ...  
  → `skills/mattpocock-git-guardrails-claude-code/GUIDE.md`
- **mattpocock-setup-pre-commit** — Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add com...  
  → `skills/mattpocock-setup-pre-commit/GUIDE.md`
- **parallel-ci-triage** — When GitHub Actions fails, fetch failing job logs and assign each failing job to a separate subagent that fixes its slice of the problem in parallel. Use for multi-job CI failures where jobs are in...  
  → `skills/parallel-ci-triage/GUIDE.md`
- **sentry-commit** — ALWAYS use this skill when committing code changes — never commit directly without it. Creates commits following Sentry conventions with proper conventional commit format and issue references. Trig...  
  → `skills/sentry-commit/GUIDE.md`
- **sentry-create-branch** — Create a git branch following Sentry naming conventions. Use when asked to "create a branch", "new branch", "start a branch", "make a branch", "switch to a new branch", or when starting new work on...  
  → `skills/sentry-create-branch/GUIDE.md`
- **sentry-gh-review-requests** — Fetch unread GitHub notifications for open PRs where review is requested from a specified team or opened by a team member. Use when asked to "find PRs I need to review", "show my review requests", ...  
  → `skills/sentry-gh-review-requests/GUIDE.md`
- **sentry-iterate-pr** — Iterate on a PR until actionable CI passes and high/medium review feedback is addressed. Use for PR CI failures, review feedback, or green-check loops; do not wait for human approval, draft status,...  
  → `skills/sentry-iterate-pr/GUIDE.md`
- **sentry-pr-link-issue** — Append a GitHub issue link and its Linear ticket to the current PR's description. Use when asked to "link issue to pr", "fill in issue and linear in pr", "add issue refs to pr", or when given a Git...  
  → `skills/sentry-pr-link-issue/GUIDE.md`
- **sentry-pr-writer** — Create and update pull requests following Sentry conventions. Use when opening a PR or refreshing an existing PR after material changes.  
  → `skills/sentry-pr-writer/GUIDE.md`
- **sentry-triage-frontend-issues** — Triage new issues in the Sentry `javascript` project by archiving non-actionable noise. Use when asked to "triage issues", "triage the javascript project", "archive non-actionable issues", "triage ...  
  → `skills/sentry-triage-frontend-issues/GUIDE.md`
- **writing-commit-messages** — Write clear, conventional commit messages with proper type prefixes, scopes, and body content.  
  → `skills/writing-commit-messages/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
