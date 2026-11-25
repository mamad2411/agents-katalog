---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
version: 1.0.0
---

# Browser Automation — agent-browser

Install: `npm i -g agent-browser` then `agent-browser install` (downloads Chromium).  
Full slash-command reference: see `commands/agent-browser.md` or use `/agent-browser`.

## Core Workflow

Every automation follows these 4 steps:

1. **Navigate** — `agent-browser open <url>`
2. **Snapshot** — `agent-browser snapshot -i` (get refs: `@e1`, `@e2`, ...)
3. **Interact** — use refs to click/fill/select
4. **Re-snapshot** — ALWAYS re-snapshot after page changes

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "pass" && agent-browser click @e3
agent-browser wait --load networkidle && agent-browser snapshot -i
```

**Important:** Refs (`@e1`) are invalidated on page change. Always re-snapshot after navigation, form submit, or modal actions.

## Chaining

Chain with `&&` when intermediate output is not needed:

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

## Authentication

**Preferred — auth vault (encrypted, reusable):**
```bash
echo "$PASS" | agent-browser auth save myapp --url https://app.com/login --username user --password-stdin
agent-browser auth login myapp
```

> **Security:** Always pass passwords via `--password-stdin` (pipe from env var). Never pass a password as a CLI argument — it will be visible in shell history and process listings.

**Persistent profile:**
```bash
agent-browser --profile ~/.myapp open https://app.com/login
```

## Essential Commands

```bash
# Navigation
agent-browser open <url>                    # Go to URL
agent-browser close                         # Close browser

# Snapshot & Interaction
agent-browser snapshot -i                   # Interactive snapshot with refs
agent-browser snapshot -s "#selector"       # Scoped snapshot
agent-browser click @e1                     # Click element
agent-browser fill @e2 "text"               # Clear + type
agent-browser type @e2 "text"               # Type without clearing
agent-browser select @e1 "option"           # Select dropdown
agent-browser check @e1                     # Toggle checkbox
agent-browser press Enter                   # Press key
agent-browser scroll down 500              # Scroll pixels

# Data Extraction
agent-browser get text @e1                  # Element text
agent-browser get url                       # Current URL
agent-browser get title                     # Page title

# Waiting
agent-browser wait @e1                      # Wait for element
agent-browser wait --load networkidle       # Wait for network idle
agent-browser wait --url "**/dashboard"     # Wait for URL match
agent-browser wait --text "Welcome"         # Wait for text visible
agent-browser wait 2000                     # Wait milliseconds

# Capture
agent-browser screenshot                    # Viewport screenshot
agent-browser screenshot --full             # Full page
agent-browser screenshot --annotate         # Annotated with element labels
agent-browser pdf output.pdf               # Save as PDF

# Downloads
agent-browser download @e1 ./file.pdf      # Download via element click
agent-browser wait --download ./output.zip # Wait for download completion

# JavaScript
agent-browser eval 'document.title'        # Simple JS eval
agent-browser eval --stdin <<'EOF'          # Complex JS (recommended)
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a=>a.href))
EOF
```

## Device & Viewport

```bash
agent-browser set viewport 375 812         # Mobile size
agent-browser set device "iPhone 14"       # Device emulation
agent-browser --headed open <url>          # Visible mode (debug)
```

## Security (AI agent context)

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1  # Mark page content boundaries
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
export AGENT_BROWSER_MAX_OUTPUT=50000      # Limit large page output
```
