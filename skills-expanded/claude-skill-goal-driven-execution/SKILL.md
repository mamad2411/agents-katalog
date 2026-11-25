---
name: claude-skill-goal-driven-execution
description: Premium Claude Skill - Goal-Driven Execution. Transforms tasks into verifiable success criteria. Leverages the LLM's ability to loop until goals are met.
license: MIT
---

# Goal-Driven Execution (Claude Skill)

**Define success criteria. Loop until verified.**

Transform imperative tasks into verifiable **Claude Skill** goals:

| Task Type | Transformation to Goal-Driven |
|-----------|-------------------------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

### Strategic Planning
For multi-step tasks, always state a brief plan with verification checkpoints:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let this **Claude Skill** function independently. Weak criteria ("make it work") require constant clarification.
