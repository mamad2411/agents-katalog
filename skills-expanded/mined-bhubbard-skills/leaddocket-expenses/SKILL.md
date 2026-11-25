---
name: leaddocket-expenses
description: >
  Track Expense records on Leads in LeadDocket. Covers adding new expenses,
  fetching by ID, listing expenses in a date range, and deleting expenses.
  Use for syncing case cost records with accounting systems or billing platforms.
---

# LeadDocket — Expenses

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

An **Expense** is a cost incurred on a case (e.g., medical record fees, filing fees, expert witness costs). Each expense is associated with a lead.

---

## Add a new expense

```http
POST /api/expenses
Content-Type: application/json

{
  "LeadId": 1234,
  "Description": "Medical Records Fee - St. David's Hospital",
  "Amount": 250.00,
  "ExpenseDate": "2026-05-15",
  "ExpenseTypeId": 3
}
```

`ExpenseAddApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to associate expense with |
| `Description` | Yes | Description of the expense |
| `Amount` | Yes | Expense amount (decimal) |
| `ExpenseDate` | No | Date of expense (YYYY-MM-DD) |
| `ExpenseTypeId` | No | Expense type from lookup |

Returns `200 OK` with `ExpenseApi`.

---

## Get an expense by ID

```http
GET /api/expenses/{id}
```

Returns `ExpenseApi`.

---

## Get expenses in a date range

```http
GET /api/expenses/getlist?startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}
```

Returns array of `ExpenseApi`. Use for billing cycle reconciliation or financial reporting.

---

## Delete an expense

```http
DELETE /api/expenses/delete/{id}
```

Returns `200 OK`.

---

## Best Practices

- **ExpenseTypeId**: Get valid type IDs from `GET /api/lookups?type=ExpenseTypes` (see `leaddocket-lookups`).
- **Date range queries**: Use `getlist` for date-range-based reconciliation. For per-lead expense tracking, fetch the lead with `leaddocket-leads` using the `LeadCustomFields` or `Settlements` flags.
- **Don't double-insert**: Check for existing expenses before adding in automated workflows — there's no duplicate detection on description/amount.
- **Decimal precision**: Two decimal places for amounts.
