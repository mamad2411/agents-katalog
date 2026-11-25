---
name: parallel-agents
description: Delegate work to subagents effectively and safely. Use when a task splits into independent parts (several unrelated failing tests or bugs, per-module reviews or migrations, broad codebase searches, research across many sources), when the main context is filling up with file dumps, or when the user asks for subagents, parallel agents, or fan-out. Covers when not to delegate, how to write a self-contained brief, how to keep agents from colliding on the same files, and how to verify their output instead of trusting their reports.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Parallel Agents

Subagents give you parallelism and a clean context, but every handoff loses information in both directions: the agent knows only what your brief says, and you only see the summary it returns. Delegation pays off when the work is genuinely independent and the brief is good. Otherwise it's slower, more expensive, and less correct than doing it yourself.

## When to delegate

**Good fits**

- Independent problems: five failing test files with unrelated causes; one review per module.
- Broad read-only exploration where you only need the conclusion, not the files: "find every place we parse dates".
- Research across many sources that would flood your context.
- An independent second opinion, where you deliberately *don't* share your conclusion.

**Poor fits**

- Tightly coupled changes where each step depends on the last.
- Tasks of a few tool calls; the brief costs more than the work.
- Anything where you'd need to re-check every line anyway.
- Work touching the same files as another agent.

## Write a brief like you're briefing a peer

The brief is the agent's entire world. Include:

```markdown
**Goal:** what done looks like, in one or two sentences.
**Context:** the relevant files, how to run things, conventions to follow.
**Already known / ruled out:** so it doesn't repeat your work.
**Scope:** exactly which files or areas it may change; what it must not touch.
**Constraints:** no new dependencies, keep the public API stable, ask before deleting anything, and so on.
**Deliverable:** the format you want back, such as a findings list with file:line, a diff summary, or test results.
**Verification:** the command that proves the work is done.
```

Hand over the problem, not your hypothesis. An agent told "the bug is probably in the cache" will usually come back confirming it.

## Avoid collisions

- Give parallel agents **disjoint files or directories**. Two agents editing the same file produce conflicts or silent overwrites.
- When each needs to edit freely, use separate git worktrees or branches and integrate afterwards.
- Keep shared resources (databases, ports, caches) isolated per agent or run those steps sequentially.

## Verify, don't trust

A subagent's report is a claim, not evidence. When results come back:

1. Read the actual diff, not just the summary.
2. Re-run the verification command yourself.
3. Check that it stayed in scope (`git status`, `git diff --stat`).
4. Look for the common failure modes: tests weakened or skipped to go green, a symptom patched instead of the cause, TODOs left behind, confident claims about code it didn't read.

Then integrate the pieces and run the full suite once more, because changes that pass separately can still conflict together.

## Sizing the fan-out

Start with the smallest number of agents that covers the independent parts, typically 2 to 5. More agents mean more integration work and more tokens; parallelism only helps while the parts are truly independent.
