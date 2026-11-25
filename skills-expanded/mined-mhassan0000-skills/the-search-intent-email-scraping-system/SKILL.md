# The Search Intent Email Scraping System (+15% Reply Rates)

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

This system scrapes LinkedIn job postings (via Apify) to find companies that are actively hiring for sales development roles. The idea: if a company is hiring an SDR, they have a sales motion and a budget. That's a warm signal for outreach. It then finds the decision maker's email (via Anymailfinder), researches them with Perplexity, writes a personalized icebreaker with GPT-4o, and pushes them straight into an Instantly cold email campaign — all automated, all deduplicated.

The +15% reply rate claim comes from the personalization layer: instead of generic openers, each lead gets a 1-2 line icebreaker grounded in real context about them specifically.

**Two-phase pipeline:**
1. **Phase 1 — Scrape & Filter:** Pull LinkedIn jobs from Apify, filter for SMB companies (under 150 employees, real website), deduplicate against your local CSV, classify relevance via GPT-4o-mini, submit for email enrichment
2. **Phase 2 — Enrich & Send:** Receive Anymailfinder results, research the DM with Perplexity, generate an icebreaker with GPT-4o, write back to CSV, add to Instantly campaign

## When to trigger

Say things like:
- "run the search intent scraper"
- "scrape linkedin jobs and find emails"
- "run phase 1" / "run phase 2"
- "process anymailfinder results from [file]"
- "/search-intent-email-scraping-system"

## Env vars required

```
APIFY_API_TOKEN=
ANYMAILFINDER_API_KEY=
OPENAI_API_KEY=
PERPLEXITY_API_KEY=
INSTANTLY_API_KEY=
INSTANTLY_CAMPAIGN_ID=
```

Optional (for Google Sheets mode only):
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```

## Data schema

`data/input.csv` is the job/lead database. Columns:

| Column | Description |
|---|---|
| id | Apify job ID |
| trackingId | LinkedIn tracking ID |
| link | Job post URL |
| title | Job title |
| companyName | Company name |
| companyLinkedinUrl | Company LinkedIn URL |
| location | Job location |
| postedAt | Post date |
| descriptionText | Job description (plain text) |
| companyWebsite | Company domain |
| companyEmployeesCount | Headcount |
| companyDescription | Company blurb |
| personFullName | DM full name (filled post-enrichment) |
| email | DM email (filled post-enrichment) |
| jobTitle | DM job title (filled post-enrichment) |
| linkedInUrl | DM LinkedIn URL (filled post-enrichment) |
| icebreaker | Generated personalized opener (filled post-enrichment) |
| addedToCampaign | "true" once pushed to Instantly |

`data/output.csv` is written by phase 2 and mirrors the enriched rows.

## Step-by-step procedure

### Phase 1: Scrape & Filter

**Step 1 — Set up your Apify actor**

Before running the script, you need to manually kick off the [LinkedIn Jobs Scraper](https://apify.com/curious_coder/linkedin-jobs-scraper) actor on Apify. Set your search query (e.g. "Sales Development Representative"), configure it, and run it. Grab the `datasetId` from the completed run.

**Step 2 — Run the scraper**

```bash
python3 scripts/scrape_and_filter.py \
  --dataset-id YOUR_APIFY_DATASET_ID \
  --db-path data/input.csv
```

This will:
- Fetch up to 100 jobs from the Apify dataset
- Filter: companyWebsite exists, not careers.linkedin.com, headcount < 150
- Deduplicate: skip companies already in `data/input.csv`
- Call GPT-4o-mini to classify each job as relevant (SDR/sales-dev roles only)
- For each relevant, new company: POST to Anymailfinder `/v5.1/find-email/decision-maker` (synchronous — email + person data returned immediately in the response) and write the result directly into the row
- Write new rows to `data/input.csv`

**Step 3 — No wait needed (v5.1 is synchronous)**

Anymailfinder v5.1 returns email + person data directly in the POST response. Phase 1 writes enrichment data inline into `data/input.csv`. If any rows are missing email after phase 1 (e.g. a transient API error), run:

```bash
python3 scripts/poll_anymailfinder.py --db-path data/input.csv
```

This re-submits unenriched rows to the v5.1 endpoint and updates the CSV.

### Phase 2: Enrich & Send

Once you have Anymailfinder results (either via polling or callback):

```bash
python3 scripts/enrich_and_send.py \
  --db-path data/input.csv \
  --output-path data/output.csv
```

This will:
- For each row in `data/input.csv` that has an `email` but no `icebreaker` (i.e. not yet processed)
- Research the DM with Perplexity (`llama-3.1-sonar-small-128k-online`), querying `{name} {jobTitle} {companyName}`
- If Perplexity returns > 500 characters, use GPT-4o to generate a personalized icebreaker (casual bar conversation tone, no exclamation points, no questions)
- Update the row with `personFullName`, `email`, `jobTitle`, `linkedInUrl`, `icebreaker`
- If `addedToCampaign` is not "true", add the lead to Instantly with `icebreaker` as the personalization field
- Mark `addedToCampaign = true` in the CSV
- Write enriched rows to `data/output.csv`

### Running both phases end-to-end

```bash
# Phase 1
python3 scripts/scrape_and_filter.py --dataset-id abc123 --db-path data/input.csv

# Wait for enrichment, or use polling:
python3 scripts/poll_anymailfinder.py --db-path data/input.csv

# Phase 2
python3 scripts/enrich_and_send.py --db-path data/input.csv --output-path data/output.csv
```

## Notes

- The deduplication check compares `companyName` — same company won't get two rows
- The Instantly `campaign_id` defaults to `INSTANTLY_CAMPAIGN_ID` env var; you can override per-run with `--campaign-id`
- Anymailfinder v5.1 endpoint (`decision_maker_category: ["ceo"]`) looks for the top decision maker at the domain synchronously — works well for sub-150 SMBs
- If Perplexity returns fewer than 500 characters (not enough context), icebreaker generation is skipped and the lead is still added to Instantly without a personalization line
- If `PERPLEXITY_API_KEY` is not set, icebreaker generation is skipped gracefully for all rows; leads still go to Instantly (without personalization)
