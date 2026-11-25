---
name: deepseek
description: Explicitly opt in to DeepSeek-backed Subagent Router delegation for a single task.
---

# DeepSeek Backend Delegation

Use this skill only when the user explicitly invokes `$deepseek` or `/deepseek`.
Normal Codex sessions must not use Subagent Router subagents just because the
DeepSeek-backed provider is installed.

## Delegation Contract

1. Use GPT-5.5 as the parent orchestrator for task decomposition, final
   consolidation, acceptance review, security-sensitive judgment, and ambiguous
   product decisions.
2. Use `subagent_router_reviewer` for first-pass reviews of uncommitted changes,
   current branches, commits, commit ranges, regression checks, and edge-case
   review.
3. Use `subagent_router_worker` for codebase exploration, isolated
   implementation, boilerplate, simple refactors, test writing, and first-pass
   bug investigation.
4. Do not use DeepSeek-backed router subagents for secrets, credentials, production
   data, security-sensitive logic, or broad architecture changes unless the
   user explicitly asks for that risk.
5. After spawning a Subagent Router agent, wait up to 300 seconds.
6. On timeout, inspect sanitized proxy activity and session mirror paths from
   `subagent-router paths` or `/debug/activity`; do not rely on repo-local hardcoded log
   paths.
7. If proxy activity is stale or missing, or the proxy agent fails, stop and
   report the failure instead of silently continuing with local implementation.

## Reviews

Do minimal scope discovery before delegation: identify the requested path,
commit, or range, and run only cheap commands such as `git status --short` or
`git diff --stat` when needed. Spawn `subagent_router_reviewer` before reading
large diffs, source files, tests, or related modules.

The parent model must consolidate the final review and report discrete,
evidence-backed findings with severity, file paths, rationale, and concrete fix
suggestions.

## Implementation

Create a short plan, delegate bounded implementation or exploration to
`subagent_router_worker` when practical, and tell the worker its file/module
ownership. Workers are not alone in the codebase; they must not revert edits
made by others.

For confirm-and-fix workflows, prefer reviewer confirmation followed by worker
patching when the fix is isolated and not security-sensitive. The parent model
reviews the worker diff, performs narrow integration cleanup if needed, and
runs relevant verification.
