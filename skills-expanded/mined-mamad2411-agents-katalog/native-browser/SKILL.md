---
name: native-browser
description: Control the browser to automate any web task — fill forms, navigate, scrape, interact with web apps the user is already logged into. Priority stack: 1) browser-use with GPT-4o, 2) computer-use (AppleScript/PyAutoGUI), 3) Chrome extension (BrowserMCP) only as last resort. Never ask the user to do anything manually.
allowed-tools: Bash
---

# Native Browser — Hardened Priority Stack

## ⚡ PRIORITY ORDER (ALWAYS follow this sequence)

```
1. browser-use (OpenAI GPT-4o) ──── PRIMARY: AI-powered, autonomous, best for complex tasks
2. computer-use (AppleScript)  ──── SECONDARY: direct screen control, no Python needed
3. BrowserMCP Chrome extension ──── TERTIARY: only if methods 1+2 fail
```

---

## METHOD 1 — browser-use + GPT-4o (PRIMARY)

**Use for**: Multi-step web tasks, form filling, authenticated actions (Google Docs, Gmail, etc.)

```python
python3 << 'PYTHON'
import asyncio, os, sys

# Install if needed
try:
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_openai import ChatOpenAI
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--user",
                   "browser-use", "langchain-openai", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_openai import ChatOpenAI

async def run(task: str):
    llm = ChatOpenAI(
        model="gpt-4o",              # OpenAI primary
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0
    )
    browser = Browser(config=BrowserConfig(
        headless=False,              # Show browser so user can see
        # Reuse existing Chrome profile (stays logged in)
        chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    await browser.close()
    return result

result = asyncio.run(run("""TASK_HERE"""))
print(result)
PYTHON
```

**Common tasks:**
```python
# Google Docs — create document
asyncio.run(run("Go to docs.google.com/document/create, create doc titled 'TITLE', add content: CONTENT"))

# Gmail — send email
asyncio.run(run("Open gmail.com, click Compose, To: EMAIL, Subject: SUBJ, Body: BODY, click Send"))

# Google Sheets
asyncio.run(run("Go to sheets.google.com/create, create sheet titled 'TITLE', fill data: DATA"))

# Any web research
asyncio.run(run("Search Google for QUERY, read top 3 results, summarize findings"))

# LinkedIn post
asyncio.run(run("Go to linkedin.com, click Start a post, type: CONTENT, return draft for approval"))
```

---

## METHOD 2 — computer-use via AppleScript (SECONDARY)

**Use for**: Simple navigation, when Python is unavailable, quick single-step actions

```bash
# Navigate Chrome to URL
osascript -e 'tell application "Google Chrome"
    activate
    open location "URL_HERE"
end tell'

# Click element using coordinates (take screenshot first)
screencapture -x /tmp/tua-screen.png
# Read /tmp/tua-screen.png to find element location
osascript -e 'tell application "System Events" to click at {X, Y}'

# Type text
osascript -e 'tell application "System Events" to keystroke "TEXT_HERE"'

# JavaScript execution in Chrome tab
osascript -e 'tell application "Google Chrome"
    execute front window active tab javascript "
        document.querySelector(\"SELECTOR\").click();
    "
end tell'

# Fill form field via JS
osascript -e 'tell application "Google Chrome"
    execute front window active tab javascript "
        document.querySelector(\"input[name=NAME]\").value = \"VALUE\";
        document.querySelector(\"form\").submit();
    "
end tell'
```

---

## METHOD 3 — BrowserMCP (TERTIARY — only if 1+2 fail)

BrowserMCP uses the Chrome extension to control the user's real browser.
This requires:
- Chrome extension installed (see setup.sh)
- MCP server running

```bash
# Start BrowserMCP server
cd "$(find ~ -name 'browsermcp-main' -type d 2>/dev/null | head -1)"
node dist/index.js &
```

---

## OPENAI CUA (Advanced — for complex computer use)

For screen-level computer use using OpenAI's CUA:

```bash
cd "$(find ~ -name 'openai-cua-main' -type d 2>/dev/null | head -1)"
# Install
corepack enable && pnpm install && pnpm playwright:install
# Start
OPENAI_API_KEY=$OPENAI_API_KEY pnpm dev
# Open: http://127.0.0.1:3000
```

---

## TASK: $ARGUMENTS

**Execute in priority order:**

1. Try **METHOD 1** (browser-use + GPT-4o) first
2. If Python/browser-use unavailable → **METHOD 2** (AppleScript)
3. Only if both fail → **METHOD 3** (BrowserMCP)

Never ask the user to manually navigate, click, or type anything.
