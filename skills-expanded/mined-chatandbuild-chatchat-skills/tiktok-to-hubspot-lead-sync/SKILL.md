---
id: tiktok-to-hubspot-lead-sync
name: tiktok-to-hubspot-lead-sync
description: "Syncs leads from TikTok Instant Forms into HubSpot CRM contacts. Covers ad account discovery, time window selection, standard field mapping, and email-based deduplication. Also guides users toward the native HubSpot Ads integration for ongoing automated sync. Use when the user wants to sync TikTok leads to HubSpot, mentions TikTok lead gen forms, wants to get TikTok leads into their CRM, asks about a historical lead backfill, asks whether they have received any TikTok leads, asks what leads came from TikTok ads, or asks about the status of their TikTok lead gen forms."
category: TikTok
user-invokable: true
---

# TikTok to HubSpot Lead Sync

## Purpose

Sync leads captured via TikTok Instant Forms into HubSpot as contacts. This skill supports one-time syncs and historical backfills. It also guides users toward HubSpot's native TikTok Ads integration, which handles ongoing sync automatically without needing to run this skill each time.

## Background

**TikTok** is a short-form video platform with over a billion active users. Businesses run ads on TikTok to reach audiences and generate leads. One of TikTok's ad formats is the **Instant Form** (also called a lead gen form): a form that appears natively inside TikTok without the user leaving the app. TikTok pre-fills the form with the user's name, email, and phone number from their profile, so submitting takes just a tap or two. When someone submits, TikTok captures their information and stores it in TikTok Ads Manager.

**HubSpot** is a CRM (Customer Relationship Management) platform where businesses manage their contacts, deals, and marketing activity. Sales and marketing teams work out of HubSpot to follow up with leads, enroll them in email sequences, assign them to reps, and track pipeline.

**Lead syncing** is the process of moving leads captured on TikTok into HubSpot so teams can act on them. Without a sync, leads sit in TikTok Ads Manager, disconnected from the CRM where all the follow-up happens. Speed matters: companies that contact a lead within five minutes are 21 times more likely to qualify them than those who wait 30 minutes, and 78% of customers buy from the first company that responds.

HubSpot has a native TikTok lead sync integration that handles this automatically via webhook. When a lead submits a TikTok Instant Form, TikTok pushes a notification to HubSpot, which then creates or updates a contact. At setup, users choose between two timeframe options: "All leads" (syncs the last 90 days plus all new leads going forward) or "New leads only" (no backfill). This timeframe cannot be changed after setup without disconnecting and reconnecting the integration. This is the best long-term solution, but it requires admin access to configure and not all users have it connected.

This skill fills three gaps the native integration does not cover:
1. **On-demand sync**: users who want to sync leads right now without setting up the native integration
2. **Deep historical backfill**: users who need leads from further back than the native integration was configured to cover
3. **Convenient backfill**: users who chose "new leads only" at setup and want historical leads without disconnecting and reconnecting their live integration

The goal of this skill is to provide immediate value while always directing users toward the native integration as the right long-term solution.

## Prerequisites

This skill has no backend of its own. It works entirely by calling two external MCP servers. If either is missing, nothing will work.

| MCP Server | Purpose | Required tools |
|---|---|---|
| **TikTok Ads MCP** | Fetch lead data from TikTok | `auth_advertiser_get`, `advertiser_info_get`, `page_get`, `page_field_get`, `page_lead_task_create`, `page_lead_task_download` |
| **HubSpot MCP** | Create and update contacts in CRM | `get_organization_details`, `get_user_details`, `query_crm_data`, `search_properties`, `search_crm_objects`, `manage_crm_objects`, `search_owners` |

## Onboarding Check

Start by saying: "Let me check what's connected and find your TikTok accounts." Then verify both MCPs are reachable. This matters because every step in this skill depends on one or both of these servers. A failure caught here gives the user a clear setup message. A failure caught mid-sync is confusing and harder to diagnose.

1. Call `auth_advertiser_get` on the TikTok Ads MCP (no parameters). If it fails or is unavailable, stop and show the TikTok setup message below.
2. Call `get_organization_details` on the HubSpot MCP (no parameters). If it fails or is unavailable, stop and show the HubSpot setup message below.
3. Call `get_user_details` on the HubSpot MCP with `include: ["TOOL_INFORMATION"]`. Check that `toolInformation.crmObjectTypeAvailability.CONTACT.write === "AVAILABLE"`. If it is anything other than `"AVAILABLE"`, stop and show the permissions message below.

If all three succeed, move directly to Step 1 without any further message.

**If TikTok Ads MCP is not configured:**
> "This skill requires the TikTok Ads MCP to be connected. Add it to your AI environment, then run this skill again. Setup instructions: https://business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3"

**If HubSpot MCP is not configured:**
> "This skill requires HubSpot to be connected to your AI environment. Set it up using the guide for your platform:
>
> - **Claude**: https://knowledge.hubspot.com/integrations/set-up-and-use-the-hubspot-connector-for-claude
> - **ChatGPT and all other platforms**: https://developers.hubspot.com/mcp
>
> Important: This skill requires the HubSpot MCP. ChatGPT's native HubSpot connector uses a different protocol and will not work. Use the link above even if you are in ChatGPT.
>
> **Gemini users**: The HubSpot connector for Gemini (https://knowledge.hubspot.com/integrations/set-up-and-use-hubspot-connector-for-gemini) is currently read-only and does not support creating or updating contacts. This skill requires write access and cannot run in Gemini today. Check back as HubSpot expands Gemini connector capabilities."

**If the user lacks write access to HubSpot contacts:**
> "Your HubSpot account does not have permission to create or update contacts. This skill requires contact write access. Ask your HubSpot admin to grant you the necessary permissions, then run this skill again."

## Process

1. **Verify MCPs**: Confirm TikTok Ads MCP and HubSpot MCP are both reachable (see Onboarding Check above)
2. **Discover ad accounts**: Fetch accessible TikTok advertiser accounts and pre-filter to those with Instant Forms
3. **Confirm scope**: Ask user which account(s) to sync leads from
4. **Set time window**: Confirm date range (inferred from last sync date, conversation context, or last 7 days)
5. **Export leads**: For each selected account, list Instant Forms, create export task, poll for completion, download results
6. **Map fields**: Translate TikTok field names to HubSpot contact properties
7. **Sync contacts**: For each lead with an email, search HubSpot and update existing or create new contact
8. **Report results**: Summarize what was synced, skipped, and next steps. Always include the native sync setup tip.

## Step 1: Ad Account Discovery

Users may have multiple TikTok ad accounts across different brands, clients, or regions. Do not assume which account to sync. Always show the list and let the user confirm.

1. Call `auth_advertiser_get` on the TikTok Ads MCP (no parameters) to get all authorized advertiser IDs
2. If `auth_advertiser_get` returns no accounts, stop and tell the user:
   > "No TikTok ad accounts were found for your credentials. Make sure your TikTok Ads MCP is authenticated with an account that has at least one active advertiser, then try again."
3. Call `advertiser_info_get` with the returned IDs and `fields: ["advertiser_id", "name", "status"]` to get account names
4. Pre-filter to accounts with lead gen forms: call `page_get` with `business_type: "LEAD_GEN"` for each account. This can be batched in parallel. Keep only accounts that have at least one Instant Form.
5. If no accounts have any Instant Forms, tell the user:
   > "None of your TikTok ad accounts have Instant Form lead gen forms set up. Create a lead gen form in TikTok Ads Manager first, then run this skill again."
6. Present the filtered account names as a clear numbered list, framed so the user understands why the list may not include every account they have:
   > "I found [N] TikTok ad account(s) with lead gen forms set up. Which would you like to sync leads from?
   > 1. Account Name A
   > 2. Account Name B"
7. If only one account exists after filtering, still confirm with the user before proceeding
8. Record selected account ID(s) for the export step

If the user refers to an account by name rather than selecting from the list (e.g., "the Acme account" or "my US account"), match their description to the closest account name in the list and confirm before proceeding: "I think you mean [Account Name], is that right?" Do not silently assume a match.

If the user asks why an account is not listed, explain that only accounts with TikTok Instant Form lead gen forms appear. Accounts without forms are excluded because they cannot have leads to sync. Direct them to create a lead gen form in TikTok Ads Manager if they want that account to appear.

## Step 2: Time Window

TikTok's lead export API does not support date range filtering. The skill downloads all leads for a form and filters by date locally. This means a large form with years of leads will still download everything before filtering. Setting a reasonable time window limits how much data needs to be processed and reduces the chance of syncing stale or duplicate leads.

Before defaulting to 7 days, try to determine a smarter default using two signals:

**Signal 1: Query the last sync date from HubSpot**

Use `query_crm_data` to find the most recently created contact sourced from TikTok. This query only finds contacts from HubSpot's native TikTok integration, not from previous runs of this skill. (`hs_analytics_source_data_1` is read-only and can only be set by HubSpot's form submission pipeline, not by the CRM API.) Run it anyway; if it returns a date, that is a useful starting point.

```sql
SELECT createdate FROM CONTACT
WHERE hs_analytics_source_data_1 = 'tiktok'
ORDER BY createdate DESC
LIMIT 1
```

If a result is returned, suggest that date as the start of the sync window: "It looks like your last TikTok lead was synced on [date]. I'll sync leads from that date to today to pick up where you left off. Does that work?"

If no result is returned, the user may not have synced before or may not have the native integration set up. Default to last 7 days.

If `query_crm_data` fails with a permissions error (missing `reporting-base-read` scope), skip it silently and move to Signal 2.

**Signal 2: Check conversation context**

- If the user said "I just ran a sync last Monday," use that date as the start
- If they are doing a historical backfill, ask for a specific start date
- If they said "all my leads" or "everything," warn them that a large range will take longer and confirm before proceeding

Default to last 7 days if neither signal provides a better answer. Always confirm the range before exporting:

> "I'll sync leads from [start date] to today. Does that look right?"

Maximum recommended range per run: 90 days. For longer ranges, suggest splitting into multiple runs.

## Step 3: Lead Export (per ad account)

**Known regional limitation**: `page_lead_task_download` currently only supports leads from regions outside EEA, CH, UK, and US. For users in those markets, lead download will not work. TikTok has confirmed this is a current gap and expects to resolve it in Q3 2026 (possibly as early as July). If a user in an affected market runs this skill, surface the limitation clearly before they get deep into the flow:

> "This skill currently cannot download leads for ad accounts in the US, UK, or EU. TikTok is working to expand regional support and expects it to be available in Q3 2026. Check back then, or reach out to TikTok support for updates."

For each selected ad account:

1. Call `page_get` with `advertiser_id`, `business_type: "LEAD_GEN"`, and `page_size: 100` to list all Instant Forms. Do not filter by status. Forms in "EDITED" (draft) state may still have leads from when they were live. The API paginates: check whether the response indicates more pages and keep calling with an incremented `page` parameter until all forms are retrieved.
2. For each form:
   a. Call `page_lead_task_create` with `advertiser_id` and `page_id` to start an async export. This returns a `task_id`.
   b. Poll status by calling `page_lead_task_create` again with `advertiser_id` and `task_id` (no `page_id`). Repeat until `status = SUCCEED`. Use exponential backoff and retry up to 5 times. Larger forms take longer to process.
   c. Call `page_lead_task_download` with `advertiser_id` and `task_id` immediately after status is SUCCEED. The download link expires 10 minutes after generation.
   d. Parse the downloaded CSV or ZIP file into individual lead records
3. Filter records by `createdAt` to keep only leads within the user's requested time window. The export API returns all leads for a form with no date range support, so this filtering must happen locally.
4. Collect filtered leads across all forms before proceeding to field mapping

Skip any form that has no leads after date filtering. Do not surface this as an error.

### Error handling

**If `page_lead_task_create` fails to create a task**: retry once after a short wait. If it fails again, skip the form, log it, and continue with the next form. Report skipped forms in the output.

**If polling exceeds 5 retries without `status = SUCCEED`**: assume the task is stuck. Skip that form and tell the user:
> "The lead export for form [form name] timed out. This can happen with very large forms. Try again with a shorter date range, or contact TikTok support if the issue persists."

**If `page_lead_task_download` fails or returns an error**: the download link may have expired (links expire 10 minutes after generation). Create a new task for that form and retry the full export sequence once. If it fails again, skip the form and report it.

**If the CSV is empty or malformed**: skip the form silently and continue. Do not stop the entire sync.

**If TikTok returns a rate limit error (HTTP 429)**: wait 60 seconds and retry. If rate limiting persists across multiple retries, pause the sync and tell the user:
> "TikTok's API is rate limiting requests. The sync has been paused. Wait a few minutes and run the skill again to continue."

## Step 4: Field Mapping

Field mapping happens before any contacts are created or updated. The goal is to build a confirmed mapping from every TikTok form field to a HubSpot contact property. This mapping is then applied to every lead row in the export.

The downloaded CSV uses display names as column headers, not API field names. For example, the email column is `Email` (capital E), not `email`. Match column headers case-insensitively against the mapping table below.

The CSV also includes metadata columns that are not contact fields: `lead_id`, `created_time`, `ad_id`, `ad_name`, `adgroup_id`, `adgroup_name`, `campaign_id`, `campaign_name`, `form_id`, `form_name`. Skip these when building the contact properties object.

Example:
```
CSV row:        { Name: "Jane Smith", Email: "jane@co.com", "Company name": "Acme" }
After mapping:  { firstname: "Jane", lastname: "Smith", email: "jane@co.com", company: "Acme" }
```

### How to build the mapping

Do not assume what the CSV column headers will be. TikTok controls the display names used in the CSV and they can change. Instead, discover the field definitions from TikTok at runtime and use those to build the mapping dynamically.

**Discover form fields from TikTok**

Call `page_field_get` on the TikTok Ads MCP with `advertiser_id` and `page_id`. This returns a list of internal field keys (e.g., `["email", "name", "phone_number"]`). It does not return display names.

For standard fields (keys in the table below), the expected CSV column header can be looked up from the standard mapping table. For custom fields, the internal key returned by `page_field_get` is itself the CSV column header (e.g., `?What's your position?` appears as-is in the CSV).

When parsing the CSV, match each column header against the known display names for standard fields (case-insensitive), and match directly against the internal key for custom fields.

**Map internal keys to HubSpot properties**

Once you have the internal key for each CSV column, apply this standard mapping:

| TikTok internal key | HubSpot property | Notes |
|---|---|---|
| `name` | `firstname` + `lastname` | Split on first space: first word = firstname, remainder = lastname |
| `first_name` | `firstname` | |
| `last_name` | `lastname` | |
| `email` | `email` | Primary deduplication key |
| `work_email` | `work_email` | Also maps to `email` if no email field is present |
| `phone_number` | `phone` | |
| `work_phone` | `mobilephone` | |
| `company_name` | `company` | |
| `job_title` | `jobtitle` | |
| `address` | `address` | |
| `city` | `city` | |
| `province_state` | `state` | |
| `zip_code` | `zip` | |
| `country` | `country` | |
| `gender` | `gender` | |

This table is keyed on internal keys, not display names, so it stays correct even if TikTok renames fields in the UI or CSV.

**Handle custom fields**

For any TikTok field not in the standard table above, do the following:

1. Call `search_properties` on the HubSpot MCP with `objectType: "contacts"` and the TikTok field name as a keyword to find the closest matching HubSpot property
2. Collect all custom fields and their suggested matches
3. Present them to the user for confirmation before proceeding:

> "Your form has [N] custom fields. Here are my suggested mappings. Please confirm or adjust each one:
>
> - `budget_range` → `budget` (suggested): confirm, change, or skip?
> - `job_level` → `seniority` (suggested): confirm, change, or skip?"

4. Apply the user-confirmed mappings alongside the standard ones

If the user wants to skip a custom field, exclude it from the sync entirely. If they want to map it to a property that does not yet exist in HubSpot, tell them to create the property in HubSpot first, then re-run the skill.

**Apply the mapping**

Once the full mapping is confirmed, apply it to every lead row. Only include fields with a non-empty value. Do not overwrite an existing HubSpot contact property with a blank value, as the contact may already have enriched data that would be lost.

## Step 5: Contact Sync (per lead)

Email is used as the deduplication key because HubSpot uses email as the primary contact identifier. Without an email, there is no reliable way to match a lead to an existing contact. Creating a contact without email would result in duplicates on every sync run.

Before syncing any leads, ask the user: "I'm about to create or update contacts in HubSpot. Would you like to approve each change individually, or approve all changes for this session?" If they approve for the session, proceed without per-contact confirmation.

For each lead in the export:

1. **No email field present**: skip the lead, increment skipped count, continue to next lead
2. **Email present**: call `search_crm_objects` with an exact email match:
   ```json
   {
     "objectType": "contacts",
     "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": "<email>"}]}],
     "properties": ["email", "firstname", "lastname", "phone"]
   }
   ```
3. **Contact found by email**: call `manage_crm_objects` with `updateRequest` using the contact's `objectId` and the mapped, non-empty field values. Always include `hs_analytics_source: "PAID_SOCIAL"` in the properties. (`hs_analytics_source_data_1` is read-only and cannot be set via the CRM API.)
4. **No email match found**: before creating a new contact, check for a potential duplicate by searching for contacts with the same first name, last name, and phone number (if those fields are present in the lead). If a likely match is found, flag it to the user rather than silently creating a duplicate:
   > "I couldn't find a contact with email [email], but I found a possible match: [Name] ([phone]). Should I update that contact, create a new one, or skip this lead?"
5. **No match at all**: call `manage_crm_objects` with `createRequest` and the mapped, non-empty field values. Always include `hs_analytics_source: "PAID_SOCIAL"` to attribute the contact to paid ads.

## Output

### Results summary

After sync completes, report results in this format:

```
TikTok to HubSpot Lead Sync Complete

Account:      [Ad Account Name]
Time window:  [Start date] to [End date]
Forms synced: [N]

Results:
  [N] contacts created
  [N] contacts updated
  [N] leads skipped (no email field)

Set up automatic sync in HubSpot
Running this skill manually works, but HubSpot's native TikTok Ads
integration syncs leads automatically going forward with no manual effort.

[Setup steps go here — see instructions below]

Full setup guide: https://knowledge.hubspot.com/ads/sync-leads-from-your-facebook-page-or-linkedin-ads-account-to-hubspot
```

For the setup steps in the output, fetch https://knowledge.hubspot.com/ads/sync-leads-from-your-facebook-page-or-linkedin-ads-account-to-hubspot and extract the TikTok-specific setup instructions to replace `[Setup steps go here]`. If the fetch fails or returns no usable content, use these fallback steps:

```
  1. Go to Settings > Marketing > Ads
  2. Click the Lead syncing tab
  3. Click Connect and select TikTok
  4. Check the box next to your ad account
```

If syncing across multiple ad accounts, show one Results block per account, then a single setup tip at the end.

### Owner assignment

If any new contacts were created, offer to assign them to a HubSpot owner. Not all users want this, so ask first:

> "Would you like to assign the [N] new contacts to a specific team member in HubSpot?"

If yes:
1. Call `search_owners` on the HubSpot MCP to list active owners
2. Present the list to the user and ask who to assign the contacts to
3. Call `manage_crm_objects` with `updateRequest` for each new contact, setting `hubspot_owner_id` to the selected owner's ID

If the user names a person rather than selecting from the list (e.g., "assign to Sarah"), match the name to the closest owner in the list and confirm before updating.

### Skipped leads

If any leads were skipped due to no email field, include a specific recommendation alongside the count:

> "[N] leads were skipped because their form submissions did not include an email address. Email is required to create or match contacts in HubSpot. To fix this for future leads, add a required email field to your TikTok Instant Form at https://ads.tiktok.com/help/article/build-instant-form."

### Zero leads found

If the sync returned no leads after date filtering, tell the user clearly rather than showing a blank results screen:

> "No leads were found in the selected time window ([start] to [end]). You can try a wider date range, or check your TikTok Ads Manager to confirm leads are being captured."

## Required API Endpoints

### TikTok Ads API
| Endpoint | Purpose |
|---|---|
| `auth_advertiser_get` | Get authorized advertiser IDs (no parameters required) |
| `advertiser_info_get` | Get account names and status for discovered advertiser IDs |
| `page_get` | List Instant Forms for an ad account |
| `page_field_get` | Get field definitions for a form |
| `page_lead_task_create` | Create async lead export task, or poll existing task status |
| `page_lead_task_download` | Download completed lead export as CSV or ZIP |

### HubSpot API
| Endpoint | Purpose |
|---|---|
| `get_organization_details` | Verify HubSpot MCP is reachable during onboarding check |
| `get_user_details` | Verify user has write access to contacts before starting |
| `query_crm_data` | Find the most recently synced TikTok contact to suggest a smart time window |
| `search_properties` | Find matching HubSpot contact properties for custom TikTok form fields |
| `search_crm_objects` | Search contacts by email for deduplication |
| `manage_crm_objects` | Create or update contacts, and assign owners |
| `search_owners` | List HubSpot owners for post-sync contact assignment |
