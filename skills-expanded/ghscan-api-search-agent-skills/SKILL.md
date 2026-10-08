---
name: integrate-provider
description: Onboard an API provider end-to-end — pull its signup, authentication, base URLs and OpenAPI from the apis.io catalog and produce concrete, runnable first-integration steps. Use when a provider is chosen and the user wants to actually wire it up.
license: CC-BY-NC-SA-4.0
---

# integrate-provider

Assemble auth, base URL, and a real first operation into steps a developer can run.

## When to use this skill

Use once a provider is chosen: "how do I get started with Twilio", "wire up Stripe",
"what's the first call". To choose the provider first, use `find-api`.

## The v1 API

Base `https://apis.io/api/v1`. All **free**.

| Step | Call | Why |
|---|---|---|
| 0. Resolve | `GET /resolve?identifier=<domain>` | Users give you a domain, not a slug. Also returns the real website + band. |
| 1. Onboarding | `GET /providers/{slug}/onboarding` | Signup, portal, docs, auth, pricing, first steps. |
| 2. Artifacts | `GET /providers/{slug}/artifacts` | Absolute URLs for every artifact, including Authentication. |
| 3. Spec | `GET /openapis/{aid}?include=content` | The OpenAPI inlined — read the real operations and servers. |

## Reading the onboarding response

```json
{ "slug": "twilio", "name": "Twilio",
  "website": "https://raw.githubusercontent.com/...",   // often NOT the company site — ignore
  "portal": "https://console.twilio.com",
  "signup": "https://www.twilio.com/try-twilio",
  "documentation": "https://www.twilio.com/docs",
  "authentication": "authentication/twilio-authentication.yml",  // relative — resolve via /artifacts
  "pricing": "https://www.twilio.com/pricing",
  "baseURLs": [],                                        // frequently empty — get servers from the spec
  "artifact_types": [ ... ],
  "first_steps": [ "Sign up: ...", "Set up authentication: ...", ... ],
  "note": "Assembled from registered links and API base URLs; not a full onboarding description." }
```

Three field-level cautions, all common enough to handle every time:

- **`website`** frequently holds a `raw.githubusercontent.com` source URL rather than the
  company's site. Use `portal`, `documentation`, or the `website` from `/resolve` instead.
- **`authentication`** may be a **repo-relative path**. Get the absolute URL from
  `/providers/{slug}/artifacts` — find the entry with `type == "Authentication"`.
- **`baseURLs`** is empty for many providers. Fall back to `servers[]` in the OpenAPI.

## Recipe

```bash
SLUG=$(curl -s "https://apis.io/api/v1/resolve?identifier=twilio.com" | jq -r '.slug')

# 1. Getting-started facts
curl -s "https://apis.io/api/v1/providers/$SLUG/onboarding" \
  | jq '{name, portal, signup, documentation, pricing, first_steps, baseURLs}'

# 2. The real authentication artifact (absolute URL)
curl -s "https://apis.io/api/v1/providers/$SLUG/artifacts" \
  | jq -r '.artifacts[] | select(.type=="Authentication") | .url' \
  | head -1 | xargs -r curl -s | head -40

# 3. Pick the API to integrate, then read its operations and servers
AID=$(curl -s "https://apis.io/api/v1/openapis?providers=$SLUG&limit=1" | jq -r '.data[0].aid')
curl -s "https://apis.io/api/v1/openapis/$AID?include=content" | jq -r '.content' > spec.yml
python3 -c "
import yaml
s=yaml.safe_load(open('spec.yml'))
print('servers:', [x.get('url') for x in s.get('servers',[])])
print('auth:', list((s.get('components') or {}).get('securitySchemes',{}).keys()))
for p,ops in list(s.get('paths',{}).items())[:10]:
    for m,op in ops.items():
        if m in ('get','post','put','patch','delete'):
            print(f'{m.upper():6} {p}  {op.get(\"summary\",\"\")}')"
```

MCP equivalents (`https://apis.io/mcp`): `resolve`, `get_provider_onboarding`,
`get_provider_artifacts`, `find_openapis`, `get_openapi`. Or run the `integrate_provider`
prompt with a `slug`.

## Output format

A short integration guide:

1. **Sign up** — the `signup` link, and `portal` for where credentials live.
2. **Authenticate** — the scheme from `components.securitySchemes` in the spec, cross-checked
   against the Authentication artifact. Name the header or flow explicitly.
3. **First call** — a runnable `curl`: method + path from the spec, base URL from
   `servers[0].url`, required parameters filled in.
4. **Next** — the SDK, Postman collection, Arazzo workflow, or MCP server to adopt, taken
   from `artifact_types`.

Cite real operations from the fetched spec. If a provider publishes no OpenAPI, say so and
point at its `Documentation` artifact — never invent endpoints or base URLs.

## Errors

All free. A 404 on the provider means a wrong slug — re-run `/resolve`. HTTP 402 means a
Pro endpoint; the body carries `error`, `detail`, `tier`, `plans`.

## Related skills

- `find-api` — pick the provider first.
- `resolve-provider` — domain, URL, or company name to slug.
- `fetch-api-spec` — deeper spec parsing.
- `discover-mcp-servers` — if the provider ships MCP, wire that in instead of raw REST.
- `agent-readiness-scan` — check whether it's ready for agent consumption at all.
