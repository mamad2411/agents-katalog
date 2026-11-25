---
name: audit
description: >
  Audit a Bubble.io app export (a .bubble file) to find UNUSED / dead entities that can be
  safely deleted: pages never navigated to, reusable elements never placed, backend API
  workflows that are neither exposed as an endpoint nor triggered, Option Sets referenced
  nowhere, installed plugins with no elements/actions/config, styles applied to no element,
  data FIELDS and TABLES (data types) that are never used — including whether each is
  exposed in Bubble's native Data API — and a workflow audit: CUSTOM EVENTS (backend and page)
  that are never called, plus workflows whose trigger element was deleted or is never rendered
  (itself or via a parent group that never shows) and so can never fire; and API Connector
  endpoints/calls that are declared but never invoked; and elements/actions referencing a plugin
  that was removed/uninstalled (broken ghost references). Produces a self-contained,
  interactive HTML report with
  confidence levels and a deletion tracker, plus a JSON summary. Use this WHENEVER the user
  hands you a `.bubble` file or a Bubble app export and asks anything like: what can I delete /
  clean up / remove, which pages/plugins/workflows/option sets/styles/fields/tables/data types
  are unused, what's exposed in the Data API, reduce technical debt, slim down or audit a Bubble
  app, "quais páginas/plugins/workflows/campos/tabelas posso excluir", "o que não está sendo
  usado", "campos ou tabelas sem uso", "limpar o app Bubble", or dead-code / orphan analysis of
  a Bubble project. Trigger even if they only mention one category (e.g. "which plugins aren't
  used", "unused database fields", "custom events never called", "dead workflows", or "unused API
  Connector calls") — the skill answers all nine areas and the user can read just the part they need.
---

# Bubble unused-entities audit

> **UnBubble pipeline — step 1 of 3.** This audit exists so the app owner can DELETE the dead
> entities inside the Bubble editor and then **re-export a lean `.bubble`**. That lean export is
> the input for **`unbubble:clone`** (step 2: as-is technical documentation + clone PRD) and then
> **`unbubble:level-up`** (step 3: re-architecture + data-migration plan). After delivering the
> audit report, tell the user this next step exists.

## Project folder (all pipeline steps write here)

Every UnBubble project gets ONE folder: **`~/UnBubble-Projects/<app-id>/`** (app id = the app's
`_id` in the export, e.g. `my-app`). Create it on first contact and put ALL generated
artifacts there — never scatter outputs in Downloads or the skill repo:

```
~/UnBubble-Projects/<app>/
  audit/       one report per round: <app>-vN_unused_report.html (+ _audit.json,
               bubble_cleanup_progress__<app>.json|md = deletions + section sign-offs + kept items)
  inventory/   bubble_inventory.py output            (step 2 · clone)
  docs/        as-is docs + PRD-clone.md             (step 2 · clone)
  levelup/     rebuild pack                          (step 3 · level-up)
```

The `.bubble` exports themselves may stay where the user keeps them (they're large); reference
their paths in the docs instead of copying.

## What this does and why it's hard

A Bubble app export (`.bubble`) is one giant single-line JSON — often 50–150 MB. There is no
built-in "find unused things" feature, and a naive text search gives false answers because
Bubble references entities in six different, non-obvious ways. This skill encodes the real
reference model so you can reliably tell an app owner what is safe to delete.

The output is a polished HTML report (interactive tables, filters, confidence badges, light/dark)
that answers seven questions:

1. **Pages** that can be deleted (not navigated to / referenced)
2. **Reusable elements** that can be deleted (never placed)
3. **Backend workflows** unused *and* not exposed as an API endpoint
4. **Option Sets** used nowhere
5. **Plugins** installed but unused
6. **Styles** not applied to any element — plus unused **color & font variables** (design tokens)
7. **Data fields & tables** never used — and whether each is exposed in the native **Data API**
8. **Workflow audit** — **Custom Events** (backend + page/reusable) never called; workflows whose
   trigger element was **deleted**; and workflows whose trigger element is **never rendered** —
   itself or via a **parent group that never shows**, accounting for default visibility, Show
   actions AND conditional `states` (the Conditional tab). Verified false-positive-free on a sample.
9. **API Connector** — declared API endpoints (calls) that are **never invoked** as a data source
   or a workflow action anywhere (`apiconnector2-<api>.<call>` appears nowhere).
10. **Removed-plugin references** — elements/actions whose plugin id (`<pluginId>-…` type) is NOT in
    the installed-plugins list: the plugin was **uninstalled** but the references remain (broken
    ghost refs). Listed with plugin name + page/reusable + the exact element or workflow.

## The one thing to run

Everything is done by one dependency-free script (Python 3.8+ stdlib only). **Do not re-derive
the analysis by hand or write your own parser** — this script encodes reference rules that are
easy to get subtly wrong, and it has been validated to reproduce a hand-audit exactly.

```bash
python3 scripts/bubble_audit.py "path/to/export.bubble"
```

Common options:

```bash
python3 scripts/bubble_audit.py export.bubble \
  --out report.html \        # HTML report path (default: <input>_unused_report.html)
  --json results.json \      # also emit a machine-readable summary
  --lang pt \                # report language: pt (default) or en
  --date 2026-07-09 \        # date stamp shown in the report header
  --pages-csv audit.csv \    # ONLY if the user hands you a page-inventory CSV for THIS app (see below)
  --state progress.md \      # optional, repeatable: pre-check items already deleted (report Export
                             #   .md/.json, or the connected-mode cleanup journal — keys are merged)
  --evidence ev.json \        # optional, repeatable: runtime evidence from the connected mode — a
                             #   "runs: N×" or "logs: N×" badge on every candidate it checked (step 3b)
  --plugin-names names.json  # optional: extra {pluginId: name} to extend the bundled registry
```

The script prints a summary to stdout and writes the HTML report. It runs in a few seconds even
on a 100 MB file. It never modifies the export.

### Workflow

1. **Locate the export.** Ask for the `.bubble` file path if not given. These are usually in
   Downloads. They're large — never `cat`/read the whole file into context; the script streams it.
   **Connected mode** (`unbubble:connect`, optional): when it is installed and the app has a session,
   offer to download a fresh export of `test` instead —
   `python3 <connect>/scripts/fetch_export.py --app <app-id> --version test` (`<connect>` = the
   `unbubble:connect` skill folder: `skills/connect/` of the UnBubble checkout) — which keeps an
   immutable copy per round and a provenance sidecar the report header shows (version, time, sha256).
   It never touches live and fails loudly instead of handing back an old cached export.
2. **Run the script** with `--out` pointing into the project folder:
   `~/UnBubble-Projects/<app>/audit/<app>-vN_unused_report.html` (N = audit round; create the
   folder if missing). Pass `--lang pt` for a Portuguese report if the user works in Portuguese.
3. **Read the stdout summary** and relay the headline counts to the user, then point them at the
   HTML report file. Lead with the high-confidence categories (backend workflows, option sets,
   reusables, styles) and frame pages carefully (see caveats).
   **If the first line says `EXPORT INCOMPLETE`, say that before anything else**: some reusable
   definitions are in the editor index but have no payload in the export (Bubble stopped inlining
   them for some large apps), so every reference made inside them is invisible and findings in
   any section can be false positives. Nothing should be deleted from that round — get a complete
   export first (re-export, or download it through `unbubble:connect`, which re-hydrates the
   definitions) and run the audit again. The report shows the same warning in red at the top, and
   `--json` carries it as `export_integrity`.
3b. **Runtime evidence (connected mode, optional).** Static analysis cannot see callers from
   outside the app: an exposed endpoint a partner calls, a webhook, a page opened by direct link, an
   API call that does run. When connected mode is available, gather evidence for this round's JSON
   from two sources — workflow runs in the workload metrics (best for workflows) and the server logs
   (pages and API calls) — and regenerate the report with both:

   ```bash
   python3 <connect>/scripts/runtime_evidence.py ~/UnBubble-Projects/<app>/audit/<app>-vN_audit.json \
       --profile <app-id> --source workload --export <export>
   python3 <connect>/scripts/runtime_evidence.py ~/UnBubble-Projects/<app>/audit/<app>-vN_audit.json \
       --profile <app-id> --export <export> --days 14
   python3 scripts/bubble_audit.py <export> --out … --json … --state … \
       --evidence ~/UnBubble-Projects/<app>/audit/runtime-evidence__<app>-vN.json \
       --evidence ~/UnBubble-Projects/<app>/audit/runtime-evidence__<app>-vN.workload.json
   ```

   Pass only files whose run exited 0. **Exit 3 means the source showed nothing even for a workflow
   known to run** (on some large apps the logs answer every query with zero rows): its zeros were
   made unknown — leave that file out and say so. Every checked candidate gets a badge naming its
   source: **runs: N×** (pt **execuções**) / **logs: N×** (seen — likely in real use: review before
   deleting; the connected-mode cleanup plan leaves these out), **runs: 0** / **logs: 0** (not seen
   in the window — strengthens "unused", never proves it), **runs: ?** / **logs: ?** (no evidence:
   the workload does not meter pages or API Connector calls, or the data was incomplete). The header
   states each source's window — for the workload, the days Bubble still keeps (about 31) — and, for
   the logs, the version read (live by default). Relay counts, never log rows; read
   `<connect>/references/evidence.md` before interpreting.
4. **Verify the report renders** if you have a browser/preview available (serve the folder with
   `python3 -m http.server` — note macOS blocks serving `~/Downloads`, so copy the HTML to a
   temp dir first, or write it there with `--out`).
5. Offer follow-ups: a CSV/checklist export, a deeper dive on one category, or applying the
   deletions through the connected mode (step 6).
6. **Apply the cleanup (connected mode, optional).** Instead of the owner deleting item by item in
   the editor, the agent can apply the high-confidence deletions on a dedicated branch: plan →
   batches previewed and approved by the owner one at a time → journal → fresh export of the branch
   → audit round N+1 with `--state` (progress + journal) → the owner merges the branch, later
   deploys, both by hand. Follow `<connect>/references/cleanup.md` exactly — it never writes to
   live, never deletes what the owner kept or what the runtime evidence shows running, and leaves
   reusable definitions, backend workflows, plugins and API Connector calls to the owner (the MCP
   cannot delete them).

## Confidence levels — this is the most important part to communicate

Not every "unreferenced" entity is safe to delete. Be honest about this; it's what makes the
report trustworthy.

- **High confidence (act on these first):** backend workflows, option sets, reusable elements,
  and styles. Their reference mechanisms are deterministic and fully captured. A non-exposed
  `APIEvent` that is scheduled nowhere literally cannot run; an option set whose `option.<name>`
  token appears nowhere is genuinely unreferenced. Two exposure subtleties the script already
  handles (do not "simplify" them away): a **missing `expose` key means EXPOSED** (Bubble only
  serializes `expose: false` when the checkbox is unchecked), and workflows the app calls on
  itself via an **API Connector self-call** (`…/wf/<name>`) count as used.
- **Data fields & tables (section 7):** a field is unused if its key appears in no expression,
  workflow, search, privacy rule or JS/HTML script; a table if it is referenced nowhere as
  `custom.<type>`, has no used field, and is not exposed. Two nuances to always convey: (a) fields
  whose **table is exposed in the Data API** are shown in a *separate* "exposed — verify" bucket
  because external consumers aren't in the export; (b) deleting a data type/field **deletes its
  data** — this is destructive, so frame it as "no references found; confirm no data to keep,"
  not "safe to delete." Field keys shared across tables are handled conservatively (marked used if
  referenced on any table), so the unused-field list under-reports rather than over-claims.
- **Lower confidence — needs a human:** **pages** and some **plugins**. Every Bubble page has its
  own public URL, so a page with no internal navigation may still be a live entry point opened by
  **direct URL, email link, or iframe/embed** (common in apps with embedded sub-tools). Dynamic
  navigation (`ListGoToPage`, dynamic page name) also can't be resolved statically. Plugins can run
  **server-side** (social login, DocuSign, Mailchimp, injected headers/scripts) with no visible
  element, or be **headless/global** — active project-wide the moment they're installed with no
  placed element (e.g. **Classify** applies CSS via the element ID; SEO/analytics/header plugins).
  So "no footprint" ≠ "safe to delete" for plugins: the orphaned bucket is a *review* list, and
  known global plugins are routed to a "verify" bucket (curated `HEADLESS_PLUGINS` in the script —
  add newly-found ones there). Config-based plugins are also handled (**Zapier** via
  `settings.zapier.zaps`, `dbconnector` via queries). And **unused PAID plugins** are flagged
  loudest (recurring wasted cost) — pricing comes from a marketplace-researched
  `references/plugin_pricing.json`, shown as a red alert + `💲 paid · price` badge.

  To shrink the page false-positive set, the script does a **second pass**: for every page with no
  id-navigation it searches the page's **name (URL slug)** across all link URLs, Run-JavaScript
  action code, HTML embeds and header scripts, looking for a real app URL to that page
  (`<app-domain>/[version-…/]<slug>`). Pages found this way — typically **OAuth callbacks**
  (e.g. `sso_landing`) and **links in emails/messages** (e.g. `confirm_email`,
  `approve_order`) — are moved out of the deletable list into a "referenced by URL/name — keep" section
  with the evidence snippet. This catches references the id-based scan structurally cannot see.
  A page still can't be proven safe by static analysis alone (bare-name JS navigation and truly
  external links remain undetectable), so keep framing the remainder as *candidates to review*.

Always tell the user: **start with the high-confidence deletions; treat the page list as
candidates to review, not a delete list.** When runtime evidence was attached (step 3b), a
**runs: N×** or **logs: N×** badge overrides the static verdict for that item — something the export
calls unused is running — while **runs: 0** / **logs: 0** only narrows the review (the window, the
workload history and the log retention are finite).

## Plugin names & marketplace links

Marketplace plugins appear in the export only as an opaque id + version (no name). The report shows,
for **every** plugin (unused *and* an in-use reference list), a **clickable link to its marketplace
page** (`https://bubble.io/plugin/<id>`) and — when known — its **display name**. Names come from a bundled registry at
`references/plugin_names.json` (plugin ids are **marketplace-global**, so the same id is the same
plugin in every app — the cache is reused across projects), the short-name label map, or an
`--plugin-names` override file.

When you encounter plugin ids that aren't in the registry yet, resolve them by fetching
`https://bubble.io/plugin/<id>` (WebFetch works — read the page title/name) and add
`"<id>": "<name>"` to `references/plugin_names.json` so future runs (and other projects) get the
name for free. A page that returns only Bubble's generic shell means the plugin is **delisted** —
store `null` for it; the report flags those as "likely delisted," which is itself a strong
safe-to-remove signal. Do this only when a report actually surfaces unknown plugins — don't
pre-resolve the whole marketplace.

## Page-audit spreadsheet: project-specific input — NEVER assume one exists

The audit is based **solely on the `.bubble` export**. Do NOT ask for, search for, or expect a
page-inventory spreadsheet as part of this skill's workflow — that was a one-off artifact of a
single project and belongs to that project only, not to the skill.

The `--pages-csv` flag exists **only** for the case where the user, on their own initiative, hands
you a page-inventory CSV for the specific app being audited (e.g. a status or a planned-action
column per page). In that case pass it with `--pages-csv audit.csv`: the script
auto-detects the page-name column (first column by default; override with `--pages-csv-name-col`)
and any status-like columns (override/add with `--pages-csv-status-col`, repeatable), and each
no-navigation page gets a verdict — **in-use**, **candidate**, or **confirmed-dead** — so the
human signal and the static signal reinforce each other. If no such file is offered, skip this
entirely; it is not a step of the audit.

## Reference model (for debugging or extending)

If a result looks wrong, or you need to adapt to an unusual export, read
`references/reference-model.md`. It documents exactly how each entity is stored and referenced
(page inner-id vs dict-key, `CustomElement.custom_id`, `ScheduleAPIEvent.api_event`,
`option.<name>`, plugin `type` prefixes, the `"style":"<id>"` pattern), the instance-suffix
gotcha, and which top-level sections must be excluded from usage scanning (`_index`, `comments`,
`holding_pen`). Skim it before changing the script.

## Deletion tracker (checkbox column + progress persistence)

Every deletable-entity table has a **"Deleted?" checkbox column** so the user can tick items off as
they remove them from Bubble. Persistence is layered, because a static HTML page cannot auto-write a
file (browsers sandbox that):

- **localStorage** is the live store — ticking a box saves instantly (namespaced by app id) and
  survives reloads, with zero friction and no server. Ticked rows show struck-through.
- **Export → `.md`** (and `.json`) produces a portable, git-committable checklist. The `.md` uses
  `- [x] \`<category>:<id>\` — <label>` lines; the backticked `<category>:<id>` is the stable key
  (survives report regeneration because it's keyed by entity id, not row position).
- **Import** reads a previously exported `.md`/`.json` back into the checkboxes (e.g. on another
  machine, or after regenerating the report).
- **Script `--state <file.md|.json>`** pre-marks already-deleted items when generating a fresh
  report, so the loop closes: *run → tick as you delete → Export .md → commit → next run `--state
  progress.md`.* The `.md`/`.json` is the durable source of truth; localStorage is the in-browser
  working copy.

Recommend this flow to the user: work in the browser (autosaved), and Export the `.md` when they
want a durable/committable record. When regenerating the report later, pass that file to `--state`.

`--state` is repeatable and merges keys from every file. Besides the report's exports it reads the
**cleanup journal** the connected mode writes when deletions are applied through the editor
(`audit/cleanup-applied__<app>.json`, `{"entries": [{key, app_version, merged, …}]}`): an entry
counts as deleted only if it was applied to `test` itself or to a branch that was later merged —
deletions on a branch that was discarded never pre-mark anything.

### Section sign-off — "audit of this section complete" (kept items)

Every section header (1 · Pages … 10 · Removed-plugin refs) has its own checkbox: **"Auditoria
desta seção concluída"**. It means *the owner reviewed this whole section*, even if some rows were
NOT ticked as deleted — some unused entities are kept on purpose (a bulk backend workflow used to
fix data by hand, a page kept as a manual tool, a plugin kept for a planned feature). Ticking a
section:

- marks the section ✓ in the report and tags its unchecked rows as **"mantido"** (kept on purpose);
- makes the console count the section as resolved, so the audit stage reaches **Concluído** when
  every section with findings is either empty or signed off — no need to delete everything;
- records the kept rows explicitly. The JSON export (v2) carries `sections_done` and
  `kept: [{key, label, section}]`; the `.md` export lists a `section:<id>` line per section and
  suffixes kept rows with "mantido de propósito". `--state` restores both the deletions and the
  sign-offs (`section:` keys) when the report is regenerated.

Kept items are **not** deleted from the app, so the lean re-export still contains them. That is
intended: the list travels to step 2, where `unbubble:clone` reads
`audit/bubble_cleanup_progress__<app>.json` and asks the owner, item by item, whether each kept
entity enters the clone/level-up as parity, becomes an operational task, or is descoped with a
dated decision. When you deliver the audit, tell the owner this is how the kept items are handled
downstream, and mention any section signed off with kept items in your summary.

**Console sync.** When the report is opened inside the UnBubble console (`ui/`, served from
`/api/projects/<app>/file`), the tracker auto-saves every change to
`audit/bubble_cleanup_progress__<app>.json` through `PUT /api/projects/<app>/audit-progress` and
shows "● salvo no console"; that file is then the source of truth (it wins over localStorage on
load). Opened as a plain file, the report behaves as before (localStorage + manual Export).

## Output structure (don't reinvent it)

The script already emits a complete, self-contained HTML report — interactive filters, confidence
badges, a deletion-tracker toolbar, per-category tables, a methodology/limits section, light/dark
theming, print CSS. Every category where the audit found nothing renders a green all-clear note
("Todos os X estão em uso.") instead of an empty table, so a clean section is an explicit positive
result, not a blank. Point the user to that file rather than rebuilding a report in the chat. Use the
stdout summary (and `--json`) for your own narration and any follow-up analysis.

The `--json` summary (`summary_version: 2`) gives every finding its tracker **`key`** — the exact
`<category>:<id>` string on the report's checkbox — so downstream tools (the connected-mode cleanup
plan, the console) never re-derive it. Backend and page custom events share the `customevent:`
prefix; their `scope` field (`backend` / `page`) tells them apart. It also carries
`export_integrity` (see step 3) and `provenance` — version, download time and sha256 when the export
came through the connected mode with a `<export>.meta.json` sidecar (the report header shows it too),
and, with `--evidence`, `runtime_evidence` (`by_key`: hits / first and last seen per tracker key and
the `kind` of evidence behind it, `logs` or `runs`; `sources`: each source's window and version read).
