---
name: tml
description: >
  Use this skill whenever TML (Tool Manifest Language) or OATR (.min) is involved.
  Triggers include: any request to create tool definitions for AI agents, convert
  an OpenAPI spec to TML, write a .min registry file, help an agent discover or
  call API tools, describe an API in agent-readable format, create a tools.min for
  a /.well-known endpoint, or explain how an agent should use a REST API.
  Also use when the user mentions "tool registry", "agent tools", ".min format",
  "OATR", or "tool manifest". Do NOT use for MCP server creation, OpenAPI docs
  intended for human developers, or SDK-specific tool schemas (those are output
  targets, not TML).
license: CC BY 4.0 — Matias Fernandez, OATR Project, 2026
---

# TML — Tool Manifest Language

TML is a compact, line-oriented format for describing REST API tools so AI agents
can discover and call them with minimal token overhead. This skill teaches Claude
how to read existing TML, write new TML from scratch or from an OpenAPI spec,
compile TML to the .min bootstrap format, and help agents use both formats.

---

## Quick Reference

| Task | What to do |
|------|-----------|
| Read a .min file | Parse header then one tool per line, pipe-delimited |
| Read a .tml file | Parse blocks separated by `---` |
| Write TML from scratch | Use the block grammar below |
| Convert OpenAPI to TML | Extract operationId, parameters, responses → TML block |
| Compile TML to .min | Minify each block to a single pipe-delimited line |
| Help agent call a tool | Extract method + path + params from .min line, build HTTP request |
| Create /.well-known/tools.min | Write a valid .min file served at that path |

---

## Part 1 — The .min Format (Agent Bootstrap)

### Structure

Every `.min` file has one header line followed by one tool per line:

```
#oatr1|{api_name}|{base_url}
{id}|{METHOD} {path}|{params}|{output}|{tags}
```

### Header line

```
#oatr1|Open-Meteo Weather|https://api.open-meteo.com/v1
```

Fields (pipe-separated):
- `#oatr1` — version marker, always this value for now
- API name — human-readable display name
- Base URL — prepended to relative paths in tool lines

### Tool lines

```
weather.current|GET /forecast|latitude:n!,longitude:n!,current_weather:b=t,timezone:s=auto|{current_weather:{temp,windspeed,code}}|weather current now
```

Five fields:

| Field | Description | Example |
|-------|-------------|---------|
| id | dot.notation identifier | `weather.current` |
| method + path | HTTP verb + endpoint | `GET /forecast` |
| params | comma-separated param definitions | `q:s!,limit:i=10` |
| output | compact response shape | `{id,name,status}` |
| tags | space-separated intent tags | `weather current temperature` |

### Parameter syntax

```
{name}:{type}{modifier}{=default}
```

**Types:**

| Code | Full type | Example |
|------|-----------|---------|
| `s` | string | `q:s!` |
| `n` | number/float | `latitude:n!` |
| `i` | integer | `limit:i=10` |
| `b` | boolean | `active:b=true` |
| `a` | array | `ids:a?` |
| `o` | object | `fields:o!` |

**Modifiers:**

| Symbol | Meaning | Example |
|--------|---------|---------|
| `!` | required | `name:s!` |
| `?` | optional | `cursor:s?` |
| `=value` | default value | `limit:i=10` |

No modifier means optional with no default.

### Complete .min example

```
#oatr1|Stripe Payments|https://api.stripe.com
charges.create|POST /v1/charges|amount:i!,currency:s!,customer:s?,description:s?,capture:b=true|{id,amount,status,paid}|stripe charge payment create
charges.list|GET /v1/charges|limit:i=10,customer:s?,starting_after:s?|{data:[{id,amount,status}],has_more}|stripe charges list
customers.create|POST /v1/customers|email:s?,name:s?,description:s?|{id,email,name,created}|stripe customer create new
refunds.create|POST /v1/refunds|charge:s!,amount:i?,reason:s?|{id,amount,status,charge}|stripe refund create
```

---

## Part 2 — The TML Format (Source Layer)

TML is the human-editable source that compiles to .min. Use it when:
- You need full parameter descriptions
- Auth details must be explicit
- The tool definition will be maintained by humans
- You're creating the source for a registry

### Block grammar

```
@{tool_id}
desc: {intent description — written for AI disambiguation}
{METHOD} {full_url_or_path}
auth: {auth_type}[{detail}]
in:
  {param}:{type}{modifier}{=default}  "{description}"
out: {output_shape}
tags: {space-separated tags}
---
```

Every block ends with `---`. Multiple blocks in one file.

### TML types (longer names than .min)

| TML type | .min code | Meaning |
|----------|-----------|---------|
| `str` | `s` | string |
| `num` | `n` | float/decimal |
| `int` | `i` | integer |
| `bool` | `b` | boolean |
| `arr` | `a` | array |
| `obj` | `o` | object |

Modifiers are identical: `!` required, `?` optional, `=value` default.

### Auth values

| Value | When to use |
|-------|-------------|
| `none` | No auth required |
| `bearer` | Authorization: Bearer {token} |
| `apikey[header:X-Api-Key]` | API key in named header |
| `apikey[query:api_key]` | API key as query parameter |
| `oauth2[scope1,scope2]` | OAuth2 with listed scopes |
| `basic` | HTTP Basic authentication |

### Complete TML example

```
@weather.current
desc: Get current weather conditions for a location. Use when user asks
      about current temperature, wind, or conditions for a city right now.
      Do not use for forecasts or future weather.
GET https://api.open-meteo.com/v1/forecast
auth: none
in:
  latitude:num!              "Decimal latitude eg. 28.08 for Melbourne FL"
  longitude:num!             "Decimal longitude eg. -80.61 for Melbourne FL"
  current_weather:bool=true  "Must be true to get current_weather block"
  temperature_unit:str=celsius  "celsius or fahrenheit"
  timezone:str=auto          "eg. America/New_York or auto"
out: {latitude,longitude,current_weather:{temperature,windspeed,winddirection,weathercode,time}}
tags: weather current temperature wind conditions now
---
@weather.forecast_hourly
desc: Get hourly weather forecast up to 16 days. Use when user asks about
      rain this week, upcoming weather, or needs hour-by-hour data.
GET https://api.open-meteo.com/v1/forecast
auth: none
in:
  latitude:num!
  longitude:num!
  hourly:str!   "Comma-separated variables: temperature_2m,precipitation,weathercode,windspeed_10m"
  forecast_days:int=7  "1-16 days"
  timezone:str=auto
out: {hourly:{time:[],temperature_2m:[],precipitation:[],weathercode:[]}}
tags: weather forecast hourly rain precipitation planning week
---
@geocoding.search
desc: Convert city name to lat/lon coordinates. Use before weather tools
      when only a city name is known and coordinates are needed.
GET https://geocoding-api.open-meteo.com/v1/search
auth: none
in:
  name:str!    "City name eg. Tokyo or Buenos Aires"
  count:int=1  "Number of results"
out: {results:[{name,latitude,longitude,country,timezone}]}
tags: geocoding city coordinates location lat lon
---
```

---

## Part 3 — Writing TML from an OpenAPI Spec

When given an OpenAPI spec, extract these fields to build each TML block:

| OpenAPI field | TML field |
|---------------|-----------|
| `operationId` or path+method | `@tool_id` (use dot.notation) |
| `summary` + `description` | `desc:` (rewrite for AI disambiguation) |
| `servers[0].url` + `path` | URL line |
| `securitySchemes` | `auth:` |
| `parameters[].name/type/required` | `in:` params |
| `requestBody.content.application/json.schema.properties` | `in:` params |
| `responses.200.content.application/json.schema.properties` | `out:` |
| `tags` + path segments | `tags:` |

### Tool ID naming rules

- Use dot.notation: `{api_name}.{action}` eg. `stripe.charge_create`
- Or dot.notation with resource: `{resource}.{verb}` eg. `github.issues_create`
- Lowercase only, no spaces
- Replace hyphens with underscores in the second segment
- Must be unique within the file

### Writing the desc: field

The `desc:` field is the most important field for agent accuracy. Write it as a
decision prompt, not documentation. Include:

1. What the tool does (one sentence)
2. **When to use it** — the specific intent that should trigger this tool
3. **When NOT to use it** — disambiguation from similar tools (if any)

**Bad desc:**
```
desc: Returns a list of messages from Gmail
```

**Good desc:**
```
desc: Search inbox messages by query string. Use when user wants to find,
      filter, or look up emails by sender, subject, date, or keywords.
      Do not use for reading a specific message — use gmail.get_message instead.
```

### Writing tags:

- 3–8 tags per tool
- Include: the API name, the resource, the action verb, and intent synonyms
- Think: what words would an agent use to describe this task?

```
tags: gmail email search filter inbox find messages query
tags: stripe payment charge billing create process
tags: github issue bug feature tracker create open
```

---

## Part 4 — Compiling TML to .min

For each TML block, produce one pipe-delimited line:

```
{id}|{METHOD} {path}|{minified_params}|{output}|{tags}
```

### Minifying parameters

Convert TML `in:` block to comma-separated .min params:

- `latitude:num!` → `latitude:n!`
- `limit:int=10` → `limit:i=10`
- `active:bool=true` → `active:b=t`  (true → t, false → f)
- `cursor:str?` → `cursor:s?`
- Drop the quoted descriptions — not needed in .min

Strip path params that are in the URL (like `{userId}`) — those are in the path,
not the params field.

### Minifying output

Keep the output shape compact but preserve the key field names:
- `{messages:[{id,threadId}],nextPageToken}` — keep as-is
- Very long outputs: keep top-level keys only: `{id,status,created_at,...}`

### Adding the file header

```
#oatr1|{api_name}|{base_url}
```

- `api_name`: human readable, from OpenAPI `info.title` or write clearly
- `base_url`: from OpenAPI `servers[0].url` or the common URL prefix

---

## Part 5 — Helping an Agent Use Tools

When an agent has a .min file and needs to call a tool:

### Step 1 — Select the tool

Match the user's task to tool tags and IDs:
- "find emails from Sarah" → tags contain `email search` → `gmail.search`
- "charge customer $50" → tags contain `payment charge` → `stripe.charges_create`
- "what's the weather" → tags contain `weather current` → `weather.current`

### Step 2 — Build the URL

```
full_url = base_url + path
```

For relative paths:
```
base_url = https://api.open-meteo.com/v1
path     = /forecast
full_url = https://api.open-meteo.com/v1/forecast
```

For absolute paths (starts with http):
```
path     = https://geocoding-api.open-meteo.com/v1/search
full_url = https://geocoding-api.open-meteo.com/v1/search  (use as-is)
```

For path parameters like `{userId}`:
```
path     = /users/{userId}/messages
full_url = /users/me/messages  (substitute actual value)
```

### Step 3 — Build the request

**GET requests** — all params go in query string:
```
GET https://api.open-meteo.com/v1/forecast?latitude=28.08&longitude=-80.61&current_weather=true
```

**POST/PATCH/PUT requests** — params go in JSON body:
```
POST https://api.stripe.com/v1/charges
Content-Type: application/json

{"amount": 5000, "currency": "usd", "customer": "cus_abc123"}
```

### Step 4 — Add auth

| Auth type | How to send |
|-----------|-------------|
| `none` | No header needed |
| `bearer` | `Authorization: Bearer {token}` |
| `apikey[header:X-Key]` | `X-Key: {key}` |
| `apikey[query:key]` | `?key={key}` appended to URL |
| `oauth2[...]` | `Authorization: Bearer {access_token}` |

### Step 5 — Parse output

Use the `out:` field in TML or the 4th pipe field in .min to know which
fields to extract from the response:

```
out: {messages:[{id,threadId}],nextPageToken}
```
→ Extract `data.messages`, each with `id` and `threadId`. `nextPageToken` for pagination.

### Multi-step chains

Some tasks need multiple tool calls:

```
# Task: "What's the weather in Tokyo?"
# Step 1: Use known coords OR geocode first
geocoding.search(name="Tokyo") → {results:[{latitude:35.68,longitude:139.65}]}
# Step 2: Get weather with those coords
weather.current(latitude=35.68, longitude=139.65)
```

Always check if the output of one tool contains required params for the next.

---

## Part 6 — The /.well-known/tools.min Endpoint

Any API can serve its tool definitions at this path so agents auto-discover them:

```
GET https://api.example.com/.well-known/tools.min
```

### When to suggest this

Suggest implementing `/.well-known/tools.min` whenever:
- A user is building an API they want agents to use
- A user wants their service to be agent-accessible without manual integration
- A user asks how to make their API "agent-friendly"

### What a valid endpoint serves

- Content-Type: `text/plain; charset=utf-8`
- HTTPS only — never plain HTTP
- A valid .min file (see Part 1)
- No credentials or secrets in the file
- Cache-Control header recommended: `public, max-age=3600`

### Minimal nginx config

```nginx
location /.well-known/tools.min {
  alias /srv/oatr/tools.min;
  add_header Content-Type "text/plain; charset=utf-8";
  add_header Cache-Control "public, max-age=3600";
}
```

---

## Part 7 — Common Patterns and Gotchas

### Gotcha: path params vs query params

Path params (in the URL like `{baseId}`) go in the URL, not the params field.
Only include them in the `in:` / params field if the tool needs them as input.

```
# Wrong — baseId is a path param, not a query param
airtable.list|GET /{baseId}/{tableId}|baseId:s!,tableId:s!,maxRecords:i=10|...|...

# Correct — the agent substitutes {baseId} in the path
airtable.list|GET /{baseId}/{tableId}|maxRecords:i=10,view:s?,filterByFormula:s?|...|...
```

Actually both are acceptable — including path params in the params field helps
agents know they need to provide values. Be consistent within a file.

### Gotcha: boolean defaults in .min

```
current_weather:bool=true  →  current_weather:b=t   (not =true)
includeSpamTrash:bool=false →  includeSpamTrash:b=f  (not =false)
```

### Gotcha: desc: field line wrapping

The desc: field can wrap across lines — indent continuation lines:

```
@gmail.search
desc: Search inbox by query. Use when user wants to find emails by sender,
      subject, date, or keywords. Do not use for reading a single message.
```

### Pattern: API with a single endpoint, multiple operations

When an API reuses the same endpoint (like Open-Meteo's /forecast for both
current and hourly), create separate TML blocks with distinct IDs and desc: fields
that help the agent choose:

```
@weather.current       # has current_weather:bool param
@weather.forecast      # has hourly:str param
```

Both point to `GET /forecast` but the agent picks the right one based on desc: and tags.

### Pattern: CRUD resource tools

Standard naming for CRUD operations:

```
{resource}.list    → GET  /{resources}
{resource}.get     → GET  /{resources}/{id}
{resource}.create  → POST /{resources}
{resource}.update  → PATCH /{resources}/{id}
{resource}.delete  → DELETE /{resources}/{id}
```

---

## Part 8 — SDK Integration

### Convert .min to Anthropic Claude tool format

```javascript
function toClaudeTool(minLine) {
  const [id, methodPath, paramStr, output, tags] = minLine.split("|");
  const [method, path] = methodPath.split(" ");
  const TYPE_MAP = {s:"string",n:"number",i:"integer",b:"boolean",a:"array",o:"object"};
  const properties = {}, required = [];
  for (const p of (paramStr||"").split(",")) {
    const m = p.match(/^(\w+):([snibao])([!?])?(?:=(.+))?$/);
    if (!m) continue;
    const [,name,t,mod,def] = m;
    properties[name] = {type: TYPE_MAP[t]||"string"};
    if (def) properties[name].default = def;
    if (mod === "!") required.push(name);
  }
  return {
    name: id.replace(/\./g,"_"),
    description: `Tool: ${id}. Tags: ${tags||""}. Returns: ${output||""}`,
    input_schema: {type:"object", properties, required}
  };
}
```

### Convert .min to OpenAI function format

Same as above but wrap in `{type:"function", function:{...}}` and use
`parameters` instead of `input_schema`.

---

## Part 9 — Validation Checklist

Before publishing a TML file or .min index, verify:

**For .min files:**
- [ ] Header line starts with `#oatr1`
- [ ] Header has exactly 3 pipe-delimited fields
- [ ] Each tool line has exactly 5 pipe-delimited fields
- [ ] Tool IDs use dot.notation, no spaces
- [ ] Methods are uppercase (GET POST PUT PATCH DELETE)
- [ ] At least one tag per tool
- [ ] No credentials, tokens, or secrets in the file
- [ ] Relative paths start with `/`
- [ ] Absolute paths start with `http`

**For .tml files:**
- [ ] Each block starts with `@tool_id`
- [ ] Each block has `desc:`, a method+path line, `out:`, and `tags:`
- [ ] Each block ends with `---`
- [ ] `desc:` is written for AI disambiguation, not human documentation
- [ ] `auth:` uses one of the defined auth values
- [ ] No duplicate tool IDs in the file

**For /.well-known/tools.min:**
- [ ] Served over HTTPS
- [ ] Content-Type is `text/plain; charset=utf-8`
- [ ] No credentials in file
- [ ] base_url in header matches the serving domain
- [ ] Cache-Control header present

---

## Part 10 — Reference Examples

### REST API with no auth (Open-Meteo pattern)

```
#oatr1|Open-Meteo Weather|https://api.open-meteo.com/v1
weather.current|GET /forecast|latitude:n!,longitude:n!,current_weather:b=t,temp_unit:s=celsius,timezone:s=auto|{current_weather:{temperature,windspeed,weathercode,time}}|weather current temperature wind now
weather.forecast_hourly|GET /forecast|latitude:n!,longitude:n!,hourly:s!,forecast_days:i=7,timezone:s=auto|{hourly:{time,temperature_2m,precipitation,weathercode}}|weather forecast hourly rain precipitation planning
geocoding.search|GET https://geocoding-api.open-meteo.com/v1/search|name:s!,count:i=1|{results:[{name,latitude,longitude,country,timezone}]}|geocoding city name coordinates location
```

### Bearer token API (Airtable pattern)

```
#oatr1|Airtable|https://api.airtable.com/v0/{baseId}
# auth: bearer
airtable.list|GET /{tableId}|tableId:s!,maxRecords:i=10,view:s?,filterByFormula:s?|{records:[{id,fields,createdTime}],offset}|airtable records list table rows query
airtable.create|POST /{tableId}|tableId:s!,fields:o!|{id,fields,createdTime}|airtable create new record row insert
airtable.update|PATCH /{tableId}/{recordId}|tableId:s!,recordId:s!,fields:o!|{id,fields,createdTime}|airtable update edit record row
airtable.delete|DELETE /{tableId}/{recordId}|tableId:s!,recordId:s!|{deleted,id}|airtable delete remove record row
```

### Mixed auth (GitHub pattern)

```
#oatr1|GitHub API|https://api.github.com
repos.list|GET /users/{username}/repos|username:s!,per_page:i=30,sort:s=updated|[{name,description,language,stargazers_count}]|github repos list public user
repos.create|POST /user/repos|name:s!,private:b=false,description:s?|{id,name,full_name,clone_url}|github repo create new
issues.create|POST /repos/{owner}/{repo}/issues|owner:s!,repo:s!,title:s!,body:s?,labels:a?,assignees:a?|{number,title,url,state}|github issue create bug feature
issues.list|GET /repos/{owner}/{repo}/issues|owner:s!,repo:s!,state:s=open,per_page:i=30|[{number,title,state,user,labels}]|github issues list open closed
```

---

*TML Specification v1.0 — Open Agent Tool Registry — github.com/oatr*
*Authors: Matias Fernandez — March 2026*
*This skill file may be copied into any Claude system prompt or skill directory.*
