---
name: fetch-api-spec
description: Fetch and parse the OpenAPI, AsyncAPI, GraphQL, or Postman description for an API in the apis.io catalog, given its aid or its apis.io URL. Use to inspect operations, summarize endpoints, or generate code from a real spec.
license: CC-BY-NC-SA-4.0
---

# fetch-api-spec

Turn an apis.io API reference into the actual machine-readable description, parsed and ready
to reason over.

## When to use this skill

Use after `search-apis` or `find-api` returns a hit, or whenever the user hands you an
`apis.io/apis/...` URL and wants the endpoints inspected, summarized, or turned into code.

## Inputs

Any one of:
- An **aid** — `provider:api-slug`, e.g. `twilio:twilio-a2p-api`.
- An apis.io **API URL** — `https://apis.io/apis/twilio/twilio-a2p-api/`.
  The aid is the last two path segments joined with a colon: `twilio:twilio-a2p-api`.
- A **provider slug**, when the user wants "the spec for Stripe" and you must pick the
  primary API first.

## Two calls

Base `https://apis.io/api/v1`. Both **free**.

| Call | Returns |
|---|---|
| `GET /apis/{aid}` | The API record with a `properties[]` array — every artifact and its URL. |
| `GET /openapis/{aid}?include=content` | The OpenAPI with its body inlined, no second fetch. |

`GET /apis/{aid}` looks like:

```json
{ "aid": "twilio:twilio-a2p-api",
  "name": "Twilio A2p API",
  "description": "The A2p API from Twilio — 5 operation(s) for a2p.",
  "tags": ["A2P"],
  "properties": [
    { "type": "OpenAPI",  "url": "https://raw.githubusercontent.com/.../twilio-a2p-api-openapi.yml" },
    { "type": "GraphQL",  "url": "..." },
    { "type": "AsyncAPI", "url": "..." },
    { "type": "APIsJSON", "url": "..." } ] }
```

Pick the artifact you need out of `properties[]` by `type` and fetch its `url` directly —
the URLs are public raw files, no key needed.

## Recipe

```bash
AID=twilio:twilio-a2p-api

# 1. What descriptions exist for this API?
curl -s "https://apis.io/api/v1/apis/$AID" | jq '[.properties[] | {type, url}]'

# 2a. OpenAPI, inlined in one call
curl -s "https://apis.io/api/v1/openapis/$AID?include=content" | jq -r '.content' > spec.yml

# 2b. Or any other artifact type, fetched from its URL
curl -s "https://apis.io/api/v1/apis/$AID" \
  | jq -r '.properties[] | select(.type=="AsyncAPI") | .url' \
  | xargs curl -s > asyncapi.yml

# 3. Summarize the operations
python3 -c "
import yaml,sys
s=yaml.safe_load(open('spec.yml'))
print(s.get('info',{}).get('title'), s.get('openapi') or s.get('swagger'))
print('servers:', [x.get('url') for x in s.get('servers',[])])
for path,ops in s.get('paths',{}).items():
    for m,op in ops.items():
        if m in ('get','post','put','patch','delete'):
            print(f'{m.upper():6} {path}  {op.get(\"summary\",\"\")}')"
```

OpenAPI files parse as YAML whether they are YAML or JSON — `yaml.safe_load` handles both.

MCP equivalents (`https://apis.io/mcp`): `get_api`, `get_api_artifacts`, `get_openapi`,
`find_openapis`, `find_asyncapis`, `find_graphql`, `find_postman`. Or run the
`explain_artifact` prompt with an `aid`.

## Starting from a provider instead

```bash
# List a provider's OpenAPIs, then take the primary one
curl -s "https://apis.io/api/v1/openapis?providers=stripe&limit=5" \
  | jq '.data[] | {aid, name, url}'
```

## What to do with the spec

- **Summarize** — list `paths` with methods and `summary`.
- **Find an operation** — match on `operationId` or path pattern.
- **Build a curl** — `servers[0].url` + path + required parameters + the auth scheme from
  `components.securitySchemes`.
- **Extract schemas** — pull the relevant entries from `components.schemas`.

Cite only operations that are actually in the file. If the spec is missing or empty, say so
and fall back to the `Documentation` artifact in `properties[]` — never invent endpoints.

## Caching

Cache per-aid within a session. Specs vary from a few KB to several MB; fetch
`?include=content` once and reuse it rather than re-requesting per question.

## Errors

Both calls are free. A 404 on `/apis/{aid}` usually means a malformed aid — confirm the
colon form, and use `/resolve?identifier=<domain>` if you only have a company or URL.

## Related skills

- `discover-apis-io` — the conventions this skill assumes.
- `search-apis` — find candidate APIs first.
- `integrate-provider` — go from spec to a working first call.
