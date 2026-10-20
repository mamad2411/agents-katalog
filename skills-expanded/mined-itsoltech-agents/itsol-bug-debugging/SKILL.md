---
name: itsol-bug-debugging
description: "Fix bugs evidence-first with root cause, regression coverage, and mode-aware authority."
---
# ITSOL Bug Debugging

Resolve all seven task-state fields through `itsol-workflow-mode`. In every mode gather evidence, isolate the failing boundary, establish root cause, implement the smallest fix, verify the changed behavior proportionately, and self-review. A failing automated test and TDD exception are not prerequisites; use `itsol-tdd-workflow` only on explicit user request.

## Mode Branches

- `governed`: run the Fix Decision Gate, wait for the user's choice, create a `Draft` Technical Fix Plan, self-review it proportionately, use isolated review only when policy or material risk warrants it, resolve concrete material findings, present the file, obtain explicit approval, mark it `Approved`, then implement.
- `autonomous-planned`: record options and choose the documented recommendation, create the plan as `Draft`, self-review it proportionately, decide whether isolated review adds value, resolve concrete material findings, mark it `Ready for execution` with delegated authorization, and continue without approval pauses.
- `direct`: do not create or require a Fix Plan, Fix Decision Gate, plan review, approval, or plan path. Record `artifact_state: not-required` and proceed from evidence/root cause to implementation and proportionate verification.

Never call an autonomous plan user-approved. Ask only for unresolved material ambiguity or independent protected-action authority. Apply `.itsol.md` through `itsol-repo-memory` when present and propagate all seven fields to artifacts and handoffs.

## Execution Policy

After resolving `itsol-workflow-mode`, load `itsol-execution-policy` whenever resource, stop, or completion state matters; it owns the full execution state and evidence validation. Never use `maxTurns` or termination as completion; preserve `partial`, `blocked`, and `failed` outcomes.

Only relevant evidence references.

Apply plan and approval prerequisites only after resolving `itsol-workflow-mode`; evidence and root-cause analysis remain mandatory in every mode.

## Technical Fix Plan Gate Routing

For bugfix planning, approval guardrails, Fix Decision Gate, Technical Fix Plan template, self-review, and Rubber Duck Plan Review, read [07-technical-fix-plan-gate.md](./references/07-technical-fix-plan-gate.md).

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Zasada ogólna; Dwa tryby pracy
- [02-praca-nad-naprawa-bledu.md](./references/02-praca-nad-naprawa-bledu.md) - Praca nad naprawą błędu
- [03-pytania-do-gumowej-kaczki-przy-bugfixie.md](./references/03-pytania-do-gumowej-kaczki-przy-bugfixie.md) - Pytania do gumowej kaczki przy bugfixie; Antywzorce przy bugfixach
- [04-debugowanie-krok-po-kroku.md](./references/04-debugowanie-krok-po-kroku.md) - Debugowanie krok po kroku; Checklista dla bugfixa; Proces myślowy - przykład bugfixa
- [05-edge-case-y-ktore-deweloper-powinien-sam-wymyslac.md](./references/05-edge-case-y-ktore-deweloper-powinien-sam-wymyslac.md) - Edge case'y, które deweloper powinien sam wymyślać; Kiedy prosić o pomoc; Komunikacja statusu; Czerwone flagi podczas pracy
- [06-definicja-ukonczenia-zadania-przez-dewelopera.md](./references/06-definicja-ukonczenia-zadania-przez-dewelopera.md) - Definicja ukończenia zadania przez dewelopera
- [07-technical-fix-plan-gate.md](./references/07-technical-fix-plan-gate.md) - Technical Fix Plan Gate; Fix Decision Gate; Approval Gate; plan file template; self-review; Rubber Duck Plan Review
