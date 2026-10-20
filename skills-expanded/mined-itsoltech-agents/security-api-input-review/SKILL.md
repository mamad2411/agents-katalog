---
name: security-api-input-review
description: "Review API changes that parse, validate, authorize, limit, or return client-controlled input."
---

# Security API Input Review

Treat all client input as untrusted; check validation, authorization, injection, SSRF, output, and error disclosure.

## Trigger boundary

Use this skill when an API change accepts, parses, validates, maps, limits, authorizes, logs, or returns client-controlled input, including injection or SSRF-sensitive outbound behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no input, trust-boundary, authorization, output, or error behavior impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-api-input-and-injection.md](./references/01-api-input-and-injection.md) - API Input And Injection
- [02-ssrf-outbound-requests.md](./references/02-ssrf-outbound-requests.md) - SSRF And Outbound Requests
