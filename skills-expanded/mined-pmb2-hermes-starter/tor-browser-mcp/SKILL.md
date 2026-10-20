---
name: tor-browser-mcp
version: 2.0.0
author: Hermes Agent
license: MIT
description: Hardened Tor Browser MCP server — drive stock Tor Browser via MCP tools for anonymous browsing, OSINT, and tor control with anti-forensics and security tooling
metadata:
  hermes:
    tags: [tor, onion, mcp-server, osint, anonymity, anti-forensics]
    triggers:
      - tor browser
      - tor mcp
      - anonymous browsing
      - tor control
      - geckodriver tor
      - marionette tor
      - tor osint
      - anti-forensics browser
    related_skills: [tor-circuit-rotation, firefox-stealth-ops, osint-recon, osint-threat]
---

## Overview

Fork of `torbrowser-mcp` (Boti-Ormandi) with hardened profile, security audit tools, and anti-forensics. Drives stock Tor Browser via geckodriver + Marionette, preserving anonymity properties (RFP, letterboxing, FPI, per-origin circuit isolation). Exposes 74 MCP tools.

## Changes from Upstream (pmb2 fork)

- **Hardened automation profile**: `dom.webdriver.enabled=false`, WebRTC/geo/telemetry disabled, sanitize-on-shutdown, resist-fingerprinting overrides
- **3 new tor security tools**: `tor_dns_leak_test`, `tor_exit_node_info`, `tor_circuit_health`
- **Anti-forensics**: Session directory files are overwritten with random data before deletion on shutdown
- **77 bool prefs** hardened against IP leaks, fingerprinting, and automation detection

## Installation & Setup

### Prerequisites
- Python 3.11+
- Tor Browser bundle extracted (TB 15.0.x)
- Geckodriver binary v0.36.0

### Install (from fork)
```bash
cd ${MY_REPOS}/Documents/github/tor-browser-mcp
pip install -e .
```

### Configuration (AppData\Local\hermes\config.yaml)
```yaml
mcp_servers:
  tor-browser-mcp:
    command: ${USER_HOME}/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
    args:
    - -m
    - torbrowser_mcp
    - --tbb-root
    - ${USER_HOME}/TorBrowser
    - --output-dir
    - ${USER_HOME}/tor-browser-outputs
    - --geckodriver-path
    - ${USER_HOME}/tor-browser-mcp/bin/geckodriver.exe
    - --headless
    timeout: 300
    workdir: ${MY_REPOS}/Documents/github/tor-browser-mcp
```

## Key Tools (74 total)

### Core Browser
- `browser_navigate(url)` — Navigate to URL
- `browser_click(target)` — Click element by selector
- `browser_type(target, text)` — Type into element
- `browser_scroll(delta_x, delta_y)` — Scroll page
- `browser_snapshot()` — Get accessibility tree (JS-based)
- `browser_take_screenshot()` — PNG screenshot to output dir
- `browser_evaluate(script)` — Run JS in page
- `browser_tabs(action, ...)` — Manage tabs
- `browser_frames()` / `browser_frame_select()` / `browser_frame_parent()` / `browser_frame_default()` — Frame management
- `browser_wait_for(text)` — Wait for text on page
- `browser_fill_form(fields)` — Fill multiple form fields
- `browser_press_key(key)` — Keyboard shortcut
- `browser_hover(target)` — Mouse hover
- `browser_drag(start, end)` — Drag and drop
- `browser_file_upload(target, paths)` — File input
- `browser_handle_dialog(action)` — JS dialog handler
- `browser_dump_page()` — Debug artifacts snapshot

### Tor Control (10 tools)
- `tor_status()` — Bootstrap, version, circuit state, SOCKS ports
- `tor_check_identity(timeout)` — Navigate check.torproject.org, returns is_tor/exit_ip
- `tor_new_identity(wait)` — NEWNYM with configurable post-signal sleep
- `tor_circuit_status(verbose, limit)` — Active circuits with relay paths
- `tor_stream_status(limit)` — Active streams with circuit bindings
- `tor_entry_guards(limit)` — Entry guard fingerprints/nicknames
- `tor_get_info(keys)` — Allowlisted read-only tor control values
- `tor_dns_leak_test(timeout)` — Browse dnsleaktest.com, report DNS servers observed
- `tor_exit_node_info()` — Current circuit exit node (nickname, fingerprint, IP, hops)
- `tor_circuit_health()` — Tor health metrics (uptime, traffic, guards, bootstrap %)

### State Management
- `browser_cookie_*` — Get/set/delete/list/clear cookies
- `browser_localstorage_*` — localStorage management
- `browser_sessionstorage_*` — sessionStorage management
- `browser_storage_state(filename)` — Collect all storage state
- `browser_set_storage_state(filename)` — Restore state from file

### DOM Extraction
- `browser_extract_links()` — All `<a href>` entries
- `browser_extract_forms()` — All `<form>` entries with action/method/fields
- `browser_extract_inputs()` — Input/textarea/select entries
- `browser_extract_tables()` — Table summaries with headers and cell data
- `browser_extract_metadata()` — Meta tags, title, language, charset, canonical
- `browser_find_text(pattern)` — Search body text
- `browser_find_selector(selector)` — CSS selector match count
- `browser_extract_scripts()` — Script elements

### Output & File Management
- `browser_output_list()` / `browser_output_read(filename)` / `browser_output_delete(filename)`
- `browser_downloads_list()` / `browser_download_save(filename)`
- `browser_page_source(filename)` — Current page source

### Network & Diagnostics
- `browser_network_requests()` / `browser_network_request(index)` — Performance API
- `browser_console_messages()` — Browser log
- `browser_get_config()` — DriverConfig snapshot
- `browser_fingerprint_probe()` — Fingerprint signal snapshot

## Capabilities (--caps flag)
Default: core, state, extract, diagnostics, tor, network-observe (24 tools)
Opt-in: vision (mouse/keyboard coords), pdf, highlight, tor-routing (exit pinning), http-over-tor, helper-extension (network capture/routing), proxy-intercept (mitmproxy decryption), unsafe (RCE escape hatches)

Run with `--caps vision,pdf,helper-extension` to add selective capabilities.

## Anti-Forensics
- Session directories are overwritten with random data (1 pass default) before deletion
- Proxy-intercept flow buffer is cleared on `browser_intercept_stop`
- Tor data directory is ephemeral (temp dir) by default
- All privacy prefs enable sanitize-on-shutdown (cache, cookies, history, sessions, site settings)

## Hardened Profile Additions
| Pref | Value | Purpose |
|------|-------|---------|
| `dom.webdriver.enabled` | false | Suppress navigator.webdriver flag |
| `useAutomationExtension` | false | Remove automation extension indicator |
| `media.peerconnection.enabled` | false | Disable WebRTC (IP leak) |
| `geo.enabled` | false | Disable geolocation |
| `toolkit.telemetry.enabled` | false | Disable telemetry |
| `privacy.sanitize.sanitizeOnShutdown` | true | Auto-clean on close |
| `privacy.resistFingerprinting` | true | Resist canvas/font/screen fingerprinting |
| `signon.rememberSignons` | false | Disable password manager |
| `network.http.speculative-parallel-limit` | 0 | Disable speculative connections |

## Companion: Tor-Camoufox Bridge

When sites block Marionette/geckodriver, use the **tor-camoufox-bridge** MCP server as a unified fallback:

- Routes through Tor Browser by default, falls back to Camoufox anti-detection browser
- 35+ full Camoufox REST API endpoints exposed as MCP tools
- Manual engine switching via `bridge_switch`
- Circuit rotation every 6h via cron

Bridge server: `~/.hermes/scripts/tor_camoufox_bridge.py`
Camoufox engine: `${MY_REPOS}/Documents/github/camofox-browser/` (port 9377)
See the `tor-camoufox-bridge` skill for full tool reference.

## Known Issues
- First startup takes 20-60s (tor bootstrap + browser launch)
- `tor_dns_leak_test` requires a functioning exit node (navigates to dnsleaktest.com)
- Orphan tor processes may block ports; use different `--socks-port`/`--control-port` or `taskkill /F /PID <pid>`
- `proxy-intercept` requires Python 3.12+ and disables per-origin circuit isolation
- npm-installed geckodriver is a shell script shim — use the real binary from GitHub releases

## Paths on This Machine
- Fork: `${MY_REPOS}/Documents/github/tor-browser-mcp` (branch: `pmb2/hardened-tor-mcp`)
- Tor Browser: `${USER_HOME}/TorBrowser`
- Geckodriver: `${USER_HOME}/tor-browser-mcp/bin/geckodriver.exe` (v0.36.0)
- Output directory: `${USER_HOME}/tor-browser-outputs`
- Config: `${USER_HOME}/AppData/Local/hermes/config.yaml`
