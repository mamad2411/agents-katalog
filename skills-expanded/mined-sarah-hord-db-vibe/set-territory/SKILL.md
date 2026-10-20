---
name: set-territory
description: Select a sales territory to set context for other skills. Use when the user says "set territory", "pick territory", "which territory", "select territory", "change territory", or needs to scope analysis to a specific region, AE, SA, or person.
---

# Set Territory

Resolves a sales territory by looking up a Salesforce user in `main.fin_live_gold.sfdc_users_mapping` and reading their region fields. Stores the populated region values as context so downstream skills (like uco-hygiene-review) can filter by them.

## Workflow

### Phase 1: Prerequisites

1. Ensure Logfood authentication: `databricks auth profiles | grep logfood`
   - If not authenticated: `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`
2. Select a warehouse using the `databricks-warehouse-selector` skill with `--profile=logfood`

### Phase 2: Ask Who

Ask the user: "Whose territory? Enter a name or email to search."

### Phase 3: Lookup User

Run `sql/lookup-user.sql` with the search term substituted for `<search_term>`:

```bash
SEARCH="<user_input>"
SQL="SELECT sfdc_user_id, name, email, title, role_name, sfdc_region_l1, sfdc_region_l2, sfdc_region_l3, sfdc_region_l4, bu, sub_bu FROM main.fin_live_gold.sfdc_users_mapping WHERE (name ILIKE '%${SEARCH}%' OR email ILIKE '%${SEARCH}%') ORDER BY name"
databricks api post /api/2.0/sql/statements/ --profile=logfood \
  --json="{\"statement\": \"$SQL\", \"warehouse_id\": \"<id>\", \"format\": \"JSON_ARRAY\", \"wait_timeout\": \"30s\"}" \
  > /tmp/users.json
```

**Handle results:**

- **0 results:** Tell the user no users matched and ask them to try again.
- **1 result:** Auto-select and confirm the name, email, title, and populated regions.
- **Multiple results:** Show a numbered list with full detail and ask the user to pick by number:

```
#  Name              Email                          Title                    Region L1     Region L2              Region L3
1  Henry Hai         henry.hai@databricks.com       Manager, PS              FINS          FINS Insurance & WAM   (none)
2  Henry Nguyen      henry.nguyen@databricks.com    Solutions Architect      FINS          FINS Insurance & WAM   FINS-INS-ENT
```

Only show region columns that have at least one non-null value across all results.

### Phase 4: Store Context

Read `role_name`, `sfdc_region_l1`, `sfdc_region_l2`, and `sfdc_region_l3` from the selected user row. Save only the fields that are populated (non-null, non-empty). Output a clear summary:

```
Territory set:
- User:      Henry Hai (henry.hai@databricks.com)
- Title:     Manager, PS
- Role:      FY27 Manager - AMER Ind - FINS Insurance & WAM
- Region L1: FINS
- Region L2: FINS Insurance & WAM
- Region L3: (not set — queries will include all L3 values under L2)
```

Downstream skills must filter only on the region levels that are explicitly set, and include all values for levels that are not set.

## SQL Resources

- `sql/lookup-user.sql` — search `main.fin_live_gold.sfdc_users_mapping` by name or email (case-insensitive)

## Important Notes

- Use `--profile=logfood` for all queries
- `fin_live_gold.sfdc_users_mapping` is a gold table — no `processDate` filter needed
- Region fields use `ILIKE` for case-insensitive matching
- The table has no `is_active` column; if stale/departed users appear in results, advise the user to search by email for precision

## Examples

### Example: Unique match
User: "Set my territory"
→ User types "henry hai" → one result → auto-select → Region L1=FINS, L2=FINS Insurance & WAM, L3=(none) stored.

### Example: Multiple matches — pick by region
User: "Set territory for henry"
→ Returns 2 Henrys in different roles/regions → show table with regions → user picks one → store their region fields.

### Example: Switch territory
User: "Switch territory to John's accounts"
→ Same flow from Phase 2, overwrites previously stored territory context.
