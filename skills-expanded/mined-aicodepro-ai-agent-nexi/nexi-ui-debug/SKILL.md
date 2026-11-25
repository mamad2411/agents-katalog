---
description: "Nexi HUD (Eel/JS) debugging — waveform/orb rendering, EEL bridge, voice-state transitions. Use when the UI lags, freezes, or ignores state updates."
license: "MIT"
---
# Nexi UI Debug

The active HUD lives in `www_mark/` (Nexi rebrand of the old `www/` — that
directory is deleted on this branch, don't debug against it).
`engine/ui_event_bridge.py` is the Python->JS bridge; `www_mark/hud_orb.js`
renders the reactive orb + waveform.

## The DOM-thrash lesson (already fixed, don't reintroduce)

`hud_orb.js`'s waveform used to rebuild via `innerHTML` every animation
frame (~1700 element constructions/sec — each a full parse + style recalc +
layout). That was the actual source of "the UI feels laggy," not slow
Python. Fix in place: build the 28 waveform bars **once**, then only mutate
`bar.style.height` / colour per frame; write colour only when the state
actually changes (see `_wfColor` diffing around line 260-275). When touching
render code here: never reconstruct DOM nodes inside the
`requestAnimationFrame` loop (`step`, ~line 355) — mutate existing nodes.

## Python -> JS bridge — `engine/ui_event_bridge.py`

- `_safe_eel_call(fn_name, payload)` wraps every Eel call; missing JS
  functions log `[EEL] missing_js_function name=<fn>` instead of raising —
  if the HUD "isn't updating," check this log line first, it tells you
  exactly which JS-side function is absent (e.g. `updateTranscript`,
  `updateSpeechCapsule`, `DisplayMessage`, `receiverText`,
  `hideSpeechCapsule`) before assuming the Python side is broken.
- `_redact_secrets(text)` scrubs outbound text — a secret leaking into the
  HUD is a bug in the redactor, not something to patch at the call site.
- State helpers (`set_state`, `speech_start/stop`, `listening_start/stop`,
  `thinking_start/stop`, `wake_detected`, `sleeping`) are the only sanctioned
  way to move HUD state — don't push raw Eel calls from elsewhere.

## Voice-state machine gotchas

- `[VOICE_STATE] transition_failed reason=no_valid_transition` in logs is
  usually correct, not a bug — most states intentionally reject transitions
  from `sleeping`/`cooldown` while a cooldown window is active
  (`[POST_TTS] cooldown_active remaining_ms=...`). Check the cooldown timer
  before "fixing" the transition table.
- `[UI_STATE] conflict_resolved previous=X next=Y` means two sources raced to
  set state; the log already tells you which one won — trace the source
  that lost if it should have won instead.

## Verifying a fix

Prefer driving the real HUD (Edge channel via Playwright/chrome-devtools
MCP) over reading the JS by eye — animation/layout bugs don't show up in a
diff review. Confirm branding stays Nexi (never Jarvis/Stark/Mark) in any
user-visible string you touch.
