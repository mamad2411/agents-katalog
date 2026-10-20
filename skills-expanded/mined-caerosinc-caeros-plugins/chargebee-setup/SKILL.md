---
name: chargebee-setup
description: Set up Chargebee sites, API keys, test vs live environments, and connect your site's Chargebee MCP server. Use when configuring Chargebee access for development or production.
---

# Chargebee Site and Key Setup

## Sites: test vs live

A Chargebee **site** is one billing environment with its own subdomain,
catalog, keys, and webhooks. You get a test site (commonly `{site}-test`,
API base `https://{site}-test.chargebee.com/api/v2/`) and a live site.
Nothing syncs automatically between them: replicate catalog, webhooks, and
settings deliberately (or script it via the API). Test sites use gateway
test mode; use test card numbers, no real charges.

Keep the site name and API key paired in config; a live key against a test
site (or vice versa) fails auth.

```bash
export CHARGEBEE_SITE=acme-test
export CHARGEBEE_API_KEY=test_...   # from a secret manager, never committed
```

## API key types (Settings > Configure Chargebee > API Keys and Webhooks)

- **Full-access keys**: read and write on everything; server-side only.
- **Read-only keys**: reporting, dashboards, analytics jobs; also scoped
  restricted variants for specific needs.
- **Publishable keys**: limited client-safe operations (e.g. creating
  tokens/estimates in front-end flows); never grant more than needed.

Rotate keys from the same screen; create one key per consumer (app server,
ETL job, MCP) so revocation is surgical. Test keys are typically prefixed
`test_`, live keys `live_`.

## Catalog version check

Before writing integration code, confirm whether the site is Product
Catalog 1.0 (`plans`/`addons`) or 2.0 (`items`/`item_prices`); endpoint
names differ everywhere. New sites are PC 2.0. See
`chargebee-billing-integration` for the PC 2.0 patterns.

## Connect your site's MCP server

Chargebee's official MCP servers are **per-site**, so there is no fixed URL
this plugin can ship. To wire yours:

1. In the Chargebee admin console: Settings > Configure Chargebee >
   Agentic AI > MCP Servers.
2. Use a predefined server (Knowledge Base: docs and API reference
   answers; Data Lookup: customers, subscriptions, invoices, payments;
   Onboarding: catalog and demo data on test sites) or create a custom
   server from selected toolsets.
3. Enable MCP Access on the server, pick auth:
   - **API key**: requests carry `Authorization: Bearer YOUR-KEY`
     (up to 5 keys per server; good for server-to-server and dev tools).
   - **OAuth**: access mirrors the signed-in Chargebee user's permissions
     (not available on Multi-Business Entity sites).
4. Copy the server URL. Format by data center:
   - US: `https://{subdomain}.mcp.chargebee.com/{server-slug}`
   - EU: `https://{subdomain}.mcp.eu.chargebee.com/{server-slug}`
   - AU: `https://{subdomain}.mcp.au.chargebee.com/{server-slug}`
5. Add it to Caeros as a custom MCP server with that URL (and the Bearer
   header if using API-key auth).

Note: the old `@chargebee/mcp` npm package is deprecated; use the hosted
per-site servers above.

## Sane defaults before going live

- Webhooks configured on BOTH sites with Basic Auth set.
- Dunning schedule and terminal action reviewed (defaults may cancel
  subscriptions sooner than you expect).
- Time zone, currency list, and invoice numbering locked before first real
  invoice; some settings are hard to change later.
- Least-privilege keys distributed; full-access key count kept minimal.
