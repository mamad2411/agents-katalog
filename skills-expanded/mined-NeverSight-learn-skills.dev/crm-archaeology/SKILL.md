---
name: crm-archaeology
description: >-
  Study a live Dynamics 365 / Dataverse environment end-to-end and produce one
  ARCHITECTURE.md — pull every customization to disk (solutions, entities, forms,
  JS and React web resources, PCF controls, classic workflows, plugins, cloud
  flows, classic RibbonDiffXml AND modern commands, security roles, embedded
  Power BI), map every business entity (standard AND custom), then trace the
  business processes layer by layer. Use whenever the user wants to learn,
  study, understand, reverse-engineer, audit, or document an existing
  Dynamics 365 / CRM / Dataverse org or model-driven app — "how does this CRM
  work", "document my D365 org", "learn the business logic of this
  environment", "what does this solution actually do", onboarding to a
  customer's CRM, or scoping a migration/rebuild. Read-only by design — it
  never writes to the org. NOT for building or changing CRM components (use the
  dataverse plugin skills) or for studying a plain source-code repo (use
  drive-to-legacy).
effort: max
---

# CRM Archaeology — study a live Dynamics 365 org, end to end

A live CRM org is unreadable in the browser, but almost everything in it can be
pulled to disk as plain text. So the method is three stages:

```
EXTRACT (steps 1–7: org → files + fragments)  →  STUDY (steps 8–9: connect the
layers into business processes)  →  DOCUMENT (step 10: one ARCHITECTURE.md)
```

Every command and query this skill relies on is in this skill's
`references/extraction-queries.md` (verified against Microsoft Learn, June 2026). Read the relevant section of that
file when you reach each step — do not improvise queries from memory; Dataverse
metadata endpoints have non-obvious casing, casting, and join-key rules that the
reference encodes.

## Hard rules

1. **Read-only.** This skill exports, GETs, and reads. It never creates,
   updates, or deletes anything in the org via the API, a script, or `pac`. The
   single sanctioned exception is the step-9 lifecycle walk-through, where a
   test record may be created **through the app UI** — by the user, or by you
   only with their explicit consent, and only in a sandbox. If the study
   reveals something worth fixing, file it as a finding — do not fix it inline.
2. **Confirm the environment before the first call.** Show the user the
   environment URL and ask them to confirm (`pac org who` to verify). Prefer a
   SANDBOX. Never assume the active `pac` auth profile is the right target.
3. **Fragments, not one giant pass.** Each step writes its output into the
   study workspace as it finishes. The study must be resumable — stopping after
   step 4 today and continuing tomorrow is a normal way to run it.
4. **No speculation in the output.** Document only what the extracted files and
   queries show. Unclear behavior is recorded as unclear.

## Step 0 — Scope gate (always first)

Ask the user (one message, not an interview):

1. **Environment** — which org URL? Confirm it; prefer sandbox.
2. **Depth** — **quick pass** (steps 1–4 + a reduced doc: entity map +
   automation inventory — enough to understand the business shape, ~hours) or
   **full study** (all steps, may span days)?
3. **Workspace** — where to put the study folder (default: `./crm-study/`).

Then verify tooling: `pac` installed and authenticated (`pac org who`). If the
`dataverse` plugin is installed, its `dv-connect` skill owns setup/auth — hand
off to it rather than improvising. Web API calls need a bearer token; reuse the
project's existing auth helper if one exists.

Create the workspace and `git init` it:

```
crm-study/
  src/            # unpacked solution(s) — the extracted "codebase"
  src-yaml/       # pac solution clone output (only if cloud flows / Power Fx commands exist)
  fragments/      # one file per step: 02-entities.md, 04-automation.md, ...
  ARCHITECTURE.md # assembled at the end
```

Git matters beyond hygiene: re-running step 1 later and reading `git diff` is
the cheap "what changed in the org since the last study?" drift check.

## Steps 1–7 — Extract

Work through these in order the first time; after step 1 lands, steps 2–7 are
independent of each other and can run as parallel subagents (give each its
reference section and the workspace path; each writes only its own fragment).

| Step | What it captures | Fragment |
|---|---|---|
| 1. Solution export | Everything to disk: web resources, PCF controls, FormXml, RibbonDiffXml, workflows-as-XAML, plugin DLLs. YAML clone too if cloud flows / Power Fx commands exist. **Checkpoint: show the user what landed before going deeper.** | `01-inventory.md` |
| 2. Entity universe | Every table the business uses — union of four sources: app components, sitemap (also keep the Area/Group names: they are the business taxonomy and the doc's chapter list), standard tables with custom columns, record counts/usage. Then expand outward via lookups to catch child entities never shown in navigation. | `02-entities.md` |
| 3. Data model | ERD edges, data dictionary, every option-set value with label — the labels ARE the business vocabulary. | `03-data-model.md` |
| 4. Server automation | `workflow` table by category (classic / business rule / action / BPF / cloud flow) + plugin steps + webhooks. Every item: trigger → behavior → **why the business needs it**. | `04-automation.md` |
| 5. Client-side logic | Form → event → `library.function` map from FormXml; web resource inventory; PCF vs HTML-hosted React; minified-bundle grep for the tables each React app touches. | `05-client-side.md` |
| 6. Command bar | BOTH generations: classic RibbonDiffXml (including the easy-to-miss Application Ribbons component) and modern `appaction` commands (Power Fx lives in the command component library `.msapp`, not in the row). | `06-commands.md` |
| 7. Security | Roles (≈ personas), BU tree, field security, which roles can use which app. | `07-security.md` |

For each step, the exact commands, queries, parsing targets, and the gotchas
that silently produce wrong results (join keys, label languages, type casts,
24-hour-stale counts) are in the matching section of `extraction-queries.md`.

**Conditional step 7b — embedded Power BI.** Detect deterministically, not by
clicking around: dashboards are `systemform` rows with `type eq 0` — scan their
`formxml` for Power BI markers (see the reference's step 7b). When found, the
analytics logic lives in a Power BI semantic model outside the solution export:
record which reports are embedded and which Dataverse tables feed them into
`fragments/07b-analytics.md`; if the `pbi-cli` skills are available,
`power-bi-docs` can document the model itself.

## Steps 8–9 — Study (this is the actual learning)

**8. Verify the static maps against the running app.** The extracted files say
what is *registered*; the app says what *runs*. Two built-in tools close the
gap: **Monitor → FormEvents** (catches JS handlers registered dynamically in
code, which FormXml never shows) and **Command Checker** (`&ribbondebug=true`
on the app URL — the authority on the merged classic+modern command bar).
Reconcile differences into the fragments.

**9. Trace business processes end to end.** For each key entity (start from the
sitemap's main work areas, not the master-data ones), connect the layers into a
lifecycle:

> who creates it (role, step 7) → which form + JS validates and cascades
> (step 5) → which buttons act on it (step 6) → which automation fires on save
> (step 4) → which status transitions exist (statuscode labels, step 3) → what
> downstream records appear.

Walk the app to confirm each lifecycle — a test record makes the cascades and
automations visible (watch what auto-populates, check audit history). Per hard
rule 1, the test record is created **through the app UI**, by the user or by
you only with their explicit consent, and only in a sandbox — never via the
API or `pac`. Write each lifecycle as a user story with a mermaid
`sequenceDiagram` into `fragments/09-processes.md`. This step is sequential by
nature — it needs all the fragments.

## Step 10 — Assemble the document

Build `ARCHITECTURE.md` from the fragments following this skill's
`references/architecture-template.md`.
The template implements the marketplace diagram convention
(`references/diagram-convention.md`).
The template's reading order puts user stories first (they answer "why does
this org exist") and enforces the one rule that makes the doc useful: **every
automation, API, and command entry carries a Why row** — what breaks without
it. Show the user the assembled doc; offer the drift-check habit (re-run step 1
periodically, `git diff`, feed changes to `management-talk` for reporting).

## Common mistakes

| Mistake | Fix |
|---|---|
| Filtering entities by `IsCustomEntity eq true` only | Most of the business lives in customized *standard* tables. Use the four-source union of step 2. |
| Reading only per-entity RibbonDiffXml | Global buttons live in the Application Ribbons component (must be added to a solution to export); modern buttons live in `appaction` rows. All three or the map is wrong. |
| Trusting FormXml as the complete JS map | Handlers added via `addOnLoad`/`addOnChange` in code never appear there. Cross-check with Monitor → FormEvents (step 8). |
| Treating the XML unpack as complete | Cloud flows and Power Fx command logic only decompose in the YAML clone (`pac solution clone`). |
| Skipping the Why on automation entries | A trigger list without business purpose is an inventory, not documentation. Every entry: what breaks without it? |
| Writing to the org "just to test something" | Never via API/script/`pac`. The only sanctioned write is the step-9 UI test record — user-consented, sandbox-only. Read-only is the contract that makes this skill safe to run against any environment. |

## Sibling skills

- `drive-to-legacy` — same discipline for a plain source repo; if step 5 turns
  up the React app's original source repository, switch to it for that part.
- `dataverse:dv-connect` / `dv-query` — auth/setup and ad-hoc data reads if the
  dataverse plugin is installed.
- `power-bi-docs` (pbi-cli) — documents embedded Power BI models (step 7b).
- `fit-gap-analysis` — consumes the fragments as the ready-made "as-is" side.
- `debug-mantra` — uses `04-automation.md` + `05-client-side.md` as the layer
  map when tracing a CRM bug.
- `seed-dataverse-data` — its duplicate-row guardrail scan is answered by
  `04-automation.md`.
