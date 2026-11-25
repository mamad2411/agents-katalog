---
name: plusvibe-leads
description: Import, read, personalize, relabel, and remove leads in PlusVibe cold-outreach campaigns, covering bulk and single adds, the dedupe and skip flags, custom variables, status and label lookups, and safe deletes. Use whenever the user wants to load a list into a PlusVibe campaign, look up or count leads, fix personalization, or clean a bad segment.
---

# PlusVibe Leads

Everything that touches lead records inside a PlusVibe workspace. Every lead
call needs a `workspace_id`; only `add_leads_to_campaign`, `add_single_lead`,
and `update_lead_status` also require `campaign_id`, which elsewhere is an
optional scope filter. Resolve the workspace with `get_workspaces`
(`PLUSVIBE_GET_WORKSPACES`) and the campaign with `list_campaigns`
(`PLUSVIBE_LIST_ALL_CAMPAIGNS`), always with a small `limit`: that tool returns
every campaign's full sequence bodies as raw HTML and will flood the context.

Remote MCP tools are lower_snake_case (`add_leads_to_campaign`). The native
Caeros app provider `plusvibe` exposes the same operations as UPPER_SNAKE
slugs (`PLUSVIBE_ADD_LEADS`), authorized under Settings -> Apps -> "PlusVibe
Auth", where one API key spans all workspaces. Where a native slug is not
written out here, read it from the provider's operation list. Never guess one.

## The ID trap

Reading the wrong key yields undefined silently, with no error.
`get_workspaces` keys workspaces `_id`. `list_campaigns` keys campaigns `id`,
not `_id`. `list_all_leads` keys lead documents `_id`. `find_lead_by_email`
returns a wrapper keyed `id` with the full document nested under `lead_data`
(itself keyed `_id`); the wrapper also carries `contact` (the email),
`campaign`, `campaign_name`, `status`, `email_opened`, `email_replied`.
`assign_lead_to_member` and `add_leads_to_subsequence` want lead `_id`
values, not email addresses.

## The standard field set

`add_single_lead` declares `email` (required) plus `first_name`, `last_name`,
`company_name`, `company_website`, `phone_number`, `linkedin_person_url`,
`linkedin_company_url`, `address_line`, `city`, `state`, `country`,
`country_code`, `job_title`, `industry`, `department`, and `notes`. It alone
also carries `hubspot_sync` and `hubspot_field_mapping`.
`add_leads_to_campaign` declares a narrower per-lead schema that omits
`state`, `job_title`, `industry`, and `department`, but accepts additional
properties, so those keys still pass through onto the stored record. Send
them, then verify with `find_lead_by_email` rather than assuming.

## Custom variables

The two add tools differ. `add_leads_to_campaign` sets
`additionalProperties: true` on each lead object, so it takes them either in a
`custom_variables` object or as extra top-level keys. `add_single_lead` sets
`additionalProperties: false`, so unknown top-level keys are rejected outright
there: put them in `custom_variables`.

They do not read back the way they are written. On the stored document they
appear as top-level `custom_*` keys (`custom_company_description`,
`custom_t5VndkoW`), and the template token is that stored key verbatim:
`{{custom_company_description}}`. Confirm the exact key with
`find_lead_by_email` before writing it into a sequence, since some workspace
fields carry generated suffixes rather than readable names.

Values are not always plain strings. Enrichment-populated variables come back
as objects shaped `{status: "SUCCESS", val: "...", msg: "Success"}`, so the
usable text is `.val`; manually supplied ones are plain strings.
`list_all_leads` never returns a custom variable's value; the un-prefixed,
always-empty extra columns some workspaces show there (`segment`,
`country_hq`, `email_draft`) are not the stored keys. Only
`find_lead_by_email` returns real values, inside `lead_data`.

## Dedupe, skip, and overwrite flags

`add_leads_to_campaign` carries the first five below. `add_single_lead`
carries all seven; `skip_lead_from_list` and `verify_lead` do not exist on
the bulk tool.

- `skip_if_in_workspace` is the widest net: skip any lead already present
  anywhere in the workspace, in any campaign, in any state.
- `skip_lead_for_active_only_camp` skips only leads sitting in an ACTIVE
  campaign. Paused campaigns do not block the add.
- `skip_lead_in_active_pause_camp` skips leads in ACTIVE or PAUSED campaigns.
  Strictly wider than the previous flag.
- `is_overwrite` updates an existing lead with the fields you supply while
  retaining every field you did not supply. Without it, a duplicate that was
  not skipped is left untouched.
- `resume_camp_if_completed` flips a COMPLETED campaign back to active when
  the leads land, which starts sending. Treat it as a send-class decision.
- `skip_lead_from_list` skips a lead that is in a list. Single-add only.
- `verify_lead` verifies the address before adding. Single-add only. The
  stored document carries `is_email_verified`, seen as `NOT_CHECKED` when no
  verification ran.

## Reading leads back

`list_all_leads` paginates with `page` and `limit`, orders with `sort` plus
`direction`, and filters on `campaign_id`, `status`, `label`, `email`,
`first_name`, `last_name`. It returns a projection: identity fields, `status`,
`label`, progress (`current_step`, `sent_step`, `total_steps`,
`next_email_time`), `replied_count`, `opened_count`, `bounce_msg`, `mx`,
`camp_name`. No sequence bodies.

`find_lead_by_email` takes `email` and paginates with `skip` and `limit`, not
`page`. Leave `campaign_id` blank to find every campaign the address appears
in. It is the only read that returns the full document.
`get_lead_count` returns a per-status array for the workspace, or for one
campaign when `campaign_id` is passed. Statuses: NOT_CONTACTED, CONTACTED,
COMPLETED, REPLIED, RESCHEDULED, UNSUBSCRIBED, BOUNCED, SKIPPED. Run it
before and after any bulk operation to size and then confirm the blast
radius. `opened_count` is meaningless when the campaign has open tracking off
(`is_emailopened_tracking: 0`), which is how real campaigns on this account
run. Check that flag before reporting zero opens as a finding.

## Labels versus statuses

`status` is system-owned and advances on its own. `label` is yours: a
free-form UPPER_SNAKE string on the lead. `INTERESTED`, `MEETING_BOOKED`, and
`MEETING_IS_BOOKED` all exist on this account, so probe with `list_all_leads`
and a `label` filter and match the spelling already in use. Subsequence
triggers are a separate namespace: a `LEAD_LABEL_UPDATED` trigger label must
start with `LEAD_MARKED_AS_`, as in `LEAD_MARKED_AS_INTERESTED`, while the
lead's own `label` field holds the bare value `INTERESTED`.

## Mutating leads

- `update_lead_variables` takes `workspace_id`, `email`, and a `variables`
  object. It updates existing keys and adds new ones, and the label goes in
  that same object as `{"label": "INTERESTED"}`. `campaign_id` is optional;
  pass it to scope the change when the address is in several campaigns.
- `update_lead_status` accepts exactly one value for `new_status`:
  `COMPLETED`. Nothing else is valid. It ends the sequence for that lead, and
  requires `campaign_id` alongside `email`, unlike `update_lead_variables`.
- `assign_lead_to_member` takes `lead_id` and a 24-hex `member_id`. Pass an
  empty string as `member_id` to unassign.
- `add_leads_to_subsequence` takes `subseq_id` and `parent_lead_ids`, which
  must be lead ids already present in the subsequence's parent campaign.

## Safety

Adding leads to an ACTIVE campaign queues real cold email to real people.
These are confirm-first and must never be chained automatically off a read:
any add into an ACTIVE campaign, and any add carrying
`resume_camp_if_completed: true`.

`delete_leads` is unrecoverable. `campaign_id` is optional, `delete_list` is
required and needs at least one address. With `delete_all_from_company: true`
PlusVibe removes every lead sharing a domain with the addresses in
`delete_list`, so one entry can wipe hundreds of records. `launch_campaign`
is Risk Send and belongs to the campaign skill. Never call it as a follow-on
to a lead import.

## Workflows

### Import a list cleanly with dedupe
1. Resolve the workspace with `get_workspaces` (read `_id`) and the campaign
   with `list_campaigns` and a `limit` (read `id`).
2. Check campaign status. If it is ACTIVE, say plainly that the import will
   start sending, and get a yes before continuing.
3. Baseline with `get_lead_count` scoped to `campaign_id`.
4. Normalize rows onto the standard field set. Put anything non-standard
   under `custom_variables`.
5. Call `add_leads_to_campaign` (`PLUSVIBE_ADD_LEADS`), rows in the required
   `leads` array, with `skip_if_in_workspace: true` for a first-touch list, or
   `skip_lead_in_active_pause_camp: true` when re-targeting is fine but
   double-sending is not. Leave `resume_camp_if_completed` unset.
6. Send large lists in batches, then re-run `get_lead_count`. The gap between
   your row count and the delta is what got skipped; report it.
7. Spot-check one address with `find_lead_by_email` to confirm the optional
   fields and custom variables actually landed.

### Personalize with custom variables
1. `find_lead_by_email` on a representative lead. Read `lead_data` and list
   its `custom_*` keys verbatim.
2. Unwrap enrichment values: `{status, val, msg}` means the text is `.val`.
3. Build tokens from the exact stored keys, and wrap anything that can be
   missing in a fallback: `{{fallback|{{custom_company_description}}|there}}`.
4. Backfill gaps with `update_lead_variables` per lead.
5. Re-read one lead before the sequence goes out. A token whose key does not
   exist renders empty rather than raising an error.

### Find and relabel a lead after a reply
1. `list_all_leads` with `status: "REPLIED"`, a `limit`, and
   `sort: "created_at"` with `direction: "desc"` for the newest first.
2. `find_lead_by_email` on the address for the full record and every campaign
   it appears in.
3. Set the label with `update_lead_variables` and
   `variables: {"label": "INTERESTED"}`, matching existing spelling.
4. Only when the thread is genuinely finished, call `update_lead_status` with
   `new_status: "COMPLETED"` to stop follow-ups. Confirm first: this ends the
   sequence for that lead.

### Safely remove a bad segment
1. Identify the segment with `list_all_leads` filtered by `campaign_id` plus
   `status` or `label`. Page through and collect addresses.
2. Report the exact count and a sample before deleting anything.
3. When the goal is "never contact again", prefer `add_to_blocklist`, which
   takes addresses or domains in `entries`: deleting loses the history that
   prevents re-import. Blocklist writes also confirm.
4. Delete with `delete_leads`, putting the addresses in `delete_list` and
   scoping to `campaign_id` when only one campaign is meant. Use
   `delete_all_from_company: true` only when the user explicitly asked to drop
   whole companies, and state the domains and projected count first.
5. Confirm the result with `get_lead_count`.
