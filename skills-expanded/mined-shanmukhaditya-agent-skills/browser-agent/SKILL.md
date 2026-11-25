---
name: browser-agent
description: Autonomous stealth browser automation agent powered by Playwright with ref-based accessibility targeting, persistent daemon architecture, and human-motor kinematics (Bézier curves, natural typing rhythms). Replaces heavy DOM-streaming tools with token-efficient ref snapshots and full anti-bot protection.
---

# Stealth Browser Agent (`agent-browser`)

`browser-agent` is an autonomous browser driver built for AI agents. It combines high token efficiency with full anti-bot stealth protection (bypassing Cloudflare, DataDome, Akamai) using a persistent background daemon.

---

## ⚡ Core Architecture

1. **Persistent Daemon**: Maintains a long-lived browser session via a Unix domain socket (`/tmp/agent_browser.sock`) to eliminate cold-start startup overhead.
2. **Token-Efficient Ref Snapshots**: After each navigation or interaction, an accessibility snapshot is generated and saved to `/tmp/browser_snapshot.yaml`. Interactive elements are assigned concise ref IDs (`e1`, `e2`, `e3`...).
3. **Human Motor Kinematics**:
   - **Mouse**: Moves along cubic Bézier curves with natural acceleration, deceleration, and micro-overshoots.
   - **Keyboard**: Types with randomized keystroke cadences (50ms–160ms) and word pauses.
   - **Scroll**: Inertial wheel scrolling with reading pauses.
4. **Native Chrome Execution**: Auto-detects and binds to `/Applications/Google Chrome.app` to provide genuine audio/video codecs, TLS JA3/JA4 fingerprints, and WebGL ANGLE hardware contexts.

---

## 🛠️ CLI Commands Overview

All commands are executed via the `agent-browser` binary located at:
`~/.gemini/config/skills/browser-agent/bin/agent-browser`

```bash
# 1. Open a URL (starts daemon automatically)
agent-browser open "https://example.com"
agent-browser open "https://example.com" --headless

# 2. Inspect current interactive elements
agent-browser snapshot

# 3. Click an element using its ref ID
agent-browser click e3

# 4. Fill or type into form fields
agent-browser fill e1 "username@domain.com"
agent-browser type e2 "securePassword123"

# 5. Press special keys
agent-browser press Enter
agent-browser press Tab

# 6. Smooth human scrolling
agent-browser scroll --down 500
agent-browser scroll --up 300

# 7. Capture visual proof
agent-browser screenshot --output "/tmp/screenshot.png"

# 8. Run custom JavaScript evaluation
agent-browser eval "document.title"

# 9. Clean shutdown
agent-browser close
```

---

## 📋 Recommended Agent Workflow

When given a browser browsing, research, or form submission task:

1. **Navigate to the target**:
   ```bash
   agent-browser open "https://target-website.com"
   ```
2. **Inspect the Snapshot**:
   Read `/tmp/browser_snapshot.yaml` (or view the returned JSON) to find the ref IDs for the elements you need.
3. **Interact with Ref IDs**:
   Execute `agent-browser click <ref>`, `agent-browser fill <ref> <text>`, or `agent-browser press Enter`.
4. **Extract Information**:
   Use `agent-browser eval` for direct DOM data or re-run `agent-browser snapshot` after page transitions.
5. **Close when Finished**:
   Run `agent-browser close` to free memory and shut down the daemon.
