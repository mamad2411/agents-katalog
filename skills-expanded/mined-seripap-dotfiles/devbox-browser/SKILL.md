---
name: devbox-browser
description: >
  Drive a remote headless browser on the devbox to take screenshots or validate
  that a web app is actually working — load a URL, check status, capture console
  errors, see what rendered. Use when the user asks to "screenshot X", "see
  what the page looks like", "is the page broken", "did my change render",
  "check if the site loads", "any console errors", or hands you a URL and asks
  if it works. Requires `bin/devbox-shot` (this dotfiles repo) and the devbox
  itself to be reachable.
---

# devbox-browser

Lets you actually see what a web app is doing, not just guess from the diff.
The browser runs on the remote devbox; you drive it from here via
`devbox-shot`, which auto-starts the server and ssh tunnel on first use.

## When this skill applies

- "Take a screenshot of <url>" / "show me what the page looks like"
- "Did my change actually render?" / "is the layout broken?"
- "Does <url> load?" / "any errors on the page?"
- After a frontend edit when verification by eye is faster than reading code
- User pastes a URL and asks if it works

If the user only wants HTTP status, `curl -I` is cheaper — skip the browser.

## Tools

Both commands auto-start `devbox-playwright` if the tunnel is down.

### Screenshot

```sh
devbox-shot shot <url> [out.png]
```

- Prints the file path on stdout.
- Defaults to `$TMPDIR/devbox-shot-<epoch>.png`, full page, 1280x800.
- Override: `DEVBOX_SHOT_VIEWPORT=1440x900`, `DEVBOX_SHOT_WAIT=load|domcontentloaded|networkidle`, `DEVBOX_SHOT_TIMEOUT_MS=30000`.

Read the PNG back with the Read tool to actually look at it — don't just
report "screenshot saved" without inspecting.

### Validate

```sh
devbox-shot check <url>
```

Returns JSON:
```json
{
  "url": "...",
  "finalUrl": "...",          // after redirects
  "status": 200,
  "title": "...",
  "consoleErrors": [],
  "pageErrors": [],
  "failedRequests": [{"url": "...", "failure": "..."}],
  "navError": null            // string if goto() threw
}
```

A page that "works" has `status: 200`, no `pageErrors`, no `failedRequests` for
first-party assets. Console warnings are noise; console *errors* often matter.

## Typical flow

1. User edits a component, asks "does it look right?"
2. Find the running dev server URL (read package.json scripts, ask if unclear).
3. `devbox-shot check <url>` first — cheap sanity check. If `navError` or 5xx,
   the server isn't up; stop and tell the user.
4. `devbox-shot shot <url> /tmp/before.png`, Read it, describe what's there.
5. After the user iterates: shot again, compare.

For local dev servers on the laptop (`localhost:3000`), the devbox can't reach
them by default. Either run the dev server on the devbox too, or set up a
reverse tunnel — flag this to the user rather than silently failing.

## Don't

- Don't run screenshots in a loop without a reason. One shot per question.
- Don't claim a page works because `status: 200` — check `pageErrors` and look at the screenshot.
- Don't leave the playwright server running forever if the user is done; `devbox-playwright stop` cleans up.
