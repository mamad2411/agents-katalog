---
name: "kong-plugin-guidelines"
description: "Choosing and configuring Kong plugins to replicate upstream policies: auth (key-auth/jwt/oauth2), rate-limiting, cors, transformers, observability. Use when mapping backend policies to Kong plugins."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# Kong Plugin Guidelines

| Need | Plugin |
|------|--------|
| API key auth | key-auth |
| JWT/OAuth | jwt / oauth2 / openid-connect |
| Throttle | rate-limiting / response-ratelimiting |
| CORS | cors |
| Tracing id | correlation-id |
| Header/body shape | request-transformer / response-transformer |
| Cache | proxy-cache |
| Metrics | prometheus |
| IP rules | ip-restriction |

- Apply auth before rate-limiting (plugin ordering).
- Scope plugins at the narrowest level (route > service > global) that satisfies the policy.
- Map each upstream policy (from `tsa.source_reference`) to exactly one plugin; document unmapped behavior in the ADR.
- Never embed secrets in plugin config; use Kong vault references / env.
