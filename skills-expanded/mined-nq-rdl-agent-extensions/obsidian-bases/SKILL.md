---
name: obsidian-bases
license: CC-BY-4.0
description: >-
  Create and edit Obsidian Bases (.base files) with views, filters, formulas,
  and summaries. Use when working with .base files, creating database-like
  views of notes, or when the user mentions Bases, table views, card views,
  filters, or formulas in Obsidian.
compatibility: >-
  Obsidian 1.9+ with the Bases core plugin (table and cards views). List and
  map views need 1.10+; map views also need the official Maps plugin. Syntax
  checked against the obsidian-help source on 2026-09-29. Date arithmetic
  application-tested in Obsidian 1.13.7 on that date.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Obsidian Bases

A base is a `.base` file of YAML that defines filters, formulas, and views over
the notes in a vault. Bases syntax changes between Obsidian releases. When a
formula or view fails and being wrong would mislead, check the canonical pages:
[syntax](https://help.obsidian.md/bases/syntax),
[functions](https://help.obsidian.md/bases/functions), and
[views](https://help.obsidian.md/bases/views). If the user's Obsidian version
is older than the compatibility note, or those pages are unreachable, say
which syntax you could not confirm instead of presenting it as certain.

## Workflow

1. **Scope**: add `filters` to select notes (tag, folder, property, or date).
2. **Formulas** (optional): define computed properties under `formulas`.
3. **Views**: add one or more views with `order` listing the columns to show.
4. **Validate**: the file must parse as YAML. Every `formula.X` you reference
   must be defined, and each filter object has exactly one key. Apply the
   quoting rules below.
5. **Test in Obsidian**: open the `.base` file. A YAML error usually means a
   quoting problem.

## References

- [references/FUNCTIONS_REFERENCE.rst](references/FUNCTIONS_REFERENCE.rst):
  read when a formula or filter needs a function that is not in "Key functions"
  below (string, number, list, file, link, object, or regexp functions, and
  date fields). It also lists the default summary formulas.
- [references/examples.rst](references/examples.rst): read when you build a
  reading list, a daily-notes index, a cards gallery, a list view, or a map
  view, or when you want a second complete example to adapt.

## Schema

```yaml
# Global filters apply to ALL views in the base
filters:
  # A single filter string, OR an object with exactly ONE key: and, or, or not
  and:
    - 'status == "active"'
    - not:
        - 'file.hasTag("archived")'

formulas:                        # Computed properties usable in every view
  formula_name: 'expression'

properties:                      # Display settings per property
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"

summaries:                       # Custom summary formulas (`values` = the column)
  custom_summary_name: 'values.mean().round(3)'

views:
  - type: table                  # table | cards | list | map
    name: "View Name"
    limit: 10                    # Optional: limit results
    groupBy:                     # Optional: group results
      property: property_name
      direction: ASC             # ASC | DESC
    filters:                     # View filters follow the same rules
      and:
        - 'status == "active"'
    order:                       # Columns, in display order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Property -> summary formula name
      property_name: Average
```

## Filters

A filter is either one statement string or an object with **exactly one** of
`and`, `or`, or `not`. Each key holds a list of statements or nested objects.
View filters are combined with global filters using AND.

```yaml
# Single statement
filters: 'status == "done"'

# One key per object; nest objects for mixed logic
filters:
  or:
    - file.hasTag("book")
    - and:
        - file.hasTag("article")
        - 'priority > 3'
    - not:
        - file.inFolder("Archive")
```

Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`, and arithmetic
`+ - * / %`.

## Properties

1. **Note properties** from frontmatter: `note.author` or just `author`.
2. **File properties**: `file.name`, `file.basename`, `file.path`,
   `file.folder`, `file.ext`, `file.size`, `file.ctime`, `file.mtime`,
   `file.tags`, `file.links`, `file.backlinks` (slow; prefer `file.links`),
   `file.embeds`, `file.properties`.
3. **Formula properties**: `formula.my_formula`.

`this` is the base file in the main area, the embedding note when embedded, and
the active note when the base is in the sidebar. For example,
`file.hasLink(this.file)` lists backlinks of the active note.

## Formulas

```yaml
formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  created: 'file.ctime.format("YYYY-MM-DD")'
  days_old: '(now() - file.ctime).days'
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

### Key functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `date()` | `date(string): date` | Parse string to date (`YYYY-MM-DD HH:mm:ss`) |
| `now()` | `now(): date` | Current date and time |
| `today()` | `today(): date` | Current date (time = 00:00:00) |
| `if()` | `if(condition, trueResult, falseResult?)` | Conditional |
| `duration()` | `duration(string): duration` | Parse duration string |
| `file()` | `file(path): file` | Get file object |
| `link()` | `link(path, display?): Link` | Create a link |

### Duration: take a numeric field before rounding

In Obsidian 1.13.7, subtracting two dates gives a **Duration**, not a number.
The canonical syntax page still describes a millisecond difference.
For other versions, verify the result in the application before adapting a formula.
Duration does NOT support `.round()`, `.floor()`, or `.ceil()`. Take a numeric field first
(`.days`, `.hours`, `.minutes`, `.seconds`, `.milliseconds`), then apply number
functions.

`.days` measures **elapsed 24-hour days**, not calendar-date boundaries.
Local midnight to the next midnight can span **23 or 25 hours** across
daylight saving time (DST). Thus, `.days` can be fractional even for date-only inputs.
Choose rounding for the user's intended result.
`.round(0)` rounds to nearest, `.floor()` rounds down, and `.ceil()` rounds up.
For example, `-1.5` becomes `-1`, `-2`, or `-1`, respectively.
Do not describe elapsed days as a calendar-day count.

```yaml
# CORRECT
"(date(due_date) - today()).days"              # Elapsed 24-hour days
"(date(due_date) - today()).days.round(0)"     # Rounded days
"(now() - file.ctime).hours.round(1)"          # Hours, one decimal

# WRONG - will cause an error
"(now() - file.ctime).round(0)"                # Duration is not a number
"((date(due) - today()) / 86400000).round(0)"  # Division then round on a Duration
```

Add or subtract a duration string to shift a date: `today() + "7d"`,
`now() + "1 day"`, `date + "1M"`. Units: `y`, `M`, `w`, `d`, `h`, `m`, `s`
(or `year(s)`, `month(s)`, `week(s)`, `day(s)`, `hour(s)`, `minute(s)`,
`second(s)`).

### Guard optional properties and define what you reference

```yaml
# WRONG - errors on notes without due_date
"(date(due_date) - today()).days"
# CORRECT
'if(due_date, (date(due_date) - today()).days, "")'
```

Every `formula.X` in `order`, `properties`, or `summaries` needs a matching
entry under `formulas`. An undefined formula fails silently.

## Views

| `type` | Shows | Needs |
|---|---|---|
| `table` | Rows and property columns; supports `summaries` | 1.9 |
| `cards` | Grid of cards, gallery-style with an image property | 1.9 |
| `list` | Bulleted or numbered list | 1.10 |
| `map` | Pins on a map from latitude/longitude properties | 1.10 and the official Maps plugin |

Views can also set `limit`, `groupBy`, their own `filters`, and `summaries`.
Default summary names are `Average`, `Min`, `Max`, `Sum`, `Range`, `Median`,
`Stddev`, `Earliest`, `Latest`, `Checked`, `Unchecked`, `Empty`, `Filled`, and
`Unique` (input types are in the functions reference). The first view loads by
default. For cards, list, and map snippets, read
[references/examples.rst](references/examples.rst).

## YAML quoting rules

- Wrap formulas that contain double quotes in single quotes:
  `'if(done, "Yes", "No")'`.
- Quote strings that contain `:`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `#`, `?`,
  `|`, `-`, `<`, `>`, `=`, `!`, `%`, `@`, or `` ` ``.
- Use double quotes for plain strings such as view names: `"My View Name"`.

```yaml
# WRONG - colon in an unquoted string
displayName: Status: Active
# CORRECT
displayName: "Status: Active"

# WRONG - double quotes inside double quotes
label: "if(done, "Yes", "No")"
# CORRECT - single quotes wrap the double quotes
label: 'if(done, "Yes", "No")'
```

## Complete example: task tracker

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: "Days Until Due"
  formula.priority_label:
    displayName: Priority

views:
  - type: table
    name: "Active Tasks"
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.priority_label
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average

  - type: table
    name: "Completed"
    filters:
      and:
        - 'status == "done"'
    order:
      - file.name
      - completed_date
```

## Embedding bases

```markdown
![[MyBase.base]]

<!-- Specific view -->
![[MyBase.base#View Name]]
```
