---
name: scraperapi-n8n
description: >
  Generate n8n workflows that use the official ScraperAPI community node
  (n8n-nodes-scraperapi-official). Use this skill whenever the user wants to
  build, design, automate, or scaffold an n8n workflow that scrapes the web
  through ScraperAPI — even when they don't say "skill" or "ScraperAPI node"
  by name. Triggers include: "build an n8n workflow that monitors Amazon
  prices", "create an n8n flow to scrape Google search daily", "generate an
  n8n JSON for a crawler that hits this site", "wire ScraperAPI into n8n to
  email me product reviews", "n8n automation for Walmart price tracking",
  "use ScraperAPI in n8n to enrich leads", "give my n8n AI Agent web access
  via ScraperAPI", "add ScraperAPI as a tool to my n8n agent". Produces
  either importable workflow JSON or a step-by-step build guide in the n8n
  editor, picking the format based on how the user phrased the request.
metadata:
  openclaw:
    emoji: "🟧"
    homepage: https://n8n.io/integrations/scraperapi/
---

# ScraperAPI in n8n — Workflow Generator

This skill helps you assemble n8n workflows around the **official ScraperAPI
community node** (`n8n-nodes-scraperapi-official`). It supports two output
shapes, picked from the user's phrasing:

| User says … | Produce |
|-------------|---------|
| "give me the workflow JSON", "export", "I want to import this", "scaffold a .json" | A complete, importable workflow JSON file |
| "walk me through it", "show me how to build", "in the n8n editor", "step by step" | A numbered build guide referencing exact resource / operation / parameter names |
| Ambiguous | Default to JSON. It's reversible — they can either import it or follow it as a recipe. |

When you produce JSON, write it to a file in the working directory (e.g.,
`scraperapi-workflow.json`) and tell the user to import it via **Workflows
→ Import from File** in the n8n UI. When you produce a build guide, format
the steps for the n8n editor (resource picker → operation picker → fields).

## Prerequisites the user must have

1. An n8n instance (Cloud, self-hosted, or desktop) where they can install
   community nodes. On self-hosted instances, an instance owner must enable
   community nodes first.
2. The community node installed: **Settings → Community Nodes → Install →
   `n8n-nodes-scraperapi-official`**. After install, "ScraperAPI" appears
   in the node picker.
3. A ScraperAPI API key from `https://dashboard.scraperapi.com/`. They
   create the credential once via **Credentials → New → ScraperAPI API**
   and paste the key. The credential is named `ScraperAPI API` in the UI
   and `scraperApi-Api` in the workflow JSON.

If the user is on n8n Cloud and the workflow JSON references this node,
importing will succeed only after the community node is installed in their
instance. Mention this when handing over JSON.

## Three resources — pick the right one

The ScraperAPI node has one operation surface (`resource`) with three
branches. Choose based on the job:

| Job | Resource | Why |
|-----|----------|-----|
| Scrape an arbitrary URL and get HTML/Markdown/Text/JSON | `api` | General-purpose proxy. Hand it any URL. |
| Get clean JSON from a supported site (Amazon, Google, eBay, Walmart, Redfin) | `sde` | Pre-parsed structured data. Saves a Set/Code node for HTML parsing and is more reliable across site changes. |
| Crawl multiple pages from one starting URL, streaming results to a webhook | `crawler` | Multi-page jobs that follow links. Returns a `jobId`; results arrive at your webhook, not as the node's output. |

A common pattern: use a structured endpoint when one exists for the site,
fall back to `api` (with `apiRender: true` or `apiPremium: true`) for
anything else, and reach for `crawler` only when one-URL-at-a-time would
need many sequential node executions.

## Required JSON shape — minimal example

This is the smallest possible workflow that uses ScraperAPI. Everything
else in this skill is variations on this shape.

```json
{
  "name": "ScraperAPI minimal example",
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "id": "trigger-1",
      "name": "When clicking 'Test workflow'"
    },
    {
      "parameters": {
        "resource": "api",
        "operation": "apiRequest",
        "apiUrl": "https://example.com",
        "apiOptionalParameters": {
          "apiRender": true,
          "apiCountryCode": "us"
        }
      },
      "type": "n8n-nodes-scraperapi-official.scraperApi",
      "typeVersion": 1,
      "position": [480, 300],
      "id": "scraperapi-1",
      "name": "ScraperAPI",
      "credentials": {
        "scraperApi-Api": {
          "id": "REPLACE_WITH_CREDENTIAL_ID",
          "name": "ScraperAPI API"
        }
      }
    }
  ],
  "connections": {
    "When clicking 'Test workflow'": {
      "main": [
        [{ "node": "ScraperAPI", "type": "main", "index": 0 }]
      ]
    }
  },
  "settings": { "executionOrder": "v1" }
}
```

### Things to get right in every workflow JSON

1. **Node type:** `n8n-nodes-scraperapi-official.scraperApi` — exact spelling,
   case-sensitive. Wrong type = "Unrecognized node type" on import.
2. **Credential block:** key is `scraperApi-Api` (not `scraperApiApi`).
   Leave `id` as a placeholder and tell the user to re-select the credential
   in the imported node. n8n cannot look up credential IDs across instances.
3. **`typeVersion: 1`** for the ScraperAPI node.
4. **Connections use node `name`**, not `id`. If you rename a node, update
   the connections map too.
5. **Position** is `[x, y]` pixels in the editor. Anything is fine on
   import; n8n re-layouts on demand. Use ~240px spacing horizontally.
6. **`executionOrder: "v1"`** under `settings` — this is current default.
   Older `"none"`/`"v0"` are deprecated and behave differently with merges.

## Expressions in node fields — the `=` prefix

n8n distinguishes a literal string from an expression by a leading `=`
character on the field's value. This applies to every field of every
node, including ScraperAPI's `apiUrl`, `sdeAsin`, `sdeQuery`, etc.

```json
"apiUrl": "https://example.com"          // literal — always this URL
"apiUrl": "={{ $json.url }}"             // expression — URL from upstream item
"apiUrl": "{{ $json.url }}"              // ⚠ literal "{{ $json.url }}" string
```

A few practical patterns that come up constantly:

```json
"sdeAsin":  "={{ $json.asin }}"
"sdeQuery": "={{ $json.body.search_term }}"           // webhook payload
"sdeUrl":   "=https://www.redfin.com/city/{{ $json.city_id }}"
```

When the value needs to be partly literal and partly dynamic, keep the
`=` only at the start of the string. Everything inside `{{ }}` is a JS
expression — `$json`, `$node['Other'].json.x`, `JSON.stringify(...)`,
inline arithmetic, etc.

For webhook-triggered workflows, remember user data lives under `body`
(see "Common mistakes" below). The expression is `={{ $json.body.x }}`,
not `={{ $json.x }}` — a single missing `body.` is the most frequent
silent failure in n8n.

## Parameter naming — the n8n trap

The node's JSON parameter names are **not** the same as ScraperAPI's HTTP
query parameter names. n8n uses camelCase with a resource prefix; the API
uses snake_case. When generating JSON, use the n8n names.

| ScraperAPI HTTP param | n8n field (api resource) | n8n field (crawler resource) |
|-----------------------|--------------------------|------------------------------|
| `url` | `apiUrl` | `crawlerStartUrl` |
| `render` | `apiOptionalParameters.apiRender` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiRender` |
| `country_code` | `apiOptionalParameters.apiCountryCode` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiCountryCode` |
| `premium` | `apiOptionalParameters.apiPremium` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiPremium` |
| `ultra_premium` | `apiOptionalParameters.apiUltraPremium` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiUltraPremium` |
| `autoparse` | `apiOptionalParameters.apiAutoparse` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiAutoparse` |
| `output_format` | `apiOptionalParameters.apiOutputFormat` | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiOutputFormat` |
| device (desktop) | `apiOptionalParameters.apiDesktopDevice` (bool) | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiDesktopDevice` |
| device (mobile) | `apiOptionalParameters.apiMobileDevice` (bool) | `crawlerOptionalParameters.crawlerApiParameters.crawlerApiMobileDevice` |

For SDE platforms, see `references/node-reference.md` — each platform/
operation has its own required field name (e.g., `sdeAsin`, `sdeQuery`,
`sdeProductId`, `sdeUrl`, `sdeCategory`) and its own optional-parameters
collection (e.g., `sdeAmazonProductOptions`, `sdeGoogleSearchOptions`).

If you're not sure of an exact field name, read the reference file before
generating JSON. Mis-named fields are silently dropped on import.

## Output of the ScraperAPI node

Every operation returns one item per input item with this shape:

```json
{
  "resource": "api",
  "response": {
    "body": "...",
    "headers": { },
    "statusCode": 200,
    "statusMessage": "OK"
  }
}
```

For `api` and `crawler`, `body` is the raw text payload (HTML, Markdown,
JSON-as-string depending on `apiOutputFormat`). For `sde`, `body` is the
parsed JSON document from ScraperAPI as a string — downstream nodes need
to parse it. The simplest pattern is a **Code** node:

```js
return $input.all().map((item, i) => ({
  json: JSON.parse(item.json.response.body),
  pairedItem: { item: i },
}));
```

The `pairedItem` field tells n8n which input item each output belongs
to. Skipping it works for linear flows, but the moment the workflow
fans out (Loop Over Items, Merge, IF that re-converges), missing
`pairedItem` causes downstream nodes to mismatch items — most often
seen as "wrong row paired with wrong scrape result" in batch
workflows. Always set it.

After this node, every field from the structured payload is accessible
directly as `={{ $json.<field> }}` downstream.

## Wiring patterns by use case

The user usually has one of these shapes in mind. Don't invent a complex
multi-node flow when one of these covers it.

### Daily monitor — scheduled scrape → diff → notify

```
Schedule Trigger → [Sheets/DB read] → Loop Over Items
                                          ↓
                                       ScraperAPI (sde)
                                          ↓
                                       Code (parse body)
                                          ↓
                                       [Sheets/DB write history]
                                          ↓
                                       IF (changed?)
                                          ↓
                                       Email / Slack
```

When the user's request resembles a **price-monitoring** or
**daily-digest** workflow (any combination of: scheduled trigger, list
of products, ScraperAPI lookup, history table, email-on-change), don't
hand-write the JSON from this shape. Fetch the canonical ScraperAPI
template and adapt it:

```
GET https://api.n8n.io/api/templates/workflows/15609
```

The full importable workflow JSON is at `response.workflow.workflow`
(it has `nodes` and `connections` at the top level, ready to drop into
n8n's import dialog). The template has 29 nodes — Schedule Trigger, 3
ScraperAPI nodes (Amazon / Walmart / Google Shopping), Data Table for
history, Code nodes for diffing, an HTML digest, plus both Gmail and
SMTP send paths so the user can pick one.

Adapt rather than reproduce: change the product list, drop retailers
the user doesn't need, swap the email path, simplify the digest. Cite
the human-readable page so the user can preview before importing:

```
https://n8n.io/workflows/15609-send-daily-price-drop-digest-emails-for-amazon-walmart-and-google-via-scraperapi/
```

If the fetch fails (offline, rate-limited, API change), fall back to
the shape diagrammed above and the simpler single-ASIN example in
`references/example-workflows.md`.

### Webhook enrichment — on-demand lookup

```
Webhook → ScraperAPI (sde or api) → Code (parse) → Respond to Webhook
```

Useful for lead enrichment, on-demand product lookups, or as an MCP-style
tool exposed to an LLM. Set the Webhook's response to "Using 'Respond to
Webhook' node" so you can return the parsed data.

### Crawler + webhook callback — multi-page jobs

```
[Trigger] → ScraperAPI (crawler / Initiate) → ... waits ...
                                                ↓
                              (results arrive at separate webhook workflow)

Webhook (the callbackUrl) → process each page → store / index
```

The Initiate operation returns a `jobId` immediately. Pages are POSTed to
`crawlerCallbackUrl` as they're scraped — this **must** be a different
workflow with a Webhook trigger, not the same workflow that initiated the
job. Always tell the user to copy the callback workflow's webhook URL into
`crawlerCallbackUrl` before activating.

### Batch from a list — CSV/Sheet fan-out

```
[Read CSV / Sheet] → Loop Over Items (batch size 5–10) → ScraperAPI → Code → Merge → Output
```

Use **Loop Over Items** (a.k.a. Split In Batches) with a small batch size
to stay under ScraperAPI's concurrency limit. The Free plan allows 5
concurrent requests; paid plans go higher. If the user knows their plan,
size the batch accordingly; otherwise default to 5.

### AI Agent tool — give an LLM live web access

The ScraperAPI node declares `usableAsTool: true`, so it can be plugged
into an n8n **AI Agent** node as a callable tool. The agent decides when
to invoke it, with what URL/query, based on the user's prompt.

```
Chat Trigger → AI Agent ─┬─ Chat Model (OpenAI / Anthropic / etc.)
                          ├─ Memory (optional)
                          └─ Tool: ScraperAPI
```

Wiring details:

1. Add the ScraperAPI node to the canvas. Its operation/parameters act
   as the *tool's signature* — the agent fills in dynamic parameters
   from context. Pick the operation that matches the job you want the
   agent to be able to do (e.g., `sde` / `googleSearch` for "let the
   agent search the web", or `api` / `apiRequest` for "let the agent
   fetch any URL").
2. For dynamic fields, use `={{ $fromAI('parameter_name', 'description', 'string') }}`.
   `$fromAI` is the n8n helper that exposes a parameter to the agent's
   tool schema; the agent picks the value at runtime.
3. Connect the ScraperAPI node into the AI Agent node via the **Tool**
   input (not the main input).
4. Give the node a clear, action-oriented **name** ("Search the web",
   "Scrape any URL") — the agent uses the node name as part of the
   tool description it sees.

```json
{
  "resource": "sde",
  "sdePlatform": "google",
  "operation": "googleSearch",
  "sdeQuery": "={{ $fromAI('query', 'The user search query', 'string') }}",
  "sdeGoogleSearchOptions": {
    "tld": "com",
    "outputFormat": "json"
  }
}
```

The agent receives the parsed JSON body as the tool result and reasons
over it. For best results add a Code node *between* the ScraperAPI tool
and the agent to slim the payload — raw SDE responses can be large
enough to blow the agent's context budget.

## Credit budgeting — warn the user

ScraperAPI charges credits per successful request. Generated workflows
that loop or schedule can burn credits silently. When the workflow
scrapes more than ~50 URLs per run or runs more than hourly, add a
note in your reply estimating the per-run and per-month cost.

| Setting | Credits per request |
|---------|---------------------|
| `api` standard | 1 |
| `api` + `apiRender: true` | 10 |
| `api` + `apiPremium: true` | 10 |
| `api` + `apiPremium: true` + `apiRender: true` | 25 |
| `api` + `apiUltraPremium: true` | 30 |
| `sde` structured endpoint | 1–10 (per vertical; see public docs) |

Failed requests (non-200) are generally not charged, but retries on
transient errors still consume credits if they eventually succeed.

For full and current pricing, link to
`https://docs.scraperapi.com/` from the response.

## Common mistakes — ❌ wrong / ✅ correct

### Missing `=` prefix turns the expression into literal text

```json
❌ "apiUrl": "{{ $json.url }}"            // n8n scrapes the literal string "{{ $json.url }}"
✅ "apiUrl": "={{ $json.url }}"           // resolved to the current item's url field
```

### Webhook data lives under `body`, not the root

```json
❌ "sdeQuery": "={{ $json.search_term }}"           // undefined
✅ "sdeQuery": "={{ $json.body.search_term }}"      // works
```

The Webhook node wraps incoming data as `{ headers, params, query, body }`.
The user's payload is `$json.body`. Same applies to a Chat Trigger that
receives a JSON body.

### Code node returning a parsed object instead of n8n item shape

```js
❌ return JSON.parse($json.response.body);
❌ return { data: parsed };
✅ return [{ json: JSON.parse($json.response.body), pairedItem: { item: 0 } }];
```

n8n expects an array of `{ json: {...}, pairedItem?: {...} }`. Returning
a raw object yields "Cannot read properties of undefined" downstream.

### `apiPremium` and `apiUltraPremium` set together

```json
❌ { "apiPremium": true, "apiUltraPremium": true }
✅ { "apiUltraPremium": true }                      // pick one; ultra implies premium
```

They are mutually exclusive in the node UI and have undefined behavior
together.

### Crawler callback routed back into the same workflow

```
❌ ScraperAPI (crawlerJobCreate) ───loops to itself───> processing nodes
✅ Workflow A:  Trigger → ScraperAPI (crawlerJobCreate, callbackUrl = "<webhook in Workflow B>")
   Workflow B:  Webhook trigger → process page → store
```

Crawler results arrive at the `callbackUrl` as HTTP POSTs from
ScraperAPI's infrastructure. Only a workflow with a Webhook trigger can
receive them — never the same workflow that initiated the job.

### Hardcoded credential ID in exported JSON

```json
❌ "credentials": { "scraperApi-Api": { "id": "abc123", "name": "ScraperAPI API" } }
✅ "credentials": { "scraperApi-Api": { "id": "REPLACE", "name": "ScraperAPI API" } }
```

Credential IDs are local to one n8n instance. An imported workflow with
a real ID from another instance will fail with a "credential not found"
error. Use a placeholder and ask the user to re-select the credential
once after import.

### Setting `sdePlatform` without a matching `operation`

```json
❌ { "sdePlatform": "amazon", "operation": "googleSearch" }   // mismatched
✅ { "sdePlatform": "amazon", "operation": "amazonProduct" }
```

The `operation` field is platform-scoped. For `sdePlatform: "amazon"`,
valid operations are `amazonProduct`, `amazonSearch`, `amazonOffers`.
For Amazon Reviews and Prices (available via the underlying API but not
yet surfaced as separate node operations), fall back to `api` +
`apiAutoparse: true` against the Amazon URL.

### Skipping the Code-node parse step after `sde`

The structured response is a JSON string inside `response.body`.
Downstream nodes referencing `={{ $json.pricing }}` see undefined until
a Code (or Set) node parses the body. See the parse snippet above.

### Hardcoded API key in node parameters

The API key belongs in the credential record, never in node parameters
or expressions. Putting it in JSON exposes it in workflow exports,
version history, and audit logs.

## When to read what

| If you need … | Read |
|---------------|------|
| The exact field name for an SDE operation | `references/node-reference.md` |
| A larger worked example (price monitor, lead enricher) | `references/example-workflows.md` |
| What a valid n8n workflow JSON looks like end-to-end | `references/workflow-json-anatomy.md` |

After producing a workflow JSON, sanity-check it:

1. `node.type` is exactly `n8n-nodes-scraperapi-official.scraperApi`
2. Every node referenced in `connections` exists in `nodes`
3. Field names match the prefix rule (`api*` / `sde*` / `crawler*`)
4. The `credentials` block uses key `scraperApi-Api`
5. No literal API key is anywhere in the JSON

## Related skills and ecosystem

- **`scraperapi-mcp`** (sibling skill in this plugin) — use when the
  user wants Claude itself to call ScraperAPI as a tool, instead of
  wiring it into an n8n workflow. Different output: live answers vs.
  reusable JSON.
- **`n8n-mcp` MCP server** (`https://github.com/czlonkowski/n8n-mcp`) —
  third-party MCP server that exposes n8n's full node catalog,
  validation, and workflow CRUD to Claude. If the user has it installed,
  recommend validating the generated JSON via `validate_workflow` and
  deploying with `n8n_create_workflow` instead of having them import
  manually. The two skills compose: this one teaches the ScraperAPI
  node's shape; `n8n-mcp` teaches the surrounding n8n surface.

## Documentation

- Node listing: `https://n8n.io/integrations/scraperapi/`
- Price-drop digest template (page): `https://n8n.io/workflows/15609-send-daily-price-drop-digest-emails-for-amazon-walmart-and-google-via-scraperapi/`
- Price-drop digest template (API, returns full workflow JSON): `https://api.n8n.io/api/templates/workflows/15609`
- npm package: `https://www.npmjs.com/package/n8n-nodes-scraperapi-official`
- ScraperAPI docs: `https://docs.scraperapi.com/`
- Dashboard: `https://dashboard.scraperapi.com/`
