---
name: github-auto-implement
description: Autonomous GitHub issue implementation — picks the next ready issue, triages it, implements with TDD, and opens a PR targeting the correct branch (default, epic feature branch, or PR-chained dependency branch). Use when running the autobot daemon, implementing GitHub issues autonomously, or starting the auto-implement loop.
metadata:
  author: CosticaPuntaru
  version: '2.0'
---

## Purpose

Pick the next unassigned issue from GitHub, investigate it formally, implement it using TDD, and open a PR—all in one shot. 

### How to Run (Daemon Mode)
This skill is designed to be run repeatedly by a daemon. To start the auto-implement loop:

```bash
node resources/scripts/github-daemon.mjs
```

The daemon will poll for `ready` issues (defined in `.agenTica.js`, default: `autobot:ready`) and execute this workflow autonomously.

### Optional Configuration
Create a `.agenTica.js` in your current working directory to customize the experience. Use it to switch between GitHub/GitLab styles or override default constants.

## Step 1: Find the Next Issue

Use `gh issue list` to find ready, unassigned tickets.

```bash
# Query is configurable in .agenTica.js. Default:
gh issue list --search 'is:open is:issue label:autobot:ready -label:autobot:question -label:autobot:in-progress' --json number,title,url,labels,comments,body
```

- **Skip**: Humans-only tickets or those requiring clarification.
- **Action**: Pick the first ready issue.

## Step 2: Branch Initialization

1. Checkout `{{BASE_BRANCH}}` and pull the latest:
   ```bash
   git fetch origin
   git checkout {{BASE_BRANCH}}
   git pull origin {{BASE_BRANCH}}
   ```
2. Create a new branch off `{{BASE_BRANCH}}`:
   ```bash
   git checkout -b {{BRANCH_NAME}}
   ```

> **Epic & dependency context**: `{{BASE_BRANCH}}` is resolved by the daemon before this skill runs.
> - For one-off tickets: `{{BASE_BRANCH}}` = the repo default branch (`main`).
> - For epic tasks with `Parent PRD: #N`: `{{BASE_BRANCH}}` = `epic/<N>-<slug>` (the epic feature branch).
> - For tasks with `Blocked by: #N`: `{{BASE_BRANCH}}` = the blocking issue's open PR branch (PR chaining).

## Step 3: Triage & Investigation (Investigation Phase)

Instead of jumping into code, investigate the issue formally.
- **Skill**: `triage-issue`
- **Action**: Run `triage-issue` on the picked ticket. Identify the root cause, establish a reproduction case, and draft a TDD-based fix plan. 
- **Checkpoint**: Save the triage result to `.agents/triage/{{ISSUE_ID}}.md`.

## Step 4: Implementation (TDD Phase)

Execute the fix plan using a strict Red-Green-Refactor loop.
- **Skill**: `tdd`
- **Action**: Run the `tdd` skill using the plan generated in the Triage phase. Ensure each requirement has a corresponding test and that all tests pass.

## Step 5: Post-Task Validation (Quality Phase)

Ensure the implementation meets project standards.
- **Skill**: `post-task-validation` (and `react-doctor` if applicable).
- **Action**: Run full validation (linting, type-checking, and all smoke tests). Fix any regressions autonomously.

## Step 6: Documentation & PR Metadata

1. **Commit**: `git commit -m "Fixes #{{ISSUE_ID}}: {{ISSUE_TITLE}}"`
2. **Push**: `git push -u origin {{BRANCH_NAME}}`
3. **Write PR metadata** to `./tmp/pr-meta.json` (the daemon will create the PR):
   ```json
   {
     "title": "Fixes #{{ISSUE_ID}}: {{ISSUE_TITLE}} [#{{ISSUE_ID}}]",
     "body": "<markdown body referencing triage notes, TDD results, and including 'Fixes #{{ISSUE_ID}}'>"
   }
   ```
   - **Title**: Must include `[#{{ISSUE_ID}}]` so the daemon can locate it for dependent tasks.
   - **Body**: Reference the triage notes and TDD results. Include `Fixes #{{ISSUE_ID}}` so GitHub cross-references the issue.

## Step 7: Final Status

Print `DONE` as the very last line of output.

## Guardrails

- **🤖 Prefix**: Every comment posted to GitHub MUST start with the 🤖 emoji.
- **Clarification Requested**: If the issue description is ambiguous during Triage:
  1. Comment: `gh issue comment <number> --body "🤖 Need clarification on..."`.
  2. Edit Labels: Swap current `inProgress` label for the `question` label (as defined in `.agenTica.js`).
  3. Output: Print the exact string `CLARIFICATION_REQUESTED` as the final output.
  4. **Stop**: Reset the branch and stop immediately.
- **No `as` Casting**: Follow `typescript-no-as-casting` (Zod validation preferred).
- **Tracer Bullets**: If the task is large, ensures it can be implemented in a single vertical slice.
- **Recursive Grill**: If requirements are unclear during drafting, re-trigger a mini-grill.
