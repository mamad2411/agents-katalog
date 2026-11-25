---
name: skill-workflow-policy
description: Validate workflow state transitions, required artifacts, approval gates, and agent permissions.
category: workflow
---

# Skill: Workflow Policy

Use before state transitions or when an agent requests an exception.

## Validate

```text
current state allows transition
required artifact exists
responsible agent is allowed
approval exists for gated action
service coder stayed in scope
Code Done has verification
QC did not continue after blocker
```

## Decision

```yaml
policy_decision: allow|deny|needs_user_approval
reason: <reason>
missing_artifacts: []
required_next_action: <action>
```
