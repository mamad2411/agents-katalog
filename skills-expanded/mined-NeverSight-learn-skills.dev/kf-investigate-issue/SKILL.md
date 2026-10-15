---
name: kf-investigate-issue
description: Investigate unclear, intermittent, unexpected, or performance-related behavior and report an evidence-backed cause and next action. Use for requests asking why something happens. Do not implement a fix unless the user also requests correction or safe diagnostic instrumentation requires a change.
---

# Investigate Issue

Turn an unclear symptom into a calibrated diagnosis without prematurely changing
the system.

## Workflow

1. Define the observed behavior, expected behavior, frequency, environment,
   timeline, and impact. Separate reported facts from assumptions.
2. Gather the smallest useful evidence set: logs, errors, configuration, runtime
   state, recent changes, reproduction steps, metrics, and relevant code paths.
3. Trace execution and data flow through the affected boundary. Compare working
   cases and analogous repository implementations.
4. List plausible hypotheses with predicted evidence and test the most
   discriminating ones first.
5. Disprove alternatives where possible and identify the most likely cause,
   contributing factors, and evidence gaps.
6. Report findings, confidence, and the next useful action. State clearly when the
   evidence supports only a hypothesis.
7. If the investigation verifies a recurring contradiction in reusable method,
   routing, or guidance, hand that evidence to `kf-learn-from-evidence`; do not
   persist a lesson in this workflow.

## Constraints

- Prefer direct observations and reproducible checks over intuition.
- Do not modify product behavior during an investigation-only request.
- Add temporary instrumentation only when it is safe, necessary, authorized by the
  task, and removable or intentionally retained.
- Do not hide contradictory evidence or overstate confidence.
- Keep investigation focused on the reported issue; avoid opportunistic refactors.

Use `kf-fix-bug` when the user wants the diagnosed defect corrected in the same task.
