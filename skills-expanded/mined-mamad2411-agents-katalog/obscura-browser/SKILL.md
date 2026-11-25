---
name: obscura-browser
description: Use Obscura for lightweight headless browsing, web scraping, and CDP automation. Trigger when users mention Obscura, want a lighter Chrome replacement for AI agents, need `obscura fetch` or `obscura scrape` commands, want to run `obscura serve`, need Playwright or Puppeteer to connect to Obscura over Chrome DevTools Protocol, or need a safe local development workflow such as Vite plus hostc plus Obscura because localhost is blocked by Obscura's SSRF protections.
---

# Obscura Browser

## Overview

Use this skill to help users operate the `obscura` CLI and connect client libraries to its CDP server. Prefer short, executable commands first, then add optional flags or sample code only if they help the user's scenario. For local development, default to `Vite + hostc + Obscura` instead of suggesting localhost access.

## Workflow

1. Detect whether `obscura` is available locally before giving run commands.
2. If it is missing, explain the shortest install path for the current OS.
3. If the target is local development, do not suggest patching Obscura or using localhost directly. Default to:
   - local app on Vite or another dev server
   - `hostc` to expose the local port as a public `https://` URL
   - Obscura against the public URL
4. Pick the narrowest Obscura flow that matches the request:
   - `fetch` for one page or one extraction
   - `scrape` for multiple URLs in parallel
   - `serve` for Playwright or Puppeteer CDP connections
5. Return one minimal command or one minimal code sample first.
6. Add only the flags that matter for the user's goal such as `--stealth`, `--timeout`, `--wait-until`, `--output`, `--concurrency`, or `--quiet`.

## Quick Start

Run `scripts/detect_obscura.py` first. It checks:

- whether `obscura` is on `PATH`
- whether `obscura-worker` is present in the same directory
- likely local binary locations on Windows, macOS, and Linux

If the binary is missing:

- Recommend the GitHub Releases archive for the user's platform.
- On Windows, remind the user to keep `obscura.exe` and `obscura-worker.exe` in the same folder for parallel `scrape`.
- If the user wants to build from source, mention `cargo build --release` and `cargo build --release --features stealth`.

## Task Patterns

### Local development with Vite

Treat this as the default answer when users want Obscura to hit `http://localhost:5173` or another local Vite port.

Recommended flow:

1. Keep Vite running locally.
2. Expose the Vite port with `hostc`.
3. Give Obscura the resulting public `https://` URL.

Use `scripts/command_templates.py vite-hostc` to generate the shortest working command set.
Use `scripts/command_templates.py vite-hostc-cdp` when the user wants the hostc flow plus a ready-to-run Playwright or Puppeteer snippet.

Minimal sequence:

```powershell
pnpm dev
npx hostc 5173
obscura fetch https://your-hostc-url --dump html
```

If the user needs browser automation instead of one fetch:

```powershell
obscura serve --port 9222
```

Then provide a Playwright or Puppeteer snippet that navigates to the hostc URL.

Example:

```powershell
python scripts/command_templates.py vite-hostc-cdp playwright --public-url https://your-hostc-url
```

### Local development with listhen

Use this only as a backup option when the user explicitly wants `listhen` or already has it. The important part is the public tunnel URL, not the local listener.

Do not recommend:

- `localhost`
- `127.0.0.1`
- LAN IPs such as `192.168.x.x`
- source patches to disable SSRF protections unless the user explicitly asks for code changes

### Single-page extraction

Use `scripts/command_templates.py fetch` to build a starter command, then adapt it.

Common examples:

```powershell
obscura fetch https://example.com --eval "document.title"
obscura fetch https://example.com --dump links
obscura fetch https://news.ycombinator.com --dump html --wait-until networkidle0
```

Prefer:

- `--eval` for one DOM expression or computed value
- `--dump html|text|links` for built-in output modes
- `--output` when the user wants a file

### Parallel scraping

Use `scripts/command_templates.py scrape` when users provide multiple URLs or ask for concurrency.

Common example:

```powershell
obscura scrape https://example.com https://example.org --concurrency 10 --eval "document.querySelector('h1')?.textContent" --format json
```

Prefer `--quiet` when the output is meant for scripts or piping.

### CDP server for Playwright or Puppeteer

Use `scripts/command_templates.py serve` to build the launch command and `scripts/command_templates.py cdp` for sample client code.

Typical serve command:

```powershell
obscura serve --port 9222
```

Add:

- `--stealth` when anti-detection matters
- `--proxy <url>` when a proxy is required
- `--workers <n>` when parallel CDP worker processes are useful

Then provide the matching client snippet:

- Playwright uses `chromium.connectOverCDP({ endpointURL: 'ws://127.0.0.1:9222' })`
- Puppeteer uses `puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:9222/devtools/browser' })`

## Response Style

Keep responses practical:

- Start with environment status if it is unknown.
- Give the exact command to run next.
- If code is needed, provide one minimal working snippet.
- Mention assumptions when choosing flags.

## References

Read these only when needed:

- `references/cli-cheatsheet.md` for command patterns and flag selection
- `references/cdp-integration.md` for Playwright and Puppeteer connection details
- `references/local-dev-tunnels.md` for `Vite + hostc + Obscura` and `listhen` fallback guidance

## Scripts

- `scripts/detect_obscura.py`
  Use to find installed binaries and validate worker co-location.
- `scripts/command_templates.py`
  Use to generate starter commands and code snippets for `fetch`, `scrape`, `serve`, CDP clients, and the default `Vite + hostc + Obscura` flow.
