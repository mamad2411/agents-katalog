---
name: srs-writing
description: Draft and change an SRS document of the hub to its template, keeping every code, and propose the change with the tool srs__propose as a version members approve.
---

# Writing an SRS to its template

A document is a list of items, each with a key the hub gives and keeps. Its template (`srs-basic` unless the plugin's
config names another) says which headings and table rows are which kind of item:

| Kind | Heading or row | Code |
|---|---|---|
| section | a numbered heading (`# 2. Use Case Specifications`), Actors, Site Map, Open Items | none |
| glossary | a heading with Definitions, Glossary, Terms, Abbreviations or Acronyms | none |
| use_case | `UC <AREA>-<n>: <title>` | `UC ORD-3` |
| business_rule | `Step (2): BR <AREA><n>-<m> – <title>`, under its use case | `BR ORD3-2` |
| screen | `Screen: <title>` | `SCR-<n>`, given by the hub |
| cbr | a row of the table under Common Business Rules | `CBR 2` |
| nfr | a row of a table whose first cell is a requirement's code | `NFR-SEC-01` |

The plugin's config may replace the pattern of a kind of code; `srs__propose` answers with the pattern when a code
does not match.

## Codes

- A code is unique in the project, across documents, aliases included, and is never given again, even after its item
  was dropped.
- Never change, renumber or reuse the code of an item that has one. Rename it, move it or rewrite its body instead;
  its code stays.
- A new use case or business rule takes the next number of its area: search the area's codes with `srs__search`
  (such as `UC ORD`) and take one above the highest. A new screen takes no code: the hub gives `SCR-<n>`.
- A table row's first cell is its code: when you edit a `cbr` or an `nfr`, keep that cell as it is.

## A use case

A use case's body holds its fields as the document's other use cases do: the actor, the preconditions, the main flow
as numbered steps, the alternative flows and the postconditions. Where the document writes Intent, Context and
Expectation rows, write those: the intent is what the actor wants and why, the context what the work must know (systems,
data, constraints, decisions taken), the expectation the checks that tell the use case is done, for the main flow and
each alternative flow. Fill every field the project requires (`required_use_case_fields`). Its business rules are headings under it that name
the steps they apply to, `Step (2)` or `Steps (2, 2.1)`. Link the screens it shows with refs `uses_screen`.

## Proposing

`srs__propose` takes the document, the version you read (`base_version`), a summary, and the changes:

```json
{
  "document": "shop-srs",
  "base_version": 4,
  "summary": "UC ORD-2: retry a declined payment twice, as the member asked",
  "changes": [
    {"key": "3f9a1c07b2d4", "body": "The whole new Markdown body of the item"},
    {"key": "77c02e5a90f1", "title": "Pay for an order with a saved card"},
    {"new": {"kind": "business_rule", "title": "Retry limit", "code": "BR ORD2-3", "parent": "3f9a1c07b2d4", "steps": ["4"]}}
  ]
}
```

- A change names an item by `key` and gives what changes: `title`, the whole `body`, `steps` of a business rule, or
  the whole list of `refs`. A new item is `new`, with its kind, title, body, code, parent (key) and the sibling it
  follows (`after`, key).
- There is no change that drops an item: tell the member that a member of the project drops it.
- When the item changed since `base_version`, the hub answers a conflict with the item's text now: read it again,
  redo the change on it and propose again.
- The version goes to review at once, written as the member who asked, so another member approves it, unless the
  project turned self-approval on (the tool's answer says so). Tell the member its number, what it changed, the
  comparison link and who may approve it.
