---
name: data-seed
description: Generate realistic seed or test data and load it into a live FileMaker solution via OData. Populates tables with contextually appropriate data while respecting referential integrity. Use when the developer asks to "seed data", "test data", "populate solution", "generate records", or wants sample records in a new or existing schema.
compatibility: Requires OData access to a hosted FileMaker Server solution.
---

# data-seed

Generate realistic seed/test data and load it into a live FileMaker solution via OData POST requests. Useful for populating a new schema before scripts and layouts are built, or for creating test datasets in an existing solution.

---

## Step 1: Resolve OData configuration

Read `agent/config/automation.json` and identify the target solution:

1. If `agent/CONTEXT.json` exists, read `CONTEXT.json["solution"]` to get the solution name.
2. Look up `automation.json["solutions"][solution_name]["odata"]` for the OData credentials and base URL.
3. If no `odata` block exists for the solution, stop and inform the developer:

> OData is not configured for this solution. Add an `odata` block to `agent/config/automation.json` under `solutions.{solution name}` with `base_url`, `database`, `username`, `password`, and `script_bridge`. See `CLAUDE.md` for the structure.

---

## Step 2: Discover the schema

Use the following sources in order of preference to understand the solution's tables, fields, and relationships:

### Option A: CONTEXT.json + index files (preferred)

1. Read `agent/CONTEXT.json` for `tables` (fields with types), `relationships` (join fields, cascade settings).
2. If CONTEXT.json is scoped to only a subset of tables, supplement with index files:
   - `agent/context/{solution}/fields.index` -- all fields across all tables
   - `agent/context/{solution}/relationships.index` -- full relationship graph
   - `agent/context/{solution}/table_occurrences.index` -- TO-to-base-table mapping

### Option B: OData `$metadata` (fallback)

If index files are not available, fetch the schema from OData:

```
GET {odata.base_url}/{odata.database}/$metadata
Authorization: Basic <base64(username:password)>
```

Parse `EntityType` elements for field names and types. Parse `NavigationProperty` for relationships.

### Option C: Developer-provided schema

If neither source is available, ask the developer to describe the tables and fields, or to run **Explode XML** or **Push Context** first.

---

## Step 3: Analyze field types and plan data generation

For each table that will be seeded, classify every field:

| Category | Action |
|----------|--------|
| **Auto-enter serial / UUID / PrimaryKey** | Skip -- FileMaker auto-generates these |
| **ForeignKey fields** | Populate with valid PrimaryKey values from the parent table (requires parent records to exist first) |
| **Global fields** | Skip -- read-only via OData |
| **Container fields** | Skip -- binary data cannot be sent via OData |
| **Calculation fields** | Skip -- read-only, computed by FM engine |
| **Summary fields** | Skip -- read-only, computed by FM engine |
| **CreationTimestamp / ModificationTimestamp** | Skip -- auto-enter by FM |
| **CreatedBy / ModifiedBy** | Skip -- auto-enter by FM |
| **All other fields** | Generate appropriate data |

### Data generation heuristics

Match field names (case-insensitive) to realistic data patterns:

| Field name pattern | Data type | Example values |
|-------------------|-----------|----------------|
| `*Name*`, `*FirstName*` | Text | "Sarah", "James", "Maria" |
| `*LastName*`, `*Surname*` | Text | "Chen", "Rodriguez", "Okafor" |
| `*Company*`, `*Organization*` | Text | "Meridian Systems", "Atlas Corp" |
| `*Email*` | Text | "sarah.chen@example.com" |
| `*Phone*`, `*Mobile*`, `*Fax*` | Text | "555-0142", "(212) 555-0198" |
| `*Address*`, `*Street*` | Text | "742 Maple Avenue" |
| `*City*` | Text | "Portland", "Austin", "Denver" |
| `*State*` | Text | "OR", "TX", "CO" |
| `*Zip*`, `*PostalCode*` | Text | "97201", "73301" |
| `*Country*` | Text | "United States", "Canada" |
| `*Date*`, `*DateDue*`, `*DateStart*` | Date | "01/15/2025" (MM/DD/YYYY for OData) |
| `*Status*` | Text | Context-dependent: "Active", "Pending", "Complete" |
| `*Amount*`, `*Price*`, `*Cost*`, `*Total*` | Number | 29.99, 150.00, 1250.50 |
| `*Qty*`, `*Quantity*` | Number | 1, 5, 12, 100 |
| `*Rate*`, `*Percentage*` | Number | 0.15, 8.5, 12.0 |
| `*Description*`, `*Notes*`, `*Comment*` | Text | Contextually appropriate sentences |
| `*URL*`, `*Website*` | Text | "https://www.example.com" |
| `*Boolean*`, `*Flag*`, `*Is*`, `*Active*` | Number | 0 or 1 |

For fields that do not match any pattern, use the FM field type:
- **Text**: short placeholder text
- **Number**: random integer or decimal appropriate to context
- **Date**: random date within a reasonable range (past 2 years)
- **Time**: random time value
- **Timestamp**: random timestamp within a reasonable range

Generate **varied, realistic data** -- avoid repeating the same values across records. Use diverse names spanning multiple cultures. Vary numeric values realistically (not all the same price, not all the same quantity).

---

## Step 4: Determine seed order

Build a dependency graph from the relationships:

1. Identify parent-child relationships by looking for PrimaryKey-to-ForeignKey join patterns.
2. Sort tables in **topological order** -- parent tables first, child tables last.
3. If circular dependencies exist, inform the developer and ask which table to seed first (foreign key will need a second pass to update).

Example order for a typical solution:
```
1. Clients       (no FK dependencies)
2. Products      (no FK dependencies)
3. Staff         (no FK dependencies)
4. Invoices      (depends on Clients, Staff)
5. Line Items    (depends on Invoices, Products)
```

---

## Step 5: Confirm with the developer

**IMPORTANT: Always confirm before creating any records.**

Present the seed plan:

> **Seed plan for {Solution Name}**
>
> | Order | Table | Records | Dependencies |
> |-------|-------|---------|--------------|
> | 1 | Clients | 10 | -- |
> | 2 | Products | 15 | -- |
> | 3 | Invoices | 25 | Clients |
> | 4 | Line Items | 75 | Invoices, Products |
>
> **Skipped fields**: PrimaryKey (auto-enter), CreationTimestamp, ModificationTimestamp, CreatedBy, ModifiedBy, all globals, all containers, all calculations
>
> Shall I proceed?

If the developer has specified volume (e.g., "10 clients, 50 invoices"), use those numbers. Otherwise, suggest reasonable defaults and ask for confirmation.

---

## Step 6: Execute the seed

### OData record creation

Create records one at a time via OData POST. The OData endpoint for creating records:

```
POST {odata.base_url}/{odata.database}/{TableOccurrenceName}
Authorization: Basic <base64(username:password)>
Content-Type: application/json

{
  "FieldName1": "value1",
  "FieldName2": 42,
  "FieldName3": "01/15/2025"
}
```

**Important OData details:**
- The table name in the URL must be the **table occurrence name** as exposed by OData, not the base table name. These are often the same but may differ. Check `$metadata` EntitySet names if unsure.
- Field names in the JSON body must match the OData-exposed field names exactly.
- The response includes the created record with its auto-generated fields (PrimaryKey, timestamps, etc.).
- **Capture the PrimaryKey** from each created parent record -- child records will need these values for their ForeignKey fields.

### Seed execution loop

For each table in topological order:

1. Generate the data for all records in this table.
2. For child tables, assign ForeignKey values by randomly selecting from the captured PrimaryKey values of the parent table. Distribute child records across parents (e.g., not all invoices assigned to the same client).
3. POST each record individually.
4. Capture the PrimaryKey from the response for use by downstream child tables.
5. Track successes and failures.

### Error handling

- If a POST fails, log the error (status code, response body) and continue with the next record.
- Common errors:
  - **401 Unauthorized** -- credentials are wrong. Stop and report.
  - **404 Not Found** -- table occurrence name is wrong. Stop and report.
  - **400 Bad Request** -- field name mismatch or invalid value. Log and continue.
  - **500 Server Error** -- FM validation rule or auto-enter conflict. Log and continue.
- If more than 50% of records for a table fail, stop seeding that table and report the pattern.

### Rate limiting

- Insert a brief pause between requests if the server returns 429 or if response times exceed 2 seconds.
- For large seed operations (100+ records), process in batches of 25 and report progress between batches.

---

## Step 7: Report results

Present a summary:

> **Seed complete for {Solution Name}**
>
> | Table | Requested | Created | Failed |
> |-------|-----------|---------|--------|
> | Clients | 10 | 10 | 0 |
> | Products | 15 | 15 | 0 |
> | Invoices | 25 | 24 | 1 |
> | Line Items | 75 | 73 | 2 |
>
> **Total**: 122/125 records created
>
> **Errors** (3):
> - Invoices record 18: 400 Bad Request -- "Field 'Status' validation failed"
> - Line Items record 41: 500 Server Error -- "Field not modifiable"
> - Line Items record 62: 500 Server Error -- "Field not modifiable"

---

## Key considerations

- **Idempotency**: Seeding is not idempotent. Running the skill twice creates duplicate records. Warn the developer if the target tables already contain records (check with a GET request first).
- **Value lists**: If CONTEXT.json includes `value_lists`, use those values for fields that reference them (e.g., Status fields should use values from the Status value list, not arbitrary strings).
- **Custom functions as constants**: If CONTEXT.json or custom function sources reveal constant functions (e.g., `DefaultCurrency`, `DefaultCountry`), use those known values rather than generating arbitrary ones.
- **Serial numbers**: If a field has auto-enter serial, do not send a value -- let FM assign it. If a field has auto-enter calculation, do not send a value unless the developer explicitly wants to override it.
- **Unstored calculations**: These appear in `$metadata` but are read-only. Filter them out before generating POST bodies.

---

## Examples

### Example 1 -- New solution, developer specifies volume

User: "Seed the solution with 10 clients, 30 invoices, and 100 line items"

1. Read automation.json -- OData configured for "Invoice Solution"
2. Fetch `$metadata` or read index files for schema
3. Plan: Clients (10) -> Products (infer ~20) -> Invoices (30) -> Line Items (100)
4. Confirm plan with developer
5. Execute: POST each record, capture PKs, wire FKs
6. Report: 160 records created across 4 tables

### Example 2 -- OData not configured

User: "Generate test data for this solution"

1. Read automation.json -- no `odata` block
2. Report: "OData is not configured. Add an `odata` block to `automation.json` for this solution to enable data seeding."

### Example 3 -- Existing data detected

User: "Seed 5 clients"

1. GET `{base_url}/{database}/Clients?$top=1` -- returns a record
2. Warn: "The Clients table already has records. Seeding will add 5 more (not replace existing). Continue?"
3. Developer confirms, proceed with seeding
