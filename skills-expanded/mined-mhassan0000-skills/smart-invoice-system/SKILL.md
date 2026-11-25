# Smart Invoice System

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Reads your unpaid invoice list, finds every row hitting a follow-up milestone (7, 14, 21, or 28 days since sent), fetches the actual email thread with that client, and asks GPT-4.1 whether a follow-up makes sense given the conversation history. If the last 72 hours already have invoice chatter, it skips. If the templated follow-up would feel out of context, it rewrites it. Only then does it create a Gmail draft — nothing goes out without your eyes on it.

This is the AI-augmented version of a basic invoice chaser. The difference is it reads context before acting, so you don't send a "just following up!" email to someone who already replied two days ago.

---

## When to trigger

- Run `followup.py` daily (cron or manually). It processes every invoice that hits a milestone day and creates drafts for any that pass the AI check.
- Or just say "run smart invoice followups" and I'll execute it for you.

---

## Node map (original n8n workflow)

| n8n node | Maps to |
|----------|---------|
| Google Sheets (read Sheet1) | `read_rows("data/input.csv")` |
| Edit Fields (daysSinceSent, email, firstName) | `compute_fields()` in `followup.py` |
| Filter (days == 7/14/21/28) | milestone filter in `followup.py` |
| Loop Over Items | per-invoice loop in `followup.py` |
| Gmail (getAll, from/to client) | `fetch_thread()` using Gmail API via `GMAIL_CREDENTIALS_JSON` |
| Aggregate (text + headers.date) | `aggregate_thread()` in `followup.py` |
| Edit Fields1 (textWithDate, followUpTemplateArray) | `build_context()` in `followup.py` |
| OpenAI gpt-4.1 (verdict + emailTemplate) | `check_with_ai()` in `followup.py` via `OPENAI_API_KEY` |
| Filter1 (verdict == "true") | verdict check in `followup.py` |
| Gmail1 (create draft) | `create_draft()` using Gmail API |

---

## Sheet / CSV columns (in order)

| Index | Column | Description |
|-------|--------|-------------|
| 0 | `Client Name` | Full name — first name extracted for email salutation |
| 1 | `Email` | Client email address |
| 2 | `Date Sent` | Date invoice was sent (YYYY-MM-DD) |
| 3 | `Invoice ID` | Your invoice reference |
| 4 | `Amount` | Invoice amount (e.g. 2500.00) |
| 5 | `Status` | `Unpaid`, `Paid`, `Overdue`, etc. |

---

## Step-by-step procedure

1. Make sure `data/input.csv` has your unpaid invoices using the columns above.
2. Set env vars (see table below). At minimum you need `OPENAI_API_KEY` and `GMAIL_CREDENTIALS_JSON`.
3. Run:
   ```bash
   python3 scripts/followup.py --input data/input.csv
   ```
4. The script prints a summary of which invoices were checked, which passed the AI verdict, and which draft subjects were created.
5. Review drafts in Gmail and send the ones that look good.

### Dry-run mode (no Gmail, no OpenAI calls)

```bash
python3 scripts/followup.py --input data/input.csv --dry-run
```

Prints which invoices would be processed and what templates would be selected, without calling any external API.

---

## Environment variables

| Variable | Required | Notes |
|----------|----------|-------|
| `OPENAI_API_KEY` | Yes | Used to call gpt-4.1 for context-aware verdict |
| `GMAIL_CREDENTIALS_JSON` | Yes | Path to a Gmail OAuth2 credentials JSON (downloaded from Google Cloud Console) |
| `GMAIL_TOKEN_JSON` | Yes | Path where the OAuth token is stored after first auth (auto-created on first run) |
| `SKILL_STORE` | Optional | Set to `sheets` to switch from CSV to Google Sheets |
| `GOOGLE_APPLICATION_CREDENTIALS` | Sheets mode only | Path to service account JSON |
| `SKILL_SHEET_URL` | Sheets mode only | Google Sheet URL |

---

## Follow-up templates (verbatim from source workflow)

The skill ships four escalating templates, used at days 7, 14, 21, and 28:

- **Day 7:** Light check-in. "Hope you're well. Just checking in on that invoice."
- **Day 14:** Offer to help. "Am here to help if anything is unclear."
- **Day 21:** Short nudge. "Thought I'd send another ping."
- **Day 28:** Final tone, not pushy. "Not my intention to bother — just want to close this out."

GPT-4.1 may rewrite any of these if the conversation history makes the default feel off.
