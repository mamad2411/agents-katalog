---
name: safereach-agent-boundary-reviewer
description: Enforces the Cursor and Kiro division of labor for SafeReach. Use when coordinating agents, delegating work, reviewing handoffs, or deciding whether a task belongs to Cursor or Kiro.
---

# SafeReach Agent Boundary Reviewer

## Required First Step

Use `safereach-context-lock` before agent coordination.

## Cursor Owns

- UI implementation
- React and TypeScript refactoring
- Accessibility review
- Component boundaries
- Styling consistency
- Browser verification
- Demo-readiness checks
- Small behavior-preserving frontend fixes

## Kiro Owns

- Heavy computation
- Broad scenario analysis
- Exhaustive reasoning
- Large generated artifacts
- High-volume simulations
- Computation-heavy validation outside normal frontend checks

## Routing Rule

Route work by task type:

```ts
function routeSafeReachTask(task: AgentTask) {
  if (task.requiresHeavyComputation || task.requiresLargeScenarioAnalysis) return 'kiro'
  if (task.affectsUI || task.affectsRefactor || task.requiresBrowserVerification) return 'cursor'
  return 'cursor'
}
```

## Handoff Requirements

Every Cursor/Kiro handoff must include:

- The two shared context paths.
- The current task owner.
- Affected files.
- Relevant PRD or deployment guide references.
- Assumptions.
- Verification status.
- Open risks.

No handoff may rely on private agent memory as product truth.
