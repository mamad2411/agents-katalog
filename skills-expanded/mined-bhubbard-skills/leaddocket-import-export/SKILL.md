---
name: leaddocket-import-export
description: >
  Bulk import and export data in LeadDocket using the CSV-based import and
  export tools in the UI. Covers importing leads and contacts from CSV files,
  field mapping, exporting lead data for backup or migration, and the rules
  for import file formatting. Use for initial data migration, bulk updates,
  or regular data exports to external systems.
---

# LeadDocket — Import & Export

LeadDocket supports bulk data operations via CSV import/export in the admin UI. These are not available as REST API endpoints — they are UI-based tools.

> Support section: [Import & Export](https://support.leaddocket.com/hc/en-us/sections/360009496551-Import-Export)

---

## Import (in the LeadDocket UI)

### Accessing Import

Navigate to **Settings → Import & Export → Import**

### Supported Import Types

| Type | Notes |
|------|-------|
| **Leads** | Import lead records with contact and source data |
| **Contacts** | Import contact records independently |
| **Referral Sources** | Bulk import referral attorney/firm records |

### Import File Requirements

- Format: **CSV (comma-separated values)**
- Encoding: **UTF-8**
- First row: **Column headers** (mapped in the import wizard)
- Phone numbers: Standard formats accepted (digits, dashes, parentheses)
- Dates: `YYYY-MM-DD` or `MM/DD/YYYY`

### Import Workflow

1. Download the **import template CSV** from the import page
2. Populate the template with your data
3. Upload the CSV
4. Map CSV columns to LeadDocket fields in the field mapper
5. Select duplicate handling (skip, update, or create)
6. Preview the first few rows and validate
7. Click **Import**
8. Review the import results report for errors

### Duplicate Handling Options

| Option | Behavior |
|--------|---------|
| **Skip** | Skip records where a matching lead/contact already exists |
| **Update** | Update existing records with CSV data |
| **Create** | Always create new records (may produce duplicates) |

---

## Export (in the LeadDocket UI)

### Accessing Export

Navigate to **Settings → Import & Export → Export**

### Export Options

| Export | Contents |
|--------|---------|
| **All Leads** | Full lead data with contact info and custom fields |
| **Leads by Status** | Filter by pipeline status before export |
| **Leads by Date Range** | Filter by created or updated date |
| **Contacts** | All contacts with custom fields |
| **Referrals** | All referral sources |

### Export Format

- Output: **CSV**
- Includes all standard fields + custom fields as additional columns
- Download link emailed when ready (large exports process asynchronously)

---

## Alternative: API-based Bulk Export

For programmatic export (without the UI), use the API's paginated sync endpoints:

```
Leads:
GET /api/leads/lastupdatedsince?date=1970-01-01&itemsPerPage=500
→ page through all leads

Contacts:
GET /api/contacts/lastupdatedsince?date=1970-01-01&itemsPerPage=500
→ page through all contacts

Custom fields (lead):
GET /api/leads/detailed/{id}?flags=LeadCustomFields
→ per-lead detail fetch
```

---

## Best Practices

- **Always use the import template**: Download the template from the import page — column order and naming may matter for field mapping.
- **Test with 5 records first**: Import a sample of 5 records before the full file to verify field mapping.
- **UTF-8 encoding**: Excel sometimes saves CSV in Windows-1252 encoding. Re-save as UTF-8 to prevent character encoding errors.
- **Back up before import**: Export existing data before importing updates, so you can restore if something goes wrong.
- **Large exports**: Very large CSV exports (50K+ leads) are generated asynchronously. Check your email for the download link.
