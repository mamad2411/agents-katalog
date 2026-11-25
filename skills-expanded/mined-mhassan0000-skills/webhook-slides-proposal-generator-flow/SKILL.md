# Webhook -> Slides Proposal Generator Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

When a Monday.com item is created or updated (via webhook), this flow:

1. Fetches full item details from Monday.com (name, column values including role/title)
2. Copies a Google Slides template and does a find-and-replace on `{{companyName}}` and `{{roleName}}` placeholders
3. Sets the new deck to "anyone with link can edit" via Google Drive
4. Writes the share link back to the Monday item's `Proposal` column and flips its `Stage` status to `Discovery`

The net result: a personalized proposal deck is created and linked on the CRM record in seconds, no copy-paste.

**When to trigger this skill:** say "run proposal generator", "generate a proposal from Monday webhook", or "test the slides proposal flow".

---

## Node map (source workflow)

| # | Module | What it does |
|---|--------|--------------|
| 2 | `gateway:CustomWebHook` | Receives Monday.com webhook payload; extracts `event.pulseId` |
| 4 | `monday:GetItem` | Fetches the Monday item by pulseId; pulls `name` and `mappable_column_values.text` (role) |
| 5 | `google-slides:createPresentation` | Copies template (`/1r8OLMI3H057RmbTLCtD5zl7B0xVtW_gkcDL-tSq1cJA`), replaces `companyName` + `roleName`, saves to My Drive with title `Proposal for {name}` |
| 6 | `google-drive:shareAFileFolder` | Shares the new presentation with type=anyone, role=writer, allowFileDiscovery=false |
| 7 | `monday:ChangeMultipleColumnValues` | On board `6057998606`, sets `link` column = share URL and `status` column index = 5 (Discovery) |

---

## Environment variables

**Required for Monday.com live mode:**
```
MONDAY_API_KEY          # Monday.com API token
MONDAY_BOARD_ID         # Monday board ID (default: 6057998606)
```

**For Google Slides output (opt-in — leave unset to use local .pptx mode):**
```
GOOGLE_SERVICE_ACCOUNT  # Path to service-account JSON with Drive + Slides scopes
SLIDES_TEMPLATE_ID      # Google Slides template file ID (default: 1r8OLMI3H057RmbTLCtD5zl7B0xVtW_gkcDL-tSq1cJA)
OUTPUT_FOLDER_ID        # Google Drive folder ID for new decks (leave blank for My Drive root)
```

**Optional:**
```
LOCAL_OUTPUT_DIR        # Directory for local .pptx files (default: ./output)
```

### Default mode: local .pptx files

When `GOOGLE_SERVICE_ACCOUNT` is **not** set, proposals are written as `.pptx` files
to `./output/` using python-pptx. The `share_link` column in the output CSV will be a
`file://` URI pointing to the local file. No Google credentials needed — works offline.

### Google Slides mode (opt-in)

Set `GOOGLE_SERVICE_ACCOUNT` to a service-account JSON that has been granted:
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/presentations`

Share your Slides template and output folder with the service account's email address.
In this mode proposals are created in Google Drive and a shareable link is returned.

---

## Step-by-step procedure

### Option A: Process from a webhook payload (live/automated)

Run the webhook listener. Monday.com sends a POST when an item is triggered; the script handles one item per call.

```bash
python3 scripts/run_webhook_server.py --port 8080
```

Configure Monday.com to POST to `http://your-host:8080/webhook`.

### Option B: Process from CSV (batch / test mode)

Put rows in `data/input.csv` (columns: `pulse_id`, `company_name`, `role_name`). Then:

```bash
python3 scripts/run_batch.py --input data/input.csv --output data/output.csv
```

Each row gets a proposal deck created and the share link written to `data/output.csv`.

### Option C: Single item by ID

```bash
python3 scripts/run_single.py --pulse-id 1234567890
```

Fetches from Monday, creates deck, shares it, writes back to Monday, prints the share link.

---

## How to use this

### If you use Claude Code
1. Download and unzip the attached folder.
2. Drop it into `.claude/skills/` in your project (so you have `.claude/skills/webhook-slides-proposal-generator-flow/SKILL.md`).
3. Invoke it by describing what you need, or type `/webhook-slides-proposal-generator-flow`. Claude picks it up automatically from the description.

### If you use a different AI agent
The SKILL.md file is just structured instructions in plain English. Open it, paste the contents into your agent's system prompt or instructions field (Cursor rules, custom GPT instructions, etc.), and keep the scripts folder alongside — the instructions reference those scripts and any agent that can run code can use them.
