---
name: make
description: Make.com API — scenarios, blueprints, connections, webhooks, data stores, scenario execution, blueprint JSON structure, and Make-to-n8n migration patterns. Auto-triggers on Make.com, Make API, scenario management, and automation migration tasks.
disable-model-invocation: false
user-invocable: true
argument-hint: "task description"
---

# Make.com API Skill

Complete reference for Make.com API and blueprint management.

**As of March 2026.** API v2 (current).

---

## 1. API Basics

```bash
BASE="https://eu1.make.com/api/v2"

# Auth header
-H "Authorization: Token $MAKE_API_KEY"

# All list endpoints support pagination
?pg[limit]=100&pg[offset]=0

# Team filter (required for list endpoints)
?teamId=YOUR_TEAM_ID
```

**MCP:** Use the official Make.com cloud MCP at `https://eu1.make.com/mcp/stateless` (Streamable HTTP, Bearer-header auth). Replace `eu1` with your zone (`eu2`/`us1`/`us2`). The legacy `D1DX/make-mcp` stdio fork is retired as of 2026-05-08.

---

## 2. Scenarios

### List Scenarios

```bash
curl -s "$BASE/scenarios?teamId=YOUR_TEAM_ID&pg[limit]=100" \
  -H "Authorization: Token $MAKE_API_KEY"
```

Response fields: `id`, `name`, `isEnabled`, `scheduling` (type, interval), `folderId`, `lastEdit`, `usedPackages`.

### Get Scenario Details

```bash
curl -s "$BASE/scenarios/SCENARIO_ID" \
  -H "Authorization: Token $MAKE_API_KEY"
```

### Activate / Deactivate

```bash
# Activate
curl -X POST "$BASE/scenarios/SCENARIO_ID/start" \
  -H "Authorization: Token $MAKE_API_KEY"

# Deactivate
curl -X POST "$BASE/scenarios/SCENARIO_ID/stop" \
  -H "Authorization: Token $MAKE_API_KEY"
```

### Create a Scenario

```bash
curl -X POST "$BASE/scenarios" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "teamId": YOUR_TEAM_ID,
    "name": "My New Scenario",
    "blueprint": "{\"name\":\"My Scenario\",\"flow\":[...]}",
    "scheduling": {"type": "indefinitely", "interval": 900}
  }'
```

### Delete a Scenario

```bash
curl -X DELETE "$BASE/scenarios/SCENARIO_ID?confirmed=true" \
  -H "Authorization: Token $MAKE_API_KEY"
```

---

## 3. Blueprints

Blueprints are JSON that define the scenario's module graph.

### Get Blueprint

```bash
curl -s "$BASE/scenarios/SCENARIO_ID/blueprint" \
  -H "Authorization: Token $MAKE_API_KEY" \
  | jq '.response.blueprint'
```

### Push Blueprint

**Critical:** Blueprint value must be a JSON-encoded string, not raw JSON.

```bash
blueprint=$(cat blueprint.json)
curl -X PATCH "$BASE/scenarios/SCENARIO_ID" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H "Content-Type: application/json" \
  --data "$(jq -n --arg bp "$blueprint" '{"blueprint": $bp}')"
```

### Blueprint JSON Structure

```json
{
  "name": "Scenario Name",
  "flow": [
    {
      "id": 1,
      "module": "gateway:CustomWebHook",
      "version": 1,
      "parameters": {
        "hook": 12345,
        "maxResults": 1
      },
      "mapper": {},
      "metadata": {
        "designer": {"x": 0, "y": 0}
      }
    },
    {
      "id": 2,
      "module": "builtin:BasicRouter",
      "version": 1,
      "routes": [
        {
          "flow": [
            {
              "id": 3,
              "module": "http:ActionSendData",
              "version": 3,
              "parameters": {},
              "mapper": {
                "url": "https://api.example.com",
                "method": "POST",
                "body": "{{1.body}}"
              },
              "filter": {
                "name": "Route 1 Filter",
                "conditions": [[{
                  "a": "{{1.type}}",
                  "b": "webhook",
                  "o": "text:equal"
                }]]
              }
            }
          ]
        }
      ]
    }
  ],
  "metadata": {
    "version": 1,
    "scenario": {"roundtrips": 1, "maxErrors": 3}
  }
}
```

### Key Module Names

| Module ID | Purpose |
|-----------|---------|
| `gateway:CustomWebHook` | Webhook trigger |
| `builtin:BasicRouter` | Router (multiple routes) |
| `builtin:BasicFeeder` | Iterator (loop over array) |
| `builtin:BasicAggregator` | Array aggregator |
| `http:ActionSendData` | HTTP request |
| `json:ParseJSON` | Parse JSON string |
| `json:TransformToJSON` | Stringify to JSON |
| `airtable2:ActionSearchRecords` | Airtable search |
| `airtable2:ActionCreateRecord` | Airtable create |
| `airtable2:ActionUpdateRecord` | Airtable update |
| `openai-gpt-3:CreateCompletion` | OpenAI chat completion |
| `google:ActionSendEmail` | Gmail send |
| `tools:SetVariable` | Set variable |
| `tools:SetMultipleVariables` | Set multiple variables |
| `util:FunctionSleep` | Sleep/delay |

### Blueprint Expression Syntax

```
{{1.body}}              — output of module 1, field "body"
{{2.data.name}}         — nested field access
{{ifempty(1.value; "default")}} — fallback
{{lower(1.currency)}}   — string functions
{{formatDate(1.date; "YYYY-MM-DD")}} — date formatting
{{parseDate(1.date; "DD/MM/YYYY")}}  — date parsing
{{toNumber(1.amount)}}  — type conversion
{{length(1.items)}}     — array length
{{emptystring}}         — empty string constant
```

### Router Filters

```json
{
  "filter": {
    "name": "Has date",
    "conditions": [
      [
        {"a": "{{1.date}}", "o": "exists"},
        {"a": "{{1.type}}", "b": "invoice", "o": "text:equal"}
      ]
    ]
  }
}
```

Conditions are AND within inner arrays, OR between outer arrays.

Operators: `text:equal`, `text:notEqual`, `text:contain`, `text:startsWith`, `number:equal`, `number:greater`, `exists`, `notExist`, `array:contain`.

### Error Handlers

```json
{
  "id": 5,
  "module": "http:ActionSendData",
  "onerror": [
    {
      "id": 6,
      "module": "builtin:Ignore",
      "version": 1
    }
  ]
}
```

Error handler types: `builtin:Ignore`, `builtin:Resume`, `builtin:Rollback`, `builtin:Break`, `builtin:Commit`.

---

## 4. Connections

```bash
# List all connections
curl -s "$BASE/connections?teamId=YOUR_TEAM_ID" \
  -H "Authorization: Token $MAKE_API_KEY"

# Get specific connection
curl -s "$BASE/connections/CONNECTION_ID" \
  -H "Authorization: Token $MAKE_API_KEY"

# Verify connection works
curl -X POST "$BASE/connections/CONNECTION_ID/test" \
  -H "Authorization: Token $MAKE_API_KEY"
```

---

## 5. Webhooks (Hooks)

```bash
# List webhooks
curl -s "$BASE/hooks?teamId=YOUR_TEAM_ID" \
  -H "Authorization: Token $MAKE_API_KEY"

# Get webhook details
curl -s "$BASE/hooks/12345" \
  -H "Authorization: Token $MAKE_API_KEY"

# Create a webhook
curl -X POST "$BASE/hooks" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Webhook","teamId":YOUR_TEAM_ID,"typeName":"gateway:CustomWebHook"}'

# Delete a webhook
curl -X DELETE "$BASE/hooks/12345?confirmed=true" \
  -H "Authorization: Token $MAKE_API_KEY"
```

Response includes `url` (production webhook URL to use in external systems).

---

## 6. Data Stores

```bash
# List data stores
curl -s "$BASE/data-stores?teamId=YOUR_TEAM_ID" \
  -H "Authorization: Token $MAKE_API_KEY"

# Get data store records
curl -s "$BASE/data-stores/12345/data" \
  -H "Authorization: Token $MAKE_API_KEY"

# Add record
curl -X POST "$BASE/data-stores/12345/data" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data":{"key":"value"}}'
```

---

## 7. Execution History

```bash
# List executions for a scenario
curl -s "$BASE/scenarios/SCENARIO_ID/logs?pg[limit]=10" \
  -H "Authorization: Token $MAKE_API_KEY"
```

Status values: `success`, `warning`, `error`.

---

## 8. Incomplete Executions (DLQ)

When a scenario errors with **Store Incomplete Executions** enabled (or hits a `Break` directive), failed bundles park in the scenario's DLQ. Two paths to clear them.

### UI deep-link

Verified pattern (team-scoped + tab suffix):

```text
https://{zone}.make.com/{teamId}/scenarios/{scenarioId}/dlq
```

Sibling tab forms: `/scenarios/{id}` (Diagram), `/scenarios/{id}/edit`, `/scenarios/{id}/history`, `/scenarios/{id}/dlq`. The `{teamId}` segment is **mandatory** — un-scoped `/scenarios/{id}` 404s in the browser. Token / browser-session auth determines which teams the URL resolves under.

URL guesses cannot be verified from the CLI — Make's SPA returns 404 for every unauthenticated probe (defense, not actual missing route). Ask the operator to paste the URL from a logged-in browser, or use the API.

### API — token auth (per public docs)

Per the [Make developer docs — incomplete executions](https://developers.make.com/api-documentation/api-reference/incomplete-executions):

```bash
# Delete specific bundles
curl -X DELETE "$BASE/dlqs?scenarioId=SCENARIO_ID&confirmed=true" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"ids":["dlqId1","dlqId2"]}'

# Delete every DLQ entry for the scenario
curl -X DELETE "$BASE/dlqs?scenarioId=SCENARIO_ID&confirmed=true" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"all":true,"ids":[],"exceptIds":[]}'

# Keep some, delete the rest
curl -X DELETE "$BASE/dlqs?scenarioId=SCENARIO_ID&confirmed=true" \
  -H "Authorization: Token $MAKE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"all":true,"ids":[],"exceptIds":["keepThisDlqId"]}'
```

The deprecated single-bundle form `DELETE /dlqs/{dlqId}` still works but prefer the batch form above.

### API — browser session cookie auth (internal API)

The same endpoint also accepts the user's browser session — useful when the public-API token is unavailable or scope-limited. The Make web app calls `DELETE /api/v2/dlqs?scenarioId={id}&confirmed=true` directly from the operator's session. Required headers (extracted from a logged-in browser):

```bash
curl -X DELETE 'https://{zone}.make.com/api/v2/dlqs?scenarioId=SCENARIO_ID&confirmed=true' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json' \
  -H 'imt-web-zone: production' \
  -H 'origin: https://{zone}.make.com' \
  -H 'referer: https://{zone}.make.com/{teamId}/scenarios/{scenarioId}/dlq' \
  -b 'sid=<session cookie>; XSRF-TOKEN=<csrf token>; userId=<userId cookie>; ...' \
  --data-raw '{"all":true,"ids":[],"exceptIds":[]}'
```

Cookie extraction: use the [`chrome-cookies`](https://github.com/D1DX/chrome-cookies-skill) skill (or Chrome DevTools → Network → copy as cURL). **Never paste live session cookies into chat, commit messages, docs, or task records** — they grant full account access for the cookie lifetime. Treat extracted cookies as Tier-0 secrets.

Auth method choice:

- **Token auth** — preferred for scripts, cron, n8n flows, and team-shared automation. Stable. Mints via Make UI → Profile → API.
- **Cookie auth** — when the token doesn't carry the needed scope, or for one-off operator-driven cleanup. Cookie expires when the browser session ends.

---

## 9. Folders

```bash
# List folders
curl -s "$BASE/scenarios-foldertree?teamId=YOUR_TEAM_ID" \
  -H "Authorization: Token $MAKE_API_KEY"
```

---

## 10. Make-to-n8n Migration Mapping

| Make Module | n8n Equivalent | Notes |
|-------------|---------------|-------|
| `gateway:CustomWebHook` | Webhook node | Path naming differs |
| `builtin:BasicRouter` | Switch / If node | Switch for >2 routes |
| `builtin:BasicFeeder` | Split In Batches / Loop | Different iteration model |
| `builtin:BasicAggregator` | Merge node (Append) | Or Code node for complex |
| `http:ActionSendData` | HTTP Request node | Direct mapping |
| `json:ParseJSON` | Not needed (auto) | n8n auto-parses JSON |
| `airtable2:*` | Airtable node | Credential re-link required |
| `openai-gpt-3:*` | OpenAI node | Model param mapping |
| `google:ActionSendEmail` | Gmail node | Credential re-link required |
| `tools:SetVariable` | Set node | Direct mapping |
| `util:FunctionSleep` | Wait node | Direct mapping |

**Expression migration:**
| Make | n8n |
|------|-----|
| `{{1.body}}` | `{{ $('Node Name').item.json.body }}` |
| `{{ifempty(1.x; "y")}}` | `{{ $json.x \|\| "y" }}` |
| `{{lower(1.x)}}` | `{{ $json.x.toLowerCase() }}` |
| `{{formatDate(1.d; "YYYY-MM-DD")}}` | `{{ DateTime.fromISO($json.d).toFormat('yyyy-MM-dd') }}` |
| `{{length(1.arr)}}` | `{{ $json.arr.length }}` |

---

## 11. Critical Gotchas

1. **Blueprint is a string** — when pushing via API, blueprint must be JSON-encoded as a string value, not a raw object. Use the `jq -n --arg bp` pattern.
2. **Zone prefix required** — calls to `make.com` without the correct zone prefix (e.g. `eu1`) return 404. Always use the full zoned base URL.
3. **Connection IDs are account-specific** — importing a blueprint from one account to another requires relinking all connection IDs.
4. **Pull before edit** — always fetch the current blueprint before modifying locally. The live scenario may have been edited in the UI.
5. **Push doesn't activate** — pushing a blueprint doesn't activate the scenario. Activate separately with `/start`.
6. **Router `:else:` toggle** — fallback route requires `:else:` ON in the Make UI. If it turns off, all requests fall through to the last route silently.
7. **Rate limits** — API has rate limits per team. Bulk operations should add delays.
9. **Scenario scheduling** — `indefinitely` means "run continuously", `once` runs once. Webhook-triggered scenarios don't need a scheduling interval.
10. **Blueprint module IDs** — IDs are local to the blueprint (1, 2, 3...). References like `{{1.body}}` use these IDs.
11. **Data store size limit** — free plan: 10MB. Check quota before bulk writes.
