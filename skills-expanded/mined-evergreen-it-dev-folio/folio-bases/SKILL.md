---
name: Folio Bases
description: Read and write Obsidian Bases (kind base) — saved queries over the pages of a space — with query_base and save_base; filters, formulas, views, an example.
version: "1.0.0"
tags: [folio, bases, properties, obsidian]
---

# Bases (`kind: base`)

A base is a `.base` file (Obsidian's YAML format): a **saved query over the
pages of a space**, not a store of its own. Its rows are pages (only those the
reader may open), its columns are their properties (front matter), file fields
and formulas. To change a value in a base you change that page's property
(`set_page_properties` with `merge: true`), not the base.

## Tools

| Tool | What it does |
|---|---|
| `read_page` (base id) | The YAML of the base |
| `query_base` | The rows of one view: values by column, groups, summaries (`view`, `limit`, `offset`) |
| `list_properties` | The property keys used in a space with their types and sample values — look here before writing a filter |
| `list_tags` | The tags of a space, for `file.hasTag(...)` filters |
| `save_base` | Create a base (`path`, e.g. `"projects/tasks.base"`) or replace one (`id` + `etag`) from the whole `yaml` |
| `set_page_properties` | Change the property a base shows, on the page itself |

## The file

```yaml
filters:                     # which pages are rows (optional): and / or / not of expressions
  and:
    - file.inFolder("projects")
    - file.hasTag("task")
    - 'status != "done"'
formulas:                    # computed columns, used as formula.<name>
  overdue: 'due < today()'
views:
  - type: table              # table, cards or list
    name: Open tasks
    order:                   # the columns, in order
      - file.name
      - owner
      - status
      - due
      - formula.overdue
    sort:
      - property: due
        direction: ASC
    groupBy:
      property: owner
      direction: ASC
    limit: 100
  - type: cards
    name: By owner
    order: [file.name, owner]
```

- **Properties**: a bare name or `note.<key>` is a front matter key
  (`status`, `note.status`); `file.name`, `file.folder`, `file.path`,
  `file.ext`, `file.tags`, `file.mtime`, `file.ctime`, `file.size`,
  `file.links`, `file.backlinks` are file fields; `formula.<name>` is a
  formula.
- **Expressions** (filters and formulas): comparisons `== != < > <= >=`,
  `&&`, `||`, `!`, arithmetic, strings in double quotes (quote the whole
  YAML line with single quotes when it contains `"` or `:`). Functions:
  `file.hasTag("a")`, `file.inFolder("dir")`, `file.hasLink("Page")`,
  `file.hasProperty("key")`, `today()`, `now()`, `date("2026-10-01")`,
  `if(cond, a, b)`, `list(x)`, `x.isEmpty()`, `x.contains("y")`,
  `number(x)`, `min()`, `max()`.
- A view's own `filters` narrow the base's top-level `filters` further.
- `summaries` per view map a column to a built-in summary — `Sum`,
  `Average`, `Min`, `Max`, `Median`, `Range`, `Earliest`, `Latest`,
  `Checked`, `Unchecked`, `Empty`, `Filled`, `Unique` — or to a key of the
  base's own top-level `summaries` (`summaries: { estimate: Sum }`).

## Writing a base

1. `list_properties` (and `list_tags` if tags matter) for the real key names
   and values — never guess them.
2. `save_base` with `space`, the whole `yaml` and `path` (a new base; put it
   under the folder of the page that is open now unless the user said
   otherwise) or `id` + `etag` (an existing base; the etag comes from a
   previous `save_base`; read the YAML with `read_page` first).
3. An invalid YAML comes back with its line number: fix and retry. Check the
   `preview` (the first view's first rows) or call `query_base`, then end the
   answer with a link to the base `[<title>](/s/<space>/p/<id>)`.
