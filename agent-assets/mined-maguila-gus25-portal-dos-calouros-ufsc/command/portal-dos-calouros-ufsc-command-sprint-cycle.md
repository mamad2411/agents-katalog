---
description: Roda um ciclo completo de sprint de ponta a ponta, sem parar para confirmação — encadeia /sprint-plan, /sprint-run e /sprint-review.
---

Act as the **Scrum Master** (`.claude/agents/scrum-master.md`), running a full sprint cycle for this project. This command chains the three existing rituals and runs them **end to end in a single turn, without stopping to ask the user for approval between them**. The user invoked the full cycle — that is the approval.

1. **Plan**: Follow `/sprint-plan` (`.claude/commands/sprint-plan.md`) in full, **except its final confirmation step** — write the plan to `docs/SPRINT.md`, state the chosen scope in a couple of lines, and continue straight to step 2 in the same turn. Do not ask for approval. Only stop if the sprint scope is genuinely ambiguous in a way that would change what gets built.

2. **Run** (immediately after step 1, no confirmation): Follow `/sprint-run` (`.claude/commands/sprint-run.md`) in full — dispatch subagents per story in dependency order, run `tester`/`debugger` as needed, update story statuses in `docs/SPRINT.md`.

3. **Review** (immediately after `/sprint-run` finishes, no extra confirmation needed): Follow `/sprint-review` (`.claude/commands/sprint-review.md`) in full — final verification, `ui-ux-review`, update `docs/product-backlog.md`/`docs/SPRINT.md`/`README.md`, retrospectiva.

4. Summarize the full cycle's outcome (planned → executed → reviewed) for the user. As in `/sprint-review`, suggest deploy but don't deploy automatically.

If at any point a step's own stop condition triggers (e.g. `/sprint-plan` finds an active unreviewed sprint, `/sprint-run` finds nothing to run, `tester` reports unfixable failures), follow that step's instructions and halt the cycle there.
