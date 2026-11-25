---
name: api-security-testing
description: "Test APIs for real vulnerabilities: authentication and authorisation bypass, object-level access control, injection, rate limits and mass assignment."
type: procedural
category: security
domain: security
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - api security testing
  - broken object level authorization
  - bola idor api
  - mass assignment vulnerability
  - api rate limit bypass
aliases:
  - api-sec
  - bola
keywords:
  - api-security
  - bola
  - idor
  - authorization
  - injection
  - rate-limit
  - owasp-api
mcp_servers:
  - postman
  - semgrep
  - github
source: custom
enabled: true
---

# API Security Testing

## Purpose

Test APIs for real vulnerabilities: authentication and authorisation bypass, object-level access control, injection, rate limits and mass assignment.

## When to Use

- An API is about to be exposed to third parties or the public.
- Authorisation is enforced in the UI rather than the endpoint.
- A pentest or compliance review requires evidence of API testing.

## When NOT to Use

- The target is not yours or you lack written authorisation.
- The scope is code review only, with no running instance.
- The concern is availability load testing, not security.

## Capabilities

- Enumerate endpoints and their auth requirements from the spec.
- Test object-level access by swapping identifiers between tenants.
- Probe injection surfaces including headers, filters and sort parameters.
- Verify rate limits and their bypass paths.
- Check mass assignment and excessive data exposure in responses.

## Inputs

- The OpenAPI document or endpoint inventory, plus two accounts in different tenancies.
- A test environment with realistic data.
- Written scope and rules of engagement.

## Workflow

1. Map every endpoint to its required role and object scope.
2. For each object endpoint, replay the request with another tenant's id.
3. Fuzz query filters, sort keys and JSON bodies with injection payloads.
4. Check that responses exclude fields the caller should not see.
5. Verify rate limiting per identity and per IP, and whether it can be reset trivially.
6. Record every finding with a request/response pair and a severity.

## Tools

- postman
- burp
- semgrep
- k6

## Examples

- `BOLA is the top API risk: `GET /invoices/123` returning another tenant's invoice is authorisation, not a bug in the UI.`
- `A 429 that resets on a new header value is not a rate limit.`

## Safety

- Only test systems you are authorised to test, in the agreed window.
- Never exfiltrate real customer records as evidence; redact and count instead.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postman` | stdio | full | medium | `POSTMAN_API_KEY` |
| `semgrep` | stdio | full | low | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/security/api-security-testing`). First-party skill, maintained in this repository.

## Notes

- Automate the boring part; authorisation logic still needs human reasoning per endpoint.
- Test the error paths too — verbose errors leak structure.
- Pairs with: `agent-reliability`, `fastapi-expert`.
