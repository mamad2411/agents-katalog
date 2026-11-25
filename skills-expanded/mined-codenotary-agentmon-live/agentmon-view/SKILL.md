---
name: agentmon-view
description: Make, change, switch or delete a custom AgentMon Live web view when the user asks, such as "make a cost view", "hide the log in the web view", "orange accent in the web view", "switch the web view back to default". Use for any request to change how the AgentMon web page looks or what it shows.
---

# AgentMon Live web views

A view is a JSON file in `~/.claude/agentmon-live/views/<name>.json`. The name is `a-z`, `0-9` and `-`, at most 40 characters. The file is at most 64 KB. The web page reads the folder every few seconds; no restart is needed.

- **Switch:** write the view's name to `~/.claude/agentmon-live/views/active` (no newline needed). Write an empty file to go back to the default page. Open pages follow at once.
- **List:** list the folder. **Copy:** copy a file under a new name. **Delete:** remove the file, and empty `active` if it named it.
- Change a view by editing its file. Read it first, and keep what the user did not ask to change.

## Format

```json
{
  "title": "Cost focus",
  "theme": { "dark": { "--signal": "#f97316" }, "light": { "--signal": "#c2410c" } },
  "sections": [
    { "id": "cost", "label": "Cost", "blocks": [
      { "type": "Row", "children": [
        { "type": "Stat", "label": "Spend", "value": "/usage/usd", "format": "usd" },
        { "type": "Stat", "label": "Running", "value": "/active", "format": "count" } ] },
      { "panel": "Calls" } ] },
    { "id": "calls", "hidden": true },
    { "id": "log", "hidden": true }
  ]
}
```

### Sections

- Built-in ids: `overview`, `calls`, `verification`, `agents`, `files`, `log`. Listed without `blocks`, a built-in section shows as usual; `label` renames it; `hidden: true` hides it.
- Sections show in the order listed. Built-in sections that are not listed come after them.
- Any other id (`a-z0-9-`) is a custom section. It needs `label` and `blocks`.
- Giving a built-in section `blocks` replaces what it shows.
- Each panel once per view. When a section embeds a panel that a built-in section shows, hide that built-in section (`{ "id": "calls", "hidden": true }`): a panel drawn twice repeats its element ids, and links and the `/` search key go to the wrong copy. Built-in panels: `overview` has Instruments, Flow, Waterfall, TurnClock, Events, Running and Steps; `calls` has Calls and Insights; `verification` has Checks and Tasks; `agents` has Agents; `files` has Files; `log` has Log.

### Blocks

- `{ "panel": "<name>" }`: one of the page's panels: `Instruments`, `Flow`, `Waterfall`, `TurnClock`, `Events`, `Running`, `Steps`, `Calls`, `Insights`, `Checks`, `Tasks`, `Agents`, `Files`, `Log`.
- `{ "type": "Row", "children": [...] }` side by side; `Column` stacked; `Card` with an optional `title` draws a box around its children.
- `{ "type": "Text", "text": "..." }`.
- `{ "type": "Stat", "label": "...", "value": "<pointer>", "format": "usd" | "count" | "dur" | "pct" | "time" }`. `count` of a list is its length; `dur` takes milliseconds; `time` takes a timestamp and adds the date when it is not today's. Over a list, add `"agg"` (`sum`, `avg`, `min`, `max`, `count`), `"field"` (the number in each row) and optionally `"where"`. `"foot"` is a line below the number. `"warnAt"` and `"badAt"` colour the number from those values on.
- `{ "type": "Table", "label": "...", "rows": "<pointer>", "columns": [{ "label": "...", "field": "<pointer inside each row>", "format": "..." }] }`, at most 8 columns. Prefer it over `List`.
- `{ "type": "Bars", "label": "...", "rows": "<pointer>", "name": "<pointer>", "value": "<pointer>", "format": "..." }`: each row's share of the total, largest first. For a record, leave `name` and `value` out. With `group`, the bar is the group and `name` is not read.
- `{ "type": "Gauge", "label": "...", "value": "<pointer>" }` for a percent; with `"max"` for any number against its top. `Meter` takes the same fields and draws a track. Both take `warnAt` and `badAt`.
- `{ "type": "Sparkline", "label": "...", "points": "<pointer to a list>", "field": "<pointer to a number in each item>", "format": "..." }`.
- `{ "type": "List", "label": "...", "items": "<pointer to a list>", "field": "<pointer inside each item>", "max": 10 }`: one value per row.

### Rows (`Table`, `Bars`)

- `rows` points at a list, or at a record, whose entries read as `/key` and `/value` (`/insights/edits`, `/insights/session`).
- `"where": [{ "field": "/isFailed", "is": true }]`: up to 4 tests, all must hold. `is`, `not` compare a text, number or boolean; `above`, `below` a number.
- `"group": "/model"`: one row per value, with `/key` (the value) and `/count`. A column then needs `"agg"` over its `field`, such as `{ "label": "Cost", "field": "/usd", "agg": "sum", "format": "usd" }`.
- `"sort"`: a column's label or a field pointer. `"desc": true` turns it. `"max"`: rows shown, 10 by default, at most 50.

```json
{ "type": "Table", "label": "Time by tool", "rows": "/trace", "group": "/tool", "sort": "Total", "desc": true, "columns": [
  { "label": "Tool", "field": "/key" },
  { "label": "Calls", "field": "/count" },
  { "label": "Total", "field": "/ms", "agg": "sum", "format": "dur" } ] }
```

Nesting stops at 6 levels and 24 children per block. Anything else is left out.

### Pointers

JSON pointers into the session's snapshot (`WebSnapshot` in the plugin's `types/index.d.ts`). Useful ones:

| Pointer | What |
| --- | --- |
| `/usage/usd` | session cost so far |
| `/usage/ctxPct`, `/usage/ctxTokens` | context use |
| `/usage/rate` | quota list (`kind`, `pct`) |
| `/turnCount` | prompts answered |
| `/turns` | recent turns; `wallMs` per turn for a Sparkline |
| `/active` | tool calls running now (`tool`, `what`, `who`) |
| `/calls` | recent tool calls (`what`, `result`, `who`) |
| `/trace` | every tool call with its time (`tool`, `what`, `who`, `at`, `ms` once done, `isFailed`) |
| `/agents` | subagents (`type`, `task`, `status`, `model`, `usd`, `input`, `output`, `cached`, `tools`, `files`, `errors`, `startedAt`, `endedAt`) |
| `/insights/tokens` | `mainIn`, `mainOut`, `mainCached`, `agentsIn`, `agentsOut` |
| `/insights/breakdown` | the context window by part (`name`, `tokens`) |
| `/insights/session`, `/insights/sessionWall` | where the session's time went (a record of milliseconds), and its whole time |
| `/insights/slow`, `/insights/big` | slowest calls (`tool`, `what`, `who`, `ms`, `at`), largest results |
| `/insights/edits`, `/insights/reads` | records of file path to count |
| `/checks`, `/tasks` | verification runs (`kind`, `result`, `at`), tasks |
| `/learned/bench` | up to 10 past sessions of the project (`at`, `turns`, `calls`, `errors`, `compactions`, `usd`, `totalUsd`, `outTokens`) |
| `/main/model` | the model |
| `/session/cwd`, `/session/branch` | where the session runs |

### Theme

`theme.light` and `theme.dark` map colour tokens to colours. Tokens: `--page`, `--surface`, `--surface-1`, `--surface-2`, `--surface-3`, `--header`, `--line`, `--line-soft`, `--line-input`, `--ink`, `--heading`, `--ink-2`, `--ink-3`, `--signal` (the accent), `--signal-bright`, `--signal-soft`, `--good`, `--warn`, `--bad`, `--good-soft`, `--warn-soft`, `--bad-soft`, `--info`, `--info-line`, `--ramp-1` to `--ramp-5`, `--ramp-other`. Values: `#hex`, `rgb()`, `hsl()` or `oklch()` only. Keep text readable: give both themes, with enough contrast against `--page` and `--surface`.

## Shipped views

`cost`, `speed` and `quality` come with the mod (`server/views/` in the plugin) and are in the menu without a file. Read one as a worked example. To change one, copy it to `~/.claude/agentmon-live/views/` under the same name and edit the copy: it takes the shipped one's place.

## Check before you report

Run `node <plugin root>/server/view-check.mjs <file>` on every view you write or change. It prints `ok`, or one line for each thing the page would leave out (`block`, `panel`, `pointer`, `colour`, `section`, `limit`) and for each pointer that finds nothing in a sample session (`empty`). Fix the file until it says `ok`; an `empty` line for data this session may not have yet (no subagents, no past sessions) can stay, and you say so. The page shows the same lines in its **View notes** box.

After writing, tell the user the view's name and that the page has switched to it. A file the page cannot read shows in its view menu with the error.
