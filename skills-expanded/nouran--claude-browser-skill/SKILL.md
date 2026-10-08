---
name: browser
description: Automate browser interactions using agent-browser CLI — navigate, click, fill forms, scrape content, take screenshots, and more.
argument-hint: <command> [args...]
allowed-tools: Bash(npx agent-browser *)
---

# Browser Automation with agent-browser

Control a headless Chromium browser via CLI commands. All commands are run with `npx agent-browser <command>`.

## Setup (first time only)

```bash
npx agent-browser install
```

## Navigation

| Command | Description |
|---|---|
| `open <url>` | Navigate to a URL |
| `close` | Close browser |
| `tab` | List open tabs |
| `tab new [url]` | Open new tab |
| `tab <n>` | Switch to tab n |
| `tab close [n]` | Close tab |
| `window new` | Open new browser window |
| `frame <selector>` | Switch to iframe |
| `frame main` | Return to main frame |

## Page Inspection (use these to understand page structure)

| Command | Description |
|---|---|
| `snapshot` | Get accessibility tree with `@e1`, `@e2` element refs (best for AI) |
| `screenshot [path]` | Capture screenshot |
| `screenshot --full` | Full page screenshot |
| `screenshot --annotate` | Screenshot with numbered element labels |
| `get text <sel>` | Extract text content |
| `get html <sel>` | Get innerHTML |
| `get value <sel>` | Get input value |
| `get attr <sel> <attr>` | Get element attribute |
| `get title` | Get page title |
| `get url` | Get current URL |
| `get count <sel>` | Count matching elements |
| `get box <sel>` | Get bounding box |
| `get styles <sel>` | Get computed styles |
| `is visible <sel>` | Check if element is visible |
| `is enabled <sel>` | Check if element is enabled |
| `is checked <sel>` | Check if checkbox is checked |

## Clicking & Interaction

| Command | Description |
|---|---|
| `click <sel>` | Click an element |
| `click <sel> --new-tab` | Click, opening in new tab |
| `dblclick <sel>` | Double-click |
| `hover <sel>` | Hover over element |
| `focus <sel>` | Focus element |
| `scroll <dir> [px]` | Scroll up/down/left/right |
| `scrollintoview <sel>` | Scroll element into view |
| `drag <src> <tgt>` | Drag and drop |

## Text Input

| Command | Description |
|---|---|
| `fill <sel> <text>` | Clear field and type text |
| `type <sel> <text>` | Type into focused element (appends) |
| `keyboard type <text>` | Type with real keystrokes |
| `keyboard inserttext <text>` | Insert text without key events |
| `press <key>` | Press a key (Enter, Tab, Control+a, etc.) |
| `keydown <key>` | Hold key down |
| `keyup <key>` | Release key |

## Form Controls

| Command | Description |
|---|---|
| `check <sel>` | Check a checkbox |
| `uncheck <sel>` | Uncheck a checkbox |
| `select <sel> <val>` | Select dropdown option |
| `upload <sel> <files>` | Upload file(s) to input |

## Semantic Find (locate elements by meaning, not CSS)

```
find role <role> <action> [value]         # By ARIA role
find text <text> <action>                 # By visible text
find label <label> <action> [value]       # By label
find placeholder <ph> <action> [value]    # By placeholder
find alt <text> <action>                  # By alt text
find title <text> <action>                # By title attribute
find testid <id> <action> [value]         # By data-testid
find first <sel> <action> [value]         # First match
find last <sel> <action> [value]          # Last match
find nth <n> <sel> <action> [value]       # Nth match
```

**Actions:** `click`, `fill`, `type`, `hover`, `focus`, `check`, `uncheck`, `text`

**Options:** `--name <name>` (filter by accessible name), `--exact` (exact match)

**Examples:**
```bash
npx agent-browser find role button click --name "Submit"
npx agent-browser find text "Sign In" click
npx agent-browser find label "Email" fill "user@example.com"
npx agent-browser find placeholder "Search..." fill "vinyl records"
```

## Waiting

| Command | Description |
|---|---|
| `wait <selector>` | Wait for element to appear |
| `wait <ms>` | Wait N milliseconds |
| `wait --text "text"` | Wait for text to appear |
| `wait --url "**/path"` | Wait for URL pattern |
| `wait --load networkidle` | Wait for network idle |
| `wait --fn "window.ready"` | Wait for JS condition |

## Cookies & Storage

| Command | Description |
|---|---|
| `cookies` | Get all cookies |
| `cookies set <name> <val>` | Set a cookie |
| `cookies clear` | Clear cookies |
| `storage local` | Get all localStorage |
| `storage local <key>` | Get localStorage key |
| `storage local set <k> <v>` | Set localStorage value |
| `storage local clear` | Clear localStorage |
| `storage session` | Same commands for sessionStorage |

## Network Interception

| Command | Description |
|---|---|
| `network route <url>` | Intercept requests matching URL |
| `network route <url> --abort` | Block matching requests |
| `network route <url> --body <json>` | Mock response body |
| `network unroute [url]` | Remove intercept routes |
| `network requests` | View tracked requests |
| `network requests --filter <pat>` | Filter requests by pattern |

## JavaScript Execution

| Command | Description |
|---|---|
| `eval <js>` | Run JavaScript in page context |
| `eval -b <base64>` | Run base64-encoded JS |

## Browser Configuration

| Command | Description |
|---|---|
| `set viewport <w> <h>` | Set viewport size |
| `set device <name>` | Emulate device (e.g. "iPhone 14") |
| `set media dark` | Emulate dark color scheme |
| `set media light` | Emulate light color scheme |
| `set offline on` | Enable offline mode |
| `set offline off` | Disable offline mode |
| `set geo <lat> <lng>` | Set geolocation |
| `set headers <json>` | Set extra HTTP headers |
| `set credentials <user> <pass>` | Set HTTP basic auth |

## Mouse Control

| Command | Description |
|---|---|
| `mouse move <x> <y>` | Move cursor to coordinates |
| `mouse down [button]` | Press mouse button |
| `mouse up [button]` | Release mouse button |
| `mouse wheel <dy> [dx]` | Scroll wheel |

## State Persistence

| Command | Description |
|---|---|
| `state save <path>` | Save auth/session state |
| `state load <path>` | Load saved state |
| `state list` | List saved states |
| `state clear [name]` | Clear a saved state |
| `state clear --all` | Clear all saved states |

## Debugging

| Command | Description |
|---|---|
| `console` | View console messages |
| `errors` | View uncaught exceptions |
| `highlight <sel>` | Visually highlight element |
| `trace start [path]` | Start trace recording |
| `trace stop [path]` | Stop and save trace |
| `profiler start` | Start CPU profiling |
| `profiler stop [path]` | Save profile |
| `pdf <path>` | Save page as PDF |

## Comparison & Diffing

| Command | Description |
|---|---|
| `diff snapshot` | Compare current vs previous snapshot |
| `diff snapshot --baseline <file>` | Compare against saved file |
| `diff screenshot --baseline <file>` | Visual pixel comparison |
| `diff url <a> <b>` | Compare two URLs |

## Typical Workflow

1. **Open a page:** `open http://localhost:3000`
2. **Inspect structure:** `snapshot` (returns element refs like `@e1`, `@e2`)
3. **Interact using refs:** `click @e3` or `fill @e5 "my text"`
4. **Verify results:** `get text @e7` or `screenshot`
5. **Close when done:** `close`

## Selectors

Commands accept these selector types:
- **Element refs** from snapshot: `@e1`, `@e2`, etc. (preferred for AI)
- **CSS selectors:** `#id`, `.class`, `div > span`
- **XPath:** `//button[@type="submit"]`
- **Semantic find:** Use the `find` command family above

## Default Login Flow

When testing locally, log in first before performing authenticated browser actions:
- URL: http://localhost:3000/auth
- Use Supabase Auth (email/password)

## Project-Specific Pages

Key pages to test in the MVP boilerplate:

| Page | URL | Notes |
|---|---|---|
| Landing | `http://localhost:3000` | Sections: Navbar, Hero, Logos, Items, Stats, Pricing, FAQ, Cta, Footer |
| Sign In / Sign Up | `http://localhost:3000/auth` | Supabase Auth UI |
| Account | `http://localhost:3000/account` | Authenticated - user profile & subscription |
| Pricing | `http://localhost:3000/#pricing` | Stripe checkout integration |

## Testing Dark Mode

```bash
# Toggle dark mode via the ModeToggle button in the navbar
npx agent-browser find role button click --name "Toggle theme"

# Or force via browser emulation
npx agent-browser set media dark
npx agent-browser set media light
```

## Testing Responsive Design

```bash
# Mobile
npx agent-browser set viewport 375 812

# Tablet
npx agent-browser set viewport 768 1024

# Desktop
npx agent-browser set viewport 1440 900
```
