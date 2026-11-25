# Doubling Your Inbound Conversion Rate with Make & AI

> Converted from the "AI Email Autoresponder" Make scenario. When a prospect submits a Typeform intake form, this skill fetches their latest response, scrapes their website, and uses Claude to write a personalized "human" follow-up email — then sends both a transactional confirmation and the AI-written reply. If no website is provided, it falls back to a generic (but still warm) follow-up. Converts cold inbound leads into booked calls by responding faster and smarter than any human team.

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Takes a CSV of Typeform intake submissions (or a single row from stdin) and for each lead:

1. Fetches the prospect's website via HTTP GET, strips HTML to plain text
2. If a website was scraped successfully, calls Claude (claude-3-5-sonnet) to write a short, personalized reply referencing the company name and their unique value prop
3. Sends a transactional confirmation email ("Thanks for filling out our intake form")
4. Waits a beat, then sends the personalized "human" follow-up (or a generic fallback if no website)
5. Logs every lead with outcome (sent/fallback/error) to `data/output.csv`

The two-email approach is the key insight from the original workflow: the transactional email buys time while Claude writes something that doesn't read like a bot. That's where the conversion lift comes from.

---

## When to trigger

Use this skill when:

- You want to replay or test the AI autoresponder against a batch of past Typeform submissions
- You're setting up the sequence for a new intake form and want to validate the email copy before going live
- You need to manually process leads that slipped through (webhook missed, Make was down, etc.)
- You're adapting the workflow to a different form tool or business

Trigger phrases: "run the email autoresponder", "process intake form leads", "send personalized follow-ups", "doubling inbound conversion", "AI email autoresponder".

---

## Node map (original Make scenario → this skill)

| Original node | Type | Maps to |
|---|---|---|
| Typeform: WatchEventsWithResponses (id 4) | Webhook trigger | `data/input.csv` rows (one row per submission) |
| Sleep 2s (id 6) | Delay | Skipped in batch mode; `--delay` flag optional |
| Typeform: ListResponses (id 5) | API fetch | `fetch_typeform_response()` in autoresponder.py (or row already in CSV) |
| HTTP: ActionSendData — Scrape Website (id 2) | HTTP GET | `scrape_website()` in autoresponder.py |
| HTMLToText (id 3) | HTML strip | `html_to_text()` in autoresponder.py |
| BasicRouter (id 11) | Branch | `if scraped_text:` branch in autoresponder.py |
| Anthropic: createAMessage (id 1) | Claude API | `generate_personalized_email()` — ANTHROPIC_API_KEY |
| Sleep 5s (id 8) | Delay | `time.sleep(5)` between emails |
| Email: ActionSendEmail transactional (id 7, 12) | SMTP | `send_email()` — SMTP_HOST / SMTP_USER / SMTP_PASS |
| Sleep 10s (id 9, 13) | Delay | `time.sleep(10)` between emails |
| Email: ActionSendEmail "human" (id 10, 14) | SMTP | `send_email()` — same SMTP credentials |
| builtin:Ignore on HTTP error (id 15) | Error handler | `try/except` around `scrape_website()`, logs and continues |

---

## Required env vars

```
ANTHROPIC_API_KEY=sk-ant-...   # Required — Claude email generation
SMTP_HOST=smtp.gmail.com       # Required — outbound email
SMTP_PORT=587                  # Default 587
SMTP_USER=you@yourdomain.com   # Required
SMTP_PASS=yourpassword         # Required
FROM_NAME=Nick                 # Display name on outbound emails
SENDER_SIGNATURE=Nick          # Signature line (default: Nick)
```

Set in your shell or a `.env` file. Never hardcode.

---

## Step-by-step procedure

### Batch mode (process a CSV of leads)

1. Make sure all env vars above are set.
2. Put your leads in `data/input.csv`. Columns: `first_name`, `email`, `phone`, `website_url`. See `data/input.csv` for a realistic sample.
3. Run:
   ```bash
   python3 scripts/autoresponder.py --input data/input.csv --output data/output.csv
   ```
4. Check `data/output.csv` — each row will have a `status` column: `sent_personalized`, `sent_generic`, or `error`.

### Single lead (test one row)

```bash
python3 scripts/autoresponder.py \
  --first-name "Sarah" \
  --email "sarah@example.com" \
  --phone "+1 403 555 0100" \
  --website "https://example.com"
```

### Dry run (generate emails, don't send)

```bash
python3 scripts/autoresponder.py --input data/input.csv --dry-run
```

Prints the generated emails to stdout without sending. Good for reviewing copy before a real batch.

### Skip delays

By default the script mimics the original Make timing (5s between transactional + human email). To skip:

```bash
python3 scripts/autoresponder.py --input data/input.csv --no-delay
```

---

## Email templates

### Transactional (sent first, both branches)

```
Subject: Thanks for filling out our intake form, {first_name}

Hi {first_name},

Thanks for filling out our intake form. We're looking forward to learning more about
you & your business — one of our team members will get back to you shortly, so watch
your email!

WorkflowLoop
```

### "Human" email — with website (Claude-generated)

Claude fills in the template below using scraped website content:

```
Hi {first_name},

Thanks for reaching out. {company_name} looks great — love your {unique_value_prop}.

I'm out of the office right now, but do you want to chat later today when I'm back?
Happy to give you a ring. Just send over a couple of times (tomorrow works too).

Thanks,
{SENDER_SIGNATURE}
```

### "Human" email — no website (generic fallback)

```
Hi {first_name},

Thanks for reaching out. Just out of the office right now, but do you want to chat
later today when I'm back? Happy to give you a ring.

If so, send me over a couple of times and I'll call you at {phone} (tomorrow works too).

Thanks,
{SENDER_SIGNATURE}
```

---

## Data columns

`data/input.csv`:

| Column | Description |
|---|---|
| `first_name` | Prospect first name (Typeform field `1b79c5b1`) |
| `email` | Prospect email (Typeform field `d228ea13`) |
| `phone` | Prospect phone number (Typeform field `ffd98604`) |
| `website_url` | Prospect website URL (Typeform field `f7b2b4e6`) |

`data/output.csv` (appended after run):

| Column | Description |
|---|---|
| `first_name` | Same as input |
| `email` | Same as input |
| `website_url` | Same as input |
| `scraped` | `true` / `false` — whether website was fetched |
| `generated_email` | Claude's output (or empty on fallback) |
| `status` | `sent_personalized` / `sent_generic` / `error` |
| `error` | Error message if status is `error` |
