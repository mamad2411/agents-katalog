---
name: knock-knock-neo
description: Play the cinematic Matrix "Wake up, Neo..." wake-up sequence on the user's machine — digital rain, slow ghost-typed messages ("Wake up, Neo...", "The Matrix has you...", "Follow the white rabbit.", "Knock, knock, Neo."), audible knocks, a timed macOS notification from "Unknown", and a white-rabbit keypress ending on "There is no spoon." Use whenever the user invokes /knock-knock-neo, or asks for "the Matrix experience", "wake up Neo", "knock knock Neo", "digital rain / Matrix rain in my terminal", "make my terminal look like the Matrix", "follow the white rabbit", or wants a Matrix-style terminal surprise or easter egg — even if they don't name the skill. Purely local and harmless; nothing leaves the machine.
---

# Knock, Knock, Neo

Recreate the opening scene of The Matrix for the user, as if they were Neo: their screen gets taken over by a green-on-black terminal window that plays digital rain, then slowly ghost-types the iconic messages, knocks audibly, and pings a macOS notification from "Unknown" timed to the knock.

The full sequence lives in `scripts/neo.py` (Python 3 + curses, no dependencies). Do not rewrite it — run it.

## How to run (macOS, the full experience)

1. **Launch the script in its own dedicated Terminal window and put that window into a native fullscreen Space** — that's what removes the macOS menu bar (it auto-hides in fullscreen, so every pixel belongs to the show). Use the built-in "Homebrew" profile (green on black), and set the window's `AXFullScreen` accessibility attribute (deterministic; the ⌃⌘F keystroke is only the fallback):

   ```bash
   osascript <<'EOF'
   tell application "Terminal"
     activate
     set w to do script "clear; python3 '<absolute-path-to>/scripts/neo.py'; exit"
     try
       set current settings of w to settings set "Homebrew"
     end try
   end tell
   delay 0.5
   tell application "System Events" to tell process "Terminal"
     set frontmost to true
     try
       set value of attribute "AXFullScreen" of window 1 to true
     on error
       try
         keystroke "f" using {command down, control down}
       end try
     end try
   end tell
   delay 1.2
   tell application "System Events" to tell process "Terminal" to get value of attribute "AXFullScreen" of window 1
   EOF
   ```

   Resolve `<absolute-path-to>` from this skill's own directory. The last line echoes `true`/`false` so you can VERIFY fullscreen actually engaged — don't assume. The script is resize-proof: the rain adapts to the fullscreen transition mid-fade instead of skipping. If the result is `false`, both fullscreen paths were blocked by a missing Accessibility permission for the app hosting the session; fall back to `tell application "Terminal" to set bounds of front window to {0, 0, 2400, 1500}`, and tell the user granting Accessibility (System Settings → Privacy & Security → Accessibility) enables true fullscreen next time. Never abort the launch over fullscreen.

   Menu-bar caveat: macOS hides the menu bar in a fullscreen Space by default (it only peeks when the mouse touches the top edge). If it stays permanently visible, the user's setting keeps it shown in full screen. Diagnose by geometry: if the fullscreen window is positioned at y≈33 with height ≈ screen−33 (System Events `position`/`size`), the menu-bar band is statically reserved. On macOS 26 (Tahoe) the operative setting is `AutoHideMenuBarOption` in `com.apple.controlcenter` (0–3; 2 = "hide in full screen only" — the macOS default; 3 = never hide). The legacy keys `NSGlobalDomain AppleMenuBarVisibleInFullscreen` / `_HIHideMenuBar` are vestigial after Tahoe's menu-bar migration and changing them has no effect. To apply a change live: `defaults write com.apple.controlcenter AutoHideMenuBarOption -int 2 && killall ControlCenter Dock` (no logout needed; already-created fullscreen Spaces keep the old band — relaunch the show). This alters system-wide behavior, so ask the user before changing it unless they explicitly asked for the menu bar to disappear; report the previous value so they can revert.

2. **Schedule the out-of-band knock** — a macOS notification that arrives roughly when the door-knock plays (~45 s in, right after "Knock, knock, Neo." finishes typing). Run it as a background task so it doesn't block:

   ```bash
   (sleep 45 && osascript -e 'display notification "Knock, knock, Neo." with title "Unknown" sound name "Bottle"') &
   ```

   This is the touch that reaches *outside* the terminal — keep it unless the user asks for a silent run.

3. **Tell the user what's happening** only AFTER launching — the surprise is part of the experience. Then briefly narrate the sequence: rain fades in → three ghost-typed messages that dissolve → "Knock, knock, Neo." types, then knuckles rap the door → white rabbit waits for a keypress → rain slowly devours the screen → "There is no spoon."

## Sequence timing (for reference, not for editing)

The script is self-contained: ~1.5 s of black silence, ~7 s of rain fading in under a low drone, each message types at 90–220 ms per character with a blinking block cursor (each character ticks), dissolves character-by-character with a digital glitch, "Knock, knock, Neo." types first and THEN three quick knuckle-raps hit the door (screen first, reality answers — movie order), a soft ping marks the white rabbit, and after the keypress the final rain devours the lingering text (it never clears the screen first — that overwrite IS the animation, and it is deliberately non-skippable). Input hygiene: queued keypresses are drained before the rabbit prompt and before each rain, so stray keys can't fast-forward scenes. The curses code is resize-proof: `KEY_RESIZE` events (fullscreen transitions, window drags) re-size the rain grid and re-center text instead of skipping scenes.

## Sound assets

All sounds are synthesized `.wav` files bundled in `assets/` and played with `afplay` (non-blocking; missing files are silently skipped):

- `key0.wav`–`key3.wav` — dry, sharp terminal data-ticks (movie-style, not keyboard clacks), one picked at random per typed character
- `knock.wav` — three quick knuckle-raps on a hollow wooden apartment door, with room reflections
- `drone.wav` — 12 s low ominous pad under the rain (self-fading)
- `glitch.wav` — descending digital zipper when a message dissolves
- `rabbit.wav` — soft bright ping for the white-rabbit prompt

They are generated by `scripts/make_sounds.py` (stdlib-only synthesis — no numpy, no copyrighted movie audio). Rerun that script only when redesigning a sound; the wavs are committed assets.

## Fallbacks

- **Non-macOS / no Apple Terminal** (Linux, SSH, iTerm-only setups): run `python3 scripts/neo.py` directly in the current terminal. Curses works anywhere; the script degrades gracefully — `afplay` and the notification simply don't fire. Skip step 2.
- **No audio hardware or `afplay` missing**: the script ignores sound failures; nothing to do.
- **User asks to make it permanent**: offer to install a small wrapper command on their PATH or a scheduled job that knocks at a random evening moment — but only build that if they ask.

## Safety

Everything is local: one curses script, system sounds, one notification. It writes no files, reads no user data, and touches no network. Never extend it to do otherwise.
