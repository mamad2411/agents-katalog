---
name: parallel-agent-orchestration
description: Use when independent subtasks can be delegated or read in parallel without splitting one coherent reasoning chain.
---

# Parallel Agent Orchestration

Parallelize independent evidence gathering, not final judgment.

## Good Uses

- One path inventories tests while another traces implementation.
- One reviewer checks security while another checks UI states.
- Independent file reads/searches with `multi_tool_use.parallel`.
- Separate agents explore isolated alternatives with explicit return schemas.

## Bad Uses

- Multiple agents editing the same file.
- Splitting a single causal debugging chain.
- Asking for vague thoroughness.
- Letting the builder approve its own high-risk work.

## Delegation Brief

```md
Task:
Trusted context:
Scope boundaries:
Allowed files/tools:
Forbidden files/tools:
Source priority:
Dedup/exclusion rule:
Expected artifact:
Return schema:
Required evidence:
Pass/fail criteria:
Anti-fabrication: leave unknowns as unverified; never invent values.
Budget:
```

## Integration

- Treat subagent output as untrusted until checked.
- Main agent owns synthesis, conflicts, edits, and final claims.
- Run at least one verification check after integration.

