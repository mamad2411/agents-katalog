---
name: itsol-technical-planning
description: "Plan architecture, implementation, rollout, rollback, monitoring, and verification."
---

# ITSOL Technical Planning

After self-review of a Technical or Technical Fix Plan, follow the effective review trigger. With `adaptive`, the main agent decides whether isolated review is proportionate to scale, uncertainty, novelty, blast radius, and verification strength. A selected read-only reviewer is pre-authorized. Resolve concrete material findings, but do not rerun for optional improvements or minor comments.

Resolve and preserve the complete task state through `itsol-workflow-mode` before applying any plan prerequisite or Decision Gate.

## Process

1. Confirm all seven workflow-state fields and applicable `.itsol.md` restrictions; propagate them into artifacts and handoffs.
2. Branch prerequisites by mode:
   - `governed`: for functional work, require the specific Business Plan to be explicitly approved; run the Technical Decision Gate and wait for the user's choice before writing the Technical Plan.
   - `autonomous-planned`: require the Business Plan to be `Ready for execution`; record feasible options, choose the documented recommendation, and continue without a user-decision pause.
   - `direct`: do not create or require a Technical Plan, Business Plan, Decision Gate, plan review, plan approval, plan path, or execution-mode approval; route ordinary technical choices directly to implementation.
3. For planned modes, map affected modules, data, contracts, cache, events, integrations, permissions, infrastructure, observability, QA, repo policy, and technology-version dependencies.
4. Load `itsol-current-tech-context` when framework, SDK, runtime, package, generated client, external API, language edition, database driver, or infrastructure tooling affects the decision.
5. Capture the selected approach, rejected alternatives, risks, open questions, owners, and verification plan. In `autonomous-planned`, ask only when equally plausible choices materially change behavior, permissions, data, rollout, or architecture.
6. Include concrete files/modules, repo-memory context, current-tech context, required ITSOL skills, logical branches, proportionate verification evidence/commands, and candidate subagent split. Do not require TDD entry points or exceptions; add a test-first plan only on explicit user request.
7. For risky release work, document deployment order, validation, monitoring, rollback, and responsibility.
8. For planned modes, write new Technical Plans as `Draft`, self-review them proportionately, run isolated review only when required or worthwhile, and resolve concrete material findings.
9. In `governed`, present the specific Technical Plan, obtain explicit user approval, change it to `Approved`, and ask for execution mode. Do not infer approval from the original request, `continue`, silence, or a generic agent statement.
10. In `autonomous-planned`, change a sufficiently self-reviewed plan to `Ready for execution`, record delegated authorization honestly, choose execution mode, and continue without an approval pause. Never call it user-approved.

## Execution Policy

After resolving `itsol-workflow-mode`, load `itsol-execution-policy` whenever resource, stop, or completion state matters; it owns the full execution state and evidence validation. Never use `maxTurns` or termination as completion; preserve `partial`, `blocked`, and `failed` outcomes.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Techniczne spotkanie implementacyjne
- [02-tech-notes.md](./references/02-tech-notes.md) - Tech notes; Planowanie techniczne i estymacja; Spike techniczny
- [03-release-i-wdrozenie.md](./references/03-release-i-wdrozenie.md) - Release i wdrożenie; Checklist dla spotkania technicznego
