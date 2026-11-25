---
name: chatgpt-sidebar-bridge
description: Drive the ChatGPT sidebar docked in Microsoft Edge with real OS-level mouse and keyboard input, attach files and long screenshots to it, and read the reply out of the sidebar's accessibility tree. Use when a task needs work from the user's own logged-in ChatGPT session through the browser UI instead of an API, when a user asks to type into ChatGPT, send it an image or a long screenshot, or read what it said, or when the sidebar bridge tooling needs running, extending, or debugging.
whenToUse: The user points at the ChatGPT sidebar/panel in Edge and wants the agent to talk to it; a task's material arrives as an image, a photo, or a long screenshot that ChatGPT itself must read; a task would benefit from a research, review, or writing answer produced by ChatGPT in the user's own browser session; or the work concerns simulated mouse and keyboard input into a browser-hosted chat UI, UI Automation targeting of a Chromium sidebar, or reading a chat transcript that has no API.
---

# ChatGPT sidebar bridge

Send prompts **and files** to the ChatGPT sidebar docked in Microsoft Edge and read the answer
back — using **real mouse movement, real clicks and real keystrokes**, not JavaScript injection,
not the network, and not an API key.

## Scope and authorization

This drives a browser the human is already signed into, on their own machine, with their own
account. Treat it as acting *as* the user toward a service they are entitled to use; it is not a
way to evade a service's controls, and it must not be pointed at an account that is not the user's.
Two operational consequences:

- **The machine is occupied while it runs.** Real input means the user cannot use the mouse or
  keyboard for those seconds. Keep prompts short and runs few.
- **Escape is the panic key.** Holding it aborts the run at the next event. Every run also carries
  wall-clock, event-count and cursor-distance caps, and restores the cursor when it finishes.

## Worked end to end

A real task: the user supplied one **640 × 8260 px** screenshot of an article and asked for a
1500-character rebuttal essay written entirely by ChatGPT. What was done, and what it produced:

| Step | Command | Evidence |
|---|---|---|
| Slice the long image | `python slice_task_image.py` | 6 slices of 640×1700, 100 px overlap |
| Attach them | `python -m dsh_chatgpt_bridge.cli attach-files` over an explicitly expanded file list | 6 attachments, count printed and verified by hand |
| Type the brief | `python sidebar_bridge.py ask --prompt-file task\brief.txt` | composer held 417 chars |
| Read the reply | (returned by `ask`) | 3869-character essay, titled, names the article's clownish parts |

## Delivering a long screenshot as material

**Why slicing is mandatory.** A chat UI downscales an image that tall until its text is
illegible, so the material must arrive as overlapping vertical slices that each survive
downscaling. `slice_task_image.py` cuts at 1700 px with 100 px overlap (long side under ~1.8k px).

**Getting files in through the real UI.** `attach-files` clicks the composer's *add* button
(`Add files and more`), clicks **Files and folders**, waits for the native Open dialog, clicks its
file-name field, types the quoted space-separated paths, and presses Enter. Four hard-won rules:

- **Batch the paths by length.** The dialog's file-name field **truncates near 256 characters,
  silently**. Six 64-character quoted paths (384 chars) produced exactly three attachments with no
  error shown. `--chunk-chars` (default 200) splits the list, and the tool reports the running
  attachment count per batch.
- **The dialog is invisible to UI Automation's top-level enumeration.** An owned modal dialog can
  be on screen and absent from `GetRootControl().GetChildren()`, which makes the tool click blind
  while the dialog swallows every click. Find it with Win32 `FindWindowW("#32770", …)` and wrap
  the handle with `ControlFromHandle` — that is what `find_dialog()` does.
- **The whole chain must run in one process.** Handing control back to the shell between steps
  lets focus move and the dialog is gone before it is filled in. This is why `attach-files` is a
  single command instead of four.
- **A dialog left open owns the screen.** `attach-files` detects an already-open dialog and fills
  it instead of clicking behind it. `fill-dialog` exists to finish one by hand.

## Composer traps, all observed

- **Enter sends.** A newline in a prompt must be typed as **Shift+Enter**. Before that was fixed,
  a four-paragraph brief fired off **four separate partial messages**, and ChatGPT answered each
  fragment. `type_text_plan(..., newline_sends=False)` is the default for exactly this reason.
- **A line starting with `N. ` autoformats into an ordered list and duplicates the marker.**
  Typing `4. 文风：…` lands in the composer as `4. 4. 文风：…`. Write prompts with labels such as
  `视角——…`, `文风——…` instead of numbered list syntax. The pre-send text check catches this.
- **The composer's value uses `\r\n`.** A raw substring test fails on any multi-line prompt even
  when the text is perfect; `normalize_for_compare()` flattens line endings and blank lines first.
- **Attachments grow the composer upward.** Its geometric centre then lands on a thumbnail, and
  clicking that opens the image preview and steals focus. Click the **text line** — `focus_point`
  is `bottom - 14`, not the centre.
- **Chromium announces completion into the transcript.** `Response complete: DONE` is ARIA
  live-region chatter and must be filtered or it lands in the extracted reply.
- **"The text changed" is not completion.** The first observable state of a reply is `Thinking`.
  `wait_for_reply()` requires a **new** `ChatGPT said:` block whose text has been stable for
  `--settle` seconds (default 3, use 5–6 for long writing).
- **The accessibility tree is built lazily.** The first query on a renderer returns frame chrome
  only; `locate_sidebar()` retries. The composer sits ~15 levels deep, so searches go to depth 20.

## Guards that must stay

1. **Focus is verified before typing.** `click_composer()` clicks, then confirms
   `GetFocusedControl()` is the composer or a descendant, retrying up to three times, and
   **aborts instead of typing** if it cannot. Without this, a missed click sprays keystrokes into
   whatever window does have focus — including the agent's own host application.
2. **The composer text is checked before Enter** by normalized containment (blank lines and
   surrounding whitespace are stripped; it is a substring test, not equality). If it does not
   match, the run aborts **before Enter** - but text may already be in the composer, because an
   abort is not a rollback. This is what caught both the newline-splitting bug and the
   list-marker duplication.
3. **Recovery exists.** `reset-composer` removes every attachment (`Remove <name>` buttons) and
   clears the text; `send --expect-file <path>` sends a message a previous run left sitting in the
   composer, re-verifying it first.

## Tooling

Everything lives in `dsh-ui-bridge/` in the workspace. Use the **base** interpreter, which has
`uiautomation` and `Pillow`:

```powershell
$py = "python"
Set-Location "."

& $py .\sidebar_bridge.py find                  # locate sidebar + composer (read-only)
& $py .\sidebar_bridge.py read                  # cleaned transcript (read-only)
& $py .\sidebar_bridge.py dump --depth 16       # the sidebar's UIA subtree

& $py .\slice_task_image.py                     # 640x8260 screenshot -> 6 readable slices
$files = (Get-ChildItem .\task\slice-0*.png | Sort-Object Name).FullName
& $py .\sidebar_bridge.py attach-files @files   # PowerShell does not expand the glob for a native program
& $py .\sidebar_bridge.py ask --prompt-file task\brief.txt --reply-timeout 540 --settle 6

& $py .\sidebar_bridge.py reset-composer        # recovery: drop attachments, clear text
& $py .\sidebar_bridge.py send --expect-file task\brief.txt
```

`ask` fails closed by design: it refuses to type without focus and refuses to send without a text
match. Exit code 2 means it aborted - but input caps or a late mismatch can be reached **after**
typing has started, so an abort does not guarantee the keyboard was untouched. Inspect the
composer and the conversation before retrying.

| File | Role |
|---|---|
| `sidebar_bridge.py` | `find` `dump` `read` `ask` `new-chat` `reset-composer` `send` `attach` `attach-files` `fill-dialog` `click` `type-keys` |
| `slice_task_image.py` | long screenshot → overlapping readable slices |
| `dump_window.py` | dump any top-level window's UIA subtree (native dialogs) |
| `recon_uia.py`, `recon_uia2.py`, `probe_sidebar.py` | how the sidebar was located |
| `inspect_windows.py`, `shot.py` | window enumeration and DPI-aware screenshots |
| `compare_composer.py` | diff the composer against an intended prompt, with the first differing index |

## Procedure for an image/material task

1. **Slice the material** if it is taller than ~2000 px, and check legibility by opening a slice.
2. **Start clean**: `new-chat` (if the control is missing, `reset-composer`).
3. **Attach** with `attach-files`, then confirm the reported attachment count equals the file count.
   Silently-short batches are the failure mode to watch for.
4. **Write the brief to a UTF-8 file** and pass `--prompt-file`. A file sidesteps shell quoting and
   console code pages for Chinese text, and it is the text the pre-send check compares against.
   Avoid `N. ` at line starts.
5. **Ask**, then read. Report the answer, naming ChatGPT as the source and the model the sidebar
   shows.

## Verification

```powershell
$py = "python"
Set-Location "."
& $py .\sidebar_bridge.py ask "Reply with just the word: DONE"     # expect: DONE
& $py .\sidebar_bridge.py read                                      # transcript contains it
```

A green run prints the composer focus line, the post-typing character count, `sent (Enter)`, then
the reply. `ABORTED: …` means the run stopped, **not** that nothing happened: text may already be
in the composer and attachments may already be uploaded. Read the reason, inspect the
conversation, and use `send --expect-file` only if what survived is what you intended.

## Related

This skill is the **tool reference**. Two companions carry the discipline and the order:

- `chatgpt-sidebar-delivery` — the gated, ordered pipeline (G0 preconditions → G0.5 smoke test →
  G1 material → G2 fresh state → G3 attach → G4 brief → G5 send → G6 read → G7 verify → G8 report).
  **Follow it for any real delivery.** Every gate asserts and stops rather than warning.
- `gui-input-hard-rules` — the twenty hard rules (H-01 … H-20) for driving any GUI with simulated
  input and accessibility reading, each derived from a recorded failure.
- `dsh-ui-bridge/POSTMORTEM.md` — the postmortem behind both: twelve mistakes with evidence, and the
  six classes of repeated work that cost the most.
- `humanized-input-lab` — the timing engine this borrows (minimum-jerk trajectories, log-normal key
  intervals) with typo injection disabled.

Installed into the custom presets `router-planner`, `ml-planner` and `fem-ml-planner`.

## Where this skill sits

The **tool reference**: commands, parameters, file layout. Use `chatgpt-sidebar-delivery` for the
ordered process and `gui-input-hard-rules` for the discipline.


---

## Toolchain internals (lowest layer)

Everything the layers above assume, as concrete mechanism. Enough to reimplement without this code.

### Aiming — UI Automation

| Fact | Value |
|---|---|
| Browser window | top-level window whose title contains `Edge` |
| Sidebar pane | `ClassName == "SidePaneRootContainer"` (also: `SidePaneRootContainerBackground`, `MainView`, `SidePaneHeaderView`) |
| Web content host | `Chrome_RenderWidgetHostHWND` → `DocumentControl` |
| Composer | the `EditControl` under the pane; search depth **20** (it sits ~15 levels down) |
| Attachment chips | `ButtonControl` named `Remove <filename>`; thumbnails are 80×80 |
| Add button | `ButtonControl` named `Add files and more` |
| Native dialog | Win32 class `#32770`; **not** reliably present in the UIA top-level enumeration |
| File-name field | the `EditControl` with `AutomationId == "1148"` |

Chromium builds the accessibility tree **lazily**: the first query on a renderer returns frame chrome
only. Every lookup therefore retries (`locate_sidebar` 4×, `page_document` 6×, ~0.7 s apart).

### Acting — `SendInput`

```python
INPUT_MOUSE = 0; INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001; MOUSEEVENTF_ABSOLUTE = 0x8000; MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_LEFTDOWN = 0x0002; MOUSEEVENTF_LEFTUP = 0x0004
KEYEVENTF_KEYUP = 0x0002; KEYEVENTF_UNICODE = 0x0004
SM_XVIRTUALSCREEN = 76; SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78; SM_CYVIRTUALSCREEN = 79
VK_BACK = 0x08; VK_RETURN = 0x0D; VK_ESCAPE = 0x1B; VK_SHIFT = 0x10; VK_CONTROL = 0x11
VK_A = 0x41; VK_L = 0x4C; VK_V = 0x56
```

- Mouse: `MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK`, with
  `dx = round((x - vx) * 65535 / (vw - 1))` and likewise for `dy` over the **virtual** screen metrics.
- Text: `KEYEVENTF_UNICODE` with `wVk = 0` and `wScan = <utf-16 code unit>`, then the same with
  `KEYEVENTF_UNICODE | KEYEVENTF_KEYUP`. Non-BMP characters are sent as surrogate pairs.
- Special keys: virtual-key codes. Combinations are sent as explicit press/release around the key.
- `ULONG_PTR` is `c_uint64` on 64-bit, `c_uint32` on 32-bit — the struct layout is wrong otherwise.
- The process calls `SetProcessDpiAwareness(2)` (per-monitor aware) so UIA rectangles, screenshots
  and click coordinates agree.

### Guards (order matters)

1. before **every** emission: panic key (`GetAsyncKeyState(VK_ESCAPE) & 0x8000`), wall-clock,
   event count, cumulative cursor distance → `InputAborted`;
2. before **typing**: `GetFocusedControl()` must be the composer or a descendant, up to 3 click
   retries, then abort — never type blind;
3. before **Enter**: `normalize_for_compare(prompt) in normalize_for_compare(composer_value)`,
   otherwise abort without sending;
4. after **every** batch: assert the attachment count read from `Remove …` buttons.

`normalize_for_compare` flattens `\r\n` → `\n`, drops blank lines and strips each line, because
Chromium's `EditControl` returns CRLF where the prompt had LF.

### Timing

With `hilab` importable (`HILAB_ROOT`): `plan_move(start, end, target_width, MotionParams(), rng,
cadence_hz=60)` yields `(t, x, y)` samples — minimum-jerk with optional overshoot + correction — and
`plan_typing(text, TypingParams(typo_rate=0.0), rng)` yields `KeyStep(key, t_down, t_up)`.
Without it: a minimum-jerk arc at 60 Hz and log-normal intervals (`lognormvariate(-3.2, 0.35)`).
Newlines become **Shift+Enter** (`newline_sends=False` by default).

### Reading

`transcript_text` walks the `DocumentControl` to depth 16 collecting `TextControl` / `EditControl`
names in tree order, dropping chrome (`Do anything`, `New chat`, `No chats in progress`, `Thinking`,
`Copy`, `Good response`, `Bad response`, `Regenerate`, `Acknowledge request`, `Send`, `Stop`,
`Search`), timestamps (`^\d{1,2}:\d{2}(\s*(AM|PM))?$`) and Chromium's ARIA announcements
(`^response (complete|finished)|message sent|stopped|chatgpt is typing|loading`).

`extract_reply` takes the text after the **last** `ChatGPT said:` marker.
`wait_for_reply` polls every 0.6 s and returns only when the transcript contains a **new**
`ChatGPT said:` block whose text has been unchanged for `--settle` seconds (default 3, use 5–6 for
long writing) and at least `min_wait_s` has passed — because the first observable state of a reply is
the placeholder `Thinking`.

### Transport of files into the dialog

Quoted, space-separated paths are typed into `#32770`'s file-name field and accepted with Enter. The
field **truncates near 256 characters without an error**, so paths are grouped by
`sum(len(path) + 3) <= chunk_chars` (default 200). Six 64-character paths → three batches of two.


---

## Clipboard and mouse buttons — what was actually verified

Three capabilities were requested and tested on a live desktop. Results, with the evidence:

### Clipboard round trip — works

```
$essay = Get-Content essay.txt -Raw; Set-Clipboard -Value $essay
$back  = Get-Clipboard -Raw
written chars: 1034      read-back chars: 1034      round-trip identical: True
```

Text is written with PowerShell's `Set-Clipboard` and read with `Get-Clipboard -Raw`. The base
interpreter has no `win32clipboard`, and one shell call beats adding a dependency for a two-way copy.
Line endings come back as CRLF, so any comparison must normalise first
(`normalize_for_compare`).

### Paste into the composer — works, and it is the preferred transport

```
$ dsh-chatgpt-bridge paste --expect-file essay.txt --send
composer focused after click #1
composer holds 1025 chars and 0 attachment(s)
pasted content verified against essay.txt (1033 chars expected)
sent (Enter)
```

`paste` focuses the composer, sends Ctrl+V, then **compares what landed against the source file**
before sending. Pasting avoids the entire family of composer traps at once: no newline can be
mistaken for Enter, and no line-start pattern can be autoformatted into a list. For payloads of a few
thousand characters it is also the only sane transport — a 1034-character essay arrives instantly
instead of after ~90 s of typing.

### Left button — works (and is the basis of every other operation)

`click_composer` left-clicks the composer's text line and confirms via `GetFocusedControl()` that the
composer (or a descendant) holds focus, retrying three times before aborting. Every successful
`ask` / `paste` run begins with that confirmation, so left-button control is exercised constantly.

### Right button — works at the OS level; the chat composer shows no menu

| Target | Result |
|---|---|
| Taskbar | **menu appeared** — `Microsoft Teams 的跳转列表`, class `Windows.UI.Core.CoreWindow`, 318×93 at (781,939) |
| Edge page area | no top-level menu window |
| ChatGPT sidebar composer | no top-level menu window |

The raw event is definitely delivered: `GetAsyncKeyState(VK_RBUTTON)` is set immediately after the
right-down is emitted.

**The lesson is about detection, not emission.** The first attempts reported "no menu" because the
check looked only for the classic Win32 menu class `#32768`. Real menus on this system use other
classes — XAML jump lists are `Windows.UI.Core.CoreWindow`, and Chromium draws its own menus in a
`Chrome_WidgetWin_1` popup — so menu detection must diff the **set of top-level windows**, not test
for one class name. `top_level_handles()` exists for exactly that.

**Right-click is therefore usable for browser-level menus** (tab context menus, the page context
menu, taskbar jump lists). The ChatGPT composer does not raise a top-level menu, so the clipboard
route plus Ctrl+V remains the way to move text into it.


---

## Console work (GitHub and similar) — three rules added after live failures

Working a web console (GitHub: rename, About, topics, uploading a directory) uses
`gh.py` alongside this tool, and adds three rules:

1. **Open a new tab first.** `Ctrl+T`, then navigate in that tab. Driving the active tab with
   `Ctrl+L` replaces the page the human is using — which is exactly what happened here, repeatedly.
2. **Prefer clickable controls when names collide.** "Commit changes" exists as both a
   `ButtonControl` and a `TextControl`; clicking the label does nothing.
3. **Verify on the server.** For a public GitHub repo:

```powershell
$repo = "<owner>/<repo>"
Invoke-RestMethod "https://api.github.com/repos/$repo" | Select-Object pushed_at
(Invoke-RestMethod "https://api.github.com/repos/$repo/git/trees/main?recursive=1").tree |
    Where-Object type -eq blob | Select-Object path, size
```

   Compare that list against the local directory before believing an upload succeeded.
