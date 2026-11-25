---
name: dokobot-remote-browser
description: Use an SSH-reachable browser host with Dokobot CLI and a real browser session to search and read rendered web pages as Markdown.
version: 1.1.0
triggers:
  - remote browser search
  - dokobot remote browser
  - dokobot ssh
  - rendered web search
  - read logged-in web pages
---

# Dokobot Remote Browser

## Core idea

Do not build a crawler, proxy, or second browser tool.

Use the official Dokobot CLI on a real browser host:

```text
Agent/controller -> SSH or Tailscale SSH -> browser host -> dokobot read --local -> local browser bridge -> browser session
```

The remote machine is the browser. The Agent only sends commands and reads Markdown from stdout.

## When to use

Use this when the Agent needs browser-quality search or page reading from a stable desktop/browser environment instead of the Agent runtime.

Good fit:

- Search result pages rendered by a real browser.
- JavaScript-heavy pages.
- Pages that need the browser host's existing cookies or login state.
- Cases where the Agent runtime IP has weak search quality, bot detection, geolocation problems, or blocked engines.

Not a fit:

- CAPTCHA solving.
- Complex click-heavy workflows.
- High-concurrency crawling.
- Reading data the browser user is not authorized to access.

## Required setup

Controller side:

- SSH reachability to the browser host.
- An SSH client/library.
- Credentials stored outside prompts and repositories.

Browser-host side:

- SSH server or equivalent remote command entrypoint.
- Node.js/npm.
- `@dokobot/cli` installed and available as `dokobot` in the non-interactive SSH shell.
- Chrome/Edge/Brave/Arc installed.
- Dokobot browser extension installed.
- Dokobot native bridge installed and connected.
- Browser profile logged into any sites that need login state.

## Best procedure

1. SSH to the browser host.
2. Run a health check:

   ```bash
   dokobot --version && dokobot doko list
   ```

3. Confirm at least one `Local:` bridge/device appears.
4. If multiple devices appear, choose one device id for this run and pass it to every read command:

   ```bash
   dokobot read --local --device "DEVICE_ID" "https://example.com"
   ```

5. For search, do **not** use `dokobot search` unless Dokobot cloud/API is configured. Build a search URL and read it through the browser:

   ```bash
   dokobot read --local --device "DEVICE_ID" "https://www.google.com/search?q=YOUR_QUERY&num=10&hl=en&gl=us"
   ```

6. Parse the returned Markdown for result titles, snippets, URLs, AI Overview/news/video blocks, etc.
7. Deep-read selected results with the same device:

   ```bash
   dokobot read --local --device "DEVICE_ID" "https://target.example/path"
   ```

8. Fall back to another search/read tool only if SSH, Dokobot, the bridge, or the browser host is unavailable.

If there is exactly one local device, `--device` can be omitted. In automated Agent workflows, prefer detecting the device from `dokobot doko list` and using it explicitly. Device ids can change after browser/bridge restarts, so do not hard-code them in public docs.

## Google URL defaults

For broad web search:

```text
https://www.google.com/search?q=<urlencoded query>&num=10&hl=en&gl=us
```

Useful variants:

```text
&tbm=nws      # Google News tab
hl=zh-CN     # Chinese interface/snippets
site:...     # constrain to a source, e.g. site:reddit.com/r/LocalLLaMA
```

## Practical limits

- Keep concurrency low. For real-browser reads, `2-3` parallel reads is usually the safe range.
- Expect single reads to take seconds, not milliseconds. Real browser rendering is the point.
- Prefer direct `dokobot read --local` over custom abstractions. A small helper is fine for quoting/SSH credentials, but the reusable skill should stay centered on the Dokobot CLI.
- Do not route this through Chrome DevTools/CDP unless the task specifically needs DOM interaction. This workflow is for search/read extraction.

## Pitfalls

- Installing only Dokobot is not enough; the browser host needs an SSH server/remote-command entrypoint.
- The controller does not need Chrome; the browser host does.
- `dokobot` must be in the PATH of the non-interactive SSH shell, not just an interactive terminal.
- Multiple local bridges cause `Multiple bridges found`; pass `--device <id>`.
- Windows shell quoting differs. Quote URLs and device ids carefully.
- Some Windows OpenSSH setups emit connection reset after command close. Capture stdout/stderr before treating the connection close as failure.
- Logged-in content depends on the active browser profile on the browser host.
- Search result list pages may work while social-platform detail pages fail due to token/referer validation.
- Treat this as privileged access: the Agent can read what the browser session can read.
- Keep SSH credentials, internal IPs, hostnames, and device ids out of public repos.

## Regression check

For a reusable validation pass, test at least:

- health check/version/device list;
- Google English search;
- Google Chinese search;
- Google News tab;
- one static deep-read page;
- one JavaScript-heavy page;
- one logged-in or social/community page if relevant;
- a small `2-3` concurrency burst.

A healthy setup should return meaningful Markdown for each non-boundary case and no CAPTCHA/unusual-traffic page.
