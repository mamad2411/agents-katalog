---
name: sillage-api
description: >
  The MCP-less fallback. Drives a Sillage workspace over the plain v2 REST API when the Sillage MCP
  can't be installed — teaches Claude how to authenticate with an `sk_live_` key and call every
  endpoint (persona, target accounts, coverage/account-mapping, watchlists, agents, signal runs,
  signals, contents) to run the same setup and edit loops the MCP skills describe. Use when there is
  no MCP connection, when a client is on an editor without MCP support, or when you must script Sillage
  from curl/HTTP. Use when you hear: "no MCP", "can't install the MCP", "use the API instead", "call
  the Sillage API", "curl Sillage", "REST fallback", "sk_live", "set up the workspace over HTTP".
metadata:
  owner: pf@getsillage.com
  version: 1.1.0
  model-tier: sonnet
  provider: Sillage REST API v2 (https://api.getsillage.com/api/v2)
  pairs-with: [sillage-onboarding, sillage-manage-workspace, sillage-help]
---

# Sillage API — drive a workspace over REST when there's no MCP

This is the **fallback transport**. The Sillage skills normally drive the workspace through the
[MCP server](https://api.getsillage.com/api/mcp/v2). When a client **can't install the MCP** — an
editor without MCP support, a locked-down environment, a pure-HTTP/curl script — everything the MCP
does is also reachable over the plain **v2 REST API**. This skill teaches Claude how.

**This skill is transport only.** The _strategy_ — how to expand a vague ICP into a sharp persona,
which keywords catch buying intent, what to track, how to reconcile a live workspace — still lives in:

- `sillage-onboarding` — decide _what_ the targeting should be (interview + expansion).
- `sillage-manage-workspace` — the setup loop and the edit/write-safety rules, described against MCP tools.
- `sillage-help` — the mental model and glossary (persona, coverage, watchlist, signal run, detection).

Read those for the _what_ and _why_. Come here for the _how_ over HTTP. Every rule in
`sillage-manage-workspace` (persona is replace-whole, the target list appends, coverage doesn't
refresh itself, confirm-before-write / poll-before-read) holds identically here — only the calls change.

## When to use

- The MCP is not connected and can't be, but you have (or can generate) a workspace API key.
- You're scripting Sillage from curl, a CI job, or any HTTP client.
- You need to translate an MCP-tool instruction into its REST equivalent → see
  `reference/mcp-to-rest-map.md`.

## When NOT to use

- The MCP **is** available → use it and the MCP skills; it's higher-level and safer.
- You haven't decided the targeting yet → `sillage-onboarding` first.
- You just want to understand the product → `sillage-help`.

## The five things that trip up every REST caller (read before any call)

1. **Always use v2.** Every call goes to `https://api.getsillage.com/api/v2` with
   `Authorization: Bearer sk_live_...`. **`/api/v1` is legacy — don't use it.** If an existing
   integration is on v1, migrate it to v2. The workspace is inferred from the key — never in the URL.
   `sk_live_` is a direct-client workspace key, generated at
   <https://www.getsillage.com/app/settings/api-keys> and shown only once; `mk_live_` is a partner
   master key. `401` = key missing/invalid/revoked. **If the user has no key yet, walk them through
   getting and setting one** — the step-by-step is in `reference/conventions.md`.
2. **Writes that enqueue work return `202` — then you poll.** Adding accounts, enriching a company,
   and launching a run are all asynchronous. The `202` only means _accepted_. Poll the matching status
   endpoint to a **terminal** state before you read results. Details and the terminal states are in
   `reference/conventions.md`.
3. **Integer ids are environment-specific and not portable.** `id`, `company_id`, `agent_id`,
   `signal_request_id`, mapping ids — all numeric SQL ids that only mean anything in prod. Never store
   them across environments; re-resolve from a human identifier (domain / LinkedIn URL / handle).
4. **Persona is replace-whole; the target list is not.** `PUT /persona` overwrites the entire persona
   (omitted fields become unset) — so **GET → merge your change into the full object → PUT**. The
   target account list **merges** on `POST /top-account-list/accounts` (existing kept) but is **wiped
   and replaced** by `POST /top-account-list`. Know which one you're calling.
5. **Errors are RFC 9457 `application/problem+json`.** Read `detail` and the `errors` map, don't retry
   blindly. `403` = the feature isn't enabled for the workspace (surface it). `402` = out of credits.
   `429` = rate-limited; back off using the `X-RateLimit-Remaining` header. Full error/rate-limit
   handling in `reference/conventions.md`.

## Setup loop — stand up a workspace over REST

Same order as `sillage-manage-workspace` (persona defines targeting before lists ingest). Start with
`GET /setup-state` — the REST equivalent of the MCP's `get_setup_state` — to see which of the four
flags (`persona_set`, `list_uploaded`, `ingestion_complete`, `has_contents`) is still missing.

1. **Persona** — `GET /persona` (null = unset) → merge → `PUT /persona`.
2. **Target accounts** — `POST /top-account-list/accounts` `{accounts:[{domain}|{linkedin_url}]}` →
   `202` → poll `GET /top-account-list/status` to `completed`. Check misses at
   `GET /top-account-list/accounts/not-found`.
3. **Coverage (people)** — `POST /enrich-company-mapping` `{domain}` per account → `202 {request_id}`
   → poll `GET /account-mapping/{request_id}/stage` to `completed`. Read people via
   `GET /company-mappings` then `GET /company-mappings/{mapping_id}`.
4. **Watchlists** — `POST /watchlists` `{type,title}` → `POST /watchlists/{kind}/{watchlist_id}/entities`
   (LinkedIn URL/handle preferred; `domain` only on company lists, ≤ the documented cap per call).
5. **Agents** — `POST /agents` `{name,type,parameters}`. Watchlist-type agents auto-create + bind a
   list unless you pass `watchlist_id`.
6. **Run** — `POST /workspace/signal-runs` `{agent_id}` → array of `{signal_request_id}` (keyword → 1,
   watchlist → 2: inbound + outbound) → poll `GET /workspace/signal-runs/{id}` to `completed` /
   `completed_partial` → read `GET /workspace/signals` (cursor-paginated) and `GET /workspace/signals/count`.

The full parameter/response detail for each call is in `reference/endpoint-catalog.md`; copy-paste curl
for the whole loop is in `reference/recipes.md`.

## Edit loop — change a live workspace over REST

Never write blind. **Snapshot → diff → patch the one axis that's off**, exactly as
`sillage-manage-workspace` prescribes.

1. **Snapshot:** `GET /persona`, `GET /agents`, `GET /watchlists`, `GET /top-account-list/accounts`.
2. **Diff** each axis (persona / accounts / watchlists / agents) → match / mismatch / missing.
3. **Patch** with the right write:
   - Persona → GET → merge → `PUT /persona` (whole object).
   - Accounts → `POST /top-account-list/accounts` to add, `POST /top-account-list/accounts/remove` or
     `DELETE /top-account-list/accounts/{id}` to remove.
   - Agent keywords / enable / rename / rebind → **one** call: `PUT /agents/{agent_id}` (the REST
     endpoint merges what MCP splits across `configure_agent` + `bind_agent_watchlist`).
   - Then re-trigger coverage (`POST /enrich-company-mapping`) or a run (`POST /workspace/signal-runs`)
     if the change should surface new results.

## Close with a summary

After a setup or edit, report plainly — same shape as the MCP skills:

```
## What I changed
<persona / accounts / watchlists / agents — before → after, in plain language>

## What's running now
<agents enabled · runs launched (signal_request_ids) · ingestion/coverage status>

## Waiting on
<anything still 202/processing, which status endpoint to poll, and when to re-check>
```

## Reference

- `reference/conventions.md` — auth, keys, base URL, pagination (offset + the signals cursor
  divergence), the async/poll model with every terminal state, RFC 9457 errors, rate limits, the
  identifier waterfall.
- `reference/endpoint-catalog.md` — every v2 endpoint, grouped, with method, path, key params, body,
  and write-class. Includes the account-mapping and company endpoints missing from the published
  OpenAPI spec.
- `reference/mcp-to-rest-map.md` — each `sillage_v2_*` MCP tool → its REST endpoint(s), so any
  instruction written against the MCP translates 1:1.
- `reference/recipes.md` — copy-paste curl for the setup loop, the edit loop, checking setup-state,
  and the common reads.

## Canonical docs (fetch when in doubt)

This skill mirrors the official docs as of its version. If something here looks stale or an endpoint
misbehaves, fetch the live source — it's authoritative:

- **API docs home:** <https://www.getsillage.com/docs/api>
- **Quickstart:** <https://www.getsillage.com/docs/getting-started/api-quickstart>
- **Get an API key:** <https://www.getsillage.com/app/settings/api-keys>
- **OpenAPI spec (JSON):** <https://api.getsillage.com/api/v1/docs/spec> — note it currently **omits**
  the three account-mapping endpoints (`POST /enrich-company-mapping`, `GET /company-mappings`,
  `GET /company-mappings/{mapping_id}`) and `GET /companies/{id}`, which are live and covered in
  `reference/endpoint-catalog.md`.
