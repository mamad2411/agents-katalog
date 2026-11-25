---
name: microsoft-clarity
description: Use when analyzing Microsoft Clarity live insights data, checking recent traffic quality signals, or breaking Clarity exports down by device, browser, country, source, or URL.
---

# Microsoft Clarity

Use this skill when the task is about recent Microsoft Clarity live insights for a project that already has a valid Clarity API token.

This repository currently focuses on the official Clarity Data Export API live insights endpoint:

- recent live-insights export for the last `1 / 2 / 3` days
- raw export as `table`, `json`, or `csv`
- basic overview summaries
- breakdowns by browser, OS, device, country, source, or URL
- frustration, errors, engagement, and traffic-quality summaries derived from live insights metrics
- structured implementation guidance for integration, consent, identify, tags, events, funnels, filters, and investigation playbooks
- local export caching enabled by default to reduce unnecessary repeat requests against the Clarity quota

It does **not** currently provide:

- heatmap export
- session replay export
- arbitrary date-range queries outside the API's `numOfDays=1..3`
- write operations or project management flows

For the current implementation scope and limitations, see [references/current-status.md](references/current-status.md).
Official reference: <https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api>

## When to Use

Use this skill when the user asks for things like:

- "show Clarity live insights for the last day"
- "break Clarity traffic down by device or browser"
- "which sources or pages got the most sessions in Clarity?"
- "export Clarity live insights to CSV or JSON"

Do **not** use this skill when the user primarily needs:

- GA4 event and conversion reporting
- Google Search Console query or page analysis
- Google Trends opportunity discovery

## Prerequisites

This skill discovers `.env` from the current working directory chain first, then the home directory chain, and also supports `--env-file`.

Start by copying [`.env.example`](../.env.example) to `.env` in your project directory or one of its parent directories.

Recommended variable:

```env
MICROSOFT_CLARITY_API_TOKEN=your-clarity-api-token
```

Token setup checklist:

- open the target Clarity project as a project admin
- go to `Settings` -> `Data Export`
- choose `Generate new API token`
- copy the generated token into your project `.env` as `MICROSOFT_CLARITY_API_TOKEN`
- keep the token out of the repository and rotate it if access changes

For a step-by-step setup guide, see [docs/microsoft-clarity-token-setup.md](../docs/microsoft-clarity-token-setup.md).

Install dependencies:

```bash
python -m venv microsoft-clarity/.venv
microsoft-clarity/.venv/Scripts/python -m ensurepip --upgrade
microsoft-clarity/.venv/Scripts/python -m pip install -r microsoft-clarity/requirements.txt
```

## Recommended Entry Points

Fetch a raw live-insights export:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/clarity_client.py ^
  --env-file .env ^
  --num-of-days 1 ^
  --dimensions device ^
  --format table
```

Force a fresh export and bypass the local cache:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/clarity_client.py ^
  --env-file .env ^
  --num-of-days 1 ^
  --no-cache
```

Get a basic overview:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/analyze.py ^
  --env-file .env ^
  --analysis-type overview ^
  --num-of-days 1
```

Review top traffic sources:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/analyze.py ^
  --env-file .env ^
  --analysis-type sources ^
  --num-of-days 1
```

Review top pages:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/analyze.py ^
  --env-file .env ^
  --analysis-type pages ^
  --num-of-days 1
```

Generate a custom event recommendation:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/guide.py ^
  --guide-type events ^
  --goal "track checkout intent"
```

Generate a consent recommendation:

```bash
microsoft-clarity/.venv/Scripts/python microsoft-clarity/scripts/guide.py ^
  --guide-type consent ^
  --region EEA
```

## Output Contract

Current output modes:

- `table`: human-readable CLI summary
- `json`: structured raw output for downstream processing
- `csv`: flattened export with `metricName` as the leading column

Current analysis coverage:

- `overview`
- `devices`
- `browsers`
- `countries`
- `sources`
- `pages`
- `os`
- `frustration`
- `errors`
- `engagement`
- `quality`

Capability boundary reference:

- [references/capability-map.md](references/capability-map.md)

Current cache behavior:

- export requests are cached on disk by request shape
- default TTL is `10800` seconds (`3` hours)
- use `--no-cache` to force a live request
- use `--cache-ttl-seconds` to override the default TTL

Current guidance coverage:

- `integration`
- `consent`
- `identify`
- `tags`
- `events`
- `funnels`
- `filters`
- `playbook`

## Common Failure Modes

### Authentication

Typical symptoms:

- `401 Unauthorized`
- `403 Forbidden`

Checks:

- verify `MICROSOFT_CLARITY_API_TOKEN`
- confirm the token belongs to the intended Clarity project

### Query Shape

Typical symptoms:

- request validation errors
- unexpectedly empty breakdowns
- exporting too often and hitting the Clarity quota

Checks:

- `--num-of-days` must be `1`, `2`, or `3`
- at most three dimensions are supported
- use the documented dimensions such as `Browser`, `OS`, `Device`, `Country/Region`, `URL`, `Source`, `Medium`, `Campaign`, `Channel`
- prefer the default local cache unless you explicitly need a fresh request

## Notes

- Do not commit real Clarity tokens.
- The current implementation targets the official Clarity Data Export API live insights endpoint.
- Current analysis is diagnostic and lightweight, not a full UX or CRO audit.
- `guide.py` generates structured recommendations; it does not create dashboard objects remotely.
