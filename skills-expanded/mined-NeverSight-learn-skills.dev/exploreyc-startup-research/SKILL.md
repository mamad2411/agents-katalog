---
name: exploreyc-startup-research
description: "Startup and company intelligence with the ExploreYC API: search and filter YC/a16z portfolio companies, build landscape and company briefs, analyze batches and industries, and work from exported CSV/JSON in a local database when rate limits are tight."
---

# ExploreYC Startup Research

Use when the user asks about startups, YC companies, a16z portfolio companies, competitive landscapes, batch/industry trends, or wants BD/investor prospect lists. This skill wraps the ExploreYC API (https://www.exploreyc.com/) — a searchable dataset of 5,800+ portfolio companies.

## Setup

All live API calls require an API key:

```bash
export EXPLOREYC_API_KEY=...   # from https://www.exploreyc.com/api-docs
# optional override:
export EXPLOREYC_BASE_URL=https://api.exploreyc.com/api/v1
```

If `EXPLOREYC_API_KEY` is not set, `scripts/exploreyc.py` exits with a clear error. Never ask the user to paste the key into chat if an environment/secret mechanism exists; never print or log the key.

## Commands

```bash
python3 exploreyc-startup-research/scripts/exploreyc.py auth-check
python3 exploreyc-startup-research/scripts/exploreyc.py search --query fintech --limit 10 --source yc
python3 exploreyc-startup-research/scripts/exploreyc.py companies --search ai --batch "Summer 2024" --source all --limit 20
python3 exploreyc-startup-research/scripts/exploreyc.py company --slug stripe
python3 exploreyc-startup-research/scripts/exploreyc.py stats
python3 exploreyc-startup-research/scripts/exploreyc.py batches
python3 exploreyc-startup-research/scripts/exploreyc.py industries
python3 exploreyc-startup-research/scripts/exploreyc.py countries
python3 exploreyc-startup-research/scripts/exploreyc.py sources
python3 exploreyc-startup-research/scripts/exploreyc.py export-url --format csv --industry Fintech --source yc
```

Filters on `companies` and `export-url`: `--source yc|a16z|all`, `--batch`, `--industry`, `--country`, `--search`, `--is-hiring`, `--top-company`. Pagination: `--limit` (1–100), `--offset`. Add `--compact` before the subcommand for single-line JSON.

Company records include: `name`, `slug`, `website`, `one_liner`, `status`, `stage`, `industry`, `batch`, `country`, `founders`, `team_size`, `is_hiring`, `exit_type`, and more.

## Rate-limit strategy (important)

ExploreYC plans: **Free 5 requests/day**, Starter 500/day, Pro 5,000/day, Enterprise custom. Before calling the API:

1. Estimate how many calls the task needs. On the Free tier, budget calls like currency — one `stats` + one filtered `companies` call often answers the question.
2. For anything iterative (scoring many companies, cross-batch comparisons, list building), do **not** loop over the API. Use the ExploreYC export feature to download CSV/JSON once, then analyze locally — see `references/local-database-workflow.md`.
3. Cache results in the workspace (e.g. `data/exploreyc/`) and reuse them within a session.
4. On a 429, stop calling; switch to cached/exported data and tell the user which plan limit was hit.

## Research workflows

- **Landscape brief** — filter by industry/batch/country, group by stage/status, produce `templates/startup-landscape-brief.md`.
- **Company brief** — `company --slug ...` plus the user's context, produce `templates/company-intelligence-brief.md`.
- **Batch/source trends** — `stats`, `batches`, and filtered counts; compare across batches or between YC and a16z sources.
- **Prospect lists** — filter (e.g. `--is-hiring`, industry, country), then rank by the user's criteria; output a table with name, one-liner, website, batch, stage.
- **Local database analysis** — import exported CSV/JSON into SQLite and answer arbitrarily many questions without API spend.

## Boundaries

- Data comes from ExploreYC, an independent product; it is not an official Y Combinator or a16z service, and results are snapshots — say when data was fetched and do not overclaim freshness.
- Never fabricate companies, metrics, or API results. If a call fails or the key is missing, report that plainly.
- This is research support, not investment advice.

## References

- `references/agent-design.md` — first-version ClawMama Agent built on this skill.
- `references/local-database-workflow.md` — export → local SQLite workflow.
- `templates/` — landscape and company brief formats.
