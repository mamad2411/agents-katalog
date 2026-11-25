---
name: schema-build
description: Create and modify FileMaker database schema via OData REST calls against a live hosted solution. Three sub-modes — connect (OData setup walkthrough), build (execute table and field creation), relationships (produce a manual relationship specification checklist). Use when the developer says "build schema", "create tables", "create fields", "run schema", "set up OData", "connect OData", "configure OData", "OData walkthrough", "relationship spec", "specify relationships", "define relationships", or "relationship checklist".
compatibility: Requires OData access to a hosted FileMaker Server solution.
---

# schema-build

Create and modify a FileMaker database schema via OData REST calls. This skill covers the full schema creation workflow from OData connectivity through table/field creation to relationship specification.

**Sub-modes**: `connect` | `build` | `relationships`

---

## Step 1: Determine the sub-mode

Parse the developer's request to identify which sub-mode to run:

- **connect** — mentions OData setup, configuration, connection, credentials, or is the first time working with a new solution that has no OData config
- **build** — mentions creating tables, fields, running the schema, or building the data model
- **relationships** — mentions relationships, TOs, join fields, cardinality, or cascade settings

If ambiguous, ask the developer which sub-mode they need. If the developer says "build schema" without prior OData config, start with `connect` and flow into `build`.

---

## Step 2: Read configuration

Read `agent/config/automation.json` to check for existing OData configuration.

- If the developer names a specific solution, look it up under `solutions.{name}.odata`
- If `CONTEXT.json` exists, read `solution` to identify the active solution and look up its config
- If no OData config exists for the target solution, route to the `connect` sub-mode first

---

## Sub-mode: connect

Walk the developer through OData setup for a FileMaker solution. The goal is a verified OData connection with credentials written to `automation.json`.

### Prerequisites checklist

Present this checklist and confirm each item:

1. **FileMaker Server is running** — Docker container or native install, accessible from this machine
2. **Database is hosted** — the FM file is open and hosted on the server
3. **OData-enabled account exists** — an account in the FM file with:
   - The `fmodata` extended privilege enabled
   - **Full Access** privilege set (required for DDL operations — creating tables and fields)
4. **SSL handling** — determine whether the server uses:
   - A trusted CA certificate (standard HTTPS)
   - A self-signed certificate (requires `--insecure` flag on curl/fetch calls)
   - No SSL (development only — `http://` instead of `https://`)

### Gather connection details

Ask the developer for:

- **Server hostname or IP** (e.g., `local.hub`, `192.168.1.100`, `host.docker.internal`)
- **Database name** — exact `Get(FileName)` value from FileMaker
- **OData username and password**
- **SSL mode** — trusted, self-signed, or none

Construct the base URL: `https://{hostname}/fmi/odata/v4`

### Verify the connection

Use `WebFetch` to test the OData endpoint:

```
GET {base_url}/{database}/$metadata
Authorization: Basic {base64(username:password)}
```

If using a self-signed certificate, add the appropriate insecure flag.

**Success**: the response contains `<edmx:Edmx>` with `<EntityType>` elements listing the solution's tables and fields. Confirm to the developer what tables were found.

**Failure scenarios**:
- 401 Unauthorized — credentials are wrong or `fmodata` privilege is not enabled
- Connection refused — server is not running or hostname is wrong
- SSL error — certificate issue; suggest `--insecure` or trusted CA setup
- 404 — database name is incorrect or not hosted

### Write configuration

On successful verification, write the OData config to `automation.json` under `solutions.{database_name}.odata`:

```json
{
  "base_url": "https://{hostname}/fmi/odata/v4",
  "database": "{database_name}",
  "username": "{username}",
  "password": "{password}",
  "script_bridge": "AGFMScriptBridge"
}
```

If the solution already has an entry in `automation.json` (e.g., with `explode_xml`), merge the `odata` block into the existing entry. Do not overwrite other keys.

Confirm to the developer that the OData connection is configured and ready.

---

## Sub-mode: build

Execute table and field creation via OData REST calls against a live hosted solution.

### Step 1: Locate the FM model

Read the FM model from `plans/schema/{solution-name}-fm-model.md`. This file is produced by the `schema-plan` skill and contains the complete table and field definitions for the solution.

If the FM model file does not exist, tell the developer:

> No FM model found at `plans/schema/{solution-name}-fm-model.md`. Run the `schema-plan` skill first to generate the data model, then come back to build it.

### Step 2: Parse the model

Extract from the FM model:
- Table names and their fields
- Field types (Text, Number, Date, Time, Timestamp, Container)
- Field properties (auto-enter, validation, unique, required/not null)
- Default fields to include (PrimaryKey, timestamps, audit fields)

### Step 3: Map field types to OData types

| FM Type | OData Type | Notes |
|---------|-----------|-------|
| Text | `VARCHAR(n)` | `n` = max characters; use 100 for short text, 500 for medium, 1000+ for long |
| Number | `NUMERIC` | Use `DECIMAL(p,s)` when precision/scale matter; `INT` for integers |
| Date | `DATE` | |
| Time | `TIME` | |
| Timestamp | `TIMESTAMP` | |
| Container | `BLOB` | or `VARBINARY` |

**Field properties mapping:**

| FM Property | OData Property | Notes |
|-------------|---------------|-------|
| Auto-enter serial | `primary: true` | For PrimaryKey fields |
| Unique validation | `unique: true` | |
| Not empty validation | `nullable: false` | |
| Global storage | `global: true` | |
| Auto-enter creation timestamp | `default: "CURRENT_TIMESTAMP"` | |
| Auto-enter creation account | `default: "USER"` | |

**Critical gotcha**: Do NOT specify `default: "NULL"` — FileMaker interprets this as a TIMESTAMP default type, not an actual null value. Omit the `default` property entirely when no default is needed.

### Step 4: Create tables

For each table in the FM model, issue:

```
POST {base_url}/{database}/FileMaker_Tables
Authorization: Basic {base64(username:password)}
Content-Type: application/json

{
  "tableName": "TableName",
  "fields": [
    { "name": "FieldName", "type": "VARCHAR(100)" },
    { "name": "Amount", "type": "NUMERIC" },
    ...
  ]
}
```

**What FileMaker auto-creates** when a table is created via OData:
- A table occurrence (TO) with the same name as the table
- A layout with the same name as the table
- Default fields: `PrimaryKey`, `CreationTimestamp`, `CreatedBy`, `ModificationTimestamp`, `ModifiedBy`

Because these default fields are auto-created, do NOT include them in the `fields` array of the POST body. Only include fields that are specific to the table beyond the defaults.

**Order matters**: Create parent tables before child tables. While OData does not enforce referential integrity at creation time (relationships are manual), creating in dependency order keeps the build log readable.

### Step 5: Add fields to existing tables

If a table already exists and needs additional fields, use PATCH:

```
PATCH {base_url}/{database}/FileMaker_Tables/{table-name}
Authorization: Basic {base64(username:password)}
Content-Type: application/json

{
  "fields": [
    { "name": "NewField", "type": "VARCHAR(100)" }
  ]
}
```

**Important**: PATCH for adding fields is non-atomic — individual fields succeed or fail independently. If 5 fields are submitted and 1 fails, the other 4 are still created. Always check the response for partial failures.

### Step 6: Verify via $metadata

After all tables and fields are created, fetch the full schema to verify:

```
GET {base_url}/{database}/$metadata
```

Parse the response to confirm:
- All expected tables exist as `EntityType` elements
- All expected fields exist with correct types
- Report any discrepancies

### Step 7: Create indexes

For fields that will be used as foreign keys or frequently searched, create indexes:

```
POST {base_url}/{database}/FileMaker_Indexes/{table-name}
Authorization: Basic {base64(username:password)}
Content-Type: application/json

{
  "indexName": "FieldName"
}
```

Index all `ForeignKey*` fields by default.

### Step 8: Write the build log

Write results to `plans/schema/{solution-name}-build-log.md`:

```markdown
# {Solution Name} — Schema Build Log

Built: {date}
Source: plans/schema/{solution-name}-fm-model.md

## Tables Created

| Table | Fields | Status |
|-------|--------|--------|
| Company | 8 | Created |
| Contact | 12 | Created |
| Invoice | 10 | Created |
| LineItem | 7 | Created |

## Fields Added (to existing tables)

| Table | Field | Type | Status |
|-------|-------|------|--------|
| ... | ... | ... | ... |

## Indexes Created

| Table | Field | Status |
|-------|-------|--------|
| Contact | ForeignKeyCompany | Created |
| Invoice | ForeignKeyContact | Created |
| LineItem | ForeignKeyInvoice | Created |

## Errors

{any errors encountered, with the OData response body}

## Notes

- Default fields auto-created by FM: PrimaryKey, CreationTimestamp, CreatedBy, ModificationTimestamp, ModifiedBy
- {any other observations}
```

### Step 9: Post-build guidance

After the build completes, tell the developer:

> Schema build complete. Next steps:
>
> 1. **Relationships** — run `schema-build` with the `relationships` sub-mode to get the relationship specification checklist
> 2. **Calculation fields** — OData cannot create calculation or summary fields. These must be added manually in Manage Database > Fields
> 3. **Auto-enter calculations** — OData only supports basic auto-enter defaults (USER, CURRENT_TIMESTAMP). Custom auto-enter calculations must be set manually
> 4. **Validation rules** — beyond `nullable: false` and `unique: true`, custom validation must be set manually

### Error handling

- **Table already exists**: Report it and skip to field additions via PATCH
- **Field already exists**: Report it, skip that field, continue with remaining fields
- **Authentication failure**: Stop and suggest re-running the `connect` sub-mode
- **Network error**: Report the error and suggest checking server status

### Destructive operations

The OData API supports deleting tables and fields:

- `DELETE {base_url}/{database}/FileMaker_Tables/{table}` — permanently removes the table and all its data
- `DELETE {base_url}/{database}/FileMaker_Tables/{table}/{field}` — permanently removes a field and its data

**MANDATORY: Always confirm with the developer before executing any DELETE operation.** State exactly what will be deleted and that the operation is irreversible. Wait for explicit approval before proceeding.

---

## Sub-mode: relationships

Produce a click-through checklist for manually creating relationships in FileMaker's Manage Database > Relationships dialog. OData cannot create relationships, TOs, or modify the relationship graph — this is a hard platform limitation.

### Step 1: Read the FM model

Read `plans/schema/{solution-name}-fm-model.md` for the relationship definitions. The model should specify:

- Table occurrence (TO) names
- Join fields (which field on each side)
- Cardinality (one-to-one, one-to-many, many-to-many)
- Cascade delete settings
- Allow creation of related records settings

### Step 2: Generate the relationship checklist

Write to `plans/schema/{solution-name}-relationships.md`:

```markdown
# {Solution Name} — Relationship Specification

Generated: {date}
Source: plans/schema/{solution-name}-fm-model.md

## Instructions

Open **Manage Database > Relationships** in FileMaker and create each relationship below.
Check off each item as you complete it.

## Table Occurrences

These TOs were auto-created when tables were built via OData. Additional TOs listed below
must be created manually.

### Auto-created TOs (verify these exist)

- [ ] Company
- [ ] Contact
- [ ] Invoice
- [ ] LineItem

### Additional TOs to create

- [ ] Contact_Invoice (base table: Contact) — for filtered portal on Invoice layout
- [ ] ...

## Relationships

### 1. Company -> Contact (one-to-many)

- [ ] **Left TO**: Company
- [ ] **Right TO**: Contact
- [ ] **Join**: Company::PrimaryKey = Contact::ForeignKeyCompany
- [ ] **Join type**: Equal (=)
- [ ] **Allow creation of related records**: Right side (Contact)
- [ ] **Cascade delete**: Off
- [ ] **Sort**: None

### 2. Contact -> Invoice (one-to-many)

- [ ] **Left TO**: Contact
- [ ] **Right TO**: Invoice
- [ ] **Join**: Contact::PrimaryKey = Invoice::ForeignKeyContact
- [ ] **Join type**: Equal (=)
- [ ] **Allow creation of related records**: Right side (Invoice)
- [ ] **Cascade delete**: Off
- [ ] **Sort**: None

### 3. Invoice -> LineItem (one-to-many, with cascade delete)

- [ ] **Left TO**: Invoice
- [ ] **Right TO**: LineItem
- [ ] **Join**: Invoice::PrimaryKey = LineItem::ForeignKeyInvoice
- [ ] **Join type**: Equal (=)
- [ ] **Allow creation of related records**: Right side (LineItem)
- [ ] **Cascade delete**: On (deleting an Invoice deletes its LineItems)
- [ ] **Sort**: LineItem::SortOrder ascending

{repeat for all relationships}

## Multi-predicate relationships

If any relationship uses compound join conditions (multiple field pairs), list each predicate:

### N. {Relationship name}

- [ ] **Left TO**: ...
- [ ] **Right TO**: ...
- [ ] **Join predicate 1**: LeftTO::Field1 = RightTO::Field1
- [ ] **Join predicate 2**: LeftTO::Field2 = RightTO::Field2
- [ ] **Join type**: Equal (=)

## Post-relationship steps

After all relationships are created:

1. [ ] Run **Explode XML** to refresh `xml_parsed/` with the new relationship graph
2. [ ] Run **Push Context** on the primary layout to refresh `CONTEXT.json`
3. [ ] Verify relationships in `agent/context/{solution}/relationships.index`
```

### Step 3: Present the checklist

Show the developer the relationship checklist and the file path. Remind them:

> Relationships cannot be created via any external API — this is a FileMaker platform limitation. Use this checklist to create them manually in Manage Database > Relationships. After completing the relationships, run **Explode XML** to refresh the agent's context.

---

## OData API reference

### Endpoints

| Operation | Method | URL |
|-----------|--------|-----|
| Create table | POST | `{base_url}/{database}/FileMaker_Tables` |
| Add fields | PATCH | `{base_url}/{database}/FileMaker_Tables/{table}` |
| Delete table | DELETE | `{base_url}/{database}/FileMaker_Tables/{table}` |
| Delete field | DELETE | `{base_url}/{database}/FileMaker_Tables/{table}/{field}` |
| Create index | POST | `{base_url}/{database}/FileMaker_Indexes/{table}` |
| Delete index | DELETE | `{base_url}/{database}/FileMaker_Indexes/{table}/{field}` |
| Get schema | GET | `{base_url}/{database}/$metadata` |

### Authentication

All requests use HTTP Basic authentication:

```
Authorization: Basic {base64(username:password)}
```

### Field type reference

| OData Type | FM Result | Notes |
|-----------|-----------|-------|
| `VARCHAR(n)` | Text | `n` = max characters |
| `NUMERIC` | Number | General number |
| `DECIMAL(p,s)` | Number | `p` = precision, `s` = scale |
| `INT` | Number | Integer |
| `DATE` | Date | |
| `TIME` | Time | |
| `TIMESTAMP` | Timestamp | |
| `BLOB` | Container | |
| `VARBINARY` | Container | |

### Optional field properties

| Property | Type | Values | Notes |
|----------|------|--------|-------|
| `primary` | bool | `true`/`false` | Marks as primary key |
| `unique` | bool | `true`/`false` | Unique validation |
| `global` | bool | `true`/`false` | Global storage |
| `nullable` | bool | `true`/`false` | `false` = not empty validation |
| `default` | string | `"USER"`, `"CURRENT_TIMESTAMP"`, `"CURRENT_DATE"`, `"CURRENT_TIME"` | Auto-enter default |

### Critical limitations

- **Cannot create**: relationships, additional TOs, layouts (beyond auto-created), value lists, scripts, custom functions, privilege sets
- **Cannot create**: calculation fields or summary fields
- **Cannot set**: auto-enter calculations, custom validation rules, field comments
- **Cannot rename or retype**: existing fields or tables
- **TO names**: OData uses TO names, not base table names — when a table is created via OData, the auto-created TO has the same name as the base table
- **NULL default gotcha**: specifying `"NULL"` as the default value causes FileMaker to interpret it as a TIMESTAMP type default — omit the `default` property entirely when no default is needed
