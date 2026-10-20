---
name: validate-quality
description: Produce deterministic quality evidence from an implementation task. Use after implementation completion for test, lint, typecheck, build, security, design, contract, and architecture-fitness validation.
---

# INPUTS
- Implementation-complete task, resolved verification context, current worktree, configured verification commands, and current governance baseline.

# PRECONDITIONS
- Ensure the task is implementation-complete and its worktree and evidence inputs are current.

# ACTIONS
- Run the control-plane QA command in the assigned worktree.
- Inspect failures or inconclusive checks and preserve the generated evidence.
- Return the task to implementation only through the control plane when required.

# OUTPUTS
- QA evidence with check outcomes, fingerprints, and pass, fail, or inconclusive verdict.

# VALIDATION
- Require current evidence, declared-scope compliance, design/contract convergence, and real configured checks before pass.

# FORBIDDEN
- Do not fabricate QA evidence, override a failed gate, review the change, or close the task.
