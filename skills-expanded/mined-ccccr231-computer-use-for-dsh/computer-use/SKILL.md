---
name: computer-use
description: Drive a Windows desktop GUI directly — screenshot for evidence, enumerate windows, read the UI element tree with exact click coordinates, move and click the mouse, type text and send shortcuts, read/write the clipboard. Use when the user asks to operate their computer, click something, type into an application, watch an on-screen process, or automate an interface-only task. Not for pure CLI, file, or network work — plain tools are faster and more reliable there.
---

# computer use for DSH

Drive a Windows machine through `scripts/gui.ps1`: observe the screen, locate elements, click, type, and leave a screenshot behind at every step.

## How to run it

```powershell
$sc = "<path-to-skill>\scripts\gui.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $sc -Action screen
```

The `-ExecutionPolicy Bypass` wrapper is mandatory. Invoking `& $sc` directly fails with `running scripts is disabled on this system`.

### Three constraints that are not optional

1. **DPI awareness is set first, inside the script.** On a scaled display, an unaware process faces two coordinate systems: UI Automation returns physical pixels while the mouse is clamped to logical pixels. Clicks then land far off target, or are clamped to the screen edge — with no error reported. The script declares `Per-Monitor-Aware V2` before any UIA / screenshot / mouse call. Do not insert code ahead of it that resets the DPI context.

2. **Keep `gui.ps1` pure ASCII.** Windows PowerShell 5.1 reads a BOM-less `.ps1` as ANSI (the system code page), so non-ASCII source characters corrupt the parser and produce misleading syntax errors. Non-ASCII text (window titles, element names, typed content) must arrive as runtime data through `-Title` / `-Text`; that path is UTF-8 safe. Bilingual documentation belongs in `README.md`, not in the script.

3. **Re-verify after every edit.** Parser errors only surface at runtime; reading the code is not enough. Run the bundled verifier, which checks encoding, syntax, live actions and coordinate alignment in one pass:
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\verify.ps1
   ```
   Exit code `0` means all checks passed.

## Workflow: observe -> locate -> act -> verify

### 1. Observe

```powershell
-Action screen                            # resolution, DPI mode, scale, cursor, foreground window
-Action windows                           # top-level windows: title, handle, rect, visible
-Action elements -Title "Notepad" -Limit 40
```

**`elements` is the primary perception channel.** It returns each element's `click` coordinate (the center of its bounding rectangle) ready to be passed to `click`.

Always check `visible` before acting on an element. An element whose `click` is `null` and whose `visible` is `false` is not on screen — clicking it is meaningless. This happens most often when the target window is minimized: the window's UIA tree survives, but its coordinates fall far outside the physical screen. Elements inside a minimized window are skipped when interactive, and otherwise reported with a null click point.

If the running model cannot accept image input, do not try to understand the UI from screenshots — they are for the human. Use `elements` for coordinates and `at` for confirmation. Attempting to read a PNG reveals whether image input is supported; when it is not, stay entirely on the element-tree path.

### 2. Locate and confirm

```powershell
-Action at -X 1625 -Y 980
```

`at` is what prevents mis-clicks: confirm the target before acting, confirm the hit after. Returns `{name, type, rect, window}`.

### 3. Act

```powershell
-Action focus  -Title "Notepad"          # restore + raise, reports is_foreground
-Action click  -X 1625 -Y 980            # also -Right 1, -Double 1
-Action move   -X 100 -Y 100
-Action type   -Text "content"           # clipboard + Ctrl+V, CJK safe
-Action keys   -Keys "^s"                # SendKeys: ^ Ctrl, % Alt, + Shift
-Action wait   -Ms 800
-Action clipboard-get
-Action clipboard-set -Text "..."
-Action screenshot -Width 1600 [-X -Y]
```

Target windows with `-Handle` (exact) or `-Title` (fuzzy). Prefer `-Handle`: fuzzy titles are ambiguous when several windows share a prefix.

### 4. Verify

`click`, `type`, `keys`, `invoke` and `select` each save a screenshot automatically and return its path. Click screenshots draw a red ring and crosshair over the landing point; `invoke` / `select` mark the target element's center.

Do not treat a screenshot as proof. **Read the real state back**: wrote a file? read the file. Submitted a form? query the list. Changed a setting? re-run `elements` and check the value. A screenshot proves you clicked; reading state back proves it worked.

## Showing the human what happened

When the user asked to watch the process:

- Report the **target element name, landing coordinate, and action type** for every step rather than a bare "done".
- Give the screenshot path so the user can open it directly.
- For flows longer than about three steps, state the plan first, then execute and report step by step.
- On failure, report the **actual state** rather than a vague failure: `is_foreground`, what `at` returned, whether the coordinate was clamped.

## Safety boundaries

This capability changes real desktop state. Hold to these rules:

- **Look before acting.** Confirm the target with `elements` or `at` before every click or keystroke. Guessed coordinates hit unknown buttons.
- **Minimize side effects.** When testing or demonstrating, use an application you started and a dedicated file. Never use a document the user is actively editing as a target.
- **Confirm irreversible actions.** Deleting, sending, paying, submitting, closing an unsaved window, overwriting files — state what is about to happen and get agreement first.
- **Stop on sensitive content.** The element tree can incidentally expose secrets: API-key-shaped strings in tab titles, text adjacent to password fields, notification bodies. Do not repeat, record, or write such content anywhere. Skip it, and at most tell the user that some window contains sensitive data.
- **Never close the user's processes or windows.** Clean up only what you started.
- **The foreground window and clipboard are shared resources.** `type` restores the previous clipboard contents, but only if they were plain text — an image or file list on the clipboard is lost. It also displaces the user. Return focus to their original window when finished.
- **Clipboard actions can fail transiently.** The clipboard is a global single-owner resource; any process may hold it. `clipboard-get` / `clipboard-set` / `type` retry briefly and then return `{"ok":false,"error":"clipboard is locked by another process"}`. Treat that as retry-later, not as a bug — and do not loop on it indefinitely.

## Action reference

| Action | Key arguments | Purpose |
|---|---|---|
| `help` | — | Print the action list |
| `screen` | — | Resolution, DPI mode, scale, cursor, foreground window |
| `windows` | — | Top-level windows (handle / rect / visible) |
| `elements` | `-Title` / `-Handle`, `-Limit` | Element tree with click coordinates (**primary perception channel**) |
| `at` | `-X -Y` | Element at a point (mis-click guard) |
| `invoke` | `-Name`, `-Title` / `-Handle` | Activate a named element via its UIA pattern, tried as `InvokePattern` -> `TogglePattern` -> `SelectionItemPattern` -> `ExpandCollapsePattern` -> `LegacyIAccessiblePattern`. More reliable than clicking a coordinate |
| `select` | `-Name`, `-Title` / `-Handle` | Selection semantics: `SelectionItemPattern` -> `TogglePattern` -> `LegacyIAccessiblePattern`. Selecting what is already selected is a no-op, not a toggle-off |
| `click` | `-X -Y`, `-Right` / `-Double` | Mouse click, auto-screenshot |
| `move` | `-X -Y` | Move the cursor |
| `focus` | `-Title` / `-Handle` | Restore + raise a window, reports `is_foreground` |
| `window-info` | `-Title` / `-Handle` | Window rect, center, owning process |
| `type` | `-Text` | Type text (CJK safe) |
| `keys` | `-Keys` | Shortcuts and special keys |
| `screenshot` | `-Width`, `-X -Y` | Full screenshot, optional action marker |
| `clipboard-get` / `-set` | `-Text` | Clipboard read / write |
| `wait` | `-Ms` | Wait for the UI to settle |

## Verified behaviours worth knowing

- `invoke` / `select` report `pattern` and `state_after`. The state is re-read after the call, so verify against that rather than assuming the action landed. `scrolled_into_view` says whether `ScrollItemPattern` had to bring the element into view first, and `note` records a deliberate no-op such as "already on; no change made".
- `LegacyIAccessiblePattern` does not exist in the UI Automation wrapper shipped with Windows PowerShell 5.1: referencing the type directly aborts the action with `Unable to find type`. The driver resolves it by name and skips that fallback where the runtime lacks it. Controls that reach UIA only through the MSAA bridge - WinForms is the common case - therefore expose no usable pattern, and `invoke` / `select` return `{"ok":false,...,"tried":[...]}`; fall back to reading `elements` and clicking the coordinate inside the same invocation. WPF and modern Windows apps such as Notepad expose the real patterns and work.
- Element names are matched exactly first, then by substring, and on-screen elements are preferred over off-screen ones carrying the same name. When a name is ambiguous, pass `-Handle` and use the most specific name you can read from `elements`.

- `Add-Type -AssemblyName WindowsBase` is the source of `System.Windows.Point`. Without it, `at` fails with `Cannot find type [System.Windows.Point]` (the script loads it).
- A minimized window reports an empty UIA `BoundingRectangle` from `window-info`/`windows`, while `GetWindowRect` returns a plausible-looking size parked at `-32000`. Both cases must be detected; size alone is not a reliable visibility signal (the script handles both).
- Elements inside a minimized window are the nastier case: they keep a plausible size but report coordinates far outside the screen (measured at roughly `-47865,-47952`), and their `IsOffscreen` stays `False`. Visibility is therefore derived from geometry against the physical screen bounds, not from `IsOffscreen` or `IsWindowVisible`.
- `windows` reports a `minimized` field, because `IsWindowVisible` stays `True` for a minimized window.
- A minimized or occluded window cannot be clicked. Call `focus` and confirm `is_foreground: true` first.
- Screen scale must be read from `GetDeviceCaps(LOGPIXELSX)`. Comparing `Screen.Bounds` to `GetSystemMetrics` returns 1.0 even at 150% scaling, because both report the physical size once the process is per-monitor aware.
- `Set-Clipboard` intermittently throws `Requested Clipboard operation did not succeed` when another process holds the clipboard. Every clipboard path retries and degrades to a JSON error rather than terminating the action.
- Multi-tab editors list every tab in `elements`, so scope input to the intended tab.
- Do not assert on the cursor position after `SetCursorPos` on a busy desktop: other software can move the pointer between the set and the read, so such a check fails at random. `verify.ps1` reports this probe as advisory for that reason, and relies on the `dpi_mode` report instead.
- **Coordinate clicks are far more fragile than they look.** Measured in one session: a click aimed at (599,31) landed at (660,81) because the window had moved between reading and clicking, hit an "NVIDIA GeForce Overlay" pane, and dropped focus to the desktop. Consequences: read the coordinate and click it inside the SAME invocation rather than across invocations; re-read coordinates after any window move; and prefer `invoke` / `select` for anything with a name.
- **Web content commonly lives inside a `Chrome Legacy Window` element.** `-Action at` reports that as the containing window rather than the browser frame. Served buttons are visible to UIA through it, but the tree can also contain hidden elements from other tabs, or the DOM of a different application rendering in the same browser window. Confirm that `elements` output actually belongs to the page you intend before acting on it.
- **A browser that hosts the agent's own UI will fight you for focus.** When the agent's chat interface and the target page are tabs of the same browser window, raising the chat tab sends keystrokes and clicks to the wrong page. Verified symptoms: `foreground` flips back to the chat tab immediately after a key is sent, and `elements` returns the chat UI's DOM instead of the target page. Mitigation: focus the target window and act within a single invocation, and verify page identity (a known button name present, the chat UI's own elements absent) before every action.
- **Never answer a real assessment, medical or psychological form on the user's behalf.** Driving the UI is in scope; inventing the answers is not. Offer to read the questions aloud, explain their meaning, and click the choices the user dictates. An answer the agent made up is not the user's answer, and on a named, archived institutional form it is a fabricated record about a real person.
- **Scope every read to the target region before reading anything.** `elements` returns the WHOLE window, and in a chat or mail client that means every conversation title, sender name, preview line and timestamp the user has. Verified failure: a filter sorted by Y instead of restricting X, so the entire conversation sidebar was pulled in and unrelated group names and message text were surfaced into the chat. Rules that follow: restrict by the target region's coordinates before touching content; never repeat, quote, log or write out content from any conversation that is not the one the user asked about; and when reporting verification, report structure (how many entries, whether one was added) rather than text. If unrelated sensitive content appears anyway — a password-shaped string, a token — say only that something sensitive is present and advise removing it, without reproducing it.
