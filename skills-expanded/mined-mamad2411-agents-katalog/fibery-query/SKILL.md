---
name: fibery-query
description: Write correct Fibery `query` calls in the q/ query language - selects, filters, sub-queries, aggregation, sorting, and pagination. Use when pulling filtered or aggregated data out of Fibery, counting or summing entities, walking relations, or when a query returns an error or empty result you need to debug.
---

# Fibery query language

The `query` tool speaks Fibery's `q/` language: a JSON s-expression dialect.
It is precise and fast once you respect its type rules, and it fails loudly
when you do not.

Call `get_fibery_skill` with `{skill: "query"}` for the exhaustive operator and
function list. This skill covers the shape, the traps, and the workflow.

## Always start from the schema

Run `schema` then `schema_detailed` on the target database before writing a
query. You need the exact field names, their types, and for enum fields their
option ids. Guessing field names is the top cause of failed queries.

## Anatomy

```json
{
  "query": {
    "q/from": "Product Management/Feature",
    "q/select": {"Name": "Product Management/Name", "Id": "fibery/public-id"},
    "q/where": ["=", ["workflow/state", "enum/name"], "In Progress"],
    "q/order-by": [[["fibery/creation-date"], "q/desc"]],
    "q/limit": 100,
    "q/offset": 0
  }
}
```

`q/from` and `q/select` are required. Everything else is optional.

## Select: four shapes

```json
"q/select": {
  "Name": "Product Management/Name",
  "Secret": ["Product Management/Description", "Collaboration~Documents/secret"],
  "Assignees": {
    "q/from": "assignments/assignees",
    "q/select": {"Name": "user/name", "Email": "user/email"},
    "q/limit": 50
  },
  "Avg Rate": ["q/avg", ["Currency Exchange/Exchange Rate(from)", "Currency Exchange/rate"]]
}
```

1. **Primitive** - a plain field name string.
2. **Path** - an array navigating through a single reference to a primitive
   on the other side.
3. **Sub-query** - for one-to-many and many-to-many collections. `q/limit` is
   **required** inside a sub-query.
4. **Aggregation** - `q/count`, `q/sum`, `q/avg`, `q/min`, `q/max`.

Alias keys on the left are arbitrary; name them for the report you intend to
write.

## The five rules that break queries

### 1. Non-primitive fields cannot be selected bare

A document, relation, or collection field has no scalar value to return.

- Wrong: `{"Description": "Product Management/Description"}`
- Right: `{"Secret": ["Product Management/Description", "Collaboration~Documents/secret"]}`
- Wrong: `{"Assignees": "assignments/assignees"}`
- Right: a sub-query (see above)

Paths work for single relations only. A one-to-many collection needs a
sub-query.

### 2. Reference fields in `q/where` need a primitive subfield

States, single-selects, and relations are references. Filtering on the
reference itself is an error.

- Wrong: `["=", ["workflow/state"], "In Progress"]`
- Right: `["=", ["workflow/state", "enum/name"], "In Progress"]`
- Right: `["=", ["workflow/state", "fibery/id"], "<uuid>"]`

Same for every relation: `["q/in", ["GitHub/Assignees", "fibery/id"], ["<uuid>"]]`.

### 3. Text fields do not use `=`

Use the text operators: `q/equals-ignoring-case?`,
`q/not-equals-ignoring-case?`, `q/contains?`, `q/contains-ignoring-case?`,
`q/not-contains?`, `q/not-contains-ignoring-case?`,
`q/starts-with-ignoring-case?`, `q/ends-with-ignoring-case?`,
`q/null-or-empty?`.

Numbers and dates do use `=`, `!=`, `<`, `<=`, `>`, `>=`.

### 4. `q/order-by` paths are always wrapped in an array

- Wrong: `[["CRM/Name", "q/asc"]]`
- Right: `[[["CRM/Name"], "q/asc"]]`

For date-range fields, wrap with `q/start` or `q/end`:
`[[["q/start", ["Space/Dates"]], "q/asc"]]`.

### 5. Aggregation is root-level only

`q/count`, `q/sum`, `q/avg`, `q/min`, `q/max` work in the top-level
`q/select`. They are **not** supported inside a sub-query. To aggregate a
collection, either query the child database directly with a filter pointing
back at the parent, or use a formula field.

Count a whole database:

```json
{"query": {"q/from": "Collaboration~Documents/Document", "q/select": ["q/count", "fibery/id"]}}
```

## Filtering

`q/where` is `[operator, [field_path], value]`, composed with `q/and` and
`q/or`:

```json
"q/where": [
  "q/and",
  [">", ["fibery/creation-date"], "2026-01-01T00:00:00.000Z"],
  ["q/or",
    ["q/equals-ignoring-case?", ["workflow/state", "enum/name"], "Open"],
    ["q/equals-ignoring-case?", ["workflow/state", "enum/name"], "In Progress"]],
  ["q/in", ["GitHub/Assignees", "fibery/id"], ["<uuid-1>", "<uuid-2>"]]
]
```

Null checks have two forms:

- Any field: `["=", ["q/null?", ["Space/Field"]], true]`
- Text emptiness: `["=", ["q/null-or-empty?", ["Space/Field"]], true]`

Date ranges: address the ends explicitly.
`["<", ["q/end", ["GitHub/Date Range"]], "2026-06-01T00:00:00.000Z"]`

Functions are available inside `q/where` and `q/select`: string
(`q/lower`, `q/upper`, `q/trim`, `q/length`), date parts (`q/year`, `q/month`,
`q/day`, `q/weekday-name`, `q/date`), location (`q/address`, `q/latitude`),
numeric (`q/abs`, `q/round`), and arithmetic (`+`, `-`, `*`, `/`).

## Pagination

`q/limit` defaults to 100 and caps at 1000. `"q/no-limit"` is accepted but
should be a deliberate choice on a database you know is small.

Page with `q/offset` plus a stable `q/order-by`. Without an order-by,
pagination is not guaranteed to be consistent across pages.

Fetch one page, check whether it answers the question, then continue. Tell the
user when results were truncated and how many you saw.

## Debugging ladder

When a query errors or returns nothing:

1. Re-read `schema_detailed`. Is the field name and space prefix exactly right?
2. Is the field a reference or collection being treated as primitive? See
   rules 1 and 2.
3. Is it a text field being compared with `=`? See rule 3.
4. Strip `q/where` entirely and select just `fibery/id`. If that returns rows,
   the filter is the problem; bisect it.
5. If it still returns nothing, the database may genuinely be empty, or you
   may not have access. Check with `display_schema_capabilities`.

Empty is a real answer. Report it as empty rather than retrying blindly or
inventing a plausible result.
