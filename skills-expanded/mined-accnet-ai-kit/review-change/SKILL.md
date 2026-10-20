---
name: review-change
description: Submit an independent review recommendation for a QA-passed task. Use to assess scope, acceptance criteria, contracts, security, regression risk, and delivery readiness.
---

# INPUTS
- QA-passed task, resolved review context, current QA evidence, task diff, contract/design evidence, and reviewer identity.

# PRECONDITIONS
- Confirm QA evidence is current and the reviewer identity differs from the executor.

# ACTIONS
- Inspect declared scope, acceptance criteria, diff, risks, and evidence.
- Record findings and submit an approve or changes-requested recommendation artifact.
- State residual risk and follow-up tasks where needed.

# OUTPUTS
- Independent review recommendation with decision, findings, evidence paths, and reviewer identity.

# VALIDATION
- Verify QA/design/contract evidence freshness and reviewer/executor identity separation.

# FORBIDDEN
- Do not modify implementation, apply the review decision, bypass findings evidence, or close the task.
