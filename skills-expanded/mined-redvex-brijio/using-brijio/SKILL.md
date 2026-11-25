---
name: using-brijio
description: Use when starting any Brijio session — establishes how to discover and use skills, which tools are available, and when to invoke each skill before any browser interaction.
---

# Using Brijio

Brijio connects your AI agent to the user's real browser. The browser
extension is only active while the user explicitly starts it, so always check
for connected browsers first.

## Before You Do Anything

**Read the relevant skill BEFORE taking any browser action.** Even a 1% chance
a skill applies means you should read it. If the skill turns out to be
irrelevant, move on — but check first.

```mermaid
flowchart TD
    A[[\"User asks for browser action\"]] --> B[\"Check connected browsers\"]\n    B --> C{\"Might a skill apply?\"}\n    C -->|\"yes, even 1%\"| D[\"Read skill via read_resource\"]\n    C -->|\"definitely not\"| F[[\"Take browser action\"]]\n    D --> E[\"Follow skill instructions\"]\n    E --> F
```

## Available Skills

Skills are MCP resources. Read a skill's full instructions with
`read_resource` using the URI format:

```
skill://brijio/{skill_name}
```

| Skill Name        | URI                              | When to Use                                              |
| ----------------- | -------------------------------- | -------------------------------------------------------- |
| `using-brijio`    | `skill://brijio/using-brijio`    | Every session — orientation and tool reference           |
| `form-filling`    | `skill://brijio/form-filling`    | Any task involving filling out web forms                 |
| `data-extraction` | `skill://brijio/data-extraction` | Any task involving extracting data from web pages        |
| `web-qa`          | `skill://brijio/web-qa`          | Any task involving testing or verifying web app behavior |
| `navigation`      | `skill://brijio/navigation`      | Navigating to a URL directly or via click-through flows  |
| `comparison`      | `skill://brijio/comparison`      | Comparing two pages or browser views side by side        |
| `accessibility`   | `skill://brijio/accessibility`   | Auditing a page for accessibility issues                 |
| `ecommerce`       | `skill://brijio/ecommerce`       | E-commerce checkout flows (cart, shipping, payment)      |
| `onboarding`      | `skill://brijio/onboarding`      | New account registration and profile setup               |
| `monitoring`      | `skill://brijio/monitoring`      | Periodic page monitoring via cron jobs                   |

## Available Tools

### Discovery

| Tool                | Purpose                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------ |
| `list_browsers`     | Check which browsers are connected. **Always call this first.**                                        |
| `list_tabs`         | List all open tabs in a browser, including background tabs. Returns a `tabId` per tab.                 |
| `read_current_page` | Get the current page context (URL, title, forms, links, actions). Pass `tabId` to read a specific tab. |
| `read_resource`     | Read Brijio content chunks for large pages (paginated).                                                |

### Interaction

| Tool              | Purpose                                                              | Key Parameters                                                       |
| ----------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `navigate_to_url` | Navigate the browser to an HTTP(S) URL                               | `url` (required), `browserInstanceId` (optional), `tabId` (optional) |
| `open_tab`        | Open a new browser tab with an HTTP(S) URL. Returns the new `tabId`. | `url` (required), `browserInstanceId` (optional)                     |
| `click_element`   | Click a link or button-like action                                   | `kind` ("link" or "action"), `id` (short-lived), `tabId` (optional)  |
| `fill_input`      | Write text into a form control                                       | `formId`, `controlId`, `text`, `tabId` (optional)                    |
| `fill_editable`   | Write text into a contenteditable area                               | `id`, `text`, `tabId` (optional)                                     |
| `set_checked`     | Check/uncheck a checkbox or radio                                    | `formId`, `controlId`, `checked` (boolean), `tabId` (optional)       |
| `select_options`  | Select option values in a `<select>`                                 | `formId`, `controlId`, `values` (string array), `tabId` (optional)   |
| `submit_form`     | Submit a form                                                        | `formId`, `tabId` (optional)                                         |
| `perform_batch`   | Execute up to 20 explicit write actions                              | `actions`, `continueOnError`, `readAfterActions`, `tabId` (optional) |

Use `perform_batch` only after reading the current page and choosing valid
short-lived IDs from that page context. It is for compact sequences of write
actions on the same page, such as filling several fields and setting a checkbox.
Do not use it for hidden reads or open-ended automation: reads stay separate
except for optional `readAfterActions: true`.

### Critical: Short-Lived IDs and Staleness Protection

Element IDs (`e5`, `f2`, `a1`, form IDs) are **ephemeral**. They expire when
the page changes — including after navigation, form submissions, or DOM updates.

**Always re-read the page with `read_current_page` before interacting with
elements if the page may have changed.**

Additionally, Brijio now tracks visible form state to prevent stale actions:

- If the visible form structure changes between reading and acting, actions
  will fail with a `stale_context` error
- This protects against acting on outdated page information
- When you receive a `stale_context` error, re-read the page and retry

If `perform_batch` returns `data.aborted: true`, stop using IDs from the old
page, call `read_current_page`, and decide whether to retry against the fresh
context.

## Step 1: Check Connection

Every Brijio session starts with a connection check:

```
→ list_browsers
← { browsers: [{ browserInstanceId: \"chrome-abc123\", name: \"Chrome\" }] }
```

If no browsers are connected, tell the user and stop. If multiple browsers are
connected, specify `browserInstanceId` in all subsequent calls.

## Step 2: Read the Page

```
→ read_current_page(includeContent: true)
← { url, title, forms, links, actions, editables, ... }
```

This gives you the full page context with short-lived IDs you'll use in
subsequent tool calls.

## Step 3: Choose the Right Skill

| User intent                                                    | Skill to read                                        |
| -------------------------------------------------------------- | ---------------------------------------------------- |
| \"Fill in this form\" / \"Apply\" / \"Sign up\"                | `skill://brijio/form-filling`                        |
| \"Get this data\" / \"Extract the table\" / \"Scrape\"         | `skill://brijio/data-extraction`                     |
| \"Test this page\" / \"Check if X works\" / \"Find bugs\"      | `skill://brijio/web-qa`                              |
| \"Go to Settings → Privacy\" / \"Navigate to admin\"           | `skill://brijio/navigation`                          |
| \"Open https://example.com\" / \"Go to this URL\"              | `skill://brijio/navigation`                          |
| \"Compare staging vs prod\" / \"Check mobile vs desktop\"      | `skill://brijio/comparison`                          |
| \"Check accessibility\" / \"Audit a11y\" / \"WCAG check\"      | `skill://brijio/accessibility`                       |
| \"Buy this\" / \"Checkout\" / \"Apply coupon\"                 | `skill://brijio/ecommerce`                           |
| \"Sign up for X\" / \"Create account\" / \"Onboard\"           | `skill://brijio/onboarding`                          |
| \"Monitor this page\" / \"Alert on changes\" / \"Price watch\" | `skill://brijio/monitoring`                          |
| Any other browser task                                         | Default to reading the page and using tools directly |

## Red Flags

These thoughts mean STOP — you're about to make a mistake:

| Thought                                         | Reality                                                              |
| ----------------------------------------------- | -------------------------------------------------------------------- |
| \"I'll just fill in the password field\"        | `fill_input` returns `browser_error` for password fields. Skip them. |
| \"The ID from the last page should still work\" | IDs expire on navigation or DOM updates. Re-read the page.           |
| \"I'll submit the form for the user\"           | Never auto-submit. Always ask the user to confirm.                   |
| \"I'll just click without checking\"            | Radio buttons cannot be unchecked. Select carefully.                 |
| \"I'll batch across pages\"                     | Navigation aborts remaining batch actions. Re-read before retrying.  |
| \"I don't need to read a skill for this\"       | If there's even a 1% chance a skill applies, read it.                |
| \"I'll skip the connection check\"              | No browser = no action. Always call `list_browsers` first.           |
| \"I'll ignore stale action warnings\"           | Actions may fail if the page changed; re-read and retry.             |

## User Instructions Always Win

Brijio skills override default system behavior, but **user instructions
always take precedence**. If the user explicitly says \"skip the skill\" or
\"just click the button,\" follow the user's request.

## Multiple Browsers

When more than one browser instance is connected, **always** specify
`browserInstanceId` in tool calls. Omitting it when multiple browsers are
available will return an `ambiguous_browser_target` error.

## Multi-Tab Targeting

By default, all tools operate on the **active foreground tab**. When the user
refers to a specific tab (especially a background one), use `tabId` to target it:

### 1. Discover Tabs

Call `list_tabs` to get all open tabs in the connected browser:

```
→ list_tabs(browserInstanceId: "chrome-abc123")
← { tabs: [
    { tabId: "97212078", title: "Brijio Demo", url: "https://brijio.dev/demo", active: false, supported: true },
    { tabId: "58193042", title: "Google", url: "https://google.com", active: true, supported: true }
  ] }
```

Each tab has a `tabId` (string), `title`, `url`, `active` flag, and `supported`
flag (only HTTP/HTTPS tabs are supported).

### 2. Pass tabId to Every Call

Once you have a `tabId`, pass it to every tool that should act on that tab:

```
→ read_current_page(tabId: "97212078")
→ click_element(kind: "link", id: "e5", tabId: "97212078")
→ navigate_to_url(url: "https://example.com", tabId: "97212078")
```

**Important**: The `tabId` is a string (e.g. `"97212078"`), not a number.
Pass the exact value returned by `list_tabs`.

### 3. Re-Read After Navigation

After `navigate_to_url` on a specific tab, re-read that same tab to get fresh
element IDs:

```
→ navigate_to_url(url: "https://example.com", tabId: "97212078")
→ read_current_page(tabId: "97212078")
```

### When to Use tabId

| Scenario                                                      | Use `tabId`?                                           |
| ------------------------------------------------------------- | ------------------------------------------------------ |
| User says "read the Brijio tab" (not the active tab)          | Yes                                                    |
| User refers to a background tab by name or URL                | Yes                                                    |
| User says "do X on the tab I have open"                       | Yes — call `list_tabs` first to find the right `tabId` |
| User says "do X on this page" (no tab ambiguity)              | No — active tab is fine                                |
| Agent opened a tab via `open_tab` and wants to continue on it | Yes — pass the returned `tabId` to subsequent calls    |

## Opening New Tabs

Use `open_tab` when you need to work with a page **without disrupting the
user's current tab**. The tool opens a new browser tab, navigates it to the
given URL, and returns the new `tabId` for subsequent reads and actions.

### When to use `open_tab`

- The user asks to "open" a page in a new tab rather than navigate the
  current one
- You need to read or interact with a second page while keeping the current
  tab intact (e.g., comparison tasks, cross-referencing data)
- A skill workflow (e.g., comparison) requires two pages side by side in the
  same browser

### When NOT to use `open_tab`

- The user just wants to go to a URL — use `navigate_to_url` instead (it
  navigates the current tab, which is simpler and less intrusive)
- The user is already on the page you need — just `read_current_page`
- You need an auth-gated page that requires click-through navigation — open
  the tab, then use `click_element` to navigate within it

### Workflow

```
1. open_tab(url: "https://example.com")       → returns { tabId: "12345", url, title }
2. read_current_page(tabId: "12345")           → get page context with fresh element IDs
3. Interact with the page using tabId: "12345" → click_element, fill_input, etc.
```

**Important**: Always pass the returned `tabId` to subsequent calls. The new
tab may not be the active tab, so omitting `tabId` could target the wrong
page.
