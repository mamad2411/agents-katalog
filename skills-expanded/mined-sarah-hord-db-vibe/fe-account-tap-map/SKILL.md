---
name: fe-account-tap-map
description: Complete TAP (TAM, Architecture, Powerbase) mapping for Databricks customer accounts. Builds on tam-sizing to add incumbent tools, champions, and DBRX penetration by workload area. Generates a comprehensive Google Doc ready for SFDC Account Plan writeback.
user-invocable: true
model: opus
---

# TAP (TAM, Architecture, Powerbase) Map for SFDC

Complete TAP mapping for Databricks customer accounts - the foundation for strategic Account Planning. Generates workload-level TAM estimates, identifies incumbent tools and competitive threats, maps champions and executive buyers, and calculates Databricks penetration. Output is a formatted Google Doc that mirrors the SFDC TAP Map structure.

## Quick Start

```
/fe-account-tap-map <Account Name>
```

Pass the account name. The workflow will:
1. Pull Salesforce data and Logfood consumption in parallel
2. Map SKUs to 8 standard workload areas and build TAM estimates
3. Pull peer benchmarks and refine TAM ranges
4. Identify incumbent tools and competitive threats per workload
5. Map executive buyers and champions to workload areas
6. Calculate DBRX % of TAM (penetration) per workload
7. Generate a comprehensive Google Doc with TAP analysis
8. **[OPTIONAL]** Write TAP data to SFDC Account Plan (requires explicit user consent)

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication`
2. **Databricks** - Run `/databricks-authentication` (for Logfood queries)
3. **Google** - Run `/google-auth` (for Google Doc creation)

## Required Information

The skill requires only an **Account Name** (e.g., "Compass", "Zillow", "Acme Corp"). Provided as: $ARGUMENTS

If no account name is provided, ask the user for one before proceeding.

## Reference Files

This skill uses resource files for detailed reference data:
- **`resources/TAXONOMY_AND_METHODOLOGY.md`** - Workload taxonomy, SKU mapping, TAM sizing methodology, champion assignment logic, competitive tool mapping, peer benchmarking approach
- **`resources/SFDC_SCHEMA.md`** - SFDC object schema, field names, picklist values, writeback process, consent flow
- **`resources/OUTPUT_TEMPLATE.md`** - Google Doc template structure, section formats, creation instructions

Load the relevant resource file when entering each phase.

---

## Phase 1: Parallel Data Collection

Launch TWO `fe-internal-tools:field-data-analyst` agents simultaneously:

**Agent 1 - Salesforce Data:**

Find the Account ID, then pull in parallel:
```bash
sf data query --query "SELECT Id, Name, Type, Website FROM Account WHERE Name LIKE '%ACCOUNT_NAME%' LIMIT 10" --json
```

Pull: Account overview, all UCOs (names, descriptions, stages, workload types, health, implementation notes, owner/champion contacts), Opportunities (INCLUDE Competitors__c), Contacts (names, titles, roles, email), Blockers (descriptions), Feature Preview Approvals, ASQs (include notes/descriptions).

**Key for Architecture Mapping:** Capture Competitors__c from Opportunities, lost UCOs and reasons, UCO names/descriptions (look for tool references like "migrate from X", "replace Y"), Contact titles (imply tooling - e.g., "Snowflake Admin"), Blocker descriptions, ASQ notes, UCO owner/champion fields.

**Agent 2 - Logfood Consumption:**

Query Logfood with the Salesforce Account ID:
```sql
-- Monthly consumption overview (last 12 months)
SELECT usage_date, SUM(dbu_dollars) as dbu_dollars
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -12)
GROUP BY usage_date ORDER BY usage_date

-- Consumption by SKU (for workload mapping)
SELECT sku, SUM(dbu_dollars) as dbu_dollars
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -12)
GROUP BY sku ORDER BY dbu_dollars DESC

-- Workspace details
SELECT workspace_id, workspace_name, SUM(dbu_dollars) as total_spend
FROM main.gtm_data.c360_consumption_monthly
WHERE account_id = 'SALESFORCE_ACCOUNT_ID'
AND usage_date >= DATE_ADD(CURRENT_DATE(), -12)
GROUP BY workspace_id, workspace_name ORDER BY total_spend DESC
```

**Troubleshooting:** If Logfood warehouse times out, retry after 30s (cold start). Capture the Salesforce Account ID early. Export results to `/tmp/claude/` as CSV.

## Phase 2: Initial TAM Sizing

**Load `resources/TAXONOMY_AND_METHODOLOGY.md`** for workload taxonomy, SKU mapping, and TAM sizing methodology.

Map SKUs to 8 workload areas using the taxonomy table. Build initial TAM per workload using:
1. Baseline (Logfood consumption)
2. Pipeline uplift (active U4-U5 UCOs)
3. Recovery potential (non-technical lost UCOs)
4. Adoption gaps (features not yet adopted)
5. Growth trajectory (observed ramp rates)

Assign confidence ratings per workload (High / Medium-High / Medium / Medium-Low / Low-Medium).

## Phase 3: Peer Benchmarking

Launch another `fe-internal-tools:field-data-analyst` agent to pull peer data from Logfood.

**Load `resources/TAXONOMY_AND_METHODOLOGY.md`** for peer benchmarking approach and queries.

1. Identify 4-8 peers (same industry, adjacent verticals, aspirational)
2. Pull consumption by SKU for each peer
3. Calculate workload mix percentages
4. Build comparison table (over/under-indexed vs peer average)

**Tips:** Minimum 2 peers needed. Exclude <$50K spend. Peer average is directional, not prescriptive.

## Phase 4: Peer-Adjusted TAM

Refine initial TAM using peer data:
- **Over-indexed (account > peer avg):** Narrow TAM range. Strengths to DEFEND.
- **Under-indexed (account < peer avg):** Widen upside. Primary EXPANSION opportunities.
- **At-parity:** Keep initial estimates. Incremental growth.

Recalculate TAM ranges, upside amounts, total account TAM, and add peer-referenced rationale.

## Phase 5: Architecture Mapping

**Load `resources/TAXONOMY_AND_METHODOLOGY.md`** for competitive tool mapping and champion assignment logic.

**5A. Incumbent Tools** - Map from Competitors__c field, lost UCOs, and UCO implementation notes to workload areas using the competitive tool mapping table.

**5B. EB/Champion** - Use the champion assignment decision tree (4 confidence levels: HIGH/MEDIUM/LOW/GAP). Prioritize UCO ownership over title matching.

**5C. DBRX % of TAM** - Calculate: `(Current Annual Spend / Est. TAM Midpoint) * 100`

## Phase 6: Google Doc Creation

**Load `resources/OUTPUT_TEMPLATE.md`** for the full document template.

Write content as markdown to `/tmp/claude/<account>_tap_map.md`, then convert:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/claude/<account>_tap_map.md \
  --title "<Account Name> - TAP Map (TAM, Architecture, Powerbase)"
```

## Output

After Phase 6, provide:
1. The Google Doc URL
2. A brief summary:
   - Current consumption vs TAM range
   - Top 2-3 workloads with highest expansion opportunity
   - Champion gaps (workloads without clear owners)
   - Next steps for data quality

## Phase 7: SFDC Writeback (EXPLICIT USER CONSENT REQUIRED)

**NEVER write data to Salesforce without EXPLICIT user approval.**

**Load `resources/SFDC_SCHEMA.md`** for the complete SFDC schema, field names, and writeback process.

After generating the Google Doc, you MUST:
1. **STOP** and show the user the Google Doc URL and summary
2. **ASK** explicitly: "Would you like me to write this TAP Map data to Salesforce Account Plan?"
3. **WAIT** for the user to respond "yes", "approve", "proceed", or similar
4. **CHECK** for existing SFDC data — if records already exist, show a field-by-field diff table comparing current SFDC values vs new TAP Map values. Flag any fields where new data would CLEAR existing values.
5. **GET SECOND CONFIRMATION** if existing data would be overwritten — the user must approve the diff before any writes happen
6. **ONLY THEN** proceed with SFDC writeback using the schema in `resources/SFDC_SCHEMA.md`

**DO NOT assume consent. DO NOT write to SFDC unless the user explicitly approves. DO NOT overwrite existing SFDC data without showing the diff first.**

## Error Handling

| Issue | Resolution |
|---|---|
| Agent killed/interrupted | Relaunch with Account ID and data already collected |
| Logfood timeout | Retry once after 30s, then fall back to Salesforce CLI |
| No peers found | Skip Phase 3-4, note in methodology, use initial estimates |
| Account not found in Salesforce | Ask user to clarify name, try variations (Inc., Corp., Group) |
| Google auth expired | Run `/google-auth` |
| <2 peers found | Broaden search to adjacent verticals or similar-sized accounts |
| No Competitors__c data | Note in doc, rely on lost UCO data only |
| No contacts found | Note champion gaps in output |
| User does not consent to SFDC writeback | STOP. Do not write. Google Doc is the deliverable. |
| No Account Plan found | STOP. Notify user to create Account Plan in Salesforce first. |
| SFDC API error | STOP. Notify user. Suggest manual writeback from Google Doc. |

## What Makes a Great TAP Map

1. **Comprehensive** - Covers all 8 workload areas with TAM, tools, and champions
2. **Grounded in data** - Every field traces back to Salesforce or Logfood
3. **Peer-validated** - TAM ranges pressure-tested against industry peers
4. **Actionable** - Clear expansion priorities, competitive threats, and champion gaps
5. **SFDC-ready** - Structure mirrors SFDC Account Plan fields for easy writeback

## Related Skills

- `/tam-sizing` - Foundation TAM sizing (Phases 1-4 only, no architecture mapping)
- `/salesforce-actions` - Salesforce query patterns
- `/logfood-querier` - Logfood query patterns
- `/google-docs` - Google Doc creation
