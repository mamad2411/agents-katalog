---
name: diagnosing-bugs
description: Diagnose a concrete failure or performance regression from code, reproduction, logs, or run artifacts.
---

# Diagnose from evidence

Establish expected behavior, the observed symptom, affected version and scope.
Inspect the relevant code and available evidence before choosing a diagnostic
method. Separate observations from hypotheses and test the most informative
prediction next; do not manufacture a fixed number of competing explanations.

## Redact diagnostic evidence

Before displaying commands, outputs, or artifact excerpts, replace secrets with
`<REDACTED>`. Keep credentials in environment variables rather than embedding
their values in commands or scripts; do not expose them through shell tracing.
Logs and captured requests can contain auth headers, cookies, and tokens: show
only the lines needed to support the diagnosis, with sensitive values removed.
If evidence is missing, request a redacted artifact or a specific safe observation.
In the HITL script, `capture` echoes observations; signing in stays a user `step`.

## Choose the available evidence path

- **Local reproduction:** use the smallest relevant existing test or command.
  Confirm it catches the reported symptom, then simplify the reproducer when
  that helps distinguish causes. Avoid spending longer building a diagnostic
  framework than investigating the actual failure.
- **Remote or costly failure:** follow the terminal traceback, effective config,
  run identifiers, and available artifacts. Form explicit hypotheses from this
  evidence even if the original environment cannot be reproduced locally.
  Identify the smallest remote check needed to distinguish them. Continue all
  useful read-only investigation before reporting a need for access.
- **Performance or intermittent failure:** record a baseline and repeat enough
  to distinguish signal from noise within the task's budget. Preserve relevant
  timing, seeds, versions, and environmental differences. Use profiling or query
  plans where they answer the question better than added logs.

Choose probes that discriminate between plausible causes. Change one causal
factor at a time when practical. A retry needs either new evidence or a defined
measurement purpose; do not repeatedly trigger the same expensive run.
Production instrumentation, state changes, and paid compute follow the user's
existing authorization and the environment's rules.

## Fix and verify

When a fix is authorized, apply the smallest change supported by the evidence.
For code behavior, use $tdd: demonstrate a relevant failing regression test before
changing the implementation, then run the affected checks. Choose the public
boundary from the code; ask only if the intended behavior is unresolved. For a
configuration or infrastructure cause, verify the effective setting or original
failure path rather than inventing an unrelated unit test.

Rerun the original scenario when feasible. Local tests can verify the code change
without proving that a remote deployment or job has recovered. Report those two
claims separately. Remove diagnostic artifacts you added when no longer needed;
retain useful evidence at the project's normal location.

Finish with the supported cause or remaining hypotheses, changes made, observed
verification, and the exact missing evidence if remote confirmation is pending.
If the request was diagnosis-only, deliver the diagnosis and proposed fix without
mutating application code. Use [the HITL script](scripts/hitl-loop.template.sh)
only when a human must perform the reproducing interaction.
