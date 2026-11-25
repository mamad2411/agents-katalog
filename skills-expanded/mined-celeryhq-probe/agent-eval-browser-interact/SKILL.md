---
name: agent-eval-browser-interact
description: Use when translating natural language eval instructions into playwright-cli commands during AI agent evaluation — clicking, typing, waiting, scrolling, screenshot capture
---

# Agent Eval — Browser Interact

## Overview

Translates natural language instructions into `playwright-cli` commands. Built on top of the playwright-cli skill — uses snapshots to find element refs, then acts on them.

## Pattern: Snapshot → Identify → Act → Screenshot

For every natural language instruction:

1. `playwright-cli snapshot` — get current page state with element refs
2. Read the snapshot to identify the target element ref (e.g., `e15`)
3. Execute the appropriate `playwright-cli` command
4. `playwright-cli screenshot --filename=<path>` — capture result

## Action Mapping

| Natural Language | playwright-cli Command |
|-----------------|----------------------|
| "Click on X" / "Click the X button" | `playwright-cli click <ref>` |
| "Type 'text' in X" / "Enter 'text' in X" | `playwright-cli fill <ref> "text"` or `playwright-cli type "text"` |
| "Wait for the page to load" | `playwright-cli run-code "async page => await page.waitForLoadState('networkidle')"` |
| "Wait for X to appear" | `playwright-cli snapshot` and check for element, retry |
| "Wait for the agent to respond" | See below |
| "Scroll down" | `playwright-cli run-code "async page => window.scrollBy(0, 500)"` |
| "Press Enter" | `playwright-cli press Enter` |
| "Go to URL" | `playwright-cli goto URL` |

## Finding Element Refs

```bash
# Take snapshot to see all interactive elements
playwright-cli snapshot

# Output shows refs like:
# e1 [textbox "Email"]
# e2 [textbox "Password"]
# e3 [button "Sign In"]
# e4 [link "Forgot password?"]

# Now use the ref that matches the natural language target
# "Click on the Sign In button" → playwright-cli click e3
# "Type 'admin@test.com' in the email field" → playwright-cli fill e1 "admin@test.com"
```

If the target element isn't obvious from the snapshot, use:
```bash
# Get more detail on a specific element
playwright-cli eval "el => el.textContent" e5
# Or take a deeper snapshot
playwright-cli snapshot --depth=6
```

## Waiting for Agent Response

This is the trickiest action. Strategy:

```bash
# 1. Capture current page text length
playwright-cli --raw eval "document.body.innerText.length"

# 2. (send message action happens)

# 3. Poll for new content — use run-code to wait
playwright-cli run-code "async page => {
  const before = await page.locator('body').innerText();
  await page.waitForFunction(
    prevLen => document.body.innerText.length > prevLen,
    before.length,
    { timeout: 30000 }
  );
  await page.waitForTimeout(2000);
}"
```

Also check for loading indicators:
```bash
playwright-cli snapshot
# Look for spinners, "typing..." indicators, loading states
# Wait until they disappear
```

## Screenshot Capture

After every action:
```bash
playwright-cli screenshot --filename=screenshots/step-01-click.png
```

## Error Recovery

If a command fails:
1. Take a screenshot of current state: `playwright-cli screenshot --filename=screenshots/step-N-error.png`
2. Take a snapshot to understand what happened: `playwright-cli snapshot`
3. Log the error and continue to next step
