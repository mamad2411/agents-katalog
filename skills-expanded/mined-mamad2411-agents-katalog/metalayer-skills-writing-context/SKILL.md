# Writing Context

Format rules for writing .md files to the vault. Follow these exactly when creating or editing any vault file.

## Verify Before Writing

Never write a context file based on assumptions. Every claim in a context file — grain, keys, cardinality, column behavior, aggregation logic, filter conditions, join paths, value lists, dedup behavior — must be verified against real data before you write it.

Find the source file for the relevant view (e.g., `source: [[snowflake]]` on the view → read `snowflake.md`). The source file tells you how to run queries — which tool, command, or MCP server to use. Use it.

Examples:

- `SELECT COUNT(*), COUNT(DISTINCT id) FROM table` — verify grain and primary key uniqueness.
- `SELECT DISTINCT status FROM table ORDER BY 1` — verify dimension values.
- `SELECT a.key, COUNT(*) FROM a JOIN b ON ... GROUP BY 1 HAVING COUNT(*) > 1` — verify cardinality and join fanout.
- `SELECT column, COUNT(*) FROM table GROUP BY 1 ORDER BY 2 DESC LIMIT 10` — verify what a column actually contains.
- `SELECT SUM(amount) FROM table WHERE status = 'completed'` — verify that your metric SQL produces reasonable numbers.

This applies to every write — imports, manual edits, and learning-phase proposals. If the source metadata says something (e.g., "this column is a primary key"), verify it. Source metadata is often wrong or stale.

If you cannot run a query (no warehouse access), say so explicitly and do not write the file. The only exception is if the user explicitly tells you to write it anyway — in which case, mark every unverified claim with `# UNVERIFIED` in the body text.

## No Dangling References

Never write a file that references objects that don't exist. If your file contains `[[wikilinks]]` — in frontmatter or body — every referenced object must either already exist in the vault or be created as part of the same batch.

For example: if you're writing a relation with `from: [[login.workspace_id]]` and `to: [[workspaces.id]]`, you must also create the field files `login.workspace_id.md` and `workspaces.id.md` if they don't already exist. Verify each one against real data before writing.

This means writes often come in dependency chains:
1. Source files first (views need them).
2. View files next (fields need them).
3. Field files (relations reference them).
4. Relations, concepts, topics, lore (reference the above).

When writing a batch, resolve the full dependency tree before presenting proposals. The user should never approve a batch that leaves dangling references.

## General Rules

- Every file starts with YAML frontmatter between `---` fences.
- `type` is required in every file's frontmatter.
- The filename IS the identity. It must be unique across the entire vault. No two files share a name.
- Field files use dotted names: `{view}.{field}.md` (e.g., `orders.total_revenue.md`).
- Organize files into folders however you want — folder structure is cosmetic, not semantic.
- All names: lowercase, underscores for spaces, short but descriptive.

## Wikilink Conventions

Use [[wikilinks]] everywhere references appear:

- **In frontmatter**: `view: "[[orders]]"`, `from: "[[orders.customer_id]]"`, `to: "[[customers.id]]"`. **Always quote wikilinks in YAML frontmatter** — unquoted `[[name]]` gets parsed by YAML as a nested list, breaking the reference. The tooling auto-fixes this, but quoting is the correct convention.
- **In body text**: "This field is the counterpart to [[customers.lifetime_value]]."
- **In SQL (composed metrics)**: `${[[orders.total_revenue]]}` resolves to that field's SQL expression at query time.
- **${TABLE}**: in field SQL, `${TABLE}` resolves to the parent view's `table` value. Always use this instead of hardcoding the table name.

## Frontmatter vs Body

- **Frontmatter**: structured data that tools parse. Types, references, SQL, aggregation, filters, lists.
- **Body**: explanations, caveats, business context, usage notes. Written for the LLM and for humans.

Put business logic in frontmatter (SQL, filters). Put business *context* in the body (why this metric exists, when to use it vs another, known data quality issues).

**Never store temporal data.** The vault stores structure (definitions, rules, relationships), not data points. "Revenue is SUM(amount) WHERE status = completed" belongs in the vault. "Revenue was $2.3M last quarter" does not — it will be stale and cause hallucinations. If it would be wrong next week, query for it fresh instead.

## Type: source

Defines how to access a data warehouse or database. A thin pointer — connection details stay in the tool's own config, not here.

```yaml
---
type: source
tool: "snow sql -q \"${SQL}\" -c zenlytic"
---

# Snowflake (Zenlytic)

Uses the Snowflake CLI with the `zenlytic` connection profile.
Connection details are in ~/.snowflake/connections.toml.
```

Required: `type`, `tool`.

`tool` is a command template. `${SQL}` is replaced with the actual query at execution time. The agent runs this command to verify data and execute queries.

For MCP-backed sources:

```yaml
---
type: source
mcp: snowflake_mcp
---

# Snowflake via MCP

Use the Snowflake MCP server tools to run queries.
```

When `mcp` is set instead of `tool`, the agent uses the named MCP server's tools directly.

Body: describe what this source connects to, any quirks, default database/schema, access notes.

**Sources must be created before views.** Every view must reference a source with `source: [[source_name]]`. The agent resolves the source to know how to query.

## Type: view

Represents a table or data source.

```yaml
---
type: view
source: [[connection_name]]
table: schema.table_name
primary_key: id
one_row_means: "one completed order"
dedup_key: id
restricted_columns:
  - ssn
  - credit_card_number
---
```

Required: `type`, `source`, `table`.
Important: `primary_key`, `one_row_means`.

`source` must match a source name defined in `config.yaml`. This tells the agent which connection to use for verification queries and SQL execution. Do not create a view without a valid source.
Optional: `dedup_key`, `restricted_columns`.

For MCP-backed views (API sources):

```yaml
---
type: view
server: mcp_server_name
tool: tool_name
tool_params:
  param1: value1
---
```

Body: describe what this table contains, its grain, known quirks, when it refreshes.

## Type: field

Represents a column, calculated field, or metric on a view.

```yaml
---
type: field
view: [[orders]]
kind: metric
sql: SUM(${TABLE}.amount)
agg: sum
filters:
  - ${TABLE}.status = 'completed'
---
```

Required: `type`, `view`, `kind`, `sql`.
Important: `agg` (for metrics), `filters`.
Optional: `validation`, `time_granularities`, `semi_additive`, `parent`, `hidden`, `tags`.

**kind values**:
- `identifier`: primary key or foreign key.
- `dimension`: categorical or descriptive column.
- `time`: date or timestamp column. Set `time_granularities` (e.g., `[day, week, month, quarter, year]`).
- `metric`: aggregated measure. Requires `agg` (sum, count, count_distinct, avg, min, max, median, custom).

**filters**: default filters applied whenever this metric is used. Express as SQL conditions using ${TABLE}.

**validation**: a natural-language rule checked against results whenever this field appears. Catches domain-specific errors. Example: `validation: "should always be positive; if negative, check for refund double-counting"`. The reflection phase reads this and checks the result set. Works the same as `validation` on lore, but scoped to this one field.

**semi_additive**: for metrics that cannot be summed across certain dimensions (e.g., account balances across time). Specify the dimension that blocks summation.

**hidden**: `true` to exclude from search results. Use for intermediate calculated fields.

For API-backed fields:

```yaml
api_property: response.data.field_name
api_type: string
```

Body: explain what this field means in business terms, when to use it vs similar fields, known caveats.

**Values**: for dimensions with a known set of values, list them under a `## Values` section in the body. This helps the LLM map user terms to actual values. For high-cardinality dimensions, note that instead of listing all values.

```markdown
## Values

- pending
- completed
- cancelled
- refunded
```

## Type: relation

Represents a join between two views.

```yaml
---
type: relation
from: [[orders.customer_id]]
to: [[customers.id]]
cardinality: many_to_one
join_type: left
label: "order to customer"
---
```

Required: `type`, `from`, `to`, `cardinality`.
Important: `join_type` (defaults to `left`), `label`.
Optional: `join_sql` (for complex join conditions beyond simple equality), `always_join`, `relation_kind`, `tags`.

**cardinality values**: `one_to_one`, `one_to_many`, `many_to_one`, `many_to_many`.

**join_sql**: override the default equi-join with a custom SQL ON clause. Use when the join involves multiple keys, date ranges, or other complex logic.

**always_join**: `true` to always include this join, even if no fields from the joined view are selected. Rare — use for security filters or required context.

Body: explain the relationship in business terms. Note any caveats (e.g., "not all orders have a customer — guest checkouts have null customer_id").

## Type: concept

Groups related fields across views under a shared name.

```yaml
---
type: concept
fields:
  - [[orders.total_revenue]]
  - [[returns.refund_amount]]
  - [[subscriptions.mrr]]
extends: [[revenue_base]]
filter: ${TABLE}.is_active = true
---
```

Required: `type`, `fields`.
Optional: `extends` (inherit fields from another concept), `filter`.

Body: explain what this concept represents and when to use it.

## Type: topic

Entry point for a domain. Resolves to a full set of context via chain: topic -> concepts -> extends -> fields -> views -> relations.

```yaml
---
type: topic
concepts:
  - [[revenue]]
  - [[customers]]
relations:
  - [[order_to_customer]]
views:
  - [[orders]]
  - [[customers]]
---
```

Required: `type`.
Important: `concepts`, `relations`, `views`.

Body: describe this domain, common questions it answers, which metrics matter most.

## Type: lore

Cross-cutting guidance that applies across multiple objects.

```yaml
---
type: lore
when: always
---
```

Or with conditional triggers:

```yaml
---
type: lore
when:
  fields:
    - [[orders.total_revenue]]
    - [[orders.net_revenue]]
---
```

```yaml
---
type: lore
when:
  views:
    - [[orders]]
---
```

```yaml
---
type: lore
when:
  description: "questions about revenue reconciliation"
---
```

Required: `type`, `when`.
Optional: `validation`.

**when values**:
- `always`: injected into every query context. Use sparingly — keep under 5 always-lore files.
- `{fields: [...]}`: injected when any listed field is in context.
- `{views: [...]}`: injected when any listed view is in context.
- `{description: "..."}`: injected when the search matches the description semantically.

**validation**: a natural-language rule that query results should be checked against during reflection. Examples:

```yaml
---
type: lore
when:
  fields:
    - "[[orders.revenue]]"
validation: "monthly revenue should be positive and under $1B"
---

Revenue should always be positive. If monthly revenue exceeds $1B, the query likely has a fanout or missing filter.
```

```yaml
---
type: lore
when:
  views:
    - "[[login]]"
validation: "login counts should exclude internal workspaces and test accounts"
---

Always filter out internal workspaces and internal email domains when counting logins for customer metrics.
```

Validation lore is loaded during reflection and checked against the result set. If a validation rule is violated, the agent flags it before presenting results. This catches domain-specific errors that generic plausibility checks miss.

If guidance applies to only one field or view, put it in that file's body instead of creating a lore file. Lore is for cross-cutting rules that span multiple objects.

Body: the actual guidance. Be direct and specific. State what to do and what not to do.

## Naming Conventions

Filenames follow the pattern `{name}__{type}.md`. The `__{type}` suffix is stripped by the resolver — wikilinks use just the name part.

| Type | Filename pattern | Example | Wikilink |
|------|-----------------|---------|----------|
| source | `{name}__source.md` | `snowflake__source.md` | `[[snowflake]]` |
| view | `{name}__view.md` | `orders__view.md` | `[[orders]]` |
| field | `{view}.{field}__field.md` | `orders.status__field.md` | `[[orders.status]]` |
| relation | `{name}__relation.md` | `orders_to_customers__relation.md` | `[[orders_to_customers]]` |
| concept | `{name}__concept.md` | `customer__concept.md` | `[[customer]]` |
| topic | `{name}__topic.md` | `order_analysis__topic.md` | `[[order_analysis]]` |
| lore | `{name}__lore.md` | `revenue_excludes_tax__lore.md` | `[[revenue_excludes_tax]]` |

General rules:
- All lowercase.
- Underscores for spaces: `total_revenue`, not `totalRevenue` or `Total Revenue`.
- Views match table names where practical: `orders` for `schema.orders`.
- Relations describe the join: `orders_to_customers`.
- Lore describes the rule: `revenue_excludes_tax`, `use_completed_orders_only`.
- Fields use dotted names: `{view}.{field}` (e.g., `orders.total_revenue`).

Files without the `__{type}` suffix still work — the resolver handles both conventions. But prefer the suffix for new files.
