---
name: uat
description: "Use when the Power Apps app tests have passed and it is time for pipeline stage 9: take the app to the acceptance environment, generate the UAT script by role and record the acceptance of real users (who and when). Rejected, it sends the fix back to the build. Do not use before /pp-en:test passes, nor to promote to production (use `/pp-en:publish`)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:uat — User acceptance (UAT)

Stage 9 of the pipeline, block **4. Validation and delivery**. The testers now are the **real users**,
with data close to the real thing, in an environment that is not development. You prepare the script
and record the acceptance; the user runs the session with the people.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Promotion between environments: `KIT/skills/power-platform/references/alm-environments.md` §2-§5 and §10.

## Before you start

1. `estado.py comecar uat`. Exit 1: show the output and stop.
2. Read `docs/planning/prd.md` (roles, P0 requirements), the latest `docs/qa/QA-*.md` and the ALM
   section of `architecture.md`.
3. **Reopened by a change** (the reason in `STATE.md` cites `CHG-<NNN>`): read
   `docs/changes/CHG-<NNN>.md`. The UAT covers the change's requests (section 2) plus a short cycle
   of the main P0 requirement, to catch regressions; it does not redo the whole script.

## Steps

1. **Where to run UAT** (`AskUserQuestion`):
   - "Acceptance environment (UAT) (Recommended)";
   - "We have no UAT environment: accept in DEV".
   The second becomes an accepted risk in `docs/qa/UAT-<date>.md`, with who accepted it.
2. **Take the app to UAT** (checkpoint `Action in the environment`, 🔴), step by step from
   `alm-environments.md` §10: export the managed solution from DEV, import it into UAT, fill in the
   environment variables, turn on the connection references, give the test users access. "Type 'done'
   or the error."
3. **UAT script** in `docs/qa/UAT-<YYYY-MM-DD>.md`:
   - one block per role;
   - one scenario per P0 requirement: short steps and the expected result;
   - the data set and the test users (one per role, one from another unit);
   - room for `passed / failed / note` and for the signature (name or role, date).
4. **Session with the users** (checkpoint `Action in the environment`, 🔴): the user runs the UAT
   with the people and comes back with the filled-in script. `AskUserQuestion`:
   - "Approved";
   - "Approved with reservations that do not block";
   - "Rejected".
5. **Record** in `UAT-<date>.md` who approved and when. Reservations become ⬜ tasks in an
   "After go-live" section of `GOAL.md`.

## Closing

- **Approved (with or without reservations):** `estado.py concluir uat --nota "acceptance by <who> on <date>"`.
- **Rejected:** each problem in `docs/qa/fixes.md` with the layer (`app` or `flows`), then
  `estado.py reabrir build --motivo "UAT-<date>: <k> problems" [--argumento app|flows]`.
  Build, test and UAT reopen together.
- Commit if `git_commit_por_etapa`: `pp(uat): UAT-<date> <approved | rejected>`.
- Summary and the "Next step" block the script printed.
