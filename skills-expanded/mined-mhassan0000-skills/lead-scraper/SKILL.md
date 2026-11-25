---
name: lead-scraper
description: Scrape leads from LinkedIn Sales Navigator via Vayne and enrich with verified emails via AnyMailFinder. Use when building lead lists, prospecting, finding potential clients, or doing outbound sales research.
allowed-tools: Read, Grep, Glob, Bash
---

# Lead Scraper — LinkedIn Sales Navigator + Vayne + Email Enrichment

## Goal
Build a high-quality list of ~2,000 leads by scraping LinkedIn Sales Navigator via Vayne, then enriching each lead with verified email addresses via AnyMailFinder. Quality is significantly higher than Apollo because we're sourcing directly from LinkedIn profiles.

## Inputs
- **Sales Navigator URL**: A LinkedIn Sales Navigator search URL with your filters applied
- **Order name**: A unique name for this batch (e.g., "SaaS CEOs March 2026")
- **Limit** (optional): Max leads to scrape (default: all)

## Building Sales Navigator URLs

**CRITICAL**: LinkedIn filter IDs (job titles, regions, industries, etc.) are proprietary internal values. Do NOT guess them — they will return wrong results silently. There are two ways to get the right URL:

### Option A: User provides a URL (preferred)
The user builds the search in Sales Navigator's UI, applies filters, and pastes the URL. This is the most reliable method.

### Option B: Build from known filters + keywords
Use `data/linkedin_filters.json` for known filter IDs and keywords for the niche/industry.

**Keywords are the primary targeting mechanism.** Use them for industry/niche targeting (e.g., `"HVAC"`, `"PPC agency"`). Use structured filters only for things like job titles and geography where we have known IDs.

Example URL structure:
```
filters:List(
  (type:CURRENT_TITLE, values:List((id:8, text:Chief Executive Officer, selectionType:INCLUDED), ...)),
  (type:REGION, values:List((id:103644278, text:United States, selectionType:INCLUDED)))
),
keywords:("HVAC" OR "heating and cooling" OR "HVAC contractor")
```

**Known filter IDs** (from `data/linkedin_filters.json`):
- Job titles: CEO (8), COO (280), CTO (153), Founder (35), Co-Founder (103), Owner (1), Co-Owner (195), Partner (18)
- Regions: United States (103644278)
- Everything else: must be discovered from a real Sales Nav URL

When a new Sales Nav URL is provided, always parse it and add any new filter IDs to `data/linkedin_filters.json` for future use.

## Quick Start (One Command)
```bash
python3 execution/scrape_linkedin.py \
  --url "YOUR_SALES_NAVIGATOR_URL" \
  --name "SaaS CEOs March 2026" \
  --limit 2000
```

This single command will:
1. Validate the URL and show prospect count (no credits used)
2. Create a Vayne scraping order
3. Wait for scraping to complete (shows progress)
4. Download the CSV
5. Enrich each lead with verified emails via AnyMailFinder
6. Export to a new Google Sheet
7. Print the Sheet URL

## Process (Step-by-Step)

**IMPORTANT**: Run each step as a separate Bash call so output is visible incrementally. Do NOT run the full pipeline as one command — it's opaque and the user can't see progress.

### Step 1: Check URL (No Credits)
```bash
python3 execution/scrape_linkedin.py --url "YOUR_URL" --check-only
```
Show the user: prospect count, confirm filters look right.

### Step 2: Scrape + Download
```bash
python3 execution/scrape_linkedin.py --url "YOUR_URL" --name "My Campaign" --limit 50 --skip-enrichment --skip-sheets
```
Show the user: order ID, scraping progress, CSV downloaded. Spot-check a few rows to verify the leads match the intended niche.

### Step 3: Enrich with Emails
```bash
python3 execution/enrich_leads.py --input .tmp/YOUR_RAW_CSV.csv
```
Show the user: how many pre-enriched from Vayne, how many found via AnyMailFinder, success rate.

### Step 4: Export to Google Sheets
```bash
python3 execution/export_leads_to_sheets.py --input .tmp/YOUR_ENRICHED_CSV.csv --create "LinkedIn Leads - Campaign Name" --valid-only
```
Show the user: Sheet URL, row count.

### Step 5: Verify Leads
After each scrape, spot-check 3-5 leads from the CSV to confirm they match the intended niche. If they don't, the URL filters are wrong — ask the user for a corrected Sales Nav URL.
- Company website

## Options
| Flag | Description |
|------|-------------|
| `--url` | Sales Navigator search URL (required) |
| `--name` | Unique name for the order |
| `--limit` | Max leads to scrape |
| `--check-only` | Validate URL, show count (no credits) |
| `--skip-enrichment` | Skip AnyMailFinder email lookup |
| `--skip-sheets` | Skip Google Sheets export |

## Execution Scripts
| File | Purpose |
|------|---------|
| `execution/scrape_linkedin.py` | Full pipeline orchestrator |
| `execution/vayne_client.py` | Vayne API client (LinkedIn scraping) |
| `execution/enrich_leads.py` | CSV enrichment with AnyMailFinder |

## Cost Estimates
For 2,000 leads with ~40% email hit rate:
- 2,000 Vayne credits (check your plan)
- 2,000 AnyMailFinder lookups → ~800 valid emails → ~$16-40
- Google Sheets: Free

## Environment
Requires in `.env`:
```
VAYNE_API_KEY=your_vayne_api_key
ANYMAILFINDER_API_KEY=your_anymailfinder_key
GOOGLE_APPLICATION_CREDENTIALS=config/credentials_leftclick.json
```
Google Sheets export uses `config/token_leftclick.json` for OAuth (has Sheets + Drive scopes). The default `token.json` does NOT have Sheets scope.

## Quality Notes
- Expect 60-75% email match rate on first pass
- Verified emails (confidence > 90%) typically 40-50% of total
- Much higher quality than Apollo because sourced directly from LinkedIn profiles
- Vayne requires Sales Navigator subscription
- AnyMailFinder bulk API is fast; some slow responses are normal (180s timeout)

## Edge Cases
- **Order name conflict**: Script auto-generates timestamps, but use unique names
- **Low email hit rate (<20%)**: Check domain extraction; healthcare/government have lower rates
- **LinkedIn session expired**: Log into Vayne dashboard and reconnect LinkedIn
- **Rate limits**: Vayne: 3 req/5s, 20/min — handled automatically with delays

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
