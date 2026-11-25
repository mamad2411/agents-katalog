---
name: navigation
description: "Navigate multi-step flows on authenticated pages: follow menu paths, click through breadcrumbs, handle SPA routing, wait for page loads, and backtrack safely. Also covers direct URL navigation with the navigate_to_url tool."
---

# Guided Multi-Step Navigation

Navigate through web pages by clicking links and actions rather than constructing
URLs. This approach survives URL changes, handles SPAs, and works on authenticated
pages where direct URL access may fail.

## When to Use Click Navigation

- "Go to Settings → Privacy → Manage Data"
- "Navigate to the admin dashboard"
- "Click through to the order history page"
- Any task that requires clicking through menus, tabs, or breadcrumbs instead
  of visiting a URL directly.

## Workflow

### 1. Check Connection

Call `list_browsers` to confirm a browser is connected. If no browsers are
available, ask the user to connect the Brijio extension.

### 2. Read the Current Page

Call `read_current_page` with `includeContent: true`. Examine the response for
navigable `links` and `actions`.

### 3. Find the Right Link

Look through the `links` array for a link whose `text` or `url` matches your
target. Example targets:

| User Request               | Look For                              |
| -------------------------- | ------------------------------------- |
| "Go to Settings"           | `text: "Settings"` or `text: "⚙"`     |
| "Open my orders"           | `text: "My Orders"`, `text: "Orders"` |
| "Click the dashboard link" | `text: "Dashboard"`                   |

If you find a matching link, call `click_element` with `kind: "link"` and the
link's `id`.

### 4. Wait and Re-Read

After clicking, the page will navigate. **You must re-read the page** to get
fresh element IDs:

```
1. click_element(kind: "link", id: "e12")  → navigates
2. read_current_page(includeContent: true)  → fresh page context
3. Continue with next navigation step
```

All element IDs from the previous page are now **invalid**. Never reuse IDs
after navigation.

### 5. Repeat Until Destination Reached

Continue the click → read → evaluate cycle until you reach the target page.
Verify you're on the right page by checking:

- The page `url` matches the expected pattern
- The page `title` contains expected keywords
- Expected content (a heading, form, or data table) is visible in the page

### 6. Breadcrumb Backtracking

If you need to go back to a previous level:

1. Look for breadcrumb links in the page content
2. Use `click_element` on the breadcrumb link
3. Re-read the page to get fresh IDs

Do **not** assume URLs are stable — always navigate by clicking, not by
constructing URLs.

---

# Direct URL Navigation

Use the `navigate_to_url` tool to navigate the browser directly to an HTTP or
HTTPS URL without clicking through the page.

## When to Use Direct URL Navigation

- You know the exact URL and need to go there directly
- The user provides a specific URL (e.g., "Go to https://example.com/dashboard")
- You need to jump to a known page quickly and re-read it
- Click-based navigation would take too many steps for a known URL

**Do not use `navigate_to_url` for:**

- Auth-gated pages where the URL alone won't work (use click navigation instead)
- URLs with schemes other than `http:` or `https:` (ftp, data, javascript — these
  return `unsupported_scheme`)
- Pages that require POST data or specific headers

## Workflow

### 1. Check Connection

Call `list_browsers` to confirm a browser is connected. If multiple browsers
are available and you need a specific one, note the `browserInstanceId`.

### 2. Navigate

Call `navigate_to_url` with:

| Parameter           | Required | Description                                                        |
| ------------------- | -------- | ------------------------------------------------------------------ |
| `url`               | Yes      | The HTTP or HTTPS URL to navigate to                               |
| `browserInstanceId` | No       | Target a specific browser when multiple are connected              |
| `tabId`             | No       | Target a specific tab (from `list_tabs`) instead of the active tab |

Example:

```
navigate_to_url(url: "https://example.com/dashboard")
```

To navigate a specific background tab without switching focus:

```
navigate_to_url(url: "https://example.com/dashboard", tabId: "97212078")
```

### 3. Check the Result

The response includes:

| Field          | Type    | Description                                               |
| -------------- | ------- | --------------------------------------------------------- |
| `url`          | string  | The final URL after navigation (may differ if redirected) |
| `title`        | string  | The page title after navigation                           |
| `redirected`   | boolean | `true` if the final URL differs from the requested URL    |
| `navigationMs` | number  | Time taken for the navigation in milliseconds             |
| `timestamp`    | string  | ISO 8601 timestamp of when navigation completed           |

### 4. Handle Errors

| Error Code            | Cause                                                   |
| --------------------- | ------------------------------------------------------- |
| `unsupported_scheme`  | URL is not http: or https:                              |
| `no_active_tab`       | No active browser tab found                             |
| `navigation_failed`   | Browser reported an error (restricted URL, crashed tab) |
| `timeout`             | Navigation took longer than 10 seconds                  |
| `browser_unavailable` | No browser extension connected                          |
| `connection_failed`   | Could not reach the Brijio WebSocket server             |
| `invalid_response`    | Extension returned an unrecognisable response           |

### 5. Re-Read After Navigation

After `navigate_to_url` succeeds, always call `read_current_page` to get fresh
element IDs. The navigation result only tells you the URL and title — you still
need page context to interact with elements.

## Choosing Between Click Navigation and Direct URL

- **Prefer `navigate_to_url`** when you have a precise URL and the page isn't
  behind a login wall or requires cookie-based auth that click-through preserves.
- **Prefer click navigation** when you need to follow menu paths, breadcrumbs,
  or when direct URL access would fail (e.g., SPA hash routes, auth-gated pages).
- **Prefer `open_tab`** when you need to open a URL in a new tab without
  navigating away from the current page. See "Opening a New Tab" below.

---

## Opening a New Tab

Use the `open_tab` tool to open a new browser tab at a given HTTP(S) URL
without disrupting the current tab. The tool returns the new tab's `tabId`,
which you pass to subsequent reads and actions on that tab.

### When to Use `open_tab`

- The user asks to "open this in a new tab" or "open a new tab to …"
- You need to keep the current page intact while working on a second page
  (e.g., comparing two pages, cross-referencing data from two sources)
- A workflow requires two pages open simultaneously in the same browser

### When NOT to Use `open_tab`

- You just need to navigate the current tab — use `navigate_to_url` instead
- The user is already on the target page — just `read_current_page`
- You need to follow a click path on the current page — use `click_element`

### Workflow

#### 1. Check Connection

Call `list_browsers` to confirm a browser is connected.

#### 2. Open the Tab

Call `open_tab` with the URL:

```
open_tab(url: "https://example.com/dashboard")
```

The response includes:

| Field   | Type   | Description                                      |
| ------- | ------ | ------------------------------------------------ |
| `tabId` | string | The new tab's ID — pass to subsequent tool calls |
| `url`   | string | The URL the tab was opened to                    |
| `title` | string | The page title (may be empty until it loads)     |

#### 3. Read and Interact

Pass the returned `tabId` to `read_current_page` and all subsequent calls
on that tab:

```
open_tab(url: "https://example.com")          → { tabId: "12345", ... }
read_current_page(tabId: "12345")              → page context with fresh IDs
click_element(kind: "link", id: "e5", tabId: "12345")
```

**Important**: The new tab may not be the active foreground tab. Always pass
the returned `tabId` — omitting it will target the active tab, which may be
a different page.

#### 4. Handle Errors

| Error Code            | Cause                                                      |
| --------------------- | ---------------------------------------------------------- |
| `unsupported_scheme`  | URL is not http: or https:                                 |
| `open_tab_failed`     | Browser reported an error creating the tab                 |
| `not_supported`       | The connected browser extension doesn't support `open_tab` |
| `browser_unavailable` | No browser extension connected                             |
| `connection_failed`   | Could not reach the Brijio WebSocket server                |

---

## SPA and Dynamic Pages

### Hash Routing

Single-page applications often use hash URLs (`/app#/settings`). The page
doesn't fully reload — only parts of the DOM change. After clicking a link
in an SPA:

1. Re-read the page (the URL and content will update even though it's the same
   browser tab)
2. Look for new content in the `forms`, `links`, and `actions`
3. The `url` field will reflect the new hash route

### Lazy-Loaded Content

Some pages load content after the initial page load (infinite scroll, dynamic
tables). If expected content isn't in the initial `read_current_page` response:

1. Click any "Load more" or "Show all" actions on the page
2. Re-read the page to capture the newly loaded content
3. Repeat if needed

### Redirect Chains

Clicking a link may redirect through one or more intermediate pages. After each
click, always re-read the page — you may end up on a different URL than
expected. Verify the final destination before continuing.

## Pitfalls

### Short-Lived IDs

Element IDs (`e5`, `f2`, `a1`) expire when the page changes. After any click
that triggers navigation, you must call `read_current_page` again before
interacting with new elements.

### Links vs Actions

- **Links** are navigation elements (`<a>` tags). Use `click_element` with
  `kind: "link"`.
- **Actions** are button-like elements (`<button>`, role="button"). Use
  `click_element` with `kind: "action"`.

Clicking an action usually does not navigate — it triggers a form submission,
opens a modal, or performs an in-page action. Clicking a link usually
navigates.

### Duplicate Link Text

Pages may have multiple links with the same text but different URLs (e.g.,
"Learn more" appearing in several sections). Check the `url` field to
disambiguate, or ask the user which one they mean.

### Navigation Timing

After clicking a link, the browser may take time to load the new page. If
`read_current_page` returns stale content (same URL, same elements), wait a
moment and try again. The WebSocket connection will deliver fresh data once the
page finishes loading.

### Multiple Browsers

When multiple browsers are connected, always specify `browserInstanceId` in
your tool calls. Navigation on the wrong browser is disorienting and
potentially destructive.
