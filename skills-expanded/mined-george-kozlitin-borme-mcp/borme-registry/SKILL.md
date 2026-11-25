---
name: borme-registry
description: Answer questions about Spanish companies from the official commercial registry gazette (BORME, Boletín Oficial del Registro Mercantil) through the BORME MCP server at mcp.bormeapi.com. Use when the user wants to look up or check a Spanish company (empresa, sociedad) or asks about its history, incorporation (constitución), director or officer appointments and terminations (nombramientos, ceses, administrador, apoderado, consejero), insolvency (concurso de acreedores), dissolution, liquidation or extinction, registered-office or name changes (domicilio social, denominación), capital changes, mergers, whether it is still active, a NIF/CIF tax ID, who owns a brand or trading name (marca, nombre comercial), or what was published in BORME on a given day or in a given province.
---

# BORME - the gazette of Spain's commercial registry

The `borme` MCP server holds the company notices of BORME Section A since
2009, parsed into typed events, plus tax-ID and trademark lookups. This
skill says which tool to call, how to chain them, and how to report what comes
back. Each tool's description and parameter schema explain its parameters;
read them too.

## Connect

The hosted endpoint is `https://mcp.bormeapi.com/mcp` (Streamable HTTP). It
works without a key on the free plan. With a key, send it in the `X-API-Key`
header:

- Claude Code:
  `claude mcp add --transport http --scope user --header "X-API-Key: YOUR_KEY" borme https://mcp.bormeapi.com/mcp`
- Clients configured with JSON (Cursor's `mcp.json` and similar):
  `{"mcpServers": {"borme": {"url": "https://mcp.bormeapi.com/mcp", "headers": {"X-API-Key": "YOUR_KEY"}}}}`
- Assistants with custom connectors that sign in with OAuth (Claude.ai,
  ChatGPT, Copilot): `https://mcp.bormeapi.com/mcp/oauth`. The user signs in
  with their BORME API account and the plan of that account applies; there is
  no key to paste.

Keys: https://bormeapi.com/account. Plans and prices: https://bormeapi.com/#pricing.
Setup for each client: https://bormeapi.com/mcp.

If the `borme` tools are not available in this session, say the BORME MCP
server is not connected, give the user the lines above, and do not answer from
memory.

## What each plan includes

- **No key (free):** `search_events`, `company_history` and `daily_digest`
  over the last 7 days; `search_companies` (first 5 results);
  `list_act_types` and `registry_stats`. 50 calls a day per IP address.
- **basic:** the last 365 days, plus `company_by_nif`, `brand_owner` and
  `company_brands`.
- **pro:** everything in basic, with the full history back to 2009.
- **risk:** everything in pro, plus `recent_signals`.

When an answer carries `plan_window`, the plan's window was applied
(`company_history` carries it on every free or basic answer). Tell the user
once, in one sentence, and say what covers the rest: a key for the last 365
days (basic), pro for the full history. Do not retry with older dates - the
server cuts them the same way - and do not take an empty result as proof that
nothing happened earlier.

A refusal that names a plan, or says a company's notices lie outside the
window, is not a server failure: relay its message, say which plan covers it,
and do not retry.

## Pick the tool

- **"How much data is there / how fresh is it?"** → `registry_stats`. Call it
  before you trust a date filter for an unusual period.
- **A company name** → `search_companies` first, then `company_history` with
  the slug of the company the user means. A `fuzzy` match is a lead, not an
  identification; say so.
- **One company's story** → `company_history`. Pass a slug; if you only have
  a name, use `search_companies` first. If `company_history` is given a name
  and returns a list of candidate slugs, show them and let the user choose; do
  not pick one yourself.
- **Events across many companies** (by date, province, event type, or a
  substring of the company name) → `search_events`.
- **"What happened in BORME on day X?"** → `daily_digest`.
- **A NIF/CIF tax ID** → `company_by_nif`, then `company_history` with the
  returned slug.
- **A brand or trading name** that is not the registered company name →
  `brand_owner`, then `company_history` with the slug.
- **What trading names a company uses, or which trademarks it sells under** →
  `company_brands` with the slug.
- **Latest risk signals** (insolvency declarations, phoenix companies, mass
  officer exits, AEAT debtor-list entries) → `recent_signals`. It returns a
  sample, at most 10 rows from the last 7 publication days: never present it
  as a complete list.

## Filters that work first time

- **Event types are enums.** Call `list_act_types` once and use its
  `act_type` values (`INCORPORATION`, `APPOINTMENTS`, `TERMINATIONS`,
  `INSOLVENCY_DECLARATION`, …). Do not invent enum names from the Spanish
  wording.
- **Insolvency:** filter on both `INSOLVENCY_DECLARATION` and
  `INSOLVENCY_STATUS`. An `INSOLVENCY_STATUS` (*Situación concursal*) notice
  can record any stage of the proceedings, among them a request for a
  declaration, the declaration, the appointment of the insolvency
  administrator, the opening of the liquidation phase and the conclusion:
  read `payload` before you say a company was declared insolvent; otherwise
  call it an insolvency-proceedings notice. The older suspension-of-payments
  and bankruptcy procedures the registry still records are
  `SUSPENSION_OF_PAYMENTS` and `BANKRUPTCY_LEGACY`.
- **Provinces** take the name BORME prints, without regard to accents or case:
  `MADRID`, `CADIZ`. Either name of a bilingual pair works (`VALENCIA` or
  `VALÈNCIA`), and so do common alternatives (`VIZCAYA`, `GERONA`, `SEVILLE`).
- **Dates** are `YYYY-MM-DD` and refer to the BORME publication day, not the
  day the company took the decision. The registry inscription date is in
  `registral.reg_date`.
- **Name search** needs at least three letters or digits. A very common word
  matches thousands of companies; `company_name_match` then says the answer
  is partial. Narrow the search with a province or a date range.
- **`count` in `search_events` is the size of this answer, not a total.** The
  tool returns the newest `limit` events (default 50, at most 200) and has no
  `offset`. When `count` equals `limit` there are more: to count a period,
  split the date range (day by day if needed) until every call returns fewer
  than `limit`, then add up. National totals per event type for one day are
  in `daily_digest`.
- `company_history` pages with `offset` and returns `next_offset`.

## Report it faithfully

- **Registry data stays as published.** Company names, people's names,
  addresses and `act_type_raw` / `role_raw` are quoted as BORME printed them.
  Translate the labels around them into the user's language: event types,
  roles and powers of attorney (`PROXY_HOLDER` is an *apoderado*, a person
  holding a power of attorney), statuses and headings. For a Spanish-speaking
  user, take act-type labels from the `spanish` field of `list_act_types` and
  spell out the registry's role abbreviations (`Adm. Solid.` → administrador
  solidario) instead of translating the English enums back.
- **BORME records changes, not the current state.** Before saying who holds a
  post now, check later events for a termination or a new appointment to the
  same post, and say "according to BORME notices up to <date of the latest
  event>". Under a plan window, say the appointment may predate it.
- **A NIF miss means "not matched yet"**, not "this company does not exist":
  BORME has no tax-ID field and the mapping covers only some of the
  companies. The exception is the reason `nif_check_character_failed`: that
  identifier fails the official check-character rule and was never issued.
  Say so, and pass on the identifier with a valid check character
  (`corrected_check_character`, which assumes the error is in the last
  character) and any `did_you_mean` companies; do not present either as the
  company's NIF.
- **`nif_caveat`** means the tax ID's first letter (the entity-type letter)
  disagrees with the legal form in the company's name. Show the caveat; do
  not present the match as settled.
- **`ambiguous: true`** means several companies are candidates. List them and
  ask which one the user means.
- **Trademarks are not names.** In `brand_owner` and `company_brands`, a
  `commercial_name` is another name for the business; a `trademark` is
  something it sells. Never say a company "is called" one of its trademarks.
  Brands are linked to companies by the holder's name (the patent office
  publishes no tax IDs), so present a hit as strong evidence, not as a
  registry-confirmed fact.
- **Risk signals are flags, not findings.** Say a company "was flagged as a
  possible phoenix company" or "appeared on the AEAT debtor list of <year>",
  never that it "is" a phoenix company or "owes" tax; name the events behind
  the flag and their dates.
- **Counts from `registry_stats` come from the latest hourly snapshot, with
  planner estimates as a fallback if no snapshot exists.** The response does
  not identify which source was used or provide a snapshot timestamp. Explain
  these limits when presenting the counts; do not describe them as live counts
  or assign them a specific timestamp.
- Give the BORME publication date and the `borme_id` of every event you cite,
  so the user can find the notice.

## Not in this server

- Annual accounts and balance sheets: BORME publishes registry events, not
  accounts.
- BORME Section C notices (legal announcements such as general-meeting calls
  and merger announcements).
- Sole traders (*autónomos*) and companies that never appeared in Section A.
- Notices published before 2009.

Say so instead of guessing, and do not fill the gap from memory.
