# Google Drive -> Cold Email Enrichment -> Instantly Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Takes a CSV of LinkedIn leads (scraped from Sales Nav / Apollo / Apify — any scraper output works), finds each person's work email via Anymailfinder, generates a GPT-4 personalized icebreaker from their LinkedIn profile data, then pushes the complete lead into an Instantly campaign — ready to send.

Original Make scenario: 2 linked flows, 10 nodes total — Google Drive trigger, Google Sheets read, GPT-3.5 name cleaner, Anymailfinder enrichment (async webhook), GPT-4 icebreaker generator, JSON parse, Instantly lead add.

The Python version collapses both flows into one synchronous pipeline: read leads from CSV, clean names, call Anymailfinder synchronously, generate icebreaker, write enriched rows to output CSV and optionally push to Instantly.

---

## When to trigger

- "Run the cold email enrichment skill"
- "Enrich leads and add to Instantly"
- "Find emails for my LinkedIn leads and write icebreakers"
- "Run the Google Drive cold email flow"
- `/google-drive-cold-email-enrichment-insta`

---

## Environment variables

```
OPENAI_API_KEY=sk-...              # required — GPT-3.5 name cleaner + GPT-4 icebreaker
ANYMAILFINDER_API_KEY=...          # required — email enrichment
INSTANTLY_API_KEY=...              # required if pushing to Instantly; skip to just write output CSV
INSTANTLY_CAMPAIGN_ID=...          # required if pushing to Instantly
```

Optional (only needed if switching to Google Sheets):
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```

---

## Step-by-step procedure

1. **Confirm data mode.** Ask the user "keep CSVs (default) or use Google Sheets?" — default is CSV, no setup needed.

2. **Check env.** Verify `OPENAI_API_KEY` and `ANYMAILFINDER_API_KEY` are set. If pushing to Instantly, also confirm `INSTANTLY_API_KEY` and `INSTANTLY_CAMPAIGN_ID`. If any are missing, ask the user to add them to their `.env` file.

3. **Confirm input file.** Default is `data/input.csv`. The required columns are `fullName`, `companyName`, `title`, `summary`, `titleDescription`, `companyLocation`, `location`. Any extra columns are passed through to the output unchanged. A minimal working sample is at `data/input.csv`.

4. **Confirm push behavior.** Ask: "Do you want to push enriched leads directly to Instantly, or just write to output CSV?" Default is CSV-only (safer — lets you review before sending). Pass `--push-instantly` flag to enable push.

5. **Run the script:**

   ```bash
   cd /path/to/skill/
   python3 scripts/run.py
   ```

   With options:
   ```bash
   python3 scripts/run.py \
     --input data/input.csv \
     --output data/output.csv \
     --push-instantly \
     --max 50
   ```

   `--max` caps how many leads to process in one run (useful for rate-limit safety).

6. **Review output.** The script writes `data/output.csv` with all original columns plus: `email_found`, `email`, `email_status`, `clean_name`, `icebreaker`, `instantly_pushed`. Rows where Anymailfinder returns no email are written to `data/no_email.csv` — you can re-run or skip them.

7. **Done.** If you used CSV-only mode, import `data/output.csv` into Instantly manually. If you used `--push-instantly`, leads are already in your campaign.

---

## Node map (original Make scenarios -> script)

| Make node | Module | Script equivalent |
|---|---|---|
| Flow1:1 | `google-drive:watchFilesInAFolder` | `read_rows()` from `io_store.py` — reads `data/input.csv` instead |
| Flow1:8 | `util:SetVariables` (API key) | env var `INSTANTLY_API_KEY` |
| Flow1:2 | `google-sheets:filterRows` | `read_rows()` from `io_store.py` — maps sheet columns to dict fields |
| Flow1:6 | `openai-gpt-3:CreateCompletion` GPT-3.5 | `clean_name()` in `run.py` — few-shot prompt, removes emojis + fixes caps |
| Flow1:5 | `util:SetVariables` (escape) | `sanitize_fields()` in `run.py` — replaces newlines/quotes in text fields |
| Flow1:3 | `http:ActionSendData` Anymailfinder | `find_email()` in `run.py` — POST to Anymailfinder v5.1 `/find-email/person`, bare key auth |
| Flow2:1 | `gateway:CustomWebHook` | collapsed — `find_email()` returns result directly (no webhook needed) |
| Flow2:2 | `openai-gpt-3:CreateCompletion` GPT-4 | `generate_icebreaker()` in `run.py` — GPT-4-turbo, returns JSON `{icebreaker}` |
| Flow2:3 | `json:ParseJSON` | `json.loads()` on GPT-4 response |
| Flow2:4 | `http:ActionSendData` Instantly | `push_to_instantly()` in `run.py` — POST to Instantly v2 `/api/v2/leads/add`, Bearer auth |
