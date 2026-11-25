---
name: test
description: "Use when every wave of GOAL.md has been built and pasted and it is time for pipeline stage 8: the Testing and Quality Agent runs the validators, checks the contract and assembles the test script for the environment (denial by role and unit, full cycle on the data). Passed, it moves on to UAT; failed, it sends the fix back to the app or the automations. Do not use before /pp-en:build, nor to investigate a number that does not match (describe it to the `power-platform` orchestrator)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:test — Testing and Quality Agent

Stage 8 of the pipeline, block **4. Validation and delivery**. The `pp-en:qa-agent` agent proves what
can be proven without an environment and writes the script for what only the environment proves; the
user runs that script. The question in the diagram: **tests passed?**

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
What counts as truly green: `KIT/skills/power-platform/references/final-gate.md`.

## Before you start

1. `estado.py comecar test`. Exit 1: show the output and stop.
2. Check in `GOAL.md` that no build task is open. If one is, the previous stage did not finish: say
   which one and point to `/pp-en:build`.

## Steps

1. **Agent.** `◆ Calling the Testing and Quality Agent...` and call `pp-en:qa-agent` with `RAIZ`,
   `KIT` (the value of `${CLAUDE_PLUGIN_ROOT}`) and the scope (all waves, or only the fixes since the
   last `docs/qa/QA-*.md`). Model: `modelos.py de qa-agent` (empty line: do not pass `model`).
2. **Reopen the strongest findings** before believing them: rerun the validators the agent cited and
   check 2 or 3 findings with the command it gave
   (`KIT/skills/power-platform/references/subagents.md`). What does not reproduce goes in as "not
   verified". A report without the requested evidence: revision. Record it with
   `estado.py veredito test --agente qa-agent --resultado <...> --motivo "..."`.
3. **Write** `docs/qa/QA-<YYYY-MM-DD>.md`: a `Criterion | Command | Output | Passes? | Date` table, the
   confirmed findings and the test script for the environment.
4. **Tests in the environment** (checkpoint `Action in the environment`, 🔴). Hand over the agent's
   script, short and numbered, to run in the development environment:
   - denial: a user **without** the permission, a user from **another unit** and a user **with** the
     permission, on every write action (the flow returns `status = "error"` for the first two);
   - full cycle: create → query → change → check in the data (not only on screen);
   - volume: counter and gallery with more than 2,000 rows, if the PRD expects it.
   "Type 'all passed' or list what failed (the step and what appeared)."
5. **Tests passed?** Passed when: no critical or high finding is open **and** the environment script
   passed in full.

## Closing

- **Passed:** `estado.py concluir test --nota "QA-<date>: <N> criteria ok"`. Next step: UAT.
- **Failed:** write each failure in `docs/qa/fixes.md` (`| # | Layer (app/flows) | Where | What
  failed | How to reproduce | Status |`), classifying the layer:
  - screen, formula, navigation or message → `app`;
  - flow, authorization, procedure or write → `flows`.
  Then `estado.py reabrir build --motivo "QA-<date>: <k> failures" --argumento <app|flows>`. If
  there are failures in both layers, omit `--argumento`: `/pp-en:build` calls both agents. This is the
  "Fix app / Fix automations" loop of the diagram.
- Commit if `git_commit_por_etapa`: `pp(test): QA-<date> <passed | k failures>`.
- Summary and the "Next step" block the script printed.
