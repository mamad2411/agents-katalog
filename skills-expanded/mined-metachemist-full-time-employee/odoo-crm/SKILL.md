---
name: odoo-crm
description: |
  Integrate with self-hosted Odoo Community via JSON-RPC API. Use for CRM
  operations (create leads, log activities, search contacts) and accounting
  draft actions (create draft invoices — never post without human approval).
  Use when processing LinkedIn connections, approved CRM actions, or when
  running the weekly accounting audit. Requires ODOO_URL, ODOO_DB,
  ODOO_USERNAME, ODOO_PASSWORD in .env.
---

# Odoo CRM & Accounting

Interact with Odoo Community Edition via the external JSON-RPC API.

## When to Use

- A new LinkedIn lead arrives → create a CRM lead in Odoo
- User asks to log an activity on an Odoo contact
- Weekly accounting audit → query open invoices / receivables
- Processing an `APPROVAL_ODOO_*.md` file from `vault/Approved/`
- Generating the weekly CEO briefing → pull Odoo metrics

## Setup

Add to `.env`:
```
ODOO_URL=http://localhost:8069
ODOO_DB=mycompany
ODOO_USERNAME=admin
ODOO_PASSWORD=your_odoo_password
```

Install Odoo Community locally:
```bash
# Docker (recommended for local dev)
docker run -d -p 8069:8069 --name odoo \
  -e HOST=db -e USER=odoo -e PASSWORD=odoo \
  odoo:17
```

Or follow: https://www.odoo.com/documentation/17.0/administration/install/install.html

## Available Operations

### CRM
- `create_lead` — Create a new CRM lead/opportunity
- `search_contacts` — Search partner/contact records
- `log_activity` — Schedule or log an activity on a record

### Accounting (DRAFT ONLY — never auto-post)
- `create_draft_invoice` — Create an invoice in draft state
- `list_open_invoices` — List unpaid/overdue invoices
- `get_accounting_summary` — Revenue + receivables summary for briefing

## Rules

- **Never** post/confirm an invoice without `vault/Approved/` file
- **Never** delete Odoo records without explicit human instruction
- **Always** log Odoo operations to `vault/Logs/`
- **Always** write approval request for any write action beyond CRM leads
- Accounting actions: draft is auto-approved; confirm/post requires approval

## Approval File Format

```markdown
---
type: approval_request
action: odoo_post_invoice
status: approved
---

# What will happen after approval?

Invoice INV/2026/00042 will be confirmed and moved from Draft to Posted state.

# Payload

- **Invoice ID:** 42
- **Amount:** $1,500.00
- **Customer:** Acme Corp
```

## Dry-Run Mode

```bash
python .claude/skills/odoo-crm/scripts/odoo_client.py \
  --operation create_lead \
  --data '{"name": "Test Lead", "partner_name": "Acme Corp"}' \
  --dry-run
```
