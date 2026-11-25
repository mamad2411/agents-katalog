---
name: implement-spec
description: Implement a whole specification as one PR by running its ticket task graph with parallel implementer subagents, merging as tickets finish. Use when a spec with tickets exists and the goal is a single PR. Not for a few small tickets (use implement).
disable-model-invocation: true
---
You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The goal is a PR which implements the entire spec on a single branch.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for **maximum concurrency**.

## Steps

1. Read the spec and tickets. Read enough to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create a branch, and a draft PR. The PR should be marked as 'closing' the spec issue and tickets.

4. Use **implementer subagents** to implement each ticket. Each implementer subagent should work in its own worktree, on its own branch.

5. Once an **implementer subagent** completes, merge its work to the PR branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, run /code-review on the PR branch. Fix all issues raised by the code review in a single **implementer subagent**.

8. Mark the PR as ready for review.

9. Clean up all **implementer subagent** worktrees.

## Purpose
Drive a spec's ticket graph to a single merged PR using parallel subagents in separate worktrees.

## When to use
A spec and its tickets exist; the whole spec should land on one branch.

## When NOT to use
- Small work -> implement.
- No tickets -> to-tickets first.

## Inputs
Spec, tickets with blocking relationships, repository, test commands.

## Edge cases and failure handling
- A ticket fails or conflicts on merge -> merger subagent resolves; if blocked, pause dependents and report.
- Frontier empty but tickets remain -> a dependency cycle or blocked ticket; surface it.

## Validation
- All tickets closed by the PR; full tests and typecheck pass on the PR branch; conflicts resolved; PR description lists tickets.

## Output requirements
A ready PR closing the spec and tickets, with a short status of each ticket.

## Example
```text
Frontier: tickets 1, 2 -> run two implementers in parallel -> merge -> frontier now 3, 4 -> repeat until done.
```

## Related skills
implement, to-tickets, to-spec, subagent-driven-development
