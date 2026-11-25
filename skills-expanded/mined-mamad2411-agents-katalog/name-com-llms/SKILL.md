---
name: name-com-llms
description: 'Reference for name.com Core API documentation, API discovery, OpenAPI specs, and domain management workflows. You MUST load this skill when interacting with the name.com Core API.'
license: MIT
---

# Skill: name-com-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Building a domain search and purchase flow (search → check availability → register).
- Managing domain settings (DNS records, nameservers, WHOIS privacy, autorenew, locks).
- Handling domain transfers (inbound from other registrars, outbound preparation).
- Implementing contact verification workflows and monitoring verification status.
- Setting up webhook subscriptions for domain and transfer status changes.
- Testing domain operations safely in sandbox before production launch.
- Integrating domain renewal, pricing, and account balance operations.

## WHEN NOT TO USE

- Interacting with domain registrars other than name.com.
- Operations entirely outside the scope of domain, DNS, and webhook management.

## Core Process

1. **Registration**: Search domains (`POST /core/v1/domains:search`), verify availability (`POST /core/v1/domains:checkAvailability`), and register (`POST /core/v1/domains`).
2. **Management**: Fetch domains (`GET /core/v1/domains/{domainName}`) and update configurations (`PATCH /core/v1/domains/{domainName}`).
3. **DNS**: Manage records using the `/core/v1/domains/{domainName}/records` endpoints.
4. **Webhooks**: Subscribe to notifications (`POST /core/v1/notifications`) and verify HMAC signatures using your API token.

## Core Principles

- **Idempotency**: Always send an `X-Idempotency-Key` header on `POST /domains` (register) and `POST /transfers` calls to prevent double-charging on retries.
- **Sandbox Testing**: Use `https://api.dev.name.com` with a `-test` username suffix and sandbox token for testing. Do not mix production credentials in the sandbox.
- **Endpoint Structure**: Do NOT URL-encode colons in endpoints (e.g., use `/core/v1/domains:search`, not `/core/v1/domains%3Asearch`).

## Common Pitfalls

- **2FA blocks API access**: Accounts with 2FA enabled cannot authenticate. Disable 2FA or enable "API Access" in Account Settings → Security.
- **Sandbox/production mismatch**: Domains created in sandbox don't exist in production. Test in sandbox first, then verify in production.
- **DNS doesn't resolve in sandbox**: Sandbox DNS calls succeed but don't publish publicly. Test request/response handling, not public resolution.
- **Verification lock after 15 days**: If contacts aren't verified within 15 days, the domain stops resolving.
- **60-day transfer lock**: New registrations and transfers in are locked for 60 days by default. Unlock with `PATCH /domains/{domainName}` setting `locked: false`.
- **Contact verification delays**: Unverified contacts appear in the API ~10 minutes after registration.

## Limitations

- Domains cannot be deleted in sandbox; use unique test domain names per test run and design tests to be idempotent.
- Rate limits are 20 requests/second and 3,000 requests/hour; implement backoff on 429 Too Many Requests.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Name.com API Catalog](https://www.name.com/llms.txt)
- [Name.com Core API Documentation](https://docs.name.com/llms.txt)
- [Name.com Agent Skill Documentation](https://docs.name.com/skill.md)
