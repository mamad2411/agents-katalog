---
name: chatgpt-web-relay
description: Hermes skill to relay prompts to ChatGPT web UI via Playwright browser
  automation. Uses persistent Chrome profile to maintain login state. Enables Hermes
  to use ChatGPT web features (GPT-5.5 Pro Extended, Deep Research, image gen, file
  upload) without API quota consumption.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- playwright
- browser
- automation
- chatgpt
- relay
- web-ui
related_skills:
- browser-automation-security
- web-app-pentest
---

# ChatGPT Web Relay for Hermes

This skill provides a Playwright-based browser automation that connects Hermes to the **ChatGPT web interface** (chatgpt.com) using your existing logged-in Chrome session. It replicates the functionality of the "GPT Relay" Codex plugin but for Hermes Agent.

## Why Use This?

- **No API quota consumption** — uses your ChatGPT Plus/Pro/Team subscription via web UI
- **Access to web-only features** — GPT-5.5 Pro Extended, Deep Research, native image generation, file upload/analysis
- **Persistent login** — reuses a Chrome user data directory, stays logged in across sessions
- **Full Hermes integration** — call as a tool from any Hermes task

## Installation

```bash
# Install Playwright and Chromium (if not already done)
pip3 install playwright playwright-stealth
python3 -m playwright install chromium

# Verify
python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## Configuration

Create a config file at `~/.hermes/chatgpt_web_relay.yaml`:

```yaml
# Chrome user data directory (persistent profile)
# Use a dedicated directory, NOT your main Chrome profile
user_data_dir: "~/.hermes/browser_profiles/chatgpt_relay"

# Chrome executable (optional, auto-detected)
# channel: "chrome"  # Use real Chrome instead of bundled Chromium (bypasses Turnstile)

# Default model/mode settings
default_model: "gpt-5.5-pro-extended"  # or "gpt-5.4-thinking-light", "deep-research", "gpt-4o", etc.
default_effort: "high"  # for thinking models: "low", "medium", "high"

# Timeouts (ms)
navigation_timeout: 60000
response_timeout: 300000  # 5 min for Deep Research

# Headless mode (false = headed, more reliable for Cloudflare/Turnstile)
headless: false

# Stealth settings
stealth: true
disable_blink_features: true
```

## Usage from Hermes

### As a Python function (in execute_code or skill scripts)

```python
from chatgpt_web_relay import ChatGPTWebRelay

relay = ChatGPTWebRelay(config_path="~/.hermes/chatgpt_web_relay.yaml")

# Simple prompt with default model
result = relay.ask("分析這個 Python 代碼的性能瓶頸", model="gpt-5.5-pro-extended")

# Deep Research
result = relay.deep_research("研究 2024 年台灣半導體產業趨勢")

# With image upload
result = relay.ask_with_image("分析這張圖表", image_path="/path/to/chart.png")

# With file upload
result = relay.ask_with_file("總結這份報告", file_path="/path/to/report.pdf")

# Switch model mid-session
relay.switch_model("gpt-5.4-thinking-light", effort="high")
result = relay.ask("用深度思考模式解決這個數學問題")

print(result["text"])
print(result["images"])  # generated image URLs/paths
print(result["conversation_url"])  # link to chatgpt.com conversation
```

### As a Hermes tool (via delegate_task or skill)

```python
# In a Hermes skill or delegate_task context
from hermes_tools import terminal

# Quick one-off via terminal
script = '''
from chatgpt_web_relay import ChatGPTWebRelay
relay = ChatGPTWebRelay()
result = relay.ask("用 GPT-5.5 Pro Extended 分析: {{prompt}}")
import json; print(json.dumps(result, ensure_ascii=False))
'''
# ... execute via terminal
```

## Core Functions

| Function | Description |
|----------|-------------|
| `ask(prompt, model, effort)` | Send prompt, wait for response |
| `deep_research(topic, model="deep-research")` | Start Deep Research, wait for completion |
| `ask_with_image(prompt, image_path, model)` | Upload image + prompt |
| `ask_with_file(prompt, file_path, model)` | Upload file (PDF, code, etc.) + prompt |
| `switch_model(model, effort)` | Change model/mode in current conversation |
| `new_chat()` | Start fresh conversation |
| `get_conversation_url()` | Get current chatgpt.com conversation link |
| `close()` | Clean up browser |

## Supported Models/Modes (web UI names)

| Model ID | Web UI Label |
|----------|--------------|
| `gpt-5.5-pro-extended` | GPT-5.5 Pro Extended |
| `gpt-5.4-thinking-light` | GPT-5.4 Thinking Light |
| `deep-research` | Deep Research |
| `gpt-4o` | GPT-4o |
| `gpt-4o-mini` | GPT-4o mini |
| `o1-pro` | o1 Pro |
| `o1` | o1 |

## Architecture

```
Hermes (Python) 
    │
    ▼
ChatGPTWebRelay class (this skill)
    │
    ▼
Playwright → Chrome (persistent profile, user_data_dir)
    │
    ▼
chatgpt.com (logged-in session)
    │
    ├── Send prompt → wait for response streaming to complete
    ├── Handle model switcher UI
    ├── Handle file/upload dialogs
    ├── Handle Deep Research progress polling
    └── Extract: text, images, conversation URL
    │
    ▼
Return structured dict to Hermes
```

## Selectors & UI Automation (ChatGPT Web UI as of 2026)

The skill uses robust selectors with fallbacks:

- **Prompt textarea**: `textarea#prompt-textarea`, `textarea[data-id="root"]`, `div.ProseMirror[contenteditable="true"]`
- **Send button**: `button[data-testid="send-button"]`, `button:has-text("Send")`
- **Model switcher**: `button[data-testid="model-switcher"]`, `button:has-text("GPT")`
- **Model options**: `div[role="option"]:has-text("{{model_name}}")`
- **Response container**: `div[data-message-author-role="assistant"]`, `.markdown.prose`
- **Image results**: `img[data-testid="image-generation-result"]`, `a[href*="files.oaiusercontent.com"]`
- **Deep Research progress**: `div:has-text("Researching")`, `div:has-text("Analyzing")`
- **File upload**: `input[type="file"]`, button with `data-testid="attach-files"`

## Pitfalls & Solutions

| Issue | Solution |
|-------|----------|
| Cloudflare Turnstile blocks headless | Use `channel="chrome"` (real Chrome) + `headless=false` |
| Session expires | Persistent `user_data_dir` keeps cookies/localStorage |
| Response not fully streamed | Wait for "Stop generating" button to disappear + network idle |
| Model switcher UI changed | Multiple selector fallbacks + text-based matching |
| File upload dialog | Use `page.set_input_files()` on hidden file input |
| Deep Research takes long | Configurable timeout (default 5 min), poll for completion |
| Multiple conversations | `new_chat()` creates fresh conversation via sidebar "New chat" |

## Example: Full Hermes Integration

```python
# In a Hermes skill or cron job
from chatgpt_web_relay import ChatGPTWebRelay

def hermess_chatgpt_relay(prompt: str, task_type: str = "analysis") -> dict:
    """Hermes-callable wrapper."""
    relay = ChatGPTWebRelay()
    
    try:
        if task_type == "deep_research":
            result = relay.deep_research(prompt)
        elif task_type == "image_analysis":
            # expects prompt to contain image path or be passed separately
            result = relay.ask_with_image(prompt, image_path=...)
        else:
            # Default: use strongest model
            result = relay.ask(prompt, model="gpt-5.5-pro-extended", effort="high")
        
        return {
            "success": True,
            "response": result["text"],
            "images": result.get("images", []),
            "conversation_url": result.get("conversation_url"),
            "model_used": result.get("model_used"),
        }
    finally:
        relay.close()
```

## Security Notes

- **Never use your main Chrome profile** — create a dedicated `user_data_dir`
- **No credentials stored** — relies on existing browser login state
- **Runs locally** — no data leaves your machine except to chatgpt.com
- **Rate limits** — respect ChatGPT web UI limits (not API limits)

## Files in This Skill

```
chatgpt-web-relay/
├── SKILL.md           # This file
├── chatgpt_web_relay.py   # Main Python module
├── config.yaml.example    # Example configuration
└── scripts/
    └── hermess_wrapper.py # Hermes integration helper
```