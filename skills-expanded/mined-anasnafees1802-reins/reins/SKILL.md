---
name: reins
description: Drive the user's real, already-running Chrome or Edge (their logged-in sessions, cookies, open tabs) through the Reins extension. Use for any task in a web app or website the user is logged into, form filling, data entry, testing a web UI, scraping a page they can see, or any "do this in my browser" request. Prefer this over Playwright or a fresh browser whenever existing sessions matter.
---

# Reins: control the user's real browser

Use the tools from the `reins` MCP server (named like `mcp__reins__snapshot`, `reins_snapshot` or `reins/snapshot` depending on the agent). Always prefer them: screenshots come back as images and there is no shell overhead.
Only if no reins MCP tools are listed in this session, fall back to the shell: `reins <tool> key=value ...` (screenshots save to `~/.reins/screenshot.jpg`), and tell the user the MCP server is not loaded.

You act inside the user's own browser with their accounts. Treat it like their hands on their keyboard.

## Loop

1. `tabs` (list) to see what is open. The user often already has the right page open. Use it with `tab:<id>`; do not open a new tab for a page that is already there.
2. `snapshot` to read the page. Every interactive element gets a ref like `e12` (iframes: `f1e5`).
3. Act with `click` / `type` / `select` / `press` / `upload` using refs.
4. Read the action's reply. It is a **diff** of what changed (`+` new, `-` removed, `~` changed in place), or a full snapshot if the page navigated. Usually you do NOT need another snapshot.
5. Repeat. Refs stay stable for the same element until the page navigates.

Actions wait for their own effects: the requests they start (searches, saves, loads) and the DOM updates after them. So the reply to "type in a search box" or "click Save" already shows the results. Do not add a `wait` unless the reply lacks something that takes longer than ~5s.

## Keep it cheap

Cost is driven by the NUMBER OF TURNS (each turn re-reads the context), not by Reins's output (about 80 tokens per call).

- **Batch.** When you already know the next refs, send them as one `batch` call: fill a whole form, click Save, then `wait` for the success text, all in one turn. Example: `batch steps:[{tool:"type",ref:"e3",text:"Ada"},{tool:"type",ref:"e4",text:"Lovelace"},{tool:"click",ref:"e9"},{tool:"wait",text:"Saved"}]`. A custom dropdown is one batch too: `[{tool:"click",ref:"e52"},{tool:"snapshot",query:"option India"}]`.
- Use `query` to pull just the lines you need (`query:"option Indian"`, `query:"Name|Email|button Save"`, where `|` means any of them).
- Snapshot before screenshot. A snapshot costs about a tenth of a screenshot. Screenshot only for visual questions (layout, charts, images, canvas, captcha-like widgets) or when a snapshot looks empty.
- Narrow big pages: `query:"invoice"`, `viewport:true`, or `mode:"interactive"`. For reading articles: `mode:"text"`.
- Snapshots leave out link URLs to save tokens; click the link's ref instead. Need the URLs (to collect links, or open one in a new tab)? `snapshot hrefs:true query:"..."`.
- Batch typing: `type ref text submit:true` instead of type, then press Enter.
- `snapshot:false` on actions whose result you do not need to see.

## Site APIs, console, background watches

- **Use the site's own API.** `network action:"start" reload:true`, then `network` lists the XHR/fetch calls. `network action:"get" id:7` shows one (credential headers are masked; you never see them). `network action:"replay" id:7 url:"...page=2"` (or `body`, `method`, `headers`) calls it again as the user. For bulk reads or repeated edits, one replay beats dozens of clicks. Same confirmation rules apply: a replayed POST is a real action.
- **Debugging a web app:** `console action:"start"`, reload, then `console` returns new messages and exceptions. Action replies also flag unread console errors.
- **Wait for something slow** (a deploy, a reply, a price): `watch action:"add" text:"Deploy finished"` (or `gone:true`, or `query:"status"` to report any change in matching lines; `reload:true` for pages that do not update live; `every` seconds, default 60). Then `watch action:"wait" timeout:0` blocks until it fires, costing no turns while it waits. `watch` (list) and `watch action:"remove" id:"w1"` manage them. Watches run in the daemon, so they keep going while you do other work.
- `run` (a shell command on each event) is CLI only. If the user wants one, give them the `reins watch action=add ... run="..."` command to run themselves; the command reads the event from the file in `REINS_EVENT_FILE`.

## When something fails

- `Cannot click: covered by <...>`: a modal, cookie banner or overlay is on top. Close it (look for its button in the snapshot) or `press key:"Escape"`. Use `force:true` only when the cover is harmless.
- After a re-render, Reins finds the same control again by role and name when it can (the reply says "was stale; used e12"). If it still says `Ref ... is stale`, take a new `snapshot`.
- `iframe fN is not responding`: that frame's page is frozen. Work with the rest of the page; retry later if you need it.
- Element missing from the snapshot: scroll (`scroll direction:"down"`), use `query`, or take a `screenshot` and `click x y` on the image coordinates.
- Custom dropdowns (not native `<select>`): click to open, then click the option ref from the diff.
- Autocomplete fields that ignore pasted text: `type ... slowly:true`.
- Results load later than the action reply (slow jobs, >5s): `wait text:"Saved"` (or `gone:true`, or `url:"/dashboard"`).
- Need data the DOM hides: `eval code:"return [...document.querySelectorAll('tr')].length"`.
- `Screenshot timed out`: the tab is in the background and the browser is not rendering it. Use snapshot instead, or `tabs action:"switch"` (this brings the tab to the front, so ask first if the user is working in that window).
- Error says the user paused control: stop and ask them. Never try to work around a pause.

## Rules

- Confirm with the user before irreversible or outward actions you were not explicitly asked to do: payments, purchases, sending messages or emails, deleting data, publishing, changing account or security settings.
- Login page with empty fields: click the username field first. The browser fills saved credentials only after a real click, and the diff shows them (passwords masked). Then click Sign in.
- Never type passwords or secrets unless the user gave them for that purpose. No saved credentials, or a 2FA/OTP code is needed: ask the user.
- JS dialogs (alert/confirm) are auto-accepted and reported in the reply.
- Links that open a new tab switch the agent's target to it automatically; the reply says so.
- Several browsers connected: pass `browser:"edge"` or `browser:"chrome"`.
- Other agents may share this browser. Each agent session gets its own target tab automatically. Never act in a tab that `tabs` marks "other agent". If you are told the tab is in use, open your own with `navigate {url, newTab:true}`. CLI users running several agents: give each its own `REINS_AGENT=<name>` env var.
