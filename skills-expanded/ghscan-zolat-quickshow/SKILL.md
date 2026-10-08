---
name: fun
description: Casual games and panel-loop demos that run in a floating QuickShow HUD panel — chess (drag pieces), tic-tac-toe (click cells), pictionary (draw, Claude guesses), and a minimal one-button click-bridge demo. Each game has its own instructions file in this skill directory; read the one the user picked before doing anything. Use when the user asks to play a game, wants a quick interactive demo of the QuickShow `panel_event` channel, or asks to see the markup feedback loop in a game-shaped form.
---

A bundle of small, casual games + panel-loop demos that run inside a
QuickShow HUD panel. Each game's full instructions live in a sibling
`.md` file — this `SKILL.md` only routes.

## Pick the game and read its instructions first

Before rendering anything, **Read** the appropriate file. Don't try
to wing it from this file — each game has its own state model,
event-loop details, and HTML starter.

| User wants… | Loop channel | Read this file |
|---|---|---|
| **Chess** — play a casual game, drag pieces on a board | `panel_event` (drag) | `${CLAUDE_PLUGIN_ROOT}/skills/fun/chess.md` |
| **Tic-tac-toe** — quick 3×3, click cells | `panel_event` (click) | `${CLAUDE_PLUGIN_ROOT}/skills/fun/tic-tac-toe.md` |
| **Pictionary** — user draws, Claude guesses | `markup` (Send button) | `${CLAUDE_PLUGIN_ROOT}/skills/fun/pictionary.md` |
| **Click-bridge demo** — minimal one-button proof of `panel_event` | `panel_event` (click) | `${CLAUDE_PLUGIN_ROOT}/skills/fun/click-demo.md` |

If the user is ambiguous ("let's play a game"), ask once which one;
don't pick for them.

## Shared notes (apply to all four)

These show up in every child file too, but worth knowing up front:

- **Pick a `group` slug per game and save it to memory.** Each
  game's body of work shares one group (e.g. `chess-<6hex>`,
  `ttt-<6hex>`). Pass it on every `show_html` / `enable_*` /
  `get_*` call so the panel survives `claude --resume`. See
  `quickshow/SKILL.md` "memory-save pattern".
- **Arm the right channel.** `enable_panel_events(group=…)` for
  chess / tic-tac-toe / click-demo. `enable_markup_events(group=…)`
  for pictionary. Both arm calls return a `Monitor` command — start
  it `persistent: true` so each event fires a notification.
- **Same `name:` + `group:` for every re-render.** Each game uses
  one panel name (e.g. `chess-board`, `ttt-board`,
  `pictionary-canvas`, `click-demo`) inside one group;
  re-rendering with the same `(name, group)` updates the panel in
  place. A different name (or group) opens a new tab/HUD and
  breaks the loop.
- **Draw mode steals pointer events.** If the user toggles markup
  draw mode (✏︎ in the title bar), the in-DOM canvas captures
  clicks and drags. Cell clicks / piece drags stop working until
  they exit draw mode. Don't try to work around it — it's the
  same trade-off the markup loop already makes.
- **Keep responses short.** "Your move." / "Nf3." / "Got it!" The
  panel is the conversation surface; don't lecture.

Now go read the file for the game the user picked.
