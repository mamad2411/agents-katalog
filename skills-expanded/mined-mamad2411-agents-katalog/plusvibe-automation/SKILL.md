---
name: plusvibe-automation
description: Build PlusVibe automation and org structure - reply-triggered subsequences, webhooks into Caeros or Slack, tags, holiday calendars, workspaces, and agency client sub-accounts. Use when the user wants a campaign to branch on replies or labels, wants PlusVibe events pushed somewhere, or is setting up a new workspace or client.
---

# PlusVibe Automation

Two tool surfaces reach the same account; use whichever is connected. The
**remote MCP** (`https://mcp.plusvibe.ai/mcp`) uses lower_snake_case names such
as `create_subsequence`, which is what this skill names. The **native Caeros
provider** (AppSlug `plusvibe`) uses UPPER_SNAKE slugs such as
`PLUSVIBE_GET_WORKSPACES` and `PLUSVIBE_UPDATE_CAMPAIGN`, authed at Settings ->
Apps -> "PlusVibe Auth", one API key spanning every workspace. Resolve any slug
not named here from the app's operation list; never invent a tool.

Every tool here takes `workspace_id` except `get_workspaces`, which takes no
parameters at all. `get_workspaces` returns workspaces keyed `_id`, but campaigns
from `list_campaigns` (`PLUSVIBE_LIST_ALL_CAMPAIGNS`) are keyed `id`; the wrong
key silently yields undefined. Webhooks, tags, and calendars never cross
workspaces.

## Safety

This plugin sends real cold email to real people.

- `launch_campaign` (`PLUSVIBE_LAUNCH_CAMPAIGN`) is Risk **Send**. Confirm
  before every launch and never chain one off a read.
- `delete_campaign`, `delete_client`, `delete_tag`, `delete_webhook`, and
  `delete_custom_holiday_calendar` are unrecoverable. Say exactly what
  disappears, then wait for a yes. `delete_campaign` also requires `is_archive`
  and `is_save_lead_data` (`yes`/`no`); offer `is_archive: "yes"`, which archives
  instead of deleting. Prefer `set_client_status` `INACTIVE` to `delete_client`.
- `delete_tag` and `bulk_assign_tags` change which mailboxes campaigns send
  from. Treat both as sending changes, not bookkeeping.

## Subsequences

A subsequence is PlusVibe's branching primitive: a follow-up campaign leads enter
automatically on an event in a parent campaign. **It is itself a campaign**,
returned by `list_campaigns` with `campaign_type: "subseq"` (regular campaigns
are `parent`), a `parent_camp_id`, and its own `sequences`, `schedule`, `status`.

### Creating one

`create_subsequence` takes exactly four fields: `workspace_id`, `name`,
`parent_camp_id`, `events`. It does **not** accept sequences, wait times, or a
schedule; those need a second `patch_campaign_update` (`PLUSVIBE_UPDATE_CAMPAIGN`)
call, where `ignore_mailbox_limit` is subsequence-only. Four entry events:

- `LEAD_LABEL_UPDATED` - needs `val`, an array of labels.
- `LEAD_REPLY_CONTENT` - needs `include_text`, plus `exclude_text`.
- `LEAD_REPLY_ALL` - no extra fields.
- `LEAD_REPLY_ALL_EXCEPT_OOO_AUTOMATIC_REPLY` - no extra fields.

Every label in `val` **must** start with `LEAD_MARKED_AS_`, for example
`LEAD_MARKED_AS_INTERESTED` or `LEAD_MARKED_AS_OUT_OF_OFFICE`; labels without
that prefix are rejected. For `LEAD_REPLY_CONTENT`, `include_text` and
`exclude_text` are comma-separated phrase lists in one string; the schema
contradicts itself on whether `exclude_text` is optional, so always send it.

`first_wait_time` is the delay in days before the subsequence sends its first
step, counted from when the lead enters. It is **not** settable on
`create_subsequence`; set it with `patch_campaign_update` afterwards. Passing a
non-empty `sequences` array there makes `first_wait_time` required in the same
call, so send both together. Inside `sequences`, `wait_time` on step N is the gap
AFTER step N is sent, so it controls the delay before step N+1; the final step's
`wait_time` does nothing and the minimum is 1.

### Reading one back, and moving leads in

`get_campaign_summary` returns counts only, never `events`, `first_wait_time`, or
`campaign_type`. Only `list_campaigns` surfaces those, and it is a token bomb
because it inlines every campaign's full HTML bodies. Always scope it: pass
`campaign_id` for the one subsequence, or `campaign_type: "subseq"` with a small
`limit`. To confirm only that steps landed, `get_campaign_variations` returns one
entry per step and no bodies: pass the subsequence as `campaign_id` and the
parent as `parent_campaign_id`.

`add_leads_to_subsequence` takes `workspace_id`, `subseq_id`, and
`parent_lead_ids`, which must already exist in the parent campaign, so source
them from `list_all_leads` filtered by the parent's `campaign_id`. Confirm the
count and the parent first: this puts real people into a sending sequence.

## Webhooks

`create_webhook` requires `workspace_id`, `url`, `camp_ids`, `event_types`.
Optional: `name`, `secret`, `is_slack`, `ignore_ooo`, `ignore_automatic`.

- `camp_ids: ["ALL"]` covers every campaign in the workspace, present and future.
  Otherwise pass specific campaign ids.
- `event_types` accepts `ALL_EMAIL_REPLIES` and any `LEAD_MARKED_AS_*` label,
  including custom ones. Production hooks on this account also use
  `FIRST_EMAIL_REPLIES`, which the schema does not document.
- `ignore_ooo`, `ignore_automatic`, and `is_slack` are each `1` or `0`. The first
  two only matter for reply events: set both to `1` for anything routed to a
  human. `is_slack` changes the payload format for Slack.

**Read shape differs from write shape.** `list_webhooks` returns
`{ "hooks": [...] }` where each hook has `_id`, `evt_types` (not `event_types`),
`integration_type` (not `is_slack`), plus `status`, `last_run`, and `last_resp`.
It also echoes `secret` back in plaintext, so never paste a returned secret into
chat, a summary, or a log. There is no update tool: to change a hook,
`delete_webhook` (takes an `ids` array) and recreate.

## Tags

Tags label email accounts and campaigns, and campaigns can select sending
mailboxes by tag. `create_tag` requires `name` and `color` (hex, 3 or 6 digits)
plus an optional `description`; names are case-insensitive and unique per
workspace. `list_tags` returns a bare array of `_id`, `name`, `color`,
`description`, `status`, and usage counts `ea_count` and `camp_count`.
`update_tag` requires `tag_id`, `name`, and `color` together, so there is no
partial edit: read first and resend unchanged fields, `description` included.

`bulk_assign_tags` takes `ids`, `tag_id`, and `action` of `ASSIGN` or `UNASSIGN`.
Despite `camp_count` existing, `ids` are **email account** ids only. Unassigning
drops those mailboxes out of any campaign selecting by that tag, which changes
live sending. `delete_tag` takes an `ids` array and cascades: it strips the tag
from every email account and campaign, and rewrites affected campaigns' email
account lists. Quote `ea_count` and `camp_count` before confirming.

## Custom holiday calendars

`add_custom_holiday_calendar` takes `name` and `holidays`, an array of
`{ name, date }` with `YYYY-MM-DD` dates. `get_custom_holiday_calendars` returns
a bare array of them. `update_custom_holiday_calendar` takes `_id`, `name`, and a
`holidays` array that **replaces** the existing list wholesale, so read first and
resend every entry you keep. `delete_custom_holiday_calendar` takes `_id`.
Campaigns carry `holiday_cal_id`, `holiday_cal_type`, and `skip_cal_holiday`,
visible via `list_campaigns`, but no API tool attaches a calendar to a campaign:
neither `patch_campaign_update` nor `set_campaign_schedule` has a holiday field.
Create the calendar, then have the user attach it in the campaign's schedule
settings in the UI.

## Workspaces and clients

`create_workspace` takes `workspace_name` plus a `workspace_id` that is **any
existing workspace, used purely to authenticate the API key**: not a parent, and
the new workspace is not nested under it. Clients are external sub-accounts with
scoped access, the agency pattern. `add_client` requires `client_email`,
`client_first_name`, `client_last_name`, `client_business_name`, and
`workspaces`; last and business name may be empty strings but must be present,
and `notify_pos_reply_email` is an optional comma-separated address list. Each
`workspaces` entry is `{ id, permissions, hide_labels }`; `hide_labels` must be
present even when empty and holds lead labels to hide, such as `IN_SEQUENCE`.
Production permissions are the `CAMPAIGN_*`, `EMAILACCOUNT_*`, `TAG_*`,
`BLOCKLIST_*`, and `TEMPLATE_*` families, each with `_CREATE`, `_EDIT`, `_LIST`,
and `_DELETE`, plus `HOOK_CREATE`.

`list_clients` returns `{ "clients": [...] }` keyed `client_id`, with grants
under `client_permissions` and the workspace keyed `workspace_id`, while the
write shape uses `workspaces` with `id`; reads also give `first_name` and
`last_name` where writes want `client_first_name` and `client_last_name`. Remap
both before feeding a read into a write. `update_client` needs `client_id` plus
all three name fields, and **replaces** the grant list, so resend everything the
client keeps. `set_client_status` flips `ACTIVE`/`INACTIVE`.

## Workflows

### Build a reply-triggered subsequence
1. `get_workspaces` for `_id`, then `list_campaigns` scoped by `campaign_id` or a
   small `limit` to get the parent's `id`.
2. `create_subsequence` with `parent_camp_id` and the trigger: for "anyone who
   replies, minus autoresponders" use
   `events: [{"name": "LEAD_REPLY_ALL_EXCEPT_OOO_AUTOMATIC_REPLY"}]`.
3. `patch_campaign_update` on the returned subsequence id, sending `sequences`
   and `first_wait_time` together. Show the copy to the user first.
4. `set_campaign_schedule`, which requires `daily_limit` and a `start_date` of
   today or later alongside exactly ONE object in `schedules`. That object
   needs `days` as a true-only map (`{"1":true,...}`, 1=Monday..7=Sunday; the
   API rejects `false`, so omit inactive days), `timezone`, and `timing`.
5. Confirm the steps with `get_campaign_variations`, then `list_campaigns` scoped
   to that `campaign_id` for `events` and `first_wait_time`. Reads echo
   `schedule` as day names plus `from_time`/`to_time`/`tz`, not the map you
   wrote. Ask before `launch_campaign`.

### Wire replies into Slack
1. Get the destination URL from the user: a Slack incoming webhook, or the Caeros
   workflow endpoint.
2. `create_webhook` with `camp_ids: ["ALL"]`, `event_types` of
   `["ALL_EMAIL_REPLIES"]`, `ignore_ooo: 1`, `ignore_automatic: 1`, and
   `is_slack: 1` for Slack. Add a `secret` for non-Slack endpoints so the
   receiver can verify payloads.
3. Verify with `list_webhooks`, reading `evt_types`, not `event_types`. To
   narrow scope later, `delete_webhook` and recreate: there is no update.

### Stand up a new client workspace
1. `create_workspace` with the new name and any existing workspace id for
   auth, then re-run `get_workspaces` to pick up the new `_id`.
2. Add email accounts and campaigns there first, so the client does not log
   into an empty shell.
3. `add_client` granting only the new workspace's id, the permission set the
   user approves, and `hide_labels` for internal-only labels. Confirm via
   `list_clients` that `client_permissions` lists that workspace and no other.
