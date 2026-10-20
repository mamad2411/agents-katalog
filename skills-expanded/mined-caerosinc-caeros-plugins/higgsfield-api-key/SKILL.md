---
name: higgsfield-api-key
description: Set up Higgsfield access, both the OAuth-based MCP connection and Cloud API keys for direct integrations. Use when the user needs to connect Higgsfield, authenticate, or wire credentials into code.
---

# Higgsfield account and key setup

There are two separate auth paths. Pick based on what the user is doing.

## Path 1: MCP connector (this plugin, no API key)

The hosted MCP server at `https://mcp.higgsfield.ai/mcp` authenticates with
the user's Higgsfield account via OAuth. There is no key to create or store.

1. The user needs a Higgsfield account at https://higgsfield.ai with credits
   on their plan (generations spend those credits).
2. On first use of the connector, a browser OAuth flow opens; sign in and
   approve. Caeros stores the session, not a key.
3. If tools start failing with auth errors, disconnect and reconnect the
   Higgsfield server to refresh the OAuth grant.

## Path 2: Cloud API key (direct code integrations)

For scripts and backends using the REST API or the `higgsfield-client`
Python SDK:

1. Create an account at https://cloud.higgsfield.ai (email, Google, Apple,
   or Microsoft sign-in). Note: Higgsfield Cloud is the developer platform;
   its plans and credits are managed there.
2. Generate credentials at https://cloud.higgsfield.ai/api-keys.
3. Export them as environment variables and read them from the environment
   in code. The SDK README documents the exact variable names it reads
   (https://github.com/higgsfield-ai/higgsfield-client); do not hardcode
   credentials in source.

```bash
# example shape: keep real values in your shell profile or a secrets manager
export HIGGSFIELD_API_KEY="..."   # from cloud.higgsfield.ai/api-keys
```

## Hygiene

- Never commit keys; add secret files to `.gitignore` and use a vault for
  production.
- Rotate keys from the same dashboard page if one leaks; old keys stop
  working immediately after revocation.
- Watch the usage dashboard: credits are plan-based and can run out
  mid-batch. Check the current plan's terms for credit expiry.
- API access and rate limits vary by plan tier; if requests start failing
  under load, check the plan before debugging code.
