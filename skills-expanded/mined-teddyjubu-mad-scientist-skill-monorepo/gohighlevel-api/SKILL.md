---
name: gohighlevel-api
description: gohighlevel-api lets the user interact with their GoHighLevel CRM account programmatically using plain-language prompts, managing contacts, opportunities, appointments, conversations, workflows, payments, invoices, webhooks, social media posts, forms, surveys, users, and location settings, which is useful when they want to automate CRM tasks, sync leads, or build custom workflows without navigating the GHL UI manually.
---

# GoHighLevel API Skill

This skill executes GoHighLevel API v2 actions from plain-language user prompts.

## What This Skill Does

This skill gohighlevel-api lets the user interact with their GoHighLevel CRM account programmatically using plain-language prompts, managing contacts, opportunities, appointments, conversations, workflows, payments, invoices, webhooks, social media posts, forms, surveys, users, and location settings, which is useful when they want to automate CRM tasks, sync leads, or build custom workflows without navigating the GHL UI manually.

## Credentials

- **API Key:** `pit-105d0b1f-3e18-41f1-95ad-00aca3775ddf` (Private Integration Token)
- **Base URL:** `https://services.leadconnectorhq.com`
- **Auth headers:** `Authorization: Bearer {API_KEY}` and `Version: 2021-07-28`
- **Location ID:** `j3Mcjo8MfNRna0x0aDqE` (Real Deal Meetup — Baltimore, MD). Use this by default unless the user specifies a different location.
- **Company ID:** `6PzD51NMmoKybzIIunfp`

## Workflow

Execute requests in this order:

1. **Interpret** the user's plain-language request → identify the target resource and action (CRUD + resource type).
2. **Resolve IDs** — if the user gives a name instead of an ID (e.g., "pipeline named Sales"), first call the list endpoint to find the ID.
3. **Build the request** — select method + endpoint from the reference, assemble params/body.
4. **Execute** using `ghl_api.py` (see below).
5. **Present results** — summarise what was done; show key fields (IDs, names, status). Do not dump raw JSON unless the user asks.

**Determine action type:**
- Retrieving data? → Use GET
- Creating something new? → Use POST
- Modifying existing record? → Use PUT or PATCH
- Removing something? → Use DELETE

## Executor Script

```bash
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py <METHOD> <ENDPOINT> [--params '<json>'] [--body '<json>']
```

**Examples:**

```bash
# Get all contacts in a location
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py GET /contacts/ --params '{"locationId":"abc123","limit":20}'

# Create a contact
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py POST /contacts/ --body '{"locationId":"abc123","firstName":"Jane","email":"jane@co.com","tags":["lead"]}'

# Update an opportunity to Won
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py PUT /opportunities/OPP_ID --body '{"status":"won"}'

# Send an SMS
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py POST /conversations/messages --body '{"type":"SMS","contactId":"CTX_ID","message":"Hello!"}'

# Book an appointment
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py POST /calendars/events/appointments --body '{"calendarId":"CAL_ID","locationId":"LOC_ID","contactId":"CTX_ID","startTime":"2026-03-10T14:00:00-05:00","endTime":"2026-03-10T15:00:00-05:00","title":"Discovery Call"}'

# Delete a contact
python3 ~/.openclaw/workspace/skills/gohighlevel-api/scripts/ghl_api.py DELETE /contacts/CONTACT_ID
```

## Reference Files

- **`references/api_reference.md`** — Full table of every endpoint (method, path, required params). Read when the user's request maps to an unfamiliar endpoint or when you need exact field names.
- **`references/master_prompts.md`** — Pre-built prompt patterns for all 40+ common actions. Read for quick lookup of standard operations.

## Key Rules

- **Always include `locationId`** in GET params or POST/PUT body — most endpoints reject requests without it.
- **Pagination:** GET list endpoints return max 100 records. Use `startAfter` + `startAfterId` to page through larger datasets.
- **Rate limits:** Max 100 requests per 10 seconds; 200,000 per day per app per location.
- **Error 403 "token does not have access to this location"** → the locationId is wrong or the token lacks permission for that location.
- **Error 422** → missing required field; check `api_reference.md` for required body fields.
- **Timestamps** must be ISO 8601 format, e.g. `2026-03-10T14:00:00-05:00`.
- **Monetary values** in invoice line items are in **cents** (e.g., `5000` = $50.00).

## Common Multi-Step Patterns

**Find then act (e.g., "update the contact named John Smith"):**
1. `GET /contacts/search?locationId=X&query=John+Smith` → get contactId
2. `PUT /contacts/{contactId}` with updated fields

**Create opportunity for a contact:**
1. `GET /opportunities/pipelines?locationId=X` → get pipelineId + stageId
2. `POST /opportunities/` with pipelineId, stageId, contactId

**Enroll contact in workflow:**
1. `GET /workflows/?locationId=X` → get workflowId
2. `POST /contacts/{contactId}/workflow/{workflowId}`

**Book appointment:**
1. `GET /calendars/?locationId=X` → get calendarId
2. `GET /calendars/{calendarId}/free-slots` → confirm slot is available
3. `POST /calendars/events/appointments`
