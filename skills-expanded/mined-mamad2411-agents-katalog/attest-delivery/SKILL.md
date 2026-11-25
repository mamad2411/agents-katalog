---
name: attest-delivery
description: Attest that a reviewed task is present in an integration commit. Use after review approval to verify branch reachability, current evidence, scope, and delivery readiness.
---

# INPUTS
- Review-approved task, resolved delivery context, integration commit SHA, delivery configuration, and current QA/review/design/contract evidence.

# PRECONDITIONS
- Confirm the integration commit exists and is reachable from the configured integration branch.

# ACTIONS
- Run delivery check and inspect pre-integration commands, dependency completion, scope, and repository conflict state.
- Produce or inspect delivery attestation evidence.
- Ask the control plane to close only after a valid attestation.

# OUTPUTS
- Delivery attestation containing commit, tree, branch, changed paths, and check results.

# VALIDATION
- Require current evidence, reachable integration commit, clean relevant worktree/index, and completed dependencies.

# FORBIDDEN
- Do not merge, commit, push, mark done, or waive delivery checks without explicit human/orchestrator authority.
