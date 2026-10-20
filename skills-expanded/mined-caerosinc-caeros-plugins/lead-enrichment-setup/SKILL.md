---
name: lead-enrichment-setup
description: Configure email-verification providers (MillionVerifier, BounceBan) for the Caeros enrichment engine. Use when enrich tools report provider_unavailable, when adding or rotating a provider API key, or when setting up a self-hosted gateway for enrichment.
---

# Lead Enrichment Setup

Provider keys are MANAGED: they live on the Caeros gateway and never reach
clients. There is nothing to configure in the desktop app or in Caeros
Secrets — requests authenticate with the user's session, and the gateway
signs provider calls server-side.

## Check what is configured

Run the `enrich_providers` tool. Each provider reports `configured` and
which one is the default (MillionVerifier is preferred when both have
keys). If none is configured, run creation fails with
`provider_unavailable`.

## Configuring keys (gateway operators only)

The gateway resolves each provider key through a chain, first hit wins:

1. `CAEROSGW_MILLIONVERIFIER_SECRET_REF` / `CAEROSGW_BOUNCEBAN_SECRET_REF` / `CAEROSGW_FULLENRICH_SECRET_REF`
   env vars holding an explicit secret reference.
2. Plain `MILLIONVERIFIER_API_KEY` / `BOUNCEBAN_API_KEY` / `FULLENRICH_API_KEY` env vars
   (local/dev).
3. GCP Secret Manager secrets named `MILLIONVERIFIER_API_KEY` / `FULLENRICH_API_KEY` /
   `BOUNCEBAN_API_KEY` in the gateway's project (production; the gateway
   service accounts need `roles/secretmanager.secretAccessor`).

Key sources: MillionVerifier keys come from the MillionVerifier dashboard
(API section); BounceBan keys from the BounceBan app. Standard hygiene:
never commit or paste keys in chat, and rotate a key immediately if it
ever transits an insecure channel — add a new secret version and the
gateway picks it up on next resolution.

## Verifying a new key

1. `enrich_providers` — the provider should now report `configured: true`.
2. `enrich_email_preview` with 1-2 addresses — a real verdict (not
   `unauthorized`) proves the key works end to end.

## Related

- `email-verification` skill: the operational flow (preview, run, export).
- The engine dispatcher runs inside the gateway by default;
  `CAEROSGW_NO_ENRICH_DISPATCHER=1` disables it and
  `CAEROSGW_ENRICH_DISPATCHER_INTERVAL` tunes the tick (default 3s).
