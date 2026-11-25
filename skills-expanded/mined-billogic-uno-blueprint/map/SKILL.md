---
name: map
description: Service blueprints — create one from service docs or discovery research, mapping how the service actually runs; import or translate a FigJam, Figma, Miro or spreadsheet blueprint; present, update or redeploy a blueprint workspace (a directory holding blueprint-workspace.json or blueprint/). Journey maps and frontstage/backstage swimlanes count. Present-tense gaps → ub:audit; hypothetical changes → ub:whatif.
---

# Service Blueprinting

Takes an org from scattered service documentation (or nothing at all) to a
**deployed, evolving service blueprint**: ingest docs, co-create from
conversation, translate foreign blueprints, review with hash-bound sign-off,
import via a backend adapter (no-DB fallback or Supabase), present with the
bundled React template, and update in place. A blueprint touched once is a
failure; touched monthly is the product.

Paths resolve against the plugin root (`${CLAUDE_PLUGIN_ROOT}` in Claude Code) or the workspace root, per `AGENTS.md`.

## The workspace

Everything revolves around one canonical artifact and one state file, both
git-tracked in the org's **workspace** (a clone of this template):

- `blueprint/*.json` — the **IR**: human-editable JSON mirroring the data
  model, validated by `references/ir-schema.json`. JSON is the supported
  authoring format (the scripts are stdlib-only; `.yaml`/`.yml` is read only
  if PyYAML happens to be installed). Text fields are locale maps
  (`{en: …, zh: …}`); every entity has a stable key that UUIDs derive from,
  so re-imports are idempotent.
- `blueprint-workspace.json` — per-scenario status + sign-off hash,
  per-locale targets, schema_version. Spec: `skills/map/references/workspace-state.md`.

Pipeline: `sources → IR → validate → review/sign-off → import (adapter) →
build check → deploy`, then the update loop re-enters at ingest or import.

## Entry-state detection (do this first)

Inspect the target directory before doing anything: does
`blueprint-workspace.json` exist? A `blueprint/` dir? A template clone? What
do the statuses say? (The SessionStart hook summarizes this when present.)
Then route:

| Entry state | Route | Read first |
| --- | --- | --- |
| Nothing — no docs, no workspace | Scaffold workspace (confirm directory!), co-create | `skills/map/references/cocreate-playbook.md` |
| Prose/service docs exist | Scaffold, then ingest | `skills/map/references/ingest-playbook.md` |
| Foreign structured blueprint (FigJam/xlsx/Shostack/Miro export) | Scaffold, then translate via crosswalk | `skills/map/references/translate-playbook.md` |
| Existing template clone, no IR yet | Ask: ingest or co-create | playbook per answer |
| Stale clone (schema_version mismatch vs plugin/template) | Upgrade recipe before any content work | `references/customization.md` |
| Mid-pipeline (workspace state shows drafted/unreviewed scenarios) | Resume at the first unmet exit condition | `skills/map/references/review-import-playbook.md` |
| Imported, never deployed (scenarios `imported`, `deploy_url` null) | Public-exposure warning → build gate → deploy | `skills/map/references/deploy-notes.md` |
| Deployed, needs update | Delta edits/docs → IR → re-sign-off → re-import → redeploy | playbook for the delta + `skills/map/references/review-import-playbook.md`, `skills/map/references/deploy-notes.md` |
| Inherited workspace (state file present, unknown provenance) | Read state + `HANDOFF.md`, verify sign-off hash, resume | `skills/map/references/workspace-state.md` |

Read the routed playbook before executing its phase; it carries the gates.

Decline early what this isn't for: org charts, gantt charts, non-journey
diagrams, real-time multi-user editing — point elsewhere rather than bend
the model.

## Hard rules

Everything in this skill is guidance you may adapt to the org — **except
these, which are where the system actually breaks**:

- ⚠ **REQUIRED — validate before import.** Run `scripts/validate_ir.py` and
  require exit 0 before any adapter runs. It catches what the DB trigger
  would abort mid-import (cells without path_steps, a dependency end that
  names no cell of this service, duplicate columns, a lane role outside the
  closed eight).
- ⚠ **REQUIRED — import only signed scenarios.** Import only scenarios whose
  recorded `content_hash` matches the current subtree, recorded after the
  user explicitly approves the preview — `skills/map/references/workspace-state.md`
  § Sign-off.
- ⚠ **REQUIRED — draft journeys only from journey docs.** Manuals and
  feature inventories describe the system; they route to co-creation as
  reference material (the ingest playbook's critical branch).
- ⚠ **REQUIRED — secrets** follow `references/adapter-contract.md` §7; a
  pre-write hook enforces the committable-file half.
- ⚠ **REQUIRED — confirm the target directory before writing anything**
  (scaffolding, IR files, generated artifacts), and the import target
  (project ref / output paths) before any import.
- ⚠ **REQUIRED — backend choice is the user's:** ask, per locale —
  `references/adapter-contract.md` §1.

## Deterministic exit conditions

Every phase ends at a quantitative stop condition.
Check them against `blueprint-workspace.json`, which is also what makes
long unattended runs ("all 6 scenarios signed off") verifiable:

| Phase loop | Exit condition |
| --- | --- |
| Ingest / co-create / translate a scenario | `scripts/validate_ir.py` exit 0 + scenario marked `drafted` in workspace state |
| Review | `blueprint-reviewer` findings resolved + sign-off hash recorded |
| Import | Transaction committed + read-back verification counts match the IR |
| Present | `tsc --noEmit` + `vite build` exit 0 + `render-checker` confirms every scenario renders |

## Agents

Pilot `document-reader` on a few docs before a whole corpus. Per-scenario
locale translation fans out to generic subagents.

Updating a deployed blueprint, a chain question ("what else does this edit
touch?") goes to `impact-tracer`, seeded with the edited cells, on the
export of the whole service (reach: CONTEXT.md **Dependency**). An
affected cell it reports in another scenario puts that scenario's cells in
the delta's review, named with their scenario and path.

## References

| Read when | File |
| --- | --- |
| Running the co-creation conversation | `skills/map/references/elicitation-protocol.md` (question script + right-sizing branches) |
| Writing or checking IR structure | `references/ir-schema.json`; model background in `references/data-model.md` |
| Assigning swimlane roles / divider lines | `references/lane-roles.md` |
| Drafting multiple phases consistently (customer spine per phase, shared actor labels) | `references/lane-vocabulary.md` |
| Building a translation mapping | `skills/map/references/crosswalk-schema.json` |
| Anything touching an import target | `references/adapter-contract.md` |
| Reading/writing workspace state or sign-off | `skills/map/references/workspace-state.md` |
| Before anything goes public; deploy gotchas | `skills/map/references/deploy-notes.md` (⚠ public-exposure warning lives here) |
| Template upgrades, lane roles, portfolio/client conventions, theming | `references/customization.md` |
| Generating the workspace handoff doc | `assets/HANDOFF.md.template` |

Correctness-critical steps (validation, seed-SQL/fallback generation,
UUIDv5 derivation) live in `scripts/` — execute them, never improvise their
logic in-context.
