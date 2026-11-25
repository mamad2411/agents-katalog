---
name: ssagent-weekly
description: Runs the weekly cadence workflow for all open ASQs. Fetches every ASQ with status In Progress, Under Review, or On Hold, researches each one in parallel, then walks through approval sequentially. Use at the start or end of each week to keep all ASQ status notes up to date.
user-invocable: true
model: haiku
---

# ASQ Weekly

Weekly note-taking pass across all your open ASQs.

**Usage:** `/ssagent-weekly`

---

## Prerequisites — Authenticate Once (Parallel)

Load the profile using `load_profile.py` from `ssagent-sfdc` (returns all keys with defaults applied). Extract `sf_org`, `sf_user_id`, and `initials`. If any is `None`, fall back to `fe-salesforce-tools:salesforce-authentication` and the User query pattern from `ssagent-sfdc` Reusable Query Patterns.

Substitute the resolved `sf_org` value as a **literal** into every `<SF_ORG_USERNAME>` placeholder below.

Get today's date: `python3 -c "from datetime import date; print(date.today())"` — carry it as `TODAY`.

**Google** — warm the auth cache so background tasks don't trigger an OAuth prompt:
```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
python3 "$GOOGLE_AUTH" token 2>/dev/null
```

---

## Step 1 — Fetch All ASQ Data in One Query

```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Status__c, End_Date__c, Request_Status_Notes__c FROM ApprovalRequest__c WHERE OwnerId = '<USER_SFDC_ID>' AND Status__c IN ('In Progress', 'Under Review', 'On Hold') AND Request_Type__c = 'Specialist SA (SSA) Request' ORDER BY AssignmentDate__c DESC" --target-org <SF_ORG_USERNAME> --json
```

Filter out any ASQ whose `Request_Status_Notes__c`, after stripping leading whitespace, already starts with the expanded `note_format.prefix` for today (default: `<INITIALS> <TODAY>:`) — these are already up to date and should be skipped silently.

Display the list to the user:
```
Open ASQs (N total, M to process):
  ✓ AR-XXXXXXXXX — [Account Name] — already noted today, skipping
  1. AR-XXXXXXXXX — [Account Name] — [Status] — due [End_Date]
  2. ...
```

If all ASQs are already noted today: tell the user and stop.
If zero open ASQs: tell the user and stop.

---

## Step 2 — Parallel Background Research

Launch one background research Task (subagent_type: `general-purpose`, `run_in_background: true`) per ASQ simultaneously. Pass each task the pre-fetched SF record data, `INITIALS`, and `TODAY` — **tasks must not re-authenticate**.

Each task receives: `{ ar, account_name, sfdc_id, end_date, existing_notes }` and should:

1. Flag `DATE_STALE = true` if `End_Date__c` is before `TODAY`

2. **Google Calendar** — invoke `fe-google-tools:google-calendar` to search for meetings with `[ACCOUNT_NAME]`:
   - Past N days (profile `lookback.calendar_past_days`, default 7) + next N days (profile `lookback.calendar_future_days`, default 14)
   - Extract: meeting titles, dates, outcomes, any agenda items

3. **Gmail** — invoke `fe-google-tools:gmail` to search for emails mentioning `[ACCOUNT_NAME]` in the past N days (profile `lookback.email_days`, default 14):
   - Extract: thread subjects, key decisions or action items

4. **Slack (fallback only)** — only invoke `fe-workflows:slack-discovery-agent` if Calendar and Gmail returned no useful context. Include the account name AND the authenticated user's name/email as required filters.

5. Based on all context, draft a note following the profile `note_format.template` (default: `<prefix>: <summary>. Next: <next steps>.`) with prefix expanded from `note_format.prefix` (default: `<INITIALS> YYYY-MM-DD`). If `custom_instructions` is set, apply it. Style rules:
   - Focus on **what** is happening and **when** — not who organised or scheduled things
   - Do not mention organiser names or internal SA names unless directly relevant to the customer outcome
   - Keep it action-oriented: what happened, what's next, what needs doing
   - If no context found: draft `<prefix>: No customer contact this week.` and flag `needs_user_input: true`

6. If `DATE_STALE`, produce a **suggested new End_Date** using this priority:
   - Upcoming calendar meeting: day after the last upcoming meeting
   - Email/Slack milestone date mentioned: day after that date
   - Fallback: **TODAY + 14 days** (not from the old stale date)

7. Return a structured result:
   ```
   ar: AR-XXXXXXXXX
   account: [name]
   sfdc_id: [id]
   draft_note: [full note string]
   needs_user_input: true/false
   date_stale: true/false
   current_end_date: YYYY-MM-DD
   suggested_end_date: YYYY-MM-DD
   date_reason: [explanation]
   existing_notes: [current field value]
   ```

Launch all background tasks at once. Wait for all to complete before proceeding to Step 3.

---

## Step 3 — Sequential Approval Loop

Once all background research tasks are complete, iterate through each result in order.

For each ASQ:

**A. Due date (if stale):** Show the warning, then use `AskUserQuestion` with options:
- "Accept suggested date: [suggested_end_date] ([date_reason])" (Recommended)
- "Enter a different date"
- "Leave as-is"

If accepted or a different date is entered: update `End_Date__c` using `sf_update.py` from `ssagent-sfdc`.

**B. Note draft:** Show the proposed note, then use `AskUserQuestion` with options:
- "Approve" (Recommended) — save to Salesforce
- "Edit" — present the full draft as editable text; apply user's changes, then save
- "Skip" — move on without saving

If `needs_user_input: true`, ask the user to describe what happened before drafting.

**Saving a note** — load `sf_update_channel` from the profile (default: `dual`).

If `sf_update_channel` is `notes` or `dual`: use `sf_update.py prepend` from `ssagent-sfdc`. Pass `--separator` based on the profile's `note_format.separator` (default `single`).

If `sf_update_channel` is `chatter` or `dual`: post the same note to Chatter:
```bash
python3 "$SF_UPDATE" chatter \
  --record-id "<SFDC_ID>" \
  --text "<APPROVED NOTE>" \
  --org "<SF_ORG_USERNAME>"
```

If any update fails: show the error and ask the user whether to retry or skip.

---

## Step 4 — Summary

After all ASQs are processed, show:
```
Weekly notes complete:
  ✓ AR-XXXXXXXXX — [Account Name] — note added
  ✓ AR-XXXXXXXXX — [Account Name] — note added, due date extended to [date]
  - AR-XXXXXXXXX — [Account Name] — skipped
  ○ AR-XXXXXXXXX — [Account Name] — already noted today
  ...
```
