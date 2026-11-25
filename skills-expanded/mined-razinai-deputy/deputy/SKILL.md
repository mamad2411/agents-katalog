---
name: deputy
description: Use the user's own browser through Deputy's browser_* tools - open pages, read them, fill and submit forms, click, extract lists and tables, and with Deputy Pro take screenshots, check layouts at other sizes, read the console and network. Use when the user asks to do something on a website or web app, in their logged-in browser, on localhost, or to check how a page looks. Also use when a Deputy tool says the extension is not connected, or when a needed browser tool is missing.
---

# Working in the user's browser with Deputy

Deputy drives the browser the user already has open, signed in as them. It turns the page into typed tools, so work in this order:

1. **Open the page:** `browser_navigate` with the URL. Its result lists the page's forms as typed tools with JSON Schemas, plus clickable actions with refs.
2. **Fill a whole form in one call:** `browser_invoke` with the form tool's name and all its fields. These page tools are not MCP tools; do not search for them.
3. **Anything else:** `browser_act` with a ref (Pro), or `browser_click` / `browser_fill` (free). Each result says what changed, so there is rarely a need to look again.
4. **Reading:** `browser_ask` for one fact (with Pro, a hosted model answers in a sentence), `browser_read` for text to reason over, `browser_extract` for lists and tables (Pro).
5. **Seeing:** `browser_screenshot` only when pixels matter: layout, styling, charts, images.

Forms that change something (payments, posts, bookings, account settings) are filled, then the user approves on the page or in the client before Deputy submits. Never press the submit button yourself unless the user's own instruction was to submit.

## Checking a frontend design (Pro)

1. `browser_navigate` to the dev server (for example `http://localhost:3000`).
2. `browser_screenshot`, with `fullPage: true` for the whole page. Compare it with what the user asked for.
3. `browser_resize` to phone (390 wide) and tablet (820 wide) sizes, and screenshot again.
4. `browser_inspect` on anything that looks wrong, for real computed styles and boxes; `browser_console` for errors.
5. Fix the code, `browser_navigate` with `action: "reload"`, and check again.

## When something is missing

**The extension is not connected** (a tool says "Deputy can't reach the browser"): tell the user to

1. open Chrome (or another Chromium browser) with the Deputy extension installed and turned on: https://chromewebstore.google.com/detail/deputy/ofcadhlipiciahelmcjofblnjhmjoepm
2. wait a few seconds for it to connect, then try again. If it still fails, run `/mcp` to reconnect Deputy.

**A tool the task needs is not available** (screenshots, tabs, scrolling, waiting, resizing, console, network, uploads, downloads, inspect, extract, act, hosted models): it is part of Deputy Pro. Say plainly which tool is missing and why the task needs it, then tell the user:

- Deputy Pro is $9.99 a month or $95.99 a year: https://deputy.razin.ai/buy
- the license key appears on the page right after paying; paste it on Deputy's setup page (Deputy icon in the toolbar, then **Setup & Pro**)
- the tools appear within seconds; if not, run `/mcp`
- cancel any time at https://deputy.razin.ai/manage; the key works to the end of the period paid for

Then carry on with the free tools if the task can still be done another way, and say what you could not check.

**A tool says the user switched it off** (screenshots, console and network, uploads, downloads): the user turned it off on Deputy's setup page under "What your agent may do". Ask them to switch it back on there if they want it; do not try to work around it.
