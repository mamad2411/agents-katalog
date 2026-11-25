---
name: bug-bounty-target-selection
description: Use when picking bug bounty targets from platform dumps.
tags: [bug-bounty, recon, target-selection, osint]
version: 1.0.0
author: Me
license: MIT
metadata:
  hermes:
    tags: [bug-bounty, recon, target-selection, osint]
    related_skills: [bug-bounty-methodology, redmess-arsenal]
---

# Bug bounty target selection

## When to Use
- User asks to pick/rank bug bounty targets, "cari korban", "scrap data tebasan", or re-scrap program data.
- Before committing to a program: verify it is paid, open, and responsive from live dumps.
- Any task needing the current scope (domains/wildcards) of public bounty programs.

Rank real bounty programs from live data instead of guessing. Source: arkadiyt/bounty-targets-data — daily dump of HackerOne, Bugcrowd, YesWeHack, Intigriti programs plus pre-extracted domain/wildcard lists (~600 paid programs at any time). Full per-platform field map and parse recipe: `references/field-map.md`.

## Procedure
1. Download all four dumps fresh each hunt — programs open/close and scope shifts daily:
   ```bash
   mkdir /tmp/bb && cd /tmp/bb
   for plat in hackerone bugcrowd yeswehack intigriti; do
     curl -sL -o ${plat}_data.json https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/${plat}_data.json
   done
   curl -sL -o domains.txt   https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/domains.txt
   curl -sL -o wildcards.txt https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/wildcards.txt
   ```
2. Sanity-check file sizes before parsing — each dump is 100KB–18MB; a ~14-byte file is a 404 page, not data. State the freshness ceiling in the report: the dump's newest commit date (`https://api.github.com/repos/arkadiyt/bounty-targets-data/commits?per_page=1`) is as fresh as any scrape can get — re-scrapes within hours of that commit yield near-identical numbers, so lead with the churn delta instead of re-deriving the full ranking.
3. Filter to paid + open: HackerOne `offers_bounties == True` AND `submission_state == 'open'`; Bugcrowd `max_payout > 0`; Intigriti check `status` and coerce `max_bounty` defensively (field can be non-int).
4. Score each program (higher = more attractive):
   - **response_efficiency_percentage** — reports actually get read; weight heaviest.
   - **bounty-eligible ratio** — `eligible_for_bounty` targets ÷ total in-scope; 100% beats partial (mixed VDP scope = wasted shots).
   - **wildcard count** — `asset_type == 'WILDCARD'` targets; subdomain surface feeds subfinder/nuclei directly.
   - **critical severity allowed** — `max_severity == 'CRITICAL'` headroom.
   - **domain fit** — fintech / login-heavy / payments (IDOR = money) over static marketing sites.
5. Sort and report top 5–10 to the user with the numbers that justify each rank (resp %, scope count, eligible count, wildcard list excerpt) — one block per program, a verdict line at the end, then ask for the one-word target pick.
6. Keep the scored list on disk — the user often asks to re-scrap later; diff old vs new to report program churn.

## Pitfalls
- Platform filenames use UNDERSCORES (`hackerone_data.json`); hyphenated names 404 and leave a ~14-byte error page that looks like a successful download. Check size, not exit code.
- Match programs by their `name` field, never a guessed `handle` — handles drift (name "8x8" ↔ handle `8x8-bounty`); build a name→handle map before per-handle lookups.
- Do not trust a single headline metric: pair response efficiency with the bounty-eligible ratio — a 100%-responsive program with mostly-VDP scope pays nothing for most findings.

## Leverage
- `wildcards.txt` (~3.5k lines) is pre-extracted scope — feed it straight into subfinder; do not re-derive from the program JSON.
- Rare top-tier signal: 100% response efficiency + 100% bounty-eligible scope + triple-digit in-scope count + dozens of wildcards in ONE program — flag it to the user immediately; almost nothing else in the dataset matches it.
