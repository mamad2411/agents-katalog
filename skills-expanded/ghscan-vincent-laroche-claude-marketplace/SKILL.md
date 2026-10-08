---
name: figma-integration-engineering
description: Design, implement, or diagnose Figma integrations and developer tooling. Use for REST or SCIM API work, webhooks, automation, plugins, widgets, asset exports, token sync, Code Connect, cross-file audits, OAuth, and CI jobs.
---

# Figma Integration Engineering

Choose the runtime first. Load `$figma-agent-core`; use a direct API only when MCP cannot perform the required operation or the job must run unattended.

## Choose the execution model

- Use the Plugin API for user-triggered, rich read/write work in one open file.
- Use REST for unattended or cross-file work only where the endpoint explicitly supports the required write. Do not claim it can arbitrarily edit visual nodes.
- Use a Widget for persistent multiplayer canvas behavior; use MCP for an available agent-mediated operation.
- For a hybrid, define the authority, data flow, authentication owner, retry behavior, and failure boundary before implementation.

## Build securely

1. Inspect the repository, manifest, typings, auth model, deployment owner, and current errors before editing.
2. Use least-privilege token/scopes and the narrowest plugin permissions, editor types, and network domains. Never embed secrets or print credentials.
3. Implement pagination, response-size limits, `Retry-After` handling, idempotency where supported, typed errors, and token-safe logs.
4. For plugins, use async document APIs, load fonts before text mutations, narrow node types, and validate the manifest, type check, build, and every declared editor mode.
5. For webhooks, verify current official documentation, authenticate and validate events, make handlers idempotent, and use a read-only or dry-run smoke test before registration or broad writes.

## Integrate with code deliberately

- Export assets through supported Figma operations and record source node, format, scale, expiry, and destination. Do not silently turn an export into a production asset upload.
- Map Code Connect only after Figma properties and code props are inspected. Omit invalid correspondences rather than inventing a prop.
- Treat a Figma-to-Shopify sync as a proposal until a repository diff, schema ownership, and release approval exist.

Report auth model (never the secret), scopes/capabilities, exact surface selected, endpoint or tool use, verification, and any approval still required. See [integration guardrails](references/integration-guardrails.md).
