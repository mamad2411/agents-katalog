---
name: security-files-integrations-review
description: "Review changes to untrusted files, storage access, webhooks, outbound requests, or credentials."
---

# Security Files Integrations Review

Check file trust, storage access, scanning, webhook authenticity, outbound request limits, live event authorization, and integration failure modes.

## Trigger boundary

Use this skill when a change handles uploads/downloads, untrusted files or content, webhooks/live events, outbound requests or SSRF, integration credentials, scanning, or storage access.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no file, webhook, outbound-request, credential, storage, or integration behavior impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-files-and-integrations.md](./references/01-files-and-integrations.md) - Files And Integrations
- [02-ssrf-outbound-requests.md](./references/02-ssrf-outbound-requests.md) - SSRF And Outbound Requests
