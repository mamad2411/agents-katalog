---
name: ttl-429
description: Answer the research question "does a keep-alive ping that itself gets 429'd still refresh the prompt-cache TTL on Anthropic's side?" from captured turn-logs. A 429'd ping has no usage body, so its effect is only visible through the NEXT successful request on the same SESSION KEY. Runs .skills/ttl-429/scripts/ttl_429.mjs over one or more instance.*.ndjson turn-logs and classifies every 429'd ping as REFRESH (warm probe across the TTL boundary, no masking 200), NO-REFRESH (cold probe), or INCONCLUSIVE (boundary not crossed, or a success refreshed it first). Also prints per-session ping warmth, which flags PHANTOM keep-alive loops (a session whose every ping reads cold — an uncacheable aux context that should never have been armed). Pass --ttl-sec 3600 for an arm running --inject-extended-cache-ttl; default 300s is Anthropic's stock cache TTL. Read-only post-hoc analysis; spends no tokens.
---

# 429'd-ping → cache-TTL analyzer

Run from the project root:

```
node .skills/ttl-429/scripts/ttl_429.mjs [--ttl-sec N] <instance.ARM.ndjson> [more.ndjson ...]
```

## The question

clawback's keep-alive ping re-reads the cached prefix, so a **successful**
ping (200, `cache_read>0`) demonstrably refreshes Anthropic's TTL. The open
question is the **429'd** ping: Anthropic returns no usage body, so we cannot
see whether the request still touched the cache. The only observable is the
**next success on the same SESSION KEY**.

## How it decides

For each 429'd ping it finds the next 200-with-usage on that session and asks:
did more than `--ttl-sec` elapse since the last known-warm event (so the cache
*should* have expired), with no intervening success to refresh it? If yes and
the probe still reads warm → **REFRESH** (the 429'd ping kept it alive). If the
probe reads cold → **NO-REFRESH**. If the boundary was never crossed, or a 200
landed first, → **INCONCLUSIVE**.

## What you need for a clean answer

A paired run where the cache is allowed to go **cold across the TTL boundary
with only a 429'd ping spanning it**. That means:

- a real inter-turn gap longer than the TTL (default 300s, or 3600s under
  `--inject-extended-cache-ttl`);
- **no** PTY 🔥 keep-alive (billable turns would refresh both arms and erase
  the isolation);
- keep-alive ON on the primary, OFF on the shadow;
- enough rate-limit pressure that the primary's gap-ping actually 429s.

Without 429'd pings the analyzer says so plainly — the stock cadence keeps the
cache warm, so no ping is ever isolated across a boundary.

## Phantom detection (bonus)

The per-session warmth table flags any session with ≥3 pings and **zero** warm
pings as `⚠ PHANTOM`: an uncacheable aux context (sub-1024-token prefix) the
keep-alive armed and is pinging for pure cost. Cross-check against the
`keepAliveMinPrefixBytes` gate in `src/keepalive.js`.
