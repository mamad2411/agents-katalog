---
name: safari
description: Safari desktop heuristics for background-computer-use. Use when the user asks you to navigate, scroll, click links, switch tabs, or otherwise drive Safari without stealing focus.
---

# Driving Safari with background computer use

Safari's accessibility coverage is good overall, but its address bar and
web content areas have two quirks that bite naive automation.

1. Always call `get_app_state app="Safari"` before interacting.
2. To navigate to a URL, call
   `set_value app="Safari" element_index=<smart-search-field> value="https://…"`.
   - The smart search field's ID is `WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD`.
   - `set_value` submits by default; don't also post a separate `Return`.
   - Internally this uses a typing fallback, because Safari silently
     ignores `AXValue` writes on the URL bar.
3. To scroll the page, call
   `scroll app="Safari" element_index=<scroll-area> direction="down"`.
   The tool tries a native AX page-scroll first, then posts wheel events
   to the correct WKWebView helper pid, then falls back to `PageDown`/
   `PageUp` keystrokes if nothing moved.
4. `click(element_index=<link>)` works on in-page links via `AXPress`
   even when the Safari window is occluded.
5. Tab switches: `click(element_index=<tab>)` on an `AXTabButton`. Close
   with `perform_secondary_action(action="close tab")` rather than
   hit-testing the tiny close glyph.

Detailed notes live in `server/app-hints/Safari.md`; they are injected as
`<app_hints>` on every `get_app_state` call for Safari.
