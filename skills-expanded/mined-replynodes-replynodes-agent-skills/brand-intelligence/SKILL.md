---
name: brand-intelligence
description: "Internal: brand identity research guidance, merged into brand-kit. Route public brand identity retrieval for a known domain to brand-kit; this slug is not a separate public successor."
license: MIT
compatibility: "The free single-domain shortcut needs only network access; the optional authenticated MCP route requires an MCP-capable agent and REPLYNODES_API_KEY in a secret store."
metadata:
  internal: true
  author: ReplyNodes
  version: "1.1.0"
  endpoint: https://mcp.replynodes.com/mcp
  keywords: [brand intelligence, brand identity, internal, merged, brand-kit]
---

# ReplyNodes brand intelligence (internal)

This is an internal compatibility skill. Agent-skills issue #57 (canonical
taxonomy #56) merged `brand-intelligence` guidance into the canonical
[`brand-kit`](../brand-kit/SKILL.md) skill. The public successor for brand
identity retrieval is **`brand-kit`**; install that slug.

## What to do instead

- **Public brand identity for one known domain** → `brand-kit`:
  `GET https://brand.replynodes.com/{domain}` (free, zero-auth, read-only).
- **Logo-only intent** → [`brand-logo`](../brand-logo/SKILL.md).
- **Keyed brand operations** (`/v1/brand/search`, `/v1/brand/retrieve`,
  `/v1/brand/fonts`, `/v1/brand/styleguide`, `/v1/brand/logo`) via
  `https://mcp.replynodes.com/mcp` or the REST origin
  `https://api.replynodes.com` with `REPLYNODES_API_KEY` in a secret store.

Never paste, expose, commit, or log the key. Run `initialize` and `tools/list`
on MCP; the live schema is authoritative. This skill remains read-only: it
retrieves public signals only and cannot modify brand assets, accounts, or
websites.

## Migration

`brand-intelligence` is not a public successor and is not deleted in issue #57;
it is retained as internal migration guidance pointing to `brand-kit`. Registry
side unpublish/redirect and readback are owned by issue #58.
