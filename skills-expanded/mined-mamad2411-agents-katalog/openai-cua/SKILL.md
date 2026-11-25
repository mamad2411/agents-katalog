---
name: openai-cua
description: Full computer use via OpenAI CUA (Computer Use Agent) with GPT-4o vision. Use for advanced screen-level computer control — seeing the screen, clicking, typing, and completing multi-step UI tasks. Combines OpenAI's Responses API with Playwright for browser sessions. More powerful than AppleScript for complex GUI workflows.
allowed-tools: Bash
---

# OpenAI CUA — Computer Use Agent

Use OpenAI's CUA (Computer Use Agent) for advanced computer control via GPT-4o vision.

## ARCHITECTURE

```
OpenAI Responses API (gpt-4o / computer-use-preview)
    ↓
Playwright Browser Session
    ↓
Real Browser with User's Accounts
```

## QUICK START

```bash
CUA_DIR="$(find ~ -name 'openai-cua-main' -type d 2>/dev/null | head -1)"
cd "$CUA_DIR"

# One-time setup
corepack enable 2>/dev/null || npm install -g corepack
pnpm install
pnpm playwright:install

# Set API key
export OPENAI_API_KEY="${OPENAI_API_KEY:-$(cat ~/.tua-agent-openai-key 2>/dev/null)}"

# Start CUA (opens browser + operator console)
pnpm dev
# Console: http://127.0.0.1:3000
```

## DIRECT PYTHON CUA (no server needed)

```python
python3 << 'PYTHON'
import asyncio, os, base64, subprocess, sys

# Install if needed
try:
    from openai import AsyncOpenAI
    from playwright.async_api import async_playwright
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "--user",
                   "openai", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from openai import AsyncOpenAI
    from playwright.async_api import async_playwright

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def take_screenshot(page) -> str:
    """Take screenshot and return as base64."""
    screenshot = await page.screenshot()
    return base64.b64encode(screenshot).decode()

async def run_cua_task(task: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        # Get initial screenshot
        screenshot_b64 = await take_screenshot(page)

        messages = [{"role": "user", "content": task}]
        computer_tools = [{
            "type": "computer_use_preview",
            "display_width": 1280,
            "display_height": 800,
        }]

        while True:
            response = await client.responses.create(
                model="computer-use-preview",
                input=messages,
                tools=computer_tools,
                truncation="auto",
            )

            # Process tool calls
            actions = [item for item in response.output
                      if item.type == "computer_call"]

            if not actions:
                # Done
                text_output = next((item.text for item in response.output
                                   if hasattr(item, "text")), "Task complete")
                print(f"Result: {text_output}")
                break

            for action in actions:
                call_id = action.call_id
                params = action.action

                # Execute action
                if params.type == "screenshot":
                    screenshot_b64 = await take_screenshot(page)
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": call_id,
                            "content": [{
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": screenshot_b64,
                                }
                            }]
                        }]
                    })

                elif params.type == "left_click":
                    await page.mouse.click(params.coordinate[0], params.coordinate[1])
                    screenshot_b64 = await take_screenshot(page)

                elif params.type == "type":
                    await page.keyboard.type(params.text)

                elif params.type == "key":
                    await page.keyboard.press(params.key)

                elif params.type == "goto":
                    await page.goto(params.url)

                await asyncio.sleep(0.5)

        await browser.close()

asyncio.run(run_cua_task("""TASK_HERE"""))
PYTHON
```

## COMMON CUA TASKS

### Open and fill a Google Form
```python
asyncio.run(run_cua_task(
    "Go to forms.google.com, find form titled 'FORM_NAME', fill all fields with data: DATA, submit"
))
```

### Navigate complex dashboards
```python
asyncio.run(run_cua_task(
    "Open linear.app, create issue titled 'TITLE' in project 'PROJECT', assign to me"
))
```

### Interact with desktop apps
```python
asyncio.run(run_cua_task(
    "Open Figma, find file 'FILENAME', export all frames as PNG to ~/Desktop/exports/"
))
```

## TASK: $ARGUMENTS

Run the CUA to complete: `$ARGUMENTS`

Start with METHOD 1 (browser-use + GPT-4o from native-browser skill) for most tasks.
Fall back to this CUA approach for complex, multi-step screen-level interactions.
