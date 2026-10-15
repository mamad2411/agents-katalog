---
name: sense-bases
description: "Translate an Obsidian Bases .base file into sense SQL that returns the same rows. Use when asked to convert, import, or reproduce a .base file (or a Bases view, filter, or formula) with sense, or when a markdown tree contains .base files whose views someone wants queryable outside Obsidian."
---

# sense-bases

A `.base` file is YAML: filters selecting notes, formulas computing values, and views ordering
and grouping them. Obsidian evaluates it against its own metadata cache; sense holds the same
data in SQL tables. Every Bases construct that selects or computes rows has a SQL equivalent.
What has none is presentation (`columnSize`, card layout) -- those change pixels, not rows, so
a translation loses nothing by ignoring them.

Translate one view to one query: base-level `filters` AND the view's `filters`, the view's
`order`/`sort`/`limit` as the SELECT list, ORDER BY, and LIMIT. A base with four views becomes
four queries; saving them under the base's name in `sense.config.json`'s `queries` block keeps
them runnable as `sense <name>`. The general query surface is the `sense` skill; this one only
maps Bases constructs onto it.

## Properties

| Bases | sense | notes |
|---|---|---|
| `note.field` / bare `field` | `f.<field>` | frontmatter column, same name |
| `file.name` | `basename(f.path, '.md')` | the Name column: no directory, no extension |
| a name with extension | `basename(f.path)` | the suffix arg is Unix basename's: present, stripped |
| `file.folder` | `f.path LIKE 'Folder/%'` | for `inFolder("Folder")` |
| `file.ext` | `'md'` | sense indexes only markdown |
| `file.size` | `f._size` | bytes |
| `file.mtime` | `datetime(f._mtime / 1000, 'unixepoch')` | stored as ms |
| `file.ctime` | `datetime(f._ctime / 1000, 'unixepoch')` | see the caveat below |
| `file.tags` | the `tags` table | frontmatter + inline `#tags`, deduplicated, Obsidian's grain |
| `file.links` | `links WHERE embed = 0` | one row per distinct written target |
| `file.embeds` | `links WHERE embed = 1` | |
| `file.backlinks` | `links WHERE dst = f.path` | |
| `this` | a bound `?` | see below |

`file.ctime` is the filesystem's creation time. A `git clone` or a copy resets it, so on a
tree that arrived as a checkout, every ctime is the checkout date and age formulas are wrong
about authorship without being wrong about the filesystem. `map` warns when modification
times have this shape; creation times share it.

## Predicates

| Bases | sense |
|---|---|
| `==` `!=` `>` `<` `>=` `<=` | same |
| `&&` `\|\|` `!` | `AND` `OR` `NOT` |
| `and:` / `or:` / `not:` filter blocks | parenthesized `AND` / `OR` / `NOT` |
| `field.isEmpty()` | `(f.field IS NULL OR f.field IN ('', '[]', '[null]'))` |
| `file.hasTag("book")` | `EXISTS (SELECT 1 FROM tags WHERE tags.path = f.path AND (tag = 'book' OR tag LIKE 'book/%'))` |
| `file.hasLink("Note")` | `EXISTS (SELECT 1 FROM links WHERE src = f.path AND dst = 'Note.md')` |
| `list.contains(x)` | `EXISTS (SELECT 1 FROM json_each(f.list) WHERE value = x)` |
| `string.contains(x)` | `instr(f.string, x) > 0` |
| `list.containsAny(...)` | the `json_each` EXISTS with `value IN (...)` |
| `/regex/.matches(x)` | no SQLite regex; `LIKE`/`GLOB` cover anchored and wildcard shapes |
| `value.isType("object")` | `json_each`'s own `type` column: `... FROM json_each(f.field) j WHERE j.type = 'object'` |

A field no note in the tree declares has no column at all, so a filter naming it errors with
`no such column` instead of treating every row as empty. Obsidian's evaluator returns empty
for unknown properties; SQL does not. Dropping the clause states the same thing the error
did, and `SELECT name FROM pragma_table_info('frontmatter')` lists what exists.

`isEmpty()` has four true cases because empty is stored three ways: NULL (key absent), `''`
(empty string value), `'[]'` (a list written `[]`), and `'[null]'` (a list key above a bare
`-`). Obsidian's `isEmpty()` is true for all of them; `IS NULL` alone finds only the first.
The IN list is the whole test -- `json_array_length()` is not: it reads `'[null]'` as length
1 and throws on plain strings. The same trap inside a list: `json_each` hands a string member
to `value` as plain text, so `json_type(value)` throws `malformed JSON` on it; the scan's own
`type` column is the discriminator.

`contains(link("Movies"))` compares against a link value. In frontmatter, a list of links
holds the written text, so the `json_each` comparison value is the literal `[[Movies]]`.
`hasLink` compares resolved paths: `links.dst` is the resolved target (`NULL` for dead
links), so the comparison value is the target's path, not its display name.

sense's own `has(field, x)` is looser than both `contains` variants: exact membership on JSON
arrays but substring on strings, so `has(f.status, 'active')` also matches `inactive`. It
reads shorter when the field is known to be a list; the `json_each` form is the exact
translation.

## Formulas

Formulas are SELECT expressions. The Bases functions map onto SQLite's:

| Bases | sense |
|---|---|
| `if(c, a, b)` | `iif(c, a, b)` or `CASE WHEN` |
| `now()` / `today()` | `datetime('now')` / `date('now')` |
| `date(x)` | `datetime(x)` |
| `(date1 - date2).days` | `julianday(date1) - julianday(date2)` |
| `(now() - acquired).months` | `(julianday('now') - julianday(f.acquired)) / 30.44` |
| `x.round(n)` / `x.toFixed(n)` | `round(x, n)` / `printf('%.2f', x)` |
| `d.format("YYYY-MM-DD")` | `strftime('%Y-%m-%d', d)` |
| `x.toString()` | `CAST(x AS TEXT)` |
| `list.length` | `json_array_length(f.list)` on a JSON column, a COUNT subquery on a table |
| `list(a).filter(list(b).containsAny(value)).unique()` | an EXISTS-joined subquery; worked example in EXAMPLES.md |

Bases durations are typed; SQL date arithmetic is julianday day-fractions. A formula chaining
duration fields (`.days.round()`) flattens to arithmetic on the julianday difference.

A formula referencing another formula becomes a CTE layer: SQL cannot read a SELECT alias in
the same SELECT list, so each dependency level computes its formulas as columns and the next
level reads them (`WITH t AS (SELECT ..., <level-1 formulas> FROM frontmatter) SELECT ...,
<level-2 formulas> FROM t`). A five-formula chain is however many *levels* it has, not five
CTEs -- formulas that only read base columns share one layer.

## Views

- `sort:` (multi-key, each with direction) -> `ORDER BY a DESC, b ASC`. `limit:` -> `LIMIT`.
- `groupBy` does not collapse rows -- Obsidian shows every row bucketed under headers with
  per-group summaries. The SQL producing the same rows and numbers is ordering plus window
  functions, not GROUP BY:

  ```sql
  SELECT f.path, f.status, f.days,
         AVG(f.days)  OVER (PARTITION BY f.status) AS group_avg,
         COUNT(*)     OVER (PARTITION BY f.status) AS group_n
  FROM frontmatter f WHERE f.days IS NOT NULL
  ORDER BY f.status, f.days DESC
  ```

  A collapsed one-row-per-group report is plain `GROUP BY` -- that is a different result than
  the Bases view shows.
- View `summaries` (Sum, Average, Median via ordering, Unique, Filled, Checked) are the
  matching aggregates, windowed as above to keep the rows, or a separate aggregate query.

## `this`

`this` is the note the base is evaluated against: the embedding note, or Obsidian's active
pane. sense has no pane, so the caller supplies the path as a bound parameter -- `sense sql
"..." <path>`, or a saved query run as `sense <name> <path>`. A CTE keeps it single-bind:

```sql
WITH me AS (SELECT ? AS p)
```

and every `this.file.*` expression joins `me`. The full Related.base translation in
EXAMPLES.md is the worked case: link overlap, mutual-link filters, and the shared-target list
via `GROUP_CONCAT`, all from one bound path.

## Not translatable, and why it costs nothing

- `columnSize`, card/table/list/map chrome: pixel layout over the same rows.
- Obsidian choosing `this` from the active pane: there is no pane; the path parameter is the
  resolution.
- Live re-evaluation as files change: every sense query reconciles against the filesystem
  first, so the freshness is already there; nothing re-renders on its own.
