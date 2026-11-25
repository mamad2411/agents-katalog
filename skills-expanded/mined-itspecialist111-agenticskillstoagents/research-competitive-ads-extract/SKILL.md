# research/competitive-ads-extract — skill payload

> Machine-readable contract: [`../competitive-ads-extract.manifest.json`](../competitive-ads-extract.manifest.json).

## What this skill does

Given a competitor's name or domain, queries public ad-library sources
(Meta Ad Library, Google Transparency Centre) for ads they're currently
running and returns structured records: ad copy, creative URL, landing
URL, observed audience signals, first/last seen dates, platform.

Read-only across public sources — no logged-in account state, no
scraping behind paywalls.

## When to use it

- A marketing analyst wants to see what messaging a competitor is
  testing right now.
- A product team wants signal on what features a competitor is
  emphasising in paid acquisition.

## When **not** to use it

- The competitor isn't running public paid ads — output will be empty.
- You need historical depth beyond what the public libraries retain
  (typically ~90 days for Meta) — use a paid intelligence service.

## Determinism and risk

Determinism: **medium** — the upstream libraries are stable APIs but
content rotates daily. Risk: **low** — read-only of public data.

## How it composes

Natural pair with `research/lead-research` (build the lead dossier and
also show what they're paying to say). Output is ready to feed into
`content/research-writer` for "competitor positioning" briefs.
