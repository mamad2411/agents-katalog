---
name: kasm-browser
description: Drive a persistent interactive browser via Chrome DevTools Protocol (KASM Chrome)
---

# KASM Browser via CDP

When invoked, drive a persistent KASM Chrome browser using Chrome DevTools Protocol. Use this when a flow needs login state, cookies that persist, captcha/2FA, or React-style synthetic events.

## Inputs
- `action` -- one of: `navigate`, `click`, `type`, `screenshot`, `close_tab`, `eval`
- `url` -- target URL (for `navigate`)
- `selector` -- CSS selector (for `click`, `type`)
- `text` -- text to type (for `type`)
- `tab_id` -- existing tab to target (optional; otherwise pick or create)
- `output_path` -- for `screenshot` action, where to save the PNG

## Output
- `screenshot` action: file path to PNG.
- Other actions: status + DOM snapshot or evaluated value.

## Steps
1. Confirm CDP reachable: `docker exec <container> curl -s http://localhost:9222/json/version`.
2. List tabs: `docker exec <container> curl -s http://localhost:9222/json`.
3. Pick or create the target tab; capture its `webSocketDebuggerUrl`.
4. Open a WebSocket to that URL from inside the container.
5. Send the CDP commands for the action, applying the **Human-Speed Rule** between every meaningful step.
6. Capture results (DOM, screenshot, console output).
7. Close the WebSocket; tidy up any tabs your flow created.

## The Human-Speed Rule (mandatory)
**Slow IS fast.**

- Minimum **1.5-3 seconds** between meaningful actions.
- Typing: one key at a time, **80-150 ms between keystrokes** with jitter. Do NOT blast a full string via `input.value = "..."` on sites that profile typing cadence.
- Wait for `Page.loadEventFired` before queuing a second navigation.
- Self-imposed rate limit: ~20 CDP calls per 10 seconds.

Bot-detection systems flag burst patterns even when intent is benign. Human-speed pacing is free immunity. Apply regardless of how impatient the user is.

## Example: navigate + read title
```javascript
const sock = new ws(tab.webSocketDebuggerUrl);
// ... open WS, set up send() helper ...
await send("Page.navigate", { url: "https://example.com" });
await new Promise(r => setTimeout(r, 3000));   // human-speed wait
const title = (await send("Runtime.evaluate", { expression: "document.title" })).result.result.value;
```

## Notes
- CDP is reachable only from inside the container -- always go via `docker exec`.
- For full setup, cross-host usage, common recipes, and troubleshooting, see `sops/SOP_Interactive_Browser_via_KASM_CDP.md`.
- Always check the target site's Terms of Service before automating against it.
