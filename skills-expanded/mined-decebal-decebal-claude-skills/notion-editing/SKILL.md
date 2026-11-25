---
name: notion-editing
description: >-
  Change a page in a Notion documentation space with the Notion connector — any page, not only a
  specification. Covers checking write access, the literal-match rules that make a content edit fail
  silently, atomicity and retries, and the operations this connector does not have. Triggers - "update
  the Notion page", "edit the registry page", "my update_content didn't match", "add a row to the
  registry", "no matches found", "can you delete that page", "move these pages into Archive".
---

# Editing Notion

Applies to every page in the space. Registries, release databases and proposal databases take the same
edits and fail the same ways; `notion-specification` governs what a specification says, not how any page
is changed. Where the space has a style-guide page, the human-facing version of these rules belongs there
— this file carries the tool names and the call shapes, which only an agent needs.

## Before the first write

`get_tool_access` with `{}` returns the access map. `create_pages` and `update_page` present mean the
direct route is open; absent means the work lands by paste and `notion-preview` owns the handoff.

Narrow the call with the **underscored** names from that map — `create_file_upload`, not
`create-file-upload`. Hyphenated names return `{}`, which is indistinguishable from a revocation and is
easily misread as one.

Write access alone is not authorisation. A page other teams read is reviewed by its owner before a write,
which is what `notion-preview` exists for.

## Call shapes

| Doing | Call |
|---|---|
| New page, or a database row with its body | `notion-create-pages`, properties and `content` in one call |
| Targeted edit | `notion-update-page` with `command: "update_content"` and `content_updates` |
| Wholesale replacement | `notion-update-page` with `command: "replace_content"` |
| Append | `notion-update-page` with `command: "insert_content"` and `position` |
| Relocate | `notion-move-pages` |
| Schema or view change | `notion-update-data-source`, `notion-create-view` — see `notion-database` |

The markdown dialect is Notion-flavoured, not CommonMark. Read `notion://docs/enhanced-markdown-spec`
through `notion-fetch` before writing content: callouts, toggles, mentions, columns and inline databases
all have spellings there, and a `<page>` tag **moves** an existing page rather than linking to it.

## What bites

Each of these is silent — the call succeeds, or fails with a message naming the wrong cause.

- **Address the block, not a span across its children.** A fenced code block matches when the backticks are
  in `old_str`; a table when `<table>` and `</table>` are. An `old_str` starting inside one child and ending
  inside another never matches, which is what makes bare table rows and numbered list items awkward — each
  is its own block. The same holds for a toggle, a callout and a column list.
- **An empty `new_str` deletes**, a whole block as readily as a single row.
- **A table row whose only cell content is a mention does match** on its own. A mention *inside* a numbered
  list item does not — anchor on plain text there.
- **Stored text is not the text you wrote.** Some bold-plus-code runs are stored with extra asterisks.
  `notion-fetch` the page and copy the target out of the response.
- **An edit that makes two rows identical breaks the next anchor**, and the error reads "No matches found"
  rather than naming the ambiguity. Order the operations so no intermediate state has duplicate rows.
- **The call is atomic.** One failing operation rolls back the ones that matched, so there is no partial
  edit to repair.
- **A large `create-pages` payload can drop the socket** after the rows are created. Query the keys back
  before retrying, or the retry duplicates every row that landed.
- **`<database url="…">` in the content of a *new* page destroys that database** rather than moving it.
  Use `notion-move-pages`.
- **No delete or archive operation exists.** Move unwanted pages to an Archive page and let a human bin
  them — and count the inbound mentions first, because binning a page leaves every mention of it intact
  and silently dead.

## Related

`notion-preview` for the review gate before a write. `notion-database` for schema, views and registries.
`notion-specification` for what a specification says. `notion-diagram` for figures.
