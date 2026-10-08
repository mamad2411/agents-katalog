---
name: markmesh
description: Manage a trademark portfolio through MarkMesh's MCP server — list trademarks, filings and deadlines, run cross-office searches and conflict research for clearance, import or refresh filings from national offices, and register watches that report what changed. Every record carries provenance (source office, fetch time, citable office URL). Use when a user asks about their trademarks, filings, renewal deadlines or clients, wants to search/import a mark from an office (USPTO, EUIPO, DPMA, etc.), wants to check whether a proposed name conflicts with existing marks, or wants to monitor a filing for changes.
license: MIT
metadata:
  author: MarkMesh LTD
  version: "2.0.0"
---

# MarkMesh — trademark portfolio over MCP

This skill drives the **MarkMesh MCP server**. MarkMesh is a multi-tenant
trademark-management platform; this server exposes a customer's portfolio
(trademarks, filings, deadlines, clients) plus live trademark-office
search/import as MCP tools, scoped to the API key's organisation.

If the MarkMesh MCP tools are **not** available in this session, the server
isn't configured — point the user to `SETUP.md` (get an API key from the
MarkMesh app, add the connector to Claude Desktop, restart). Don't invent a
local fallback; there is no local data.

## How auth & scoping work (read this first)

- Every tool runs as the **API key's organisation**. You only ever see that
  org's data — never assume you can reach another firm's or client's records.
- Two key types: **`mm_live_*`** → real production portfolio;
  **`mm_test_*`** → sandbox. Tell the user which one is active if it
  matters. The sandbox isolates the **portfolio** (trademarks, filings,
  clients, watches), NOT office search: `search_office` and
  `search_conflicts` read the same public register corpus either way, so
  a sandbox search returns real marks. Do not tell a user their sandbox
  search results are fake.
- Calls count against the key's rate limit (live ~300/min, test ~60/min) —
  the same budget as the REST API. Don't poll in tight loops; batch your
  reasoning and make deliberate calls.
- Authorisation is enforced server-side by org policies. A tool returning an
  empty list usually means "nothing in your org matches", not an error.

## Tools

**Reads** (each supports `filter`, `sort`, `limit`, `offset` — so one tool
covers both "list everything" and "get one by id"):

- `list_trademarks` — trademarks in the org. Filter by `id`, `name`, etc.
- `list_filings` — filings, one row per trademark × office. Carries status,
  dates, and **deadline fields** (`expiry_date`, `renewal_date`,
  `renewal_status`). Filter by `trademark_id`, `office_id`, `status`.
- `list_clients` — the org's clients (the entities a trademark belongs to).
- `list_organisations` — the org(s) the key can see (its own; plus managed
  orgs for partner/agency keys).

**Office actions:**

- `search_office` — cross-office search for marks matching a term. Read-only;
  results are NOT saved. Args: `query` (required, ≥2 chars), `offices`
  (optional list of ISO codes like `["EU","DE"]` — defaults to a small set),
  `nice_classes` (optional, scope to classes 1-45), `limit`. **The office
  fan-out is ONE call**, not one per office. Returns `results` plus
  `served_from` and `offices` (see "Reading a response" below).
- `search_conflicts` — clearance research. Takes `names` (a shortlist of up
  to 5 candidate names in one call), plus optional `nice_classes`, `offices`,
  `limit`. Returns `candidates_by_name`. Each candidate carries the overlap
  signals SEPARATELY: `text_similarity`, `shared_nice_classes`,
  `same_jurisdiction`. **It returns no verdict and no combined score. Never
  produce one yourself** — see the guardrail below.
- `import_filing_from_office` — pull a filing from an office by `office` +
  `number` and save it. Provide EITHER `trademark_id` (attach to an existing
  trademark) OR `name` + `client_id` (create a new trademark first). Returns
  the imported filing.
- `refresh_filing_from_office` — re-sync a filing's office-sourced fields.
  Asynchronous: it enqueues a sync and returns immediately with
  `sync_status: pending`. Re-fetch the filing a moment later to see updates.

**Watch (monitoring):**

- `list_watches` — the org's active watches, each with the watched filing and
  that filing's provenance.
- `create_watch` — start watching a filing. Args: `filing_id`,
  `recipient_mode` (`all_members` or `specific_user`), and
  `recipient_user_id` when the mode is `specific_user`. A recipient must be a
  member of the same organisation; there is no way to notify an outside
  address.
- `update_watch_recipient` — change who is notified for an existing watch.
- `watch_changes_since` — **poll what changed.** Args: `since` (timestamp of
  your last check). Returns only the watches whose filing recorded events
  after that moment, each carrying just those new events. An empty result
  means nothing changed, NOT that the watch is broken. There is no delete
  tool: you can start and re-target a watch but not remove one.

## Reading a response (provenance + predictability)

Every record carries a `provenance` object. Two of its fields change what you
are allowed to say:

- **`served_from`** — `local` means MarkMesh served it from its own corpus
  (fast, no dependency on the office being up). `external` means it was
  fetched from that office during this call.
- **`citation`** — has a `kind`:
  - `office_record` → a deep link to that exact record. **You may cite it.**
  - `office_portal` → that office publishes no per-record page; the link is
    just its search form. **Do not present it as the source of a specific
    mark.**
  - `unavailable` → no public URL is held.
- **`fetched_at`** — when that data was captured. Use it to tell the user how
  fresh the answer is instead of implying it is live.

Cross-office calls also return an `offices` map: `attempted`, `succeeded`,
`failed`, `timed_out`.

## Common workflows

**"What's expiring soon?"** → `list_filings`, then reason over `expiry_date`
/ `renewal_date` / `renewal_status`. Deadlines live on the filing row; there
is no separate deadlines tool.

**"Do we already own MARK X?"** → `list_trademarks` (filter by name) and/or
`list_filings`. For marks NOT yet in the portfolio, `search_office`.

**"Add EU trademark 0181xxxxx for client Acme"** →
1. `list_clients` to resolve the client's `id` (or confirm it exists).
2. `import_filing_from_office` with `office: "EU"`, `number: "0181xxxxx"`,
   and either `trademark_id` or `name` + `client_id`.
3. Confirm the returned filing's status/dates back to the user.

**"Is NAME safe to use?"** → `search_conflicts` with `names` (their
shortlist), `nice_classes` (ask which classes if they haven't said), and
`offices`. Present candidates grouped by name with their signals and
citations, state which offices failed or timed out, and offer a watch. Do
NOT answer the literal question with yes or no; answer with what exists and
who should judge it.

**"Refresh the status of filing Y"** → `refresh_filing_from_office` with the
filing id, then `list_filings` (filter by that id) after a short pause to
read the updated fields.

## Conventions & guardrails

- **Confirm before importing.** `import_filing_from_office` writes to the
  portfolio. Echo what you're about to import (office, number, target
  trademark/client) and get a nod first, unless the user already said "do it".
- **Search before import.** If the user gives a fuzzy mark name rather than an
  exact application/registration number, `search_office` first, show the hits,
  let them pick.
- **Offices are identified by code** (e.g. `EU` = EUIPO, `DE` = DPMA,
  `US` = USPTO). If unsure which office a number belongs to, ask.
- **No destructive tools exist** in this server — you cannot delete or
  overwrite a trademark/filing via MCP. Direct the user to the MarkMesh web
  app for edits/deletions.
- **Don't fabricate ids.** Resolve `trademark_id` / `client_id` via a read
  tool; never guess a UUID.
- **Check `offices.failed` and `offices.timed_out` before saying anything is
  clear.** An office that did not answer is NOT an office that found nothing.
  Both produce an empty list, and only that map tells them apart. Say "I
  couldn't reach the UK register" rather than "no conflicts in the UK".
- **Never give a clearance verdict.** `search_conflicts` deliberately returns
  no verdict and no combined score, and you must not synthesise one. Do not
  tell a user a name is clear, safe, available, or low-risk, and do not invent
  a percentage. Show the candidates, say which signals fired (text similarity,
  which classes actually overlap, same territory), name what you could not
  check, and leave the judgement to a qualified professional. Clearance turns
  on how goods and services are worded, whether a mark is genuinely in use,
  and how a particular registry has treated similar marks — none of which this
  API returns.
- **`text_similarity` is blunt.** It is text distance only: no phonetics, no
  transliteration, no visual similarity of figurative marks. A low score means
  "not textually close", never "no conflict".
- **Cite the register, not MarkMesh.** Quote `citation.url` only when
  `citation.kind` is `office_record`. Linking five different candidates to one
  office search form is not five citations.
- **Watch instead of re-running.** If a user cares about a mark over time, end
  with `create_watch` and poll `watch_changes_since`, rather than telling them
  to ask again later. The conflict that matters is often an application
  published after the search.

See `reference/tools.md` for the full argument reference and `SETUP.md` for
connection setup.
