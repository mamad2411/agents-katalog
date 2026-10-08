---
name: ea-zoho-crm
description: "Zoho CRM for Ali Rao's EA via the official Zoho CRM connector: look up accounts, contacts, deals, activities, notes and tasks; build a 360 view of a firm combined with email, calendar and meeting history; controlled writes (notes, tasks, stage changes) behind approval. Use for 'what is happening with', 'which clients need attention', 'update Zoho', 'log this in CRM'."
---

# Zoho CRM

Load `ea-operating-model` first. Reads are LOW. Adding a note or task is MEDIUM. Changing a deal stage, amount, owner, or any contact/account field is HIGH. Deleting anything is PROHIBITED.

## First use in a session

Call `Get_Modules` once and cache the module API names in your reply context (Accounts, Contacts, Deals, Tasks, Notes, Events, Calls are standard; the org may have custom modules such as Properties or Mandates). If the connector is not connected, say so and continue from email and state files only.

## Lookup ("what is happening with ABC?")

1. Search Accounts by name (fuzzy: try the firm's short name and domain). If several match, list them and ask.
2. Pull: account fields, related Contacts, open Deals (stage, expected close, last modified), last 10 Activities and Notes, open Tasks.
3. Combine with: email threads with that domain (last 60 days), calendar events with those contacts (past and upcoming), `meetings/*.md` for that firm, `04-commitments.md` for that firm.
4. Answer in this shape, under 200 words:

```
ABC Capital · Deal: Media City block · Stage: Negotiation (since 3 Sep) · Owner: Sarah
Last touch: email 17 Sep (they asked for the title deed copy) · Meeting 10 Sep (Zoom)
Open: NDA countersigned? · Site visit date · Our reply to 17 Sep email (2 days, waiting on Ali)
Next: <one line recommendation>
```

## "Which clients need attention?"

Open deals where any of: last activity older than 14 days; a task overdue; an inbound email unanswered more than 48h; expected close within 14 days; a commitment in `04-commitments.md` overdue. Rank by deal stage and VIP status. One line each.

## Writes

Always via a card except where `06-automation-rules.md` allows notes and tasks.

- **Note** on an account or deal: title, body (never price in a note body; write "pricing discussed by phone, see Ali").
- **Task**: subject, owner, due date, related record.
- **Deal stage change**: from → to, with the evidence (decision line from the meeting note).
- **New contact / account**: only when the party is genuinely new; check `03-firm-register.md` and search Zoho first to avoid duplicates.

After a write, read the record back and confirm the change is visible before reporting `SUCCESS`. Log.

## Data hygiene

Never overwrite a field that already has a value unless Ali asked for that specific change. Never merge records. Never change ownership. If Zoho data contradicts email evidence, report both and let Ali decide.
