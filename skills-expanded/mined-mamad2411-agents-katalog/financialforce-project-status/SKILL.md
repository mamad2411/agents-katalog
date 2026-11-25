---
name: financialforce-project-status
description: Update the Project Status RAG field (Green/Amber/Red) on FinancialForce/Certinia PSA projects (pse__Proj__c). Use when the user asks to change a FinancialForce project RAG status, check project status in FinancialForce/Certinia, or update pse__Project_Status__c.
---

# FinancialForce Project Status

Update the `pse__Project_Status__c` field on `pse__Proj__c` (FinancialForce Project) records in Salesforce.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.

## Valid Values

`pse__Project_Status__c` accepts exactly three values:

| Value | Meaning |
|-------|---------|
| `Green` | On track |
| `Amber` | At risk / needs attention |
| `Red` | Off track / blocked |

**Do not** accept any other value. If the user says "yellow", map it to `Amber`. If unclear, ask.

## Reading Current Status

### Option A: Logfood (fast, recommended for lookups)

```sql
SELECT Id, Name, pse__Project_Status__c, pse__Stage__c, pse__Is_Active__c
FROM main.sfdc_bronze.pse__Proj__c
WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.pse__Proj__c)
  AND Name LIKE '%<search_term>%'
  AND pse__Is_Active__c = true
ORDER BY Name
LIMIT 20
```

> Use `execute_sql` MCP tool or Databricks SQL. Always filter on `MAX(processDate)`.

### Option B: Salesforce API (real-time)

```bash
sf data query \
  --query "SELECT Id, Name, pse__Project_Status__c, pse__Stage__c FROM pse__Proj__c WHERE Name LIKE '%<search_term>%' AND pse__Is_Active__c = true ORDER BY Name LIMIT 20" \
  --target-org <alias>
```

## Updating Project Status

**Always confirm with the user before updating.** Show them the current value and the proposed new value.

```bash
sf data update record \
  --sobject pse__Proj__c \
  --record-id <18-char-Id> \
  --values "pse__Project_Status__c=<Green|Amber|Red>" \
  --target-org <alias>
```

### Workflow

1. **Find the project** — search by name using Logfood or SOQL (see above)
2. **Confirm the match** — if multiple results, ask the user to pick one. Show Id, Name, and current status.
3. **Confirm the update** — state: "I'll update *Project Name* (Id: `aXXXXXX`) from **Green** to **Amber**. Proceed?"
4. **Execute the update** — run `sf data update record`
5. **Verify** — re-query the record to confirm the change took effect

### Example

```bash
# 1. Find the project
sf data query \
  --query "SELECT Id, Name, pse__Project_Status__c FROM pse__Proj__c WHERE Name LIKE '%Acme Migration%' AND pse__Is_Active__c = true" \
  --target-org prod

# 2. Update (after user confirmation)
sf data update record \
  --sobject pse__Proj__c \
  --record-id a1B7g000001XXXXX \
  --values "pse__Project_Status__c=Amber" \
  --target-org prod

# 3. Verify
sf data query \
  --query "SELECT Id, Name, pse__Project_Status__c FROM pse__Proj__c WHERE Id = 'a1B7g000001XXXXX'" \
  --target-org prod
```

## Important Notes

- **Do not** use `--use-tooling-api` flag.
- The Salesforce object is `pse__Proj__c` (FinancialForce/Certinia managed package prefix `pse__`).
- Record IDs are 18-character Salesforce IDs (e.g., `a1B7g000001XXXXX`).
- Logfood data syncs daily — for just-updated records, use the Salesforce API to verify.
- This skill only covers `pse__Project_Status__c`. For other project fields, extend this skill or create a new one.
