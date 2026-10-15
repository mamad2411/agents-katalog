---
name: hyday-whiteboard
description: Create, edit, list, query, inspect, and lay out Hyday whiteboards through the hyday-whiteboard MCP server. Use whenever the user adds, modifies, moves, deletes, lists, or asks about whiteboard cards, sticky notes, groups, or connections — or wants to inspect what's on a board, build a layout from existing notes, or organize notes visually — or mentions whiteboard, canvas, board, sticky note, group. Common triggers: "幫我做張白板", "列出我的白板", "把這幾篇筆記放上白板", "白板上有什麼", "整理筆記成白板". Requires the `hyday-whiteboard` MCP server to be configured (see installation below).
---

# Hyday Whiteboard Skill

> **First time in this conversation? Run Step 0 from `hyday-vault-layout` to find the vault root.** The whiteboard MCP server below resolves it for you automatically (from `~/Library/Application Support/Hyday/settings.json` on macOS or `%APPDATA%\Hyday\settings.json` on Windows — `journalPath` field), so as long as the server is configured and the user has opened Hyday once, you're fine. If you ever need to call the server with `--data-root`, see Step 0 in `hyday-vault-layout` for the lookup chain.

Hyday's **Whiteboard** is a 2D canvas where the user pins note cards, sticky notes, and grouping containers, and draws connections between them.

Unlike notes (which are plain `.md` files), whiteboard state lives in a sidecar JSON at `<DATA_ROOT>/.hyday/whiteboards-v2.json`. You operate it through the **`hyday-whiteboard` MCP server**, which exposes 12 tools.

## Installation (one-time)

Before this skill works, the user must configure the MCP server in their agent's MCP config. See `mcp-servers/hyday-whiteboard/README.md` in this repo for the exact steps. The short version:

1. `npm install` inside `mcp-servers/hyday-whiteboard/`.
2. Add an entry to `.mcp.json` pointing `node` at `whiteboard-server.cjs`.
3. The server auto-detects the Hyday vault from `settings.json`; override with `--data-root` if needed.

Once configured, the agent has access to tools named `mcp__hyday-whiteboard__*` (or similar — the exact prefix depends on the agent).

## What's on a whiteboard

A board contains zero or more **items** and zero or more **connections**.

### Item kinds

| Kind | What it is | Created with |
|------|-----------|--------------|
| `note` (card) | A card linked to an existing `.md` note. Shows the note's title and a preview. | `addNoteToWhiteboard` or `buildWhiteboardLayout` |
| `sticky` | A free-form text snippet that lives only on the board — no backing `.md` file. | `addStickyNote` |
| `group` | A visual container that wraps other items under a labelled header. | `createWhiteboardGroup` or `buildWhiteboardLayout` |

### Connections

Edges between two items. The server auto-picks the best handle (top/bottom/left/right) for the shortest path.

## Coordinate system

- `x` increases to the right, `y` increases **downward** (top-left is `0,0`).
- Positions can be negative — the canvas extends infinitely.
- Item position is the **top-left corner** of the item's bounding box.

## Workflow: build a board from scratch (preferred path)

**Use `buildWhiteboardLayout`.** It takes groups of note IDs plus optional connections and handles **all** positioning — column distribution, group sizing, card heights, connection handles. This avoids overlapping cards and bad spacing.

1. Make sure every note you want as a card exists as a `.md` file in the vault (see `hyday-markdown` and `hyday-vault-layout`). Get each note's `fileId` (filename without `.md`).
2. Group the notes thematically — `[{title, noteIds}]`.
3. Optionally declare connections between notes — `[{fromNoteId, toNoteId, label?}]`.
4. Call `buildWhiteboardLayout` once. The server returns a summary of what was created.

Example call shape:

```json
{
  "groups": [
    {"title": "Foundations", "noteIds": ["systems-thinking-intro", "feedback-loops"]},
    {"title": "Case studies", "noteIds": ["case-toyota", "case-netflix", "case-spotify"]},
    {"title": "Practice", "noteIds": ["weekly-review-template", "decision-journal"]}
  ],
  "connections": [
    {"fromNoteId": "systems-thinking-intro", "toNoteId": "case-toyota", "label": "applies to"}
  ]
}
```

The server arranges groups left-to-right, places cards in 1 or 2 columns per group depending on count, sizes each card based on note content length, and draws connections with optimal handle positions.

## Workflow: tweak an existing board

For incremental edits, use the per-item tools:

1. `listWhiteboards` — find the right `boardId` (default is `'main'`).
2. `listWhiteboardItems(boardId)` — see what's already there. Note each item's `id`, `x`, `y`, `width`, `height`.
3. Then any of:
   - `addNoteToWhiteboard` — append one card. Use the returned `width×height` to pick the next card's Y.
   - `addStickyNote` — add a sticky.
   - `createWhiteboardGroup` — wrap existing cards in a group (create the group **after** the cards so you know their bounding box).
   - `createWhiteboardConnection` — connect two items by their `itemId`s.
   - `moveWhiteboardItems` — batch reposition / resize.
   - `updateWhiteboardItem` — edit text / color / size of a single item.
   - `removeWhiteboardItems` — delete items (auto-drops their connections).

## Tool reference

All tools take an optional `boardId`; omit to target the default board (`'main'`).

### Read

- **`listWhiteboards()`** — returns boards with `id`, `name`, `itemCount`.
- **`listWhiteboardItems({boardId?})`** — returns items with `id`, `noteId`, `itemKind`, `title`, `x`, `y`, `width`, `height`.

### Boards

- **`createWhiteboard({name})`** — new board.
- **`deleteWhiteboard({boardId})`** — soft-delete (recoverable). Cannot delete `'main'`.

### Items

- **`addNoteToWhiteboard({boardId?, noteId, x, y, width?, height?})`**
  - `noteId` is the note's filename without `.md`.
  - **Do not pass `height`** — let the server estimate from content. The response includes the actual `width×height`; use it to compute the next card's Y.
  - Default `width` is 200. Standard card.
- **`addStickyNote({boardId?, content, x, y, color?})`**
  - `content` is plain text — keep it short (a few words to one sentence).
  - `color`: `yellow` (default), `blue`, `green`, `pink`, `purple`, `orange`.
  - Sticky is `200×150`.
- **`createWhiteboardGroup({boardId?, title, x, y, width?, height?})`**
  - **`title` MUST be a meaningful theme name** (e.g. `"系統思考基礎"`). Do not pass generic strings like `"Group Name"` — the server's description literally calls this out.
  - Create groups **after** placing the cards so you know the bounding box.
  - Positioning rule: `x = leftmost-card-x - 30`, `y = topmost-card-y - 60` (room for title).
  - Sizing rule: `width = card-area-width + 60`, `height = card-area-height + 90`.

### Connections

- **`createWhiteboardConnection({boardId?, fromItemId, toItemId, label?})`** — by **item ID**, not note ID. Handles are picked automatically.

### Edits

- **`updateWhiteboardItem({boardId?, itemId, content?, color?, width?, height?})`** — change at least one field.
- **`moveWhiteboardItems({boardId?, moves: [{itemId, x, y, width?, height?}]})`** — batch.
- **`removeWhiteboardItems({boardId?, itemIds})`** — also removes connections touching the removed items.

### Batch

- **`buildWhiteboardLayout({boardId?, groups, connections?, cardWidth?, columns?})`** — see workflow above. **Preferred** for any layout of >2 cards.

## Key constraints and gotchas

- **`noteId` ≠ note title.** It's the filename without `.md`. If you only have a title, find the file first (see `hyday-vault-layout`).
- **Cards must not overlap.** When placing cards manually, the rule is: `nextY = previousY + previousHeight + 40`. With `buildWhiteboardLayout` this is handled for you.
- **Don't pass `height` to `addNoteToWhiteboard`.** The auto-estimate is content-aware; an explicit height usually makes the card too tall or too short.
- **Groups go behind cards** (`zIndex = 0`). Create cards first, then groups, otherwise the group title visually sits under cards.
- **Connections are by `itemId`, not `noteId`.** Item IDs are returned when a card is created (or appear in `listWhiteboardItems`). Inside `buildWhiteboardLayout`, you specify connections by `noteId` because the server maps note → item for you.

## Example: building a "Q3 reading review" board

1. Ensure these notes exist (use `hyday-markdown` skill to create them if needed):
   - `reading-notes-atomic-habits.md`
   - `reading-notes-deep-work.md`
   - `reading-notes-thinking-fast-slow.md`
2. Call:

```json
{
  "tool": "buildWhiteboardLayout",
  "input": {
    "groups": [
      {
        "title": "Best of Q3",
        "noteIds": ["reading-notes-atomic-habits", "reading-notes-deep-work"]
      },
      {
        "title": "Skim again later",
        "noteIds": ["reading-notes-thinking-fast-slow"]
      }
    ],
    "connections": [
      {
        "fromNoteId": "reading-notes-atomic-habits",
        "toNoteId": "reading-notes-deep-work",
        "label": "shared theme: deliberate practice"
      }
    ]
  }
}
```

3. Optional follow-up: add a header sticky at the top.

```json
{
  "tool": "addStickyNote",
  "input": {
    "content": "Q3 Reading Review",
    "x": 0,
    "y": -100,
    "color": "yellow"
  }
}
```

4. Show the user — Hyday's whiteboard view will reflect changes immediately when they switch to it.

## Validation checklist

After any whiteboard operation, verify:

1. Every `noteId` you used corresponds to a real `.md` file (otherwise the card shows the noteId as title and no preview).
2. Group titles are meaningful, not `"Group Name"` or `"Untitled"`.
3. If you placed cards manually, no two cards overlap (use the returned `height` from each `addNoteToWhiteboard` to space them).
4. Connections reference real `itemId`s (per-item flow) or real `noteId`s (`buildWhiteboardLayout` flow).
5. You used `buildWhiteboardLayout` when creating >2 cards at once.

## Notes on sync and portability

- The whiteboard sidecar is a regular file (`.hyday/whiteboards-v2.json`). If the user's vault folder is inside iCloud, Dropbox, or another file-sync tool, the whiteboard syncs across machines along with the vault.
- The server keeps 3 rotating backups (`.backup.1`, `.backup.2`, `.backup.3`) next to the sidecar.
- Soft-deleted boards move to `trashedBoards` inside the same sidecar — they're not gone.

## References

- Server installation and config: `mcp-servers/hyday-whiteboard/README.md`
- Creating the notes that become cards: see `hyday-markdown` skill
- Where notes live: see `hyday-vault-layout` skill
