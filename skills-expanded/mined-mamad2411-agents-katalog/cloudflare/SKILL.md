---
name: cloudflare-skill
description: Work with Cloudflare via the official cf CLI — find the right cf command, list zones, list/create/edit/delete DNS records, query the GraphQL Analytics API (zone traffic, Web Analytics/RUM), and run any other cf command (Workers, R2, KV, D1, Pages, cache). Output is parsed JSON.
allowed-tools: "cloudflare"
metadata:
  author: opencompany
  version: "2.0"
  category: deployment

---

# Cloudflare Skill

Wrapper over the official [Cloudflare CLI](https://developers.cloudflare.com/cf/)
(`cf`, in open beta — "the next version of Wrangler"). Typed operations
cover the core zone and DNS flows, `search_commands` finds any other
command, and `custom` runs it. cf prints the API result as JSON, so
results come back parsed in `result`.

## Tool: cloudflare

### Operations

| Operation | Purpose | Key fields |
|---|---|---|
| `whoami` | Who the CLI acts as, and the accounts it can use | — |
| `search_commands` | Find the cf command for a task (5 matches) | `search_query` |
| `zones_list` | List / filter zones | `name_filter`, `account_id`, `page`, `per_page` (all optional) |
| `dns_records_list` | DNS records of a zone | `zone`; optional `name_filter` (full record name), `record_type`, `page`, `per_page` |
| `dns_record_create` | Create a record | `zone`, `record_body` (the record as JSON) |
| `dns_record_edit` | Change some fields of a record | `zone`, `record_id`, `record_body` (only the changed fields) |
| `dns_record_delete` | Delete a record | `zone`, `record_id` |
| `graphql_query` | GraphQL Analytics API | `graphql_query`, `graphql_variables` (JSON) |
| `custom` | Any other cf command | `command` — what you would type after `cf ` |

`zone` takes a zone ID or the domain (`example.com`). `account_id` matters
when the login can see more than one account: commands then fail with
"More than one account available ..." until it is set. `whoami` lists
the accounts.

### Response

```json
{
  "operation": "dns_records_list",
  "success": true,
  "result": [{ "id": "372e67954025e0ba6aaa6d586b9e0b59", "type": "A", "name": "www.example.com", "content": "192.0.2.1", "proxied": true, "ttl": 1 }]
}
```

Parsed JSON lands in `result`; text output (a BIND zone export, for
example) lands in `stdout`; `stderr_tail` carries cf's status lines when
there are any. Lists return one page: use `page` / `per_page` and keep
going until a page comes back shorter than `per_page`. On failure the
tool raises an error carrying cf's own message — surface it verbatim.

## Finding commands

cf covers almost the whole Cloudflare API: more than 2,900 commands
shaped `cf <product> [group] <verb>`, with the verbs `list`, `get`,
`create`, `edit` (partial update), `update` (overwrite) and `delete`.
Don't guess command names:

1. Search, describing the task generically:
   `{ "operation": "search_commands", "search_query": "purge cache for a zone" }`.
   Describe the action and resource only — never names, domains, emails
   or IDs.
2. Check the request shape: run the match with `cf` replaced by
   `schema`, e.g. `{ "operation": "custom", "command": "schema cache purge" }`.
   It lists the path, query parameters and body fields.
3. Preview with `--dry-run` (prints the HTTP request; nothing is sent),
   then run the command.

## DNS records

`record_body` is the API's DNS record JSON:

```json
{ "operation": "dns_record_create", "zone": "example.com", "record_body": "{\"type\":\"A\",\"name\":\"www\",\"content\":\"192.0.2.1\",\"ttl\":1,\"proxied\":true}" }
```

Common fields: `type` (A, AAAA, CNAME, TXT, MX, NS, SRV, CAA), `name`
(`@` for the zone apex, or a subdomain), `content`, `ttl` (`1` =
automatic), `proxied` (the orange cloud), `priority` (MX / SRV),
`comment`. Find record IDs with `dns_records_list` (narrow it with
`name_filter: "www.example.com"` and `record_type: "A"`), then:

```json
{ "operation": "dns_record_edit", "zone": "example.com", "record_id": "372e67954025e0ba6aaa6d586b9e0b59", "record_body": "{\"content\":\"192.0.2.2\"}" }
{ "operation": "dns_record_delete", "zone": "example.com", "record_id": "372e67954025e0ba6aaa6d586b9e0b59" }
```

`dns_record_edit` changes only the fields you pass. To replace a record
entirely, use `custom` with
`dns records update <record-id> --zone <zone> --body '<the full record>'`.
Several changes in one request:
`dns records batch --zone <zone> --posts '[...]' --patches '[...]' --deletes '[{"id":"..."}]'`.
Zone file: `dns records export --zone <zone>` (BIND text in `stdout`).

## Other products via custom

```json
{ "operation": "custom", "command": "zones get --zone example.com" }
{ "operation": "custom", "command": "cache purge --zone example.com --body '{\"purge_everything\":true}'" }
{ "operation": "custom", "command": "workers list" }
{ "operation": "custom", "command": "r2 buckets list" }
{ "operation": "custom", "command": "r2 objects list --bucket-name my-bucket --prefix logs/" }
{ "operation": "custom", "command": "kv namespaces list" }
{ "operation": "custom", "command": "kv keys list --namespace-id <namespace id>" }
{ "operation": "custom", "command": "d1 list" }
{ "operation": "custom", "command": "d1 query <database id> --sql 'SELECT * FROM users LIMIT 10'" }
{ "operation": "custom", "command": "pages list" }
{ "operation": "custom", "command": "accounts list" }
```

Rules for `custom`:

- **Destructive commands need `--force`.** Without it cf asks for a
  confirmation that a workflow cannot give, and the tool reports that
  nothing ran. Confirm with the user before adding `--force` unless
  they asked for the deletion.
- Request bodies go in `--body '<json>'` (single quotes around the
  JSON; the command is split like a shell command) or
  `--body @file.json`. Relative paths resolve in the workflow workspace.
- Account-scoped commands (Workers, R2, KV, D1, Pages) use `account_id`;
  most commands have no `--account-id` flag. Zone-scoped commands take
  `--zone <zone ID or domain>`.
- Sign-in (`auth login`, `auth logout`) is not available here; it lives
  in Credentials -> Cloudflare. `auth whoami` works (or use the `whoami`
  operation).
- Project commands (`init`, `build`, `dev`, `deploy`) need Node.js
  22.18+ and a project directory. OpenCompany runs cf on bun, so prefer
  the API commands.

## Analytics — the GraphQL Analytics API

Cloudflare's legacy Zone Analytics REST API was deprecated (2021) and
the DNS analytics REST API is scheduled for removal (2026-12-01); the
official replacement for both is the GraphQL Analytics API. cf has no
GraphQL command, so the `graphql_query` operation POSTs to the official
endpoint `api.cloudflare.com/client/v4/graphql`.

**It needs a credential stored in Credentials -> Cloudflare** (the CLI
login stays inside the cf CLI): an API token with `Account > Account
Analytics > Read`, plus `Zone > Analytics > Read` for zone-scoped
queries, or the Global API Key with the Account Email.

Zone HTTP traffic (official migration-guide query, current dataset):

```json
{
  "operation": "graphql_query",
  "graphql_query": "query Sample($zoneTag: string, $start: Time, $end: Time) { viewer { zones(filter: {zoneTag: $zoneTag}) { series: httpRequestsAdaptiveGroups(limit: 5, orderBy: [count_DESC], filter: {datetime_geq: $start, datetime_lt: $end, requestSource: \"eyeball\"}) { count avg { sampleInterval } sum { visits edgeResponseBytes } dimensions { coloCode } } } } }",
  "graphql_variables": "{\"zoneTag\": \"<zone id>\", \"start\": \"2026-07-01T00:00:00Z\", \"end\": \"2026-07-15T00:00:00Z\"}"
}
```

Web Analytics / RUM (account-scoped datasets:
`rumPageloadEventsAdaptiveGroups`, `rumPerformanceEventsAdaptiveGroups`,
`rumWebVitalsEventsAdaptiveGroups`):

```json
{
  "operation": "graphql_query",
  "graphql_query": "query Rum($accountTag: string, $start: Time, $end: Time) { viewer { accounts(filter: {accountTag: $accountTag}) { rumPageloadEventsAdaptiveGroups(limit: 100, orderBy: [count_DESC], filter: {datetime_geq: $start, datetime_lt: $end}) { count sum { visits } dimensions { requestPath } } } } }",
  "graphql_variables": "{\"accountTag\": \"<account id>\", \"start\": \"2026-07-01T00:00:00Z\", \"end\": \"2026-07-15T00:00:00Z\"}"
}
```

DNS analytics: `dnsAnalyticsAdaptive` / `dnsAnalyticsAdaptiveGroups`
(zone- and account-scoped). Notes: a query spans at most 10 zones or 1
account; the user quota is 300 queries per 5 minutes; wide time ranges
are sampled (multiply by `sampleInterval` for estimates). Web Analytics
site configuration is a cf command: `rum site-info list`,
`rum site-info get <site id>`, `rum site-info create --body '...'`
(with `account_id`).

## Authentication

Two independent paths; the API token wins when both exist (cf's
documented resolution order):

1. **Login** — Credentials -> Cloudflare -> Login. Cloudflare's device
   page opens and the modal shows a one-time code; approve the request
   in any browser (this also works when OpenCompany runs on a remote
   server). Or run `cf auth login` in a terminal on the server.
2. **API token** — pasted in the credentials panel (or
   `CLOUDFLARE_API_TOKEN` in the server environment; the panel value
   wins). Needed for unattended use and for `graphql_query`. Create one
   at dash.cloudflare.com/profile/api-tokens with the permission groups
   the task needs. A Global API Key (cfk_) in the panel works only for
   `graphql_query` — the cf CLI does not accept Global API Keys.

If a command fails because nothing is signed in, the tool stops and asks
the owner to connect Cloudflare. A 403 means the token or login lacks a
permission — tell the user which permission group is missing; never ask
them to paste a token in chat.

## Best practices

1. **Run `whoami` first** when the auth state or the account is unknown.
2. **Pass `zone` as the domain or the zone ID**, and set `account_id`
   when several accounts exist.
3. **Use `search_commands`, `schema` and `--dry-run`** instead of
   guessing commands.
4. **Confirm destructive operations** (record deletes, any `--force`
   command) with the user unless they explicitly asked.
5. **Surface cf error messages verbatim** — don't paraphrase.
