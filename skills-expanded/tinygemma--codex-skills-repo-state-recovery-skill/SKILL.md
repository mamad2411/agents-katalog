---
name: repo-state-recovery
description: Recover where repo work stood after an interruption by combining recent context, git state, tests, plan files, and ignored-file auditing. Use when the user asks what was happening before a crash or wants the current repo situation reconstructed reliably.
---

# Repo State Recovery

Use this skill when the user cares about what is true now, not what chat folklore says
was probably true before the interruption.

## Procedure

1. Recover recent context
   - use available session/thread context if it exists
   - read repo handoff files, plans, and state artifacts
2. Inspect git state
   - `git status --short --branch`
   - recent commits
   - `git diff --stat`
3. Verify current health
   - run the repo's declared tests or gates
   - if the repo has no clear test entrypoint, say so explicitly
4. Audit local-only risk
   - inspect untracked files
   - inspect ignored files if anything looks suspicious
5. Reconstruct the workstream
   - identify the last meaningful increment
   - identify what is committed, what is local, and what is ambiguous

## Output

Give the user:

- where work had reached
- current test or gate status
- committed vs local-only state
- likely next actions
- any recovery-risk findings

## Pitfalls

- Do not rely only on git history.
- Do not rely only on prior conversation.
- Do not skip ignored-file checks when source files seem to be missing.
- Do not say the repo is probably fine if you can verify it.
