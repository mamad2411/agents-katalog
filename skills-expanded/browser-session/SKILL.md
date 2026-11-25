---
name: browser-session
description: Open, drive and close a stealth browser session when the user asks to browse, scrape or automate a website without being detected.
---

# Browser session

Use the `stealth-browser` CLI to control a Firefox-based browser that hides
automation fingerprints.

## Workflow

1. Start a session with `stealth-browser open <url>` and note the session id.
2. Drive the page with `stealth-browser click`, `stealth-browser type` and
   `stealth-browser snapshot`.
3. Close the session with `stealth-browser close <session-id>` when finished.

## Fingerprint guidance

Read references/guide.md for the fingerprint profiles the server supports and
which one to pick for a given target site.
