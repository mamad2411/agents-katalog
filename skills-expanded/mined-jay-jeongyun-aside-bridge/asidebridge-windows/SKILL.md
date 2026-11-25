---
name: "asidebridge-windows"
description: "Control the Windows desktop (any window or app, Explorer, Settings, browsers) from an AI agent (for example the Aside agent on Windows) through AsideBridge for Windows, a local helper that runs PowerShell, UI Automation, Unicode keyboard/mouse input, screenshots and OCR in the logged-in user's interactive desktop session. Use when a task needs a desktop app and your own shell cannot see or drive the user's windows."
---

# AsideBridge for Windows skill

Your shell may not be able to reach the user's interactive desktop (no window list, no SendInput, no
UI Automation, no screen capture, no elevation). AsideBridge for Windows runs jobs there for you.
Send work with `bridgectl.py` (or `bridgectl.ps1` when Python is missing).

```powershell
python "$env:LOCALAPPDATA\aside-bridge\bridgectl.py" status   # "running": true means ready
# if the user installed elsewhere, ASIDEBRIDGE_HOME points at that folder
```

Exit codes: 0 ok, 1 command failed (read stderr or use `--json`), 2 bridge unavailable
(tell the user AsideBridge is not running; ask them to sign in again or run `Start-ScheduledTask AsideBridge`;
do not try to install it yourself).

## Workflow

1. Look: `wins [filter]` (titles, pid, rect; `Affinity` != 0 means capture-protected) -> `uia tree --win "Title" --depth 5`
   (names, types, center coordinates) -> if UI Automation is thin, `ocr --win "Title"` (text lines with screen coordinates).
2. Act: prefer `uia action --win "Title" --name "Save" --type Button --action invoke|setvalue|focus`;
   otherwise `activate "Title"` + `click X Y`, or `clicktext 'Label' --win "Title"`.
3. Text: `type 'any Unicode text'` (IME-safe) or `paste 'long text'` (restores the clipboard). Never type
   non-Latin text key by key.
4. Verify with a fresh `uia ... --action text`, `ocr`, or `cdp eval` before reporting success.
5. Many steps: one `seq` call instead of many round-trips. Check `recipe list` first for a saved flow.

## Commands

```text
ps 'Get-Process | Select -First 3'    cmd 'dir'    (-f FILE for scripts; --timeout N; ps runs with the bridge's rights)
wins [filter] | front | idle | sysinfo
shot [--win T] [--region x,y,w,h] [--out P] [--ocr] [--bg]     --bg = PrintWindow, works on covered windows
ocr [PATH] [--win T] [--find TEXT]                               coordinates are physical pixels
wait text|gone-text|window|gone-window TARGET [--win T] [--timeout S]
watch [--win T | --region ..] [--wait S]                         returns when the area changes
type 'text' | paste 'text' | key ctrl+shift+s | click X Y | dclick | rclick | move | drag X1 Y1 X2 Y2 | scroll X Y LINES
clicktext 'Label' [--win T]
activate T | win move|min|max|restore|close|top|notop T [--region x,y,w,h]
uia tree|find|action --win T [--name N] [--type T] [--id ID] [--action A] [--value V]
run --name 'Start menu name' | run PATH [ARGS] [--elevated]      default: normal user rights
filedlg 'C:\path\file.txt'  |  reg get|set|del 'HKCU:\Software\Key' NAME [VALUE] [--type DWord]
cdp tabs|eval|navigate|new [--port 9222] [--expr JS] [--url U]  after scripts\start-browser-cdp.ps1
clip [get|set|paste] | notify 'msg' | notifications [--app NAME]
seq 'activate Notepad' 'key ctrl+a' 'paste hello' '?wait text hello --win Notepad'   (or seq -f steps.txt)
recipe list | run NAME k=v
stop | resume
```

## Input guard (do not fight it)

Every input command checks: the STOP file (`STOPPED`), the lock screen or UAC secure desktop (`LOCKED`),
the user being idle for 3 s (waits up to 20 s with a notification, then `USER_ACTIVE`), and with
`--expect TITLE` the foreground window (`FRONT_CHANGED`). On these errors, stop and tell the user; do
not retry in a loop. Use `--force` only when the user explicitly asks.

## Safety rules

- Anything sent as the user (messages, mail, files) needs the user's approval of the exact recipient and
  text first, unless the user already gave both explicitly.
- Never pay, delete, change security settings, or write the registry without explicit confirmation.
- Windows with `Affinity` != 0 (capture-protected, e.g. managed work apps) come out black: do not try to bypass that.
- Never print or copy the token file. Screenshots in `work\` may contain private content: do not upload them.
- If the user says stop, run `bridgectl stop` immediately.
