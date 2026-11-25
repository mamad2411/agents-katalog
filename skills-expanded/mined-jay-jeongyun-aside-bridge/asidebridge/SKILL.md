---
name: "asidebridge"
description: "Control native macOS apps from a sandboxed AI agent (for example the Aside browser agent) through AsideBridge, a local helper that runs AppleScript/JXA/shell, guarded keyboard and mouse input, screenshots and OCR OUTSIDE the sandbox. Use when a task needs a desktop app (Finder, Mail, Notes, messengers, System Settings, any app) and plain shell fails with -10827 or Apple Events errors."
---

# AsideBridge skill

Your shell runs in a sandbox that blocks Apple Events and LaunchServices: `osascript` to other
apps and `open -a` fail with `-10827`. AsideBridge is a helper app running outside the sandbox.
Send it work with `bridgectl.py`; it runs with the user's Accessibility, Automation and Screen
Recording grants.

```bash
B="python3 ${ASIDEBRIDGE_HOME:-$HOME/.asidebridge}/bridgectl.py"   # if ~ is remapped, use the absolute path
$B status        # "running": true and "axTrusted": true means ready
```

Exit codes: 0 ok, 1 command failed (read stderr or use `--json`), 2 bridge unavailable
(tell the user AsideBridge is not running; do not try to install it from the sandbox).

## Commands

```bash
$B as 'tell application "System Events" to get name of every application process whose visible is true'
$B jxa 'Application("Finder").windows().length'
$B sh 'open -a "Notes"' --timeout 20
$B as -f /path/script.applescript --timeout 120 --json
$B sh 'slow_command' --bg                   # detached, parallel; use when a permission prompt might appear

$B wins [filter] | front | idle | sysinfo   # JSON
$B ocr --win APP [--find TEXT]              # text + screen-point coordinates; works on covered windows
$B shot --win APP --out /path/x.png
$B wait text|gone-text|window|gone-window TARGET --win APP --timeout 10
$B watch --region x,y,w,h --sec 1           # percent of pixels changed

$B type 'any Unicode text' | paste 'long text' | key cmd+shift+g
$B click X Y | dclick X Y | rclick X Y | move X Y | drag X1 Y1 X2 Y2 | scroll DY [DX]
$B clicktext 'Button label' --win APP
$B activate APP | clip [text] | notify 'msg'
$B seq -f steps.txt --expect APP            # many steps in one call; stops on failure with a screenshot
$B recipe list | run NAME k=v
$B stop | resume                            # pause switch
```

Coordinates are screen points (not Retina pixels). `ocr` returns `cx`/`cy` you can pass to `click`.

## Input guard (do not fight it)

Every input command checks: STOP file (`STOPPED`), lock screen (`LOCKED`), the user being idle
for 3 s (waits up to 20 s, then `USER_ACTIVE`), and with `--expect APP` the front app
(`FRONT_CHANGED`). On these errors, stop and tell the user; do not retry in a loop.
Use `--force` only when the user explicitly asks.

## Working style

- Prefer AppleScript/JXA with the app's dictionary or System Events AX actions over pixel clicks.
- Prefer one `seq` over many single calls: each agent round-trip costs far more than the action.
- For non-Latin text use `type` (input-method safe) or AX `set value`, not `keystroke`.
- Verify results with `ocr`, `wins` or AX reads before reporting success.

## Safety rules

- Anything sent as the user (messages, mail, files) needs the user's approval of the exact
  recipient and text first, unless the user already gave both explicitly.
- Never pay, delete, or change system security settings without explicit confirmation.
- Never print or copy the token file.
- If the user says stop, run `$B stop` immediately.

## Vercel agent-desktop / agent-browser

If `agent-desktop` or `agent-browser` fail inside the sandbox (no Accessibility, cannot start Chrome), run them through the bridge: `bridgectl desktop ARGS...` (alias `ad`) and `bridgectl browser ARGS...` (alias `web`, dedicated session `aside-bridge`). Read `bridgectl desktop skills get desktop` first.
