---
name: nitro-browser-testing
description: For projects using nitro-web only. Browser testing a Nitro-web app. Use only when explicitly asked to open, click through, screenshot, or verify the app.
---

  By default, the user checks the UI themselves, so only do this when asked...

# Dev server

  - The user keeps the dev server running themselves, outside Claude Code. The URL is normally documented in CLAUDE.md.
  - Never scan ports, probe, or launch a new dev server for this project.
  - If you cannot find the dev server URL, request the user to define it in CLAUDE.md so AI doesnt continue guessing and probing for it.

# Login

  - Nitro projects commonly auto-log in a dev user by detecting the browser agent (detects `Claude/` in the User-Agent).
  - If a sign in page still appears, check CLAUDE.md for dev credentials, and if they are there, submit and carry on without asking if it works.
  - If none are documented, ask the user for them and suggest adding them to CLAUDE.md so it doesn't come up again.

# Tips

  - `read_page` over `screenshot` for checking text and structure, it is cheaper and more reliable.
  - `read_console_messages` and `read_network_requests` are usually faster than clicking around when something is failing.
