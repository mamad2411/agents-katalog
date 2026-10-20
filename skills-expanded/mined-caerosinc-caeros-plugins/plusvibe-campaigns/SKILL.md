---
name: plusvibe-campaigns
description: Build, configure, verify, launch, pause, rename, and troubleshoot PlusVibe cold-email campaigns end to end - create the draft, inject the sequence, attach sending accounts, set the schedule, then launch. Use whenever the user wants to create, edit, schedule, launch, pause, archive, delete, or debug a PlusVibe campaign or asks why a campaign is not sending.
---

# PlusVibe campaigns

PlusVibe is a cold-email outreach platform. Two tool surfaces are valid: the
**remote MCP** at `https://mcp.plusvibe.ai/mcp`, using lower_snake_case names
(`create_campaign`), the primary naming below; and the **native Caeros app
provider** (AppSlug `plusvibe`), using UPPER_SNAKE slugs across 70 operations
tiered Read 24, Write 15, Admin 19, Delete 8, Send 4, authed at Settings ->
Apps -> "PlusVibe Auth" with one API key spanning every workspace. Slug
mapping is not mechanical (`set_campaign_schedule` is
`PLUSVIBE_SET_CAMPAIGN_SCHEDULES`) and some MCP tools have no native twin at
all, `get_campaign_variations` and the three campaign-account tools among
them. Read slugs off the app's tool list rather than guessing.

Every call except `get_workspaces` takes `workspace_id`; `get_workspaces`
(`PLUSVIBE_GET_WORKSPACES`) itself takes no arguments. Resolve the id once and
reuse it; if the user has several workspaces and named none, ask first.

## Read cheaply, and mind the two ID keys

`get_workspaces` returns workspaces keyed **`_id`**. `list_campaigns`
(`PLUSVIBE_LIST_ALL_CAMPAIGNS`) returns a bare array of campaigns keyed
**`id`**, not `_id`; `list_email_accounts` also keys accounts `id` but wraps
them in `{"accounts":[...]}`. The wrong key silently yields undefined, which
you then pass into a write.

`list_campaigns` is a token bomb: every campaign in full, including the whole
`sequences` array with raw inline-styled HTML bodies, tens of KB for one live
campaign. Always pass `limit` (1-3 while exploring) and narrow with `status`
or `campaign_type` (`parent` or `subseq`). An empty result comes back as
`{}`, not `[]`. Status values: DRAFT, ACTIVE, PAUSED, INACTIVE, COMPLETED.

Prefer a narrow read per facet: `get_campaign_status` for status,
`get_campaign_summary` for lead-funnel counts (no status field),
`get_campaign_variations` for steps, `get_campaign_email_accounts` for
senders. `list_campaigns` gives `sequence_steps` and `email_accounts_count`,
but its `camp_emails` was `[]` on a 493-account campaign: never read sender
state from that field.

## The sequences array

Inject steps with `patch_campaign_update` (`PLUSVIBE_UPDATE_CAMPAIGN`). Each
entry needs `step`, `wait_time`, and `variations[]`; each variation requires
all four of `variation`, `name`, `subject`, `body`. `body` is HTML.

**`wait_time` is a trailing gap.** It is the days to wait AFTER step N is
sent, before step N+1, never a delay before step N. Step 1 goes out at start
whatever its `wait_time`, the final step's does nothing, and the minimum is 1.
An empty `subject` on a follow-up replies into the thread, deliberate here.

Note a schema contradiction: `patch_campaign_update` labels `first_wait_time`
"Only for subsequence", yet its own `sequences` description says a non-empty
`sequences` makes it required, and live parent campaigns carry it. Send it
alongside `sequences`, then read the campaign back to confirm.

## Spintax and variables

Spintax is in production use and resolves at send time. `{{random|A|B|C}}`
picks one variant in subject or body; `{{fallback|{{first_name}}|there}}`
supplies a default; `{{sender_first_name}}` and `{{sender_signature}}` are
sender-side. Custom variables resolve from the lead's `custom_variables` and
are named by whoever created them, live campaigns here using `{{Ai_Result}}`,
`{{custom_one_line}}`, `{{custom_verticals}}`. Never assume a name, read one
lead first. Unmatched variables render empty, so wrap load-bearing ones.

## Sending accounts: three doors, two currencies

- `set_campaign_email_accounts` takes `account_list`, a list of email
  **ADDRESSES**, and **replaces** the entire set.
- `add_campaign_email_account` / `remove_campaign_email_account` take a
  single `email` address and leave the rest alone.
- `patch_campaign_update`'s `email_accounts` field takes account **IDs**.
  Addresses versus IDs is the easy mistake; `list_email_accounts` returns
  both `id` and `email` per account.

## Schedule: the write shape is not the read shape

Reads return `schedule: {days:["Monday","Tuesday",...], from_time:"07:30",
to_time:"17:00", tz:"America/New_York"}`, days spelled out. In
`set_campaign_schedule`, `daily_limit`, `start_date` and optional `end_date`
are **top-level**; `schedules` holds exactly one `{days, timezone, timing}`.

- `days` is a **true-only map**, 1=Monday through 7=Sunday, e.g.
  `{"1":true,"2":true,"3":true,"4":true,"5":true}`. The API **rejects
  `false`**; omit inactive days entirely.
- `timing` carries the daily window using the same `from_time`/`to_time` keys
  the read returns, 24h `HH:MM`. It is declared free-form, so verify after.
- `start_date` must be today or later. Past dates are rejected.

`patch_campaign_update` also accepts a `schedules` array, but nests
`daily_limit`, `daily_limit_new_lead`, `start_date`, and `end_date` *inside*
each object. Never copy a payload between the two.

## Settings worth knowing on patch_campaign_update

Booleans are asymmetric: writes take `"yes"`/`"no"` strings, reads return 0/1.

- `stop_on_lead_replied` halts the sequence for a lead who replies;
  `is_acc_based_sending` halts the whole domain once anyone there replies.
- `is_emailopened_tracking` toggles open tracking (see below);
  `is_unsubscribed_link` adds the unsubscribe link; `unsub_blocklist` pushes
  unsubscribes onto the workspace block list.
- `is_pause_on_bouncerate` plus numeric `bounce_rate_limit` auto-pauses above
  that bounce percentage.
- `exclude_ooo` keeps sending after an out-of-office reply, with `ooo_nr_opt`
  (`AI` or `MAN`), `ooo_nr_d` (fixed days when `MAN`), and `ooo_nr_ai_d`
  (fallback days when AI cannot read a return date).
- `send_as_txt` (plain text), `send_risky_email`, `is_esp_match`,
  `other_email_acc` (fallback sending), `opportunity_val` (deal value), and
  `send_priority` 0 to 1: 0 = all new leads, 1 = all follow-ups, 0.5 = even.
- `status` accepts only `ACTIVE`, `PAUSED`, `INACTIVE`. DRAFT and COMPLETED
  are read-only states you cannot write.

**Open rates are meaningless when tracking is off.** A campaign with
`is_emailopened_tracking: 0` reports `open_rate: 0` and `opened_count: 0`
whatever really happened, and real campaigns here have it off. Check the flag
first, then say "open tracking is disabled", never "0% opens".

## Safety

`launch_campaign` is Risk **Send**: it puts real cold email in front of real
people. Launches, sends, deletes, and blocklist or account admin operations are
irreversible and outward-facing, so confirm each with the user and **never
chain a send or launch automatically off a read**. `delete_campaign`,
`delete_leads`, and `delete_email_account` are unrecoverable.

## Workflows

### Launch a new campaign A to Z

1. `get_workspaces` -> take `_id`. Confirm the workspace with the user.
2. `create_campaign` (`PLUSVIBE_CREATE_CAMPAIGN`) takes only `workspace_id`
   and `camp_name`, creating an **empty DRAFT**: no sequence, schedule, or
   senders, and nothing sends until steps 3-5 supply all three. Keep its id.
3. `patch_campaign_update` with `sequences` (plus `first_wait_time`) and any
   settings above. Author bodies as HTML with spintax.
4. `list_email_accounts` for addresses, then `set_campaign_email_accounts`;
   verify with `get_campaign_email_accounts`.
5. `set_campaign_schedule`: top-level `daily_limit` and `start_date` (today or
   later), plus one schedules entry with the true-only `days` map.
6. Add leads with `add_leads_to_campaign` (`PLUSVIBE_ADD_LEADS`), confirm
   with `get_lead_count` (`PLUSVIBE_COUNT_LEADS_BY_STATUS`). Leave
   `resume_camp_if_completed` alone: true flips a COMPLETED campaign back to
   ACTIVE, so it starts sending with no `launch_campaign` call.
7. **Verify before launching.** `get_campaign_variations` returns one
   `{step, variations[]}` entry per step, so `array length == step count`
   proves the sequence landed. Each variation carries `variation`, `name`,
   `is_active` and stats, but **not** subject, body, or `wait_time`; re-read
   the campaign for those. Confirm DRAFT, accounts attached, leads loaded.
8. Show the user the assembled campaign and **ask for explicit
   confirmation**. Only then `launch_campaign` (`PLUSVIBE_LAUNCH_CAMPAIGN`),
   and confirm with `get_campaign_status`.

### A/B test, pause, resume, rename

Put two objects in one step's `variations` array with distinct `variation`
values (`"A"`, `"B"`) and a different subject or body; PlusVibe rotates them
and `get_campaign_variations` reports `sent`, `open`, `reply`, `pos_reply` per
variation, `open` being meaningless when tracking is off. `pause_campaign`
stops an ACTIVE campaign; resume with `launch_campaign`, which is Send-tier
and needs confirmation again. `set_campaign_name` renames, as does `camp_name`
on `patch_campaign_update`.

### Delete versus archive

`delete_campaign` requires **both** `is_archive` and `is_save_lead_data` as
`"yes"`/`"no"` strings: archive instead of delete, and preserve leads into a
list. Default to both `"yes"`, and get an explicit yes from the user first.

### Triage: "why did nothing send"

1. **Status.** `get_campaign_status`. DRAFT, PAUSED, INACTIVE never send.
2. **Nothing attached.** `email_accounts_count` of 0 or an empty
   `get_campaign_email_accounts` (creation attaches none), an empty
   `get_campaign_variations` (no sequence), or `get_lead_count` of 0.
3. **Schedule.** An empty `schedule: {}` means none was ever set. Check
   `start_date` is not in the past, today is in the `days` set, and the
   `timing` window has not closed in that `timezone`.
4. **Daily limits.** Two caps apply: the campaign `daily_limit` against its
   top-level `email_sent_today`, and each mailbox's `payload.daily_limit`
   against its own `payload.analytics.daily_counters.email_sent_today` in
   `list_email_accounts` (live accounts here cap at 5/day).
5. **Auto-paused on bounces.** `is_paused_at_bounced: 1` with
   `last_paused_at_bounced` set means `bounce_rate_limit` tripped. Fix
   deliverability before raising the limit.
6. **Account health.** A disconnected mailbox sends nothing, and per-account
   `status` from `list_email_accounts` is the connection state.
   `check_email_account_health` (`PLUSVIBE_CHECK_ACCOUNT_VITALS`) is a
   different check, SPF/DKIM/DMARC on the domains behind its required
   `accounts` list, and it POSTs at Risk **Admin**, so ask before running it.
