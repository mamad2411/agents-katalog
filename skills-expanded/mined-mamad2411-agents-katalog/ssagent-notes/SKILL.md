---
name: ssagent-notes
description: Adds a timestamped note to a single ASQ. Looks up recent Google Calendar meetings and emails for context, drafts a note for approval, then prepends it to Request_Status_Notes__c in the correct SSA format. Use when adding a progress update to an ASQ, or when invoked by ssagent-weekly.
argument-hint: "AR-XXXXXXXXX"
user-invocable: true
model: haiku
---

# ASQ Notes

Add a timestamped status note to a Salesforce ASQ.

**Usage:** `/ssagent-notes AR-XXXXXXXXX` or `/ssagent-notes munich; quick note hint here`

---

## Prerequisites

Load the profile using `load_profile.py` from `ssagent-sfdc` (returns all keys with defaults applied). Extract `sf_org` and `initials`. If either is `None`, fall back to `fe-salesforce-tools:salesforce-authentication` and the User query pattern from `ssagent-sfdc` Reusable Query Patterns.

Substitute the resolved `sf_org` value as a **literal** into every `<SF_ORG_USERNAME>` placeholder below.

---

## Step 1 — Resolve ASQ

Parse `$ARGUMENTS`:
- The AR number is the first token. If it starts with `AR-` → direct fetch by AR number. Otherwise → fuzzy match against open ASQs by customer name fragment, confirm with the user before proceeding.
- Extract any note hint from the arguments: text after `;`, `, `, or ` - `. Carry it into Step 3 as a starting point for the draft.

Once the ASQ is confirmed, fetch the ASQ record:

```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Status__c, End_Date__c, Request_Status_Notes__c FROM ApprovalRequest__c WHERE Name = '<AR-XXXXXXXXX>'" --target-org <SF_ORG_USERNAME> --json
```

Note: `Id`, `Account_Name__c`, `End_Date__c`, current `Request_Status_Notes__c` (full value — needed for prepend), and `<INITIALS>` (from profile or Prerequisites fallback).

**Data quality check — due date (flag only here):**
If `End_Date__c` is in the past, set `DATE_STALE = true` and carry it forward. Do **not** prompt the user yet — wait until after Step 2 so context can inform the suggested extension date.

---

## Step 2 — Gather Context (Parallel)

Run all in parallel to find recent and upcoming activity for this customer:

**A. Google Calendar** — invoke `fe-google-tools:google-calendar` to search for meetings with `[ACCOUNT_NAME]` covering:
- **Past N days** (profile `lookback.calendar_past_days`, default 7) — completed meetings (what was discussed)
- **Next N days** (profile `lookback.calendar_future_days`, default 14) — upcoming meetings (what is planned)
Extract: meeting titles, dates, attendees, any noted outcomes or agenda items.

**B. Gmail** — invoke `fe-google-tools:gmail` to search for emails mentioning `[ACCOUNT_NAME]` in the **past N days** (profile `lookback.email_days`, default 14). Extract: thread subjects, key decisions or action items mentioned.

**C. Slack (fallback only)** — only invoke `fe-workflows:slack-discovery-agent` if **both** Calendar and Gmail returned no useful context. When searching, include the account name **and** the authenticated user's name/email as a required filter — only return threads where the user is directly mentioned, tagged, or a participant.

If none of A, B, or C find anything, note that — the draft will prompt the user instead.

---

## Step 2.5 — Resolve Stale Due Date (if flagged)

Only run this step if `DATE_STALE = true` from Step 1.

Using context gathered in Step 2, determine the best suggested extension date using this priority order:

1. **Upcoming calendar meeting** — if there is a meeting with the customer in the next 14 days, suggest the day **after** the last such meeting
2. **Email or Slack context** — if a specific date, deadline, or milestone is mentioned, suggest the day after that date
3. **Fallback** — **today's date + 14 days** (not from the old stale date)

Then show the warning and use `AskUserQuestion` with options:
- "Accept suggested date: [SUGGESTED_DATE] ([reason])" (Recommended)
- "Enter a different date"
- "Leave as-is"

If accepted or a different date is entered: update `End_Date__c` using `sf_update.py` from `ssagent-sfdc`. Confirm success, then continue to Step 3.

---

## Step 3 — Draft Note

Using context from Step 2 (and any hint from the arguments), draft a concise note following the profile `note_format.template` (default: `<prefix>: <summary>. Next: <next steps>.`), where `<prefix>` is expanded using `note_format.prefix` (default: `<INITIALS> YYYY-MM-DD`).

If `custom_instructions` is set in the profile, apply it to the draft (e.g. "Always mention stakeholder names", "Keep notes in Dutch").

**Note style rules:**
- **Be concise** — the summary should be a single sentence capturing the key update
- **Always end with next steps** — prefix with `Next:` and state the concrete upcoming action(s)
- Focus on **what** happened and **what's next** — not who organised or scheduled things
- Do not mention organiser names or internal SA names unless directly relevant to the customer outcome
- Do not include notes about calendar conflicts with other internal events
- Omit filler words, meeting logistics, and obvious context — get straight to the point

If no context was found in Step 2: ask the user to describe what happened or what they want to note. Do not invent content.

Present the draft, then use `AskUserQuestion` with options:
- "Approve" (Recommended) — proceed to Step 4
- "Edit" — present the current draft as editable text; apply the user's changes, then confirm and proceed
- "Skip" — stop here

---

## Step 4 — Write to Salesforce and Chatter

Load `sf_update_channel` from the profile (default: `dual`).

**If `sf_update_channel` is `notes` or `dual`:**
Use `sf_update.py prepend` from `ssagent-sfdc` to safely write the combined notes to `Request_Status_Notes__c`. Pass `--separator` based on the profile's `note_format.separator` (default `single`). If the profile value is `double`, pass `--separator double` to insert a blank line between notes.

**If `sf_update_channel` is `chatter` or `dual`:**
Post the same note to Chatter so it appears in the ASQ's right sidebar:
```bash
python3 "$SF_UPDATE" chatter \
  --record-id "<SFDC_ID>" \
  --text "<APPROVED NOTE>" \
  --org "<SF_ORG_USERNAME>"
```

If any update fails: show the error and ask the user whether to retry or skip.
