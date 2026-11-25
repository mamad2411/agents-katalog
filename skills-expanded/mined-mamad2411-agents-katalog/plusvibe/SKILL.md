---
name: plusvibe
description: Drive PlusVibe cold-email outreach through the PlusVibe MCP server or the native Caeros PlusVibe app - workspaces, campaigns, sequences, leads, sending mailboxes, unibox replies, and analytics. Use whenever the user mentions PlusVibe, cold email, outreach campaigns, sequence steps, mailbox warmup, or their unibox, and route from here to the specialist plusvibe-* skills.
---

# PlusVibe

PlusVibe (plusvibe.ai) is a cold-email outreach platform: leads go into a
campaign, the campaign sends a multi-step email sequence from a pool of
mailboxes, and replies land in a shared unibox. This skill is the entry point
for every PlusVibe request. Orient here, then hand off to a specialist skill.

**These tools send real email to real people.** Read the safety rail before
any write.

## Step 0: find the surface

Two surfaces exist and they do not share a naming convention.

1. **MCP server** at `https://mcp.plusvibe.ai/mcp?api_key=KEY` (Streamable
   HTTP). Tool names are lower_snake_case: `get_workspaces`, `list_campaigns`,
   `add_leads_to_campaign`. This is the primary surface, and every tool named
   in these skills is an MCP name.
2. **Native Caeros app provider**, AppSlug `plusvibe`, 70 operations with
   UPPER_SNAKE slugs: `PLUSVIBE_GET_WORKSPACES`,
   `PLUSVIBE_LIST_ALL_CAMPAIGNS`. The native slug appears in parentheses the
   first time a tool is used in a workflow.

Check which one is connected before planning. If neither is, say exactly that
and stop. Do not fall back to web search, hand-roll a REST call, or invent
tool names. The surfaces do not cover the same ground: per-variation campaign
stats, inbox-placement tests, custom holiday calendars, `send_new_email`, and
the campaign email-account setters exist only on the MCP. If a tool you need
has no native slug, say so instead of substituting a different operation.

## Connecting

- **Native provider**: Settings -> Apps -> "PlusVibe Auth", paste the API key.
  One key covers every workspace on the account.
- **MCP**: register `https://mcp.plusvibe.ai/mcp?api_key=YOUR_KEY` as a
  Streamable HTTP server. The MCP requires a PlusVibe Business plan.
- Get the key from PlusVibe's own API settings. Never echo a key back into the
  transcript, a file, or a URL you show the user.

`get_workspaces` (`PLUSVIBE_GET_WORKSPACES`) doubles as the key test: it hits
`/authenticate` and returns the workspaces the key can reach. A failure there
is an auth problem, not a data problem.

## The mental model

- **Workspace** is the unit of isolation. Leads, campaigns, mailboxes, tags,
  the blocklist, and webhooks all live inside one workspace and never cross.
- **Campaign** holds the sequence, the schedule, the sending mailboxes, and
  the leads. `campaign_type` is `parent` or `subseq`. `status` is one of
  DRAFT, ACTIVE, PAUSED, INACTIVE, COMPLETED.
- **Sequence** is an ordered array of steps, each with one or more
  `variations` (A/B) carrying a `subject` and an HTML `body`, plus a
  `wait_time`: the gap AFTER that step sends, never a delay before it, so the
  final step's `wait_time` does nothing. Minimum 1 (days).
- **Leads** carry `email`, name and company fields, and a `custom_variables`
  bag that the sequence interpolates.
- **Email accounts** are the sending mailboxes, each with its own daily limit
  and warmup state. A campaign draws from a pool of them.
- **Unibox** is the shared inbox where replies arrive.
- **Subsequences** are child campaigns triggered by an event on the parent and
  carry `parent_camp_id` plus `first_wait_time` in days.

## Workspace first, always

Nearly every tool requires `workspace_id`. Resolve it before anything else.

1. Call `get_workspaces`. It takes no arguments.
2. If exactly one workspace comes back, use it.
3. If several come back and the user did not name one, ask which. Do not guess
   by name similarity. Several workspaces on the same account routinely have
   near-identical names, and sending into the wrong one is not recoverable.
4. Carry that id through the whole task. Never mix ids from two workspaces in
   one report.

## ID discipline

`get_workspaces` returns workspaces keyed **`_id`**. `list_campaigns`
(`PLUSVIBE_LIST_ALL_CAMPAIGNS`) returns campaigns keyed **`id`**, not `_id`.
Reading the wrong key yields undefined silently, and you end up passing an
empty `campaign_id`. Check the key name on every response shape.
Containers differ too: `list_campaigns` returns a bare array and answers a
query that matches nothing with `{}` rather than `[]` (no matches, not an
error), while `list_email_accounts` wraps its rows in `{"accounts": [...]}`.

## list_campaigns is a token bomb

`list_campaigns` returns every matching campaign in FULL, including the whole
`sequences` array with raw inline-styled HTML bodies. A single production
campaign can be tens of kilobytes.

- Always pass `limit` (1 to 5 unless you genuinely need more), and narrow with
  `status`, `campaign_type`, or `campaign_id`.
- When you need one facet only, use the narrow reader:
  `get_campaign_summary` (`PLUSVIBE_GET_CAMPAIGN_SUMMARY`) for lead-level
  counts, `get_campaign_status` (`PLUSVIBE_GET_CAMPAIGN_STATUS`) for a
  two-field status check, `get_campaign_variations` for the per-step and
  per-variation breakdown without any bodies.
- Pull the full listing only when sequence copy is actually the question.

## Never report open rates blind

`open_rate` and `opened_count` read 0 whenever `is_emailopened_tracking` is 0
on the campaign, regardless of what really happened, and real campaigns on
this account run with tracking off. Check that flag before saying anything
about opens, and report "open tracking is off" rather than "0% opens". Sent,
reply, and bounce counts are unaffected.

## Tool families and where to go

| The user wants | Skill |
|---|---|
| Campaigns, sequence copy, spintax, schedule, launch | `plusvibe-campaigns` |
| Add, find, filter, label, clean leads and custom vars | `plusvibe-leads` |
| Performance numbers, per-step stats, rollups | `plusvibe-analytics` |
| Reading and answering replies in the unibox | `plusvibe-inbox` |
| Mailboxes, warmup, health, blocklist, placement | `plusvibe-deliverability`|
| Subsequences, webhooks, tags, client access | `plusvibe-automation` |

## Safety rail

These are confirm-first every single time. Never chain one off the back of a
read, and never batch several on one approval.

- **`launch_campaign` (`PLUSVIBE_LAUNCH_CAMPAIGN`)** is Risk Send. It starts
  real cold email to real inboxes. State the campaign name, lead count, daily
  limit, schedule, and step count, then wait for a yes.
- **Unibox sends** (`reply_to_email`, `forward_email`, `compose_new_email`,
  `send_new_email`) are Risk Send. Show the exact recipient, sender mailbox,
  subject, and body first. `save_email_as_draft` is the safe rehearsal.
- **Deletes are unrecoverable**: `delete_campaign`, `delete_leads`,
  `delete_email_account`, `delete_email_thread`, `delete_email_message`,
  `delete_webhook`, `delete_tag`. Name what disappears and how many rows.
- **Admin operations** on mailboxes, warmup, blocklist, clients, and webhooks
  change sending behaviour across the whole workspace. Confirm those too.
- Reads are free. `pause_campaign` is the safe stop; prefer pausing to
  deleting, and offer it whenever the user asks to "stop" something.

## Workflows

### First five minutes in a new workspace

Pure reads. Nothing here touches state.

1. `get_workspaces`. Note each `_id` and `name`, and confirm the target with
   the user when more than one comes back.
2. `get_lead_count` (`PLUSVIBE_COUNT_LEADS_BY_STATUS`) with just
   `workspace_id`. One call gives the whole funnel: NOT_CONTACTED, CONTACTED,
   COMPLETED, REPLIED, RESCHEDULED, UNSUBSCRIBED, BOUNCED, SKIPPED.
3. `list_campaigns` with `limit: 5` and `status: "ACTIVE"`. Read `id`,
   `camp_name`, `status`, `lead_count`, `sent_count`, `replied_count`,
   `bounced_count`, `is_emailopened_tracking`, `schedule`, `sequence_steps`.
   Ignore the `sequences` payload.
4. `list_email_accounts` (`PLUSVIBE_LIST_EMAIL_ACCOUNTS`) with `limit: 5`.
   Confirms sending capacity exists. Zero accounts means the workspace cannot
   send at all, which explains most "why is nothing going out" questions.
5. `get_unread_email_count` (`PLUSVIBE_GET_UNREAD_EMAIL_COUNT`) to see whether
   replies are waiting.

Report: workspace, active campaigns with their funnel, mailbox count and
warmup state, unread replies. Flag anything obviously wrong (no mailboxes, an
ACTIVE campaign with an empty `schedule`, bounces above the campaign's
`bounce_rate_limit`) and stop there. Do not fix it unasked.

### Routing a vague request

1. Resolve the workspace.
2. If the user named a campaign in words rather than by id, map name to id
   with `list_campaigns` using a small `limit` plus a `status` filter. Never
   guess an id, and never assume a name is unique.
3. Pick the specialist skill from the table above and follow it. Come back
   here only when the request spans families.

## Working practices

- **Read before you write.** Fetch the campaign's current state before
  patching it. `patch_campaign_update` (`PLUSVIBE_UPDATE_CAMPAIGN`) is a true
  PATCH, so omitted fields keep their values, but you still need to know what
  you are changing and what it will start sending. Its `email_accounts` takes
  account IDs; `set_campaign_email_accounts` takes email ADDRESSES.
- **Report only what a tool returned.** No inferred rates, no filled gaps.
  If a field came back empty, say it was empty.
- **Paginate deliberately.** `list_campaigns` and `list_email_accounts` take
  `skip`/`limit`, `list_all_leads` (`PLUSVIBE_FETCH_WORKSPACE_LEADS`) takes
  `page`/`limit`, and `get_emails` takes an opaque `page_trail` cursor. Fetch
  one page, decide if it answers the question, and say when you truncated.
- **Dates are YYYY-MM-DD** on every stats and schedule tool.
