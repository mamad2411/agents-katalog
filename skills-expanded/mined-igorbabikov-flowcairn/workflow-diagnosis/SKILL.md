---
name: workflow-diagnosis
description: Diagnose a bounded bugfix or verified scenario failure before proposing a source correction.
---

# Evidence before correction

- Read the original criterion, current source owner, consumers, immutable test oracle and actual failed receipt/report. A failed scenario confirms an observation; it does not automatically identify the cause.
- Distinguish a source defect, inconsistent plan, environment failure, wrong verifier and uncertain process. Name a falsifiable cause hypothesis and connect it to the relevant source and scenario. Use existing read-only evidence; the Executor runs checks after a brokered proposal.
- Correct source only when the hypothesis explains the original expected behavior. Keep the approved scope, interfaces, criteria and tests unchanged. Do not make a timeout disappear by disabling an assertion, weakening an expected result, adding an unapproved dependency or replacing a real integration with a mock.
- For missing capability, bad oracle, contradictory requirements or unresolved uncertainty, report the specific blocker and propose no speculative edits. No report, zero tests, unknown termination and stale inputs cannot authorize a repair.
- The existing repair budget is finite. A repair closes only with fresh required checks against the final source/artifact/environment; a self-reported diagnosis or successful edit is not proof.
