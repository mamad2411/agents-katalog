# Build This Automated AI LinkedIn DM System in 1 Hour (N8N)

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Takes a plain-English audience description (e.g. "SaaS founders in the US, 1-50 employees"), converts it to an Apollo.io search URL via GPT, scrapes up to 500 matching leads via Apify, generates a personalized LinkedIn connection-request icebreaker for each lead via GPT-4o, writes all enriched leads to your data store, aggregates them, then kicks off a PhantomBuster agent to actually send the connection requests.

Original n8n workflow: 8 nodes — form trigger, GPT URL generator, Apify actor run, limit (3 leads for demo), GPT icebreaker personalizer, Google Sheets upsert, aggregate, PhantomBuster launch.

This skill replaces the Google Sheets node with `read_rows()` / `write_rows()` from `io_store.py`. All external API calls (OpenAI, Apify, PhantomBuster) use env-var keys, never hardcoded.

---

## When to trigger

- "Run the LinkedIn DM outreach skill"
- "Generate LinkedIn icebreakers for [audience]"
- "Build a LinkedIn connection campaign for [niche]"
- "Scrape Apollo leads and personalize LinkedIn messages"
- `/build-this-automated-ai-linkedin-dm-syst`

---

## Environment variables

```
OPENAI_API_KEY=sk-...               # required — URL generation + icebreaker personalization
APIFY_API_KEY=apify_api_...         # required — scrapes Apollo.io leads
PHANTOMBUSTER_API_KEY=...           # required — launches the connection-request agent
PHANTOMBUSTER_AGENT_ID=...          # required — ID of your PhantomBuster LinkedIn agent
```

Optional (only needed if switching to Google Sheets):
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```

---

## Step-by-step procedure

1. **Confirm data mode.** Ask the user "keep CSVs (default) or use Google Sheets?" Default is CSV.

2. **Check env.** Verify `OPENAI_API_KEY`, `APIFY_API_KEY`, `PHANTOMBUSTER_API_KEY`, and `PHANTOMBUSTER_AGENT_ID` are all set. If any are missing, ask the user to add them to their `.env` file.

3. **Get the audience description.** Ask: "Who are you targeting? Describe your audience in plain English (job title, company type, location, size)." Example: `"Founders and CEOs at creative agencies in the United States, under 200 employees."`

4. **Confirm lead limit.** Default is 10 leads (safe for testing). Ask: "How many leads do you want to process? Default is 10. The Apify actor can pull up to 500." Pass via `--limit`.

5. **Confirm PhantomBuster launch.** By default the script generates and saves leads but does NOT fire PhantomBuster (so you can review first). Ask: "Do you want to automatically launch PhantomBuster after saving leads, or just generate and review?" Pass `--launch-phantom` to trigger it.

6. **Run the script:**

   ```bash
   cd /path/to/skill/
   python3 scripts/run.py --audience "Founders and CEOs at creative agencies in the US"
   ```

   With optional overrides:
   ```bash
   python3 scripts/run.py \
     --audience "SaaS founders in the US, 1-50 employees" \
     --limit 25 \
     --output data/output.csv \
     --launch-phantom
   ```

7. **Review output.** The script writes `data/output.csv` with columns: `id`, `first_name`, `last_name`, `name`, `linkedin_url`, `title`, `email_status`, `photo_url`, `icebreaker`. Review the icebreakers before launching at scale — the GPT prompt paraphrases profile details to sound human-written.

8. **Launch PhantomBuster.** If you didn't pass `--launch-phantom`, you can kick off the agent manually once you're happy with the leads: `python3 scripts/launch_phantom.py`. This fires the POST to PhantomBuster's agent launch endpoint.

---

## Node map (original n8n workflow -> script)

| n8n node | Type | Script equivalent |
|---|---|---|
| On form submission | `formTrigger` | CLI `--audience` arg in `run.py` |
| Generate Search URL | `openAi` (gpt-4.5-preview) | `generate_apollo_url()` in `run.py` — chat completion, returns `{searchUrl}` |
| Run Apify Actor & Get Results | `httpRequest` POST | `scrape_apollo_leads()` in `run.py` — Apify actor `jljBwyyQakqrL1wae`, sync run |
| Limit | `limit` (maxItems: 3) | `--limit` CLI arg, slices lead list |
| Personalize Outreach | `openAi` (gpt-4o) | `personalize_icebreaker()` in `run.py` — chat completion with few-shot example, returns `{icebreaker}` |
| Add to Google Sheet | `googleSheets` appendOrUpdate | `write_rows()` from `io_store.py` — writes to CSV (or Sheets) |
| Aggregate | `aggregate` | list comprehension collects all rows before PhantomBuster trigger |
| Trigger PhantomBuster Agent | `httpRequest` POST | `launch_phantom.py` — POST to PhantomBuster agents/launch |
