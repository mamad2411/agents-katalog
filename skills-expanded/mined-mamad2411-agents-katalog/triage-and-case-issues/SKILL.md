---
name: triage-and-case-issues
description: Turn pasted logs, stack traces, terse bug reports, and feature ideas into concise, repo-aware issue cases across Linear and GitHub. Use when the user pastes raw artifacts with little explanation, asks to triage or case work, wants bug or feature classification, needs duplicate or stale tracker work corrected, or wants a larger problem split into parent and child issues with blocker links.
---

# Triage and Case Issues

## Apply the Skill

- Start from the pasted artifact or terse request. If the user provides logs, traces, or other raw evidence without much explanation, assume something is not working in the current repo or project unless the user says otherwise.
- Read `references/rules.md` before writing tracker updates.
- Respect repo-local instructions such as `AGENTS.md` before running commands, choosing validation, or touching trackers.
- Preserve exact evidence: error text, route strings, env vars, versions, issue IDs, branch names, and file paths.

## Work in This Order

1. Orient the case.
   - Identify the repo, likely language, and failing seam from the artifact and local checkout.
   - Rephrase the report into concise technical terminology without losing the original evidence.
   - If the request is clearly future product work rather than a current failure, case it as a feature or improvement for `n+1` instead of a bug.
2. Classify and size.
   - Decide type, scope, rough effort, severity, and likely owner shape using `references/rules.md`.
   - If the evidence is too thin for a confident fix, case it as investigation or needs-info rather than inventing certainty.
3. Check tracker state before creating anything.
   - Search Linear first, then read matching issues, comments, status, parent-child links, and completion state.
   - If a duplicate already exists, update, reopen, or amend it instead of filing a blind duplicate.
   - If an old issue was marked done but the problem clearly persists, comment with fresh evidence and mention the original creator or assignee when that context is useful.
4. Decompose only when it helps execution.
   - Create a parent issue when the work spans multiple surfaces, repos, or order-dependent tasks.
   - Create child issues that are independently actionable and wire `blocks` or `blockedBy` immediately.
5. Mirror actionable work into GitHub.
   - Resolve the repo from the local checkout when possible.
   - Prefer `gh` for GitHub issue creation in the current repo, and use GitHub MCP for reading or fallback creation when it is the better surface.
6. Close the loop.
   - Leave concise AI-generated triage comments when changing or reviving tracker state.
   - Return the created or updated issue set, duplicate decisions, blocker graph, and any missing information.

## Tool Rules

- Search for available `linear` and `github` tools before assuming exact names.
- Read before write in Linear.
- Verify `gh auth status` before using `gh issue create`.
- Use repo-native validation when reproducing or confirming a bug. If Rust tests are needed, run `cargo test` from WSL2.

## Reference Map

- Read `references/rules.md` for classification rubrics, duplicate handling, issue templates, GitHub CLI patterns, and blocker decomposition rules.
