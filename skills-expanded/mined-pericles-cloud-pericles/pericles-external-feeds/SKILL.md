---
name: pericles-external-feeds
version: 2026.05.0
description: >
  How to integrate external data feeds (NOAA, GDELT, NVD, FRED, WHO/CDC, TheNewsAPI,
  X/Twitter, MarineTraffic, etc.) the Pericles way. Use this WHENEVER you add or change
  an external API call in a monitoring tool or a new feed. Encodes the timeout + UA
  convention, treating every response as untrusted, API-key handling, and the rule that
  new feeds go behind MCP while the existing inlined integrations are grandfathered.
doctrine_refs: [§5; Security §5]
depends_on: [pericles-mastra-tool, pericles-mcp-layer, pericles-prompts]
last_reconciled: 2026-05-28
---

# Pericles External Feeds (build skill)

The Topical tools reach the outside world: NOAA/USGS/EONET (weather), GDELT (political/
geopolitical), NVD/CISA (cyber), FRED (economic/regulatory), WHO/CDC (pandemic),
TheNewsAPI + X/Twitter (news/social), RSS (maritime/labor). These feeds are
**untrusted** and **flaky** — integrate them defensively.

## When to use this skill

Adding/changing an external API call in a monitoring tool; adding a new feed; debugging
a feed timeout or a malformed response.

## The conventions (as built)

- **Timeout every call:** `fetch(url, { signal: AbortSignal.timeout(10000) })`. No
  unbounded external calls.
- **Identify the client:** `User-Agent: Pericles-SupplyChainMonitor/1.0
  (contact@pericles.cloud)`.
- **Validate the response against a Zod schema** before use; treat the body as
  **untrusted data**, boundary-marked if it ever enters a prompt (`pericles-prompts`).
  A poisoned feed item must not become instructions or bypass the output schema.
- **Use the shared helpers** `output-limiter.ts` (cap result size) and `tool-logger.ts`
  (structured per-tool logging) (`pericles-mastra-tool`).
- **Degrade gracefully:** a feed failure logs to `MonitoringAuditLog`
  (`source_fetch`/`error`) and the cycle continues; one bad source never aborts the run.

## API keys

Optional feed keys live in env (`THENEWSAPI_API_KEY`, `TWITTERAPIIO_API_KEY`,
`OPENWEATHER_API_KEY`, `MARINETRAFFIC_API_KEY`, …) loaded from `.env.local`. Never hard-
code keys or put them in URLs/logs; missing optional keys disable that feed gracefully,
they don't crash the pipeline.

## MCP & grandfathering (§5)

The current inlined integrations are **grandfathered** — keep them working. **New** feeds
should be added behind MCP (`pericles-mcp-layer`) so they're swappable, audited, and
tenant-scoped, not inlined into a new tool's `execute()`.

## What this forbids

An external call without a 10s timeout; using a response without schema validation;
treating feed content as trusted/instructions; hard-coding API keys or putting them in
URLs/logs; a feed failure that aborts the whole monitoring cycle; inlining a NEW feed
instead of using MCP.

## Verification

Every external call has a timeout + UA; responses are schema-validated and treated as
untrusted; failures are logged and isolated (cycle continues); keys come from env and
never leak; new feeds are MCP-registered.

## Existing standards (read alongside)

`CLAUDE.md` (External API Integration Pattern); the 10 monitor tools;
`.cursor/rules/001-application/000-Integrations/*` (twitterapi-io, gdelt);
`pericles-mastra-tool`.

## Open questions

- Which feeds migrate to MCP first (the highest-churn or licensed ones) — sequence with
  `pericles-mcp-layer`.
- Per-feed rate-limit handling (caching via `KeyValueStore`?) — define with
  `pericles-postgres-queue`.

## Changelog

- 2026.05.0 — Initial draft from the real external-API pattern; timeout/UA, untrusted
  responses, env keys, MCP-for-new / grandfather-inline.
