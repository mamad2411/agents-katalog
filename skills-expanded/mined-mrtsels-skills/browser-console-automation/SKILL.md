---
name: browser-console-automation
description: Use when writing browser console automation scripts.
metadata:
  imported_from: hermes
---

# Browser Console Automation Scripts

Bookmarklet-style scripts pasted into the browser DevTools console (or injected via CDP) that automate page actions: check checkboxes, click buttons at a target time, validate forms. Example class: course-registration helpers such as `~/cuhk-tools/validate.js` and `~/cuhk-tools/enroll.js`.

## Log Overlay Conventions (user preferences — apply by default)

1. **Bottom-anchored**: `position: fixed; bottom: 0; left: 0; width: 100%`
2. **Single-line display**: `overlay.innerText = message` (replace), NOT appendChild — show only the latest line
3. **Millisecond timestamps** for timing scripts: `HH:MM:SS.mmm` (e.g. `12:11:43.377`)
4. **STE100 English** log messages: active voice ("The script clicks the Enroll button." not "Enroll button clicked."), short sentences, consistent terms, no "will" / "eg" / "etc." — see the `simplified-technical-english` skill
5. **Center alignment** (user iterated left → right → center; center is final)
6. Always `console.log(message)` in parallel — the overlay shows one line, the console keeps full history

Starter file: `templates/overlay-script.js` (copy and modify).

## Pitfall: styles on reused overlays

Put style assignments OUTSIDE the `if (!overlay) { create }` block. On a second run in the same page the overlay element already exists, the creation block is skipped, and styles set only inside it silently do not apply.

```js
let overlay = document.getElementById("log-overlay");
if (!overlay) {
  overlay = document.createElement("div");
  // ...create + set styles + append...
}
overlay.style.textAlign = "center"; // runs on EVERY execution
```

## Injecting via CDP (chrome-devtools-mcp / mcporter)

- `evaluate_script` wants a **function declaration**, not an IIFE: strip `(function () {` ... `})();` and wrap the body as `function run() { ... }`. Passing the raw IIFE fails with "Unexpected token ';'".
- Handle `window.prompt` / `window.confirm` via `dialogAction`: `"accept"`, `"dismiss"`, or a STRING that becomes the prompt's response (e.g. a target time `"2026-08-10 12:30:00"`). Alternative: `handle_dialog(action, promptText)` afterwards.
- Large scripts: build the JSON payload in Python (`json.dumps({"function": fn, "dialogAction": ...})`), quote with `shlex.quote`, run `mcporter call chrome-devtools.evaluate_script --args <json>`. `--args @file` syntax is NOT supported.
- Verify effects by reading state back: `overlay.innerText`, `overlay.childNodes.length` (line count), `getComputedStyle(overlay).textAlign`, checkbox checked state.

## Page-navigation context loss

A `location.href` assignment (e.g. auto-redirect to the correct page) destroys the injected script — the new page has no script. Design for it: detect the page state and prompt the user to re-paste, or open the target in a new tab. Do not expect the script to survive navigation.

## Testing loop

Run script → sleep → read overlay logs via evaluate_script → confirm final page state (success text, e.g. "Okay to Add") → tune timings from measured latency (e.g. measured select→click takes 2 ms → keep a 200 ms margin).

## CUSIS specifics

DOM structure, URL modes, multi-login restriction, and reference scripts for the CUSIS PeopleSoft cart: see `references/cusis-2026-structure.md`.
