---
name: clone
description: >
  Reverse-engineer a Bubble.io app export (a .bubble file) into complete AS-IS technical
  documentation plus a PRD to recreate the system as a functional clone. Covers: DATABASE
  (tables, fields, relationships, option sets, privacy rules), EXTERNAL APIs (API Connector
  providers, endpoints, auth, which are in use), PLUGINS (purpose, which hold API keys, which
  external service each talks to), DATA API exposure (which tables/methods are public),
  BACKEND WORKFLOWS (exposed endpoints vs internally-scheduled, the logic of each), PAGES
  & REUSABLES (what the system does, the business rules implemented in each workflow — the
  as-is state), and CREDENTIAL PRESERVATION (every API key/private config value from
  settings.secure extracted by script into secrets/.env + ENV-KEYS.md so the rebuild agent
  can configure the new system later — keys are never lost). Use WHENEVER the user hands you
  a .bubble export and asks to document the app, understand it, extract its schema/APIs/logic,
  pull its API keys into a .env, or produce a PRD/spec to rebuild or clone it:
  "document this Bubble app", "documentação técnica do app", "o que esse sistema faz", "regras
  de negócio", "clonar o sistema", "PRD para recriar", "reverse engineer", "as-is", "levantar
  requisitos do Bubble". Step 2 of the UnBubble pipeline — ideally run on the LEAN re-export
  produced after cleaning with unbubble:audit; followed by unbubble:level-up (re-architecture
  + migration plan).
---

# UnBubble · clone — as-is documentation + clone PRD

**Pipeline position: step 2 of 3.** Input should ideally be the **lean** `.bubble` re-exported
after the owner deleted the dead entities found by `unbubble:audit` (running on a dirty export
works, but you will document garbage — warn the user if an audit was never done). Output feeds
`unbubble:level-up` (step 3).

The goal of THIS step is **fidelity, not judgment**: document what the system IS and produce a
PRD to recreate it **as a functional clone** (feature parity). Do NOT redesign, modernize, or
criticize the architecture here — that is `level-up`'s job. Record smells you notice in
`08-open-questions.md` as notes for step 3 instead.

**`<workdir>` is the project folder** `~/UnBubble-Projects/<app-id>/` (same folder the audit
uses; create it if this is the first step run for the app). Everything this skill emits lives
there: `inventory/`, `secrets/`, `docs/`, `PRD-clone.md`, `PARITY-MATRIX.md`.

## Workflow

### 1 · Extract the inventory + preserve the credentials (deterministic)

```bash
python3 scripts/bubble_inventory.py "path/to/export.bubble" --outdir <workdir>/inventory
python3 scripts/bubble_secrets.py   "path/to/export.bubble" --outdir <workdir>/secrets
```

**Connected mode** (`unbubble:connect`, optional): once the owner has merged the cleanup into
`test`, the lean export can come straight from the editor —
`python3 <connect>/scripts/fetch_export.py --app <app-id> --version test` (`<connect>` =
`skills/connect/` of the UnBubble checkout) — instead of a manual export. Either way, record the
source in `00-overview.md`: for a downloaded export its provenance sidecar `<export>.meta.json`
(version, `fetched_at`, `sha256`); for a manual one the file name and the date the owner exported it.

Both are dependency-free (Python 3.8+). The inventory emits nine JSON files and prints a
summary. Read `summary.json` first — it has counts and **security flags** (endpoints without
auth, endpoints ignoring privacy rules) you must surface in the docs.

`bubble_secrets.py` is NOT optional: the export is often the only place the app's API keys
still exist, and the inventory deliberately redacts them — without this step they are lost.
It preserves every credential/private config value (settings.secure: named service keys,
the API Connector private auth/params, plugin secure keys, Bubble Data-API tokens, OAuth
apps, mobile signing; plus plugin client-safe config) into:

| File | Contents |
|---|---|
| `secrets/.env` | every value, commented with its export path — **live credentials**, chmod 600, gitignored; you never open it |
| `secrets/.env.example` | same vars blanked — safe to commit in the rebuild repo |
| `secrets/ENV-KEYS.md` | the map var ↔ export path ↔ service ↔ test/live ↔ in-use (no values) — **this** is what you read and cite |

The script prints a leaf-accounting line and exits non-zero if any secure value escaped
extraction — if it fails, stop and investigate before proceeding.

| File | Contents |
|---|---|
| `summary.json` | app domain, counts, security flags |
| `database.json` | data types → fields (type, list-ness, reference target), privacy rules per role, Data-API exposure; `relationships` edge list |
| `option_sets.json` | every option set with options (display + db_value) |
| `api_connector.json` | providers → calls: name, method, URL (masked), publish_as (action/data), param key names, **used** flag |
| `plugins.json` | installed plugins: name, version, usage count, config/secure **key names only** |
| `data_api.json` | Data/Workflow API global switches + exposed tables |
| `backend_workflows.json` | every backend WF: kind, endpoint name, expose, auth flags, params, action chain (types), schedule graph (`schedules_workflows` / `scheduled_by`) |
| `pages.json` | per page: title, content type, element census, workflows (trigger + editor-name label + action types), reusables/plugins/API calls used, nav targets |
| `reusables.json` | same census per reusable + `placed_instances` |

For export semantics (what ids mean, how references work, editor names), read
`../audit/references/reference-model.md` — do not re-derive it.

### 1b · Entities the owner KEPT on purpose in the audit (ask before documenting)

The audit report lets the owner sign a section off as *reviewed* without deleting every row.
Those unused-but-kept entities survive in the lean export, so the inventory will list them as if
they were live product features. BEFORE step 2, read
`<workdir>/audit/bubble_cleanup_progress__<app>.json` (or the `.md` export): the `kept` array
(`[{key, label, section}]`, keys like `workflow:<inner_id>`, `page:<id>`, `plugin:<id>`) is the
list of unused entities the owner chose to keep. If it is non-empty, ASK the owner (AskUserQuestion,
batches of up to 4, one question per item or per homogeneous group) what each one becomes in the
new system:

- **Parity** — it is a real feature: document it like any other entity (BR-xxx / PRD requirement,
  PARITY-MATRIX `REQ`/`BR-xxx`).
- **Operational tooling** — e.g. a bulk backend workflow used to fix data by hand: keep it OUT of
  the product docs and PRD, and record it in `08-open-questions.md` under "Ferramentas
  operacionais a recriar" so level-up turns it into an ops/maintenance task (PARITY-MATRIX
  `INFRA (ops task, decisão N)`).
- **Descoped** — it dies with Bubble: dated owner decision in `08-open-questions.md`, PARITY-MATRIX
  `DESCOPED (decisão N, YYYY-MM-DD)`, and it must not appear in PRD-clone as a requirement.

Record every answer as a dated decision (same "Decisões do dono (YYYY-MM-DD)" section as 3b). A
kept item without a disposition is a silent gap — the level-up gate (step 0) checks for them. If
there is no progress file, or its `kept` list is empty, skip this step and say so.

### 2 · Interpret business logic (model work — the part that matters)

The inventory gives structure; **you** extract meaning. The JSONs deliberately contain only
action *types* — for any workflow whose purpose isn't obvious from its trigger + action chain,
open the export itself with targeted python (never `cat` a 100 MB file) and read the action
`properties` to reconstruct the rule in plain language ("when a customer submits an order
above X, notify the account manager and set status to Pending Review").

Prioritize by impact, not page order:
1. **Backend exposed endpoints** (external contract — document every one: params, what it does,
   who calls it).
2. **Database trigger events + recurring events** (invisible automation — the rules nobody
   remembers).
3. The **top pages by workflow_count** and any page whose `content_type` is a core table.
4. Reusables placed on many pages (shared behavior).

For a big app (300+ pages), work in batches and consider subagents (one per module/folder);
group pages into functional modules by name prefix + nav graph (`navigates_to`) before writing.

### 3 · Write the documentation set

Write to `<workdir>/docs/`. Every file starts with a one-paragraph summary. Use tables, use
mermaid for diagrams, cite the source (`pages.json`, page name, workflow trigger) so claims
are checkable. English or the user's language — ask if unclear, default to the language the
user is speaking.

End `docs/00-overview.md` with one attribution line, in the docs' language:
`_Generated with [UnBubble](https://github.com/yowpi-tech/unbubble)._` (pt: `_Gerado com o
[UnBubble](https://github.com/yowpi-tech/unbubble)._`, es: `_Generado con
[UnBubble](https://github.com/yowpi-tech/unbubble)._`). Leave it out when the owner asks or the
environment sets `UNBUBBLE_NO_ATTRIBUTION=1` (check with `echo "$UNBUBBLE_NO_ATTRIBUTION"`),
the switch `bubble_audit.py` honours too. Add nothing else about UnBubble or its authors to the
docs: agencies hand these documents to their own clients.

```
docs/
  00-overview.md            what the system is, actors/roles, functional modules, key flows;
                            the source export (version, date, sha256 when downloaded)
  01-database.md            per table: purpose, fields table, relationships (mermaid erDiagram),
                            option sets used, privacy rules, Data-API exposure
  02-external-apis.md       per provider: what it's for, auth type, calls table (method, URL,
                            used?), which workflows/pages invoke it, and the ENV VAR names
                            holding its credentials (from secrets/ENV-KEYS.md)
  03-plugins.md             per plugin: purpose, external service, holds API keys? (the ENV
                            VAR names from secrets/ENV-KEYS.md), where used, marketplace link
  04-data-api.md            switches, exposed tables, what privacy rules imply for each,
                            security notes (from summary.security_flags)
  05-backend-workflows.md   endpoints (external contract) vs internal jobs; per WF: trigger,
                            params, logic in plain language, schedule graph
  06-pages-and-reusables.md per module then per page: purpose, content type, key elements,
                            workflows → business rules; reusables and where they're placed;
                            what each role sees, when screen captures exist (below)
  07-business-rules.md      cross-cutting rules extracted from all of the above, numbered
                            (BR-001 …) and written in VERIFIABLE form (see below)
  08-open-questions.md      ambiguities, suspected dead logic, smells noted for level-up,
                            anything requiring the owner's confirmation
```

#### What each role sees (connected mode, optional)

When the owner has captured the screens (`<connect>/references/screens.md`: test users per role on
`version-test`, `capture_screens.py`), link each page's captures per role in
`06-pages-and-reusables.md` (`visual/bubble/<role>/<page>.png`; `visual/INDEX-bubble.md` lists them,
with "no access in this role" where a page redirects) and write down what each role sees and can
do there: the information shown, the fields, the actions, the navigation. That is documentation of
CONTENT and ACCESS — never describe colors, layout or spacing from the captures; the rebuild gets a
new design system. Pages without a capture stay documented from the export alone.

#### Business rules must be verifiable, not merely descriptive

A rule an executor can "read past" is a rule that does not get built. Every **behavioural**
BR-xxx states an observable trigger→response, so it converts to a test with no translation:

> **BR-021 — Reembolso.** QUANDO um pedido pago é cancelado em até 7 dias, O SISTEMA DEVE
> estornar o valor integral e marcar o pedido como Reembolsado. _Aceite:_ cancelar no 7º dia
> estorna 100%; no 8º dia o pedido fica Cancelado, sem estorno. _(fonte: 06 Cancel Order; 05)_

- Use `QUANDO … O SISTEMA DEVE …` (or `WHEN … SHALL …`) plus an explicit `Aceite:` line.
- Keep the source citation — verifiability never replaces traceability.
- A rule that is pure context (a hierarchy, a glossary, an inventory) is **not** behavioural:
  mark it `[descritivo]` on the definition line so the level-up's coverage gate exempts it
  instead of demanding a test for it.

Same rule for the PRD's parity requirements: each is testable or it is not a requirement.

### 3b · Resolve open questions WITH the user (blocking gate — do NOT skip)

`08-open-questions.md` is not a parking lot: it is a question list for the owner. BEFORE writing
the PRD, ask the user every owner-blocking question you collected (use the AskUserQuestion tool
when available — batches of up to 4 questions with concrete options plus free-text "Other";
otherwise ask in chat). Then:

- Record each answer in `08-open-questions.md` under a dated **"Decisões do dono (YYYY-MM-DD)"**
  section — decisions are binding for the PRD.
- Propagate the answers into the affected docs (01–07) at the exact spots, citing the decision
  date, and adjust the PRD scope accordingly (descoped endpoints, authorized deviations, etc.).
- Only questions the user genuinely cannot answer now stay open — say so explicitly in 08 and in
  the PRD's out-of-scope section.
- Never deliver a PRD with silently unresolved blocking questions.

Classic blocking questions worth hunting for proactively: integrations **gated by a config flag
whose runtime value lives in the DATABASE** (the export shows the code path but cannot tell if it
is live — trace the flag, then ask the owner "is it on in production?"; a dormant route can
remove whole integrations and endpoints from the parity contract), endpoints kept only for
testing, external consumers not visible in the export (API tokens), and where any
"encryption"/token logic actually runs.

**Bring evidence to the question when connected mode is available.** Two of these have a runtime
answer in the live app, before asking: *does this exposed endpoint have external consumers?* (runs
of the backend workflow behind it) and *is the integration behind this flag alive?* (runs of the
workflow or the API Connector call on that path). Use `<connect>/scripts/runtime_evidence.py` —
`--source workload` counts workflow runs (Workflow API calls by endpoint name), the default reads
the server logs — for many candidates, or for one `bubble_workload_usage_breakdown` or
`bubble_logs_fetch` with `contains: "<workflow or call name>"` over 14–30 days, and put the counts
in the question ("the endpoint ran 1,284 times in 30 days — keep it in the parity contract?").
Counts only, never log rows. Runs and log rows answer "it runs"; silence only covers the window
(and, for logs, only after a workflow known to run came back: some apps answer every logs query
with zero rows), so the owner still decides — record the evidence next to the decision.

### Plugin policy (encode it in 03-plugins.md)

Classify every installed plugin as one of:

- **Frontend functionality** (rich-text editors, toasts, pickers, icons, masks/validations,
  QR/barcode rendering, JS utilities…) — in the rebuild these are **replaced by own code**.
  Document the observable behavior to reproduce; never propose "an equivalent plugin".
- **External-service integration** (talks to an outside API and/or holds credentials) — document
  the service and the ENV VAR names from `secrets/ENV-KEYS.md` (the values themselves are already
  preserved in `secrets/.env`); the keep × replace decision belongs to level-up's integration map.

### 4 · Generate the clone PRD

Write `<workdir>/PRD-clone.md`. This is the **first PRD** — recreate the system as-is on a new
platform. Structure:

1. **Purpose & scope** — what the clone must do; explicit non-goals (no redesign yet).
2. **Actors & permissions** — roles derived from privacy rules + page auth patterns.
3. **Functional requirements** — per module, referencing BR-xxx business rules; every exposed
   endpoint and Data-API table is a requirement (external consumers may exist).
4. **Data model** — the as-is schema (tables/fields/option sets) as the contract to reproduce.
5. **Integrations** — every external API + plugin-service the clone must reconnect. Cite the
   ENV VAR names per integration and state that the working values are preserved in
   `<workdir>/secrets/.env` (mapped by `ENV-KEYS.md`) — the rebuild configures from there
   instead of hunting for credentials.
6. **Parity checklist** — a testable list: pages/flows, endpoints, automations (DB triggers,
   recurring), reports/exports.
7. **Out of scope / deferred to level-up** — architecture choices, migration, UX changes.

### 4b · Parity traceability matrix (nothing exists without a disposition)

The PRD is narrative; **parity needs a ledger**. Write `<workdir>/PARITY-MATRIX.md`: one row per
inventory entity, each with exactly one disposition — a blank cell blocks delivery.

Rows come from `inventory/*.json`, **generated by script** (never hand-listed) so the row count
provably equals the inventory count per class — print both next to each section:

| Entity class | Source |
|---|---|
| page | `pages.json` |
| reusable that has workflows | `reusables.json` (workflow_count > 0) |
| exposed endpoint / internal backend WF / custom event / DB trigger | `backend_workflows.json` |
| data table | `database.json` |
| option set | `option_sets.json` |
| API provider call | `api_connector.json` |
| plugin | `plugins.json` |

Allowed dispositions (one per row): **`REQ <PRD §>`** (parity requirement) · **`BR-xxx`** (rule
that covers it) · **`DESCOPED (decisão N, YYYY-MM-DD)`** (dated owner decision — from the 3b
round) · **`UI-ONLY`** (pure presentation, nothing behavioral to reproduce — valid only for
pages/reusables/plugins) · **`INFRA`** (replaced by platform capability, say which).

The matrix is ALSO the executor's completeness checklist: at the end of the rebuild every row must
be checked off or carry an owner-signed deviation (level-up's `EXECUTION-CONTRACT.md` enforces
this). A dispositionless row means the clone missed something — go back before delivering.

### Secrets & PII hygiene (non-negotiable)

`settings.secure` holds LIVE API keys and `raw_data` on endpoints can hold real user data.
The division of labor is strict:

- **Values are preserved exactly once, by script**: `bubble_secrets.py` → `secrets/.env`
  (chmod 600, gitignored). That file is for the future rebuild agent's configuration step —
  **you never open, cat, print, or quote it**, and you never open the raw `settings.secure` /
  `raw_data` sections either. If the script failed, fix the script run; never extract values
  by hand.
- **Docs carry names, never values**: reference env VAR names via `secrets/ENV-KEYS.md`
  (safe to read — names, paths and lengths only). No credential-looking string ever appears
  in inventory JSONs, docs, the PRD, chat, or commits.
- Treat the whole `<workdir>` as internal material; `secrets/.env` additionally must never
  leave the machine (no cloud sync, no attachments, no artifacts).

## Quality bar

- Every active table and field appears in `01-database.md`; every provider call in
  `02-external-apis.md` (marked used/unused); every exposed endpoint in `05-…` with params.
- `secrets/.env` + `ENV-KEYS.md` exist (bubble_secrets.py ran and its leaf accounting passed);
  every integration in `02-…`/`03-…` and in PRD §Integrations cites its ENV VAR names; no
  credential value appears anywhere outside `secrets/.env`.
- Workflows are described as **rules in plain language**, not action-type lists.
- Every behavioural BR-xxx is in verifiable form (`QUANDO … DEVE …` + `Aceite:`); purely
  descriptive ones are marked `[descritivo]`. The level-up gate checks this.
- Anything you could not determine is in `08-open-questions.md` — no silent gaps.
- Numbers in `00-overview.md` match `summary.json` exactly, and it names the source export
  (version and date; sha256 when it came through the connected mode).
- `PARITY-MATRIX.md` has a script-generated row for EVERY inventory entity, each with exactly one
  disposition; its per-class row counts are printed next to the inventory counts and match.
- Finish by telling the user the docs + PRD-clone + PARITY-MATRIX are the input for
  **`unbubble:level-up`**.
