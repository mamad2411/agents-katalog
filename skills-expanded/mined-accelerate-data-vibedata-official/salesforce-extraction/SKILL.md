---
name: salesforce-extraction
description: >
  Extract Salesforce data via dlt into dbt on Microsoft Fabric. Use when
  building Salesforce pipelines, handling CPQ overrides, soft deletes, or
  managed package fields. Also use when choosing CDC timestamps or debugging
  missing Salesforce records.
tools: Read, Write, Edit, Glob, Grep, Bash
type: source
domain: Salesforce data extraction
version: 1.0.0
---

# Salesforce Data Extraction — Practitioner Patterns

Hard-to-find patterns for extracting Salesforce data via dlt into dbt on Microsoft Fabric. Focuses on what Claude gets wrong without explicit guidance: field semantic traps, CDC timestamp choices, soft-delete visibility, managed package entropy, and dlt source configuration.

## Quick Reference

The patterns most likely to prevent silently wrong data:

### CDC timestamp: always `SystemModstamp`

| Field | Updates on user edit | Updates on system change | Indexed |
|---|---|---|---|
| `LastModifiedDate` | Yes | No | No |
| `SystemModstamp` | Yes | Yes | Yes |

**Rule**: Use `SystemModstamp` as the incremental cursor for all CDC extraction. `LastModifiedDate` misses system-initiated changes (workflow field updates, process builder, triggers, batch Apex) and is not indexed. The dlt Salesforce verified source defaults to `SystemModstamp` — do not override this.

**What goes wrong**: A nightly pipeline using `LastModifiedDate` silently skips records updated by automated processes. Revenue reports are understated because workflow-updated Opportunities never appear in the delta. The error is invisible — no failures, no warnings, just missing rows.

### Soft deletes: `queryAll()` or you lose records

Standard Salesforce `query()` silently excludes records where `IsDeleted = true`. These are soft-deleted records sitting in the Recycle Bin (retained for 15 days).

**Rule**: Any extraction pipeline for objects that support soft deletes (Opportunity, Account, Contact, Lead, Case, Task, Event) must use `queryAll()` (SOAP API) or the `/queryAll` endpoint (REST API). In Apex, use the `ALL ROWS` keyword.

**What goes wrong**: A pipeline using standard `query()` extracts 10,000 Opportunities. 200 were soft-deleted during the extraction window. The warehouse shows 10,000 records but the actual count is 10,200. Downstream aggregations are wrong, and deleted records never appear in the warehouse for audit trails.

**dlt note**: The dlt Salesforce verified source uses `simple-salesforce` under the hood. Verify your dlt version supports `queryAll` — if it uses standard `query()`, you need to customize the source or add a post-load reconciliation step. Check the `is_deleted` column in your loaded data; if it is always `false` or missing, your source is not capturing soft deletes.

### CPQ overrides `Opportunity.Amount`

When Salesforce CPQ (formerly Steelbrick) is installed, the standard `Opportunity.Amount` field is **not the source of truth** for deal value. CPQ syncs its own calculated totals to the Opportunity, but the flow is:

```
SBQQ__Quote__c (Quote)
  └─ SBQQ__QuoteLine__c (Quote Lines)
       └─ syncs to → OpportunityLineItem
            └─ rolls up to → Opportunity.Amount
```

The problem: CPQ's `SBQQ__NetTotal__c` on the Quote is the authoritative value. `Opportunity.Amount` may lag, reflect a different discount structure, or be overridden by manual edits. In CPQ orgs, `Amount` and `SBQQ__NetTotal__c` frequently diverge.

**Key CPQ fields on Opportunity** (namespace `SBQQ__`):
- `SBQQ__RenewedAmount__c` — renewal value for renewal Opportunities
- `SBQQ__ContractedAmount__c` — contracted value after negotiation
- `SBQQ__AmendedContract__c` — link to the amended contract

**Key CPQ fields on Quote** (`SBQQ__Quote__c`):
- `SBQQ__NetTotal__c` — the CPQ-calculated net total (this is the real amount)
- `SBQQ__ListTotal__c` — list price before discounts
- `SBQQ__CustomerDiscount__c` — applied discount percentage

**Rule**: In any org with CPQ installed, extract `SBQQ__Quote__c` and `SBQQ__QuoteLine__c` alongside Opportunity. Join on `SBQQ__Opportunity2__c` (the Quote's lookup to Opportunity). Use `SBQQ__NetTotal__c` from the primary Quote (`SBQQ__Primary__c = true`) as the authoritative deal value.

**Detection**: Query `SELECT COUNT(*) FROM SBQQ__Quote__c` — if it returns rows, CPQ is installed. Also check for the `SBQQ__` namespace prefix in the org's object list.

### `RecordTypeId` filtering is mandatory in multi-RT orgs

Salesforce objects can have multiple Record Types. Without filtering, a query on `Opportunity` returns all record types mixed together — new business, renewals, internal deals, partner deals.

**Rule**: Always check `SELECT DISTINCT RecordType.DeveloperName FROM Opportunity` before building extraction. Filter by `RecordTypeId` in extraction queries or add `RecordTypeId` and `RecordType.DeveloperName` as extracted columns so dbt can filter downstream.

**What goes wrong**: A pipeline extracts all Opportunities. Revenue reports double-count because renewal Opportunities and new-business Opportunities are summed together. The error looks like a data quality issue, not a pipeline bug.

**dlt note**: Add `RecordTypeId` to your selected fields. dlt will not automatically resolve the `RecordType.DeveloperName` relationship field — you need to either extract the `RecordType` object separately and join in dbt, or use a SOQL relationship query.

### `ForecastCategory` and `StageName` are independent

These fields appear coupled but are independently editable:

- `StageName` is the pipeline stage (Prospecting, Negotiation, Closed Won, etc.)
- `ForecastCategory` is the forecast bucket (Pipeline, Best Case, Commit, Closed, Omitted)
- Salesforce maps a default `ForecastCategory` per `StageName`, but users can override `ForecastCategory` without changing `StageName`

**What goes wrong**: A pipeline groups revenue by `StageName` and assumes `ForecastCategory` matches the default mapping. A sales rep manually overrides `ForecastCategory` to "Commit" while `StageName` is still "Qualification". The forecast report shows committed revenue that the pipeline report shows as early-stage. Neither report is wrong — they reflect different fields.

**Rule**: Extract both fields. Never derive one from the other. In dbt, create a reconciliation model that flags records where `ForecastCategory` does not match the expected mapping for that `StageName`.

## Anti-patterns

What Claude consistently gets wrong without this skill:

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| `LastModifiedDate` for CDC cursor | Misses system-initiated changes | Use `SystemModstamp` |
| `query()` for soft-deletable objects | Silently excludes deleted records | Use `queryAll()` |
| `Opportunity.Amount` in CPQ orgs | Not the authoritative value | Use `SBQQ__NetTotal__c` from primary Quote |
| No `RecordTypeId` filter or column | Mixes deal types silently | Extract `RecordTypeId`, filter or partition in dbt |
| Deriving `ForecastCategory` from `StageName` | They are independently editable | Extract both, flag mismatches |
| Ignoring managed package fields | Missing critical business data | Detect namespace prefixes, extract ISV objects |
| Hardcoding `RecordTypeId` values | IDs differ across sandbox/prod | Use `RecordType.DeveloperName` |

## Managed Package Entropy

Enterprise Salesforce orgs rarely run vanilla Salesforce. Common managed packages that inject objects and override standard field behavior:

| Package | Namespace | What it does to your pipeline |
|---|---|---|
| Salesforce CPQ | `SBQQ__` | Overrides `Amount`, adds Quote/QuoteLine objects, injects calculated fields |
| Clari | `clari__` | Adds forecast objects, custom Opportunity fields for AI-predicted close dates |
| Gong | `gong__` | Adds engagement objects, links Activities to Gong call records |
| LeanData | `LeanData__` | Adds routing objects, custom Lead/Account matching fields |
| Conga (Apttus) | `Apttus__` / `Apttus_Config2__` | Overrides CPQ behavior if installed alongside Salesforce CPQ |

**Rule**: Before building extraction, run:
```sql
SELECT NamespacePrefix, COUNT(*)
FROM EntityDefinition
WHERE NamespacePrefix != null
GROUP BY NamespacePrefix
ORDER BY COUNT(*) DESC
```
This reveals which managed packages are installed. For each significant namespace, check whether it overrides standard fields or injects objects that carry business-critical data.

**dlt note**: Managed package fields use the namespace prefix in their API names (e.g., `SBQQ__NetTotal__c`). dlt will extract these fields if you include them in your object list or use `SELECT *`. However, the column names in your warehouse will include the prefix — plan your dbt staging models accordingly. Use `{{ source('salesforce', 'sbqq__quote__c') }}` with the lowercased, prefixed name.

## dlt Salesforce Source Configuration

The dlt verified source for Salesforce handles authentication, pagination, and incremental loading. Key configuration decisions:

### Write disposition by object type

| Object category | Write disposition | Rationale |
|---|---|---|
| Reference data (User, UserRole, Product2, Pricebook2) | `replace` | Small tables, full refresh is cheap |
| Transactional data (Opportunity, Account, Contact, Lead) | `merge` | Large tables, incremental on `SystemModstamp` |
| Event data (Task, Event, CampaignMember) | `merge` | Append-heavy, incremental preferred |

### Selecting objects

```python
from dlt.sources.salesforce import salesforce_source

# Load specific objects only
source = salesforce_source()
load_data = source.with_resources(
    "opportunity",
    "account",
    "contact",
    "opportunity_line_item",
    "user",
)
```

For CPQ orgs, add:
```python
load_data = source.with_resources(
    "opportunity",
    "account",
    "sbqq__quote__c",
    "sbqq__quote_line__c",
    "opportunity_line_item",
    "user",
    "record_type",  # for RecordType resolution in dbt
)
```

### Credentials

```toml
# .dlt/secrets.toml
[sources.salesforce.credentials]
user_name = "integration-user@company.com"
password = "password"
security_token = "token"
```

For production, prefer Connected App (JWT bearer) auth:
```toml
[sources.salesforce.credentials]
user_name = "integration-user@company.com"
consumer_key = "connected_app_consumer_key"
privatekey_file = "/path/to/server.key"
```

### Incremental cursor

The dlt Salesforce source uses `SystemModstamp` as the default incremental cursor. Verify this in your pipeline by checking the dlt state:

```python
# After a pipeline run, inspect the state
import dlt
pipeline = dlt.pipeline(pipeline_name="salesforce")
sources_state = pipeline.state.get("sources", {})
# Look for last_value entries — they should reference SystemModstamp
```

### Bulk API vs REST API

The dlt Salesforce source uses `simple-salesforce`, which defaults to the REST API (SOAP under the hood for some operations). For large objects (>50k records), consider:

- **Bulk API**: Better for initial full loads and large incremental batches. Processes asynchronously. Use when extracting >50k records per object.
- **REST/SOAP API**: Better for small incremental deltas. Synchronous, simpler error handling. Default for dlt.

If you need Bulk API, you may need to customize the dlt source or use `simple-salesforce`'s bulk methods directly.

## Reference Files

For deeper guidance on specific patterns:

- **[references/field-semantics.md](references/field-semantics.md)** — Salesforce field semantic traps: system fields, formula fields, polymorphic lookups, currency handling, and field-level security filtering.
- **[references/extraction-patterns.md](references/extraction-patterns.md)** — dlt Salesforce source setup, incremental loading patterns, soft-delete handling, reconciliation queries, and staging model conventions.
- **[references/evaluations.md](references/evaluations.md)** — Test scenarios for validating skill behavior.
