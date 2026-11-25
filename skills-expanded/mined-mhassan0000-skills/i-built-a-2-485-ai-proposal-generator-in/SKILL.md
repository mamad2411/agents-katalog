# AI Proposal Generator

Converts raw sales call notes into a polished, fully-populated proposal in seconds -- either a Google Slides deck you own or a signed PandaDoc document. Fires off the email automatically when done.

Sourced from: "I Built A $2,485 AI Proposal Generator In N8N (Copy This)"

---

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) -- nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

After a sales call you fill out one row in `data/input.csv` with the prospect's company name, email, the problem they described, your proposed solution, rough scope, price, and timeline. Run the script and GPT-4o writes the entire proposal copy -- title, problem summary, three solution pillars, scope bullets, milestone timeline -- then:

- **slides mode**: copies your Google Slides master template into Drive, swaps every `{{placeholder}}` with the generated content, and emails the prospect a link.
- **pandadoc mode**: creates a PandaDoc document from your template (with a live pricing table), adds both parties as signers, and emails the link.
- **draft mode** (default, no external calls beyond OpenAI): writes all generated fields to `data/output.csv` so you can review before sending anything.

There are two OpenAI prompt schemas -- one for the Slides template (23 fields) and one for PandaDoc (15 fields). The script picks the right one automatically based on `--mode`.

---

## When to trigger this

- right after a sales call when you want to send a proposal same-day
- batch processing multiple calls at once (one row per call in the CSV)
- anytime you want draft proposal copy without sending it yet (`--mode draft`)

---

## Required env vars

Always:
```
OPENAI_API_KEY
GMAIL_SENDER_EMAIL        # e.g. nick@leftclick.ai
```

For slides mode only:
```
GOOGLE_SLIDES_TEMPLATE_ID          # Drive file ID of your master template
GOOGLE_APPLICATION_CREDENTIALS     # path to service-account JSON (needs Drive + Slides scopes)
```

For pandadoc mode only:
```
PANDADOC_API_KEY
PANDADOC_TEMPLATE_UUID              # from PandaDoc template URL
PANDADOC_SENDER_EMAIL
PANDADOC_SENDER_FIRST
PANDADOC_SENDER_LAST
PANDADOC_SENDER_COMPANY
```

---

## Input CSV columns

| Column | Required | Notes |
|---|---|---|
| First Name | yes | prospect first name |
| Last Name | yes | prospect last name |
| Company Name | yes | used in proposal title |
| Email | yes | where the proposal gets sent |
| Website | optional | context for GPT |
| Problem | yes | what they told you on the call |
| Solution | yes | what you proposed |
| Scope | yes | deliverables / what's included |
| Cost | yes | e.g. `$2,200` |
| How soon? | yes | e.g. `6 weeks` |

A fake but realistic sample is pre-loaded at `data/input.csv`.

---

## Step-by-step procedure

**Step 1 -- fill in leads**

Open `data/input.csv` and add one row per call. You can batch as many as you like; they run sequentially with a short pause between each to avoid OpenAI rate limits.

**Step 2 -- choose a mode**

- `draft` -- just generate the copy, no external services needed beyond OpenAI. Good for review before committing.
- `slides` -- needs Google service account + your Slides template ID.
- `pandadoc` -- needs PandaDoc API key + template UUID.

**Step 3 -- run the script**

```bash
# draft (default) -- review output before sending
python scripts/generate_proposals.py --mode draft

# slides -- full end-to-end with email
python scripts/generate_proposals.py --mode slides

# pandadoc -- full end-to-end with email + invoice
python scripts/generate_proposals.py --mode pandadoc

# custom paths
python scripts/generate_proposals.py --mode draft --input /path/to/leads.csv --output /path/to/results.csv
```

**Step 4 -- check output**

`data/output.csv` contains every input column plus:
- `ai_proposalTitle`, `ai_descriptionName`, `ai_oneParagraphProblemSummary`, and all other generated fields prefixed with `ai_`
- `proposal_url` (slides/pandadoc modes only)
- `status` -- one of `draft`, `slides_created`, `pandadoc_created`, `sent`

**Step 5 -- (optional) switch to Google Sheets**

Set `SKILL_STORE=sheets`, `GOOGLE_APPLICATION_CREDENTIALS`, and `SKILL_SHEET_URL` in your env. After that `read_rows()` and `write_rows()` in `io_store.py` pull from / push to your Sheet instead of CSV.

---

## Node-to-code mapping (original n8n workflow)

| n8n node | What it did | Script equivalent |
|---|---|---|
| On form submission / On form submission1 | Webhook form trigger collecting 10 fields | `read_rows()` from `data/input.csv` |
| OpenAI (slides schema, 23 fields) | GPT-4o call with few-shot example | `call_openai(row, "slides")` |
| OpenAI1 (pandadoc schema, 15 fields) | GPT-4o call with different schema | `call_openai(row, "pandadoc")` |
| Google Drive (copy) | Copied Slides master template | `slides_copy_template()` via Drive API |
| Replace Text | `batchUpdate` to swap all `{{placeholders}}` | `slides_replace_text()` via Slides API |
| HTTP Request | POST to PandaDoc `/public/v1/documents/` | `pandadoc_create_document()` |
| Gmail / Gmail1 | Sent proposal link email | `send_email_gmail()` via gmail skill |

---

## Files

```
scripts/
  io_store.py              -- CSV/Sheets switch (verbatim canonical pattern)
  generate_proposals.py    -- main entry point
data/
  input.csv                -- add your leads here
  output.csv               -- generated after a run
SKILL.md                   -- this file
TESTING.md                 -- test checklist
```
