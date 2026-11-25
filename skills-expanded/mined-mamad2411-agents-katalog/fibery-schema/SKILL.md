---
name: fibery-schema
description: Design and evolve Fibery workspace structure - create spaces, databases, fields, relations, workflows, and formulas, and rename or remove them safely. Use when the user wants to model a domain in Fibery, set up a new space or tracker, add fields or link databases together, or restructure an existing workspace.
---

# Modelling in Fibery

Fibery's value comes from structure: several connected databases rather than
one table with many columns. When a user asks for "a CRM" or "a hiring
pipeline", the job is to design the graph, not to add fields to a Task.

## Design before you build

Ask, or infer and state, three things:

1. **What are the nouns?** Each distinct thing becomes a Database:
   Candidate, Interview, Role. Not one Candidate database with an
   "interview 1 notes" text field.
2. **How do they connect?** Each connection is a Relation with a cardinality.
   A Role has many Candidates. A Candidate has many Interviews.
3. **What moves through stages?** That is a workflow field, one per database.

Then check what already exists with `schema`, and `schema_detailed` on anything
you might extend. Extending an existing space is usually better than creating a
parallel one.

## Naming restrictions

Space, database, and field names may contain **only letters, numbers, and
spaces**. Slashes, dots, ampersands, commas, question marks, and other
punctuation are rejected.

Field and database names are passed fully qualified as `Space/Name`, and the
space prefix must match the database's own space. The one exception: when a
relation targets `fibery/user`, the field name on the user side uses the
`user/` prefix.

## What you get for free

`create_databases` automatically creates these. Never create them by hand:

- `fibery/id`, `fibery/public-id`
- `fibery/creation-date`, `fibery/modification-date`
- `fibery/created-by`, `fibery/modified-by`
- `{Space}/Name`, the title field
- `{Space}/Description`, a rich-text document field

## The field toolbox

| Tool | Makes |
|---|---|
| `create_primitive_fields` | text, int, decimal, bool, date, date-time, date-range, date-time-range, location, document |
| `create_single_select_fields` | one-of-N option field |
| `create_multi_select_fields` | many-of-N option field |
| `create_relation_fields` | a link between two databases |
| `create_workflow_field` | the stage/status field |
| `create_formula_field` | a calculated read-only field |
| `create_files_fields` | file attachments |
| `create_comments_fields`, `create_avatars_fields`, `create_icon_fields` | comment threads, avatars, icons |

### Prefer typed fields to bare text

A bare `fibery/text` field is almost always the wrong answer. It cannot be
filtered cleanly, grouped on a board, or color-coded. Reach for a select field,
a relation, or a typed primitive instead.

When text genuinely is right, give it meaning through meta:

```json
{"database": "SoftDev/Task", "name": "SoftDev/Contact Email",
 "fieldType": "fibery/text", "meta": {"ui/type": "email"}}
```

`ui/type` accepts `text`, `email`, `url`, `phone`.

Numbers carry formatting meta: `ui/number-format` (`Number`, `Money`,
`Percent`), `ui/number-currency-code` (ISO 4217), `ui/number-precision` (0 to
8), `ui/number-thousand-separator?`, `ui/number-unit`.

```json
{"database": "SoftDev/Task", "name": "SoftDev/Budget", "fieldType": "fibery/decimal",
 "meta": {"ui/number-format": "Money", "ui/number-currency-code": "USD",
          "ui/number-precision": 2, "ui/number-thousand-separator?": true}}
```

### Status is a workflow field, not a select

This is the mistake to avoid. If the field represents a process stage, use
`create_workflow_field`. Only one may exist per database and it is always named
`workflow/state`, which is what makes boards, `set_state`, and time-in-state
reports work. A single-select called "Status" gets none of that.

```json
{
  "database": "SoftDev/Task",
  "options": [
    {"name": "To Do", "type": "Not started"},
    {"name": "In Progress", "type": "Started", "color": "#2196F3"},
    {"name": "Done", "type": "Finished", "color": "#4CAF50"}
  ],
  "defaultOption": "To Do"
}
```

The `type` on each option (`Not started`, `Started`, `Finished`) is what tells
Fibery which states count as complete. Set it thoughtfully.

### Relations create a field on both sides

One call, two fields. You name both.

```json
{
  "database": "Planning/Feature",
  "relationDatabase": "SoftDev/Story",
  "name": "Planning/Stories",
  "relationFieldName": "SoftDev/Feature",
  "cardinality": "one-to-many"
}
```

Cardinality is `one-to-one`, `one-to-many`, `many-to-one`, or `many-to-many`,
read from the source database's perspective. Above, one Feature has many
Stories, so the Feature side (`Planning/Stories`) is a collection and the Story
side (`SoftDev/Feature`) is a single reference.

Get cardinality right the first time. It determines whether the field is a
collection, which in turn determines whether writes go through
`update_entities` or `add_collection_items`, and whether queries need a
sub-query.

### Formulas are described, not written

`create_formula_field` takes a plain-English `description` and generates the
expression. Describe the calculation precisely:

```json
{"database": "SoftDev/Task", "name": "SoftDev/Days Since Created",
 "description": "Number of days since the entity was created"}
```

Formulas are read-only and can only reach data the entity is related to. An
entity can roll up its own children, not every record in the workspace. If the
calculation needs something unrelated, add the relation first.

Verify the result with `schema_detailed` after creating, and adjust with
`update_formula_field` if the generated expression missed the intent.

## Build order

Dependencies run one way, so build in this order:

1. `create_space`
2. `create_databases`
3. `create_primitive_fields`, select fields, `create_files_fields`
4. `create_relation_fields` (both databases must exist)
5. `create_workflow_field`
6. `create_formula_field` (every field it references must exist)
7. Views (see `fibery-views`) and data (see `fibery-entities`)

Each create tool takes an array, so batch all fields for a database into one
call instead of looping.

## Changing what exists

- `rename_databases` and `rename_fields` preserve data and auto-update
  formulas that reference the renamed field.
- `update_single_select_fields`, `update_multi_select_fields`,
  `update_workflow_field` adjust options on existing fields.
- `update_formula_field` rewrites a formula.

Renaming is nearly always safer than deleting and recreating, which loses the
data.

## Removing, and how recoverable it is

| Tool | Recovery |
|---|---|
| `delete_fields` | restorable by the user from the Activity Log |
| `delete_databases` | restorable from the Activity Log |
| `delete_space` | restorable from the Activity Log, takes all its databases with it |
| `delete_entities` | permanent, see `fibery-entities` |

Deleting a relation field automatically removes the matching field on the other
database. Do not delete both sides; that is an error.

Even though schema deletions are restorable, they take real data out of view.
Name exactly what will disappear, including the databases inside a space and
roughly how many entities they hold, and wait for confirmation. Fibery's own
system spaces (`fibery/user`, `fibery/file`, `comments`) cannot be deleted.

## Checking your work

After building, run `schema_detailed` on the new databases with
`includeRelatedDatabases: true` and read it back to the user: databases,
their fields with types, and how they connect. That is the moment to catch a
wrong cardinality, while it is still cheap to fix.
