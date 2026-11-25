---
name: agent-browser
description: "Vercel Labs agent-browser — fast Rust-native browser automation CLI for Hermes. Replaces the slow built-in browser_use engine."
version: 1.0.0
author: AGON (EREVUS Systems)
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [browser, automation, web, agent-browser, vercel]
    related_skills: [hermes-agent]
---

# agent-browser — Fast Browser Automation for Hermes

> Replaces Hermes' slow built-in `browser_use` engine with Vercel Labs' Rust-native agent-browser CLI. 35.6k stars. Blazing fast.

## Setup

agent-browser is already installed globally. Verify:

```bash
agent-browser --version
```

If missing:

```bash
npm install -g agent-browser
agent-browser install
```

## Wrapper Script

A Python wrapper lives at `Bluepill/scripts/agent-browser.py` in the hermes-agon repo.
Run it from any Hermes session:

```python
from hermes_tools import terminal
terminal("python Bluepill/scripts/agent-browser.py open https://example.com")
```

## Quick Commands

| Task | Command |
|------|---------|
| Open URL | `agent-browser open https://...` |
| Get page snapshot | `agent-browser snapshot -i` |
| Click element | `agent-browser click @e2` |
| Fill input | `agent-browser fill @e3 "text"` |
| Type text | `agent-browser type @e4 "hello"` |
| Get element text | `agent-browser get text @e1` |
| Screenshot | `agent-browser screenshot page.png` |
| Close tab | `agent-browser close` |
| Batch commands | `agent-browser batch --json '[{"cmd":"open","url":"..."}]'` |

## Why agent-browser over Hermes built-in

| | Hermes built-in | agent-browser |
|--|----------------|---------------|
| Engine | Python (browser_use) | Rust native |
| Speed | Slow — blocks gateway | Instant |
| Telegram | Causes "typing..." hang | Clean exit |
| Install | Bundled | `npm i -g agent-browser` |
| Submodule | N/A | Added to hermes-agon repo |

## Telegram Bot Note

The built-in Hermes `browser` toolset is **disabled** in gateway mode to prevent the Telegram bot from hanging ("keeps typing without doing anything"). Use agent-browser CLI directly from terminal instead.

To re-enable built-in browser if needed:
```bash
hermes config set agent.disabled_toolsets '[]'
```

## Batch Workflow Example

```json
[
  {"cmd": "open", "url": "https://example.com"},
  {"cmd": "wait", "ms": 2000},
  {"cmd": "snapshot"},
  {"cmd": "click", "ref": "@e2"},
  {"cmd": "screenshot", "path": "result.png"},
  {"cmd": "close"}
]
```

DEUS VULT.
