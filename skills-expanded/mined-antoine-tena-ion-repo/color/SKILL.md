---
name: color
description: Change the color of the bar beside the person's messages in the chat, or of the gray one of a task or another session - a palette, more on request, any color named. Use when the user wants another color for their messages or the gray ones, or from `/repo:look`.
argument-hint: "[a color, by name or #rrggbb]"
---

Talk to the user in their language; nothing outside `~/.claude/` is touched.

The bar takes its color from the theme: `professionalBlue` (the bar, `chat.tsx`) and
`briefLabelYou` (Claude Code's own label on the person's messages), both set to the color chosen.
A theme is a JSON file in `~/.claude/themes/<slug>.json` (`name`, `base`, `overrides`), chosen by
`"theme": "custom:<slug>"` in `~/.claude/settings.json`.

1. Read `theme` in `~/.claude/settings.json` (absent: `dark`). A `custom:<slug>` theme is edited in
   place, its `base` kept; a preset (`dark`, `light`, their `-daltonized` and `-ansi` forms) becomes
   the `base` of a new theme `mine` (`"name": "Mine"`). Light bases take the light column below.
2. With `$ARGUMENTS`, that color is the choice: go to 3. Otherwise show the whole palette as a
   short list (name and hex), then ask with the AskUserQuestion tool: three colors that stand
   apart from the current one, and "Other colors". Any name or `#rrggbb` the user types in "Other"
   is taken; "Other colors" asks again with three colors not offered yet, then with colors of the
   user's own description ("a deep green"), as long as they want.

   | Color | Dark base | Light base |
   |---|---|---|
   | Blue | `#4c8dff` | `#1d4ed8` |
   | Cyan | `#22d3ee` | `#0e7490` |
   | Teal | `#2dd4bf` | `#0f766e` |
   | Green | `#4ade80` | `#15803d` |
   | Lime | `#a3e635` | `#4d7c0f` |
   | Yellow | `#facc15` | `#a16207` |
   | Coral | `#fb7185` | `#be123c` |
   | Pink | `#f472b6` | `#be185d` |
   | Violet | `#a78bfa` | `#6d28d9` |
   | Lavender | `#c4b5fd` | `#7c3aed` |
   | Silver | `#d1d5db` | `#4b5563` |

   Claude's orange (`claude`) is never offered: the two bars must stay apart.

   The gray bar of what came from elsewhere (a task, another session), only when the user asks
   for it: same palette and questions, `Gray (Recommended)` first for the default, and none of
   the person's color nor Claude's orange. The theme has no key of its own for it (`inactive`
   would gray all of Claude Code), so it goes to `~/.claude/chat-colors.json` as `{"others":
   "#rrggbb"}`, other keys kept; gray chosen: the key removed, the file too once empty. The mod
   reads it within ten seconds; skip 3.
3. Write the theme with both overrides (other keys of an existing theme kept), then set `theme` to
   `custom:<slug>` in `~/.claude/settings.json`, every other key unchanged (`python3 -I` with
   `json`, indent 2). When `chezmoi source-path <file>` answers for one of the two files, update its
   source too (`chezmoi add ~/.claude/themes/<slug>.json`, `chezmoi re-add
   ~/.claude/settings.json`) and say chezmoi's repo has it to commit.
4. Claude Code reloads `~/.claude/themes/` live: the bar changes at once, and the status line
   too when its palette is `chat` (`/repo:statusline`). If the folder did not
   exist when the session started, say a restart of Claude Code is needed once. Ask whether it
   suits; if not, back to 2.
