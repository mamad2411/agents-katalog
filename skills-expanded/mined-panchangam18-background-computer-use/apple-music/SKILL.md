---
name: apple-music
description: Apple Music (Music.app) playback and search heuristics for background-computer-use. Use when the user asks you to play a song, add to the queue, adjust volume, or search the library via Apple Music.
---

# Driving Apple Music with background computer use

1. Always call `get_app_state app="Music"` (display name) or
   `get_app_state app="com.apple.Music"` before interacting.
2. The Play/Pause button toggles its title; re-read state after each press.
3. Prefer `set_value` over `type_text` when replacing the search field's
   contents; submit with `press_key key="Return"`.
4. Use `perform_secondary_action` with `ShowMenu` on track rows to reach
   "Add to Queue", "Play Next", "Copy Song Link", etc.
5. Use `scroll` against the library `collection` element's index, not the
   window. For a specific off-screen row, prefer
   `perform_secondary_action index "ScrollToVisible"`.
6. The volume slider is `settable=true`; use `set_value` with a string like
   `"0.5"` rather than arrow keys (which change playback position).

Extended guidance is injected as `<app_hints>` on every `get_app_state` call
for Apple Music; the source lives in `server/app-hints/AppleMusic.md`.
