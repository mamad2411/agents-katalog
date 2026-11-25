---
name: tailscale-admin
description: Use when the user wants to manage their Tailscale tailnet via the Admin API — listing devices, retagging or removing nodes, managing auth keys, reading ACLs, or auditing the tailnet for stale devices and unused keys. Calls the Tailscale Admin API at api.tailscale.com using the TAILSCALE_API_TOKEN env var. Performs live writes against the user's tailnet. For local-node CLI ops (tailscale up/down/serve/funnel), see majiayu000/claude-skill-registry's tailscale skill instead.
---

# Tailscale Admin

## Prerequisites

- `TAILSCALE_API_TOKEN` — API access token from Tailscale admin console → Settings → Keys → API access tokens
- `curl` and `jq` on PATH
- Tailnet auto-resolved via the `-` shorthand (no separate env var needed)

If `TAILSCALE_API_TOKEN` is missing, **stop and ask the user to set it**. Do not invent or guess.

## When to use this skill

- The user mentions Tailscale, their tailnet, a Tailscale device, or `ts.net` hostnames.
- The user wants to audit or clean up devices, manage auth keys, or inspect ACLs.
- The user asks "what's on my tailnet" / "find stale devices" / "kick this node off" / "make me an auth key".

## API over CLI

This skill is for **tailnet-wide Admin API operations** (reachable from anywhere with a token). For local-node CLI ops on a machine running `tailscaled` (`tailscale up/down/status/serve/funnel/ssh/file`), use [`majiayu000/claude-skill-registry`](https://github.com/majiayu000/claude-skill-registry)'s Tailscale skill instead. The two are complementary.

## Entity model

Read [`references/entity-model.md`](./references/entity-model.md) before any create or update operation. Key constraints: device IDs are the public identifiers, tags use `tag:foo` format and **must be declared in the ACL `tagOwners` block before they can be applied**, and auth key secrets are returned **only once** at creation.

## Recipes (load on demand)

| Task | Reference |
|---|---|
| Read current ACL (read-only) | [`references/recipes/read-acl.md`](./references/recipes/read-acl.md) |
| List devices (with filters: tag, staleness, hostname) | [`references/recipes/list-devices.md`](./references/recipes/list-devices.md) |
| List / create / delete auth keys | [`references/recipes/auth-keys.md`](./references/recipes/auth-keys.md) |
| Delete / expire / retag a device | [`references/recipes/device-actions.md`](./references/recipes/device-actions.md) |
| Audit tailnet (composite: devices + keys + ACL summary) | [`references/recipes/audit-tailnet.md`](./references/recipes/audit-tailnet.md) |

For anything not covered, consult [`references/api-overview.md`](./references/api-overview.md) and Tailscale's API docs at https://tailscale.com/api.

## Safety

Writes go straight through. The host runtime (Claude Code, Cursor, Codex, etc.) gates network calls — **do not add a second confirmation layer in this skill**.

**High-impact ops — summarize before firing, never as one-liners without showing the user what will happen:**

- `DELETE /device/{id}` — permanently removes the device from the tailnet
- `POST /device/{id}/expire` — kicks the device offline immediately (re-auth required to rejoin)
- `POST /device/{id}/tags` — **replaces all tags, does not merge**; can break ACL-gated access
- `DELETE /tailnet/-/keys/{id}` — revokes the key (existing sessions unaffected, new connects fail)

## Limitations

- **ACL write deferred to v2** — needs `If-Match` ETag handling; lockout risk is real.
- **No DNS/MagicDNS recipes** — use the web UI.
- **No exit-node / subnet-router management** — use the web UI.
- **No OAuth client flow** — use API tokens; OAuth is the production-grade upgrade path (see `references/api-overview.md`).
- **Runtime device logs not available** — Tailscale doesn't expose per-device runtime logs via API.
