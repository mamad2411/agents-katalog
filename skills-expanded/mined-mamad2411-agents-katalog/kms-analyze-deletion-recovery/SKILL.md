---
name: kms-analyze-deletion-recovery
description: Analyze AWS KMS key disablement, scheduled deletion, deletion windows, cancellation, dependent-service impact, and recovery options. Use for accidental deletion, disablement incidents, or lifecycle governance.
---

# Analyze Deletion and Recovery

1. Identify key state and whether deletion is scheduled.
2. Inspect deletion window and dependent resources/services.
3. Determine whether cancellation is still possible.
4. Assess impact of disabled or pending-deletion state on applications.
5. For multi-Region keys, inspect replica relationships before deletion decisions.
6. Never schedule or accelerate deletion without explicit authorization.

## Output
- Key State
- Deletion Timeline
- Dependent Resources
- Recovery Options
- Recommended Action
