# CLAUDE.md — project-wide operating rules for Claude Code sessions

Loaded automatically by Claude Code on every session in this repo. Applies to **all** bots regardless of lane.

**Current priorities live at the top of `KANBAN.md`, period.** This file and the bibles hold slow-moving invariants; fast-moving focus (what's active/paused/next) is KANBAN's job — never encode priority or lane status into a versioned governance doc (it is guaranteed to go stale).

> **Doc version:** v2.9.4 (2026-09-26) — §3 lane list: D4 can now run on its own Render service (`exos-web`, from `JulianS4K/EXP`); with `EXOS_ORIGIN` set, `/bridge/*` here reverse-proxies to it and `static/bridge/` is only the fallback. · v2.9.3 (2026-09-26) — §3 lane list: D4's `*exos*` migrations + `tests/exos` moved to `JulianS4K/EXP` as well; nothing Exos-sourced remains here except the built `static/bridge/` bundle. · v2.9.2 (2026-09-26) — §3 lane list: D4's edge functions (`exos-*`, `stripe-webhook`) moved to `JulianS4K/EXP` too; migrations stay here. · v2.9.1 (2026-09-24) — §3 lane list: D4's SPA source moved to `JulianS4K/EXP`; ownership unchanged. · v2.9.0 (2026-09-10) — §3 lane list: **retired D6 (paciolan/eVenue) into A1** — a browser collector + `paciolan_*` schema + crons 532/533 is A1's data plane, not a product surface; nine lanes→eight. Records that retiring a lane does not stop its code. D3/Broadway has the same shape but is deliberately left alone pending operator review. · v2.8.0 (2026-09-10) — §3 lane list corrected: this file still said **six lanes (D0–D4)** long after D5 (fantasy, 2026-07-08) and D6 (paciolan/eVenue, 2026-07-27) were added to `PROJECT_BIBLE §2`, which is the canonical owner — real drift in the file every session reads first. Now nine lanes, including the new **D7 · N2S obligation-covering** carved out of D0. · v2.7.0 (2026-07-08) — §5: catalogued the second shipped skill, `check-poll-mapping-health` (read-only data-poll-failure + event-mapping-drift sweep; run daily by a scheduled routine or on demand — reports + one `bot_chat` ledger row, never mutates). · v2.6.0 (2026-07-04) — added the **"On activation — classify the task first"** rule: every session opens by asking the operator whether the task is a **SQL query** (read-only investigation, Rule 1) or a **code change** (full lane/permission/CI discipline), unless the prompt already makes it unambiguous. (No hierarchy edit needed — v2.5.0's dissolution language is current.) · v2.5.0 (2026-07-03) — A1-as-gatekeeper language retired: prod-DB apply + Render writes are **Applier** actions run per-task by any session under operator direction, not centralized on A1 (A1/B1/D0 codes are naming conventions for surface ownership, not a chain of command — the hierarchy stays dissolved). · v2.4.0 (2026-07-02) — tier-2 lane consolidation (KANBAN C1-OPS-3): C1 folded into B1 (docs = Auditor work), D2 folded into D0 (both broker); six lanes now (substrate A1·B1 + products D0·D1·D3·D4). · v2.3.0 (2026-07-02) — §4 Render access restated under the 3-principal model (`PROJECT_BIBLE §2.1`); D0 "workspace-wide Render parity" retired; added the priority-lives-in-KANBAN rule up top; actor hierarchy dissolved (A1/B1/C1/D0–D4 now flat lane identifiers, not ranks — `PROJECT_BIBLE §2`). Full prior doc-version history → [`docs/archive/2026-07-02-doc-version-history.md`](docs/archive/2026-07-02-doc-version-history.md).

## 🟢 On activation — classify the task first

**At the start of every session, ask the operator whether this is a SQL query or a code change** — unless the prompt already makes it unambiguous (e.g. it hands you a migration to apply, names a file to edit, or is plainly read-only). The answer sets your mode and how much of the discipline below applies:

- **SQL query** → read-only investigation only: `SELECT` / `information_schema` / `pg_*` / MCP `list_*`·`get_*` / log inspection. **No** mutation, migrations, deploys, or file edits (Rule 1). Answer the question, then stop.
- **Code change** → author files/migrations under the full lane + permission + CI discipline (`PROJECT_BIBLE §2`, Push protocol). Prod mutation is still an **Applier** action (Rule 1); read the bible before authoring.

If the answer is "both" (or the task turns out to need writes mid-investigation), do the read-only part first, then confirm the write scope with the operator before any mutation.

## 🔖 READ PROJECT_BIBLE.md FIRST (token discipline)

**Before doing anything, read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md).** It consolidates the 80% you need from this file + lane ownership (its §2, which absorbed `BOT_HIERARCHY.md`) + MIGRATION_CONVENTIONS.md + data-source docs into a single per-session reference. Saves ~5× the tokens vs reading every governance file at session start.

The bible has:
- Hard rules (no-mutation, read-only-upstream, lane scope)
- Lane ownership map (labels = surface regions, not a hierarchy) + Render service ownership per lane
- Canonical SECDEF RPCs (`get_broker_event_page_v2`, matchers, bot_chat_log, etc.)
- Key tables + freshness expectations + **column-name landmines** (catch schema bugs before authoring)
- MCP tool scope per lane
- SQL macros / common patterns (cancel filter, SG dedupe, sports gate, outdoor gate, email gate, cron wrapper)
- Workflow recipes ("I want to author a migration", "I want to wire a UI panel", etc.)
- Recent landmark migrations (don't re-do work already shipped)
- Drift watchlist (known gaps — don't waste cycles rediscovering)
- Self-check (10-item pre-task checklist)

This file (CLAUDE.md) remains the canonical source for security rules + lockdown invariants. The bible is the operational handbook bots read once per session.

Ownership (which lane owns a surface) and permission (the three principals — Applier/Auditor/Builder) both live in `PROJECT_BIBLE.md §2` (which absorbed `BOT_HIERARCHY.md` on 2026-06-19, itself having absorbed `LANE_DISCIPLINE.md`). §2 keeps the two separate: ownership is a surface map, permission is per-action (restructured 2026-07-02 — the former per-bot permission grid was the drift generator). The per-bot self-contracts were retired into §2 (2026-06-19); only `docs/b1_operating_constraints.md` remains, kept for its security severity matrix (referenced by `.github/SECURITY.md` + the secret-scan workflow).

## Global operator rules (2026-05-13 lockdown)

These three rules supersede prior MCP-applied autonomy. They apply to every bot in every lane.

### 1. SQL data is read-only by default

Read freely: `SELECT`, `information_schema`, `pg_*` views, log inspection, MCP `list_*`/`get_*` calls.

**Need explicit operator permission before:**
- `apply_migration` against any prod project
- `execute_sql` with `INSERT` / `UPDATE` / `DELETE` / `DDL` on prod
- Cron schedule changes (`cron.schedule`, `cron.unschedule`)
- Edge function deploys that mutate data
- Any change to `vault.*` / `auth.*` / `cron.*` schemas

**Standing permissions (no per-call ask):**
- `bot_chat` writes via `bot_chat_log()` / `bot_chat_resolve()` — these are the designed cross-lane coordination surface
- Supabase **branch** creation (`create_branch` produces a copy-on-write fork — no prod-data mutation)
- Author migrations as files in `supabase/migrations/` — application to prod is gated separately

**Resolve-protocol semantics (2026-05-15 — C1 / A1 convention):**
A `bot_chat` reply with `event_type='status'` and `p_in_reply_to` set is the **canonical closure signal** for its parent thread. The `v_bot_chat_unresolved` view (C1-owned, see PR #114 Cluster D-1) auto-excludes any row that has a `status` reply pointing at it via `in_reply_to`. Implications for bot authors:
- If you are CLOSING a thread (work shipped, question answered), use `event_type='status'`. This will mark the parent as resolved automatically.
- If you are still working on a thread (acknowledging without fixing), use `event_type='flag'` or `'question'`. These do NOT close the parent — the unresolved view still surfaces it.
- Premature `status` replies that conflate "I saw this" with "I fixed this" defeat the resolve hygiene. When in doubt, use `flag`.

### 2. Upstream third-party APIs are read-only

Applies to **every** external API the project integrates with — TEvo, SeatGeek, SeatData, TickPick, Vivid, and any future client (`*_client.py`).

OK: search / suggestions / events / performers / venues / ticket_groups / listings — any GET / read endpoint.

**Forbidden without explicit operator authorization:**
- Order creation (`POST /orders`, `POST /v9/orders`, equivalent on SG / TP / Vivid)
- Holds, locks, reservations, inventory mutations
- Any write / mutation endpoint on any upstream API
- Webhook subscription changes
- Account / seller-side configuration changes

**Listing-source lockdown — price changes + force-pulls cannot influence upstream, no bypass *(operator directive 2026-06-01)*:**
- **EVO and SeatGeek (and every listing source) listing prices cannot be changed.** There is no reprice / set-price / update-listing code path anywhere, and none may be added. Each `*_client.py` is GET-only *by construction* — `ALLOWED_HTTP_METHODS = frozenset({"GET"})` + `_assert_readonly_method()` that **raises** on any non-GET — so a price/inventory mutation is impossible, not merely discouraged. (The guard *body* is single-sourced in `core/readonly_guard.py` since BR-CODE-2, but every client still declares those two tokens in-file — the `check_readonly.py` static audit requires them per-file; **never re-inline-then-weaken or widen the allowlist**.) (Lone carve-out: SeatData permits one non-data metadata POST, `/event-request-add`, which writes none of our data and touches no price/inventory.)
- **On-demand / "force-pull" refresh paths may READ but must NEVER influence a listing-source API.** The force/sync triggers (`raw-tevo?force=true`, `/api/seatgeek/.../sync-listings`, `/sync-sales`, `/api/seatdata/.../sync-sales`, `/auto-search`, `/api/collect/run`, `/api/admin/collect-*`) pull data **in**; they never push an order, hold, write, or price/inventory change **out** to TEvo / SG / SeatData / TP / Vivid. Refreshing the data is fine; influencing the source is forbidden.
- **No bypass — enforced mechanically.** `scripts/check_readonly.py` (CI static audit: fails the build on any write to a broker host, or a removed guard token) + `tests/test_readonly_guards.py` (asserts every client raises on POST/PUT/PATCH/DELETE). Weakening, deleting, or routing around either guard is a **security-CRIT** change (RULE-2 is **A1**'s DB/API-security domain as of the 2026-06-17 reorg; B1 owns git/code security) and is forbidden without explicit operator authorization.

### 3. Free reign on HTML / wiring within your lane

Each bot has operational latitude on UI files and JS wiring routed to them. Build, iterate, refactor without per-step approval.

Lane assignments per `PROJECT_BIBLE.md §2` (**eight** lanes: a two-area substrate + six products; peer surfaces, not a chain):
- **A1** — data plane (DB + full ingest pipeline + cross-source xref + DB security + crons)
- **B1** — build + guards + governance (git/code security, CI + guards, drift, freshness, tests, **and the docs surface** — bibles + registry + `bot_chat` + seam register, absorbed from C1 2026-07-02; this is the Auditor principal's home)
- **D0–D7 products** — distinct surfaces, each owning its Render service + UX/speed testing (D0 terminal + orders-dashboard · D1 store · D3 broadway · D4 Exos/Bridge *(source in `JulianS4K/EXP`: SPA since 2026-09-24; edge functions, `*exos*` migrations + `tests/exos` since 2026-09-26. The DB is still shared, so they apply/deploy to this project; only the built `static/bridge/` bundle lives here, and with `EXOS_ORIGIN` set `/bridge/*` is reverse-proxied to the `exos-web` service instead (`core/exos_proxy.py`), keeping the same URL + login)* · D5 fantasy · D7 N2S obligation-covering). ⚠ **D7 is a NAMED SUBSET of D0's surface**, not a separate tree — `subs.{html,js}` and `n2s_*` only; see `PROJECT_BIBLE §2.3`.
- **Retired as lanes**: C1→B1 (docs governance = Auditor work) and D2→D0 (both broker-facing), 2026-07-02 (KANBAN C1-OPS-3); **D6→A1** (paciolan/eVenue — a collector + schema + crons is A1's data plane, not a product), 2026-09-10. `c1`/`d2`/`d6` remain only as historical branch/KANBAN/`bot_chat`-tier tokens. ⚠ A retirement is an **ownership** change — D6's crons 532/533 keep running; stopping them is a separate operator call.
- Operator may explicitly route work to a session outside its default lane (this is the override path)

### 4. Render workspace — per-service scoped access (2026-05-14, reorg 2026-05-15; testing-unified 2026-05-16)

**Testing-unified architecture (2026-05-16, PR #168)**: During dev/test, all runtime traffic flows through `vibepass-storefront-test` (starter plan, no cold-start drag). It hosts D0 terminal + D1 storefront + D2 dashboard via `app.include_router` mounts in `server.py`. `vibepass-terminal-test` remains as the D0 static CDN host; `d2-orders-dashboard` stays alive as an idle placeholder. At beta, each surface migrates back to its own service via dedicated DNS + un-mounting from `server.py`.

Render MCP tools (`mcp__render__*`) follow the **three-principal permission model** (`PROJECT_BIBLE.md §2.1`), not a per-bot grid. The former per-bot Render matrix — including D0's "workspace-wide parity with A1" (2026-05-16) — was **retired 2026-07-02**: surface *ownership* (which lane owns a service's files/IaC, `PROJECT_BIBLE §2.7`) is separate from *write authority*.

**Render reads are open to every session** (`list_*`/logs/metrics — monitoring is universal, no per-call ask).

**Render writes are an Applier action** (`PROJECT_BIBLE §2.1`): deploys, service config, provisioning/deletion, workspace-level operations (`create_web_service`, `create_postgres`, `create_static_site`, `create_cron_job`, `select_workspace`), ownership changes. The Applier action is taken **per-task by any session under operator direction** — not centralized on a lane. A session that owns a Render service's *surface* (D0/D1/D2 per §2.7) authors its `render*.yaml` IaC as a **Builder**, but the runtime write is applied through the Applier principal — not standing per-bot authority. Any standing deviation is a dated row in `PROJECT_BIBLE §2.2`.

**Standing rules:**
- Read ops always OK (no per-call ask).
- Service Tokens are the preferred enforcement mechanism when feasible (Render's Member-role token can't perform writes by API constraint — hard isolation beyond policy). Until tokens are scoped, the scoping is policy-level and audited via Render's audit log.
- A write to a service whose surface another lane owns is a cross-lane action — surface a `flag` in `bot_chat` per the cross-lane rules.

### 5. Skill conventions (SKILL.md structure + discoverability)

Recurring procedures are encoded as **workflow skills** under `.claude-plugins/terminal2-governance/skills/<name>/SKILL.md` — the executable form of the `PROJECT_BIBLE.md §8` recipes. Shipped: `ship-a-migration`, `check-poll-mapping-health`.

**SKILL.md structure** (four labeled sections, trimmed for token discipline; keep ≤~80 lines):
- **frontmatter** — `name`, `description`.
- **Process** — the numbered operative steps (check → act → tools).
- **Red flags** — the must-NOT list.
- **Verification** — a one-line evidence-based self-check the skill *reasons about* before finishing (phrase as a check, never an action). A `Rationalizations` table (excuse→rebuttal, wired to §3 landmines) is encouraged.

**Procedures → skills, facts → bibles, link don't copy** — a skill points to `§3`/`§0`/`§14`, never restates them.

**Discoverability is mechanical, not memory.** `.claude-plugins/terminal2-governance/hooks/hooks.json` runs a **PreToolUse** router (`scripts/skill_router.py`) that matches a tool call to a skill and injects a **non-blocking** nudge (editing `supabase/migrations/*.sql`, `apply_migration`, or DDL via `execute_sql` → surfaces `ship-a-migration`). Fires once per (session, skill); `ROUTES` is the single source of truth.

### 6. Documentation discipline — the canonical doc set is CLOSED (2026-05-28)

The repo's governance/reference docs are a **closed set**. The registry table in [`README.md`](README.md) lists every canonical root doc and exactly what it owns. This rule exists because the prior consolidation regrew into sprawl — nothing gated new-doc creation. Now there is a gate.

- **Do NOT create new root or governance `.md` files.** To add a fact, edit the doc that already owns that topic (the README registry names the owner). A genuinely new top-level doc is an operator decision — ask first.
- **No lane-specific bibles (2026-06-19).** Bots don't pre-know their lane at session start, so a per-lane `<BOT>_BIBLE.md` goes unread while the universal facts inside it get missed. Everything universal lives in the **main set** (`PROJECT_BIBLE`/`RESOURCES_BIBLE`); lane-specific *procedure* (e.g. building the D0 terminal) is an on-demand `docs/` reference, not a session-start read. (The former `D0_BIBLE.md` was split 2026-06-19: cross-source architecture → `PROJECT_BIBLE §5`, build manual → `docs/d0_terminal_build.md`.)
- **One fact, one home — never duplicate; link.** If a fact already lives somewhere, point to it (`see <DOC> §<n>`) rather than restating it. Duplicated facts are exactly how these docs drifted out of sync.
- **Ephemeral work never becomes a new doc.** Audits, checkpoints, session logs, handoffs, status snapshots → use `bot_chat` (durable cross-lane record) or `KANBAN.md` (open work). Only if a durable dated artifact is genuinely needed: `docs/archive/YYYY-MM-DD-<topic>.md` (historical, non-canonical).
- **Enforcement is a hard CI gate** (server-side; `--no-verify` cannot skip). `docs-registry-check` (`bin/check-docs.sh`) fails a PR that adds a root `*.md` not in the README registry, or a dated/working-note file in `docs/` outside `docs/archive/`. *(Keeping the bible current when a change adds a catalogued resource (RULE 0) is a judgment prompt — `PROJECT_BIBLE` self-check #12 + the PR checklist — deliberately NOT a gate: a mechanical check can't distinguish a change that needs a doc from one that doesn't, so forcing it would just spam no-op edits.)*
- **One `**Doc version:**` line per doc; no per-section tags (2026-06-19).** Bump the doc-version line on material change; the gate fails any registry doc (except `CHANGELOG.md`) missing it. Per-heading `(vX · BOT · date)` tags are removed — git blame is the audit trail. Full convention in [`README.md`](README.md) *Doc-writing rules*.

## Cross-lane writes

If your work needs to touch another lane's surface:
1. Propose via PR comment to the lane owner first
2. If owner offline, surface as `flag` in `bot_chat` for B1/A1 resolution
3. **Never silently write across lanes** — even read-only-looking writes (e.g. cache files, logs) count

## Push protocol *(reorg 2026-06-17)*

- **Push to `main` is per-task/per-agent, not bot-tier-gated.** Each task is pushed by the session it's delegated to, after green CI; `main` is maintained per-task, with no sole-pusher lane. (Supersedes the prior "A1 sole pusher" immutable rule, operator directive 2026-06-17. See `PROJECT_BIBLE.md §2.3`.)
- **Prod-DB apply is per-task/session-run, not lane-gated** — any session may apply its own reviewed, CI-green migration to prod under operator direction; **there is no A1 gatekeeper**. The A1/B1/D0 codes are naming conventions for *surface ownership*, not a chain of command (the actor hierarchy is dissolved, `PROJECT_BIBLE §2`). Author the migration file, get it reviewed + CI-green, then apply. (Git push ≠ DB apply — both are per-task, neither centralized on a lane.)
- Open a PR per task; CI must be green before merge.

## When in doubt

- Ask via `AskUserQuestion` for a quick clarification
- Use `bot_chat` `question` event_type for cross-lane queries
- Read-only investigation is always safe; mutation is never safe by default
