---
skillId: sdp-worker
skillVersion: 1.0.0
minimumToolkitVersion: 0.2.0
capabilities:
- sdp.slice.implement
- sdp.fix.implement
compatibilityNotes: Initial formal version for SDP Toolkit 0.2.0.
---

# SDP Worker

Use this skill only after the Master assigns one explicit Slice or Fix.

1. Read the work contract and linked requirements, architecture, design, release
   target and verification requirements.
2. Confirm goal, expected files, invariants, non-goals and completion signal.
3. Inspect current code and records before changing them.
4. Implement the smallest coherent solution satisfying the assigned contract.
5. Avoid unrelated cleanup, release publication, version inflation and speculative
   abstractions.
6. Run required verification and record exact commands, environment and results.
7. Update only the implementation notes and release-note entries requested by the
   contract.
8. Return changed files, decisions, evidence, residual risks and discoveries.
9. Stop; do not begin another Slice or Fix.

Return contradictions or architecture changes to the Master rather than silently
broadening scope.
