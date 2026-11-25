---
name: gui-input-hard-rules
description: Mandatory engineering rules for driving a real Windows GUI with simulated OS mouse and keyboard input while reading state from the UI Automation tree, derived from a recorded postmortem of twelve concrete failures. Load this before writing or running any UI-driving automation, and whenever a UI automation keeps failing, mis-targets, silently half-succeeds, or leaves a window in a blocking state.
whenToUse: Any task that moves the real cursor, types real keystrokes, or reads another application's accessibility tree; any agent writing scripts with SendInput, pyautogui, uiautomation, or Win32 window APIs; any moment a UI automation "succeeded" but the screen disagrees.
---

# GUI input hard rules

These are not guidelines. Each rule exists because it was violated once, on a real machine, with a
recorded consequence. The accompanying evidence lives in `dsh-ui-bridge/POSTMORTEM.md`.

**The one-line thesis:** every failure below was a decision made at the wrong level of abstraction —
editing source by line number, calling a container's centre "the input area", reading "no error" as
"accepted", reading "not observed" as "not present". A rule is what removes the need to decide.

---

## A. Editing and code discipline

**H-01 — Never edit a source file by line index from a shell.** Each shell invocation is a fresh
process; variables from a previous call are `$null`, and `lines[0..($null-2)]` silently produces a
nonsense slice. *Incident:* a 1200-line tool was corrupted into a syntactically invalid 1324-line
file. **Enforcement:** edit source with the editor tool. If a script must rewrite a file, compute
indices *in that same process*.

**H-02 — Back up before any programmatic rewrite, and assert invariants before writing.** The repair
was only possible because the original text happened to survive inside the damaged file.
**Enforcement:** copy aside; before writing, assert that each critical definition appears exactly
once in the new text; refuse to write otherwise.

**H-03 — One library module, not N throwaway scripts.** *Incident:* the same DPI call, the same
`find_descendant`, and the same window lookup were copied into six one-off probe files; a fix then
had to be applied in six places, and drift began. **Enforcement:** probes may be written fast, but
they must end up folded into the module or deleted. Never leave two copies of a helper.

---

## B. Targeting and window discovery

**H-04 — Click a semantic point, never a container's geometric centre.** *Incident:* with several
attachments the composer grew upward, its centre landed on a thumbnail, and the click opened an
image preview — the input control then vanished from the tree and the focus check failed three
times in a row. **Enforcement:** derive the point from what it is (`bottom - 14` is the text line),
not from the middle of a rectangle.

**H-05 — Discover windows through at least two mechanisms.** *Incident:* an owned modal dialog was
missing from UI Automation's top-level enumeration while plainly on screen; Win32 `FindWindowW`
found it immediately. **Enforcement:** UIA + Win32 cross-check; when one is empty and the other is
not, the empty one is wrong.

**H-06 — "Not observed" is not "not present".** *Incident:* from a single negative enumeration the
conclusion "the dialog closed by itself" was written down. It had not; it was still modal and was
swallowing every subsequent click. **Enforcement:** before any conclusion about absence, confirm
with a second method and say which methods were tried.

**H-07 — A modal chain is one atomic process.** *Incident:* clicking a menu in one command and
filling the dialog in the next lost the dialog in between. **Enforcement:** open → fill → confirm
inside a single process; never hand control back to the shell mid-chain.

**H-08 — Pre-flight for leftover modals and dirty state.** *Incident:* a modal left open by an
earlier probe blocked the real run and ate its clicks. **Enforcement:** at start, detect a blocking
dialog (`#32770`) or a non-empty composer and clear it; interactive probes must close what they open.

**H-09 — Look at the whole screen when a region looks wrong.** *Incident:* a sidebar screenshot was
blank and the sidebar internals were briefly blamed; another window simply covered it.
**Enforcement:** when a region looks empty or wrong, capture the full screen and check the
foreground window before touching code.

---

## C. Input semantics

**H-10 — Verify focus immediately before typing, and abort rather than guess.** *Incident:* after a
click landed on the wrong element, focus was not on the composer. *Result:* the guard refused to
type, so ~440 characters never sprayed into a different application — including the agent's own host.
**Enforcement:** query the focused control; require it to be the target or a descendant; retry a
bounded number of times; then abort.

**H-11 — Newlines do not all mean the same thing.** *Incident:* in a send-on-Enter composer, a
trailing newline in a prompt file pressed Enter; a four-paragraph brief went out as **four separate
partial messages**, and each fragment was answered separately. **Enforcement:** type newlines as
**Shift+Enter** wherever Enter commits; strip trailing whitespace from any prompt read from a file.

**H-12 — Rich editors mutate what you type.** *Incident:* a line starting `4. ` was autoformatted
into an ordered list and the marker was duplicated in the content (`4. 4. 文风…`).
**Enforcement:** avoid commit-triggering syntax at line starts in typed prompts; always compare the
field's actual content against the intent before committing.

**H-13 — Normalise text before comparing it.** *Incident:* a correct 449-character composer value
failed a substring test because Chromium returns `\r\n` where the prompt had `\n`, and a correct
message was refused. **Enforcement:** normalise line endings, blank lines and edge whitespace on
both sides, then compare; report the first differing index on mismatch, not just "not equal".

**H-14 — Verify content immediately before the committing action.** *Incident:* the pre-send check
caught both H-11 and H-12 before anything left the machine. **Enforcement:** no Enter, no delete, no
submit without re-reading the field and matching it against the intent.

---

## D. Silent partial success

**H-15 — "No error" is not "accepted".** *Incident:* a dialog's file-name field truncates near 256
characters; six 64-character quoted paths produced exactly **three** attachments with no error at
all. **Enforcement:** bound batch size by a character budget derived from measured limits; after
each batch, **assert the resulting count**; treat an unexplained count as a failure.

**H-16 — Assert the postcondition of every reset or "start fresh" step, and abort when it fails.**
*Incident:* a `New chat` click reported "no button named …" and the run continued anyway; the
composer then accumulated twelve attachments instead of six. **Enforcement:** a failed precondition
is a stop, not a warning; assert empty transcript and zero attachments before attaching anything.

**H-17 — Wait on a domain completion signal, not on "the output changed".** *Incident:* the first
read of a reply returned the state `Thinking` with no content, because "the text changed" is
satisfied by a placeholder. **Enforcement:** name the signal that means done for this surface
(a new message block whose text is stable for N seconds, a progress indicator disappearing).

---

## E. Budget, safety and reporting

**H-18 — Prove the pipeline with a cheap smoke test before the expensive real task.** *Incident:*
the full 438-character brief was used to discover the newline bug; the task ran about six times and
the deliverable was generated repeatedly, costing the user real quota. **Enforcement:** a three-line
fake task must exercise every phase — target, type, commit, wait, read — before real content is used.

**H-19 — Constrain output volume at the source.** *Incident:* one dump pulled a 624 KB API payload
into the transcript. **Enforcement:** print selected fields with explicit caps; write large results
to a file and query them afterwards.

**H-20 — Keep the abort and restore machinery.** Every run carries wall-clock, event-count and
cursor-distance caps, a panic key (Escape) checked before each emission, and restores the cursor
afterwards. These are load-bearing: real input means the human cannot use their own machine while
the automation runs, and a runaway loop is not recoverable by the user.

---

## Compliance checklist (run before shipping any UI automation)

1. Does every click target a semantic point? (H-04)
2. Is window discovery cross-checked? (H-05, H-06)
3. Is every modal chain atomic, with a pre-flight? (H-07, H-08)
4. Is focus verified before typing, and content verified before committing? (H-10, H-14)
5. Are newline and autoformat semantics handled for this specific field? (H-11, H-12)
6. Is every text comparison normalised? (H-13)
7. Does every batch-producing step assert its count? (H-15)
8. Does every reset step assert its postcondition and abort on failure? (H-16)
9. Is the completion signal domain-specific? (H-17)
10. Was the pipeline smoke-tested cheaply first? (H-18)
11. Are caps, panic key and cursor restore in place? (H-20)

## Related

- `chatgpt-sidebar-delivery` — the ordered, gated process that applies these rules to one concrete
  surface (the ChatGPT sidebar in Edge).
- `chatgpt-sidebar-bridge` — the tool reference (commands, parameters, file layout).
- `dsh-ui-bridge/POSTMORTEM.md` — the recorded incidents each rule is derived from.

## Where this skill sits

The **discipline**: twenty rules and the incidents behind them, for any GUI driven with simulated
input. `chatgpt-sidebar-delivery` is one concrete application of them.


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

## F. Browser-console discipline (added after two live failures)

**H-21 — Never navigate a tab you did not open.** Browser automation belongs in its own tab.

*Incident:* the console work drove `Ctrl+L` on whatever tab happened to be active, so each
navigation **destroyed the page the human had open** — repeatedly, across the whole session. Their
working tabs were replaced by GitHub pages they never asked for.

*Rule:* press `Ctrl+T` first and drive only that tab; close it when finished. Never send `Ctrl+L`
into a tab the automation did not create. A dedicated tab also gives a stable, predictable layout
for every later step, which the shared tab never does.

**H-22 — Match the control, not just its name.** The same accessible name often exists on both a
label and its button.

*Incident:* GitHub's upload page carries

```
d15  ButtonControl   'Commit changes'    <- the real button
d16  TextControl     'Commit changes'    <- a text label with the same name
```

The lookup returned the first match in tree order — the label — and clicked it. Nine uploads ended
with the console reporting `commit requested` and **not one commit was created**.

*Rule:* when several nodes share a name, prefer `ButtonControl` / `HyperlinkControl` before falling
back to anything else, and never treat "I clicked it" as evidence that the action happened.

**H-23 — Verify side effects on the server, not in the UI.** A UI click is a request, not a fact.

*Incident:* the failure above survived nine rounds because the only evidence used was the console
line `commit requested`. A single API read settled it:

```powershell
Invoke-RestMethod "https://api.github.com/repos/<owner>/<repo>" |
    Select-Object pushed_at, size
Invoke-RestMethod "https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1" |
    Select-Object -ExpandProperty tree | Where-Object type -eq blob |
    Select-Object path, size
```

*Rule:* after any action with a durable effect (commit, push, release, settings change), confirm it
from the server's own record — for GitHub that is the public REST API, which needs no token for a
public repository — and compare against the state before the action. Prefer this over reading the
page, which can serve a stale accessibility tree.


**H-24 — Before automating a web console, check whether the machine already holds a credential
for it.** Content transfer belongs to `git`, not to a browser form.

*Incident:* nine web-console upload batches reported `commit requested` and produced **zero**
commits — first because the commit lookup returned a *label* rather than the *button*, then
because an empty repository has no branch for `/upload/<branch>` to target (it redirects to the
repo home, where the page says "Select a branch to upload files"). One `git push` against the
credential Git Credential Manager already held moved the entire 43-file tree, with structure
intact, in a single operation.

*Rule:* let `git` use its credential helper directly — confirm auth with a secret-free `git ls-remote <url>` and **never** print credential-helper output ( `git credential fill` writes the token straight to stdout, where it lands in agent transcripts and command logs). A push is exact, preserves paths, carries a real commit
message, and is verifiable with one API call. Reserve browser automation for the things git
cannot do — renaming a repository, editing About, setting topics — and verify each of those on
the server afterwards (H-23).

**Trap worth naming:** on an **empty** repository, `/<repo>/upload/<branch>` cannot work, because
the branch does not exist yet. The first commit has to come from somewhere else — a clone and
push, the web editor, or an upload form reached from the repo home page rather than by URL.
