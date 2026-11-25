---
name: today-page
description: "Put single things on the Today page so they stay on screen and refresh by themselves: a city's weather, a stock, this computer's CPU and RAM, scheduled tasks. Use for put it on my Today page, always show, keep an eye on. To design the whole page with a form, use today-designer."
version: 0.3.0
platforms: [linux, macos, windows]
---
# Today page

Use this when someone wants something to **stay on screen and keep updating**: "always show Seattle weather", "keep an
eye on my Mac", "put NVDA and my scheduled tasks on the Today page".

**The Today page** is a dashboard of this plugin's blocks, in the sidebar, set with the `dashboard` tool. Its
sections name a source and a view: `system` (kpis), `weather.<City>` (weather or kpis), `stock.<SYMBOL>` (kpis or
chart), `tasks` (table or list), and the assistant's and calendar's sources when the personal assistant is set up.
It refreshes without you.

Two other asks belong elsewhere:

- To design the whole page with the user (name, weather, mail tabs, work sections), follow the `today-designer`
  recipe.
- A one-off question ("how is NVDA doing?") is answered with blocks in the reply.

## Steps

1. **`show` first**, and keep every section the user didn't ask to remove.
2. **One `set` call.** It replaces the whole spec, so pass every section that should stay, plus the new one.
3. **Pass on the reply in one sentence.** Don't repeat numbers; they refresh by themselves.

## Examples

"Keep an eye on my Mac": first

```text
{"tool": "dashboard", "args": {"action": "show"}}
```

then the spec with a system section added to what was there:

```text
{"tool": "dashboard", "args": {"action": "set", "spec": {"title": "Today", "sections": [{"from": "system", "title": "My Mac"}]}}}
```

"Always show Seattle weather":

```text
{"tool": "dashboard", "args": {"action": "set", "spec": {"title": "Today", "sections": [{"from": "weather.Seattle"}]}}}
```

"Put NVDA's month and my scheduled tasks on the Today page":

```text
{"tool": "dashboard", "args": {"action": "set", "spec": {"title": "Today", "sections": [{"from": "stock.NVDA", "as": "chart"}, {"from": "tasks", "as": "table"}]}}}
```

## Rules

- Never draw blocks in the reply for this, and never write HTML, a `::preview` widget or a code block for it: the
  Today page draws itself.
- **There is no ticker or status-bar strip.** If the user asks for one ("put NVDA in my ticker"), say so in one
  sentence and offer to put it on the Today page instead.
- Only these sources exist. A scheduled task's output text, a web page or URL, or news can't be shown yet: say so
  plainly.
- Stats come from the machine running Hermes, which may not be the one the user is looking at.
- "Remove my Today page": `dashboard` `clear`.
