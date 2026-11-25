---
name: cr-process
description: "Change Request process. Use when changes are needed after spec finalization."
---

# Change Request Process

## CR Document Format
```markdown
## CR-{number}: {Title}

- **Requester**: {agent name} (ticket where issue was found)
- **Reason**: Why the change is needed
- **Impact Scope**: Affected ADRs, ticket list
- **Severity**: Minor | Major | Critical
- **PO/PM Verdict**: Approved / On Hold / Rejected
- **Architect Update**: ADR Amendment content (if any)
- **Human Approval**: Required / Not Required
```

## Severity Criteria

| Severity | Criteria | Approval Required |
|----------|----------|-------------------|
| Minor | Implementation detail change, affects 1-2 tickets | PO/PM only |
| Major | Architecture change, affects 3+ tickets | PO/PM + Human |
| Critical | Stack change, full redesign | Re-run entire Review cycle |

## Flow
1. Dev agent requests CR → PO/PM receives
2. PO/PM assesses impact scope and determines severity
3. Approval process based on severity
4. On approval, Architect writes ADR Amendment
5. Save CR document to `docs/cr/`
