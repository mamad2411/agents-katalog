---
name: orca-human-like-control
description: >-
  Drive a real desktop Chrome window (via Orca's `orca computer`) and a real USB Android
  phone (via adb + scrcpy) the way a person does: look, find one target, act once with
  human-shaped input (random point inside the target, press duration and pressure, curved
  swipes, keystroke rhythm, Unicode text in any language), check, pause. Use when a task needs a
  signed-in browser session, a page only a real browser shows, or an app on a physical
  phone. Not for headless/embedded browsers, emulators, or work an API/CLI can do.
license: MIT
compatibility: >-
  Python 3.9+ (stdlib only). Chrome surface: macOS + Orca CLI with Accessibility and Screen
  Recording granted. Android surface: adb, USB debugging authorized, Android 10+.
metadata:
  version: "0.1.0"
  repository: https://github.com/spksoft/orca-human-like-control
---

# Orca human-like control

`scripts/human.py` (next to this file) turns one intent into human-shaped input and prints
one JSON line per action as evidence. Keep using raw `orca computer` / `adb` to *read*
state; use the helper to *act*.

```bash
H="<this skill's directory>/scripts/human.py"    # e.g. .agents/skills/orca-human-like-control/scripts/human.py
python3 "$H" --version
python3 "$H" --dry-run android swipe --direction up   # shows what would be sent, touches nothing
```

## Rules (stop and ask the user)

- Posting, commenting, liking, following, messaging, uploading, going live, buying,
  deleting, or changing account/app/device settings: only the exact action the user asked
  for. Draft it, show it, wait.
- Human-shaped input is for the user's own accounts at personal-use volume. It narrows the
  gap to a real person; it does not make automation undetectable (see "Fidelity"). A
  captcha, "unusual traffic" or HTTP 429 page means stop and report.
- Read only what the task needs. Never open mail, DMs, banking or password screens
  unprompted; never read cookies, passwords, autofill or a PIN. Never print clipboard
  contents.
- Installing anything (adb, an APK, a keyboard) needs the user's approval.
- Locked phone: ask the user to unlock it. Never type a PIN or pattern.
- `--restore-window` takes over the user's screen and mouse; ask first.

## The loop

1. **Look.** Fresh tree (`orca computer get-app-state`, `human.py android find`) plus a
   screenshot when layout or media matters. Never act on a tree older than your last action.
2. **Find.** One target by label, text or resource id. Two matches: disambiguate first.
3. **Act once** through the helper.
4. **Check.** Read the result or look again and name what changed. Nothing changed means
   unproven: change approach once (see fallbacks), then report. Never repeat blindly.
5. **Pause.** `python3 "$H" pause glance|think|read|watch` sleeps a lognormal human interval
   (medians 0.6 / 1.4 / 3 / 7 s).

## Chrome (desktop window, background input)

```bash
orca computer list-windows --app com.google.Chrome --json            # pick the window id
orca computer get-app-state --app com.google.Chrome --window-id <id> --json   # tree + screenshot

python3 "$H" chrome click  --window-id <id> --box x1,y1,x2,y2 --scale 2          # box read off the screenshot
python3 "$H" chrome type   --window-id <id> --box <field box> --scale 2 --element-index <field> --text "Hi, you@x.io"
python3 "$H" chrome type   --window-id <id> --element-index <field> --text "Grüße · こんにちは · สวัสดี 👋"   # non-ASCII
python3 "$H" chrome scroll --window-id <id> --x 700 --y 450 --pages 1.2
```

- `click`: random point in the middle 60% of the box, ~150 ms press at pressure 0.5, 0.5-3 px
  slip (implemented as a tiny `orca computer drag`, because a background `click --x --y`
  never reaches Chrome's page).
- `type`: ASCII becomes real keystrokes with the right key codes, Shift for capitals and
  symbols, and irregular gaps. Anything else (accents, CJK, Thai, Cyrillic, Arabic, emoji) grows the field value in 1-3 code
  point bursts with `set-value`, which replaces the field's content. It ends with a
  `chrome.readback` line.
- `scroll`: several 80-160 px wheel steps with a jittered position instead of one jump.
- Fallback: if a human click changes nothing, press the element once with
  `orca computer click --element-index <n>` (some widgets ignore synthetic drags).
- Never use `type-text` or `paste-text` on web pages: Chrome receives the text twice.

Navigation, tab etiquette, key coverage and the raw-verb event table: `references/chrome.md`.

## Android (physical phone over USB)

```bash
adb devices -l                                        # one device in state "device"
python3 "$H" android shot --out /tmp/phone.png        # then look at the image
python3 "$H" android find --text "Search" --contains  # nodes + bounds; no selector = clickable nodes

python3 "$H" android tap --text "Display"             # or --desc / --id / --box l,t,r,b / --x --y (px or 0..1)
python3 "$H" android long-press --desc "Instagram"
python3 "$H" android swipe --direction up --speed read    # finger up = next content; no fling
python3 "$H" android swipe --direction up --speed fling   # next short video
python3 "$H" android type --text "你好 · Привет · สวัสดี 👋"   # ADBKeyBoard, one code point per keystroke
python3 "$H" android type --method paste --text "long caption"   # clipboard paste, clipboard restored
python3 "$H" android batch <<'EOF'
tap --desc "Clear search field"
pause glance
swipe --direction down --speed fling
EOF
```

- Touches go through a control-only scrcpy server (v2.4, sha256-pinned; Orca's cached copy
  is reused, else it is downloaded once) so the helper controls timing and pressure.
- `tap`: Gaussian point inside the node, 45-220 ms hold, 0-3 px drift, varying pressure.
- `swipe`: quadratic arc, ~120 Hz samples; `read` decelerates and stops before lift,
  `fling` accelerates into the release.
- `type --method ime` switches to ADBKeyBoard, types, then restores the user's keyboard
  and disables ADBKeyBoard even on error; check `ime_restored: true`.
- `uiautomator` refuses while video plays; use `android shot` and `--box` / `--x --y` then.

Setup (ADBKeyBoard), touch model details and why not `sendevent` / `input`:
`references/android.md`.

## Fidelity

|Signal|Chrome|Android|
|---|---|---|
|Click/tap point|random inside target|random inside target|
|Press duration, pressure|~150 ms, 0.5|45-220 ms, 0.22-0.5, varying|
|Scroll/swipe|80-160 px wheel steps|curved, accelerating or decelerating|
|Typing|real key codes + rhythm (ASCII); value bursts (Unicode)|IME commits per code point + rhythm|
|Still detectable|window focus/blur flicker per action; no pointer travel before a click|events are injected, not from the touch panel; USB debugging on; ADBKeyBoard visible while typing|

## Evidence to report

- The helper's JSON lines (`at`, `hold_ms`, `node`, `readback`, `ime_restored`,
  `clipboard_restored`), window titles or the foreground activity before/after, and a final
  screenshot path.
- Anything unverified is reported as unproven, especially if it could have sent or published.
