---
name: clawd-cursor
version: 0.5.1
description: >
  AI desktop agent with smart 4-layer pipeline. Controls Windows and macOS natively via screen + accessibility APIs.
  Works with any AI provider (Anthropic, OpenAI, Ollama, Kimi) or completely free with local models.
  Auto-configures via 'clawd-cursor doctor'. Smart Interaction Layer handles browser tasks with 95% fewer tokens.
  Cross-platform: Windows (PowerShell/.NET) + macOS (JXA/AppleScript).
privacy: >
  All screenshots and data stay local on the user's machine. AI calls go only to the user's own configured
  API provider and key — no data is sent to third-party servers or skill authors. With Ollama, everything
  runs 100% locally with zero external network calls.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    install:
      - git clone https://github.com/AmrDab/clawd-cursor.git
      - cd clawd-cursor && npm install && npm run build
      - cd clawd-cursor && npx clawd-cursor doctor
    privacy:
      - Screenshots processed by user's own configured AI provider only
      - With Ollama, fully offline — no external API calls
credentials:
  - name: AI_API_KEY
    sensitivity: high
    description: API key for AI provider (Anthropic, OpenAI, or Kimi). Not needed if using Ollama locally.
    required: false
---

# Clawd Cursor

**One skill, every app.** Instead of integrating dozens of APIs, give your agent a screen. Gmail, Slack, Jira, Figma — if you can click it, your agent can too.

## What's New in v0.5.1

- **Smart Interaction Layer** — Browser tasks use 1 LLM call instead of 18 (95% token savings)
- **CDP Driver** — Chrome DevTools Protocol for fast, free browser DOM interaction
- **UI Driver** — Native UI Automation for Windows (.NET) and macOS (JXA)
- **macOS Support** — Full cross-platform: JXA scripts for accessibility, AppleScript for UI control
- **Doctor Version Check** — Tells you when updates are available
- **Self-healing pipeline** — Falls through layers automatically on failure

## Quick Start

```bash
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor
npm install && npm run build
npx clawd-cursor doctor    # auto-detects and configures everything
npm start
```

That's it. The doctor handles provider detection, model testing, and pipeline configuration.

### macOS Users
Grant **Accessibility permission** to your terminal app:
**System Settings → Privacy & Security → Accessibility → add Terminal/iTerm**

See `docs/MACOS-SETUP.md` for full setup guide.

## How It Works — 4-Layer Pipeline

Every task flows through layers. Most tasks are handled by Layer 1 (free, instant). Only complex tasks reach Layer 3.

| Layer | What | Speed | Cost |
|-------|------|-------|------|
| **0: Browser Layer** | URL detection → direct navigation | Instant | Free |
| **1: Action Router** | Regex + UI Automation. Opens apps, types, clicks by name | Instant | Free |
| **1.5: Smart Interaction** | 1 LLM plan → CDP/UIDriver executes steps free | ~2-5s | 1 LLM call |
| **2: Accessibility Reasoner** | Reads UI tree → cheap text LLM decides action | ~1s | Free (Qwen) or $0.25/M (Haiku) |
| **3: Computer Use** | Full screenshot → vision LLM or Anthropic Computer Use | ~5-8s | ~$3/M (Sonnet) |

**Example:** Sending a Gmail email — Layer 1.5 does it in **1 LLM call, 21 seconds**. Computer Use would take 18 LLM calls, 162 seconds.

## Provider Support

| Provider | Setup | Layer 2 | Layer 3 | Computer Use |
|----------|-------|---------|---------|-------------|
| **Ollama** | `ollama pull qwen2.5:7b` | Qwen (free) | Limited | ❌ |
| **Anthropic** | `AI_API_KEY=sk-ant-...` | Haiku or Qwen | Sonnet | ✅ |
| **OpenAI** | `AI_API_KEY=sk-...` | GPT-4o-mini | GPT-4o | ❌ |
| **Kimi** | `AI_API_KEY=sk-...` | Moonshot-8k | Moonshot-8k | ❌ |

## Platform Support

| Platform | UI Automation | Accessibility | Browser (CDP) |
|----------|--------------|---------------|---------------|
| **Windows** | PowerShell/.NET UIAutomation | ✅ Full | ✅ Edge/Chrome |
| **macOS** | JXA/AppleScript + System Events | ✅ Full | ✅ Chrome |
| **Linux** | Not yet | Not yet | ✅ Chrome |

## OpenClaw Agent Instructions

When an OpenClaw agent dispatches Clawd Cursor tasks:

### Simple Tasks
```
POST http://localhost:3847/task
{"task": "Open Notepad and type hello world"}
```

### Complex Tasks (two-agent pattern)
For heavy workloads, spawn two sub-agents:
1. **Setup agent** — runs `doctor`, starts server, validates connectivity
2. **Task agent** — sends tasks via REST API, monitors status, reports results

## Doctor (Self-Healing)

```bash
npx clawd-cursor doctor
```

The doctor:
1. Checks for updates against GitHub releases
2. Tests screen capture and accessibility bridge
3. Detects available AI providers and tests models
4. Builds the optimal pipeline config
5. Falls back gracefully if models are unavailable
6. Saves config to `.clawd-config.json`

## API Endpoints

`http://localhost:3847`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/task` | POST | `{"task": "Open Chrome"}` |
| `/status` | GET | Agent state |
| `/confirm` | POST | `{"approved": true}` |
| `/abort` | POST | Stop current task |

## Safety

| Tier | Actions | Behavior |
|------|---------|----------|
| 🟢 Auto | Navigation, reading, opening apps | Runs immediately |
| 🟡 Preview | Typing, form filling | Logs before executing |
| 🔴 Confirm | Sending messages, deleting | Pauses for approval |

## Security

- Screenshots are NOT saved to disk by default (memory only, sent to user's own AI provider)
- API binds to 127.0.0.1 only — not network accessible
- Use `--debug` to opt-in to disk screenshot saves
- Run in a sandbox/VM when testing with sensitive screen content
- With Ollama, everything runs 100% locally — no external API calls
