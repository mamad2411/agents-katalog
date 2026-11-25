---
name: client-crm
description: "Creates a complete client relationship management system in Notion with pipeline stages, contact records, deal values, and follow-up tracking. Use when a user wants to replace spreadsheet-based client tracking, set up a CRM without paid software, or build a sales pipeline from scratch."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-fetch
metadata:
  author: Salah-XD
  version: "1.0"
---

# Client CRM

## When to Use This Skill

Use this skill when you need to:
- Build a sales pipeline and client database in Notion from scratch
- Replace a spreadsheet, sticky notes, or memory-based system for tracking clients
- Set up follow-up reminders so deals stop falling through the cracks
- Import an existing contact list into a structured CRM database
- Create filtered views for pipeline stages, overdue follow-ups, and closed deals

**DO NOT** use this skill for:
- Enterprise CRM migration from Salesforce, HubSpot, or Pipedrive (too complex for a Notion database)
- E-commerce product catalog management (different schema needed)
- Project management or task tracking (use a project-tracker skill instead)
- Email automation or drip sequences (this tracks contacts, it does not send emails)

---

## Quick Reference: CRM Features

| Feature | Details |
|---------|---------|
| Properties | 11 fields per contact record |
| Pipeline stages | 6 default (Lead through Closed Won/Lost) |
| Database views | 4 pre-built filtered views |
| Seeding | Bulk import from user-provided contact list |
| Usage guide | Daily/weekly operations documented for the user |

## Quick Reference: Database Schema

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| Name | Title | Contact's full name | Required |
| Company | Rich text | Organization or business name | Empty |
| Email | Email | Primary email address | Empty |
| Phone | Phone number | Primary phone number | Empty |
| Pipeline Stage | Select | Current position in sales pipeline | Lead |
| Deal Value | Number (USD) | Estimated or actual deal amount | 0 |
| Next Follow-Up | Date | When to reach out next | Empty |
| Last Contact | Date | When you last spoke or emailed | Empty |
| Source | Select | How you found this contact | Other |
| Notes | Rich text | Conversation history, context, preferences | Empty |
| Tags | Multi-select | Categories for filtering and grouping | Empty |

### Pipeline Stages

```
Lead --> Qualified --> Proposal Sent --> Negotiation --> Closed Won --> Closed Lost
```

| Stage | Meaning | Action Required |
|-------|---------|-----------------|
| Lead | New contact, not yet vetted | Research and qualify within 48 hours |
| Qualified | Confirmed fit, budget, and interest | Schedule discovery call or send intro |
| Proposal Sent | Proposal or quote delivered | Follow up within 5 business days |
| Negotiation | Active back-and-forth on terms | Respond within 24 hours |
| Closed Won | Deal signed, payment received or agreed | Onboard and deliver |
| Closed Lost | Deal did not close | Log reason in Notes, revisit in 90 days |

### Source Options

Referral, Website, Social Media, Cold Outreach, Event, Inbound, Other

### Default Tags

`hot-lead`, `vip`, `past-client`, `needs-follow-up`, `referral-partner`, `do-not-contact`, `high-value`, `retainer`, `one-time-project`

---

## Core Workflow

EVERY CRM BUILD STARTS BY CREATING THE DATABASE WITH THE FULL SCHEMA BEFORE ADDING ANY CONTACTS -- NEVER ADD PAGES TO A DATABASE THAT IS MISSING PROPERTIES.

### Phase 1: Gather CRM Requirements

Collect these details from the user before building anything:

1. **Notion parent page** -- where should the CRM database live
2. **Contact list** -- existing contacts to import (spreadsheet, list, or dictated)
3. **Custom pipeline stages** -- any modifications to the default 6 stages
4. **Custom tags** -- additional tags beyond the defaults
5. **Currency** -- USD is the default for Deal Value; confirm or change

If the user provides only item 1, proceed with all defaults.

**Brief template for vague requests:**

```
I'll build your CRM in Notion. Quick answers needed:

1. Which Notion page should I create the CRM database under?
2. Do you have existing contacts to import?
3. Any changes to the default pipeline: Lead > Qualified > Proposal Sent > Negotiation > Closed Won > Closed Lost?
4. Any custom tags to add?
5. Currency for deal values? (default: USD)
```

### Phase 2: Locate the Parent Page in Notion

1. Call `notion-search` with the page name or keywords the user provided
2. Identify the correct parent page from the search results
3. Confirm the page ID with the user if multiple matches exist

```
Found Notion page: "Business Hub"
Page ID: abc12345-def6-7890-ghij-klmnopqrstuv

I'll create the CRM database under this page. Correct?
```

**IF THE PAGE IS NOT FOUND:**
- Ask the user for the exact page title or a URL
- Try `notion-search` again with the corrected term
- **After 3 failed searches, stop and explain:** "I cannot find that page. Please verify the page exists and that the Notion integration has access. Check Settings > Connections in Notion."

### Phase 3: Create the CRM Database

1. Call `notion-create-database` with the parent page ID and full schema:

**Database title:** `Client CRM`

**Properties to create:**

```
Name           -> title
Company        -> rich_text
Email          -> email
Phone          -> phone_number
Pipeline Stage -> select
  options: Lead (gray), Qualified (blue), Proposal Sent (purple),
           Negotiation (orange), Closed Won (green), Closed Lost (red)
Deal Value     -> number (format: dollar)
Next Follow-Up -> date
Last Contact   -> date
Source          -> select
  options: Referral (green), Website (blue), Social Media (pink),
           Cold Outreach (yellow), Event (orange), Inbound (purple), Other (gray)
Notes          -> rich_text
Tags           -> multi_select
  options: hot-lead (red), vip (yellow), past-client (brown),
           needs-follow-up (orange), referral-partner (green),
           do-not-contact (gray), high-value (blue), retainer (purple),
           one-time-project (pink)
```

2. Verify creation by calling `notion-fetch` with the returned database ID
3. Confirm to the user with a summary of all configured properties

**IF DATABASE CREATION FAILS:**
- Verify the parent page ID by calling `notion-fetch` on it
- Retry once with the same parameters
- **If it fails again:** "Database creation failed. Please check that the Notion integration has 'Can edit' access on that page. Go to the page > three-dot menu > Connections."

### Phase 4: Seed with Existing Contacts

**SKIP THIS PHASE if the user has no existing contacts to import.**

1. Parse the user's contact list. Accept these formats:
   - CSV (name, company, email, phone, stage, deal value)
   - Bullet point list with details
   - Natural language ("John at Acme, met at the conference, potential $5K project")
   - Tab-separated spreadsheet paste

2. For each contact, map data to the schema:
   - **Name** -- required, extract from the data
   - **Company** -- extract if mentioned, otherwise leave empty
   - **Email/Phone** -- extract if provided; **NEVER guess or fabricate**
   - **Pipeline Stage** -- infer from context, default to "Lead"
   - **Deal Value** -- extract if mentioned, default to 0
   - **Next Follow-Up** -- set to 3 business days from today for Lead/Qualified stages
   - **Last Contact** -- set to today if recently mentioned
   - **Source** -- infer from context (e.g., "met at conference" = Event), default "Other"
   - **Notes** -- capture any extra context provided
   - **Tags** -- infer from context (e.g., "big opportunity" = hot-lead, high-value)

3. Call `notion-create-pages` to add contacts in batches
4. Report seeding results with names, stages, and deal values

**IF CONTACT PARSING IS AMBIGUOUS:**
- Present your interpretation to the user before creating pages
- Example: "I interpreted 'John, Acme, 5K deal' as: Name: John, Company: Acme, Deal Value: $5,000, Stage: Lead. Correct?"

**IF BATCH CREATION PARTIALLY FAILS:**
- Report which contacts succeeded and which failed
- Retry failed contacts individually
- If retries fail, provide details for manual entry

### Phase 5: Create Database Views

**Notion MCP does not support creating views programmatically.** Provide exact instructions for these 4 views:

```
RECOMMENDED VIEWS (create these in Notion):

1. ALL CONTACTS (Table view)
   - Sort: Last Contact (descending)
   - No filter
   - Purpose: Full contact list, most recently contacted first

2. ACTIVE PIPELINE (Board view)
   - Group by: Pipeline Stage
   - Filter: Pipeline Stage is not "Closed Won" AND is not "Closed Lost"
   - Sort: Deal Value (descending)
   - Purpose: Kanban board of active deals

3. FOLLOW-UPS DUE (Table view)
   - Filter: Next Follow-Up is on or before today
   - Sort: Next Follow-Up (ascending)
   - Purpose: Daily action list of who needs outreach

4. WON DEALS (Table view)
   - Filter: Pipeline Stage is "Closed Won"
   - Sort: Deal Value (descending)
   - Purpose: Revenue tracking and past client reference
```

### Phase 6: Deliver Usage Guide

Present this operations guide after the CRM is built:

```
CLIENT CRM — USAGE GUIDE

DAILY ROUTINE (5 minutes):
1. Open "Follow-Ups Due" view
2. Work through each overdue contact
3. After each touchpoint, update:
   - Last Contact -> today's date
   - Next Follow-Up -> next planned outreach date
   - Notes -> what you discussed
   - Pipeline Stage -> advance if appropriate

ADDING A NEW CONTACT:
1. Click "+ New" in the "All Contacts" view
2. Fill in Name (required) and known details
3. Set Pipeline Stage to "Lead"
4. Set Next Follow-Up to 3 business days from now
5. Tag with relevant labels

MOVING A DEAL FORWARD:
1. Open "Active Pipeline" board view
2. Drag the contact card to the next stage
3. Update Notes with what happened
4. Adjust Deal Value if scope changed
5. Set Next Follow-Up:
   - Qualified: 3-5 days
   - Proposal Sent: 5 business days
   - Negotiation: 1-2 days

CLOSING A DEAL:
- Won: Move to "Closed Won", update Deal Value, add Notes
- Lost: Move to "Closed Lost", log reason in Notes,
  set Next Follow-Up to 90 days for re-engagement

WEEKLY REVIEW (15 minutes):
1. Check for stalled deals (no activity in 7+ days)
2. Review contacts not contacted in 30+ days
3. Count deals per stage — healthy pipeline has contacts in every stage
```

---

## Example 1: Freelance Consultant CRM

**User request:** "I'm a freelance UX consultant. I have 8 clients and prospects I track in a Google Sheet. I want to move everything to Notion. My page is called 'Freelance Business'."

**Execution:**

1. **Requirements:** Parent page "Freelance Business", 8 contacts, default stages, custom tags: `ux-audit`, `design-sprint`

2. **Locate parent page:** `notion-search` query "Freelance Business" returns page ID `pg_freelance123`. Confirmed.

3. **Create database:** `notion-create-database` with full schema + custom tags. Database ID: `db_ux456`.

4. **Seed contacts:** User provides 8 contacts. Parsed and imported:

```
Contacts imported: 8 of 8 successful

  Rachel Kim (Fintech Startup)         — Qualified, $12,000
  Dev Patel (Bloom Health App)          — Proposal Sent, $8,500
  Amy Torres (Torres Consulting)        — Closed Won, $6,000
  Jake Nguyen                           — Lead, $3,000
  Olivia Grant (GrantCo Design Agency)  — Negotiation, $20,000
  Sam Whitfield                         — Lead, $0
  Diana Brooks (BrooksMedia)            — Qualified, $5,000
  Chris Yamamoto (Yamamoto Ventures)    — Lead, $15,000

Pipeline total (active deals): $63,500
Tags applied: past-client (Amy Torres)
Next follow-ups set for all Leads (3 business days from today)
```

5. **Views + usage guide delivered.**

**Final delivery:**

```
Your CRM is live under "Freelance Business":
  Database: Client CRM (db_ux456)
  Contacts: 8 imported
  Active pipeline value: $63,500
  Stages: Lead (3), Qualified (2), Proposal Sent (1), Negotiation (1), Closed Won (1)
```

---

## Example 2: Agency Sales Pipeline

**User request:** "I run a small marketing agency. We have about 20 contacts at various stages. I want to track retainer vs. project clients. Our Notion page is called 'Sales & Revenue'."

**Execution:**

1. **Requirements:** Parent "Sales & Revenue", 20 contacts (2 batches), add "Discovery Call" stage, custom tags: `retainer-client`, `project-client`, `agency-referral`, custom source: "Partner Agency"

2. **Locate parent page:** `notion-search` returns `pg_sales789`. Confirmed.

3. **Create database:** 7 pipeline stages (default + Discovery Call), expanded tags and sources. Database ID: `db_agency012`.

4. **Seed contacts in 2 batches:**

```
Batch 1: 10 of 10 successful
  Greenfield Organics        — Discovery Call, $4,500/mo retainer
  TechPulse Inc.             — Proposal Sent, $25,000 project
  Harmon Legal Group         — Negotiation, $8,000/mo retainer
  BlueSky Fitness            — Lead, $3,000
  Cascade Real Estate        — Qualified, $12,000 project
  Rivera & Associates        — Closed Won, $6,500/mo retainer
  Northwind Bakery           — Lead, $1,500
  Summit Financial           — Proposal Sent, $18,000 project
  Apex Coworking             — Discovery Call, $7,000
  Cedar Creek Wellness       — Closed Lost, $10,000

Batch 2: 10 of 10 successful
  Prism Creative Studio      — Qualified, $9,000
  Driftwood Coffee Roasters  — Lead, $2,000
  Ironside Manufacturing     — Negotiation, $35,000 project
  Velvet Events Co.          — Discovery Call, $5,500
  Cornerstone Accounting     — Proposal Sent, $4,000/mo retainer
  Bright Horizons Childcare  — Lead, $3,500
  Stonebridge Property Mgmt  — Closed Won, $7,200/mo retainer
  Redwood Marketing          — Qualified, $0 (referral partner)
  Atlas Sports Academy       — Lead, $6,000
  Lunar Labs                 — Negotiation, $22,000 project
```

5. **Views + usage guide delivered** with agency-specific tip: "Tag every contact as retainer-client or project-client. Filter the Active Pipeline board by tag to see retainer vs. project pipelines separately."

**Final delivery:**

```
Your agency CRM is live under "Sales & Revenue":
  Database: Client CRM (db_agency012)
  Contacts: 20 imported (2 batches)
  Active pipeline: $171,700
  Retainer pipeline: $30,200/mo (4 deals)
  Project pipeline: $121,500 (8 deals)
  Custom: "Discovery Call" stage, Partner Agency source, retainer/project tags
```

---

## Pre-Delivery Checklist

Run this checklist before delivering the CRM. **DO NOT SKIP ANY ITEM.**

| Check | What to Verify | How |
|-------|----------------|-----|
| Database exists | Created and accessible | `notion-fetch` with database ID |
| All 11 properties | Every schema property configured | Verify in `notion-fetch` response |
| Pipeline stages | All stages exist as select options | Check select options |
| Source options | All sources exist as select options | Check select options |
| Tags configured | All tags exist as multi-select options | Check multi-select options |
| Deal Value format | Number formatted as dollar/currency | Verify number format |
| Dates configured | Follow-Up and Last Contact are date type | Verify property types |
| Contacts seeded | All provided contacts created | Count pages vs. expected |
| No duplicates | Same contact not added twice | Check for duplicate names |
| Follow-ups set | Leads/Qualified have Next Follow-Up dates | Verify dates on pages |
| View instructions | User received all 4 view configs | Confirm in delivery |
| Usage guide | User received operations guide | Confirm in delivery |
| Parent page correct | Database under requested page | Verify parent in fetch |

```
Pre-Delivery Checklist:
  [x] Database created and accessible
  [x] All 11 properties configured
  [x] Pipeline stages correct
  [x] Source options present
  [x] Tags configured
  [x] Deal Value formatted correctly
  [x] Date properties configured
  [x] All contacts seeded successfully
  [x] No duplicate contacts
  [x] Follow-up dates set for Leads/Qualified
  [x] View setup instructions delivered
  [x] Usage guide delivered
  [x] Database under correct parent page
```

---

## Recovery and Troubleshooting

### Notion Search Returns No Results

1. Ask the user for the exact page title
2. Try searching with a shorter keyword (e.g., "Sales" instead of "Sales & Revenue Dashboard")
3. Ask the user to confirm the page is shared with the Notion integration
4. **After 3 failed searches:** "I cannot locate that page. Check Settings > Connections in Notion and verify the integration has access."

### Database Creation Fails

1. Verify the parent page ID with `notion-fetch`
2. Check for permission errors in the response
3. Retry once with the same parameters
4. **If it fails again:** "Please go to the parent page > three-dot menu > Connections and ensure the integration has 'Can edit' access."

### Contact Seeding Partially Fails

1. Report which contacts succeeded and which failed
2. Retry failed contacts individually with `notion-create-pages`
3. If individual retries fail, provide contact details formatted for manual entry

### Notion API Rate Limits

1. Pause for 10 seconds between batches
2. Reduce batch size to 5 contacts per call
3. **DO NOT skip contacts due to rate limits** -- slow down and retry

### Schema Modification After Build

**Notion MCP does not support modifying existing database schemas.** Instruct the user:
- Add property: Click "+" in the header row, choose type, name it
- Modify property: Click column header > "Edit property" > change type/name/options

### Duplicate Detection

Flag potential duplicates before creating pages:
```
Possible duplicates detected:
  "John Smith" and "John Smith Jr." — same person?
  "Acme Corp" appears twice with different emails
Please confirm which entries to keep before I import.
```
**NEVER create duplicate contact records** -- always confirm with the user first.

---

## Anti-Patterns

- **DO NOT** create the database without the full property schema -- adding properties after pages exist causes alignment issues
- **DO NOT** guess or fabricate email addresses, phone numbers, or deal values
- **DO NOT** skip the parent page confirmation -- creating under the wrong page is difficult to undo
- **DO NOT** seed contacts without parsing confirmation for ambiguous data
- **DO NOT** deliver without the usage guide -- the CRM is only valuable if the user knows how to operate it
- **DO NOT** promise features Notion cannot deliver -- this is a database, not a CRM with automated emails or reminders
- **DO NOT** create views programmatically -- Notion MCP does not support this; provide manual instructions
