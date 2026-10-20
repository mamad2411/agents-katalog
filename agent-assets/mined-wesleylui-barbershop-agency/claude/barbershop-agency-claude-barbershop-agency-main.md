# CLAUDE.md

Context for future Claude Code sessions in this repo. Read this first.

## What this repo is

A lead-generation pipeline for a barbershop marketing agency. It finds barbershops
with broken booking funnels via Google Maps + web scraping, scores them with Claude,
stores qualified leads in Supabase, and notifies the team via Discord.

## Architecture (`pipeline/`)

- **maps.py** — queries the Google Maps Places API for shops matching a niche + city and returns their basic details (name, address, website, phone, rating, review count).
- **scraper.py** — fetches a shop's website content as markdown via the Firecrawl API.
- **scorer.py** — sends shop details + scraped content to Claude (Haiku) using `prompts/scoring.txt` and returns a scored verdict as JSON.
- **database.py** — Supabase client wrapper for inserting/reading leads and pipeline runs.
- **notifier.py** — posts a run summary and the top qualified leads to a Discord webhook.
- **run.py** — orchestrates the pipeline (maps → filter → scrape → score → store → notify) and hosts the CLI / manual menu trigger.

## Conventions to follow

- **Commits:** Conventional Commits style (`feat:`, `fix:`, `chore:`, `docs:`), one logical
  change per commit, imperative mood. Body explains *why*, not *what*.
- **Do not touch business logic without confirmation first:** never modify scoring
  thresholds, verdict logic, or the qualification prompt (`prompts/scoring.txt`), nor the
  `cheap_filter()` thresholds in `run.py`. These are joint business/engineering decisions,
  not pure refactors.
- **Match the model to the task** in any Claude API calls: Haiku for scoring/classification,
  Sonnet for anything needing real reasoning (e.g. the learning-loop review).

## Current state

The daily auto-scrape is **paused**. The Railway `cronSchedule` has been removed because the
`barbershop Calgary` query pool is exhausted and there is an uncontacted outreach backlog.
Scraping is now **manual and menu-driven**: running `python -m pipeline.run` with no flags
shows a numbered menu of curated queries (from `pipeline/search_queries.py`). Passing
`--city` and `--niche` still runs a query directly for scripting/testing.

Do **not** "fix" this back to an automatic daily cron — the pause is intentional. See
`docs/SCRAPING.md` for the resume rule.
