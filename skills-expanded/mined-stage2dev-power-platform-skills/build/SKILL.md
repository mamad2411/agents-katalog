---
name: build
description: "Use when the Power Apps architecture is ready and the environment has AS-BUILT-NAMES filled in, for stage 7 of the pipeline: builds the next wave of GOAL.md with the Power Apps Canvas Agent (screens, components, Power Fx) and the Power Automate Agent (flows, approvals, notifications, errors) in parallel, checks the app↔flow integration and guides the paste into the environment. With `app` or `flows`, runs only one agent (a fix coming from testing). Do not use before /pp-en:architecture, or for a one-off tweak outside the pipeline (use `powerapps-canvas` or `power-automate`)."
argument-hint: "[app|flows]"
user-invocable: true
disable-model-invocation: true
---

# /pp-en:build — Power Apps Canvas and Power Automate Agents

Stage 7 of the pipeline, block **3. Building on the Power Platform**. Each session builds **one wave**
of `GOAL.md`: the two agents work in parallel, you check the integration and the user pastes into the
environment. The stage only closes when the last wave closes.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Queue and evidence: `KIT/skills/power-platform/references/goal-queue-mode.md`.

## Before you start

1. `estado.py comecar build`. Exit 1: show the output and stop.
2. **Who works:** `$ARGUMENTS` = `app` (Canvas only), `flows` (Power Automate only) or empty (both).
3. **Environment gate.** Read `power-platform.config.json` (`nomes_as_built`) and open
   `AS-BUILT-NAMES`. Missing, empty or without the tables the wave uses: checkpoint `Action in the
   environment` with wave 0 of `GOAL.md` (what to create, who creates it, how to capture the names)
   and **stop**. Writing a screen on guessed names is the number 1 cause of rework.
4. **What to build:**
   - stage *reopened* with `docs/qa/fixes.md`: only the open items of the requested layer (fix mode);
   - otherwise, the **first wave** of `GOAL.md` with an undone 🟢 task and the previous wave's gate closed.
   Show the wave: tasks, screens and flows.
5. **Contract closed?** Each flow in the wave has its parameters (positional, text) and the return
   `{status, description, id, url}` in `architecture.md`. Missing: write it now, before the agents.

## Steps

1. **Split the wave** by files (Files column of `GOAL.md`), never two agents on the same file:
   - screens in groups of up to 3, one `pp-en:canvas-agent` per group. The tokens (`App.Formulas`,
     `App.OnStart`, first wave only) belong to a single agent, the one that gets `TOKENS: yes`;
   - flows in groups of up to 3, one `pp-en:automate-agent` per group;
   - fix: `app` items go to Canvas; `flows` items for a flow go to Automate and for a procedure to
     `pp-en:sql-agent` (`CORRECOES`);
   - at most 5 agents per message; the rest goes in a second batch, after judging the first.
     Small wave (up to 3 screens and 3 flows): one of each.
2. **Agents in parallel**, in the **same message**:
   ```
   ◆ Calling 3 agents in parallel...
     → Power Apps Canvas Agent #1: Home, Orders, Detail
     → Power Apps Canvas Agent #2: Register, Report
     → Power Automate Agent: wave <n> flows
   ```
   - `pp-en:canvas-agent` with `RAIZ`, `KIT` (the value of `${CLAUDE_PLUGIN_ROOT}`), `TELAS` (the
     group's screen tasks) and `TOKENS` (yes or no), or `CORRECOES` (`app` items);
   - `pp-en:automate-agent` with `RAIZ`, `KIT`, `FLUXOS` (the group's flow tasks) or
     `CORRECOES` (`flows` items for a flow);
   - `pp-en:sql-agent` with `RAIZ`, `KIT` and `CORRECOES` (`flows` items for a procedure), only in fix mode.
   Each one's model: `modelos.py de <agent>` (empty line: do not pass `model`).
3. **Judge the deliverables and the app ↔ automation integration** (you yourself, not an agent;
   `KIT/skills/power-platform/references/subagents.md`, "Judging the deliverable"):
   - `python "${CLAUDE_PLUGIN_ROOT}/skills/powerapps-canvas/scripts/validar-telas.py"` and
     `python "${CLAUDE_PLUGIN_ROOT}/skills/power-automate/scripts/verificar-fluxo.py"`, from the root:
     `0 error(s)` and files read > 0 (procedure fix: also
     `python "${CLAUDE_PLUGIN_ROOT}/skills/sql-procedures/scripts/lint-procedure.py"`);
   - each `.Run(` in the screens has the contract's number and order of parameters
     (`grep -n "\.Run(" <screens-folder>`);
   - each screen handles the return: `.Run()` inside `IfError`, success = `status <> "error"`, toast
     with `description`, `Refresh` after writing;
   - table and column names in the screens and flows exist in `AS-BUILT-NAMES`
     (`grep -n "<name>" <AS-BUILT-NAMES>`).
   Whatever fails goes back to the layer's agent as a revision (the item, the file, the output). One
   verdict per agent (`--agente canvas-agent#1`, `automate-agent`...):
   `estado.py veredito build --agente <name> --resultado <...>`.
4. **Paste into the environment** (checkpoint `Action in the environment`, 🔴). Merge the two agents'
   instructions into a single step by step, in this order:
   1. flows first: create the trigger by hand with the parameters in order, paste the scope, relink the
      connections, save and test with the test data;
   2. `fx*` tokens in `App.Formulas` (first wave only);
   3. screens: select the screen, **Paste code**, add the flow to the app, run.
   "Type 'done' or paste the error message."
5. **Error on paste:** diagnose with the layer's skill (`powerapps-canvas` or `power-automate`) and
   send it back to the layer's agent as a revision, with the exact message from Studio or the designer
   and the file line; you do not edit the screen or the flow. A message the layer's skill does not
   explain: first, `pp-en:research-agent` with the exact message (`ONDE: both`, `PARA QUE: corrigir
   a colagem`; model:
   `modelos.py de research-agent`), and the findings go along in the revision. Then repeat step 4. Two failures for the
   same cause: escalated (stop, record it in `GOAL.md` and tell the user what was tried).
6. **Update the queue:** each task in the wave becomes ✅ with evidence (command + last line of the
   validator + "pasted on <date>"). Fix: mark the item as `done` in `docs/qa/fixes.md`.

## Wave exit gate

- [ ] Both layers' validators at `0 error(s)`, files read > 0.
- [ ] Contract checked: parameters, return and real names.
- [ ] User pasted and tested with no error; evidence in the `GOAL.md` column.

## Wrap up

- **A wave is still ahead:** do not conclude the stage. Show the queue progress (waves done /
  total) and run `estado.py proximo`: it points to `/pp-en:build` again, in a new session.
- **Last wave or fix finished:** `estado.py concluir build --nota "<N> waves; <screens> screens, <flows> flows"`.
- Commit if `git_commit_por_etapa`: `pp(build): wave <n>` (or `fixes <app|flows>`).
- Summary and the "Next step" block the script printed.
