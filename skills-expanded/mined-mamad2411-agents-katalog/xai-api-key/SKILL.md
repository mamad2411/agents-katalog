---
name: xai-api-key
description: Set up xAI credentials — create a key at console.x.ai, wire it into code, and enable Grok models plus native X search inside Caeros. Use when the user needs to configure or debug xAI authentication.
---

# xAI API Key Setup

## Get a key

Create an API key at https://console.x.ai (team-scoped; billing and rate
limits live there too). Never commit a key or paste one into chat.

## Use it in code

- Environment: `export XAI_API_KEY=xai-...`
- Requests: Bearer token in the `Authorization` header against
  `https://api.x.ai/v1`.
- OpenAI-compatible clients: pass the key as `api_key` with
  `base_url="https://api.x.ai/v1"`.

## Use it in Caeros

Add the key under Settings → Models (xAI provider). That unlocks:

- **Grok lanes**: Grok 4.6, Grok 4.5, and Grok Build as selectable models.
- **Native X search**: server-side X search fires on Grok lanes ("Searched
  X" in the transcript) — no X account required.

The in-app key is independent of any `XAI_API_KEY` your generated code reads
from its own environment.

## Hygiene

- One key per environment; rotate on exposure.
- Watch spend at console.x.ai — Grok 4.6 prompts at 200K tokens and above bill at
  double rates, which shows up as surprising line items.
- If Grok lanes don't appear after adding the key, verify the key is active
  in console.x.ai and re-open model settings; a 401 in the app's logs means
  the key itself, not the wiring.
