---
name: track-codex-resets
description: Build and maintain clear, timezone-aware Codex reset-credit expiry ledgers and predictions. Use when a user asks to fetch exact account reset-credit expiries, track Tibo/Codex reset credits, infer expiries from a visible reset-bank count, map reset credits to Tibo/OpenAI reset announcements, inspect reset-bank expiration, handle 30-day reset windows, parse X/Twitter reset-announcement URLs, render countdown tables, or emit Markdown/JSON reset ledgers for downstream export tooling.
---

# Codex Reset Credits

## Overview

Use this skill to turn Codex reset credits into an exact, scan-friendly expiry ledger. Prefer source-of-truth expiry timestamps from the account reset-credit endpoint or Codex UI when available; otherwise compute clearly labeled estimates from reset announcements, known public reset events, and the user's visible reset-bank count.

## Workflow

1. Gather reset evidence in this order:
   - Exact account reset-credit rows from `scripts/fetch_account_resets.py`.
   - Exact `expires_at` shown by Codex or another trusted collector.
   - Exact `grant_at` timestamp from a screenshot, API result, or user-provided text.
   - X/Twitter reset announcement URL; derive the post timestamp from the status ID when possible.
   - Relative phrases such as "yesterday" only after resolving them to a concrete date, time, and timezone.
2. Resolve the display timezone. Use the user's requested timezone, the local timezone, or ask for one if the output will be published or shared.
3. Use `scripts/fetch_account_resets.py` first when the user wants their own account's exact reset credits and local Codex auth is available.
4. Use `scripts/reset_expiry.py` for deterministic date math, public-event inference, and table rendering.
5. State the expiry rule. Default to `grant_at + 30 days` only when an exact expiry is unavailable.
6. Show each reset with local expiry, UTC expiry, time remaining, status, quantity, source, and uncertainty.
7. If using `auth.json`, read it only to authenticate the read-only endpoint. Do not print, store, commit, or transmit access tokens, refresh tokens, account ids, raw headers, or full endpoint payloads.

## Quick Start

From the skill directory:

```bash
python scripts/fetch_account_resets.py --timezone Asia/Kolkata --format markdown
```

If account fetch is unavailable, estimate from a public announcement:

```bash
python scripts/reset_expiry.py --timezone Asia/Kolkata https://x.com/thsottiaux/status/2070653282440405046
```

Render a persistent ledger:

```bash
python scripts/reset_expiry.py --input ../examples/resets.example.json --format markdown
```

Infer the likely expiry windows for a visible reset bank count:

```bash
python scripts/reset_expiry.py --bank-count 3 --timezone Asia/Kolkata
```

Use `--format json` when another tool, calendar exporter, website, or app extension will consume the result.
Use `--format ledger` with `fetch_account_resets.py` when saving sanitized account rows for later rendering.
Use `--view compact`, `--view table`, or `--view full` with Markdown output to control how much expiry detail is shown. Use `--limit N` to show only the next N expiring credits and `--hide-details` to suppress provenance notes.

## Input Rules

- Accept one-off reset inputs as positional values. Values may be ISO timestamps, X/Twitter status URLs, or `label=value` pairs.
- Accept durable ledgers with `--input path/to/resets.json`.
- Prefer `fetch_account_resets.py` for exact personal account data; it emits only sanitized fields.
- If a reset has `expires_at`, treat that as authoritative.
- If a reset has `grant_at` but no `expires_at`, compute `expires_at = grant_at + expiry_days`.
- If a reset has only an X/Twitter status URL, derive `grant_at` from the status ID and mark it as an announcement-based estimate.
- If the user only knows their reset-bank count, use `--bank-count N` to select the latest active likely bankable events from `assets/known-reset-events.json`.
- Use `--include-immediate` only for historical or diagnostic views; immediate resets are not the same as banked reset credits.

## Output Standards

- Always include local time and UTC time for the next expiry.
- In Markdown output, include an `Upcoming Expiries` list so every shown credit's expiry date is visible without horizontal scrolling.
- Sort by expiry time so the riskiest reset is first.
- Use status buckets: `expired`, `today`, `critical`, `soon`, `watch`, and `ok`.
- Make uncertainty visible. For example, "estimated from announcement URL" is different from "provided by Codex UI."
- Treat `confidence: exact` from the account endpoint differently from public-event estimates.
- When grant rollout timing is uncertain, show an expiry window instead of a single overconfident timestamp.
- For public output, avoid relative-only phrasing such as "next month"; include the exact calendar date and timezone.

## References

- Read `references/reset-credit-format.md` before changing the JSON schema, adding calendar export, designing a Codex app GUI, integrating screenshot/API collectors, or updating the public reset-event catalog.

## Verification

After edits, run:

```bash
python scripts/reset_expiry.py --timezone UTC https://x.com/thsottiaux/status/2070653282440405046
python scripts/reset_expiry.py --bank-count 3 --timezone Asia/Kolkata --format markdown
python scripts/reset_expiry.py --bank-count 3 --timezone Asia/Kolkata --format markdown --view compact --limit 2
python scripts/fetch_account_resets.py --input-response ../examples/account-resets.sample.json --timezone UTC --format markdown
python /path/to/skill-creator/scripts/quick_validate.py .
```
