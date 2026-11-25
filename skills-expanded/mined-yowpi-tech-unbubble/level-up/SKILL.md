---
name: level-up
description: >
  Re-architect a Bubble.io app for rebuild OUTSIDE Bubble with an engineering upgrade. Takes
  the as-is documentation + clone PRD produced by unbubble:clone and: assesses the current
  system against market best practices (tech debt, security posture, data-model quality,
  performance, maintainability), designs a state-of-the-art target architecture where
  INFORMATION SECURITY and RESULT RELIABILITY come first and UX/UI second, redesigns the data
  model where Bubble's structure is inadequate, and produces the Bubble→new-system DATA
  MIGRATION PLAN (CSV export/import vs consuming the Bubble Data API, cutover, validation).
  Output is an AI-ready rebuild pack (assessment, target architecture, frontend design brief, new
  data model + mapping, migration plan, PRD v2, backlog, risks). When the `enterprise-best-practices`
  skill is available it is applied as a production-readiness lens (13 layers + 5 business themes);
  otherwise the user is asked whether to install it. Use when the user asks to: "level up", "sair do Bubble",
  "migrar do Bubble", "recriar com melhores práticas", "modernizar o sistema", "upgrade de
  engenharia", "plano de migração", "reengenharia", "novo stack", "repensar o sistema",
  evaluate tech debt of a Bubble app, or plan the rebuild after unbubble:clone. Step 3 (final)
  of the UnBubble pipeline.
---

# UnBubble · level-up — re-architecture + migration plan

**Pipeline position: step 3 of 3.** Inputs: the `docs/` set + `PRD-clone.md` from
`unbubble:clone` (required — if missing, run clone first) and optionally the `.bubble` +
inventory JSONs for spot-checks. Output: a **rebuild pack** an AI (or team) can execute to
recreate the system on a new platform with an engineering upgrade.

All inputs and outputs live in the project folder `~/UnBubble-Projects/<app-id>/` (shared by
the whole pipeline): read `docs/` + `PRD-clone.md` from there and write the `levelup/` pack
next to them.

**Priorities, in order — never trade down:**
1. **Information security** and **reliability of results** (the system must be trustworthy:
   correct numbers, no data leaks, no silent failures).
2. **UX/UI** — preserved where good, improved where weak.
3. Everything else (cost, delivery speed, stack preferences).

## Workflow

### 0 · Gate: resolve open questions with the user FIRST

Read `docs/08-open-questions.md` before anything else. If any question that affects security,
architecture, data model or migration is still unanswered, ASK THE USER NOW (AskUserQuestion tool
when available, batches of up to 4 with concrete options + free-text; otherwise ask in chat) and
record the answers in 08 as dated owner decisions ("Decisões do dono (YYYY-MM-DD)"). Do not design
around an unanswered blocking question — an assessment built on guesses produces a rebuild pack
the owner has to redo.

Also check the audit's kept items: `<workdir>/audit/bubble_cleanup_progress__<app>.json` (`kept`
array) lists unused entities the owner deliberately kept when signing sections off. Every one of
them must already carry a disposition from the clone step (PARITY-MATRIX `REQ`/`BR-xxx`, `INFRA
(ops task, …)` or `DESCOPED (decisão N, data)`; decisions in `08-open-questions.md`). If the clone
ran before the sign-off existed, or a kept item has no disposition, ask the owner NOW — parity,
operational tooling (becomes an `[infra]` maintenance story in BACKLOG.md), or descoped — and record
the dated decision before designing. Descoped items never resurface in PRD-v2 or BACKLOG.md;
operational ones become stories in the migration/cutover epic, not product features.

### 0b · Load the production-gate lens (`enterprise-best-practices` skill)

The level-up is exactly a "day-0 architecture + production-readiness" moment, which is what the
**`enterprise-best-practices`** skill exists for (13 production layers + 5 business themes as
quality gates). Use it as a lens across the whole pack — assessment dimensions, target-architecture
day-0 decisions, and the backlog's readiness stories.

1. **Check availability.** If `enterprise-best-practices` is in this session's available-skills
   list, **invoke it now** (Skill tool) and carry its 13-layer / 5-theme gates into steps 1, 2 and
   5 — cite the layer next to the finding/story it drives.
2. **If it is NOT available, ASK the user** (AskUserQuestion when available) whether to install it,
   offering:
   - **Install it** — clone `https://github.com/yowpi-tech/enterprise-best-practices` into
     `~/.claude/skills/enterprise-best-practices` (a new interactive session then sees it); then
     invoke it.
   - **Proceed without it** — continue using only `references/assessment-checklist.md`; note in
     `ASSESSMENT.md` that the enterprise gates were not applied.
   Do not clone anything without the user's yes, and never block the level-up on it — it enriches
   the pack, it is not a hard dependency.

When applied, record in `ASSESSMENT.md` which layers/themes were checked, so the pack states its
own coverage.

### 1 · Assess the as-is system

Read `references/assessment-checklist.md` and score the current system against it. Ground every
finding in evidence from the clone docs / inventory (quote the table, endpoint, or workflow).
Deliver `ASSESSMENT.md`:

- Scorecard (1–5) per dimension: security, reliability/correctness, data model, performance,
  maintainability, UX. One paragraph of evidence per score.
- **Tech-debt register**: each debt item with severity, evidence, and what it costs the business
  (e.g. "all admins share one sentinel account → per-user audit impossible").
- **Security findings first-class**: start from `summary.json.security_flags` (endpoints without
  auth, endpoints ignoring privacy rules), Data-API over-exposure vs privacy rules, secrets
  handling, roles enforced client-side.
- What is **good** and must be preserved (flows users like, rules that encode hard-won domain
  knowledge). A rebuild that loses these is a regression.

### 2 · Design the target architecture

Deliver `TARGET-ARCHITECTURE.md`:

- **2–3 candidate stacks** with trade-offs, then ONE recommendation with justification tied to
  the assessment (team skills, app shape, integration list). "State of the art" means proven
  and appropriate for the case — not fashionable.
- **Security architecture** (priority 1): authn (managed IdP vs roll-your-own), authz model
  translating Bubble privacy rules → server-enforced policies (e.g. Postgres RLS or a policy
  layer), tenancy/hierarchy scoping, secrets management, audit logging, backups/DR, LGPD/PII
  handling.
- **Reliability architecture** (priority 1): typed schema with real constraints (FKs, unique,
  not-null), transactions where Bubble had multi-step workflows, idempotent jobs replacing
  recurring/DB-trigger events, input validation at the boundary, automated tests on the
  BR-xxx business rules, observability (structured logs, error tracking, metrics).
- **UX/UI plan** (priority 2): design system choice, which flows are kept as-is vs redesigned,
  accessibility and responsiveness baseline. Two recurring UX translations worth calling out:
  **theme (light/dark)** is CSS + client state (custom properties / `prefers-color-scheme`), never
  a DB enum/column — drop the Bubble theme option set and per-user theme field; and a **WYSIWYG
  HTML editor** is a candidate to become a **Markdown WYSIWYG** (e.g. Milkdown) when the owner
  wants Markdown as the canonical content — if so, plan the HTML→Markdown conversion in the
  migration (archive the original HTML) and render Markdown→HTML server-side for any PDF pipeline.
- Integration map: every external API/plugin-service from the clone docs → how the new system
  talks to it (direct SDK, webhook, queue) and its credentials plan. The working values were
  already preserved by the clone step in `<workdir>/secrets/.env` (map: `secrets/ENV-KEYS.md`)
  — decide per integration **reuse** (same account/key, renamed to the new stack's var) vs
  **re-issue** (new key, e.g. scoped/rotated), and record the old→new var mapping so the
  executor configures the secret store without hunting. Never copy values into the pack.
- **Plugin translation policy (standing owner decision):** plugins that provide FRONTEND
  functionality (editors, toasts, icons, masks/validation, QR rendering, JS utils…) are rebuilt
  as **native code** in the new stack — turn each one (from `03-plugins.md`) into a build task;
  only EXTERNAL-SERVICE integrations get a keep/replace/SaaS evaluation here.

### 2b · Frontend design brief for Claude Design

Deliver `FRONTEND-DESIGN.md` — a self-contained brief the owner runs through **Claude Design**
BEFORE any UI implementation starts. It must contain:

- **Design tokens extracted from the actual export** (not invented): the real color palette
  (`settings.client_safe.color_tokens_user`, ranked by usage in the raw export), the fonts in use,
  and neutrals — mapped to CSS-variable token names with a light/dark note and an accessibility
  caveat (flag brand colors that fail AA on text).
- **Design principles** tied to what the app IS (a dense work tool vs a marketing site, the tone
  the domain needs).
- **Component inventory** (design-system pieces) and a **screen inventory** ranked by priority
  using `pages.json` element/workflow counts.
- **Content inventory per screen and role**, when the Bubble screens were captured
  (`unbubble:connect` › `references/screens.md`; `visual/INDEX-bubble.md`): for each P0 screen and
  each role, the information it shows, its fields, its actions, its navigation and its empty
  states, citing the capture. Screens a role cannot open are listed as such.
- **Ready-to-paste prompts** for Claude Design: one for the system/tokens, then one per P0 screen;
  each screen prompt carries that screen's content inventory.
- A handoff note: approved tokens → `tailwind.config` + CSS vars, components → shadcn/ui, feeding
  the design story in BACKLOG. The brief changes presentation only — never BR-xxx rules or the
  data model.

Extract the palette/fonts with a small script over the `.bubble` (never hand-wave the tokens);
put the color anchors and font names in the doc so Claude Design has real brand input.

**The new design system rules the visuals — write this rule into the brief.** The captures are a
*minimum-parity* reference for CONTENT and FLOW only: what each screen must show and let each role
do. They are never a style reference — layout, typography, colors, spacing and component shapes of
the Bubble app are not targets, and the rebuild is expected to look different and better. The
tokens extracted from the export are brand input, not a ceiling. Prompts cite the captures for
content and flow, never for appearance ("show the same fields and actions as the capture, in the
design system's own layout").

### 3 · Redesign the data model

Deliver `DATA-MODEL.md`: the new schema (mermaid erDiagram + DDL sketch) plus a **field-by-field
mapping table** old → new. Apply the Bubble anti-pattern translations in the checklist (option
sets → enums/lookup tables, list-fields → join tables, text-as-FK → real FKs, satellite/cache
tables → views or materialized queries…). Every as-is field must appear in the mapping — mapped,
transformed, or explicitly dropped with a reason.

### 4 · Plan the data migration

Deliver `MIGRATION-PLAN.md`. Decide **per table** between the two mechanisms (decision matrix in
the checklist):

- **CSV export/import** — one-shot, good for small/static tables; loses type fidelity (dates,
  lists serialize as comma-joined text), requires manual re-linking of relations, no delta.
- **Bubble Data API consumption** — the new system (or an ETL job) pages through
  `/api/1.1/obj/<type>` with a **Modified Date cursor**: preserves the Bubble `unique id` (keep
  it as `bubble_id` column for traceability + FK resolution), supports incremental delta sync,
  enables **dual-run** and a low-downtime cutover. Requires enabling the Data API, exposing the
  migrated types, and an API token. Know what the token is: per Bubble's manual, a request with an
  **admin API token acts with the builder's permissions — privacy rules do not limit it**, it can
  read, change and delete every record of every exposed type, and Bubble tokens **cannot be
  scoped** to read-only or to some tables. The only hard boundary is **per-type exposure** (a type
  not exposed is unreachable for every caller). So: expose only the types being migrated, have the
  owner create a **dedicated migration token by hand** (Settings → API) straight into the new
  system's secret store, and delete it — and revert the exposures — after the cutover. The app's
  existing tokens (preserved as `BUBBLE_API_TOKEN_*` in `<workdir>/secrets/.env`, see
  `ENV-KEYS.md`) belong to existing integrations: do not reuse them for the ETL. Requests without a
  token (or with a user token) only get what the privacy rules let that caller see — check what
  "everyone" may read on every type you expose.

Also cover: file/S3 asset migration (Bubble-hosted files must be downloaded and re-uploaded),
option-set values → enum seed data, ordering of tables by FK dependency, **validation &
reconciliation** (row counts + checksums per table, spot-check queries the owner signs off),
rollback plan, and the cutover runbook (freeze window or dual-write, DNS/embed switch, Bubble
kept read-only as archive).

**Size it with real numbers when connected mode is available** (`unbubble:connect` ›
`references/diagnostics.md`, read-only): file storage used (`bubble_storage_usage_get` — the
asset-migration volume), WU per day and hour and what spends it (`bubble_workload_usage_by_date`,
`bubble_workload_usage_breakdown` — peak load to size the new platform, the quietest window for a freeze), plan usage and
workflow run counts. Cite the figures and the date they were read.

**The Bubble side of the cutover runbook** follows `unbubble:connect` › `references/cutover.md`:
every step names its tool (`set_data_type_api_exposure`, `create_301_redirect`, the logs) and its
check, and every write there is an **owner checkpoint** — previewed, approved by the owner, applied
on a branch, merged and deployed by the owner; the executor never writes to Bubble. Write into the
runbook that: exposing a type on `test` also publishes the TEST database through the Data API; the
owner's deploy carries everything pending in `test`, so the changelog since the last deploy is
reviewed before every deploy; and traffic drain after the switch is verified in the server logs
(WU per hour falling to background level, each endpoint and webhook no longer seen — anything still
seen is a caller to re-point).

### 5 · Produce the rebuild pack

```
levelup/
  ASSESSMENT.md            scorecard, tech-debt register, security findings, keepers
  TARGET-ARCHITECTURE.md   stack decision, security & reliability architecture, UX plan
  FRONTEND-DESIGN.md       design brief for Claude Design: tokens from the export, screen
                           inventory, ready-to-paste prompts (run BEFORE UI implementation)
  DATA-MODEL.md            new schema + old→new mapping table
  MIGRATION-PLAN.md        per-table mechanism, cutover runbook, validation
  PRD-v2.md                PRD-clone rewritten for the new platform: parity requirements
                           (BR-xxx) + the upgrade requirements (security, reliability, UX)
                           + explicit non-goals
  BACKLOG.md               epics → ATOMIC stories with acceptance criteria, sequenced:
                           foundations (auth, schema, CI) → migration pipeline → modules by
                           business value → cutover; every story CITES the requirement ids it
                           implements. If the enterprise-best-practices gates were applied
                           (step 0b), each unmet production layer becomes a readiness story.
  RISKS.md                 top risks with mitigations (migration data loss, endpoint consumers
                           breaking, scope creep, dual-run drift)
  EXECUTION-CONTRACT.md    rules of engagement for the executing AI — read order, story
                           discipline, the final completeness gate, deviation protocol
  screen-parity.md|json    (when screens were captured) minimum-parity report per P0 screen and
                           role, written by unbubble:connect's screen_parity.py — step 6b
  screen-parity-verdicts.json  the owner's verdict for every missing item (renamed / moved /
                           dropped / missing)
```

The pack must be **self-sufficient for an AI to implement**: no reference to "the conversation",
every decision recorded with its why, every requirement testable.

End `TARGET-ARCHITECTURE.md` with the same attribution line as the clone's `00-overview.md`
(`_Generated with [UnBubble](https://github.com/yowpi-tech/unbubble)._`, in the pack's language)
and under the same switch: none when the owner asks or `UNBUBBLE_NO_ATTRIBUTION=1` is set, and
nothing beyond that one line.

### 5b · Execution contract (so the executing AI leaves nothing behind)

Write `EXECUTION-CONTRACT.md` — the FIRST file the executing AI must read. It contains, at
minimum:

1. **Source of truth & read order**: this pack (PRD-v2 → DATA-MODEL → TARGET-ARCHITECTURE →
   BACKLOG → MIGRATION-PLAN) plus the clone `docs/` for domain context and `PARITY-MATRIX.md` as
   the completeness ledger. Nothing in the pack may be contradicted or "improved away" without a
   dated owner decision.
2. **Story discipline**: implement in BACKLOG order respecting dependencies; a story is DONE only
   when its acceptance criteria demonstrably pass (test or observed behavior); stories are never
   skipped or silently merged.
3. **Final completeness gate** — the rebuild is only "done" when: every `PARITY-MATRIX.md` row is
   checked off (or carries a signed deviation); `spec_coverage.py` and `parity_check.py` both
   pass; the BR-xxx test suite is green; readiness stories from the enterprise gates (if applied)
   are done; MIGRATION-PLAN validation is signed by the owner; and, when the Bubble screens were
   captured, `screen_parity.py --strict` passes on the P0 screens of every role — every missing
   content or action carries an owner verdict, none is left as `missing` (step 6b).
4. **Deviation protocol**: anything the executor cannot or believes should not implement becomes a
   listed deviation (what, why, impact) requiring the owner's dated sign-off — dropping a
   documented item silently is a contract violation, and "the AI decided it was unnecessary" is
   not a valid disposition.
5. **Bubble is the owner's**: the executor never writes to the Bubble app, never deploys it and
   never creates or reads its API tokens. Every Bubble-side step of the cutover (Data API exposure,
   redirects, the final deploy) is an **owner checkpoint** in BACKLOG — the executor prepares it and
   stops; the owner applies it (connected mode, with approval per batch, or by hand) and signs it
   off.
6. **Secrets rule**: integration credentials come from the clone's `<workdir>/secrets/.env`,
   mapped old→new by `secrets/ENV-KEYS.md` + the integration map — configure them in the new
   system's secret store / env, never hardcode, never commit `.env` (commit `.env.example`
   instead), and never print values in logs, chats, or docs. Keys marked re-issue/rotate in the
   integration map must be replaced before go-live.

### 5c · Spec-coverage gate — no requirement without an executor (run BEFORE delivering)

The parity matrix guards *legacy → disposition*. This gate guards the opposite direction,
**requirement → story**, which is where documented features die: they are written in the docs and
the PRD, no BACKLOG story ever owns them, and the executor delivers a subset that looks complete.
(Seen in practice: features written in the business rules and in the PRD that no story cited
were simply not built, and only users noticed.)

```bash
python3 scripts/spec_coverage.py \
  --spec <workdir>/docs/07-business-rules.md \
  --spec <workdir>/levelup/PRD-v2.md \
  --backlog <workdir>/levelup/BACKLOG.md \
  --out <workdir>/levelup --strict-acceptance
```

It fails (exit 1) on: a requirement no story cites (coverage is transitive — a story citing
`P-DOC-1` covers the `BR-010` it derives from); a story citing no requirement; a story left
undecomposed; and, with `--strict-acceptance`, a requirement without verifiable form.

**Do not deliver the pack until it passes.** Fix by writing the missing story, adding the
citation, splitting the story, or — only with a dated owner decision — descoping the requirement.
Two conscious escape hatches exist and both must be *earned*: `[infra]` on a story that
implements no product requirement (bootstrap, migration, cutover) and `[descritivo]` on a
requirement that is context rather than behaviour.

Write the requirements so this passes by construction:

- **PRD requirements are testable.** `U-REL-1` style: state the behaviour and an explicit
  `*Aceite:*` (or `QUANDO … DEVE …`). "Implementar X bem" is not a requirement.
- **Stories are atomic.** No `(G)` and no "quebrar depois" survives into the delivered pack — an
  epic marked for later decomposition is precisely where the executor improvises. Split until
  each story has its own verifiable acceptance criterion.
- **Every story cites its requirement ids** (`P-DOC-1…5`, `BR-020…023`, `U-SEC-1/2` — ranges and
  slash-lists are understood).

### 6 · Parity check — verify the rebuild actually uses the whole model

The clone step guarantees *every active field is documented*; step 3 guarantees *every as-is
field is mapped* in `DATA-MODEL.md`. Neither guarantees the **rebuilt code reads or writes it**.
That last hop is where fields silently disappear: a column survives the export, the docs, the
mapping and the migrated schema, but the reconstruction wires only a subset — so the feature is
"lost" even though the data is right there. (Seen in practice: a whole group of foreign keys
and their lookup tables existed in the migrated DB, but the module's types/repository/UI never
touched them.)

Run the parity check against the rebuilt app **whenever a module is reported done**, and again
before cutover:

```bash
python3 scripts/parity_check.py \
  --schema <app>/supabase/migrations \   # or a DATA-MODEL DDL file, or {"tables": {...}} JSON
  --app    <app>/src \
  --out    <workdir>/levelup
```

Dependency-free, read-only. It writes `parity-report.md` / `.json` listing **orphan tables**
(a schema table whose name never appears in code) and **orphan columns** (split into
high-confidence composite names and low-signal short names to verify by hand). Structural
columns (`id`, `organization_id`, timestamps, `bubble_id`, `deleted_at`) are ignored. A
column/table counts as referenced when its exact snake_case identifier appears anywhere in the
source (DB names surface in query strings even when the app uses camelCase variables).

For every orphan, record a verdict — this is the gate:
- **Used** elsewhere (view / generated type / RPC) → note where; not a miss.
- **Deferred** on purpose → add a BACKLOG story with the reason (so it is tracked, not lost).
- **Forgotten** → wire the types/repository/UI now.

Never let an orphan pass silently: an unclassified orphan is a candidate lost feature. Record
the run (coverage %, and the classified orphan list) in `ASSESSMENT.md` or a `PARITY.md` note.

### 6b · Minimum screen parity — content and actions per role (connected mode)

`parity_check.py` proves the code touches the data; it cannot see a screen that lost a field, a
button or a whole tab for one role. When the Bubble screens were captured
(`unbubble:connect` › `references/screens.md`), capture the same screens of the rebuilt app and
compare them **whenever a module is reported done** (its P0 screens, every role) and before the
cutover:

```bash
python3 <connect>/scripts/capture_screens.py --app <app-id> --target rebuild \
    --base-url http://localhost:3000 --route-map routes.json --roles anon,admin,agent
python3 <connect>/scripts/screen_parity.py --app <app-id> --pages <P0 pages> --strict
```

(`<connect>` = `skills/connect/` of the UnBubble checkout; the rebuilt app's test users sign in
once per role with `capture-app-session --target rebuild`.) It lists what each Bubble screen offers
that the rebuilt one does not — headings, labels, fields, buttons and links, images — ignoring
geometry, typography, colors and spacing. **Visual differences are expected and never fail the
gate**; only missing content or actions without an owner verdict do. Each item gets a verdict in
`levelup/screen-parity-verdicts.json`: `renamed` / `moved` (present in another form or place),
`dropped` (dated owner decision), or `missing` (a real gap → a BACKLOG story, gate stays open).
The MCP's geometric tools (`bubble_visual_compare`, `bubble_visual_audit`) are not part of this
gate, and their repair plans target Bubble: never apply them.

## Quality bar

- Every assessment claim cites evidence from the clone docs/inventory.
- Security/reliability decisions are never traded for UX or speed — if a trade-off is forced,
  it is written down in RISKS.md with the user's explicit sign-off required.
- The migration plan accounts for **every** table and file field in DATA-MODEL.md's mapping.
- PRD-v2 keeps full traceability to BR-xxx rules so parity is verifiable after the rebuild.
- FRONTEND-DESIGN.md uses tokens **extracted from the export**, not invented, and is written to be
  run through Claude Design before UI work starts.
- ASSESSMENT.md states whether the `enterprise-best-practices` gates were applied (which layers/
  themes), or that they were skipped and why (step 0b).
- EXECUTION-CONTRACT.md exists and its completeness gate references the clone's PARITY-MATRIX —
  the executor has no path to "done" that skips documented scope.
- The integration map covers every var group in the clone's `secrets/ENV-KEYS.md` with a
  reuse/re-issue decision and an old→new mapping (unused-in-app keys may be dropped with a note);
  no credential value appears in the pack.
- `spec_coverage.py --strict-acceptance` **passes** before delivery: every requirement has a story
  that implements it, no story is orphan or undecomposed, every behavioural requirement is
  testable. A pack that fails this gate is not delivered.
- After a module is rebuilt, `scripts/parity_check.py` was run and **every** orphan table/column
  it reports is classified (used / deferred-with-reason / fixed) — no silent drops between the
  DATA-MODEL and the running code (step 6).
- When the Bubble screens were captured: FRONTEND-DESIGN.md carries the content inventory per P0
  screen and role and states that the captures are never a style reference; after a module is
  rebuilt, `screen_parity.py --strict` passes on its P0 screens for every role (step 6b).
- MIGRATION-PLAN.md describes the Data API token correctly (admin token: privacy rules do not limit
  it; it cannot be scoped; exposure per type is the boundary; a dedicated token created by the
  owner, deleted after the cutover), and every Bubble-side cutover step is an owner checkpoint.
