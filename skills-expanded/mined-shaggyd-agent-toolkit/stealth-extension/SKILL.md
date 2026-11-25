---
name: stealth-extension
description: "Manifest V3 Chrome extension that patches browser fingerprint vectors at document_start for WAF bypass"
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
license: MIT
tags: [chrome, extension, stealth, fingerprint, waf-bypass, manifest-v3]
---

# Stealth Extension

A Chrome extension that makes headless Chrome look like a real browser. Patches fingerprint signals at document_start, before any page scripts can detect them.

## Problem

Most stealth approaches run too late. By the time your content script or flag kicks in, the page has already sampled navigator.webdriver, checked plugin count, probed the languages array, and queried the Permissions API. Once those signals are read, you've already lost.

## Built

A Manifest V3 extension with a single content script (stealth.js) that executes at document_start, before any page script or inline JS runs. It patches:

- **navigator.webdriver** - Set to `undefined` (removes the automation flag)
- **navigator.plugins** - Populated with realistic plugin entries
- **navigator.languages** - Set to `['en-US', 'en']`
- **Permissions API** - Returns realistic permission states
- **Chrome runtime** - Hides extension IDs and runtime signals

## Outcome

By the time the page loads, your browser fingerprint is indistinguishable from a real Chrome installation. WAFs like Cloudflare, LinkedIn, and Indeed see a normal user session and let traffic through.

## Installation

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select the `extensions/stealth-extension/` directory
5. Verify the extension shows up in the toolbar

No config needed. The extension runs automatically on all pages.

## Usage with agent-browser

```bash
agent-browser --args "--disable-blink-features=AutomationControlled,--load-extension=/path/to/stealth-extension" open https://example.com
```

## Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension manifest (Manifest V3, host permissions) |
| `stealth.js` | Patches browser fingerprint vectors at document_start |

## See Also

- [browser-automation](../browser/browser-automation/) skill - agent-browser CLI usage with stealth
- [stealth-browser MCP](../../mcp/stealth-browser/) - MCP server that bundles the extension inline
