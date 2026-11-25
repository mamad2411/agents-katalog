---
name: risk-execution-control
description: Route requests through risk, intent, no-assumption, execution, tool permission, approval, and validation gates before side-effect actions.
---
# Risk and Execution Control

Use for any action involving file mutation, command execution, Git, dependency changes, database work, deployment, packaging, CI, MCP writes, or external-system mutation.

Primary references:

- `prompts/150_global_risk_gate.md`
- `prompts/151_intent_stage_router.md`
- `prompts/153_assumption_ban_contract.md`
- `prompts/154_execution_control.md`
- `prompts/155_tool_permission_policy.md`
- `prompts/156_human_approval_protocol.md`
- `prompts/157_validation_and_reporting_gate.md`

Output a decision before execution:

```yaml
execution_decision:
 action: ""
 stage: ""
 risk_class: "low | medium | high | critical"
 allowed: "yes | no | approval_required"
 reason: ""
 validation_required: []
```
