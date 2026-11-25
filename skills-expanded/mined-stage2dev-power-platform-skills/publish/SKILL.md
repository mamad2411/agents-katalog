---
name: publish
description: "Use when the Power Apps app's UAT has been approved and it is time for stage 10, the last of the pipeline: go-live checklist, documentation (user manual by role, technical guide) and the production release guided step by step, with a smoke test. Do not use before /pp-en:uat passes, nor to move a one-off fix between environments (describe it to the `power-platform` orchestrator)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:publish — Publishing and documentation

Stage 10 of the pipeline, block **4. Validation and delivery**. It ends with the app in production,
documented for those who use it and for those who maintain it.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Promotion: `KIT/skills/power-platform/references/alm-environments.md` §10 (procedure) and §11 (literals).

## Before you start

1. `estado.py comecar publish`. Exit 1: show the output and stop.
2. Read `prd.md`, `screen-inventory.md`, `architecture.md`, `GOAL.md` and the latest `docs/qa/UAT-*.md`.
3. **Reopened by a change** (`CHG-<NNN>` in the reason): it is a new version. Checklist and documents
   only for what the change altered (the manual, if usage changed; the technical guide, if the
   contract or database changed); the tag bumps the version (`v1.1.0`); the `CHG` becomes "published".

## Steps

1. **Go-live checklist** in `docs/delivery/GO-LIVE-CHECKLIST.md`, each item with an owner and a status:
   - solution version;
   - production environment variables;
   - connection references and service accounts;
   - access for real users (groups, roles, flags; nobody with permission by default);
   - data load, if any;
   - rollback plan (previous solution version, data);
   - communication to users and support channel.
2. **Documentation** in `docs/delivery/`:
   - `user-manual.md`: one chapter per role, the step by step of each P0 task, what each error
     message means and who to ask for help. Use the language of the screen, no technical jargon;
   - `technical-guide.md`: data track and ADRs, tables and procedures (from `AS-BUILT-NAMES`), each
     flow with its contract, where the log is, how to promote a fix, the validators and what each
     one does not cover.
3. **No environment literal:** `grep -rnE "dev[A-Z_]|[0-9a-f]{8}-[0-9a-f]{4}-" <config folders>`
   finds no server, no `dev*` table and no GUID in the delivery artifacts (`alm-environments.md` §11).
4. **Publish** (checkpoint `Action in the environment`, 🔴), step by step from `alm-environments.md` §10:
   import the managed solution into production, fill in the variables, connect the connections, share
   the app with the user groups, turn on the flows. "Type 'done' or the error."
5. **Smoke test** (checkpoint `Review`): with one real user of each role, open the app, query and do
   **one** agreed test write; check the flow log. "Type 'passed' or what failed." Failed: go back to
   step 4 with the rollback plan at hand.
6. **Milestone:** if `git_commit_por_etapa`, commit `pp(publish): go-live` and tag `v1.0.0`.

## Exit gate

- [ ] Go-live checklist with every item done or with an accepted risk (owner and date).
- [ ] User manual and technical guide written.
- [ ] Published in production and the smoke test passed.

## Closing

1. `estado.py concluir publish --nota "go-live on <date>; smoke ok"`.
2. Summary: where the app is, where the documents are, who gives support, and the final block the
   script printed (🎉 App published).
