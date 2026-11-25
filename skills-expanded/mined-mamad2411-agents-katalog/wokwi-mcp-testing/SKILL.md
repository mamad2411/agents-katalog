---
name: wokwi-mcp-testing
description: Use when testing or debugging ESP32/Arduino firmware in Wokwi via the Wokwi MCP server — starting simulation, reading serial or pin state, verifying boot, or when the sim won't start, the MCP tool errors, or the host can't reach the simulated device's web server.
---

# Wokwi MCP Testing

## Overview

Test ESP32 firmware in the Wokwi simulator through MCP tools. Verify boot and hardware state via serial logs and pin reads. The host cannot reach the sim's virtual network — there is no HTTP bridge.

## When to Use

- Verify firmware boots (serial log shows WiFi IP, "HTTP server started")
- Check failsafe / initial pin state (pin read at boot)
- Debug "sim won't start" or Wokwi MCP tool errors
- Answer "does the web UI work on the sim?" — see mock-server technique below

## Gotchas (learned the hard way)

### 1. Token: `user.tok` is a LICENSE, not a CI token
- `~/.wokwi/user.tok` → sim start fails: `Invalid character in header content [Authorization]`
- Real token comes from https://wokwi.com/dashboard/ci (read at runtime via env var, or in `.mcp.json` command line)
- `.mcp.json` now embeds the real token → **gitignore it** (otherwise the secret gets committed)
- Never print token contents to output or write them into repo files

### 2. Editing `.mcp.json` mid-session kills the MCP connection
- After the file changes, Wokwi tools return `No such tool available`
- Fix: restart the Claude Code session — MCP reloads `.mcp.json` cleanly
- Do not restart the wokwi-cli service yourself; report the need instead

### 3. No HTTP bridge — host cannot reach the sim's web server
- Sim device gets an IP like `10.13.37.2` on Wokwi's virtual network (e.g. `Wokwi-GUEST`)
- `curl http://10.13.37.2/` from the host → always UNREACHABLE
- The Wokwi MCP has no fetch/HTTP tool — you cannot drive `/on` `/off` `/toggle` from the host
- Verify web logic another way: serial logs, pin reads, or a mock server (below)

### 4. Screenshot with partId returns a tiny placeholder
- `wokwi_take_screenshot` of a part returns ~16x16 px, useless for visual state
- Don't rely on it to show an LED on/off

## Verification Workflow

1. Start sim → `wokwi_start_simulation` (returns "started")
2. Wait ~4s → `wokwi_read_serial` — expect `WiFi connected, IP: 10.13.37.2` and `HTTP server started`
3. Failsafe check → `wokwi_read_pin` on the LED pin — expect `false` (off at boot)
4. To prove the web UI logic → replicate `htmlPage()` + routes in a Python mock server, drive it with BrowserClaw (same HTML + routes as firmware = logic verified)
5. For a live LED toggle the user can see → VS Code Wokwi extension: start sim, open browser to the sim IP, click the buttons

## Common Mistakes

| Mistake | Fix |
|---|---|
| Used `~/.wokwi/user.tok` as token | Get a CI token from https://wokwi.com/dashboard/ci |
| Edited `.mcp.json` then wondered why tools died | Restart the Claude Code session |
| Tried to `curl` the sim IP from host | Not possible — use serial/pin reads or the mock server |
| Committed `.mcp.json` containing the token | Add `.mcp.json` to `.gitignore` |
