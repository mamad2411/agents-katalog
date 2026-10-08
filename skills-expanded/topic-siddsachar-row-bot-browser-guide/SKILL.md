---
name: browser_guide
display_name: Browser Guide
icon: "🌐"
description: Guidance for browser automation workflows.
tools:
  - browser
tags: []
---
BROWSER AUTOMATION (experimental):
- You have a browser tool that opens a REAL visible browser window.
  The user can see the browser and interact with it too (e.g. to type
  passwords or solve CAPTCHAs).
- Workflow: browser_navigate → read the snapshot → browser_click /
  browser_type / browser_scroll → read updated snapshot → repeat.
- You can manage tabs with browser_tab: list open tabs, switch between
  them, open new tabs, or close tabs by index.
- Use browser_back to navigate back to the previous page.
- Each snapshot lists interactive elements with numbered refs like
  [1] button "Submit", [2] input[text] "Search". Use the ref number
  to click or type.
- IMPORTANT: refs become stale after any navigation or page change.
  Always use the refs from the MOST RECENT snapshot only.
- If you encounter a login page or CAPTCHA, tell the user to handle it
  in the browser window, then call browser_snapshot to see the result.
- When the user says 'browse', 'open in the browser', or asks you to
  interact with a page (click, scroll, fill forms), ALWAYS use the
  browser_* tools.  Use read_url ONLY when you need raw text from a URL
  and the user has NOT mentioned the browser.
