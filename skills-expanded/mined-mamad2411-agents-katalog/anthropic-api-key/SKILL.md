---
name: anthropic-api-key
description: Set up Anthropic credentials — API keys, OAuth profiles via the ant CLI, CI credentials, and wiring a key into Caeros' own model settings. Use when the user needs to create, configure, or debug Anthropic authentication.
---

# Anthropic API Key Setup

## Get a key

Create keys in the Anthropic Console (https://platform.claude.com — API keys
are workspace-scoped; use one workspace per trust boundary). Never commit a
key; never paste one into chat history.

## Use it

- **Environment**: `export ANTHROPIC_API_KEY=sk-ant-...` — every SDK's
  zero-arg client (`anthropic.Anthropic()`) picks it up.
- **OAuth profile (no static key)**: `ant auth login` stores a profile under
  `~/.config/anthropic/`; SDKs and the `ant` CLI resolve it automatically.
  Raw HTTP with a profile token: `Authorization: Bearer $(ant auth
  print-credentials --access-token)` PLUS the header
  `anthropic-beta: oauth-2025-04-20`.
- **CI / servers**: use Workload Identity Federation env vars
  (`ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`,
  `ANTHROPIC_SERVICE_ACCOUNT_ID`, `ANTHROPIC_IDENTITY_TOKEN_FILE`) instead of
  long-lived keys.

The #1 trap: an exported `ANTHROPIC_API_KEY` (even empty) silently overrides
profiles and WIF. `ant auth status` shows which credential source is active.

## In Caeros

To run Claude models inside Caeros itself, add the key under Settings →
Models (Anthropic provider). That powers the app's Claude lanes; it is
independent of any key your generated code reads from the environment.

## Organization admin (optional Composio app)

This plugin can bind the **Anthropic Admin** app via Composio (connect it
from the plugin page). When connected, use `apps_execute_tool` with
app=anthropic_administrator for organization-level operations — member and
workspace management, API-key inventory, usage and cost reports. Admin API
calls need an admin-scoped key; plain inference keys will 403 there.

## Hygiene

- Rotate on any suspected exposure; scope keys per environment.
- Prefer short-lived credentials (profiles, WIF) over static keys.
- If a request 401s with a seemingly valid key, check for BOTH
  `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` set — the API rejects
  requests carrying both.
