---
name: obo
description: Control the user's real Chrome browser with their logged-in sessions, cookies, and extensions. Triggers include "open a website", "click a button", "fill a form", "take a screenshot", "check my email", "browse as me", or any task requiring the user's authenticated browser.
allowed-tools: Bash(obo:*), Bash(npx @agenthand/obo:*)
---

# obo — Open Browser Operator

Control the user's real Chrome browser via CLI. The browser keeps all logins, cookies, and extensions.

## Prerequisites

1. The Chrome extension **Open Browser Operator** must be installed and enabled.
2. The `obo` server must be running (`obo` or `obo server`).
3. Use the default `127.0.0.1:3333` unless the user is already in an advanced connection setup.

Check with:

```bash
obo doctor
obo status
```

`obo status` only checks connectivity; it does not auto-start the server.

If the server is not running, start it:

```bash
obo &
```

## Server URL Selection (Important)

`obo` defaults to `http://127.0.0.1:3333`. Most users should not change this.

If the extension popup shows another endpoint because the user already configured Advanced connection settings, use that server URL explicitly:

```bash
obo status --url http://192.168.0.139:3334
```

For multi-command sessions, set once:

```bash
export OBO_URL=http://192.168.0.139:3334
obo status
obo tabs
```

Only suggest LAN or non-loopback hosts when one of these is true:

1. The browser environment cannot reach `127.0.0.1`.
2. The extension popup already uses a reachable machine address instead of `127.0.0.1`.
3. `obo status` works on `127.0.0.1:<port>` in terminal, but the extension still cannot connect.
4. Extension logs show repeated connection failures for the configured websocket endpoint.

When this is truly needed, start the server with:

```bash
obo server --host 0.0.0.0 --port <PORT>
```

Then align the extension Advanced host/port and CLI URL:

```bash
export OBO_URL=http://<REACHABLE_HOST>:<PORT>
obo status
```

Use this only on a trusted local network. Switch back to `127.0.0.1` when the advanced setup is no longer needed.

Quick diagnostics:

- `ERR_CONNECTION_REFUSED`: wrong port/host or server not listening on that address.
- `ERR_SOCKS_CONNECTION_FAILED`: browser or network proxy path issue.

## Core Workflow

Every browser task follows this loop:

```
obo tabs              → pick a tabId (or create one with `obo new`)
obo snapshot <id> -i  → read the page (interactive elements only)
obo click/type/scroll → interact
obo snapshot <id> -i  → verify the result
```

Always re-snapshot after any interaction — element refs (`@e1`, `@e2`, ...) are invalidated when the page changes.
Each snapshot includes `snapshotId` for traceability.

When opening or attaching a tab for a distinct user task, pass a short semantic group title:

```bash
obo new "https://example.com" --group "Market Research"
obo attach <tabId> --group "Market Research"
```

Keep group titles short (2-5 words). OBO prefixes them in Chrome as `OBO: <title>`.

## Commands

### Check Status

```bash
obo doctor
obo status
obo status --url http://127.0.0.1:3334
```

Use `obo doctor` first for human-readable diagnostics. Use `obo status` when you need raw JSON connection status and active sessions.

### List Tabs

```bash
obo tabs
```

Returns all open tabs with their `id`, `url`, and `title`. Pick the `id` for subsequent commands.

### Open New Tab

```bash
obo new                    # blank tab
obo new "https://github.com"  # navigate immediately
obo new "https://github.com" --group "GitHub Review"
```

Returns the new tab's info including its `id`.

### Close Tab

```bash
obo close <tabId>
```

### Activate Tab

```bash
obo attach <tabId>
obo attach <tabId> --group "Market Research"
```

Attaches the debugger and groups the tab. Use `--group` when the task has a meaningful short name.

### Navigate

```bash
obo open <tabId> "https://example.com"
obo navigate <tabId> "https://example.com"  # alias for open
```

Navigates an existing tab to a URL. Wait briefly, then snapshot to see the result.

### Snapshot (Accessibility Tree)

```bash
obo snapshot <tabId>       # full tree
obo snapshot <tabId> -i    # interactive elements only (recommended)
```

Returns a plain-text accessibility tree. With `-i`, only interactive elements (buttons, links, inputs, etc.) are shown, each labeled with a ref like `@e0`, `@e1`.

Example output:

```
document "GitHub"
  heading "Dashboard"
  link "Pull requests" @e0
  link "Issues" @e1
  textbox "Search or jump to..." @e2
  button "New repository" @e3
```

**Always use `-i`** unless you need the full page structure. It dramatically reduces output size.

### Extract (Normalized Page Content)

```bash
obo extract <tabId>                    # JSON (default)
obo extract <tabId> --format json
obo extract <tabId> --format md
```

Use `extract` for read-heavy tasks (summaries, lead discovery, content review).
Use `snapshot -i` for interaction-heavy tasks.

### Screenshot

```bash
obo screenshot <tabId>                 # save to temp file, print path (default)
obo screenshot <tabId> -o page.png     # save to specific file
obo screenshot <tabId> --base64        # output base64 to stdout
```

By default, screenshots are saved to `~/.obo/tmp/screenshots/` and the file path is printed. This is agent-friendly — you can use the Read tool to view the image directly.

Use `-o` to save to a specific location, or `--base64` (or `-b`) for programmatic use.

### Click

```bash
obo click <tabId> @e1          # click by ref
obo click <tabId> 500 300      # click by coordinates (x y)
```

Prefer refs over coordinates. Always re-snapshot after clicking — the page may have changed.

### Type

```bash
obo type <tabId> @e2 "hello world"           # type into element
obo type <tabId> @e2 "search query" --submit  # type and press Enter
```

The `--submit` flag presses Enter after typing — useful for search boxes and forms.

### Scroll

```bash
obo scroll <tabId>                  # scroll down (default: 500px)
obo scroll <tabId> --dy -500        # scroll up
obo scroll <tabId> --dy 500 --ref @e1  # scroll within element
obo scroll <tabId> --dx 300         # scroll right
```

### Wait

```bash
obo wait <tabId> --load [--timeout 10000]
obo wait <tabId> --idle [--timeout 10000] [--idle-time 500]
```

`wait` returns structured JSON fields (`ok`, `timedOut`, plus mode-specific metadata).

### Evaluate JavaScript

```bash
obo eval <tabId> "document.title"                    # direct expression
obo eval <tabId> -f /tmp/script.js                   # from file
obo eval <tabId> --stdin < script.js                 # from stdin
obo eval <tabId> -b "ZG9jdW1lbnQudGl0bGU="           # base64-encoded
```

Returns the result as JSON. Use for extracting data or performing actions not covered by other commands.

**Shell quoting issues?** Complex JavaScript with nested quotes can break in the shell. Use one of these alternatives:

- **`-f <file>`**: Read script from file (most reliable for complex code)
- **`--stdin`**: Pipe script via stdin: `cat script.js | obo eval <tabId> --stdin`
- **`-b <base64>`**: Base64-encode the script to bypass all shell escaping

## Ref Lifecycle

Refs (`@e0`, `@e1`, ...) are assigned per-snapshot. They become **invalid** after:

- Any click, type, or scroll that changes the page
- Navigation (`obo open`)
- Page-initiated navigation (e.g., clicking a link)

**Always re-snapshot** before using refs. Using stale refs will fail or target the wrong element.

## Error Codes and Recovery

Most failures return `{ error, code }`. Handle by `code`, not only message text.

- `EXTENSION_NOT_CONNECTED`: run `obo status` (or `obo status --url <popup-matched-http-url>`), ensure extension/server are active, then retry.
- `TAB_ID_REQUIRED`: run `obo tabs`, select a valid tab, retry.
- `TARGET_REQUIRED`: run fresh `obo snapshot <tabId> -i`, then retry with a new `@e*`.
- `URL_REQUIRED` / `TEXT_REQUIRED` / `FILES_REQUIRED` / `EXPRESSION_REQUIRED`: fix payload and retry.
- `REQUEST_TIMEOUT`: retry once with smaller scope.
- `INTERNAL_ERROR`: stop and report route + payload summary.

Reference: `docs/ERROR_CODES.md`.

## Output Formats

| Command | Output |
|---------|--------|
| `doctor` | Plain text diagnostics |
| `snapshot` | Plain text (accessibility tree) |
| `extract --format md` | Plain text (Markdown) |
| `screenshot` | File path (default) or base64 (with `--base64`) |
| `tabs` | JSON array |
| `status` | JSON object |
| All others | JSON object |

## Tips

- **Start with `obo tabs`** to see what's available before interacting.
- **Always use `-i`** with snapshot to keep output small and focused.
- **Re-snapshot after every interaction** — refs change when the page changes.
- **Use `obo new` + `obo open`** instead of navigating in existing tabs if you don't want to disrupt the user's browsing.
- **Use `--submit`** with `obo type` for search boxes to avoid a separate Enter keystroke.
- **Check `obo status`** first if commands fail — the extension may be disconnected.
- **Multiple interactions?** Do them one at a time: act → snapshot → verify → next action.

## Example: Check GitHub Notifications

```bash
obo tabs                           # find GitHub tab or...
obo new "https://github.com/notifications"  # open notifications
# wait a moment for page load
obo snapshot <tabId> -i            # see notification links
obo click <tabId> @e2              # click a notification
obo snapshot <tabId> -i            # read the content
```

## Example: Fill a Form

```bash
obo snapshot <tabId> -i            # see form fields
obo click <tabId> @e1              # focus first field
obo type <tabId> @e1 "John Doe"   # fill name
obo type <tabId> @e2 "john@example.com"  # fill email
obo click <tabId> @e5              # click submit
obo snapshot <tabId> -i            # verify result
```
