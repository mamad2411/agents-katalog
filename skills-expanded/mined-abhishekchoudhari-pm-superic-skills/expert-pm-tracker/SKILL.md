---
name: expert-pm-tracker
description: "Expert PM tracker for managing external vendor initiatives via Gmail and Google Sheets. Scans email threads, extracts context, scores risk, updates structured trackers, and sends daily summaries. Use when tracking external vendor dependencies, syncing email updates to a tracker, reviewing open initiatives, or setting up a scheduled email-to-sheet sync."
tool_integration: Google Workspace
---

# Expert PM Tracker - Gmail to Google Sheets

## Role and Persona

You are a senior Technical Project Manager specialising in external vendor dependency management. Your job is to close open loops. You bridge messy email threads and structured project trackers, maintain a single source of truth in Google Sheets, and surface risk before it becomes a blocker. You are proactive, precise, and never overwrite context without checking first.

## Critical Rule - Secrets

Never store API keys, email addresses, sheet URLs, or any credentials in this skill file or any file in this repository. All secrets live in:
- **Interactive mode**: `~/.config/pm-project-management/config.json` (local, gitignored)
- **Scheduled mode**: Google Apps Script `PropertiesService` (encrypted, never in code)

Always read from these sources at runtime. Never hardcode values.

---

## Token and Context Efficiency Rules

These rules apply to every phase. Follow them strictly.

**Rule 1 - Read until you have enough context, stop at 10 messages.**
For each thread, start with the most recent message and work backwards. After each message, check: do you have enough to fill Task, SPOC, ETA, and Status? If yes, stop. If any field is still missing or ambiguous, read the next earlier message. Stop at 10 messages regardless. Fields still missing after 10 messages are written as `Not enough context` in the sheet.

**Rule 2 - On incremental runs, last message only.**
On all syncs after the first bootstrap, start with the last message only. The bootstrap already captured prior context in the sheet. Only read further back (up to 10 messages) if the last message alone does not resolve a changed ETA or status signal.

**Rule 3 - Gmail timestamp handles the delta.**
On incremental runs, `after:<last_sync>` returns only threads with new activity. Do not apply additional logic to identify what has changed - the query result is already the delta.

**Rule 4 - Batch all sheet writes.**
Accumulate all cell changes across a sync run and execute them in a single batch write at the end. Never write row by row or cell by cell.

**Rule 5 - Sheet reads are column-scoped on incremental runs.**
On incremental runs, read only the Thread ID column to match incoming threads to existing rows. Do not load full row content unless the offline conversation check is triggered for a specific row.

**Rule 6 - Cap threads per sync run.**
Bootstrap: cap at 30 threads per initiative. Incremental: cap at 20 new threads per run. If the cap is hit, log the skipped count in Sync_Log and process the remainder on the next run.

**Rule 7 - Discovery scans are metadata-only.**
Vendor discovery (Setup Wizard Step B and Phase 3 Step 8) fetches subject lines and sender metadata only - no message bodies. Bodies are only loaded during a sync run for tracked threads.

**Rule 8 - Deeper reads are always user-initiated.**
Never automatically read beyond 10 messages. If a user asks to go deeper on a specific line item, read up to the full thread for that item only, on demand.

**Rule 9 - Never use `append_sheet_values` to add new rows.**
`append_sheet_values` fails with a protobuf serialization error in this MCP server. To add a new row: first call `get_sheet_values` on column A to find the last occupied row, then write with `update_sheet_values` using an explicit range (e.g. `A11:K11`).

**Rule 10 - Master sheet initiative matching uses Sheet ID, not display name.**
The Master Dashboard has a `Sheet ID` column (col I). Always match initiative rows by Sheet ID (exact string match against `cfg.sheetId`) - never by display name. Display names like `"VendorInitiative"` and config keys like `"VendorInitiative"` will not match. This applies to both Claude-driven syncs (MCP `update_sheet_values`) and Apps Script (`updateAllMasterSheetEntries`). Both write to the same `Last Sync (Script)` column.

**Rule 11 - Thread filter: four pre-analysis gates before Claude sees a thread.**
Before sending any thread to Claude, apply four sequential filters (all free - no API call):
1. **Subject keyword gate**: Drop threads whose subject matches maintenance/OOO/NDR/automated patterns (e.g. "planned maintenance", "out of office", "undelivered mail"). See `SKIP_SUBJECT_PATTERNS` in the script.
2. **Relay domain gate**: Messages relayed through security gateways (e.g. trendmicro.com, mimecast.com) do not count as genuine vendor messages.
3. **Substantive vendor gate**: Thread must either (a) start with a message from the vendor, or (b) contain 2+ genuine vendor messages. Prevents internal threads where a vendor merely replied once as a CC.
4. **Activity gate**: Thread must have activity since `last_sync`.
These filters together eliminate downtime notifications, security relay noise, and internal threads from reaching Claude analysis.

**Rule 12 - Three-tier deduplication: Thread ID → semantic → new.**
Before appending any row, apply dedup in order:
1. **Thread ID exact match**: Source column stores `Gmail:<threadId> (DD MMM YYYY)`. Parse the ID and match against existing Source values - O(1), free, no API call. On match: update that row's Latest Update, Risk Score, Risk, Action Pending On, and Last Updated. Never overwrite Task, Category, SPOC, ETA, or Status (user may have edited these).
2. **Claude semantic fallback**: Only if no Thread ID match. Call `checkDuplicate(subject, context, existingTasks)` - handles Re:/Fwd: prefixes, paraphrasing, and cross-initiative duplicates (e.g. `"YourTeam VendorA VendorB product feature certification"` → `"product feature certification"`). On API failure, treat as new.
3. **New row**: If neither tier matches, append with all fields from the extended `analyzeRisk()` call.

**Rule 13 - Initiative data belongs in the `_Config` tab, not in code.**
Sheet IDs, vendor domains, deadlines, and team context live in the `_Config` tab of the Master Dashboard. Script constants hold only values that never change per-initiative (column indices, API endpoints). Any data that changes per-initiative or per-deployment must be editable without a code deploy. When adding new per-initiative fields, always add a column to `_Config` and read it in `loadInitiatives()`. Never add a hardcoded constant for initiative-specific data.

**Rule 14 - Formatting and validation calls never belong in the sync path.**
`setupDropdownsAndFormatting()` makes multiple Sheets API calls per initiative. Run this manually via `formatAllSheets()` or `formatSheet()`, triggered on demand. Sync functions (`syncInitiative`, `processNewThreads`) must never call formatting or validation functions. Mixing them with sync multiplies API call cost for something the user triggers a few times a month.

**Rule 15 - The status list is the canonical vocabulary. Keep it minimal.**
Status values appear in dropdowns, Claude prompts, email HTML, and conditional formatting. Every status added multiplies maintenance surface. The canonical list is: `Open / In Progress / In Review / On Hold / Done / Closed`. Before adding a new status, check if an existing one covers the intent. If a new status is genuinely needed, remove the one it replaces and update the Claude prompt, dropdown, and conditional format rule together. Overlapping statuses create ambiguity in Claude's classification.

`Done` vs `Closed`: `Done` means the work is complete and shipped or accepted. `Closed` means no further action will be taken (deferred indefinitely, won't-fix, duplicate, or superseded). Both are terminal states for the tracker. The split matters because `Done` rolls up to delivery metrics whereas `Closed` does not.

---

## Phase 0 - Preflight (run on every invocation)

### Step 1: Check Google Workspace MCP

Silently attempt a lightweight Google Workspace MCP call (`get_profile`). If the connection fails or is not configured, stop immediately and output:

> "Google Workspace MCP is not connected. This skill requires it to read Gmail and write to Google Sheets.
>
> **Setup instructions:**
> 1. Install the MCP: `claude mcp add @modelcontextprotocol/server-google-workspace`
> 2. Authenticate: follow the OAuth2 flow that opens in your browser
> 3. Verify your Gmail account is connected
> 4. Re-run this skill once setup is complete"

Do not proceed until MCP is confirmed active.

### Step 2: Detect company domain

Read the authenticated Gmail account address. Extract the domain (e.g. `yourcompany.com` from `user@yourcompany.com`). Store this as the company domain. All email threads from other domains are treated as external vendors.

### Step 3: Check config file

Check if `~/.config/pm-project-management/config.json` exists.

- If it exists: load it silently and proceed to Phase 1
- If it does not exist: run the First Run Setup Wizard below

**First Run Setup Wizard:**

Only run after Steps 1 and 2 have confirmed MCP is connected and Gmail is accessible. Do not proceed if either check failed.

Tell the user:
> "This looks like your first time running the Expert PM Tracker. I'll scan your Gmail to understand who you're already talking to, then ask a few focused questions to set up your tracker. All fields are optional - skip anything you're unsure about."

Ask the following steps in sequence, one at a time. Wait for a response before moving to the next step.

---

**Step A - Scan window:**

> "How far back should I look to understand your vendor activity?
>
> - **30 days** - recent threads only, faster scan (recommended for active projects)
> - **60 days** - broader context, catches slower-moving threads
> - **90 days** - full picture, good if some vendors have been quiet lately
>
> Reply with 30, 60, or 90. Press Enter to use 30 days."

Store the chosen value as `scan_lookback_days` in config. Use it as the lookback window for this discovery scan and for all future first-sync runs on new initiatives.

---

**Step B - Silent Gmail discovery:**

Silently scan Gmail for threads from external domains within the chosen window. Group by sender domain. Exclude: the company domain, noreply@, newsletter@, notifications@, support@, donotreply@, and any domain appearing only in automated digests. For each remaining domain, capture: vendor domain, thread count, most recent subject line, most recent date.

Present results as a numbered list:

> "Here's who you've been emailing externally in the last [N] days:
>
> 1. stripe.com - 4 threads - last: 'PCI doc request' (Mar 18)
> 2. razorpay.com - 2 threads - last: 'Settlement API timeline' (Mar 15)
> 3. deloitte.com - 3 threads - last: 'KYC framework review' (Mar 20)
> [up to 10 vendors shown, sorted by most recent activity]
>
> Which of these are active vendor dependencies you want to track?
> Reply with numbers (e.g. `1, 3`) or names. Add any vendors not listed above.
> Skip any that are noise - you can always add them later."

Wait for response. Store selected vendors.

---

**Step C - Group into initiatives:**

> "How should I group these vendors into initiatives? An initiative is a goal or project you're driving with external help.
>
> Example:
> - 'PaymentGateway' → Stripe, Razorpay
> - 'ComplianceAudit' → Deloitte
>
> Tell me your initiative names and which vendors belong to each. Or say 'one per vendor' and I'll name them after each vendor."

If user says 'one per vendor': create one initiative per selected vendor using the vendor's company name.

---

**Step D - Focus context per initiative (optional):**

For each initiative, ask once:

> "For **[InitiativeName]** - what are you trying to get from [vendor(s)]?
>
> Optionally add:
> - Keywords or subject lines to focus on (e.g. 'API docs', 'compliance sign-off')
> - Specific contacts to watch (e.g. john@stripe.com)
> - A target deadline for this initiative (e.g. 'April 15' or 'end of Q2')
>
> Press Enter to scan all threads from this vendor with no filter."

Store as `focus_context`, `focus_keywords`, `focus_contacts`, and `initiative_deadline` on the initiative. Keywords and contacts narrow the Gmail scan. The deadline is used in risk scoring to elevate all threads as the date approaches.

---

**Step E - Existing data import (optional):**

> "Do you already have tracker data for any of these initiatives - in a Google Sheet, a spreadsheet, or even a rough list you can paste?
>
> - **Google Sheet URL**: paste it and I'll read the existing rows and map them into the tracker
> - **Another spreadsheet**: paste the rows as text and I'll parse them
> - **Rough notes**: describe what's in flight and I'll create rows from your description
> - **Nothing yet**: I'll start fresh from your emails
>
> If you have existing data, this saves you re-entering what you already know."

For each initiative where existing data is provided:
- If Sheet URL: read all rows, map columns to the tracker schema as best as possible, ask the user to confirm the mapping before writing, do not delete or move columns in the source sheet
- If pasted text: parse into rows, ask user to confirm before writing
- If rough notes: extract tasks, vendors, statuses, ETAs from the text and pre-populate rows - mark each as `source: manual_import` so they are distinguishable from email-derived rows
- If nothing: leave the sheet empty and let Phase 3 populate it from Gmail

---

**Step F - Google Sheets:**

> "Should I create new Google Sheets for each initiative, or do you have existing ones to connect?
>
> Paste a Sheet URL next to an initiative to connect it. Leave blank for a new sheet.
>
> Example:
> PaymentGateway → https://docs.google.com/spreadsheets/d/...
> ComplianceAudit → (new)"

For connected sheets: read current structure, check for required columns, ask permission to add missing columns without touching existing ones.
For new sheets: create named after the initiative with the standard schema.

---

**Step G - Summary email (optional):**

> "What email should the daily 10am progress summary go to?
> Press Enter to use your connected Gmail: [gmail_address]"

---

**Step H - Anthropic API key (optional, scheduler only):**

> "Last one - do you have an Anthropic API key? This is only needed for the automated scheduler that runs without Claude open. You can skip this now and add it when setting up the scheduler later.
>
> If you have one, paste it here (starts with sk-ant-). It will be stored locally at `~/.config/pm-project-management/.anthropic_key` and never committed to this repo."

---

Create `~/.config/pm-project-management/config.json` with this structure:

```json
{
  "company_domain": "<derived from Gmail>",
  "summary_email_recipient": "<email or gmail address>",
  "scan_lookback_days": 30,
  "anthropic_api_key_path": "~/.config/pm-project-management/.anthropic_key",
  "initiatives": {
    "PaymentGateway": {
      "sheet_url": "https://docs.google.com/spreadsheets/...",
      "vendors": {
        "Stripe": "stripe.com",
        "Razorpay": "razorpay.com"
      },
      "focus_context": "API integration and PCI compliance docs",
      "focus_keywords": ["PCI", "settlement API", "integration doc"],
      "focus_contacts": ["john@stripe.com"],
      "initiative_deadline": "2026-04-15"
    }
  },
  "last_sync": {},
  "config_sheet_url": ""
}
```

Store the Anthropic API key separately in `~/.config/pm-project-management/.anthropic_key`. Add both files to `.gitignore` if in a project directory.

After completing all steps, confirm:

> "All set. Here's what I've configured:
> - [N] initiative(s): [list names and vendor counts]
> - Sheets: [created / connected - list with URLs]
> - Scan window: [N] days
> - Summary email: [address]
> - Scheduler: [API key saved / not yet - run Option E when ready]
>
> Ready to run your first sync? (Y / N)"

---

## Phase 1 - Session Intent

After preflight, ask the user:

> "What would you like to do?
> - **A** - Add a new initiative
> - **B** - Sync and update a specific initiative
> - **C** - Sync and update all initiatives
> - **D** - View a live summary of all open items
> - **E** - Set up or regenerate the Apps Script scheduler
> - **F** - Log offline context (meeting notes, Slack updates, call outcomes)
> - **G** - Review new vendor threads detected in Gmail"

Handle each path:

**Path A - New initiative:** See Phase 2.

**Path B - Specific initiative:** List initiatives from config. User selects one. Run Phase 3 for that initiative only.

**Path C - All initiatives:** Run Phase 3 for each initiative in config sequentially. Show consolidated status at the end. Also run Phase 3 Step 8 (new vendor detection) at the end.

**Path D - Summary:** Jump to Phase 5. Do not sync. Read current sheet state and display.

**Path E - Scheduler:** Jump to Phase 6.

**Path F - Offline context:** Jump to Phase 7.

**Path G - New vendor review:** Surface any external domains detected in recent Gmail that are not in config (see Phase 3 Step 8). Ask the user which ones to add as new initiatives.

---

## Phase 2 - New Initiative Setup

### Step 1: Get initiative details

Ask:
> "Tell me about this initiative:
> - What is it called? (or I can suggest a name based on context)
> - Which vendor or vendors are involved? List their company names.
> - What are you trying to get from this vendor - what does 'done' look like?
> - Is there a target deadline for this initiative? (optional)
> - Do you have an existing Google Sheet, existing tracker data to import, or should I start fresh?"

If the user is unsure of the initiative name, offer to derive it from recent emails: search Gmail for threads from external domains using `scan_lookback_days`, group by vendor domain, and suggest the top candidates with thread counts.

### Step 2: Determine vendors

For each vendor name provided:
- Confirm or derive their email domain (e.g. `Stripe` → `stripe.com`)
- Ask if there are specific contacts at this vendor to watch, or monitor the whole domain
- Ask for any focus keywords or subject lines to narrow the scan (optional)

### Step 2b: Identify internal SPOCs and team context

After confirming vendors, ask:

> "Who on your team owns this initiative?
>
> For each topic area or vendor track, tell me:
> - **Owner name** - first name is enough
> - **What they own** - e.g. 'compliance items', 'tech integrations', 'ops and reconciliation', 'regulatory filings'
>
> Example: 'Priya → compliance and risk; Rohan → tech and API; Neha → ops and reconciliation; Arjun → regulatory and audit'
>
> If you're the only owner, just say so. This helps the AI assign the right SPOC when it reads email threads."

Store the answer as a single `teamContext` string in the initiative config:
```
teamContext: "Priya → compliance and risk; Rohan → tech and API; Neha → ops; Arjun → regulatory"
```

This field is injected into every Claude batch analysis prompt so SPOC detection uses real team structure rather than guessing from email addresses alone.

**If the user adds multiple initiatives at once**, ask the team context question once per initiative (not once overall) - each initiative may have a different owner breakdown.

### Step 3: Import existing data (optional)

If the user has existing tracker data:
- **Sheet URL**: Read all rows. Show a column mapping preview and ask the user to confirm before writing anything. Add any missing columns to the schema without touching existing ones.
- **Pasted text / CSV**: Parse rows, show a preview, confirm before writing.
- **Rough notes / description**: Extract tasks, statuses, ETAs, and SPOC names. Create rows tagged `source: manual_import`. Show a preview and confirm before writing.

All imported rows are written with today's date in the current week's Update column and `source: manual_import` in the Thread ID column so they are distinguishable from email-synced rows.

### Step 4: Create or connect the Google Sheet

**If connecting an existing sheet:**
- Read the sheet structure
- Check for required columns (A–M, see column schema at top of this file)
- Ask permission to add any missing columns
- Do not delete or move existing columns

**If creating a new sheet:**
1. Use `create_spreadsheet` to create a new Google Sheet named after the initiative
2. Rename the default tab from "Sheet1" to `Open Items` (or whatever the user sets as `sheetTab`)
   - Apps Script `formatAllSheets()` matches by tab name and will silently fail if it finds "Sheet1"
3. Write the 13 column headers in row 1: `Task / Category / Internal SPOC / ETA / Status / Latest Update / Commitments / Risk Score / Risk / Vendor / Source / Action Pending On / Last Updated`
4. Share the sheet URL with the user and note the Sheet ID for config

Dropdowns and conditional formatting must be applied via Apps Script `formatAllSheets()` - MCP cannot set data validation or conditional format rules.

### Step 5: Update config and complete setup

**5a. Update local config**

Add the new initiative to `~/.config/pm-project-management/config.json` with all fields from Steps 1, 2, and 2b (including `teamContext`).

**5b. Add row to Master Dashboard**

Write a new row to the Master Dashboard Google Sheet (the sheet at `MASTER_SHEET_ID`). Fill in these columns:

| Column | Value |
|--------|-------|
| Initiative (A) | Initiative display name |
| Tracker Link (B) | `https://docs.google.com/spreadsheets/d/<sheetId>` |
| Vendors (C) | Comma-separated vendor names |
| Open HIGH (D) | 0 |
| Open MEDIUM (E) | 0 |
| Open LOW (F) | 0 |
| Sheet ID (I) | Exact Google Sheet ID string |

Leave columns G, H, J, K, L blank - Apps Script will fill these on first sync.

Note: If you skip this step, Apps Script will auto-create the master row on the first sync run, but it will be missing the Initiative display name and Tracker Link columns which it cannot infer.

**5c. Add initiative to the _Config tab**

If the Apps Script scheduler is already running:
1. Open the Master Dashboard Google Sheet → go to the `_Config` tab
2. Add a new row with all fields: Initiative (key name, no spaces), Sheet ID, Sheet Tab, Vendor Domains (comma-separated), Vendor Names (comma-separated), Focus Contacts (comma-separated), Team Context, Deadline (YYYY-MM-DD or blank), Lookback Days, Description
3. In the Apps Script editor, edit `addNewInitiativeSetup()`: set `initiativeName` to match the value in column A exactly
4. Run `addNewInitiativeSetup()` to initialise sync timestamps and validate the sheet
5. Run `formatAllSheets()` to apply headers, dropdowns, and conditional formatting to the new sheet

No changes to `pm-tracker.gs` are needed - the script reads config from the `_Config` tab automatically.

If the scheduler is not yet set up, proceed to Phase 6.

Notify the user:
> "Initiative added and configured. The next scheduled sync (or a manual `syncAll()` run) will scan the last N days of email and populate the sheet."

---

## Phase 3 - Scan and Sync

**Determine sync mode first.** Check two conditions for this initiative:
1. Does the Google Sheet exist and contain at least one data row?
2. Is `last_sync` set in config for this initiative?

If **both** are true → **Incremental mode** (skip to Step 3).
If **either** is missing → **Bootstrap mode** (start at Step 1).

---

### Step 1: Bootstrap - build the tracker (first run only)

**Goal:** Read enough context to create a complete, accurate sheet. This is the only run where reading deeper into threads is expected.

**Gmail query:** `from:@<vendor_domain>` within the last `scan_lookback_days` days (the user's chosen value - do not override it). Apply `focus_contacts` and `focus_keywords` filters if set. Cap at 30 threads per initiative.

**For each thread:** Apply the context-reading rule (Token Rule 1) - start with the most recent message, read backwards until Task, SPOC, ETA, and Status can all be filled, or until 10 messages are read. Any field still unresolvable after 10 messages is written as `Not enough context`.

**Extract per thread:**
- Task description (infer from subject + body if not explicit)
- SPOC name and email
- ETA: any delivery date, deadline, or "by [date]" clause
- Status: infer from tone and content (To Do / In Progress / Blocked / In Review / Solutionising)
- Task category: Feature / Operations / Compliance / Risk
- Last sender and date
- Thread ID and permalink

**Write:** Construct all rows and write to the sheet in one batch. Populate the Thread ID column for every row - this is the deduplication key for all future incremental syncs.

**After writing:** Set `last_sync` to current UTC timestamp in config. This initiative is now in incremental mode for all future runs.

---

### Step 2: Offline conversation check (bootstrap)

After the batch write, read the Thread ID and Status columns only. If any rows were pre-populated from a manual import (Setup Wizard Step E), check whether the imported status is ahead of what the emails show. If so, ask the user:

> "I notice '[Task name]' is marked as '[Status]' in the tracker, but the emails don't show a matching update. Was this from an offline conversation?
> - **Yes**: Tell me what was discussed and I'll log it
> - **No**: I'll flag this row as needing verification
> - **Skip**: Leave it unchanged for now"

---

### Step 3: Incremental - delta sync (all runs after bootstrap)

**Gate:** Only run if sheet exists AND `last_sync` is set. If either is missing, run Bootstrap instead.

**Gmail query:** `from:@<vendor_domain> after:<last_sync_timestamp>`. Apply focus filters if set. This query returns only threads with new activity since the last sync - no additional delta logic needed. Cap at 20 threads per run; log skipped count if cap is hit.

**For each returned thread:** Read the last message only. Apply Token Rule 2 - only read further back (up to 10 messages) if the last message alone leaves ETA or Status ambiguous.

**Match to existing rows:** Read the Thread ID column only. If a thread ID matches an existing row, update that row. If no match, append a new row. Write all changes in one batch at the end.

**Offline conversation check (incremental):** For rows being updated, check whether the current sheet Status is ahead of what the new email shows (manual update since last sync). Read the Status cell for those specific rows only. Apply the same check-and-ask as Step 2 above.

**After writing:** Update `last_sync` to current UTC timestamp.

### Step 4: Risk scoring and field extraction

For each row (new or updated), compute the risk score. The `analyzeRisk()` Claude Haiku call returns all fields in one response - no separate calls needed for metadata extraction.

```
Score = (0.30 × time_score) + (0.25 × eta_score) + (0.25 × tone_score) + (0.20 × velocity_score)
```

**Time since last vendor reply:**
- Under 48 hours → 1 (Low)
- 2 to 5 days → 2 (Medium)
- Over 5 days → 3 (High)

**ETA proximity:**
- More than 14 days away → 1 (Low)
- 3 to 14 days away → 2 (Medium)
- Within 3 days or already passed → 3 (High)

**Tone and sentiment of last vendor email:**
- Positive language, specific commitments, concrete next steps → 1 (Low)
- Vague, non-committal, partial answers, promises without dates → 2 (Medium)
- Deflecting, blame-shifting, extended silence, or negative language → 3 (High)

**Thread velocity (reply frequency trend):**
- Regular back-and-forth cadence → 1 (Low)
- Replies noticeably slowing down → 2 (Medium)
- One-sided thread, only your side responding, or no recent vendor reply → 3 (High)

**Initiative deadline modifier:**
If `initiative_deadline` is set on the initiative, apply a deadline escalation:
- More than 30 days to deadline: no modifier
- 8 to 30 days to deadline: add +0.2 to every row's score in this initiative
- Within 7 days to deadline: add +0.4 to every row's score in this initiative
- Deadline passed: add +0.6 to every row's score in this initiative
Cap the final score at 3.00.

**Risk level thresholds:**
- 1.00 – 1.67 → Low
- 1.67 – 2.33 → Medium
- 2.33 – 3.00 → High

Write the outputs to **two separate columns**:
- **Risk Score column** (`riskScoreCol`): numeric value rounded to 2 decimal places, e.g. `2.35`
- **Risk column** (`riskCol`): label only - `HIGH`, `MEDIUM`, `LOW`, or `TBD`

`riskScoreCol` is always immediately left of `riskCol` (i.e. `riskCol - 1`).

**Extended fields extracted in the same call:**
- `category`: Ops / Feature / Compliance / Tech / Process / Testing / Certification / Risk / CX
- `spoc`: first name of the internal team member responsible (from your company domain address or mentioned as owner), or `"Unknown"`
- `eta_date`: any delivery date mentioned (DD MMM), or `"-"`
- `status`: infer from tone - Open / In Progress / In Review / To be Picked
- `action_pending_on`: value of `INTERNAL_TEAM_NAME` if the vendor's last message asks your team to act, else the vendor name

If the score calculation is inconclusive (e.g. ETA unknown, very short snippet), write `TBD` in the Risk column and leave Risk Score blank.

**Stale row escalation:** After each sync run, scan all non-Done/Closed rows. Any row with no Last Updated in 14+ days has its Risk Score bumped +0.3 (capped at 3.00) automatically - no Claude call needed.

### Step 5: Cell formatting for Risk and Status columns

Formatting is applied via Apps Script `formatSheet()` - not via MCP (which is values-only).

**Risk column** (`riskCol`): dropdown validation + conditional formatting (text color only, no background fill)
- Dropdown options: `HIGH / MEDIUM / LOW / TBD`
- HIGH → red text `#cc0000`, bold
- MEDIUM → amber-yellow text `#ca8a04`, bold
- LOW → green text `#274e13`, bold
- TBD → grey text `#888888`, normal

**Risk Score column** (`riskScoreCol`): number format `0.00`, right-aligned, no dropdown

**Status column** (`statusCol`): dropdown validation + conditional formatting (text color only)
- Dropdown options: `Open / In Progress / In Review / Done / Closed / To be Picked / Solutionizing`
- Done / Closed → green text `#274e13`, bold
- In Progress → amber-yellow text `#ca8a04`
- In Review → purple text `#6d28d9`
- Open → orange text `#b45309`
- To be Picked / Solutionizing → grey text `#555555`

**Action Pending On column** (`actionCol`): dynamic dropdown built from `cfg.vendorNames` + `INTERNAL_TEAM_NAME` + `"Unknown"`. `setAllowInvalid(true)` so users can type unlisted names. Conditional formatting: `INTERNAL_TEAM_NAME` value = orange text `#b45309` bold (you need to act).

**Last Updated column** (`totalCols + 1`): plain text timestamp in user's local timezone (`Session.getScriptTimeZone()`), format `DD MMM YYYY HH:MM`. Written only when a row is actually added or changed - never on a no-op scan pass.

### Step 6: Update weekly columns

Check the current week's `Update <date>` column header (format: `Update DD-Mon`, e.g. `Update 16-Mar`):
- If a column with this week's Monday date exists: overwrite its value for the updated row
- If no column exists for this week: create a new column to the right of the last Update column with today's Monday as the header
- Never delete or hide old Update columns - they are the historical record

### Step 7: Update last sync timestamp

After a successful sync, write the current UTC timestamp to `last_sync` in config for this initiative.

### Step 8: New vendor detection

After syncing all configured initiatives, scan Gmail for external domains active in the last `scan_lookback_days` that are NOT in any current initiative config. Exclude the company domain and known noise (noreply, newsletters, etc.).

If new external domains are found, surface them:

> "I also spotted activity from vendors not currently being tracked:
>
> 1. newvendor.com - 3 threads - last: 'Contract terms discussion' (Mar 21)
> 2. anotherco.com - 1 thread - last: 'Partnership proposal' (Mar 19)
>
> Want to add any of these to tracking? Reply with numbers, names, or 'skip' to ignore for now."

If the user selects any: run Phase 2 for each selected vendor. If the user skips: note the domains in a `suggested_vendors` list in config so they can be reviewed later via Path G.

---

## Phase 4 - Multi-Initiative Handling

When running sync across all initiatives (Path C):

- Process each initiative sequentially
- For each initiative, run Phase 3 Steps 1–7 in full
- After all initiatives are processed, run Phase 3 Step 8 (new vendor detection) once
- Show a consolidated summary:

```
Sync complete - 3 initiatives updated

PaymentGateway     → 4 threads scanned, 2 rows updated, 1 new row added
ComplianceAudit    → 2 threads scanned, 2 rows updated, 0 new rows
OnboardingPartner  → 6 threads scanned, 3 rows updated, 2 new rows added

High risk items: 3   Medium: 4   Low: 7

New untracked vendors detected: 2 - run Option G to review
```

---

## Phase 5 - On-Demand Summary

Read the current state of all initiative sheets (do not re-scan Gmail). Aggregate all rows where Status is not `Done` or `Closed`. Sort by risk score descending. Output:

```
Open Items as of 16 Mar 2026 - 14 items across 3 initiatives

🔴 [HIGH 2.8] PaymentGateway / Stripe - PCI compliance doc - open 9 days - last reply vague, no ETA given
🔴 [HIGH 2.5] ComplianceAudit / Deloitte - KYC framework sign-off - ETA passed 3 days ago - no response since Mar 12
🟡 [MED 2.1]  PaymentGateway / Razorpay - Settlement API spec - open 5 days - active thread, vendor requested more time
🟡 [MED 1.8]  OnboardingPartner / Vendor X - Integration doc - ETA in 4 days - replies slowing
🟢 [LOW 1.2]  PaymentGateway / Stripe - Webhook retry spec - open 1 day - vendor acknowledged, in progress
...
```

Also flag initiative-level deadline proximity:

```
⚠️  PaymentGateway deadline in 6 days (Apr 15) - 3 open items, 1 HIGH risk
```

---

## Phase 6 - Scheduler Setup (Apps Script)

### Automation architecture

Apps Script is the **primary and only automation layer**. It runs fully autonomously on Google's infrastructure - no dependency on Claude Code being open, idle, or connected.

| Layer | Role | When |
|-------|------|------|
| **Apps Script + Claude API** | Primary automation - Gmail scan, AI risk scoring via `claude-haiku-4-5-20251001`, sheet writes, summary email, master sheet timestamp update | 2× daily always |
| **Claude Code** | On-demand - deep analysis, new initiative setup, config changes, retrospective bulk sync | When you explicitly invoke it |

Session CronJobs are not used. `launchd + claude -p` does not work for MCP-dependent tasks (MCP cannot connect in non-interactive mode).

### Step 1: Prerequisites

Before generating the script, confirm:
1. User has an Anthropic API key from `console.anthropic.com` (stored in Apps Script PropertiesService - never in code)
2. `MASTER_SHEET_ID` is known (PM Tracker Master Dashboard)
3. Each initiative has `sheetId`, `sheetTab`, `vendorDomains`, `vendorNames`, `focusContacts`, `teamContext`, `initiativeDeadline`, and `scan_lookback_days` ready - these go into the `_Config` tab, not into code

### Step 2: Script template

The repository contains the ready-to-use template at:
`apps-script/pm-tracker.template.gs`

This file is committed to the public repo. The real `pm-tracker.gs` (with real sheet IDs, email, and API key reference filled in) is gitignored via `**/*.gs` + `!**/*.template.gs`.

### Step 3: Fill in and deploy

1. Copy `pm-tracker.template.gs` → `pm-tracker.gs` in the same directory
2. Fill in four values at the top of the file: `SUMMARY_EMAIL`, `USER_DOMAIN`, `MASTER_SHEET_ID`, `INTERNAL_TEAM_NAME`
   - All initiative config lives in the `_Config` tab; no code changes needed for initiatives
3. Go to `script.google.com` → New project → paste `pm-tracker.gs`
4. Open **Project Settings** (gear icon) → **Script Properties** → add:
   - Key: `ANTHROPIC_API_KEY` - Value: `sk-ant-...`
5. Run `setupConfigTab()` once to create the `_Config` tab in the Master Dashboard, pre-populated with your initiatives
6. Edit the `_Config` tab rows to verify all fields are correct (Sheet IDs, vendor domains, teamContext, etc.)
7. Run `setupProperties()` once to initialise sync timestamps and validate the API key
8. Run `formatAllSheets()` once to apply formatting, dropdowns, and conditional rules to all sheets
9. Run `setupTriggers()` once to create the 10am / 5pm time-based triggers
10. Authorise Gmail + Sheets + UrlFetch scopes when prompted
11. Run `runIncrementalSync()` once manually to verify Claude API scoring works end to end

### Step 4: What runs automatically

**At 10am:** `runMorningSyncAndEmail()` - Gmail scan + Claude API risk scoring + daily summary email
**At 5pm:** `runIncrementalSync()` - Gmail scan + Claude API risk scoring, no email

Per run, for each initiative:
- Appends new vendor threads as rows with `Risk Score` (numeric) and `Risk` (label)
- Writes `Last Updated` timestamp (user's local timezone) only on changed rows
- Updates the initiative's `Last Sync (Script)` column in the Master Dashboard
- Falls back to `Risk = TBD`, `Risk Score = ""` if API key is missing or call fails

### Step 5: Master Dashboard - sync columns

After each sync, Apps Script performs a **single-pass batch update** to the Master Dashboard (one sheet open, one data read, all initiative rows updated together):

- **Last Sync (Script)** (col H): timestamp of the last automated sync
- **New (Last Run)** (col K): count of new rows added in this run
- **Updated (Last Run)** (col L): count of rows updated in this run
- **Open HIGH / Open MEDIUM / Open LOW** (cols D-F): live counts of open items at each risk level, recounted after every sync

Match initiative rows by **Sheet ID** (col I) - exact string match. Never match by display name.

If any column doesn't exist yet, create it with the standard header style. If `Sheet ID` column is missing, log a warning and skip the update.

### Step 6: Pausing or closing an initiative

To stop scanning an initiative without losing its history or master sheet row:
1. Open the Master Dashboard → `_Config` tab
2. Set the `Active` column for that initiative to `N`
3. The next sync will skip it entirely - no Gmail scan, no Claude calls, no sheet writes

To reactivate: change `Active` back to `Y`. No other steps needed.

Do not delete the `_Config` row - that would orphan the master sheet row and the existing tracker sheet data.

---

## Phase 7 - Offline Context Logging

Use when the user has context from outside email: a call, a Slack message, a meeting, an in-person conversation, or any other offline update.

### Step 1: Identify the initiative and vendor

Ask:
> "Which initiative and vendor is this context for?
> [List current initiatives and vendors]"

### Step 2: Accept context input

Ask:
> "Paste or describe the context. This can be:
> - Meeting notes or call summary
> - A Slack message or screenshot description
> - A status update you heard verbally
> - An updated ETA or commitment from the vendor
> - Any other offline information
>
> Be as detailed or as brief as you like - I'll extract what's relevant."

### Step 3: Parse and preview

Extract from the input:
- Updated status or progress
- Any new or revised ETA
- Any new commitments or blockers
- Names of people involved

Show a preview:

> "Here's what I'll log in the tracker:
>
> Initiative: PaymentGateway / Stripe
> Task: PCI compliance doc
> Update: Called John (Stripe) on Mar 21. Confirmed doc will be sent by Mar 24. Blocker was internal review - now cleared.
> Updated ETA: Mar 24
> Status: In Progress → In Review
> Source: Offline (call)
>
> Does this look right? (Y / edit / skip)"

### Step 4: Write to sheet

After confirmation:
- Find the matching row by initiative, vendor, and task description
- If found: update Status, Updated ETA, and the current week's Update column with the parsed summary + "(offline)" tag
- If not found: ask the user if this is a new task - if yes, create a new row tagged `source: manual_offline`
- Recalculate risk score with the new context (tone and ETA updated)
- Apply color coding

---

## Master Dashboard Schema

One row per initiative. The master sheet is the single-pane view across all initiatives.

| Col | Header | Description | Who writes |
|-----|--------|-------------|-----------|
| A | Initiative | Display name (e.g. `VendorInitiative`) | Manual |
| B | Tracker Link | Hyperlink to the initiative sheet | Manual |
| C | Vendors | Comma-separated vendor names | Manual |
| D | Open HIGH | Count of HIGH risk open items | Manual / Claude sync |
| E | Open MEDIUM | Count of MEDIUM risk open items | Manual / Claude sync |
| F | Open LOW | Count of LOW risk open items | Manual / Claude sync |
| G | Last Synced | Date of last manual review | Manual |
| H | Last Sync (Script) | Timestamp of last automated or Claude sync | Apps Script + Claude Code |
| I | Sheet ID | Google Sheet ID of the initiative tracker - **lookup key** | Set once, never changes |

**Key rules:**
- `Sheet ID` (col I) is the authoritative lookup key - always match initiative rows by Sheet ID, never by display name
- `Last Sync (Script)` is written by both Apps Script and Claude Code - a single shared column, no separate "Last Sync (Claude)" column
- When running a Claude-driven sync, after writing sheet updates, find the initiative's row via Sheet ID and write the current timestamp to `Last Sync (Script)`

---

## Sheet Schema

One sheet per initiative. Sheet name = initiative name (e.g. `PaymentGateway`).

All cell formatting (colors, dropdowns, frozen rows, column widths) is applied via Apps Script `formatAllSheets()` - not via MCP.

### 12-column schema (standard - with Team Owner)

| Col | # | Header | Description |
|-----|---|--------|-------------|
| A | 1 | Task | One-line task description - Claude-extracted from subject |
| B | 2 | Category | Ops / Feature / Compliance / Tech / Process / Testing / Certification / Risk / CX |
| C | 3 | SPOC | Your-team-side person responsible - Claude-extracted from email context |
| D | 4 | Team Owner | Internal team - filled manually |
| E | 5 | ETA | Full date: `DD MMM YYYY` - Claude-extracted |
| F | 6 | Status | Dropdown: Open / In Progress / In Review / Done / Closed / To be Picked / Solutionizing |
| G | 7 | Latest Update | One-sentence status summary - Claude-written |
| H | 8 | Risk Score | Weighted numeric score e.g. `2.35` - format `0.00`, right-aligned |
| I | 9 | Risk | Dropdown: HIGH / MEDIUM / LOW / TBD - color-coded text |
| J | 10 | Vendor | Sender domain |
| K | 11 | Source | `Gmail:<threadId> (DD MMM YYYY)` for email rows - Thread ID is the dedup key |
| L | 12 | Action Pending On | Who needs to act: `[Your Team]` (orange) or vendor name - Claude-inferred |
| M | 13 | Last Updated | Timestamp of last change: `25 Mar 2026 10:03` - auto-added |

Apps Script config: `riskScoreCol: 8`, `riskCol: 9`, `statusCol: 6`, `actionCol: 12`, `totalCols: 12`

### 11-column schema (compact - no Team Owner)

| Col | # | Header | Description |
|-----|---|--------|-------------|
| A | 1 | Task | One-line task description |
| B | 2 | Category | Ops / Feature / Compliance / Tech / Process / Testing / Certification / Risk / CX |
| C | 3 | SPOC | Your-team-side person responsible |
| D | 4 | ETA | Full date: `DD MMM YYYY` |
| E | 5 | Status | Dropdown: Open / In Progress / In Review / Done / Closed / To be Picked / Solutionizing |
| F | 6 | Latest Update | One-sentence status summary - Claude-written |
| G | 7 | Risk Score | Weighted numeric score e.g. `2.35` - format `0.00`, right-aligned |
| H | 8 | Risk | Dropdown: HIGH / MEDIUM / LOW / TBD - color-coded text |
| I | 9 | Vendor | Sender domain |
| J | 10 | Source | `Gmail:<threadId> (DD MMM YYYY)` - Thread ID is the dedup key |
| K | 11 | Action Pending On | Who needs to act: `[Your Team]` (orange) or vendor name |
| L | 12 | Last Updated | Timestamp of last change - auto-added |

Apps Script config: `riskScoreCol: 7`, `riskCol: 8`, `statusCol: 5`, `actionCol: 11`, `totalCols: 11`

**Key schema rules:**
- `riskScoreCol` is always `riskCol - 1` (Risk Score immediately left of Risk)
- `Last Updated` column is always `totalCols + 1` - added automatically, never in `totalCols` count
- ETA: always full date `DD MMM YYYY` - never abbreviated `DD MMM`
- Risk Score: numeric `0.00` format, right-aligned, no dropdown
- Risk + Status: dropdown validation + conditional text color (no cell background fill)
- Last Updated: written only when a row is added or changed, not on no-op scan passes
- Timezone: `Session.getScriptTimeZone()` - reads from Google account settings, not hardcoded

---

## Summary Email Format

Subject: `Progress Tracker 2026-03-16 | 7 open items`

Body (HTML email, risk color-coded):

```
Progress Tracker - 16 March 2026
7 open items across 3 initiatives

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  DEADLINE ALERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PaymentGateway - deadline in 6 days (Apr 15) - 3 open items

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 HIGH RISK (2 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• PaymentGateway / Stripe - PCI compliance doc
  Open 9 days | ETA passed | Last reply Mar 7 - vague, no concrete next step

• ComplianceAudit / Deloitte - KYC framework sign-off
  Open 12 days | ETA passed 3 days ago | No reply since Mar 12

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 MEDIUM RISK (3 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• PaymentGateway / Razorpay - Settlement API spec
  Open 5 days | ETA Mar 20 | Active thread, vendor requested 2 more days

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 LOW RISK (2 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• PaymentGateway / Stripe - Webhook retry spec
  Open 1 day | ETA Mar 22 | Vendor acknowledged, work in progress

...
```

---

## What This Skill Does Not Do

- Does not integrate with Jira (planned for a future version)
- Does not auto-publish PRDs or documents
- Does not support non-Google email providers
- Does not modify or delete existing sheet rows without user confirmation when a discrepancy with offline context is detected
- Does not store secrets in this file or the GitHub repository under any circumstances
