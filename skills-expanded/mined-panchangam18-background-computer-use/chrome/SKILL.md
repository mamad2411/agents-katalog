---
name: chrome
description: Google Chrome heuristics for background-computer-use. Use when the user asks you to navigate, scroll, click links, fill forms, or otherwise drive Chrome without stealing focus. Also applies to Chromium-family browsers (Brave, Edge, Arc) that share the same AppleScript JavaScript execution primitive.
---

# Driving Chrome with background computer use

Chrome is Chromium-based and cooperates well with background automation once
the server enables `AXManualAccessibility` (which happens automatically on
the first `get_app_state`).

1. Call `get_app_state app="Google Chrome"` before interacting. The webpage
   DOM is exposed as accessibility nodes under a single `HTML content`
   element.
2. **URL navigation**: set the `Address and search bar` text field.
   `set_value app="Google Chrome" element_index=<N> value="https://…"` works
   and submits by default.
3. **Clicks on in-page links and buttons**: use `click(element_index=...)`.
   Chrome honors `AXPress` on Chromium AX nodes even when the window isn't
   key, so clicks don't steal focus.
4. **Typing into form fields**: `set_value` auto-falls-back to a typing
   path when the AX write is rejected (which is typical for Chromium
   controls). Focus stays with whichever app you had foremost.
5. **Scrolling**: `scroll app="Google Chrome" element_index=<HTML content>
   direction="down"` works via AppleScript `execute ... javascript`. It
   finds the nearest scrollable ancestor at the viewport center (so it
   picks the right sub-scroller in app-style pages like Gmail, LinkedIn,
   or Notion, not just `window`).

Known limitation:
- `scroll` for Chrome always scrolls a window-level or sub-scroller
  picked by the "viewport-center ancestor" heuristic. If you need to
  scroll a specific sub-region that isn't at the viewport center, click
  into it first to re-center the heuristic, or use `press_key key="PageDown"`
  with the understanding that it will focus Chrome.

Detailed notes live in `server/app-hints/Chrome.md`; they are injected as
`<app_hints>` on every `get_app_state` call for Chrome.
