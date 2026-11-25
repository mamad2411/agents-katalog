# 7 Make.com Automations That Make Me +$200,000/Yr (Steal Them)

Converted from the Make.com blueprints shared in the course video. Eight automation systems (the course bundles a few as one "system") covering content ideation, client proposals, hiring, payroll, currency conversion, waitlist billing, and project management. Every data node that was Google Sheets or Airtable in the original now reads/writes local CSV by default.

---

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What's in here

Ten Make.com blueprints, eight distinct automation systems:

| # | System | Source workflow | APIs |
|---|--------|-----------------|------|
| 1 | Referral autoresponder | Clever Referral Autoresponder | Typeform, SMTP |
| 2 | Discovery call -> AI proposal | Dashboard Tracking: Discovery Call Form -> Send Email | Typeform, OpenAI, PandaDoc, SMTP |
| 3 | YouTube content idea generator | YouTube Content Idea Generator | Apify, OpenAI, Google Sheets (-> CSV) |
| 4 | Hiring pipeline (3 parts) | 1/2/3. Application -> ClickUp -> Trial | Typeform, ClickUp, SMTP |
| 5 | Autonomous waitlist billing | Autonomous Waitlist Management | HTTP, Google Sheets (-> CSV), Stripe |
| 6 | Currency convert + Wise payment | Convert Currency & Queue Up Wise Payment | PandaDoc, Airtable (-> CSV), Wise, ExchangeRate |
| 7 | Contractor payroll | "Payroll" System for Hourly Contractors | Harvest, PandaDoc |
| 8 | ClickUp project manager | ClickUp Project Manager | ClickUp, Google Drive, Google Docs, Harvest |

---

## When to trigger this skill

- Someone asks to run or adapt any of the automations from the "7 Make.com Automations" course
- Setting up contractor payroll, client proposal generation, hiring pipelines, or waitlist billing
- Converting any of the individual Make.com blueprints to work locally without Make
- Debugging or extending any of the eight systems

---

## Node map (every node in every workflow)

### 1. Referral Autoresponder (`referral_autoresponder.py`)
```
typeform:WatchEventsWithResponses
  -> util:FunctionSleep (rate limit buffer)
  -> typeform:ListResponses (pull full response)
  -> util:SetVariables (format datetime)
  -> email:ActionSendEmail (smart referral email with calendar link)
```
Local replacement: typeform trigger -> rows from `data/input.csv`. Email send via SMTP.

### 2. Discovery Call -> AI Proposal (`discovery_call_proposal.py`)
```
typeform:WatchEventsWithResponses
  -> util:FunctionSleep
  -> typeform:ListResponses
  -> openai-gpt-3:CreateCompletion (Generate Proposal JSON)
  -> json:ParseJSON
  -> openai-gpt-3:CreateCompletion (Generate Milestones/Timelines JSON)
  -> json:ParseJSON
  -> pandadoc:createADocuments (Send Proposal)
  -> email:ActionSendEmail
```
Local replacement: form responses from CSV -> OpenAI (real API) -> PandaDoc (real API) -> SMTP.

### 3. YouTube Content Idea Generator (`youtube_content_ideas.py`)
```
apify:finishedActorRuns (trigger on actor completion)
  -> apify:fetchDatasetItems (get scraped data)
  -> openai-gpt-3:CreateCompletion (Filter & Create Content Idea — JSON)
  -> builtin:BasicFeeder (iterate ideas)
  -> util:SetVariables
  -> openai-gpt-3:CreateCompletion (Create Hook & Outline — JSON)
  -> google-sheets:addRow  [-> write_rows() to CSV]
```
Local replacement: scraped items from CSV (or live Apify run ID) -> OpenAI -> `data/output.csv`.

### 4. Hiring Pipeline Parts 1/2/3 (`hiring_pipeline.py --step 1|2|3`)
```
Part 1: typeform:WatchEventsWithResponses -> util:FunctionSleep
  -> typeform:ListResponses -> util:Switcher (Select Role)
  -> clickup:createTaskInList

Part 2: gateway:CustomWebHook (ClickUp status change)
  -> clickup:getATask -> email:ActionSendEmail -> clickup:editATask

Part 3: typeform:WatchEventsWithResponses -> util:FunctionSleep
  -> typeform:ListResponses -> clickup:editATask -> email:ActionSendEmail
```
Local replacement: CSV rows -> ClickUp (real API) -> SMTP.

### 5. Autonomous Waitlist Management (`waitlist_management.py`)
```
http:ActionSendData (fetch waitlist endpoint)
  -> regexp:Parser (extract emails/data)
  -> google-sheets:filterRows (check already billed)  [-> read_rows() from CSV]
  -> stripe:retrieveCustomer
  -> stripe:createInvoiceItem -> util:FunctionSleep
  -> stripe:createInvoice -> util:FunctionSleep
  -> stripe:finalizeInvoice -> util:FunctionSleep
  -> stripe:confirmPaymentIntent
  -> builtin:BasicRouter (success/fail branch)
```
Local replacement: waitlist entries from CSV (with stripe_customer_id) -> Stripe (real API).

### 6. Currency Convert + Wise Payment (`convert_currency_wise.py`)
```
util:SetVariable2 (PandaDoc trigger placeholder)
  -> pandadoc:getADocument (Get Invoice Details)
  -> airtable:ActionSearchRecords (Find Team Member)  [-> read_rows() from CSV]
  -> util:Switcher (Switch payIn Balance)
  -> app#wise:listBalanceAccounts
  -> currency:ActionConvert (Convert Currency)
  -> app#wise:createQuote
  -> app#wise:createTransfer
```
Local replacement: team member + invoice records from CSV -> ExchangeRate API -> Wise (real API).

### 7. Contractor Payroll (`payroll_system.py`)
```
harvest:getUsers (List Active Users)
  -> util:Switcher (Set Pay-Period Dates)
  -> harvest:getAUser (Get User Record)
  -> harvest:getTimeEntries (List Pay-Period Time Entries)
  -> util:FunctionAggregator2 (Sum Hours)
  -> pandadoc:createADocuments (Generate Contractor Invoice)
```
Local replacement: contractor list from Harvest (real API) or from CSV override -> PandaDoc (real API).

### 8. ClickUp Project Manager (`clickup_project_manager.py`)
```
util:SetVariable2 ("New Task" Webhook)
  -> clickup:getATask -> clickup:editATask (status: Creating Project Folder)
  -> clickup:postATaskComment (log execution)
  -> google-drive:searchForFilesFolders (Search Projects Folder)
  -> google-drive:createAFolder (Create Project Folder)
  -> clickup:editATask (status: Creating Google Doc)
  -> google-drive:searchForFilesFolders (Search for Template)
  -> google-docs:createADocumentFromTemplate (Create Content Brief)
  -> google-drive:shareAFileFolder
  -> clickup:editATask (Add Project Folder Link)
  -> util:FunctionSleep (10s delay)
  -> harvest:createAProject
  -> clickup:editATask (Add Harvest Project ID)
  -> builtin:BasicRouter
```
Local replacement: task IDs from CSV -> ClickUp + Google Drive + Harvest (all real APIs).

---

## Step-by-step procedure

### Setup (do once)

1. Copy the skill folder into your project's `.claude/skills/` so the path is `.claude/skills/7-make-com-automations-that-make-me-200-/`.
2. Edit `data/input.csv` — the sample rows show the column shape each script expects. You can delete the sample rows and add your own, or point scripts at a different CSV with `--input`.
3. Set env vars for whichever automations you're running (see env var tables per script below). You don't need all of them — only the ones for the automations you use.

### Running a specific automation

Pick the script for the system you want. Every script supports `--dry-run` to skip live API calls and just log what would happen.

**Referral autoresponder:**
```bash
python scripts/referral_autoresponder.py --input data/input.csv --output data/output.csv --dry-run
# Remove --dry-run when env vars are set: SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS REFERRAL_FROM_EMAIL REFERRAL_CALENDAR_URL
```

**Discovery call -> AI proposal:**
```bash
python scripts/discovery_call_proposal.py --input data/input.csv --output data/output.csv --dry-run
# Env vars: OPENAI_API_KEY PANDADOC_API_KEY PANDADOC_TEMPLATE_ID SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS PROPOSAL_FROM_EMAIL
```

**YouTube content idea generator:**
```bash
# From local CSV (scraped items already in data/input.csv):
python scripts/youtube_content_ideas.py --input data/input.csv --output data/output.csv
# From live Apify run:
python scripts/youtube_content_ideas.py --apify-run-id YOUR_RUN_ID --output data/output.csv
# Env vars: OPENAI_API_KEY APIFY_API_TOKEN (only for live Apify)
```

**Hiring pipeline:**
```bash
python scripts/hiring_pipeline.py --step 1 --input data/input.csv --output data/output.csv --dry-run
python scripts/hiring_pipeline.py --step 2 --input data/output.csv --output data/output_step2.csv --dry-run
python scripts/hiring_pipeline.py --step 3 --input data/output_step2.csv --output data/output_step3.csv --dry-run
# Env vars: CLICKUP_API_KEY CLICKUP_LIST_ID SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS TRIAL_EMAIL_FROM TRIAL_FORM_URL
```

**Waitlist management:**
```bash
python scripts/waitlist_management.py --input data/input.csv --output data/output.csv --processed data/processed.csv --dry-run
# Env vars: STRIPE_SECRET_KEY PRODUCT_DESCRIPTION PRODUCT_AMOUNT_CENTS PRODUCT_CURRENCY
```

**Currency convert + Wise payment:**
```bash
python scripts/convert_currency_wise.py --input data/input.csv --output data/output.csv --dry-run
# Env vars: WISE_API_TOKEN WISE_PROFILE_ID EXCHANGERATE_API_KEY (optional)
```

**Contractor payroll:**
```bash
python scripts/payroll_system.py --output data/output.csv --pay-period biweekly --dry-run
# Or override with CSV (skips Harvest): --input data/input.csv
# Env vars: HARVEST_ACCOUNT_ID HARVEST_ACCESS_TOKEN PANDADOC_API_KEY PANDADOC_TEMPLATE_ID PANDADOC_FOLDER_UUID
```

**ClickUp project manager:**
```bash
python scripts/clickup_project_manager.py --input data/input.csv --output data/output.csv --dry-run
# Env vars: CLICKUP_API_KEY GOOGLE_SA_JSON_PATH GDRIVE_PROJECTS_FOLDER_ID GDRIVE_TEMPLATE_ID HARVEST_ACCOUNT_ID HARVEST_ACCESS_TOKEN HARVEST_CLIENT_ID
```

### If you want Google Sheets instead of local CSV

Set these env vars:
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_ID/edit
```
Share your Sheet with the service account email. Everything else is identical.

---

## Files

```
scripts/
  io_store.py                    CSV/Sheets switch (imported by every script)
  referral_autoresponder.py      Automation 1
  discovery_call_proposal.py     Automation 2
  youtube_content_ideas.py       Automation 3
  hiring_pipeline.py             Automations 4a/4b/4c (--step 1|2|3)
  waitlist_management.py         Automation 5
  convert_currency_wise.py       Automation 6
  payroll_system.py              Automation 7
  clickup_project_manager.py     Automation 8
data/
  input.csv                      Sample rows (fake data) showing expected columns
TESTING.md                       Test checklist skeleton
```
