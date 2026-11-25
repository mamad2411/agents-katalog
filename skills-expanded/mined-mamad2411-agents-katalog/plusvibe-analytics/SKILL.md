---
name: plusvibe-analytics
description: Pull and interpret PlusVibe cold-email numbers - sends, replies, positive replies, bounces, unsubscribes, per-step and per-variation stats, and lead status counts - and turn them into an honest read of campaign health. Use whenever the user asks how a PlusVibe campaign or workspace is performing, wants a report or a comparison, or asks why replies, opens, or sends dropped.
---

# PlusVibe analytics

Reporting on PlusVibe cold-email performance. For creating, editing,
scheduling, or launching campaigns, use `plusvibe-campaigns`. Two tool
surfaces are valid: the remote MCP at `https://mcp.plusvibe.ai/mcp` with
lower_snake_case names (primary naming below), and the native Caeros app
provider (AppSlug `plusvibe`) with UPPER_SNAKE slugs, authed at Settings ->
Apps -> "PlusVibe Auth". `get_workspaces` (`PLUSVIBE_GET_WORKSPACES`) is the
one call taking no arguments at all; every other call here requires
`workspace_id`. Resolve it once, read it off the `_id` key, and ask which
workspace if the user did not name it. The wrong workspace returns plausible,
wrong numbers.

## Seven doors onto the same numbers

| You need | Call | Cost |
|---|---|---|
| One campaign, lifetime totals | `get_campaign_summary` (`PLUSVIBE_GET_CAMPAIGN_SUMMARY`) | cheapest |
| Every campaign in the workspace, raw counts | `get_campaign_stats` (`PLUSVIBE_GET_CAMPAIGN_STATS`) | medium |
| Rates plus a daily time series | `get_campaign_detailed_stats` (MCP only) | heavy |
| Send and contact volume over a range | `get_campaign_analytic_count` (`PLUSVIBE_GET_CAMPAIGN_COUNT`) | light |
| One workspace-wide rollup | `get_analytics_stats` (`PLUSVIBE_GET_ALL_CAMPAIGN_STATS`) | light |
| Leads broken down by status | `get_lead_count` (`PLUSVIBE_COUNT_LEADS_BY_STATUS`) | light |
| Per-step and per-variation stats | `get_campaign_variations` (MCP only) | light |

Detailed stats and variations are MCP-only; do not invent a native slug.

Required arguments differ, and that is the usual first error:
`get_campaign_summary` takes no dates at all; `get_campaign_stats` and
`get_campaign_analytic_count` require `start_date` with `end_date` optional;
`get_campaign_detailed_stats` and `get_analytics_stats` require **both**.
`get_analytics_stats` returns one flat object for the whole workspace, no
per-campaign breakdown and no rates.

`get_campaign_detailed_stats` is the only tool returning computed rates. It
returns `{header, chart}` with `chart` one row per day, so a 209-day window
came back as 75 KB across 2,763 lines and overflowed the tool output limit.
Keep windows to a month or less. It also takes optional `campaign_id`
(omit for the workspace aggregate), `parent_campaign_id`, `status`, `tags`,
`recp_provider`, and `cache`. **The `status` filter has two traps.** In
workspace-aggregate mode it matches current status, not status during the
window: a campaign that sent 300 on 6 Jan and is PAUSED today returns zeros
under `status: "ACTIVE"` and the real 300 under `status: "PAUSED"`. With
`campaign_id` set the filter is ignored outright, so that same PAUSED campaign
returns full numbers under `status: "DRAFT"`. Never treat `status` as evidence
a campaign was or was not running. Live stats rows also carry `ARCHIVED`,
beyond DRAFT, ACTIVE, PAUSED, INACTIVE, and COMPLETED.

## Field names change from tool to tool

The same quantity has a different key in almost every response, so never carry
a key across tools.

| Quantity | summary | stats | detailed header | analytic_count |
|---|---|---|---|---|
| leads contacted | `contacted` | `lead_contacted_count` | `total_contacted_count` | `new_leads_contacted` |
| emails sent | `total_sent_emails` | `sent_count` | `total_sent_count` | `total_emails_sent` |
| replies | `leads_who_replied` | `replied_count` | `total_reply_count` | `leads_replied` |
| bounces | `bounced` | `bounced_count` | `total_bounce_count` | not returned |
| positive replies | `positive_reply_count` | `positive_reply_count` | `total_pos_reply_count` | not returned |

Campaign ids move too: `get_campaign_stats` rows are keyed `_id`, while
`list_campaigns` (`PLUSVIBE_LIST_ALL_CAMPAIGNS`) keys campaigns `id` and
`get_campaign_summary` / `get_campaign_analytic_count` return `campaign_id`.
`get_lead_count` sidesteps all of it, returning `{status, count}` over eight
statuses: NOT_CONTACTED, CONTACTED, COMPLETED, REPLIED, RESCHEDULED,
UNSUBSCRIBED, BOUNCED, SKIPPED. Pass `campaign_id` to scope it.

## Which tool to believe when they disagree

Verified on one live campaign, one window, all four tools back to back:

| Metric | Trust | Because |
|---|---|---|
| Bounces | summary, detailed | both said 43, `get_campaign_stats` said 0 |
| Opens | detailed, `list_campaigns` | both said 0, while stats' `unique_opened_count` was 109, exactly its own `replied_count` |
| Replies | summary, stats, detailed | all said 109; `get_campaign_analytic_count` said `leads_replied: 0`, so use it for volume only |

## Date-scoped versus lifetime

`get_campaign_stats` mixes both in one object. `sent_count`,
`lead_contacted_count`, and `replied_count` respect the date range;
`lead_count` and `completed_lead_count` are lifetime and ignore it;
`new_lead_contacted_count` and `new_completed_lead_count` are window deltas.
`bounced_count` is in neither camp: it read 0 on every window tried live, one
of which showed 12 bounces in detailed stats. A 2025 campaign therefore shows
`lead_count: 1743` next to `sent_count: 0` for a 2026 window, which is not a
bug. `completed_lead_count` can also exceed `lead_count` (4,057 against 1,124
live), so never compute "completion %" from it. `get_campaign_summary` has no
dates; it is all lifetime. `get_analytics_stats` returns this same key set as
one flat object, broken `bounced_count` included.

## Interpretation

**Open rate is structurally zero when tracking is off.** A campaign with
`is_emailopened_tracking: 0` returns `open_rate: 0`, `opened_count: 0`, and
`total_open_count: 0` regardless of what really happened, and real production
campaigns here have it off. The flag lives only on `list_campaigns`, so read
it with `campaign_id` and `limit: 1` before you mention opens. Say "open
tracking is disabled, so opens are not measured", never "0% opens".

**Reply rate is the real signal.** `reply_rate` in the detailed header is
replies over contacted leads (109 / 3,528 = 3.1) and it **excludes**
out-of-office replies, counted separately as `total_ooo_reply_count`;
`reply_rate_with_ooo` is the inflated version (126 / 3,528 = 3.6). Report
`reply_rate`, treat OOO as a deliverability signal, and note that
`list_campaigns` calls the lifetime version `replied_rate`.

**`pos_reply_rate` is a share of replies, not of sends.** 71 of 109 replies is
`pos_reply_rate: 65.1`. Positive replies over emails sent is a different
number (about 2%) and usually what users mean, so state the denominator.

**Sentiment buckets do not sum to replies.** `list_campaigns` returns
`positive_reply_count`, `negative_reply_count`, and `neutral_reply_count`
separately; live these were 71, 0, and 0 against 109 replies, leaving 38
unclassified. Never present a split as if the three buckets partition replies.

**Bounce rate has a hard consequence.** `bounce_rate` is bounces over
contacted (43 / 3,528 = 1.2). When `is_pause_on_bouncerate` is 1, crossing
`bounce_rate_limit` auto-pauses the campaign, and `is_paused_at_bounced: 1`
with `last_paused_at_bounced` set is the fingerprint. Live campaigns here use
limits of 4 and 5, so flag anything past 2 to 3 percent early.

**Sent and leads are different units.** `sent_count` counts emails,
`lead_count` counts people, and a multi-step sequence sends several emails per
lead, so sent can exceed leads. Sent can also sit under contacted, and the two
tools disagree about it: summary returned `total_sent_emails: 3523` against
`contacted: 3528` where stats put both at 3,528. Use `lead_contacted_count`
for coverage.

**`opportunity_val` is manually set**, the deal value someone attached via
`patch_campaign_update`, named `total_opportunity_amt` in detailed stats. It
is 0 on every campaign here, so do not report pipeline value from it.

## Safety

Analytics work is read-only and must stay that way; never chain a write off a
report. `launch_campaign` is Risk **Send**: it puts real cold email in front
of real people. If a finding suggests pausing, relaunching, or deleting
anything, say so and get an explicit yes in the same turn before calling it.
`delete_campaign`, `delete_leads`, `delete_email_account` cannot be undone.

## Workflows

### Weekly campaign health report

1. `get_workspaces` for the `_id`, and confirm the workspace.
2. `get_campaign_detailed_stats` over a 7-day window with no `campaign_id` for
   the header and daily chart, then `get_campaign_stats` on the same dates for
   the per-campaign breakdown, ranked by `replied_count`.
3. Per campaign, `list_campaigns` with `campaign_id` and `limit: 1` for
   `is_emailopened_tracking`, `bounce_rate_limit`, `is_paused_at_bounced`,
   `last_lead_sent`, `last_lead_replied`, plus `get_lead_count` for funnel.
4. Report sent, contacted, `reply_rate`, positive replies with both
   denominators, `bounce_rate` against the campaign's own limit, and
   unsubscribes. Say plainly where opens are not measured, and flag any ACTIVE
   campaign whose `last_lead_sent` predates the window.

### Compare two campaigns fairly

1. Use the **same** `start_date` and `end_date` for both, via two
   `get_campaign_detailed_stats` calls with `campaign_id` set. Lifetime
   summaries are not comparable when the campaigns started months apart.
2. Compare `reply_rate` and `pos_reply_rate`, never `open_rate`, and confirm
   both carry the same `is_emailopened_tracking` value before comparing
   anything open-related at all.
3. Check volume parity. 100 sends against 3,500 is not comparable on rate
   alone; say how thin the smaller sample is rather than crowning a winner.
4. Check `stop_on_lead_replied`, `is_acc_based_sending`, `send_as_txt`, and
   `sequence_steps` from `list_campaigns`. Different settings mean you are
   comparing configurations, not copy.
5. Inside one campaign use `get_campaign_variations`, which returns `sent`,
   `open`, `reply`, and `pos_reply` per variation per step. On a live A/B, A
   took 45 replies on 1,766 sends and B took 56 on 1,762. Guard the division:
   one step returned `sent: 0` with `reply: 5`, so skip 0-send variations.

### Diagnose a drop in replies

Walk in order, stop at the first hit, and separate "we stopped sending" from
"they stopped answering" before anything else.

1. `get_campaign_detailed_stats` over the last 30 days and read the `chart`
   day by day. If `total_sent_count` fell first this is a sending problem, not
   a copy problem; hand off to the triage ladder in `plusvibe-campaigns`.
2. If sends held and `total_reply_count` fell, check `total_bounce_count` and
   `bounce_rate` on the same chart. Rising bounces mean list quality or
   deliverability, and replies fall with them.
3. Check `is_paused_at_bounced` and `last_paused_at_bounced` on
   `list_campaigns`. An auto-pause explains a cliff exactly.
4. Compare `total_ooo_reply_count` against `total_reply_count`. A window that
   is mostly OOO is a calendar effect, not a decline.
5. `get_campaign_variations` to see whether one variation or step carries the
   loss, and whether a step went `is_active: false`.
6. Check whether the mix changed. `send_priority` shifts new leads versus
   follow-ups, and a campaign that has exhausted its NOT_CONTACTED pool
   (`get_lead_count`) is sending follow-ups only.
7. Only then look at copy, and say which of the above you ruled out.
