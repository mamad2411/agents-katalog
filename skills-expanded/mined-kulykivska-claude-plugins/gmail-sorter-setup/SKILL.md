---
name: gmail-sorter-setup
description: >
  Set up the "Morning Gmail Sorter" cloud routine for whichever claude.ai
  account is currently logged in: creates a daily scheduled cloud agent that
  triages the connected Gmail inbox into Attention / Health / Receipts labels
  and flags obvious spam. Trigger on "set up mail sorting",
  "set up gmail sorter", "/gmail-sorter-setup". Works for any account —
  the Gmail connector of the CURRENT account is used.
---

# Gmail Sorter Setup

Goal: create (or update) a daily cloud routine named **Morning Gmail Sorter**
for the currently logged-in claude.ai account, identical to the one described
below. Do NOT run the triage yourself — only create the scheduled routine.

## Which account?

The routine lands on whichever account this Claude Code process is logged in as.
To target another account, do NOT use `/login`; start the session under that
account's profile instead: `claude-as <profile>` (e.g. `claude-personal`), or
headless: `claude-personal -p "/gmail-sorter-setup"`. `claude-as list` shows
profiles and login state. First run of a new profile asks for a one-time login.

## Steps

1. **Load the scheduler context.** Invoke the `schedule` skill (Skill tool,
   skill: `schedule`) with args "set up daily gmail triage routine". Its output
   lists the current account's available MCP connectors (with
   `connector_uuid`), environments, and the user's timezone. Then load the
   `RemoteTrigger` tool via ToolSearch.

2. **Verify the Gmail connector.** Find a connector whose URL is
   `https://gmailmcp.googleapis.com/mcp/v1` (name "Gmail") in the schedule
   skill's connector list. If it is missing, STOP and tell the user to connect
   Gmail for THIS account at https://claude.ai/customize/connectors, then
   re-run this skill. Use the `connector_uuid` from the list — it is different
   on every account; never reuse a UUID from another account or from memory.

3. **Check for an existing routine.** `RemoteTrigger {action: "list"}`. If a
   routine named "Morning Gmail Sorter" already exists on this account, ask
   the user whether to update it or leave it; do not create a duplicate.

4. **Pick the time.** Default: 7:00 in the user's local timezone, daily.
   Convert to a UTC cron expression (5 fields, e.g. 7:00 America/Chicago in
   summer = `0 12 * * *`). Confirm the conversion with the user only if they
   asked for a non-default time; otherwise state it in the final summary and
   mention the DST caveat (cron is fixed UTC, so local time shifts by an hour
   across DST changes).

5. **Create the routine.** `RemoteTrigger {action: "create"}` with:
   - `name`: "Morning Gmail Sorter"
   - `cron_expression`: from step 4
   - `enabled`: true
   - `mcp_connections`: the Gmail connector from step 2
     (`connector_uuid`, `name: "Gmail"`, `url: "https://gmailmcp.googleapis.com/mcp/v1"`)
   - `job_config.ccr.environment_id`: this account's default environment id
     from the schedule skill output
   - `job_config.ccr.session_context`: `model: "claude-sonnet-5"`,
     `sources: []`, `allowed_tools: ["Bash","Read","Write","Edit","Glob","Grep"]`
   - one user event with a freshly generated lowercase v4 UUID and the exact
     agent prompt from the section below (verbatim).

6. **Report.** Give the user the routine link
   `https://claude.ai/code/routines/{id}`, the local run time, and remind them
   that labels are created automatically on the first run.

## Agent prompt (use verbatim as the routine's message content)

```
You are a morning email triage assistant for a personal Gmail inbox. Use the Gmail MCP tools.

STEP 1 — Ensure labels exist (idempotent):
Call list_labels. If any of these user labels are missing, create them with create_label:
- "⚠️ Attention" (color preset RED) — things the owner must read or act on
- "Health" (color preset GREEN) — medical/health related
- "Receipts" (color preset BLUE) — purchases, payments, invoices
Remember each label's ID.

STEP 2 — Fetch new mail:
Call search_threads with query "in:inbox newer_than:1d" (paginate until done, up to ~100 threads). Skip any thread that already carries one of the three labels above.

STEP 3 — Classify each remaining thread by sender, subject and snippet (call get_thread only if the snippet is genuinely ambiguous):
- ATTENTION: personal messages from real people; anything requiring action or a reply; deadlines; account security alerts (real ones, e.g. password changed, new sign-in); bills due; messages from banks, government, landlord, school; delivery problems. Apply "⚠️ Attention".
- HEALTH: doctors, clinics, labs, pharmacies, insurance (medical), appointment reminders, test results, fitness/medical apps with meaningful info. Apply "Health".
- RECEIPTS: order confirmations, payment receipts, invoices, subscription charges, delivery confirmations, booking confirmations. Apply "Receipts".
- SPAM: unsolicited cold outreach, scams, phishing, sketchy marketing from senders the owner never interacted with. Use mark_thread_spam ONLY when clearly junk; when in doubt, leave it alone. NEVER mark as spam: anything matching Attention/Health/Receipts, personal mail, or transactional mail from services the owner actually uses.
- Everything else (ordinary newsletters, promos from known services, social notifications): leave untouched.
A thread can get both Health and Receipts (e.g. a paid clinic invoice) — apply both; Attention may combine with either when action is needed. Use label_thread with the label IDs from step 1. Do not archive, trash, or mark anything read.

STEP 4 — Summary:
Finish with a short morning digest: counts per category, then one line per Attention thread (sender — subject — why it needs attention), a short list of Health and Receipts items, and how many were sent to spam. Keep it concise and in English.
```
