---
name: spotify
description: Spotify desktop heuristics for background-computer-use. Use when the user asks you to pause, skip, search, queue, or otherwise control Spotify without stealing focus.
---

# Driving Spotify with background computer use

Spotify is Electron + WebView, so accessibility coverage is partial. Mix
element indexes with coordinate and keyboard fallbacks.

1. Always call `get_app_state app="Spotify"` before interacting.
2. Trust post-action snapshots, not pre-action ones — the UI lags real
   playback state by 300–800 ms.
3. Transport controls have reliable keyboard shortcuts; prefer them over
   coordinate clicks:
   - `space` — play/pause
   - `command+Right` / `command+Left` — next / previous
   - `command+Up` / `command+Down` — volume up / down
4. For search, try `set_value` on the search field first. If it silently
   fails, `click` the field, `press_key key="command+a"`, then `type_text`.
5. Track rows advertise `ShowMenu` as a secondary action for queue / add-to-
   playlist. Re-read state after the menu opens.

Detailed notes live in `server/app-hints/Spotify.md`; they are injected as
`<app_hints>` on every `get_app_state` call for Spotify.
