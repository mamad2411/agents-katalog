---
name: stealth-browser-mcp
description: MCP server providing browser automation tools that bypass Cloudflare, LinkedIn, Indeed, and other WAF-protected sites using agent-browser with anti-detection stealth.
version: 1.1.0
author: Dustin Chadwick (@ShaggyD)
tags: [browser, automation, stealth, mcp, cloudflare, bypass, agent-browser, web-scraping]
license: MIT
---

# Stealth Browser MCP

An MCP server that provides browser automation tools with built-in WAF and Cloudflare bypass. Uses agent-browser CLI with anti-detection Chrome flags and a bundled stealth extension.

## Problem

Browser automation MCP servers hit the same WAF blocks as everything else. Cloudflare, LinkedIn, and Indeed detect headless Chrome before your first tool call completes. Running a browser MCP server means either accepting the blocks or maintaining a separate stealth setup that has to stay in sync.

## Built

An MCP server that wraps agent-browser CLI with anti-detection flags and a stealth extension bundled inline -- no external dependency on a separate skill or extension install. Exposes 10 tools: navigate, snapshot, click, eval, type, set_viewport, screenshot, close, status, and install. The stealth extension patches browser fingerprint vectors at document_start, before any page scripts can detect them.

## Outcome

Works through Cloudflare, LinkedIn, and other WAFs from any MCP-compatible agent. Zero external dependencies beyond agent-browser itself. Drop in the MCP registration, install agent-browser, and your agent has full browser automation that bypasses protections.

## How it works

The stealth extension + Chrome flags trick the site into thinking you're a real user on a real Chrome browser:

| Technique | What it does |
|-----------|-------------|
| `--disable-blink-features=AutomationControlled` | Removes Chrome's automation flag |
| Real Chrome 125 user agent | Masks headless browser identity |
| Stealth content script | Patches `navigator.webdriver` → `undefined`, adds plugins, fixes languages |
| Consistent viewport (1920×1080) | Avoids headless screen-size detection |
| Extension loaded at `document_start` | Patches fire before any page JS runs |

## Installation

### 1. Install dependencies

```bash
npm install -g agent-browser
agent-browser install --with-deps
```

### 2. Register the MCP server

```bash
# Find the server script
MCP_SERVER="$HOME/.hermes/skills/software-development/stealth-browser-mcp/assets/mcp_server.py"

# Register with the agent
hermes mcp add stealth-browser --command "python3 $MCP_SERVER"
```

Or add to `config.yaml`:

```yaml
mcp_servers:
  stealth-browser:
    command: python3
    args: ["~/.hermes/skills/software-development/stealth-browser-mcp/assets/mcp_server.py"]
    timeout: 120
```

### 3. Start a fresh session

```bash
hermes chat --reset
```

The stealth browser tools will appear in the agent's tool list automatically.

## Available Tools

| Tool | Description |
|------|-------------|
| `navigate` | Open a URL with full stealth protection |
| `snapshot` | Get page content as readable text |
| `click` | Click an element by accessibility ref ID (e.g., `@e3`) |
| `eval` | Execute JavaScript and return the result |
| `type` | Type text into a form field |
| `set_viewport` | Set viewport dimensions (default 1920×1080) |
| `screenshot` | Take a full-page screenshot (base64) |
| `close` | Close the browser session |
| `status` | Check if agent-browser and Chromium are installed |
| `install` | Install or verify agent-browser + Chromium deps |

## Usage

Once registered, the agent can use the tools naturally:

> "Navigate to https://www.linkedin.com/jobs/search/?keywords=admin&location=Remote"
> "Get the page text"
> "Click @e5 to see job details"
> "Check the stealth browser status"

### Typical workflow

1. `navigate` to the target URL
2. `snapshot` to see page content with element refs (shown as `@e1`, `@e2`, etc.)
3. `click` on elements to interact, expand, or navigate further
4. `eval` to extract structured data (pricing, job listings, search results)
5. `screenshot` for visual confirmation
6. `close` when done

## Job Search Example (LinkedIn, no login)

```python
# 1. Navigate to LinkedIn jobs
navigate("https://www.linkedin.com/jobs/search/?keywords=front+office+coordinator&location=American+Fork%2C+Utah&f_TPR=r604800")

# 2. Extract job listings
eval("""
JSON.stringify(
  Array.from(document.querySelectorAll('.job-card-container')).map(c => ({
    title: c.querySelector('.job-card-list__title')?.innerText?.trim(),
    company: c.querySelector('.job-card-container__company-name')?.innerText?.trim(),
    location: c.querySelector('.job-card-container__metadata-item')?.innerText?.trim(),
    link: c.querySelector('a')?.href
  }))
)
""")

# 3. Click into a specific job
click("@e3")

# 4. Get full description
snapshot()
```

## Self-Contained

The MCP server is fully self-contained — the stealth extension JS and manifest are bundled inline in the Python script. On startup, it extracts them to a temporary directory. No external skill or file dependencies.

## Requirements

- Python 3.10+
- `mcp` package (`pip install mcp`)
- `agent-browser` CLI + Chromium (`npm install -g agent-browser && agent-browser install --with-deps`)

## Troubleshooting

### MCP server registers but tools return errors

```bash
# Check the server connected and found tools
hermes mcp test stealth-browser

# Check agent-browser is installed and Chromium is ready
agent-browser doctor
```

### "Daemon already running" conflicts

If agent-browser was used manually before starting the MCP server, close orphaned daemons:

```bash
agent-browser close --all
```

Then the next `navigate` call will start a fresh session.

### Eval returns "(empty result)"

The page may not have finished loading. Call `navigate` first, wait briefly, then `eval`. For pages with heavy JS rendering, use `eval("document.readyState")` to check if the page is fully loaded.

### Server exits immediately after starting

Check stderr for import errors:

```bash
python3 /path/to/mcp_server.py 2>&1 </dev/null | head -5
```

Most common: `pip install mcp` is missing.

### Chrome for Testing vs real Chromium — WAF fingerprinting gap

agent-browser downloads and uses **"Google Chrome for Testing"** — a special Chromium build with a distinct binary fingerprint. Aggressive WAFs like DataDome (Wellfound, some enterprise portals) can identify Chrome for Testing by its binary signatures alone, even when all stealth patches are passing (`webdriver: false`, clean UA, extension loaded) and the browser runs in headed mode. This is independent of any flag or extension — the binary itself is the tell.

**Signs you're hitting this:** The page shows "Access is temporarily restricted" / DataDome CAPTCHA despite all stealth patches passing. Your real browser on the same IP works fine.

**Fix:**

1. Install system Chromium:
```bash
sudo apt-get install chromium-browser
```

2. Override agent-browser's Chrome binary:
```bash
export AGENT_BROWSER_CHROME_PATH=/snap/bin/chromium
```

3. For aggressive WAFs, also use headed mode:
```bash
AGENT_BROWSER_CHROME_PATH=/snap/bin/chromium \
AGENT_BROWSER_HEADED=true \
agent-browser open <url> --args "--no-sandbox" --headed
```

4. For the MCP server, wrap with `env`:
```yaml
mcp_servers:
  stealth-browser:
    command: env
    args:
      - AGENT_BROWSER_CHROME_PATH=/snap/bin/chromium
      - python3
      - /path/to/mcp_server.py
    enabled: true
```

**Persistence:** DataDome may learn the system Chromium fingerprint after the first request. Each fresh browser launch buys one successful page load. Pair with a residential proxy for recurring scraping.

## Architecture

See `references/architecture.md` for detailed design: daemon lifecycle, JSON response unwrapping, thread safety model, command output shapes, and stealth extension internals.
