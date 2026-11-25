---
name: paste-text
description: Enter literal text — especially Chinese, emoji, and punctuation — reliably through clawtouch-mcp by writing it to the system clipboard and pasting it, instead of typing character-by-character. Sidesteps the input-method editor (IME) and keyboard-layout problems that make hid.type produce garbled or wrong characters. Load whenever an agent must enter non-ASCII text, or any exact text, into a focused field on a machine where an IME (Pinyin, etc.) or a non-US keyboard layout may be active.
---

# Skill: paste-text (reliable text entry via the clipboard)

> **Cross-cutting technique** — not tied to any one app or app version, and
> works with any `clawtouch-mcp` release. If a command here is wrong on your
> OS, open an issue at
> [tinqiao-oss/clawtouch-skills](https://github.com/tinqiao-oss/clawtouch-skills/issues).

For LLM agents entering literal text through `clawtouch-mcp`. `hid.type`
sends **raw US-layout HID keycodes** — the same bytes a physical US
keyboard sends. The operating system, its active **input method (IME)**,
and its **keyboard layout** then decide which character each keycode
becomes. That makes `hid.type` unreliable for anything beyond plain ASCII
on a US layout:

- **Chinese / Japanese / Korean** — not possible at all. There is no
  keycode for 你 or 好; a Pinyin IME turns `ni hao` into a
  candidate-picking session, not the literal text.
- **Punctuation under a CJK IME** — changes silently. With Pinyin's
  "Chinese punctuation" mode on, `:` becomes `：` and `,` becomes `，`.
- **Non-US layouts** (AZERTY / Dvorak / Colemak) — the same keycodes map
  to different glyphs, so `hid.type("123")` can come out as `&é"`.

## The reliable way: put text on the clipboard, then paste

Pasting hands the exact bytes to the field in one shot — no IME
composition, no candidate picking, no layout translation.

**Step 1 — write the text to the system clipboard.** This is an ordinary
OS command run from your own shell, *not* an HID call:

- **macOS:**
  ```bash
  printf '%s' '你好，ClawTouch！' | pbcopy
  ```
- **Windows (PowerShell)** — encoding-safe; do **not** pipe to `clip`, it corrupts non-ASCII:
  ```powershell
  Set-Clipboard '你好，ClawTouch！'
  ```
- **Linux (X11):**
  ```bash
  printf '%s' '...' | xclip -selection clipboard
  ```
- **Linux (Wayland):**
  ```bash
  printf '%s' '...' | wl-copy
  ```

> These commands deliberately add **no trailing newline**: use `printf '%s'`
> (not `echo`, which appends `\n`) on macOS/Linux; `Set-Clipboard '...'` is
> exact on Windows (verified). A stray trailing newline in the clipboard can
> auto-submit a chat box — see Known gotchas. If the text itself contains a
> quote/apostrophe, shell-escape it (here-doc / stdin) instead of naive
> single-quoting.

**Step 2 — paste with an HID shortcut:**

| OS | Paste call |
|----|-----------|
| macOS | `hid.key("cmd+v")` |
| Windows / Linux | `hid.key("ctrl+v")` |

The text arrives literally and instantly, independent of the active IME
or layout.

## When to use this vs `hid.type`

| Situation | Use |
|-----------|-----|
| Any non-ASCII text (Chinese, emoji, accented) | **Clipboard paste** — the only reliable way |
| Exact ASCII where punctuation must be correct | **Clipboard paste** — avoids IME punctuation drift |
| Short plain-ASCII on a known US / ABC layout | `hid.type` is fine |
| Keyboard shortcuts (`ctrl+c`, `alt+tab`, …) | `hid.key` — keycodes are layout-immune and the IME ignores them |

## Known gotchas

- **Paste overwrites the host clipboard.** On a machine the user is also
  using, you are clobbering whatever they had copied. If that matters,
  read the current clipboard first (`pbpaste` / `Get-Clipboard` /
  `xclip -selection clipboard -o`) and restore it after the paste lands.
  Restoring does **not** scrub the text from clipboard-history /
  cloud-clipboard tools (Win+V, Universal Clipboard, third-party
  managers) — avoid this route for secrets you don't want captured or
  synced off-box.
- **The target field must accept a paste.** Most fields accept paste
  (including password fields — that's how password managers work), but a
  few hardened secure-input controls block `Ctrl+V`; if paste silently
  does nothing, fall back to `hid.type` for ASCII.
- **Give the paste a moment.** After `cmd+v` / `ctrl+v`, wait briefly (a
  `hid.hover` over a safe spot, or a short sleep) before the next action
  so the field commits — a large paste is not instantaneous.
- **A pasted newline may submit.** In a chat box, a literal newline in
  the clipboard text can send the message. Paste the body, then send
  `enter` yourself only when you actually mean to.
- **Switching the IME to ABC is a weaker fallback.** It only makes ASCII
  reliable — it still cannot enter Chinese — and the toggle shortcut
  varies per IME (Caps Lock / Shift / Ctrl+Space), so it is easy to flip
  the wrong way. Prefer paste.

## When this skill doesn't help

- **No shell access.** This pattern needs some way to write the OS
  clipboard (a shell command). An MCP client that exposes only `hid.*`
  and nothing else cannot use it, and is limited to `hid.type`'s ASCII
  range.
- **Rich content** (formatted text, images): a paste delivers whatever
  the clipboard already holds; building rich clipboard content is
  app- and OS-specific and out of scope here.
