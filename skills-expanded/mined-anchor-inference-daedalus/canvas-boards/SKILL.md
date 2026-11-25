---
name: canvas-boards
description: Draw clear, editable canvases in Daedalus (flows, plans, architectures, decision trees, mind maps) with the Canvas tools, and link the operator to the board.
requires: canvas
---
# Canvas boards

A canvas is a living board the operator opens at `/app/canvas/<id>` and edits by hand: cards with
Markdown, groups, links and arrows between card sides, in Obsidian's JSON Canvas format. It is not a
picture. The tools compute card sizes, placement and edge sides; you decide the content.

## Workflow

1. **Lay out first.** Anything with flow or structure (steps, components, a decision tree) goes
   through `CanvasCreate` with `nodes` and `edges`, or `CanvasEdit` with `layout_graph` to add a laid-out
   part beside an existing board. Do not place cards by coordinates unless asked.
2. **Tweak with `CanvasEdit`:** change a card's words (`{id, text}`), recolour it (`{id, color}`), add
   a card (it goes right of the board, sized for its words), connect two cards (`edges: [{from, to,
   label}]`), group cards (a `group` node whose box surrounds them), delete (`delete_ids`; a card's
   edges go with it, a group's contents stay).
3. **Read before every edit.** `CanvasRead` gives the version, the ids, places and what each group
   holds. Pass that `version`. The operator may be moving cards right now: your edit still saves when
   it touches other items, and is refused only when the operator changed the same item; then read
   again and redo the change on what is there.
4. **Link it.** Finish with a markdown link in this form:
   `[Payment flow](/app/canvas/0123456789abcdef0123456789abcdef)`. The id is 32 hex characters; the
   chat turns that form into an in-app link.

A message from the canvas's comment bar names the canvas and its id, and may quote an element of a
frame the operator pointed at: read the canvas and act on it there.

## Content

- **Short card text:** a bold first line, detail below (`"**Validate order**\nschema + stock"`).
  Cards are Markdown: lists, links and code work.
- **At most about 15 cards** per board section. Split a large system into groups, or an overview
  board and one board per part.
- **One direction per flow:** `right` for processes and pipelines, `down` for hierarchies and
  decision trees. A loop back is fine; label it.
- **Edge labels** only where they carry meaning: the branch of a decision (`yes` / `no`), a protocol,
  a data name.
- **Stable, readable ids** (`api`, `queue`, `worker`), so later edits can name them.

## Colours

`color` is a preset `"1"` to `"6"` (red, orange, yellow, green, cyan, purple), which each app draws in
its own shade, or `#rrggbb`. Use a handful, consistently: green for the happy path's end, red for
failure or risk, yellow for a decision or something needing attention, cyan or purple for extra groups
when a legend card says what they mean. Leave most cards uncoloured.

## Scope

A canvas belongs to this chat (the default) or to its project (`scope: "project"`), where every chat of
the project sees it. Choose the project for a board the whole project works from (a roadmap, an
architecture); the chat for anything that belongs to this conversation alone.
