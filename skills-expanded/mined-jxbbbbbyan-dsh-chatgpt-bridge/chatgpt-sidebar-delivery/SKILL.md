---
name: chatgpt-sidebar-delivery
description: The gated, ordered pipeline for delivering a task to the ChatGPT sidebar in Edge with real mouse and keyboard input, from raw material (including long screenshots) through to a verified deliverable. Use when a user wants ChatGPT to produce something and the material must reach it through the browser UI, when a delivery attempt has already gone wrong and needs recovering, or when the process itself must be repeated reliably.
whenToUse: A user hands over material (text, an image, a long screenshot, a document) and wants ChatGPT to work on it in their own logged-in session; a previous attempt produced fragmented messages, polluted the composer, or half-attached the files; or the same delivery has to be run again and must not repeat earlier mistakes.
---

# ChatGPT sidebar delivery

A fixed sequence of gates. **Every gate asserts its exit condition, and a failed assertion stops the
run** — it is never downgraded to a warning. The rules behind the assertions are in
`gui-input-hard-rules`; the commands are in `chatgpt-sidebar-bridge`.

**Non-negotiable:** never build the next phase on state you have not verified. Every incident in the
postmortem came from continuing past an unverified assumption.

---

## G0 — Preconditions

| | |
|---|---|
| **Entry** | A task and its material exist. |
| **Do** | `sidebar_bridge.py find`. Confirm a sidebar pane, a document, and a composer rect are all reported. Check for a leftover modal and a non-empty composer. |
| **Exit assertion** | `find` prints a composer rect; no `#32770` dialog is on screen. |
| **If it fails** | Sidebar closed → say so, do not click blind. Dialog present → `fill-dialog` it or cancel it. Composer dirty → `reset-composer`. |

## G0.5 — Smoke test (never skip)

| | |
|---|---|
| **Do** | Run one three-line throwaway prompt through the whole chain: aim, click, focus check, type, commit, wait, read. |
| **Exit assertion** | The reply is read back correctly and exactly one message appears in the transcript. |
| **Why** | This is where the newline bug, the `\r\n` compare bug and the autoformat bug would each have been caught for ~1 % of the cost. The real task ran about six times because this gate was skipped. |

## G1 — Material

| | |
|---|---|
| **Do** | For any image taller than ~2000 px: slice it (`slice_task_image.py`, 1700 px slices, 100 px overlap) and open one slice to confirm the text is legible after downscaling. |
| **Exit assertion** | The slice count and the on-screen legibility are both confirmed. |
| **Why slicing** | A chat UI downscales a 640 × 8260 image until the text cannot be read at all. |

## G2 — Fresh state

| | |
|---|---|
| **Do** | `new-chat`. Then re-read the state. |
| **Exit assertion** | Attachment count is 0 **and** the transcript has no assistant message. |
| **If it fails** | `reset-composer`, re-assert. If it still fails, **stop and report** — do not attach into a dirty chat. *Incident:* this gate was reduced to a printed warning once, and the composer went from 6 to 12 attachments. |

## G3 — Attach

| | |
|---|---|
| **Do** | `attach-files <paths>` with the default character-bounded batching. |
| **Exit assertion** | The reported attachment count equals the number of files. |
| **If it fails** | A short count means the dialog's file-name field truncated: lower `--chunk-chars` and retry once. If it still mismatches, `reset-composer` and stop — never send with a partial material set. |
| **Why** | The field truncates near 256 characters **silently**; six paths yielded three attachments with no error. |

## G4 — Brief

| | |
|---|---|
| **Do** | Write the brief to a UTF-8 file and pass `--prompt-file`. Avoid `N. ` at line starts (autoformats into a list and duplicates the marker). The reader strips trailing whitespace. Dry-run with `ask --dry-run` if the trajectory matters. |
| **Exit assertion** | The file has no line beginning with a digit-plus-period, and no trailing blank line. |
| **Why a file** | It sidesteps shell quoting and console code pages for CJK text, and it is the exact text the pre-send check compares against. |

## G5 — Send

| | |
|---|---|
| **Do** | `ask --prompt-file <brief> --reply-timeout 540 --settle 6`. Newlines are typed as Shift+Enter. |
| **Exit assertion** | Console prints the focus confirmation, the post-typing character count, and `sent (Enter)`. |
| **If it prints `ABORTED`** | Nothing was typed or sent. Then: composer holds the intended text → `send --expect-file <brief>`. Composer holds mangled text → `reset-composer`, fix the brief, retype. **Never** press Enter by hand to "just get it out". |

## G6 — Read

| | |
|---|---|
| **Do** | Read the reply that `ask` returns, or `read` afterwards. |
| **Exit assertion** | The reply is the text after the **last** `ChatGPT said:` marker, with UI chrome (timestamps, `Thinking`, `Response complete: …`) removed, and a **new** block was awaited rather than "the text changed". |
| **If it fails** | A reply consisting of `Thinking` means completion was judged too early: raise `--settle`, re-read; do not re-send. |

## G7 — Verify against the brief, numerically

| | |
|---|---|
| **Do** | Enumerate every explicit requirement in the brief (length, named elements, title, style, structure) and check each one against the reply **with a measured number**, not an impression. |
| **Exit assertion** | Each requirement has a pass/fail with evidence (e.g. "3820 characters ≥ 1500 → pass", "contains 小丑 → pass"). |
| **If a requirement fails** | Send **one** surgical follow-up that names the single required change and asks for the full text again. Do not re-run the whole task. |

## G8 — Clean up and report

| | |
|---|---|
| **Do** | Save the deliverable to a file, `reset-composer` if the next run should start clean, restore the cursor, and state the source. |
| **Exit assertion** | The deliverable exists on disk; the machine is left in a usable state. |
| **Report** | Name ChatGPT as the author (not the agent), the model the sidebar shows, the measured size, and the file path. |

---

## Failure → action table

| Symptom | Meaning | Action |
|---|---|---|
| `ABORTED: could not focus the composer` | a click missed or opened an overlay | screenshot, close the overlay, retry from G0 |
| `ABORTED: composer does not contain the intended text` | newline split or autoformat duplication | `reset-composer`, fix the brief, redo G4–G5 |
| attachment count < file count | dialog field truncated | lower `--chunk-chars`, retry once, assert again (G3) |
| `no button named 'New chat'` | header control changed or chat not resettable | `reset-composer`; if still not clean, **stop** (G2) |
| transcript shows several partial `You said:` blocks | a newline committed the message early | stop; reset; the fix is Shift+Enter (G5) |
| reply reads `Thinking` only | completion judged too early | re-read with a longer `--settle` (G6) |
| mouse is somewhere unexpected | a run died mid-way | check the cursor restore; never start a new run with a stale overlay open |

## What a correct run looks like

The worked case: a 640 × 8260 article screenshot and a 421-character brief.

```
G0   find            -> sidebar, document, composer [1554,928,1896,972]
G0.5 smoke test      -> "DONE" read back, one message
G1   slice           -> 6 slices, 640x1700, legible
G2   new-chat        -> 0 attachments, empty transcript   (asserted)
G3   attach-files    -> 3 batches, 6 attachments          (count asserted)
G4   brief.txt       -> 421 chars, no leading "N. ", no trailing newline
G5   ask             -> focused on click #1, composer held 417 chars, sent (Enter)
G6   read            -> new "ChatGPT said:" block, stable 6 s
G7   verify          -> 3869 chars >= 1500; contains 小丑; self-titled; three detailed attacks
G8   save + report   -> task/essay.md
```

## Related

- `gui-input-hard-rules` — the rules each gate enforces, with the incidents behind them.
- `chatgpt-sidebar-bridge` — the command reference and the tool file map.
- `dsh-ui-bridge/POSTMORTEM.md` — the full recorded postmortem this pipeline was derived from.

## Where this skill sits

The **process**: gates G0–G8, each asserting and stopping. It applies the rules in
`gui-input-hard-rules` to one surface, using the commands in `chatgpt-sidebar-bridge`.


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

## G9 — Browser-console work (renaming, About, topics, file upload)

Console operations follow the same gates, plus three rules learned the hard way:

- **Open the automation its own tab** (`Ctrl+T`) before navigating anywhere. Driving the active tab
  replaces whatever the human had open (`H-21`).
- **Click the button, not its label.** GitHub renders a `TextControl` with the same name as the
  button it labels; a name-only lookup returns the label and the click does nothing (`H-22`).
- **Verify every durable change from the server.** After each commit, read
  `git/trees/<branch>?recursive=1` and compare the file list with the local one; after a rename or an
  About edit, re-read `repos/<owner>/<repo>`. `commit requested` in a console log is not evidence
  (`H-23`).

A batch that reports success but changes nothing is the normal failure mode of web-console
automation, which is why the verification step is part of the gate rather than a courtesy.
