# Automatic Lead Magnet Generator Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Takes a list of lead magnet requests (topic, summary, company name, recipient email) and for each one:

1. Calls OpenAI (gpt-4) with a structured few-shot prompt to generate all the copy for a 5-section lead magnet as JSON.
2. Copies a Google Slides template, filling in every placeholder field (title, subheading, 5 section headings, 2 bullets, and all sub-headings + paragraphs across sections 2-5).
3. Sets the resulting Google Slides file to "anyone with the link can view."
4. Sends a personalized HTML email to the prospect with their name in the subject line and a direct link to the presentation.
5. Writes the outcome row (status, presentation URL, slide ID) to `data/output.csv`.

Original Make.com flow: `New Request Form Entry -> Generate Lead Magnet & Email to Prospect`. The Typeform webhook trigger and the 3s sleep delay are replaced by batch processing from CSV. Everything else maps 1:1.

---

## When to trigger this

- "run the lead magnet generator"
- "generate lead magnets for these requests"
- "process lead magnet queue"
- `/automatic-lead-magnet-generator-flow`

Any time you have a batch of prospect requests (topic + summary + email) and want a slide deck + delivery email for each one.

---

## Required env vars

```
OPENAI_API_KEY          # OpenAI API key
GOOGLE_SLIDES_TEMPLATE_ID   # Drive file ID of the master template presentation
                            # (original: 1h_xLn4LcUHMrUd29eQKkq0W7HI79hvA7ErqQGrjZZRs)
GOOGLE_APPLICATION_CREDENTIALS  # path to service account JSON with Drive + Slides + Gmail access
SMTP_FROM               # sender email address for outbound delivery email
SMTP_HOST               # SMTP host (or leave blank to use Gmail API via service account)
SMTP_PORT               # SMTP port (default 587)
SMTP_USER               # SMTP username
SMTP_PASS               # SMTP password
```

If `SKILL_STORE=sheets` is set, also set `SKILL_SHEET_URL` + `GOOGLE_APPLICATION_CREDENTIALS` for the CSV switch (handled by `io_store.py`).

---

## Input CSV columns (`data/input.csv`)

| column | description |
|---|---|
| `topic` | What the lead magnet should be about |
| `summary` | Brief notes on key points to include |
| `company_name` | The brand name to reference in the copy |
| `recipient_name` | First name for the email greeting |
| `recipient_email` | Where to send the finished presentation link |

---

## Step-by-step procedure

1. Read `data/input.csv` with `io_store.read_rows()`. Each row is one job.
2. For each row, call `generate_copy.py` which hits the OpenAI Chat API with the structured few-shot prompt (same system + 4-turn few-shot from the original flow). Model: `gpt-4`, temperature `0.7`, max_tokens `4096`. Parses the JSON response.
3. Call `slides_builder.py` which:
   a. Copies the template presentation (Drive API `files.copy`) into the user's Drive root.
   b. Sends a `batchUpdate` to replace all `{{placeholder}}` text in the copy with the generated JSON values (all 38 fields).
4. Call `drive_share.py` to set the new presentation to `reader` + `anyone` via Drive permissions API.
5. Call `email_sender.py` to send the HTML delivery email via SMTP (subject: `{recipient_name}, your lead magnet is ready`, body includes the share link).
6. Write result rows to `data/output.csv` via `io_store.write_rows()` — columns: everything from input + `slide_id`, `share_link`, `status`, `error`.

Run the full pipeline:

```bash
python3 scripts/run_pipeline.py --input data/input.csv --output data/output.csv
```

Or process a single row inline (handy for testing):

```bash
python3 scripts/run_pipeline.py --input data/input.csv --output data/output.csv --limit 1
```

---

## How to use this (Claude Code)

1. Download and unzip the attached folder.
2. Drop it into `.claude/skills/` in your project (so you have `.claude/skills/automatic-lead-magnet-generator-flow/SKILL.md`).
3. Fill in `data/input.csv` with your prospect rows.
4. Set the env vars above in your `.env` or shell.
5. Invoke by saying "run the lead magnet generator" or `/automatic-lead-magnet-generator-flow`.

## How to use this (different AI agent)

The SKILL.md is plain English instructions. Paste it into your agent's system prompt or custom instructions field (Cursor rules, custom GPT, etc.) and keep the `scripts/` folder alongside. Any agent that can run Python can execute the scripts directly.

---

## Node map (original Make.com → this skill)

| Make node | Module | Maps to |
|---|---|---|
| 7 | `typeform:WatchEventsWithResponses` | CSV row (trigger replaced) |
| 9 | `util:FunctionSleep` | removed (no async needed in batch) |
| 10 | `typeform:ListResponses` | CSV row fields (`topic`, `summary`, `company_name`, `recipient_name`, `recipient_email`) |
| 3 | `openai-gpt-3:CreateCompletion` | `generate_copy.py` — OpenAI chat API, gpt-4 |
| 6 | `json:ParseJSON` | `json.loads()` inside `generate_copy.py` |
| 2 | `google-slides:createPresentation` | `slides_builder.py` — Drive `files.copy` + Slides `batchUpdate` |
| 11 | `google-drive:shareAFileFolder` | `drive_share.py` — Drive permissions API |
| 8 | `email:ActionSendEmail` | `email_sender.py` — SMTP |
