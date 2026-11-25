---
name: change
description: "Use when the Power Apps app has already been published by the pipeline (or already has the kit's power-platform.config.json) and the user brings a list of changes: fix, adjust, add a field, screen or rule. It scopes each request, gathers context with research agents, writes one spec per front, sends the build agents in parallel, judges each deliverable (accepted, revision, escalated), runs the change's QA and reopens UAT. Do not use with the pipeline mid-way (the prototype and test loops handle that), on an app without the kit (describe it to the `power-platform` orchestrator) nor for a change that redoes the MVP (reopen the pipeline at brainstorm)."
argument-hint: "[the list of changes, as it came]"
user-invocable: true
disable-model-invocation: true
---

# /pp-en:change — Changes to a published app

Outside the 10 stages: it runs when the app is already live and a list arrives ("fix this, change
that, a field is missing"). It is the head-and-hand cycle applied to a list: you scope, gather the
context, write one spec per front, the agents do it in parallel, you judge, and the user only sees
what passed. **You do not write screens, flows or procedures**: you judge and decide (`subagents.md`).

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Judging: `KIT/skills/power-platform/references/subagents.md`. Template:
`KIT/skills/power-platform/assets/change-template.md`.

## Before you start

1. Banner `PP ► CHANGE` (`output-format.md` §2) and one sentence about what will happen.
2. Where the project stands:
   - `estado.py mostrar`. Some stage before **Publishing** is not done: the pipeline is mid-way;
     show the "Next step" block and stop (adjustments and fixes have their own loops);
   - no `STATE.md` but a `power-platform.config.json`: app adopted by the kit; go on, without the
     state commands;
   - neither: stop and tell the user to describe the request to the `power-platform` orchestrator.
3. Read `power-platform.config.json` (track, folders, `nomes_as_built`), `docs/planning/prd.md`
   (roles, `BR-xx` rules), `architecture.md` (contract), `ux-design-system.md` and the earlier
   `docs/changes/CHG-*.md` (the next number and what was already requested).

## Steps

1. **The list.** `$ARGUMENTS` or ask: "What needs to change? A messy list, screenshots and user
   messages all work." Create `docs/changes/CHG-<NNN>.md` from the template, with the list as it came.
2. **Scope** (you). Each request rewritten in one line, to catch a misunderstanding cheaply, with the
   layer (screen, flow, procedure or table, visual identity) and the size:
   - **small or medium:** proceeds in this change;
   - **large** (new role, new entity, track swap, redoes the MVP): stays out. Recommend reopening the
     pipeline at brainstorm (`estado.py reabrir brainstorm --motivo "..."`); the user decides.
   A request that breaks a `BR-xx` rule or the contract becomes a question, not a spec.
3. **Questions in one round** (checkpoint `Decision`): the scope table and everything still unknown
   (ambiguous, conflicts with a rule, who approves), together: up to 4 closed questions in one
   `AskUserQuestion` call, plus one open one if needed. "Correct whatever is not right."
4. **Context** (you do not do the broad reading). One `pp-en:research-agent` per touched area
   (screens, flows, database), in the **same message**, with `ONDE: project`, `PARA QUE: write the
   change's specs` and the question: which files the change touches, their conventions, the
   gotchas, and **what else depends on it** (another screen that uses the column, another flow that
   calls the procedure). Model: `modelos.py de research-agent`. Judge.
5. **Specs** in section 3 of the CHG, one per front: the agent, the **exact files**, what changes
   (before → after), "done when" with the command that proves it, and what stays out. Two fronts on
   the same file: one after the other. A contract change between app and flow: update `architecture.md`
   first (a new parameter always goes last; screen and flow change in the same change).
6. **Parallel execution**, in the same message, at most 5 agents: `pp-en:canvas-agent`,
   `pp-en:automate-agent` or `pp-en:sql-agent`, each with `RAIZ`, `KIT` and `MUDANCA` (the CHG path
   and the section of its spec). Model: `modelos.py de <agent>`. Identity change (color, font,
   navigation): the spec includes `ux-design-system.md` and the `App.Formulas` tokens.
7. **Judge each deliverable** (`subagents.md`, "Judging the deliverable"): the layer's validator at
   `0 error(s)`, spec × deliverable, alerts. Verdict in section 4 of the CHG; revision with the
   request tightened, at most two; the third is escalated.
8. **The change's QA:** `pp-en:qa-agent` with scope = the changed files and what depends on them (from
   step 4). Model: `modelos.py de qa-agent`. Reopen the strongest findings before believing them.
   A high finding: revision for the layer's agent.
9. **Paste into the development environment** (checkpoint `Action in the environment`, 🔴): flows
   first, tokens if they changed, then the screens; the procedure goes to the DBA. Error: back to
   the layer's agent.
10. **Test in the environment** (🔴): the QA script for the requests; if permissions were touched,
    denial by role and by unit. "Type 'all passed' or what failed."
11. **Synthesis** in section 6 of the CHG and in the chat (summary from `output-format.md` §1):
    delivered, verified, reviewed, with you, out.

## Exit gate

- [ ] Every request has a destination: accepted, escalated to the user or out (large), in section 2 of the CHG.
- [ ] Validators of the touched layers at `0 error(s)`; the change's QA with no high finding open.
- [ ] Pasted and tested in development, or the pending item written in the CHG.

## Closing

- **With `STATE.md` and something pasted in the environment:** `estado.py reabrir uat --motivo "CHG-<NNN>: <k> requests"`.
  UAT and publishing reopen; the next step is `/pp-en:uat`, which covers the change's requests and
  goes out as a new version in production.
- **Without `STATE.md`:** promotion follows `KIT/skills/power-platform/references/alm-environments.md` §10.
- Commit if `git_commit_por_etapa`: `pp(change): CHG-<NNN> <summary>`.
- The summary and the "Next step" block the script printed (with `STATE.md`).
