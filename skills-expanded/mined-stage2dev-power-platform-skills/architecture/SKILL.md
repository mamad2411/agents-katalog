---
name: architecture
description: "Use when the Power Apps prototype has been approved and it is time for stage 6 of the pipeline: decide with the user the data track (Dataverse or SQL Server) and call the Architecture Agent, which writes the data model, permissions, integrations, the app↔flow contract, the data scripts and the GOAL.md build queue. Do not use before the prototype is approved, or for a single procedure or table (use `sql-procedures` or `dataverse`)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:architecture — Architecture Agent

Stage 6 of the pipeline, block **3. Building on the Power Platform**. You bring the user the one big
decision of the stage (where the data lives) and call the `pp-en:architecture-agent` agent, which turns
the PRD, inventory and prototype into a data model, permissions, integrations and the build queue.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.

## Before you start

1. `estado.py comecar architecture`. Exit 1: show the output and stop.
2. Read `docs/planning/prd.md`, `screen-inventory.md`, blocks 4, 7 and 8 of `brainstorm.md`,
   and `KIT/skills/power-platform/references/technology-matrix.md` and `default-decisions.md`.

## Steps

0. **Research, if a fact is missing** for the track: the PRD mentions a source that already exists
   (spreadsheet, database, system) with files in the project, or there is a doubt about licensing or
   limits. Call `pp-en:research-agent` with `ONDE: both`, `PARA QUE: escolher a trilha de dados`
   (model: `modelos.py de research-agent`). Judge it and use the sourced findings among the facts of
   step 1.
1. **Data track** (checkpoint `Decision`). Apply the matrix to the brainstorm answers and
   recommend **one** track, with the 3 facts that weighed most (volume above 2,000, SQL database that
   already exists, compliance, DBA, transaction across several tables). `AskUserQuestion`, the
   recommended one first:
   - "SQL Server + procedures";
   - "Dataverse";
   - "I need to confirm with IT".
   The third becomes a `D-xx` with owner and date in `prd.md`; the stage stays in progress. Say what to
   ask and whom, and stop: running `/pp-en:architecture` again resumes from here.
2. **Environment facts** the user already knows, in short questions with "I don't know": publisher
   prefix (Dataverse), server and database **by role only** ("DEV database"; never a real name in the
   file), who creates tables, whether there are DEV/HML/PRD environments.
3. **Agent.** Show `◆ Calling the Architecture Agent...` and call `pp-en:architecture-agent` with
   `RAIZ`, `KIT` (the value of `${CLAUDE_PLUGIN_ROOT}`), `TRILHA` and the facts from step 2.
   Model: `modelos.py de architecture-agent` (empty line: do not pass `model`).
4. **Judge the deliverable** (`KIT/skills/power-platform/references/subagents.md`, "Judging the deliverable"):
   - `power-platform.config.json` with `trilha_dados` (and `prefixo_publisher` on Dataverse);
   - `GOAL.md` with wave 0 (environment, 🔴) and the build waves, each task with "done when";
   - SQL track: every write in the contract has a procedure specified in section 4.1, with a group;
   - every P0 `FR-xx` appears in at least one `GOAL.md` task (traceability);
   - mockup load written: run
     `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/montar-carga-mockup.py" <spec>` yourself
     (on Dataverse, with `--flow`) and check `0 error(s)`, one sheet per model table, on SQL the
     `mockup-load.sql` and on Dataverse the `dataverse-plan.json` and the `dataverse-builder/` folder.
   Missing or an error: revision. An open question only the user can answer: escalated. Record it with
   `estado.py veredito architecture --agente architecture-agent --resultado <...> --motivo "..."`.
5. **Procedures in parallel** (SQL track only). One `pp-en:sql-agent` per group in section 4.1, all in
   the **same message**, each with `RAIZ`, `KIT` and `PROCEDURES` (the group's names); model:
   `modelos.py de sql-agent`. Judge each deliverable: `python "${CLAUDE_PLUGIN_ROOT}/skills/sql-procedures/scripts/lint-procedure.py"`
   over the procedures folder at `0 error(s)`, and each procedure with the parameters and codes from
   the spec. One verdict per agent (`--agente sql-agent#<group>`).
6. **Prepare the environment** (checkpoint `Action in the environment`, 🔴). Show wave 0 of `GOAL.md` as
   a step by step:
   - SQL: hand the package to the DBA or run the scripts in the DEV database, in the package's order;
   - Dataverse: ask with `AskUserQuestion` how the tables are created, the recommended one first:
     - "Dataverse builder (flow)": import `dataverse-builder/ConstrutorDataverse_1_0_0_0.zip`,
       create the connection and run the flow with the `dataverse-plan.json` and the solution name
       (`KIT/skills/power-platform/references/dataverse-builder.md`). It creates tables, columns with
       the spec's type, Choices, relationships, mockup rows and keys. It requires the HTTP with
       Microsoft Entra ID connector to be allowed and a customization role (§2 of the reference). Say
       that running it in a real environment has not been confirmed in the kit yet and show §9;
     - "Spreadsheet only": import `mockup-load.xlsx`, all sheets at once through Power Query
       (`KIT/skills/power-platform/references/mockup-load.md` §4), with the project publisher's
       preferred solution. **Tell the user in so many words:** Dataverse infers each column's type
       from the data and often gets it wrong. Choice and Lookup arrive as text. They check column by
       column (sheet `Type check`).

     On both paths, `montar-carga-mockup.py <spec> --conferir <export.json>` must give
     `0 error(s)` before any real data;
   - SQL: after the DDL, run `mockup-load.sql` **only in the DEV database**;
   - both: capture the real names in `AS-BUILT-ENVIRONMENT/AS-BUILT-NAMES.md`. On Dataverse, the
     `EntityDefinitions` export + `extrair-nomes-as-built.py` from the `dataverse` skill generates the file.
   Say this may take days (DBA, IT) and that **the build only starts with `AS-BUILT-NAMES` filled
   in**: `/pp-en:build` checks it before writing any screen.

## Exit gate

- [ ] Track ADR in `docs/decisions/ADR-001.md`; config and `00-READ-ME-FIRST.md` with the same track.
- [ ] `architecture.md` with data model, permission matrix (flags), integrations and the contract
      of each flow (positional parameters and return `{status, description, id, url}`).
- [ ] Data scripts ready (SQL with `lint-procedure.py` at `0 error(s)`; Dataverse with the table
      model and security roles).
- [ ] Mockup load for both tracks: `montar-carga-mockup.py <spec>` at `0 error(s)`, `.xlsx` written
      (and `.sql` on SQL; on Dataverse, also the plan and the builder); on Dataverse, the user chose
      builder or spreadsheet and was warned that they must check the typing.
- [ ] `GOAL.md` in waves, with traceability of every P0 FR.

## Wrap up

1. `estado.py concluir architecture --nota "<track> track; <N> waves in GOAL.md"`.
2. Commit if `git_commit_por_etapa`: `pp(architecture): model, contract and build queue`.
3. Summary (track, waves, what the human needs to do in the environment and with whom) and the "Next
   step" block the script printed.
