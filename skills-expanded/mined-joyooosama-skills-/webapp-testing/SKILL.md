---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# webapp testing

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`
- **examples/** - Examples showing common patterns:
- `element_discovery.py` - Discovering buttons, links, and inputs on a page
- `static_html_automation.py` - Using file:// URLs for local HTML

## Available sections

- Web Application Testing
- Decision Tree: Choosing Your Approach
- Example: Using with_server.py
- Reconnaissance-Then-Action Pattern
- Common Pitfall
- Best Practices
- Reference Files

## Bundled resources

- examples
- scripts

Open these resources only if the current task needs deeper detail or executable helpers.
