---
name: desktop-browser-routing
description: Three-tier routing runbook for macOS desktop apps and browsers (Native CLI/API -> Built-in Browser & agent-desktop -> Computer Use / LCU), including Chrome dedicated-window locking, PreToolUse guard rules, and permission troubleshooting. Read before automating desktop UIs or logged-in browsers.
---

# Desktop & Browser Three-Tier Routing Runbook

## 1. Quick Decision Matrix

| Target Scenario | Primary Tool | Escalation Signal |
| :--- | :--- | :--- |
| App files, drafts, notes, cloud workspaces | **Tier 1: Native CLI / API / File Edit** | Escalate only for UI-only steps (e.g., final export dialog, live plugin UAT) |
| Web pages in hosts with Chrome cookie sync (**Codex** / **Claude Code**), or public web pages in **Antigravity** | **Tier 2A: Built-in Agent Browser** | Escalate to real Chrome (`agent-desktop`) only if pure CLI mode has no built-in browser or an interactive fallback is needed |
| Logged-in web workflows where host browser is isolated (**Antigravity**, or pure CLI sessions) | **Tier 2B: `agent-desktop` (dedicated Chrome `--window-id`)** | Single snapshot caps around ~2,500 nodes; no arbitrary JS execution |
| Accessible native / Electron apps (Obsidian, Finder, menu bars) | **Tier 2B: `agent-desktop` (headless default)** | Escalate if tree is empty or headless click returns success without UI change |
| Custom-drawn UIs (video editors, AE dialogs, iPhone Mirroring, visual QA) | **Tier 3: Computer Use (`LCU` MCP `js` / native CUA)** | Slower & higher token cost, per-app Touch ID approval |
| Apps in `~/.config/agent-desktop-router/blocked-apps.json` + Notification Center | **Strictly Blocked** | Enforced by `PreToolUse` hook + CLI wrapper + window/coordinate probe |

## 2. `agent-desktop` Usage & Safety Guard Contract

### Check Accessibility Readiness
```bash
agent-desktop status
```
If `accessibility.state` is `"denied"`, ask the user to grant Accessibility access to the host application (e.g., Claude, Antigravity, ChatGPT/Codex, or Terminal) in **System Settings → Privacy & Security → Accessibility**.

### Guard Rules (Mandatory)
1. **Direct CLI calls only**: Run `agent-desktop` directly in the shell tool. Never wrap it inside `.sh`/`.py` scripts, `python3 -c`, heredocs, `xargs`, or `agent-desktop batch`.
2. **Literal targets**: Always write literal values for `--app`, `--window-id`, `@snapshot:eN` refs, and `--xy` coordinates (never `$VARS` or `$(...)` substitutions).
3. **Explicit scope**: Always pass `--app "<App>"`, `--window-id w-<num>`, or a `@snapshot:eN` ref on `snapshot`, `find`, `screenshot`, `press`, and `wait`. Unscoped commands that target the frontmost app are blocked.
4. **Headless first**: Omit `--headed` by default so the user's cursor and focus are untouched. Use `--headed` or `mouse-click` only after a headless click fails to change the UI — notify the user first and verify the target window is frontmost.

### Dedicated Chrome Window Workflow (`Default` Profile)
```bash
# 1. Open a clean 1-tab window in Chrome's primary profile (no restart, avoids scanning huge personal windows or blank MCP profiles)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --profile-directory="Default" --new-window "https://example.com"

# 2. List Chrome windows and grab the new dedicated window ID (w-<number>)
agent-desktop list-windows --app "Google Chrome"

# 3. Read interactive elements from that locked window in the background
agent-desktop snapshot --window-id w-1234 -i --compact

# 4. Act on a qualified ref and re-snapshot to verify
agent-desktop click @s8f3k2p9:e5
agent-desktop snapshot --window-id w-1234 -i --compact
```

## 3. Computer Use (`LCU` MCP) Notes

- Shares the local `ChatGPT.app` Computer Use engine across Claude Code, Antigravity, Codex CLI, and Pi via `amontlabs/lcu`.
- If a target app is not yet approved and the host cannot display an interactive approval card, run `lcu apps allow "<App>"` with a timeout of at least 300 seconds so the user can approve via Touch ID, and offer `lcu apps revoke "<App>"` when done.
- Run `python3 ~/.local/share/agent-desktop-router/scripts/doctor.py` to diagnose permissions, `probe` binary health, or `ChatGPT.app` bundle signature issues.
