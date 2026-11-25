# How to Automate Slack with Make.com

Converted from the Make.com workflow: "Example Lead Capture: New Reply in Instantly -> Categorize with GPT-4 -> Add ClickUp Task"

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

This skill replicates the workflow from Nick's "How to Automate Slack with Make.com" video. The original Make.com scenario watches for new inbound email replies (via an Instantly webhook), passes the reply text through GPT-4 to classify it as Positive, Not Interested, or Unsubscribe, extracts the domain from the lead's email address, and then fires a formatted Slack Block Kit message to a private sales channel if the reply is Positive.

You give it a CSV of email replies (or let it run against a live webhook). It categorizes each reply with OpenAI, filters to Positive ones, and posts a rich Slack notification with the lead's name, reply snippet, and a link to the Instantly inbox.

---

## When to trigger this

- You want to automate lead reply triage from any cold outreach tool and post warm leads to Slack in real time.
- You're building a "new warm lead" alert for a sales team.
- You want to learn how webhook trigger -> GPT classify -> Slack notify flows actually work in practice.

---

## Node map (source workflow)

| # | Module | What it does |
|---|--------|--------------|
| 1 | `gateway:CustomWebHook` | Trigger — receives Instantly reply payload via webhook (`lead_email`, `firstName`, `lastName`, `reply_text`, `reply_text_snippet`) |
| 2 | `openai-gpt-3:CreateCompletion` | GPT-4 chat completion — few-shot classifies `reply_text` into `Positive`, `Not Interested`, or `Unsubscribe` as JSON |
| 3 | `json:ParseJSON` | Parses the GPT JSON string into a `category` field |
| 4 | `slack:CreateMessage` | Posts a Block Kit message to a private Slack channel (`#sales`) — only fires when `category == "Positive"` |
| 5 | `regexp:AdvancedParser` | Regex `@(.*)` on `lead_email` to extract the domain/website |

---

## Prerequisites

Set these env vars before running:

```
OPENAI_API_KEY=sk-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C05680ESF2L   # or your own private channel ID
```

Optional (webhook mode only):
```
WEBHOOK_PORT=8000   # port to listen on for incoming Instantly payloads
```

---

## Step-by-step procedure

### Option A: Batch mode (CSV input, recommended for testing)

1. Fill in `data/input.csv` with your email reply rows (see the fake sample already there).
2. Run:
   ```
   python3 scripts/run_batch.py
   ```
3. The script reads each row, calls OpenAI to classify the reply, extracts the domain, and posts a Slack message for every Positive reply.
4. Results (category + domain) are written to `data/output.csv`.

### Option B: Webhook listener mode (mirrors the Make.com trigger exactly)

1. Run:
   ```
   python3 scripts/run_webhook.py
   ```
2. The server starts on `WEBHOOK_PORT` (default 8000) and accepts POST payloads from Instantly (or any tool) at `/webhook`.
3. Each incoming payload goes through the same classify -> filter -> Slack notify pipeline as the batch mode.

---

## Scripts

| File | Purpose |
|------|---------|
| `scripts/io_store.py` | CSV/Sheets switch (verbatim from CSV-DEFAULT-PATTERN.md) |
| `scripts/classify.py` | GPT-4 classify function with few-shot prompt |
| `scripts/slack_notify.py` | Posts the Block Kit message to Slack |
| `scripts/run_batch.py` | Entry point for CSV batch mode |
| `scripts/run_webhook.py` | Entry point for live webhook listener mode |
