---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)
- `scripts/cdp_connect.py` - Connects to a running Electron app via CDP

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it an Electron app?
    ├─ Yes → Is CDP available (port 9222)?
    │     ├─ No  → Start Electron with --remote-debugging-port=9222
    │     │        Validate: python scripts/cdp_connect.py --validate-only
    │     └─ Yes → Run: python scripts/cdp_connect.py --help
    │              Then use helper + write Playwright script (connect_over_cdp)
    │
    └─ No → Is it static HTML?
        ├─ Yes → Read HTML file directly to identify selectors
        │         ├─ Success → Write Playwright script using selectors
        │         └─ Fails/Incomplete → Treat as dynamic (below)
        │
        └─ No (dynamic webapp) → Is the server already running?
            ├─ No → Run: python scripts/with_server.py --help
            │        Then use the helper + write simplified Playwright script
            │
            └─ Yes → Reconnaissance-then-action:
                1. Navigate and wait for networkidle
                2. Take screenshot or inspect DOM
                3. Identify selectors from rendered state
                4. Execute actions with discovered selectors
```

## Electron App Testing (via CDP)

To test an Electron desktop app, connect to it via Chrome DevTools Protocol using Playwright's `connect_over_cdp()`. This gives full Playwright API access inside the real Electron renderer (including `window.electronAPI`).

### Prerequisites

1. Start Electron with remote debugging enabled:
   ```bash
   electron . --remote-debugging-port=9222
   # Or for Vesper: bun run electron:dev  (ensure --remote-debugging-port=9222 is set)
   ```

2. Validate CDP is reachable:
   ```bash
   python scripts/cdp_connect.py --validate-only
   ```
   See also: `electron-cdp-testing` skill's `validate-setup.sh` for deeper environment checks.

### Usage with cdp_connect.py

```bash
# Run a test script with CDP_ENDPOINT auto-set
python scripts/cdp_connect.py -- python your_test.py

# Custom port
python scripts/cdp_connect.py --port 9223 -- python your_test.py
```

### Code Pattern

```python
from playwright.sync_api import sync_playwright
import os

CDP_ENDPOINT = os.environ.get("CDP_ENDPOINT", "http://localhost:9222")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
    context = browser.contexts[0]       # Existing Electron context
    page = context.pages[0]             # Existing Electron page
    page.wait_for_load_state('networkidle')

    # Full Playwright API works: locators, screenshots, evaluate, etc.
    page.screenshot(path='/tmp/electron.png')

    # Access Electron's preload bridge
    has_api = page.evaluate("typeof window.electronAPI !== 'undefined'")

    # CRITICAL: Do NOT call browser.close() — it kills the Electron app!
```

### Common Pitfall

- **Never call `browser.close()`** when connected via CDP. The close command terminates the Electron process. Simply let the script end without closing.
- **Use `browser.contexts[0].pages[0]`** to access the existing Electron page. Do not create new pages/contexts — they won't have `electronAPI`.

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly.
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done — **except** when connected via CDP to Electron (never call `browser.close()` in that case)
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation
  - `electron_app_testing.py` - Basic Electron app testing via CDP (element discovery, screenshots, electronAPI detection)
  - `electron_ipc_testing.py` - Electron IPC testing (calling electronAPI methods, console capture, UI→IPC flows)