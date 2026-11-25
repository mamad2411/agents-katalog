# Indeed Automatic Resume Customization Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

This skill scrapes job listings from Indeed for any role and location, then rewrites your resume for each job using GPT-4o. The rewrite keeps your actual work history (companies and dates stay the same) but rewrites everything else — headline, summary, bullet points, skills section — to match the job's requirements and language. Results land in `data/output.csv` with one row per job, including the customized resume in markdown.

Optionally it can also save each resume as a Google Doc (one doc per job) if you've set up Google Docs credentials. Without that, the markdown output in the CSV is fully usable.

Two-phase flow matching the original Make.com workflow:
1. **Scrape** — fires Apify's `misceres/indeed-scraper` actor for your search query, polls until the run completes, fetches up to 100 results
2. **Customize** — for each job description, calls GPT-4o with a few-shot resume customization prompt, appends the result to the output CSV

---

## When to trigger

Use this when someone says any of:
- "customize my resume for Indeed jobs"
- "scrape Indeed and tailor my resume"
- "run the resume customization flow"
- `/indeed-automatic-resume-customization-fl`

---

## Env vars required

```
APIFY_API_TOKEN      # Apify API token (apify.com → Settings → Integrations)
OPENAI_API_KEY       # OpenAI API key

# Optional (only if exporting to Google Docs):
GOOGLE_APPLICATION_CREDENTIALS   # path to service account JSON
GOOGLE_DRIVE_FOLDER_ID           # Drive folder to save docs into (defaults to root)

# Optional (only if using Google Sheets instead of CSV):
SKILL_STORE=sheets
SKILL_SHEET_URL=<your sheet URL>
```

---

## Step-by-step procedure

1. **Check env vars** — confirm `APIFY_API_TOKEN` and `OPENAI_API_KEY` are set. If not, ask the user to add them.

2. **Load search config from input CSV** — `read_rows("data/input.csv")`. Each row is a search job: `position`, `location`, `country`, `max_items`. If the file doesn't exist, ask the user what role and location to search.

3. **Load the master resume** — read `data/resume.md`. If it doesn't exist, ask the user to paste their resume. Save it to `data/resume.md` for future runs.

4. **Run the scraper** — for each row in input.csv, call `scripts/scrape_jobs.py` which:
   - POSTs to Apify REST API to start actor `hMvNSpz3JnHgl5jkh` (misceres/indeed-scraper) with the row's search params
   - Polls the run status every 10 seconds until `SUCCEEDED`
   - Fetches up to 100 dataset items (JSON)

5. **Customize resume per job** — for each scraped job, call `scripts/customize_resume.py` which:
   - Sends a GPT-4o chat completion with the system prompt, two-shot example (hardcoded), then the real resume + job description
   - Model: `gpt-4o`, temp: 0.7, max_tokens: 4096
   - Returns markdown resume

6. **Write output** — append each job + its customized resume to `data/output.csv` using `write_rows()`. Columns: `position_name`, `posted_at`, `scraped_at`, `salary`, `job_type`, `company`, `location`, `description`, `url`, `customized_resume_md`.

7. **Optional: export to Google Docs** — if `GOOGLE_APPLICATION_CREDENTIALS` is set, call `scripts/export_gdoc.py` to create one Google Doc per job and add the doc URL to the output row.

8. **Done** — report how many jobs were scraped and customized. Print a summary table (position, company, location). Tell the user where the output file is.

---

## Run it

```bash
# Full run (scrape + customize):
python3 scripts/run.py

# Customize only from existing scraped CSV (skip Apify):
python3 scripts/run.py --customize-only data/scraped.csv

# Custom paths:
python3 scripts/run.py --input data/my_searches.csv --resume data/my_resume.md --output data/results.csv
```
