---
name: lead-intake
domain: sales
version: 1.0.0
catalog: goflowtics-catalog@2026.05
description: Files a new lead into the Goflowtics sales pipeline. Accepts a name, company, source channel, and optional context, enriches the lead via web search, creates Notion People + Company records, sets a follow-up task, and logs to the vault. Use when the user says "new lead", "add lead", "intake lead", "log lead", or /lead-intake. ON-DEMAND — one lead at a time.
ai_literacy: "Uses Claude to search the web for lead enrichment and write to Notion via MCP. Logs one line to the tenant vault. No data is shared outside these two systems."
---

# lead-intake

Accepts minimal input, enriches, and files. Goal: every new lead gets into Notion with a follow-up date before the conversation that surfaced them is over.

## Inputs (provide these)

- **Name** — person's full name (required)
- **Company** — company name (required or "unknown")
- **Source** — channel: LinkedIn / referral / email / event / cold outreach / other
- **Context** — optional: email snippet, event name, who referred them, any notes

## Steps

1. **Web search** — search `[Name] [Company] LinkedIn` and company website. Collect: role/title, company size/industry, LinkedIn URL if found. Keep enrichment to 2–3 searches — don't over-research.

2. **Notion — People record** — see `references/notion-schema.md`
   - Search People database for existing record by name or email to avoid duplicates
   - If exists: update with new source/context, don't overwrite existing data
   - If new: create record with all available fields set

3. **Notion — Company record**
   - Search Company database by name
   - If exists: link People record to existing company
   - If new: create Company record, link from People record

4. **Notion — follow-up task**
   - Create a task on the People record due in 3 business days
   - Task title: "Follow up with [Name]"
   - Link to People record

5. **Vault log** — append one line to `<vault>/Projects/sales/leads-log.md`:
   `- YYYY-MM-DD — [Name] ([Company]) via [Source] — Notion filed, follow-up [date]`
   Create the file if it doesn't exist.

6. **Terminal summary** — output: name, company, Notion URL (if returned), follow-up date, enrichment summary (role, LinkedIn URL, company size)

## Output format

```
Lead filed: [Name] ([Company])
Source: [channel]
Notion: [URL or "record created"]
Follow-up: [date]
Enrichment: [role] at [company] · [size] · [LinkedIn URL or "not found"]
```

## Constraints

- Do not create duplicate company records — always check first
- Do not auto-email or contact the lead
- If Notion MCP unavailable: log to vault only, note Notion step skipped
- Match language (IS/EN) to context provided
- Notion schema: `references/notion-schema.md`
