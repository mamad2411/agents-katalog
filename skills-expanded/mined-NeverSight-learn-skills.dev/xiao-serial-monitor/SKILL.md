---
name: xiao-serial-monitor
description: >
  Serial monitoring for a XIAO ESP32S3 (or any Arduino board) on Windows, in
  both modes that matter: a bounded read the agent can run to debug its own
  changes, and a persistent terminal monitor handed to the user with clear
  instructions for checking output later. Auto-detects the COM port by USB
  vendor ID, survives the port dropping on every reset and re-upload, and adds
  one-word `mon` / `flash` shortcuts to the PowerShell profile. Use this skill
  WHENEVER serial output is involved: reading what a board is printing, asking
  to "open the serial monitor", wanting it available "every time" or as a
  shortcut, a monitor that keeps disconnecting, needing Ctrl+C before every
  upload, the wrong COM port being picked, or whenever you are about to tell
  the user how to watch the board themselves.
license: MIT
compatibility: Windows + PowerShell 5.1, arduino-cli >= 1.x
---

# Serial monitor: bounded for you, persistent for the user

Opening a serial port serves two different purposes, and one script covers both.

| | You debugging | The user watching |
|---|---|---|
| Goal | capture output, act on it | keep a window open all session |
| Command | `mon.ps1 -Seconds 10` | `mon.ps1` |
| Ends | on its own | on Ctrl+C |

Read the board yourself whenever you need to verify something — that is what
bounded mode is for, and it returns a normal exit code.

## The rule that matters most

**Bounded when you run it; hand over the interactive one with a note.**

`mon.ps1` without `-Seconds`, and `flash.ps1` without `-NoMonitor`, never
return. Running those in a tool call hangs the session while the user watches
nothing happen — the complaint that motivated this skill was literally "if you
start it, it takes forever." So:

- Debugging your own change → `mon.ps1 -Seconds 10`. Bounded, safe, no handoff.
- Upload inside a script → `flash.ps1 <sketch> -NoMonitor`, which exits with a
  real status code.
- The user wants to watch it themselves, now or later → don't launch it. Leave
  the exact command they can run whenever they want.

That last one is the part worth being deliberate about. After you set the
scripts up or finish a change the user will want to observe, close with a short
handoff — the command, and how to run it:

> The serial monitor is ready whenever you want to check it:
> ```
> ! C:\path\to\scripts\mon.ps1
> ```
> In Claude Code the `!` prefix runs it right in the session. Ctrl+C exits.
> If you added the profile shortcuts, `mon` works from any new terminal.

Adapt the wording, but keep the three parts: the literal command, how to launch
it, and how to stop it. The user should never have to ask "so how do I see the
output?"

## Setup

Copy `scripts/` next to the user's sketches, or leave it in the installed skill
folder and reference it by absolute path. Then confirm detection works — this
returns immediately:

```powershell
. .\scripts\Find-BoardPort.ps1
Find-BoardPort -Explain
```

A COM port means you are ready. An empty result prints every COM port with its
vendor ID so the user can pick one manually with `-Port`.

Optional but this is usually the actual request — one-word access from any
directory. `assets/profile_snippet.ps1` defines `mon`, `flash`, and `boards`.
Append it to `$PROFILE`, edit the `$env:XIAO_TOOLS` path at the top, and note
that **the profile only loads in newly opened terminals**.

```powershell
# create the profile if absent, then append
if (-not (Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
Get-Content assets\profile_snippet.ps1 | Add-Content -Path $PROFILE -Encoding utf8
```

## Usage the user should be told about

```powershell
mon                      # monitor, port auto-detected
mon COM6 9600            # explicit port and baud
flash blink              # compile + upload + monitor
flash blink -NoMonitor   # upload only
boards                   # what is attached
```

And for your own verification, which returns:

```powershell
.\scripts\mon.ps1 -Seconds 10                  # read 10 s and exit
.\scripts\mon.ps1 -Seconds 10 -Send "ping"     # send a line first
```

Bounded mode opens the port with DTR asserted, which resets the board, so
output starts from a fresh boot banner rather than mid-stream.

## Pitfalls

These each cost a real debugging session once.

1. **The first "Serial Port (USB)" row is usually not your board.** Dev
   machines tend to carry a permanently attached USB-UART bridge (CP210x,
   CH340, FTDI), and it frequently enumerates on a *lower* COM number, so a
   naive pick silently monitors the wrong device — a dead-quiet window with no
   error. Match on USB vendor ID instead: `303A` Espressif, `2341` Arduino.
   `Find-BoardPort.ps1` does this. Note that `arduino-cli board list` shows the
   XIAO as `Unknown` with an empty FQBN column even when the esp32 core is
   installed, so FQBN matching alone will not find it.

2. **The COM number changes when the board is replugged.** Observed jumping
   COM5 → COM6 across one unplug. Anything with a hard-coded port breaks the
   moment someone moves a cable, which is why detection runs on every launch.

3. **`arduino-cli monitor` exits whenever the port drops.** USB-Serial/JTAG is
   part of the ESP32-S3 itself rather than a separate bridge, so the port
   disappears on every reset and every upload. Plain `arduino-cli monitor`
   treats that as end-of-session. `mon.ps1` waits and reattaches, which is the
   only reason one invocation can cover a whole debugging session.

4. **An open monitor owns the port and uploads fail against it.** There is no
   graceful sharing. Close the monitor with Ctrl+C, upload, reopen — or just
   use `flash.ps1`, which sequences it correctly and says so when an upload
   fails while a monitor is holding the port.

5. **Attaching to an already-running board shows no boot banner.** Everything
   printed from `setup()` is long gone, so a monitor that opens onto silence
   looks broken when it is fine. Press the board's Reset button, or upload
   again, to replay startup. If the sketch only prints during setup, this is
   the difference between "no output" and "working".

6. **PowerShell 5.1 mangles non-ASCII in BOM-less UTF-8 scripts.** It falls
   back to the ANSI codepage, so Korean, Japanese, and accented characters come
   out as mojibake — the script still runs, it just becomes unreadable. Save
   any `.ps1` containing non-ASCII as **UTF-8 with BOM**:

   ```powershell
   $utf8bom = New-Object System.Text.UTF8Encoding($true)
   $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
   [System.IO.File]::WriteAllText($path, $text, $utf8bom)
   ```

   The scripts here are pure ASCII and unaffected; this applies once someone
   translates the messages.

7. **`Serial.begin(115200); delay(3000);` before the first print.** USB CDC
   needs time to enumerate and early output is dropped without warning. A
   monitor that "misses the first lines" is usually this, not a monitor bug.

8. **The profile does not apply to already-open terminals.** After editing
   `$PROFILE`, `mon` stays undefined in the current window. Open a new terminal
   or run `. $PROFILE`. Also note `$PROFILE` differs between Windows PowerShell
   5.1 and PowerShell 7 — editing one leaves the other untouched.

## Files

| Path | Purpose |
|---|---|
| `scripts/Find-BoardPort.ps1` | vendor-ID port detection, dot-sourced by both scripts |
| `scripts/mon.ps1` | reconnecting monitor; `-Seconds N` makes it bounded |
| `scripts/flash.ps1` | compile + upload + monitor; `-NoMonitor` returns |
| `assets/profile_snippet.ps1` | `mon` / `flash` / `boards` shortcuts for `$PROFILE` |

Related: `xiao-esp32s3` for the compile/upload workflow and the pin map. Its
`read_serial.ps1` is the same bounded reader as `mon.ps1 -Seconds N`; use
whichever is already installed.
