# Personalized 1000+ Cold Emails Using THIS AI System (FREE TEMPLATE)

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Takes a list of Apollo/LinkedIn search URLs, scrapes hundreds of leads from each one (via Apify), filters to people who have both a company website and an email, then deep-crawls up to 3 internal pages per company website. Each page gets summarized by GPT-4.1. Those summaries get fed into a second GPT-4.1 call that writes a hyper-personalized two-paragraph multiline icebreaker for each lead — one that sounds like you actually read their site, because you did.

End result: `data/output.csv` with one row per lead, including `first_name`, `last_name`, `email`, `website_url`, `headline`, `location`, `phone_number`, and `multiline_icebreaker`. Import directly into Instantly, Smartlead, etc.

Flow at a glance:

1. Read search URLs from `data/search_urls.csv`
2. Call Apify scraper for each URL (returns leads with org data)
3. Filter: keep only leads with both `organization.website_url` and `email`
4. For each lead — scrape their homepage, extract all internal links, normalize to relative paths, deduplicate, take up to 3
5. Fetch each sub-page HTML, convert to Markdown
6. Summarize each page with GPT-4.1 (structured JSON `{"abstract": "..."}`)
7. Aggregate all abstracts for the lead
8. Generate multiline icebreaker with GPT-4.1 (structured JSON `{"icebreaker": "..."}`)
9. Write output row to `data/output.csv`

---

## When to use this

- You're running a cold email campaign and want icebreakers that actually don't sound like icebreakers
- You have 100-1000+ leads to personalize and doing it by hand isn't realistic
- You want a fully local, auditable pipeline you can tune (swap models, change prompts, adjust crawl depth)

---

## Required env vars

```
OPENAI_API_KEY=your_openai_api_key
APIFY_API_TOKEN=your_apify_api_token
```

Add to `.env` or export in your shell. No Google OAuth needed by default.

---

## Step-by-step procedure

### Step 1 — Populate search URLs

Edit `data/search_urls.csv`. One row per search. Column: `URL`.

These are Apollo or LinkedIn Sales Navigator search URLs that the Apify actor knows how to paginate. Example: an Apollo search URL filtered to "CEO" + "web development agency".

### Step 2 — Scrape leads

```bash
python scripts/scrape_leads.py --input data/search_urls.csv --output data/leads_raw.csv
```

Calls the Apify `jljBwyyQakqrL1wae` actor for each URL (synchronous, blocks until done). Writes all returned leads to `data/leads_raw.csv`. Skips any lead missing `organization.website_url` or `email`.

Fields written: `first_name`, `last_name`, `email`, `headline`, `city`, `country`, `organization_website_url`.

### Step 3 — Generate icebreakers

```bash
python scripts/generate_icebreakers.py --input data/leads_raw.csv --output data/output.csv
```

Loops over each lead. For each one:
- Scrapes their homepage
- Extracts all `<a href>` links, normalizes to root-relative paths, deduplicates
- Fetches up to 3 internal sub-pages
- Converts each page's HTML to Markdown
- Summarizes each page with GPT-4.1 (one API call per page)
- Aggregates all abstracts, sends to GPT-4.1 to generate the multiline icebreaker
- Appends the result row to `data/output.csv`

Errors on individual lead pages are skipped (won't crash the whole run). Leads where all pages fail get an empty icebreaker field flagged as `scrape_error`.

### Step 4 — Import to your outreach tool

`data/output.csv` columns: `first_name`, `last_name`, `email`, `website_url`, `headline`, `location`, `phone_number`, `multiline_icebreaker`.

The `multiline_icebreaker` field contains the full two-paragraph opener, newlines included (CSV-quoted). Map it as a custom variable in Instantly/Smartlead.

---

## Node map (original n8n workflow)

| Original n8n node | Script / function |
|---|---|
| `Get Search URL` (Google Sheets read, "Search URLs" tab) | `io_store.read_rows("data/search_urls.csv")` |
| `Call Apify Scraper` (HTTP POST to Apify actor `jljBwyyQakqrL1wae`) | `scrape_leads.py` → `call_apify()` |
| `Only Websites & Emails` (filter) | `scrape_leads.py` → filter inline |
| `Scrape Home` (HTTP GET homepage) | `generate_icebreakers.py` → `scrape_homepage()` |
| `HTML` (extract `<a href>` links) | `generate_icebreakers.py` → `extract_links()` |
| `Edit Fields` (set/normalize fields) | `generate_icebreakers.py` → inline field mapping |
| `Loop Over Items` (splitInBatches) | `generate_icebreakers.py` → `for lead in leads` |
| `Split Out` (expand links array) | `generate_icebreakers.py` → `for link in links` |
| `Filter` (links starting with `/`) | `generate_icebreakers.py` → `normalize_links()` |
| `Code` (normalize URL paths to relative) | `generate_icebreakers.py` → `normalize_links()` |
| `Remove Duplicate URLs` | `generate_icebreakers.py` → `list(dict.fromkeys(...))` |
| `Limit` (max 3 pages) | `generate_icebreakers.py` → `links[:3]` |
| `Request web page for URL` (HTTP GET sub-pages) | `generate_icebreakers.py` → `fetch_page()` |
| `Markdown` (HTML to Markdown) | `generate_icebreakers.py` → `html_to_markdown()` (markdownify) |
| `Summarize Website Page` (GPT-4.1, JSON abstract) | `generate_icebreakers.py` → `summarize_page()` |
| `Aggregate` (collect abstracts) | `generate_icebreakers.py` → `abstracts` list |
| `Generate Multiline Icebreaker` (GPT-4.1, JSON icebreaker) | `generate_icebreakers.py` → `generate_icebreaker()` |
| `Add Row` (Google Sheets append, "Leads" tab) | `io_store.write_rows("data/output.csv")` (append mode) |
