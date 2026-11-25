---
name: plusvibe-deliverability
description: Audit and fix PlusVibe cold-email deliverability - sending-account health, SPF/DKIM/DMARC records, warmup, inbox-placement tests, and the blocklist. Use before launching a campaign, when replies or inbox rates drop, when bounces spike, when sending accounts disconnect, or when adding or rotating sending domains.
---

# PlusVibe Deliverability

Sequence copy decides whether a reply happens. Sender infrastructure decides
whether the email is ever seen. This skill covers the mailbox fleet, warmup,
inbox placement, and suppression. Every tool here requires `workspace_id`, from
`get_workspaces` (`PLUSVIBE_GET_WORKSPACES`), which returns workspaces keyed
`_id`. Never carry a workspace id across a switch of brand or client.

## The two tool surfaces

MCP names are primary. The native provider (`pkg/apps/plusvibe`, AppSlug
`plusvibe`, auth via Settings -> Apps -> "PlusVibe Auth") covers only part of
this domain, and its slugs are not mechanical uppercasings:
`check_email_account_health` is `PLUSVIBE_CHECK_ACCOUNT_VITALS`, `get_blocklist`
is `PLUSVIBE_LIST_BLOCKLIST`, `bulk_assign_tags` is
`PLUSVIBE_BULK_ASSIGN_ACCOUNT_TAGS`. Read the slug from the catalog rather than
transforming the MCP name. **No native equivalent exists** for the
placement-test suite, `update_email_account`, `update_email_account_warmup`,
`mark_email_account_fixed`, or `get_email_account_stats`; those need the MCP
server or the PlusVibe UI. Say so rather than substituting another operation.

## The account fleet

`list_email_accounts` (`PLUSVIBE_LIST_EMAIL_ACCOUNTS`) returns
`{accounts: [...]}`, each account keyed **`id`**, not `_id`; reading `_id`
silently yields undefined. Top level: `email`, `status`, `warmup_status`,
`provider`, `warmup_enb_dt`. Under `payload`: `daily_limit` and `sending_gap`
(campaign throttle), a `warmup` block, `sending_rampup`, `warmup_rampup`,
`tags`, and `cmps`, the campaigns currently sending from this mailbox. Read
`cmps` before touching an account; a live campaign can lose a sender.
`payload.analytics` holds `health_scores` (`7d_overall_warmup_health`, the
Google / Microsoft / other per-provider variants, `1d_miss_warmup_rate`,
`3d_bounce_rate`) and `reply_rates` (7d..90d reply and OOO).

**`-1` means "no data", not zero.** Health scores and reply rates use `-1` as
the insufficient-data sentinel, and on live accounts here `3d_bounce_rate` is
routinely `-1` because no campaign mail went out. Never report `-1` as a rate or
call it a clean bounce record; say the window was empty.
`get_email_account_status` (`PLUSVIBE_GET_EMAIL_ACCOUNT_STATUS`) is the cheap
single-mailbox check, returning only `account`, `status`, `warmup_status`.

## Domain records

`check_email_account_health` (`PLUSVIBE_CHECK_ACCOUNT_VITALS`) takes an
`accounts` array of email **addresses** but answers per **domain**,
deduplicated: twenty mailboxes on five domains returns five rows. Rows land in
`success_list` or `failure_list` carrying `domain`, `spf`, `dkim`, `dmarc`, `mx`
(checked too, not just the three auth records), and `allPass`. Anything in
`failure_list` is a hard blocker, and DNS is fixed at the registrar, not through
this API, so report the failing record and domain and hand it back.

## Warmup

Warmup sends mail between seeded mailboxes and rescues it from spam, building
reputation before real volume; a new domain that starts cold outreach without it
lands in spam. `enable_warmup` and `pause_warmup`
(`PLUSVIBE_ENABLE_ACCOUNT_WARMUP` / `PLUSVIBE_PAUSE_ACCOUNT_WARMUP`) take an
`email` address. `bulk_update_warmup` (`PLUSVIBE_BULK_UPDATE_ACCOUNT_WARMUP`)
takes `ids` (account ids, not addresses) and a `warmup_status` of `ACTIVE` or
`INACTIVE` only, changing nothing else: it cannot set limits, ramp-up, or a
schedule, so those need `update_email_account_warmup` or
`bulk_update_email_accounts`. `update_email_account_warmup` tunes one account by
`id` and demands ten fields at once including `warmup_schedule`; there is no
partial update, so read the account first and echo current values for anything
you are not changing.

`get_warmup_stats` (`PLUSVIBE_GET_WARMUP_STATS`) is **workspace-level only**.
Its description mentions `email_acc_id`, but that parameter is not in the
schema: it takes `workspace_id`, `start_date`, `end_date` (`YYYY-MM-DD`) and
nothing else, so do not promise per-account warmup metrics. It returns an
`emailAcc` object whose percentages are **strings** (`"99.6"`) when the window
has data but numeric `0` when it is empty, so coerce before comparing, plus
per-day `chart_data`, `total_inboxes`, `total_domains`, and
`email_domain_detail` (a per-domain score map).

For sending performance use `get_email_account_stats` (dates required; optional
`email_acc_id`, `provider`, `recp_provider`, `tags`), returning
`{header, chart}` with `total_sent_count`, `total_bounce_count`, `bounce_rate`,
and reply counts. Its `open_rate` and `total_open_count` mean nothing unless
open tracking is on: campaigns with `is_emailopened_tracking: 0` report zeros
regardless of reality, so never present 0% opens as a finding without checking
that flag.

## Placement tests

A placement test sends to seed mailboxes at real providers and reports where the
mail landed, the only direct measurement of inbox versus spam. Parent tests and
runs are different objects: parent-level reads take `parent_test_id`, except
`update_email_placement_test`, which takes the same parent id as **`test_id`**,
and the delete, which takes `ids`. Runs use `test_id`.

`create_email_placement_test` takes `name` plus `type` of `AUTOMATIC`
(recurring, the default), `MANUAL`, or `ONE_OFF`, and lands in DRAFT.
`update_email_placement_test` then sets `recipient_config`, `sender_config`,
`content_config`, schedule, and throttle. Its `status` accepts only `ACTIVE` or
`INACTIVE`, never `DRAFT`; `min_intv` is required when `throttle` is
`SEQUENTIAL`, and `no_of_week` plus `days_of_week` when `frequency` is `WEEKLY`.
`get_email_placement_recipient_providers` supplies seed ids for
`recipient_config`, grouped keyed `_id` by account class, each `items` entry
carrying its own `_id` and a `recipient_type`. The live set here is
`PERSONAL_GMAIL`, `GOOGLE`, `MICROSOFT`; read it rather than assuming, since the
tool docs cite examples this account cannot use.

Find tests with `list_email_placement_tests` (optional `status` / `type`
filters, sorting, paging) and read one back with
`get_email_placement_test_detail`. Read results with
`get_email_placement_test_summary` (parent aggregate),
`list_email_placement_test_runs` then `get_email_placement_test_run_detail` or
`get_email_placement_test_stats` per run, and
`get_email_placement_test_automatic_result` per sender mailbox (`test_id` +
`sender_acc_id`). Manual tests from `create_email_placement_manual_test` read
back through `get_email_placement_manual_test_result`.
`duplicate_email_placement_test` needs `parent_test_id` and a new `name`; it
copies the configuration as-is, so re-point `sender_config` afterwards rather
than assuming it targets a new domain set. `delete_email_placement_test` needs
`ids` (parent test ids) **or** `all: "yes"`, and neither is marked required in
the schema, so a call omitting both fails rather than defaulting to something
safe. `all: "yes"` wipes every parent test in the workspace; never pass it
unless asked for exactly that, and confirm the ids either way.

## Blocklist

`get_blocklist` (`PLUSVIBE_LIST_BLOCKLIST`) returns a **bare array**, not a
wrapped object, and pages with `skip` / `limit`. Entries carry `_id` and
`value`, where `value` holds either a full address or a bare domain, so one
entry can suppress a whole company. `add_to_blocklist` and
`remove_from_blocklist` take an `entries` array of addresses or domains. This is
not just hygiene: opt-out and do-not-contact requests are a legal obligation
under CAN-SPAM and GDPR. Treat removal as destructive and confirm exact entries,
since dropping a suppression can put someone who asked to be left alone back
into a live sequence.

## Safety

Most of this domain is Risk **Admin** natively, including
`PLUSVIBE_DELETE_EMAIL_ACCOUNT` (Admin, not Delete), every bulk account
operation, and both warmup toggles. Admin and Delete operations are
confirm-first: state which mailboxes or domains are affected and how many, then
wait for a yes. Never chain a write off a read, and never launch or resume
sending as a follow-on to an audit. `PLUSVIBE_CHECK_ACCOUNT_VITALS` is the one
Admin-tiered exception safe to run unprompted: despite the tier and the POST it
only reads DNS.

- `delete_email_account` is unrecoverable and orphans every campaign listed in
  that account's `payload.cmps`.
- `bulk_assign_tags` needs `ids`, a `tag_id` from `list_tags`, and `action` of
  `ASSIGN` or `UNASSIGN`. It reshapes campaign sender pools as a side effect,
  since tag-selected campaigns update their lists automatically, so a tag edit
  can silently change who a campaign sends as.
- `bulk_reconnect_email_accounts` works only when credentials are unchanged;
  Google and Microsoft almost always need a manual UI reconnect. Try once.
- `mark_email_account_fixed` only clears the error flag, so call it after the
  real problem is resolved. With `email` omitted it applies at the API's default
  scope, so pass it.
- `update_email_account` requires `first_name`, `daily_limit`, and
  `interval_limit_in_min` on every call, so changing a signature alone still
  resends the throttle; read the account first or you will overwrite it. When
  `is_slow_rampup` is `"yes"`, `rampup_daily_limit` and `rampup_daily_inc`
  become required and their sum must not exceed `daily_limit`.
  `apply_all_sign: "yes"` writes the signature to every account on that domain,
  a fleet-wide edit wearing a single-account shape.
- `bulk_add_email_accounts` returns acceptance, not results; the real outcome
  arrives by email. Do not report the accounts as added.
- `bulk_update_email_accounts` (`PLUSVIBE_BULK_UPDATE_EMAIL_ACCOUNTS`) takes
  `ids` and writes only the fields you pass, but `daily_limit` becomes required
  once `bulk_is_slow_rampup` is set either way.

**Read shape is not write shape.** Reads expose `payload.sending_gap`,
`payload.warmup.limit`, `.increment`, `.reply_rate`; the matching writes are
`interval_limit_in_min`, `warmup_max_daily_limit`, `warmup_pace_increment`,
`warmup_reply_rate`. Live accounts report `reply_rate` as an integer percent
(35, 48) while the write parameter is documented as `0.0` to `1.0`. Confirm the
intended value instead of copying a read into a write.

## Workflows

### Pre-launch deliverability checklist

Run before `launch_campaign` (`PLUSVIBE_LAUNCH_CAMPAIGN`, Risk Send), never as
part of it.

1. `get_campaign_email_accounts` (`PLUSVIBE_GET_CAMPAIGN_EMAIL_ACCOUNTS`), so
   you audit the mailboxes the campaign will actually send from.
2. `check_email_account_health` on those addresses. Any row in `failure_list`
   stops the launch; report the failing record and domain.
3. `list_email_accounts` and confirm each sender is `status: "ACTIVE"`,
   `warmup_status: "ACTIVE"`, with `warmup_enb_dt` at least two to three weeks
   old. A domain warmed for days is not ready.
4. Check `health_scores`, flagging warmup health below about 90 and treating
   `-1` as unmeasured. Compare `payload.daily_limit` against list size; prefer
   many mailboxes at low volume over few at high volume.
5. Optionally run a placement test, then report a clear go or no-go and ask for
   confirmation. Launching is the user's call.

### Diagnosing a bounce spike

1. `get_email_account_stats` over the spike window and a comparable earlier
   window. Compare `bounce_rate`, not raw counts, since volume may differ.
2. Re-run with `email_acc_id` per suspect mailbox to tell a fleet-wide problem
   from one bad mailbox or domain.
3. Fleet-wide: run `check_email_account_health`, since an expired or newly
   edited DNS record is the usual cause. Isolated: check
   `get_email_account_status`, because a disconnected mailbox and an unhealthy
   one look alike in the stats alone.
4. Check the lead source. Bounces concentrated in one campaign usually mean an
   unverified import, not infrastructure.
5. Recommend, then act only on approval: `pause_campaign`
   (`PLUSVIBE_PAUSE_CAMPAIGN`), lower `daily_limit` on affected mailboxes, and
   `add_to_blocklist` for persistently bouncing domains.

### Rotating in new sending domains

1. Confirm DNS with `check_email_account_health` on the new addresses. Stop if
   `failure_list` is non-empty.
2. Add mailboxes with `bulk_add_email_accounts`
   (`PLUSVIBE_BULK_ADD_EMAIL_ACCOUNTS`) after confirming full SMTP and IMAP
   details with the user.
3. Enable warmup at once via `bulk_update_warmup` with `warmup_status:
   "ACTIVE"`. That call sets warmup status and nothing else, so ramp-up is a
   second write: `bulk_update_email_accounts` with
   `bulk_warmup_is_slow_rampup`, `warmup_initial_daily_limit`, and
   `warmup_pace_increment`, or the `enable_warmup_rampup` fields at add time.
   Volume should climb, not start flat.
4. Wait two to three weeks minimum before campaign traffic, tracking
   `get_warmup_stats` for `spam_percent` and per-day `chart_data`. Do not
   shortcut this because the user is impatient; state the risk plainly.
5. Tag the cohort with `bulk_assign_tags`, passing a `tag_id` from `list_tags`
   (`PLUSVIBE_LIST_TAGS`) and `action: "ASSIGN"`.
6. Retire old domains gradually: lower `daily_limit` over several days and check
   `payload.cmps` so no campaign is left without senders. Swap senders with
   `set_campaign_email_accounts`, whose `account_list` takes email **addresses**
   and **replaces** the whole pool (`patch_campaign_update`'s `email_accounts`
   takes account **ids** instead), or one at a time with
   `add_campaign_email_account` / `remove_campaign_email_account`.
