---
name: incremental-implementation-pro
description: Implement software in small, safe, verifiable slices. Use for multi-step features, risky refactors, UI/API/database changes, or any task that should be split into atomic commits or phases.
---

# Incremental Implementation Pro

## Workflow

1. Split work into vertical slices that each produce testable behavior.
2. Start with the smallest slice that validates the architecture.
3. Avoid mixing unrelated concerns in one change.
4. Verify each slice before expanding.
5. Update docs and evolution records at meaningful milestones.

## Slice Rules

- One slice should have a clear behavior change.
- Prefer end-to-end thin slices over broad unfinished scaffolding.
- Keep migrations, API changes, UI changes, and release toggles explicitly sequenced.
- Use feature flags or compatibility layers when rollout risk is high.

## Stop Conditions

Stop and report if:
- A slice requires unknown credentials or infrastructure.
- Existing architecture conflicts with the requested design.
- The next slice would be destructive or high-risk.

## Output

Report completed slice, remaining slices, verification, and docs updated.
