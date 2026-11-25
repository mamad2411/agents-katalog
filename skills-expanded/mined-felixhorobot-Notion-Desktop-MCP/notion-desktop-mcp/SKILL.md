---
name: notion-desktop-mcp
description: Drive the user's Notion Desktop app (running in debug mode, remote debugging port 9222) fast and safely through the notion-desktop-mcp MCP tools (notion_*), read pages, edit and restyle content, build tables/databases/diagrams, delete and restore blocks or pages, organise the sidebar, in any workspace they are logged into (incl. guest workspaces the official Notion API connector cannot reach). Use whenever the task touches Notion through notion_* tools, or the user asks to read, edit, design, organise or visualise a Notion page in the desktop app.
---

# notion-desktop-mcp

You are driving the user's real, logged-in Notion desktop app. Every edit is live and, in shared
workspaces, visible to the whole team. Work like a careful power user: **read once, plan, act in
batches, verify, never destroy what you didn't create.**

Reference files (read the one you need, not all):
- `reference/features.md`, what Notion can do: blocks, slash commands, shortcuts, markdown, styling, links, media.
- `reference/organisation.md`, workspaces, teamspaces, sidebar, favourites, permissions, databases, trash/history.
- `reference/coverage.md`, what is verified live vs untested vs blocked. Check before promising a feature.
- `scripts/helpers.js`, the `page.n` helper library used by the server and inside `notion_run_code` (§0b).
- `scripts/outline.js`, `scripts/markdown.js`, `scripts/access.js`, page outline, blocks → Markdown, permission check.
- `launcher/notion.ps1` (repo/plugin root): start Notion in debug / normal mode (desktop shortcuts call it).

## 0. Tools (MCP server `notion-desktop-mcp`)

| Tool | Use |
|---|---|
| `notion_launch {mode}` | start/restart Notion in debug mode (ask first: it restarts Notion) |
| `notion_status` | first call: connection, workspace, tabs, access |
| `notion_open {url}` | open a page |
| `notion_outline` / `notion_read` | blocks with ids / page or blocks as Markdown |
| `notion_insert {markdown, after? , position?}` | add blocks (rolls back if an existing block vanishes) |
| `notion_create_database {title, table}` | a whole database from a Markdown table in ONE step |
| `notion_delete_blocks {block_ids, confirm?, allow_shared?}` | delete; backs up Markdown first |
| `notion_list_deletions`, `notion_restore_blocks {deletion_id?}` | undo a delete, blocks go back to their old spot |
| `notion_trash_page {title, confirm?}`, `notion_restore_page {url \| title}` | page to / from Notion Trash |
| `notion_switch_workspace {name}`, `notion_screenshot` | workspace switch; visual check |
| `notion_run_code {code}` | escape hatch: `async (page) => {...}` with `page.n` helpers (databases, views, tables…) |

**Speed:** write a whole section per `notion_insert` (one paste, any number of blocks) and bulk data via
`notion_create_database`; per-cell `n.db.*` edits take ~1 s each: use them for types and fixes only.

Every tool takes an optional `page` (URL or id); default is the active Notion tab. Tools bring the
target tab to the front: block selection only works in the active tab.

**Delete / restore rules (enforced by the server):**
- `notion_delete_blocks` and `notion_trash_page` only preview until you pass `confirm: true`.
  Show the user the preview and get a yes first.
- Guest / shared workspace (or workspace unknown) → refused unless `allow_shared: true`. Only pass it
  after the user explicitly said yes for this change.
- Never delete with `notion_run_code`, it bypasses the backup.
- Block backups are Markdown in `~/.notion-desktop-mcp/deletions.jsonl`. Restored blocks get new ids; colours,
  toggle open/closed state and code languages other than mermaid don't survive. Child pages and
  databases go to Notion Trash instead: restore them with `notion_restore_page`.

## 0a. Preconditions (check once per session)

1. Notion must be running with the debug port, or every tool fails with "not running in debug mode".
   With the user's OK (it restarts Notion) call `notion_launch`; or they use the "Notion (Claude debug)"
   shortcut. `notion_launch {mode:"normal"}` closes the port again when they're done.
   **Keep the window open:** a window closed to the tray stops rendering and ignores input, relaunch
   with the launcher. If clicks time out on "visible, enabled and stable", the window is occluded or
   minimised: `page.mouse.click(x, y)` still works.
2. The server connects through an in-process CDP relay that hides Notion's renderer targets that never
   answer CDP (url-less pages, untitled file:// pages), without it Playwright's connect hangs. It also
   drops Playwright's `prefers-color-scheme` override so Notion keeps the user's theme.
3. Long pages unmount off-screen blocks: `n.outline()` sees only rendered ones; `n.fullOutline()` scrolls
   and returns every block (guards and restores use it). Never act in the "Tab Bar" target. `n.tabs.list()` / `n.tabs.activate(title)` manage tabs.
4. Know which workspace you are in (`notion_status`). A guest workspace is shared with a team; a
   private workspace is the user's own. Say which one before editing.

## 0b. Helpers inside `notion_run_code` (`page.n`)

Every Page has `page.n` (there is no `import`/`require` in run_code).
Do a whole task in ONE call. Verified end to end, 2026-10-31:

| Helper | Does |
|---|---|
| `n.outline()` / `n.access()` | read page blocks / permission + refusal signals |
| `n.esc(k)`, `n.away()` | close popups; park the mouse mid-page (narrow window → sidebar hover flyout covers menus) |
| `n.menuText()`, `n.clickMenu(label)` | read / click inside whatever menu or dialog is open (both Notion menu variants) |
| `n.block(text)`, `n.caretAtEnd(textOrId)` | find a block; put caret at its end |
| `n.paste(md)` | paste Markdown via synthetic paste event (no clipboard, works unfocused) |
| `n.insertAfter(anchor, md)` | add blocks after a block; **throws + Ctrl+Z if any existing block vanished** |
| `n.guard(fn)` | run anything with that same before/after block check → `{added, removed}` |
| `n.slash(cmd, option)` | `/cmd` → pick option |
| `n.newPage(title)` → Page | new page (Private) in a new tab, titled, caret in body |
| `n.trashPage(expectTitle)` | Actions → Move to Trash, only if the title matches |
| `n.actions(item)` | open ••• Actions (dispatch) and click item |
| `n.workspace(name)` | switch workspace/account |
| `n.tabs.list/open/closeActive/page` | tabs; Ctrl+T / Ctrl+W equivalents |
| `n.table.read/scrollX/setCell(r,c,v)` | simple tables: read all cells (no scroll), replace a cell's whole text |
| `n.db.addRow/addProperty/setOption/setToday/setText/addView/switchView/filter/sort` | database editing |
| `n.db.columns/read/cellByName/scrollX` | wide databases: `read()` scrolls to collect virtualised cells |
| `n.db.ready/views/allViews/current` | wait for view header; visible tabs; all views incl. "N more…"; selected view |
| `n.db.setCheckbox/setPerson/setPlace/setFileLink/setRelation` | values for non-text property types |
| `n.db.addRelation(target)`, `setFormula(col, expr)`, `setRollup(col, relCol, prop)` | computed properties |
| `n.db.headerMenu(col, item)`, `calculate(col, fn)` | column menu (Freeze, Hide, Wrap/Unwrap, Edit property…); footer Sum/Average/… |
| `n.db.settings(item)`, `groupBy(prop)`, `subItems()`, `colorRule(prop)` | view settings panel |
| `n.db.chart({x, y, agg, type})` | chart view config; type 0 vbar · 1 hbar · 2 line · 3 donut · 4 number |

**After every Notion update** (or when helpers misbehave): run `scripts/selftest.js` with
`notion_run_code` in your own (non-shared) workspace. It builds and trashes "Claude selftest (safe to delete)" and returns
PASS/FAIL per step (22 steps, ~65 s; 22/22 on Notion 7.41.1, 2026-10-31). On any FAIL it keeps the page and
returns `keptForInspection`, inspect, fix helpers.js, then trash it with `n.trashPage('Claude selftest (safe to delete)')`.
Updating Notion: the in-app File → "Restart to Apply Update" does NOT update this Microsoft Store build;
`winget upgrade --id Notion.Notion` does (ask the user first; it restarts Notion without the debug port: 
re-run the launcher afterwards). Note `winget upgrade <name>` INSTALLS; to only check use `winget list --name Notion`.

Example:
```js
async (page) => {
  const p = await page.n.newPage('Sprint plan');
  await p.n.paste('## Goals\n- Ship MVP\n\nTasks');
  await p.n.caretAtEnd('Tasks'); await p.keyboard.press('Enter');
  await p.n.slash('table', 'Table view'); await p.n.clickMenu('New empty data source');
  await p.n.db.addRow('Set up repo'); await p.n.db.addProperty('Status');
  await p.n.db.setOption('Set up repo', 1, 'In progress'); await p.n.db.addView('Board');
  return p.n.outline();
}
```
If a helper throws, read its message: it names what was showing instead (e.g. Notion's update prompt
: never accept/dismiss that yourself, ask the user).

## 1. Speed rules: fewest round-trips

| Instead of | Do |
|---|---|
| Snapshot → click → snapshot → type … | One `notion_run_code` script doing the whole sequence with Playwright locators |
| Typing a page block by block | Write the whole section as Markdown and **paste** it once (§3) |
| Full accessibility snapshot to read | `notion_outline` → `[depth, type, blockId, text]` |
| Hunting for a block by pixel | Locator `[data-block-id="<id>"]` from the outline |
| Clicking menus | Keyboard: slash commands, `Ctrl+/` block menu, `Ctrl+Shift+<0-9>` turn-into, `Ctrl+Shift+↑/↓` move (see features.md) |
| Screenshots to check styling | Only when visual layout genuinely matters; outline otherwise |

Plan the full edit list from one outline read, then execute it in one or two scripts.

Playwright patterns inside `notion_run_code` (`page` is provided):
```js
const blk = page.locator('[data-block-id="ID"] [contenteditable="true"]').first();
await blk.click();                       // caret into block
await page.keyboard.press('End');        // caret to end of block
await page.keyboard.press('Enter');      // new empty block below
await page.keyboard.type('/callout');    // slash menu filters
await page.keyboard.press('Enter');
```
Wait for UI with `await page.waitForTimeout(150)` only after opening menus; Notion is fast.

## 2. Reading a page

1. `notion_outline` → title, breadcrumb, block tree (`notion_read` for the content as Markdown).
2. Block `type` values are Notion's internal names: `text`, `header` (H1), `sub_header` (H2),
   `sub_sub_header` (H3), `bulleted_list`, `numbered_list`, `to_do`, `toggle`, `quote`, `callout`,
   `divider`, `code`, `image`, `page` (sub-page), `alias` (link to page), `collection_view`
   (inline database), `collection_view_page` (linked/full-page database), `column_list`/`column`,
   `table`/`table_row` (simple table), `transclusion_container` (synced block),
   `table_of_contents`, `breadcrumb`, `equation`, `bookmark`, `embed`. Unknown → inspect, don't guess.
3. For full text of a block: `page.locator('[data-block-id="ID"]').innerText()`.
4. Navigate to a sub-page: click its block or `page.goto(href)` with the `/p/...` link from the outline.

## 3. Writing content fast: paste

Notion converts pasted Markdown/HTML into real blocks (headings, lists, to-dos, quotes, code,
tables, links, dividers). Build the section text, then paste at the caret:

```js
// inside notion_run_code
await page.locator('[data-block-id="ANCHOR"] [contenteditable="true"]').first().click();
await page.keyboard.press('End'); await page.keyboard.press('Enter');
await page.evaluate(md => navigator.clipboard.writeText(md), MARKDOWN);
await page.keyboard.press('ControlOrMeta+V');
```
If clipboard write is refused, dispatch a synthetic paste instead:
```js
await page.evaluate(md => {
  const dt = new DataTransfer(); dt.setData('text/plain', md);
  document.activeElement.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
}, MARKDOWN);
```
Then re-run the outline and confirm the new blocks exist with the right types.

**Verified live (2026-10-30, clipboard + Ctrl+V, ~2 s for 16 blocks):** `##`/`###` headings, bold /
italic / inline code / `[links](url)`, nested `-` bullets, `1.` numbered, `- [ ]` / `- [x]` to-dos
(ticked state kept), `>` → **quote** (when pasted; typed `> ` makes a toggle), fenced code with
language, Markdown pipe tables → real table, `---` divider, ```` ```mermaid ```` → rendered diagram.
`navigator.clipboard.writeText` works without extra permissions.

The clipboard is the user's: read it first (`navigator.clipboard.readText()`) and write it back
after pasting.

Things paste can't do: use slash commands / menus afterwards: callout icon & colour, block
background colours, columns, synced blocks, toggle headings, database views, page icon/cover.

## 3b. Verified gotchas (live tests, 2026-10-30)

- Start every `notion_run_code` script with `page.setDefaultTimeout(4000)`, the 30 s
  default turns one wrong locator into a 30 s stall.
- A menu left open (`.notion-overlay-container` has text) blocks clicks on the page underneath.
  Press `Escape` twice before clicking into the page, or act inside the menu.
- New pages open in a **NEW TAB** (in Private), with focus not yet in it: typing right away goes
  nowhere. Ctrl+N over CDP worked once and then not at all; use the Tab Bar `[aria-label="New"]`
  compose menu → `1` instead (§7). Then use the returned Page, click
  `[placeholder="New page"]` (the title) and type. Enter moves to the first body block.
  Under a page in a shared workspace prefer `/page` inside the parent instead.
- Never type until you've clicked a specific element: keystrokes go wherever focus happens to be.
- Image block menu: tabs are `role="tab"` named Upload / Link / Unsplash / GIPHY inside
  `.notion-overlay-container`. By URL: tab `Link` → type URL → Enter. Upload: wait for
  `filechooser` while clicking button `Upload file`, then `chooser.setFiles(path)` inside `notion_run_code`.
  Both verified.
- Verified keys: `Ctrl+Shift+1` turn-into H1 (no Windows clash), `/callout` + Enter,
  `Ctrl+/` → `blue background` + Enter, `@today` + Enter (date mention).
- Find a block by its text: `page.locator('.notion-page-content [data-block-id]', { hasText: 'X' }).last()`
  (`.last()` = innermost, since wrappers share text).
- Outline wrappers: a callout shows as `callout` with a nested `text` child of the same text, normal.
- **Top bar buttons (Share, Favorite, ••• Actions) are covered by the window's drag `HEADER`**, real
  clicks time out. Use `locator.dispatchEvent('click')`, e.g.
  `page.locator('.notion-topbar-more-button').dispatchEvent('click')` opens the page Actions menu:
  Copy link · Copy page contents · Duplicate · Move to · Version history · Updates & analytics ·
  Appearance & layout · Use with AI · Suggest edits · Notify me · Available offline · Lock page ·
  Move to Trash · More. Favourite = `.notion-topbar-favorite-button`. The menu renders EITHER inside
  `.notion-overlay-container` with `role="menuitem"` items OR as a `[role="dialog"]` with
  `role="presentation"` items (seen both on 2026-10-30). Robust:
  `page.locator('[role="dialog"], .notion-overlay-container').filter({hasText:'Move to Trash'}).last().getByText('Move to Trash',{exact:true})`.
- Trashing a page (Actions → Move to Trash) makes the tab navigate to another page. Before trashing,
  assert both the title and the page id in the URL; afterwards confirm it's gone from the sidebar.

## 4. Safety protocol: never delete other people's work

Hard rules:
- **Before any edit in a shared workspace, state the exact change (page, location, what) and get
  the user's go-ahead.** Edits by your hand appear under the user's name.
- Only delete or overwrite blocks **you created this session** or that the user named explicitly.
  Never chain `Ctrl+A` with typing/Backspace/Delete: one press selects the block, more presses
  widen the selection toward the whole page.
- Markdown gotcha: `> ` at line start makes a **toggle**, not a quote (quote is `" `).
- Never delete pages, databases, or database views; never move pages between parents, unfavourite,
  rename or change sharing unless the user asked for exactly that.
- Insert new content **below an anchor** with End → Enter; don't click into existing text and type.
- Selected blocks (blue highlight) + any key = replaced/deleted. Press `Esc` twice to clear
  selection before typing anything.
- Deleting a source database deletes it everywhere; deleting a *linked view* only removes the view.
  Deleting a synced block's original (>10 copies) removes all copies and Undo can't fix it.
  Check `type` in the outline before removing anything.
- **Never drag pages in the sidebar**, it re-parents them and changes who can access them.
- Don't click "Save for everyone" on filters/sorts, Lock/Unlock page, or delete properties unasked.
- If the breadcrumb shows "Locked", stop and ask: don't unlock on your own.
- Prefer non-destructive options on shared pages: add new blocks, or use comments / Suggest edits.
- Guest limits: no Notion AI, no automations, no top-level pages, export only
  with Full access. Don't plan around those.

Verification loop after every batch:
1. Re-run the outline. Compare block count and the neighbours of the edit with the pre-edit read.
2. Anything unexpected missing → `Ctrl+Z` immediately (repeat as needed), then re-check.
3. Still wrong → stop and tell the user. Recovery ladder: Ctrl+Z → Trash (30 days) → ••• → Version
   history (needs Can edit; Free plan keeps 7 days). See organisation.md.

Before a large restructure, note the time: version history restores by timestamp.

## 5. Quick recipes (details in reference/)

| Task | Fastest route |
|---|---|
| Switch page | `Ctrl+P` → type title → Enter; or `page.goto` with a `/p/...` URL from the outline |
| Tabs (Ctrl+T / Ctrl+W) | `n.tabs.open/closeActive/activate` (they act on the separate "Tab Bar" page). Real Ctrl+T/W are Electron window accelerators, so CDP keys are ignored. **Ctrl+T** = `window.tabsApi.newTab()` → "Open in new tab…" search opens in the active page → type title → Enter. **Ctrl+W** = REAL click on the active tab's `[aria-label^="Close Tab, "]` (index from `listTabs`, which reads `{id,title,active}` from React props). Refuse to close the last tab. Never `page.close()` |
| Switch workspace / account | sidebar bottom-left `.notion-sidebar-switcher` → menuitem with the workspace name (see §6) |
| Move page | Ctrl+Shift+P (shown in Actions menu) or Actions → Move to: only when asked; guests usually can't |
| Favourite a page | star icon in the top bar (personal only: safe) |
| Link page → page | type `@` + page name → Enter (inline, creates backlink) or `/link` block |
| New sub-page in place | `/page` or `+name` → "Add new sub-page" |
| Link to a specific block | Ctrl+/ on that block → Copy link to block → select text → Ctrl+K → paste |
| Emoji / symbol | `:name` inline; page icon: hover title → Add icon; callout icon: click it |
| Insert image | `/image` → tab `Link` + URL + Enter, or button `Upload file` + file chooser (both verified) |
| Web link | select text → Ctrl+K → URL; bare URL paste → "Paste as mention" / bookmark |
| Heading levels | `#`/`##`/`###` + space, or `Ctrl+Shift+1/2/3`; editor has no H4 |
| Text style | Ctrl+B/I/U, Ctrl+Shift+S strike, Ctrl+E code, Ctrl+Shift+H last colour |
| Block colour | Ctrl+/ → type e.g. `blue background` → Enter |
| Page font / width | ••• top right → Default/Serif/Mono, Small text, Full width |
| Columns | drag block by ⋮⋮ beside another until vertical blue guide (`page.dragTo`) |
| Diagram | `/mermaid` → paste Mermaid source → set view to Preview |
| Table | `/table` (simple) or `/table view` (database); data-heavy → database |
| Collapse sections | turn heading into toggle heading: Ctrl+/ → Turn into → Toggle heading N |

## 6. Workspaces, accounts, settings, permissions (verified 2026-10-30)

**Switch workspace / account**, the switcher is the sidebar's bottom-left `.notion-sidebar-switcher`
(real click). Its menu lists every logged-in account and its workspaces as `role="menuitem"`;
the workspace icon letter is glued to the name ("MMy Workspace"), so match with
`overlay.getByRole('menuitem').filter({ hasText: 'My Workspace' })`, not an anchored regex.
Picking a workspace under another account switches the account too (no re-login). ~3.5 s to settle.
`tabsApi.toggleWorkspaceSwitcher()` does nothing visible: don't use it.
Always tell the user which workspace you're switching to, and switch back when done.

**Settings**, switcher menu → `Settings` (menuitem). Sections (left nav, click by name):
Account: Preferences · Notifications · Mail & Calendar, Workspace: General · People · Sidebar · Import, 
Features: Notion AI · Meeting notes · Connections · Notion MCP · Public pages · Emoji · Offline · Developer, 
Admin: Teamspaces, Access & billing: Billing · Explore plans.
Preferences holds Theme, High contrast, Enter-for-newline, Language, Number format, Spellchecker,
Start week on Monday, Date format, Time zone, Open on start.
Rules: read freely; change a setting only after the user approves that exact change. Never touch
security/login (password, passkeys, 2FA, sessions, log out), account email, billing/plan, People
(members, roles), Public pages, Connections/Notion MCP clients, or deleting a workspace: tell the user to do those.
Workspace sections need workspace-admin rights; as a guest they are absent.

**Permissions & why Notion refuses**, run `scripts/access.js` (`n.access()`) before editing and
after any action that seemed to do nothing. Signals:
| Signal | Meaning |
|---|---|
| `canEditBody: false` | You have Can view / Can comment here |
| `locked: true` ("Locked" in top bar) | Page lock: ask the user; don't unlock |
| hint `Request membership` | You are a guest in this workspace |
| `disabledMenuItems` (aria-disabled) | Action blocked by your access level, e.g. as a guest: Copy page contents, Move to, Move to Trash |
| hint `Upgrade` / `limit` or an upgrade dialog | Plan limit (charts, history days, file size, guests) |
| `alerts` (`role=alert/status`, toasts) | Notion's own error text: quote it to the user |
| menu item missing entirely | Feature not available to you (guest → no Notion AI, no automations, no top-level pages) |
Open the relevant menu first (e.g. Actions) so disabled items are in the DOM, then run access.js.

## 7. Databases (all verified live 2026-10-30, Notion 7.40)

`db = page.locator('.notion-collection_view-block').first()`, `ov = page.locator('.notion-overlay-container')`.
| Step | How |
|---|---|
| Create page to work in | Tab Bar `[aria-label="New"]` (real click) → compose menu in the active page → press `1` (New page; `4` = New database) → opens in a new tab → click `[placeholder="New page"]` and type title. (Ctrl+N over CDP is unreliable.) |
| Insert inline DB | `/table` → option **"Table view · Database"** (plain "Table" = simple table) → popup → **"New empty data source"** (also: Import CSV, templates, Link to existing data source) |
| Rename DB | `db.locator('[placeholder="New database"]').click({force:true})`, assert `document.activeElement` placeholder, then type. The visible "New" next to it is not editable. After "Turn into database" the force-click does nothing, use `page.mouse.click` on the placeholder's box instead |
| Simple table → DB | click a `td`, Escape (selects block), Ctrl+/ → `getByRole('option')` "Turn into database" (role=option, not menuitem). Keeps headers + data as Text columns; then header → Change type → Number/Select |
| Delete a simple table | NOT td-click + Escape + Delete (that only clears the cell). Use td-click → Escape → Ctrl+/ → `getByRole('option')` "Delete"; verify with outline. Several top-level blocks in a row: click first → Escape → Shift+ArrowDown ×(n-1) → assert `.notion-selectable-halo` count === n → Delete (verified; Ctrl+/ on a heading has no Delete option) |
| Rename view | click the active view tab → menu "Rename" → focused input placeholder "View name" → type, Enter |
| View filter/sort in a shared DB | changes show a "Reset · Save for everyone" bar = local only until saved. Saving needs the user's OK. Save = `page.mouse.click` on the centre of the "Save for everyone" text (locator.click hit the wrong element); confirm the toast "Changes saved for everyone" and that "Reset" is gone (the chip bar may be collapsed: click Filter to show it) A new view copies the current view's hidden properties, re-show via Settings → Property visibility → hover row → `[aria-label="Toggle property visibility"]` click({force:true}) |
| Two-way relation | header → Edit property → click "Two-way relation" → toggle `input[role="switch"]` (the "Enable" text is not a button) |
| Mermaid diagram | paste a ```mermaid fence. Notion **strips `click` hrefs** (anchors keep target=_blank, href=null) → boxes are not clickable; add a list of Markdown links beside it. Subgraph `direction TB` is ignored when an edge leaves the subgraph: keep end nodes inside; `R ~~~ P` puts two subgraphs side by side. Display mode: hover block → `[aria-label^="Open language preview format"]` (mouse.click) → `[aria-label="Show only preview and hide code"]`. Edit code: click into it, select activeElement via Range, synthetic paste |
| Add row | `db.getByRole('button',{name:'New page',exact:true}).last()` → type name → Esc Esc |
| Cell | row = `db.locator('[data-block-id]').filter({hasText: rowName}).last()`; cell = `row.locator('.notion-table-view-cell').nth(colIndex)` → click |
| Status value | `ov.getByRole('option').filter({hasText:/^In progress$/})` (plain getByText hits group labels) |
| Date value | calendar popup → `ov.getByText('Today',{exact:true})` or type a date |
| Select value | click cell → type option name → Enter (creates the option if new) |
| Add property | first one: button "Add property"; afterwards the header's **unlabeled** button: `db.locator('.notion-table-view-header-row [role="button"]').filter({hasText:/^$/}).first()` → menu "Select type" → `ov.getByText('Status',{exact:true})`. `.notion-table-view-add-column` is **property visibility**, not add |
| Add view | hover `.notion-collection-view-tab` → `.notion-collection-add-view` appears → menu **"Add a new view"** → `ov.getByRole('gridcell',{name:'Board'})`. Types: Table, Board, Gallery, List, Chart, Dashboard, Timeline, Feed, Map, Calendar, Form |
| Views overflow | extra views hide behind "N more…" (`db.getByText(/^\d+ more/)`): list there; it also has option "New view" |
| Filter | `db.locator('[aria-label="Filter"]')` → popup is **outside** `.notion-overlay-container`: `page.getByPlaceholder('Filter by…').fill('Status')` + Enter → values are `role="menuitem"`; for Status, group names repeat option names → click the **last** match |
| Sort | `db.locator('[aria-label="Sort"]')` → `ov.getByText('Name',{exact:true})` |
| Chart | add Chart view → "Edit chart" panel opens for axes/grouping |

Wide tables (verified with 10–15 columns on 7.40/7.41): header cells are always all in the DOM, but
**database ROW cells are virtualised horizontally**, off-screen cells may simply not exist (a 10-column
row rendered only 7 cells after a filter re-render). Never read cells by position or expect
`cells.length === columns.length`. `n.db.read()` scrolls `.notion-scroller.horizontal` in steps, merges
cells by `data-col-index` per row id, and restores the scroll. Clicking a cell auto-scrolls it into view.
Simple tables (`n.table.read()`) rendered all cells in tests. In simple-table cells Ctrl+A does NOT select
the cell and Shift+Home only selects the last wrapped line: `n.table.setCell` selects via the DOM.

Options map (all exercised live on 7.41.1, 2026-10-31: see coverage.md):
- Column header menu: Edit property · Property access · Change type · Filter · Sort · Calculate · Freeze ·
  Hide · Wrap/Unwrap content · Insert left/right · Duplicate · Delete property.
- Calculate: None/Count/Percent at top level; Sum/Average/Median/Min/Max/Range under **More options**.
  Footer shows e.g. "SUM 52" (uppercase via CSS); with Group by, each group gets its own footer.
- View settings: Layout · Property visibility · Filter · Sort · Group · Conditional color · Copy link · Source ·
  Edit properties · Automations · AI Autofill · Turn into · More settings (Sub-items, Dependencies,
  Connections, Customize page layout) · Manage data sources · Lock database.
- Chart settings: Chart type (5) · X axis What to show / Omit zero · Y axis What to show (Count or a property,
  then Sum/Average/Min/Max/Median/Distinct) · Group by · Range · Reference line · Color · Save chart as… (export).
- Number/Rollup cells can "Show as" Number / Bar / Ring (in-cell visualisation).
- Relation setup: search "Link to a data source…", pick target, "Add relation"; two-way by default on self.
- Form view asks "Create N questions" from existing properties; the view is named "Form builder".
- Side panels (Conditional color, chart settings) ignore Escape: `n.esc()` also clicks their ✕ (`aria-label="Close"`).
- Person menu items aren't role=option: pick by text ("Your Name (You)"). Place's first suggestion is
  "Current Location": pick the matching suggestion, never Enter. Checkbox state = cell's input.checked.

Locating the database: Notion renders a floating 24px copy of the DB header OUTSIDE `.notion-page-content`
and many nested inner blocks with the same class. Always use the outermost block inside the page content
(what `n.db.at()` does). View tabs vanish for a moment after adding/switching views: `n.db.ready()` waits.
Visible tabs are only part of the list when there are many views: use `n.db.allViews()`.

Traps found live:
- The "+ Add view" button can render OUTSIDE `.notion-collection_view-block`, `n.db.addView` picks
  the one nearest the DB; with one view it's `[aria-label="Add view"]`; with overflow use "N more…" → New view.
- The previous view's settings panel can linger and cover the +: addView retries after Esc.
- Compose menu (Tab Bar "New") has two variants: centred "New page · Press 1" or dropdown
  "Page · Chat · AI Meeting Notes · Database", and it opens in the ACTIVE tab. Notion reuses a hidden
  `/blank` tab for the new page: detect it by URL change, not by a new Page object.
- After adding a view, a "New view" settings panel opens whose layout picker uses the **same gridcells**.
  Clicking "Timeline" there converts the current view instead of adding one. Only click a gridcell when
  the menu text contains **"Add a new view"**.
- A view that "disappears" is usually in "N more…": check before assuming it was changed.
- On shared databases filter/sort changes are personal until "Save for everyone": never click that unasked.

## 8. Design defaults (when asked to "make it look better")

- Structure: H1 only as page title; H2 for sections; H3 for subsections; ≤ 3 levels.
- Lead with a short summary callout (💡, gray background), then a table of contents for long pages.
- Group related content in toggles or toggle headings; side-by-side info in 2 columns.
- Status/progress → a database with Board or Timeline view, not bullet lists.
- Flows, architecture, timelines → a Mermaid code block (`/code`, language Mermaid, view "Preview").
- Link related pages with `@mention` inline or a "Link to page" block, never by pasting raw URLs.
- Colours: one accent colour per page; colour backgrounds for callouts/status only.
- Propose the layout as an outline first; apply only after the user agrees.
