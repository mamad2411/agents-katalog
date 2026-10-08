---
name: macos-font-defaults
description: Set macOS's "user fixed-pitch font" and per-app fixed-width fonts (TextEdit plain text, Stickies default note) to a chosen font — by default JetBrains Mono NL Nerd Font. Idempotent and parameterized, so it doubles as a fresh-machine setup step. Use when the operator wants their default monospaced/fixed-width font changed, or asks "make my fixed-width font X", "default mono font", "set Stickies/TextEdit font". TRIGGERS - default fixed-width font, monospaced font default, set my mono font, fixed-pitch font, Stickies default font, TextEdit plain text font.
allowed-tools: Bash
---

<!-- SKILL-PLUGIN-ROOT-OK: explains why this variable must not be used here -->

# macos-font-defaults — set the system fixed-width font

> **Self-Evolving skill** — if a macOS release changes these defaults keys or Stickies' storage, fix this SKILL.md and `apply.sh`; see the Post-Execution Reflection at the bottom.

macOS has **no single system-wide monospaced-font setting**. This skill sets the three
levers that exist, in one idempotent command:

Resolve the script first — `$CLAUDE_PLUGIN_ROOT` is NOT a shell variable and expands to empty
in a Bash call (it exists only inside plugin manifests and hook/MCP subprocesses):

```bash
APPLY="$(cc-plugin-root macos-font-defaults)/skills/macos-font-defaults/apply.sh"
```

| Lever                                 | What it controls                                                                                |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| global `NSFixedPitchFont`             | `+[NSFont userFixedPitchFontOfSize:]` — TextEdit plain text and other standard-text-system apps |
| `com.apple.TextEdit NSFixedPitchFont` | TextEdit's plain-text font explicitly (belt-and-suspenders)                                     |
| Stickies `DefaultFont`                | new Stickies notes (archived `NSFont` in the sandbox container plist)                           |

## Usage

```bash
"$APPLY" check                          # report current values, change nothing
"$APPLY" apply                          # set everything to JetBrains Mono NL (size = macOS default)
"$APPLY" apply --font "Menlo-Regular"   # a different font (PostScript name)
"$APPLY" apply --size 13                # also pin a size (omit to keep macOS default ~11pt)
```

Always run `check` first and show the operator the current values before `apply`.

## What it does NOT cover (be honest)

- **Terminal / iTerm / VS Code / editors** keep their own font settings — unchanged.
- **Apple Notes** hardcodes its monospaced face and cannot be redirected to a custom font.
  Its only mono lever is the per-note **Monostyled** style (the `draft-park` skill uses it).
- This is **not** a system-UI font override; menus/Finder are unaffected.

## Notes

- The default font is the JetBrains Mono NL Nerd Font regular PostScript name
  `JetBrainsMonoNLNF-Regular`. `apply` fails fast if the font isn't installed.
- The Stickies step only runs when the stored default differs, and quits a running
  Stickies first (it would otherwise overwrite the plist on exit). Re-running is safe.
- Relaunch target apps to pick up changes; already-running apps cache the font.
- Reverse the global lever with `defaults delete -g NSFixedPitchFont NSFixedPitchFontSize`.

## Post-Execution Reflection

After running `apply`, check before closing:

1. **Did `check` confirm all three levers?** — if a value didn't stick, the key or write path drifted; fix `apply.sh`.
2. **Did an app fail to pick up the font?** — note the relaunch requirement, or add that app's own font key.
3. **Did a macOS update move/rename the Stickies plist or change `NSFixedPitchFont` semantics?** — update the levers table here.

Only update if the issue is real and reproducible — not speculative.
