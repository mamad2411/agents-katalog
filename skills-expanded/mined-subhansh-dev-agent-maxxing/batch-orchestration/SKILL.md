---
name: batch-orchestration
description: Orchestrate large parallelizable changes by decomposing into independent units and spawning parallel worker agents in isolated worktrees.
---

# Batch Orchestration — Parallel Work

Extracted from Claude Code's bundled `batch` skill.

## Phase 1: Research and Plan

1. **Understand the scope.** Launch subagents to deeply research what the task touches. Find all files, patterns, and call sites that need to change.

2. **Decompose into independent units.** Break the work into 5-30 self-contained units. Each unit must:
   - Be independently implementable in an isolated git worktree
   - Be mergeable on its own without depending on another unit's PR
   - Be roughly uniform in size

   Scale the count to the actual work: few files → closer to 5; hundreds → closer to 30. Prefer per-directory or per-module slicing.

3. **Determine the e2e test recipe.** Figure out how a worker can verify its change actually works end-to-end:
   - Browser automation for UI changes
   - CLI verifier for terminal changes
   - Dev-server + curl for API changes
   - Existing e2e/integration test suite

4. **Write the plan** with:
   - Summary of research findings
   - Numbered work units (title, files, description)
   - E2e test recipe
   - Worker instructions template

## Phase 2: Spawn Workers

Spawn one background agent per work unit. All agents use `isolation: "worktree"` and `run_in_background: true`. Launch them all in a single message block.

Each agent's prompt must be self-contained:
- Overall goal
- Specific work unit description
- Files/directories to modify
- E2e test recipe
- The exact changes to make

## Phase 3: Collect and Merge

After all workers complete:
1. Review each worktree's changes
2. Verify e2e tests pass for each
3. Merge worktrees back into the main branch
4. Resolve any conflicts
5. Run a final integration test

## Rules

- Workers must not modify files outside their assigned scope
- If a worker fails, diagnose and retry with more context
- Never skip e2e verification — unit tests aren't enough
- Keep worker prompts concise but complete
