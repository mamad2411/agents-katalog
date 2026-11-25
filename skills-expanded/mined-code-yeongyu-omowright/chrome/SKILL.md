---
name: chrome
description: Read this when you need Chrome MV3-shaped APIs — bookmarks, tabs, windows, history, downloads, or top sites — in standalone OmOWright.
---

# Chrome MV3 APIs (standalone)

`createChromeApi(connection, options?)` returns MV3-shaped namespaces backed by
CDP and the browser's own profile files — no extension required.

```js
import { createChromeApi } from "omowright";

const chrome = createChromeApi(connection, {
  profilePath: "/path/to/user-data-dir", // enables bookmarks/history/topSites/downloads.search
  downloadDir: "/path/to/downloads", // optional, defaults to a temp dir
});
```

**PROFILE-BACKED METHODS THROW `UnsupportedOperationError` WITHOUT `profilePath`.**
A `connectPipe` browser gets a fresh profile, so bookmarks and history are empty
there — these APIs matter when attaching to a real user browser via `connect()` or
reading a real profile directory. Profile reads are read-only and WAL-safe against a running
browser.

## tabs — CDP `Target.getTargets`

- `chrome.tabs.query({ url?: string | string[], title?, windowId? })` — `url`
  takes MV3 match patterns (`*://*.example.com/*`), `title` is a substring match. **THESE THREE
  ARE THE ONLY HONORED FILTERS.**
- `chrome.tabs.get(tabId)` — `tabId` is a string; throws when no tab has it.
- Returns `{ id, url, title, windowId, active, pinned, audible, discarded, groupId, index }`.
  **IDS ARE CDP TARGET-ID STRINGS, NOT MV3 NUMBERS**, and the last six fields are
  fixed defaults — they are not observable over CDP.

Tab lifecycle stays on `connection.newTab(url)` / `page.close()`; interaction on
`page.goto()` / `page.locator()`.

## windows — CDP `Browser.getWindowForTarget`

`get(windowId, queryOptions?)`, `getCurrent(queryOptions?)`, `getAll(queryOptions?)`.

- `queryOptions: { populate?: boolean }` — `populate: true` adds a `tabs` array.
- Returns `{ id, type, state, alwaysOnTop, incognito, tabs? }`. **THERE IS NO
  `focused` FIELD**: CDP exposes no window focus state, and `document.hasFocus()`
  is true in every page OmOWright attaches to (it enables focus emulation),
  background agent windows included.
- `getLastFocused()` throws `UnsupportedOperationError` for the same reason. With
  the extension bridge, follow `chrome.windows.onFocusChanged` instead.
- `getCurrent` returns the first window; it does not tell you where the user is
  working.

## bookmarks — profile `Bookmarks` JSON, read-only

`get(idOrIdList)`, `getChildren(id)`, `getRecent(numberOfItems)`,
`getSubTree(id)`, `getTree()`, `search(query)` where `query` is a string or
`{ query?, url?, title? }`.

Nodes: `{ id, title, type: "url" | "folder", url?, dateAdded?, children? }`.

## history — profile `History` SQLite, read-only

- `search({ text, startTime?, endTime?, maxResults? })` — times are Unix ms.
  Returns `[{ id, url, title, visitCount, lastVisitTime }]`, newest first.
- `getVisits({ url })` — returns `[{ id, url, visitTime, transition }]`.

## downloads — `History` SQLite + `Browser.setDownloadBehavior`

- `search({ url?, filename?, limit? })` — returns
  `[{ id, url, filename, startTime, bytesReceived, totalBytes, state }]`; state is
  `complete | canceled | interrupted | in_progress`. Needs `profilePath`.
- `download({ url, filename? })` — downloads through the real browser and resolves
  `{ id, url, filename, state: "complete" }` with `filename` as the absolute saved
  path. 30s timeout; rejects when the URL starts no download. It uses an in-page
  anchor click rather than `Page.navigate`, which hangs on download navigations,
  and re-asserts the download behavior on every call because tab initialization
  resets it.

## topSites — profile `Top Sites` SQLite

`get()` returns `[{ url, title }]` ordered by rank, max 50.

## Write methods require the extension bridge

These throw `UnsupportedOperationError` because they would mutate the user's own
browser state: `bookmarks.create/update/move/remove/removeTree`,
`history.addUrl/deleteUrl/deleteRange`,
`downloads.pause/resume/cancel/erase`, and all of `chrome.tabGroups`.
