# Slack Approval System Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Two-flow system for human-in-the-loop lead qualification via Slack. When a new lead lands in ClickUp, the first flow pulls its details and posts an interactive Slack message with Approve and Deny buttons. A reviewer clicks a button, the second flow catches that button click, updates the ClickUp task status to "qualified" or "unqualified", and posts a confirmation back to Slack. No more manually jumping between your CRM and Slack to move leads through your pipeline.

**APIs used:** Slack (Block Kit + Interactivity), ClickUp (Tasks API), inbound webhooks.

---

## When to trigger this

- you want human approval gating before a lead moves to the next CRM stage
- your team reviews leads in Slack and needs a one-click way to qualify or disqualify
- you're replacing a manual "check ClickUp, post in Slack, go back to update ClickUp" loop
- trigger phrase: "slack approval flow", "send leads to slack for approval", "approve leads in slack"

---

## Source workflow node map

### Flow 1 — New Lead -> Slack Notification

| # | Module | What it does |
|---|--------|-------------|
| 1 | `gateway:CustomWebHook` | Inbound webhook trigger; receives `payload.id` (ClickUp task ID) |
| 2 | `clickup:getATask` | Fetches task by ID; pulls name, Email, Phone, Form Answer custom fields |
| 3 | `slack:CreateMessage` | Posts Block Kit message to approval channel with Approve (value: `qualified`) and Deny (value: `unqualified`) buttons |

### Flow 2 — Button Click -> CRM Update

| # | Module | What it does |
|---|--------|-------------|
| 1 | `gateway:CustomWebHook` | Receives Slack interactive-component payload when reviewer clicks a button |
| 2 | `gateway:WebhookRespond` | Responds 200 with `{"challenge": ...}` immediately (required by Slack within 3s) |
| 3 | `slack:CreateMessage` | Posts confirmation message back to the channel |
| *(implied)* | ClickUp update | Updates the ClickUp task status to `qualified` or `unqualified` based on button value |

---

## Environment variables

```bash
# Required for Flow 1 (notify)
SLACK_BOT_TOKEN=xoxb-...          # chat:write scope
SLACK_CHANNEL_ID=C072D9YDQNT      # approval channel
CLICKUP_API_KEY=pk_...            # ClickUp personal token

# Required for Flow 2 (handle approval)
SLACK_SIGNING_SECRET=...          # from Slack app -> Basic Info
CLICKUP_STATUS_APPROVE=qualified  # ClickUp status name for approved leads
CLICKUP_STATUS_DENY=unqualified   # ClickUp status name for denied leads

# Optional
CLICKUP_BASE_URL=https://api.clickup.com/api/v2
```

---

## Step-by-step procedure

### One-time setup

1. **Create a Slack app** at api.slack.com/apps. Add `chat:write` bot scope. Install to workspace.
2. **Enable Interactivity** in the Slack app settings. Set Request URL to your `handle_approval.py` server endpoint (see below).
3. Copy your bot token (`SLACK_BOT_TOKEN`) and signing secret (`SLACK_SIGNING_SECRET`) into your `.env`.
4. Get your ClickUp personal API token from ClickUp -> Profile -> API Token. Set `CLICKUP_API_KEY`.
5. Confirm the ClickUp status names for qualified/unqualified leads in your list. Set `CLICKUP_STATUS_APPROVE` and `CLICKUP_STATUS_DENY`.
6. Set `SLACK_CHANNEL_ID` to the channel where approval messages should land.

### Running Flow 1 (notify Slack of new leads)

Drop ClickUp task IDs into `data/input.csv`:

```
task_id,lead_name,notes
abc123xyz,Acme Corp - John Smith,High priority
```

Then run:

```bash
pip install requests
python3 scripts/notify_slack.py --input data/input.csv --output data/output.csv
```

Each row fetches the ClickUp task, builds a Block Kit message, and posts it to Slack. Results (including `slack_ts` for threading) written to `data/output.csv`.

### Running Flow 2 (handle button clicks)

Start the approval handler server:

```bash
pip install flask requests
python3 scripts/handle_approval.py --port 5000
```

Expose it publicly (e.g. `ngrok http 5000`) and set that URL as your Slack app's Interactivity Request URL. When a reviewer clicks Approve or Deny, the server:

1. Verifies the Slack signature
2. Parses the task ID from the button's `action_id`
3. Updates ClickUp task status
4. Posts a confirmation message back to the channel

### Using Google Sheets instead of CSV

Set these env vars and the same scripts work against your Sheet:

```bash
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```

---

## File layout

```
slack-approval-system-flow/
  SKILL.md                    ← this file
  TESTING.md                  ← test plan
  data/
    input.csv                 ← task IDs to notify Slack about
    output.csv                ← written after notify_slack.py runs
  scripts/
    io_store.py               ← CSV/Sheets abstraction (standard pattern)
    notify_slack.py           ← Flow 1: fetch ClickUp task, post to Slack
    handle_approval.py        ← Flow 2: Flask server handling button clicks
```
