---
name: gutenberg-build-page
description: >
  Build or edit a page in the live Gutenberg block editor with Novamira Visual
  tools. Use when creating or changing native block content (headings,
  paragraphs, lists, images, columns, groups) in the open block editor.
editor: gutenberg
---

# Building Gutenberg pages in Novamira Visual

You are editing live inside the open Gutenberg editor. Changes apply directly
in the editor and save with the page. There is no pending queue and no
finalization step, and you never write `post_content` or block markup through
`execute-php` or another backend tool.

## Start in the editor

There is no backend tool for page content. Open the page in its editor first; to
create a page, open a new page in the editor. The block tools below only exist
once the editor is open.

Before changing anything, read `get_page_structure` to see the current block
tree (clientIds, names, nesting). Discover what a block accepts with
`list_block_types` and `get_block_schema`, and read a single block's values with
`get_block_attributes`. Build from a block's real attributes, supports, and
preset slugs, not from guesses.

## Compose with native blocks

Use the most specific native block: `core/heading` (set `level`),
`core/paragraph`, `core/list` + `core/list-item`, `core/image`, `core/quote`,
`core/buttons` + `core/button`, `core/table`, `core/code`, `core/separator`.
Express layout and nesting with `core/group` and `core/columns` + `core/column`
and `inner_blocks`, not HTML.

If a registered third-party block fits what you are building (WooCommerce,
Kadence, and similar), use it by name with its attributes instead of
reproducing its output.

Use `core/html` only for a small fragment with no native equivalent, and keep it
minimal. Never wrap whole sections, or the whole page, in `core/html` or inline
styles. Raw HTML is not visually editable and defeats native editing.

## Tools

- `create_block`: add a block. Pass `inner_blocks` for containers like
  `core/columns`. Returns the new `clientId`.
- `update_block`: change attributes on an existing block by `clientId`.
- `replace_inner_blocks`: rebuild a container's children in one call.
- `move_block` / `delete_block`: reorder or remove blocks.
- `get_page_structure`, `get_block_schema`, `list_block_types`,
  `get_block_attributes`, `get_editor_settings`: read state and schema.
- `save` persists the page; `undo` / `redo` step the editor history.

## Text alignment

To align a block's TEXT (left, center, right), pass `text_align` to
`create_block` or `update_block`. The tool stores it where this block keeps text
alignment. Do not use the `align` attribute for text: `align` is block WIDTH
(wide/full), and setting it to left/center/right does not move the text.

## Colors, sizes, spacing

Prefer the theme's preset slugs from `get_block_schema` / `get_editor_settings`
(for example a `textColor` slug, a named font size) over hardcoded hex values
and pixel sizes, so the page stays consistent with the theme and editable.

## Verify

After building, re-read `get_page_structure` to confirm the block tree matches
the intent, then `save`.
