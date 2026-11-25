---
name: windows-ui-automation
description: Drive and screenshot native Windows apps from PowerShell - window/control tree, MSAA+UIA accessibility, real mouse/keyboard, message-level control, occlusion rescue, Set-of-Marks screenshots, batch steps. Use for GUI debugging, verification, or scripted UI automation (Win32/WPF/Qt/UWP/Electron).
metadata:
  short-description: PowerShell UI automation for Windows apps (self-contained)
---

# Windows UI Automation

Pure PowerShell + P/Invoke, no dependencies, no installs: runs on the inbox Windows PowerShell 5.1 and on
PowerShell 7 (`pwsh`). Examples use `pwsh`; substitute `powershell -NoProfile -ExecutionPolicy Bypass -File`
where 7 is absent or policy blocks scripts (UIA and screenshots work on both).

```powershell
$ui = "$env:USERPROFILE\.codex\skills\windows-ui-automation\scripts\ui.ps1"
pwsh -File $ui selftest                            # self-check
pwsh -File $ui windows -Visible                    # list windows -> note the Handle
pwsh -File $ui tree -Window <handle>               # control tree with control IDs
pwsh -File $ui som -Window <handle> -Out shot.png  # numbered screenshot + marks table (full resolution)
pwsh -File $ui look -Path shot.png -Ask "is the Send button enabled?"   # read it; the file is gone
pwsh -File $ui somclick -Window <handle> -Index 3  # click mark 3 (-PreferAction: no mouse)
pwsh -File $ui steps -Window <handle> -Do "activate|type:hello|key:ENTER|shot:C:\temp\a.png"
```

## Commands

`windows` `tree` `marks` `som` `somclick` `click` `type` `typein` `key` `drag` `wheel` `set` `cmd` `shot`
`look` `cleanup` `budget` `wait` `uia` `msaa` `msaaaction` `decide` `steps` `focus` `activate` `state`
`reveal` `occluders` `restore` `taskbar` `searchapp`. Full table with parameters (keeps this file small):
`pwsh -File <path>\ui.ps1 help`.
`steps` vocabulary: `win: winh: activate click: msgclick: dblclick: rclick: clicktext: clickxy: type: paste:
key: set: check: combo: tab: cmd: drag: wheel: move: wait: waitwin: waittext: uia: shot: log:`
(`-Force` reaches every step that types or clicks.)

## Real input vs API calls

- **Real input** (`click`, `type`, `typein`, `key`, `drag`, `wheel`, `steps`): actual mouse and keyboard -
  identical to a human, works even without accessibility, but moves the cursor, steals focus and is slower.
- **API-level** (`-Message`, `msgclick`, `set`, `cmd`, `uia invoke`, `msaaaction`, `-PreferAction`, window
  `move`/`state`/`topmost`): posts messages or accessibility actions - no cursor, no focus change, faster and
  safer, but it skips real event handling and some apps ignore it. It is gated by the same safety rules as
  real input.
- Choose per case; **when the point is to prove the UI itself works** (interaction/design verification, "does
  this click fire", visual QA, an exact human replica) real input is mandatory.

## Rules

**User instruction wins over everything else**: "no UI" means no UI at all (neither engine); "use UI" means
pick the best of the two; naming one engine means use only that one; with no explicit instruction, choose what
works best.

1. **UI only when needed.** Run `decide` first; prefer any more reliable CLI/API/file channel.
2. **Elements first, coordinates last.** Take indices from `som`/`marks`, then `somclick -Index n`; a real
   click verifies the landing point and aborts instead of hitting whatever covers it.
3. **Occlusion rescue.** `reveal`: raise -> minimise blockers -> move blockers -> taskbar switch -> close
   session-created blockers -> Start Menu / Desktop / UWP search. Occluded screenshots use a temporary topmost
   grab that does not steal focus.
4. **Typing uses the clipboard by default** (bypasses IME interference); `-Raw` types character by character;
   `typein` makes the window foreground and focused first.
5. **Safety.** Every input - real and message-level alike - is gated by language-independent rules (process,
   window class, loader command line, control-panel CLSID): terminals, consoles, security & credential UI,
   password managers and the Codex window are refused on any Windows UI language, and writing into an existing
   user document needs `-Force` (which never unlocks the hard categories). Keys are checked against the focused
   window, raw coordinates against the point's owner (the target is raised and re-checked first) - keys land in
   whatever has focus, so activate a safe target first (the app, or the desktop/shell for shortcuts such as
   `WIN+D`). Touch only windows you launched or the user named; never save, delete or send anything.
6. **Launch an app the way a human would.** Desktop shortcut first: search `%USERPROFILE%\Desktop` and
   `%PUBLIC%\Desktop`; if one exists, show the desktop (`WIN+D`; the taskbar corner hot spot may be disabled)
   and double-click the icon with the real mouse. Otherwise use the Start menu / Start search / UWP list
   (`searchapp`, `Start-UiFromShortcut`), and only then a raw path or URL (`open`).
   Do not hand-roll this: `scripts/desktop-launch.ps1 launch "<name>"` resolves the icon, proves the landing
   point, double-clicks it and confirms a window appeared (`verify` only measures, `-DryRun` skips the click).
   Enumerate and click from the *same* DPI-aware process - mixing an unaware enumeration with an aware click is
   what makes a double-click land on the wrong icon.

## Gotchas

- Measure -> act -> read back in one step; re-measure after any state change (layouts shift; a stray window
  taking focus lands the input elsewhere) and verify the effect on screen, not just that the call returned.
- Desktop icons show up only through MSAA on the desktop `SysListView32` (nested under `WorkerW`: search
  descendants, not children); the desktop cannot be raised (Progman stays at the bottom of the Z order), so
  `WIN+D` is the reliable "show desktop".
- Chromium/Electron apps often publish no accessibility tree (`som` returns one element): use a 1:1 screenshot,
  read the position, real click/drag, read the screen back.
- Packaged apps (Windows 11 Notepad, UWP) create their window from a second process; `open` matches process
  name plus a handle that did not exist before the launch, so it still finds the real window.
- Scripting the library directly: dot-source `uikit.ps1` and call `Initialize-UiKit` first - coordinates are
  physical pixels only for a DPI-aware process. The wrappers in `scripts/` do the same, in one process.

## Reading the screen without blowing up the request body

Every image the model reads is stored in the conversation and re-sent **byte for byte on every later request**,
so the body only grows. DeepSeek's gateway (openresty) buffers that body and rejects anything above ~50 MB
(measured boundary: 48 MiB accepted, 51 MB rejected) with

```
413 Payload Too Large: Failed to buffer the request body: length limit exceeded
```

which ends the run for good: the history never shrinks, deleting the file from disk does not undo it, and only a
fresh thread can continue from the artefacts on disk - say so afterwards instead of stopping to ask. This engine
therefore never puts a capture into the conversation, the way native Computer Use keeps screenshots in its
harness and gives the model observations only:

- **Capture**: `shot`, `som` and the `shot:` step always grab the **full-resolution** frame - never cropped,
  downscaled or re-encoded (`-MaxWidth` shrinks only when a caller asks for that on purpose) - and print the
  exact read command for the file.
- **Read: `look`, always.** `look -Path <png> -Ask "<question>"` hands the full-resolution file to a throw-away
  Codex run (`--ephemeral`: it persists no session) and brings back **text only**. A UI capture is never opened
  with `view_image`.
- **Delete the moment the read is over.** `look` deletes its own picture, on success and on failure alike; for a
  capture answered any other way (a `som` whose marks table already replied) use `cleanup -Path <png>`. Nothing
  is deleted by age, and nothing is kept unless the user - or the run itself - says so with `-Keep`: hold only
  what is unread and re-shoot instead of hoarding stale frames.
- **Nothing stale in the working memory.** A kept capture is a screen that no longer exists, still competing for
  attention; reading out of band keeps the session's picture in step with the window actually being driven.
- **Text channels first.** `tree`, `marks -Json`, `uia text` / `uia value`, `msaa` and `list` often answer the
  question outright - no picture, no read, no round trip. A failed read falls back to such a channel or a fresh
  capture, a call the agent makes itself rather than stopping to ask the user.
- `budget` prints the live conversation size (since the last compaction) and every shot still on disk, so a long
  run can check itself; the DeepSeek catalog also compacts on its own at 200k tokens
  (`auto_compact_token_limit` in `~/.codex/models.json`).

## Speed

1. **Uploading the body** is what makes UI work slow: every turn re-sends the whole conversation at roughly
   1.3 MB/s here (48 MB ~ 36 s, 5 MB ~ 4 s per turn). No picture ever joins it: each capture goes through
   `look` and is deleted the moment the read is over, which keeps the body flat.
2. **Round-trips per action** - one `pwsh -File` process per command costs ~0.5 s of startup (the P/Invoke
   helpers compile once and are cached as DLLs under `%TEMP%\codex-uia\asm`, ~20 ms afterwards, shared by the
   wrappers too). Batch with
   `steps -Do "activate|click:<id>|type:...|key:ENTER|shot:out.png"` and read state with `marks -Json` /
   `uia value` instead of taking another screenshot.
3. **Capture cost** - `shot` encodes the frame once, `som` annotates and encodes in one pass, `-Region` crops
   instead of scaling.

## Model fit

Built and debugged with **DeepSeek-V4.1**; other models are neither excluded nor recommended - the engine is
tuned to that model's habits. On a **DeepSeek model with native vision this is the preferred channel**.

With Computer Use (`@oai/sky`) on **GPT-series models**: prefer the built-in plugin, and split the work -
element-level actions there (accessibility indices), window-level and physical input, message-level control,
batch steps, logging, safety gates and visual grounding here. **Never mix both input paths inside one turn**
(Computer Use policy); switch per turn. When Computer Use is unavailable, clearly times out or underperforms
(elements missing, clicks missing, state unreadable), this engine takes over the whole flow, and switching back
later is allowed. An explicit user instruction outranks every preference (see Rules).

## Files

`scripts/`: `uikit.ps1` (core), `ui.ps1` (CLI), plus thin wrappers `real-input.ps1`, `drive-controls.ps1`,
`capture-window.ps1`, `list-windows.ps1`, `desktop-launch.ps1` (desktop-first launch with a verified landing
point). Logs: `%TEMP%\codex-uia\YYYYMMDD.jsonl`; marks: `%TEMP%\codex-uia\marks-<handle>.json`.

Keep this package to universal behaviour only: no task-specific recipes, screenshots, sample data or test
records - those belong to the task at hand and are added only when the user asks for them.
