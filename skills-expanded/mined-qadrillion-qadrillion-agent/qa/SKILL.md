---
name: qa
description: Test a ticket, feature or bug end to end; resume a QA handoff or plan exploratory testing. Accepts tracker IDs and free text. Does not implement unrelated product features.
---

# QA orchestrator

First distinguish a question from requested QA work. A question is `quick`:
answer using relevant facts, without creating a ticket or loading execution
specialties. For QA work, continue below.

Use the shared contracts in `.agent/rules/`; read
`.agent/skills/qa-workflow/SKILL.md` once when starting QA.

1. **Locate state.** Read the requested ticket's frontmatter, if present. For
   free text, choose a collision-free `LOCAL-<number>` ID and `tracker: null`.
   Never invent a ticket description, build, connection, fixture or permission.
2. **Resolve capabilities.** Read `qa-config.json` and relevant manifest entries.
   Tools are optional. Choose an available tracker CLI/API/MCP or supplied ticket
   text; source repository or black-box interface; runner or manual session.
   Read `docs/reference/integrations.md` only when choosing/connecting a transport.
   If only an ID is supplied and no reader is available, persist the access
   blocker and ask for ticket text. Continue independent work when possible.
3. **Classify.** State `api`, `ui-web`, `mobile`, `backend`, `desktop`, `data`,
   `device`, `other`, `multi-surface` or `tooling`. Inspect repository status with
   `python3 tools/workspace/refresh.py --scope <scope>`; this does **not** fetch.
   Updates are explicit and occur before pinning the tested revision.
4. **Resume carefully.** Check owner/branch, source commit, build, target and
   config identity against the handoff. Preserve old evidence, mark what is stale,
   then resume the earliest affected step. A done ticket can start a new dated
   run; do not reuse its Pass for a different build.
5. **Select procedures and execute.** Read [routing](references/routing.md).
   Name the actual surfaces, selected specialties and risk reason in the plan.
   Load only their SKILL.md files, then the conditional recipe for the team's
   observed tools. A mixed task composes procedures around one state/evidence
   record; a missing runner limits that path, not the other surfaces. Continue
   through authoring, execution, diagnosis and handoff when capabilities exist.
   Use only workers that add value. For a meaningful code
   change, locate then review available source; without source, test the exposed
   contract and record the review gap. One agent can perform the same roles
   sequentially when subagents are unavailable. Pass workers a bounded task,
   paths/revisions and required contract, not the entire conversation.
   A skill supplies expertise; it is not a worker. The execution-only test-runner
   does not author tests. Author directly or assign a general worker a bounded
   test suite in a separate checkout, with the applicable specialist procedure.
6. **Persist and report.** One writer per checkout. Serialize ticket updates;
   do not dispatch competing writers. Prepare external comments locally. Publish
   within explicit task authorization and runtime permissions, without repeated
   approval for routine updates. Follow `tracker-reporting.md` for publication
   scope; a missing approval hook is not consent. Preserve posted IDs and reconcile an
   uncertain response before retrying a write.

Stop the affected action for unknown target identity, unavailable required access,
ambiguous acceptance criteria that change the oracle, or a spent error budget.
Do not block all useful QA because an optional tool, source checkout or test ID
is missing. Do not switch transport to evade a denial.

Output: scope; changes; source risks or review gap; tests/exploration; concise
results with artifact paths and relevant output; prepared/posted tracker state;
blockers; verdict `Pass | Partial | Fail`. Scope Pass to the agreed checks.
