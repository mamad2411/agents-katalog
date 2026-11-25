---
name: playwright
description: Drive a real web browser at the DOM level — navigate, click, type, fill forms, extract text, screenshot, handle tabs/dialogs/downloads — through the "playwright" MCP server. Use whenever the user asks to do something on a website or web app, scrape/extract web content, fill or submit a web form, log in to a site, or automate anything in a browser. Prefer this over coordinate-based machine-control for ANY web task.
---

# Browser automation (Playwright)

You can drive a real browser through the **playwright** MCP server. Its tools are
exposed as `mcp__playwright__browser_*`. Unlike machine-control (which clicks screen
pixels), this works at the **DOM / accessibility level** — you target elements by a
stable `ref` from a page snapshot, not by coordinates. So the core loop is
**snapshot → act → (re)snapshot**:

1. **Snapshot**: `browser_snapshot` returns the page's accessibility tree — every
   interactive element with a human label and a `ref` id. This is your map. (No need
   to take a picture and read pixels; the snapshot already tells you what's there.)
2. **Act**: `browser_click` / `browser_type` / … using the element's `ref` (and pass
   its label as `element` for clarity).
3. **Verify**: snapshot again (or `browser_wait_for`) to confirm the page changed.

Use `browser_take_screenshot` only when the user wants an image or you need to see
visual/canvas content the snapshot can't express — not as the primary way to act.

## When to use this vs machine-control
- **Web pages / web apps → playwright.** Faster, cheaper, far more reliable (no broken
  coordinates, auto-waits for elements, reads real page text/HTML).
- **Native Windows apps, OS dialogs, installers, the desktop, `<canvas>`/WebGL, video,
  cross-app drag/drop → machine-control.** Playwright only sees the browser.

## Tools

**Navigation**
- `browser_navigate {url}` — go to a URL.
- `browser_navigate_back` / `browser_navigate_forward`.
- `browser_close` — close the browser (page). `browser_resize {width,height}`.

**Read the page**
- `browser_snapshot` — accessibility tree with element `ref`s. **Your primary "look".**
- `browser_take_screenshot {filename?, fullPage?, element?, ref?}` — PNG; Read it if you
  need to see it. Use for visuals, not for locating clickable elements.
- `browser_console_messages` — page console output.
- `browser_network_requests` — requests the page made.
- `browser_evaluate {function, element?, ref?}` — run JS in the page (e.g. extract
  data, read `document.title`, scrape a table). Powerful escape hatch.

**Interact** (get `ref` from a snapshot first; pass the visible label as `element`)
- `browser_click {element, ref, button?, doubleClick?}`
- `browser_type {element, ref, text, submit?}` — type into a field; `submit:true` presses Enter.
- `browser_fill_form {fields:[{name|ref, value}]}` — fill several inputs at once.
- `browser_press_key {key}` — `Enter`, `Tab`, `Escape`, `ArrowDown`, etc.
- `browser_hover {element, ref}`
- `browser_select_option {element, ref, values:[…]}` — pick from a `<select>`.
- `browser_drag {startElement,startRef,endElement,endRef}`
- `browser_file_upload {paths:[…]}` — set files on a file input.

**Tabs**
- `browser_tabs {action:"list"|"new"|"select"|"close", index?}` — multi-tab control.

**Waiting / dialogs**
- `browser_wait_for {text?, textGone?, time?}` — wait for content to appear/disappear,
  or a fixed time. Prefer text waits over fixed sleeps.
- `browser_handle_dialog {accept, promptText?}` — accept/dismiss alert/confirm/prompt.

*(Exact tool set comes from `@playwright/mcp`; if a name differs, list the
`mcp__playwright__*` tools and pick the closest.)*

## Recipes

**Open a site and click something**
1. `browser_navigate {url:"https://example.com"}`.
2. `browser_snapshot` → find the target element's `ref` + label.
3. `browser_click {element:"Sign in button", ref:"…"}`.
4. `browser_snapshot` (or `browser_wait_for {text:"Welcome"}`) to confirm.

**Fill and submit a form**
1. `browser_navigate` → `browser_snapshot` to see the fields.
2. `browser_fill_form {fields:[{name:"Email",value:"a@b.com"},{name:"Password",value:"…"}]}`
   (or `browser_type` per field).
3. `browser_click` the submit button, then `browser_wait_for` the result.

**Extract page data**
- `browser_snapshot` for structured text, or
- `browser_evaluate {function:"() => [...document.querySelectorAll('h2')].map(e=>e.textContent)"}`
  for precise scraping. Return the data to the user.

**Screenshot a page for the user**
- `browser_navigate` → `browser_take_screenshot {fullPage:true}` → Read the PNG and/or
  hand the path back.

## Rules of thumb
- Always `browser_snapshot` before interacting, to get fresh `ref`s — they change as the
  page changes. A stale `ref` → re-snapshot.
- Prefer `browser_wait_for {text:…}` over guessing with fixed delays.
- For login/secret values, use the value the user provided; don't invent credentials.
- First run downloads the browser if missing — give it a moment.
- This controls a browser only. For anything outside the browser, use **machine-control**.