---
name: emit-fn-key-on-macos
description: Emit a real Fn key on macOS (for Typeless push-to-talk, macOS dictation, screenshot shortcuts, emoji picker, Spotlight via.
allowed-tools: Read, Edit, Write, Bash
---

# Emit a Real Fn Key on macOS

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Macos's Fn key (also called the "globe" key on modern MacBooks) is special. It's not a regular modifier — it carries `kCGEventFlagMaskSecondaryFn`, a flag that macOS's input subsystem **discards if set from userland via `CGEventPost`**. Many "remap anything" tools assume Fn behaves like Cmd / Option / Ctrl and try to emit it via `CGEventPost` — and silently fail for dictation, Typeless, macOS's dictation shortcut, Spotlight-via-globe, emoji picker, etc.

The only userland path that emits a Fn the kernel accepts is a **DriverKit VirtualHIDDevice**. Karabiner-Elements ships one. That's why Karabiner is the only FOSS tool for this job in 2026.

## When to Use This Skill

- User wants a macro-pad button, mouse button, or any external key to trigger:
  - **Typeless** push-to-talk (`pushToTalk: "Fn"` by default)
  - macOS dictation (`Fn Fn` double-tap, or single-Fn in System Settings)
  - Emoji picker (`Fn+E`)
  - Spotlight-via-globe (`Fn`)
  - App-specific Fn combos that don't work when remapped by BTT
- User reports "BTT says the shortcut is firing but nothing happens in Typeless"
- User tries `hidutil property --set` with Fn mappings and sees no effect
- User flashed QMK/ZMK on a board and Fn emission is broken

## Prerequisite Check

```bash
# 1. Karabiner-Elements installed (the only userland tool that can emit real Fn)?
test -d /Applications/Karabiner-Elements.app && echo OK || brew install --cask karabiner-elements

# 2. Karabiner has Input Monitoring + Accessibility?
#    System Settings → Privacy & Security → Input Monitoring → Karabiner = ON
#    System Settings → Privacy & Security → Accessibility → Karabiner = ON

# 3. On macOS Sequoia+: privileged daemon approved in Login Items?
#    System Settings → General → Login Items → Allow in the Background
#    → Karabiner-Elements Privileged Daemon = ON
#    Without this, Karabiner's DriverKit VirtualHIDDevice won't load and
#    your Fn remap will silently do nothing.
```

If Fn already works when pressed on your built-in keyboard but not via a remap, the DriverKit daemon is loaded but the remap rule is wrong — jump to "The One Magic Incantation" below. If even the built-in Fn stops working, re-check prerequisite 3.

## The Core Truth

```
┌───────────────────────────┐          ┌───────────────────────────┐
│  Real Fn (from keyboard)  │          │  Fn via CGEventPost(...)  │
│  Hardware → DriverKit →   │          │  Userland app → Quartz →  │
│  HIDEvent with            │          │  kCGEventFlagMaskSecon-   │
│  NX_DEVICE_CAPABILITY_    │          │  daryFn flag is DROPPED   │
│  INPUTKEYBOARD_FUNCTION   │          │  before reaching input    │
│  flag set                 │          │  subsystem.               │
│                           │          │                           │
│  ✅ Typeless / dictation  │          │  ❌ Typeless / dictation  │
│     accept it.            │          │     never fire.           │
└───────────────────────────┘          └───────────────────────────┘
```

**Karabiner-Elements** registers a DriverKit VirtualHIDDevice. When its remap rule says "emit Fn", it does so through the same kernel path a hardware keyboard uses. The `NX_DEVICE_CAPABILITY_INPUTKEYBOARD_FUNCTION` flag survives and Typeless/dictation accept it.

## The One Magic Incantation

In a Karabiner manipulator's `to` block:

```json
{ "apple_vendor_top_case_key_code": "keyboard_fn" }
```

Not:

- ❌ `{"key_code": "fn"}` — no such key_code, silently ignored
- ❌ `{"modifiers": ["fn"]}` — modifier flag without a key-down, doesn't trigger Fn semantics
- ❌ `{"consumer_key_code": "..."}` — wrong HID usage page
- ❌ `{"key_code": "function"}` — not a Karabiner keyword

The `apple_vendor_top_case_key_code` namespace is Karabiner's mapping for HID Usage Page `0x00FF` (Apple Top Case) with Usage `0x03` (Keyboard Fn). That's the descriptor Apple's own internal keyboard uses.

## Minimal Working Example

Remap the Caps Lock key (on a specific external keyboard only — adjust VID/PID) to emit real Fn:

```json
{
  "description": "Caps Lock → Fn (on external keyboard)",
  "manipulators": [
    {
      "type": "basic",
      "from": { "key_code": "caps_lock" },
      "to": [{ "apple_vendor_top_case_key_code": "keyboard_fn" }],
      "conditions": [
        {
          "type": "device_if",
          "identifiers": [{ "vendor_id": 19530, "product_id": 16725 }]
        }
      ]
    }
  ]
}
```

Drop into `~/.config/karabiner/karabiner.json` → profile 0 → `complex_modifications.rules`.

## Verification

```bash
# Open Karabiner-EventViewer
open -a "Karabiner-EventViewer"

# Press your remapped key; the Main tab should show:
# name:  fn (not apple_vendor_top_case_key_code)
# ↑ Karabiner normalizes the display back to "fn" but under the hood it's emitting
#   the Apple-Top-Case variant that carries the kernel flag.

# Then test the real consumer (e.g., Typeless with pushToTalk: "Fn"):
#   Press and hold → mic opens
#   Release → mic closes, transcript appears
```

If EventViewer shows the right event but Typeless doesn't fire:

1. Check Typeless has Accessibility permission
2. Confirm `pushToTalk` in Typeless `app-settings.json` is set to `"Fn"` (not `"fn"`, not `"Function"`)
3. Confirm no other tool is also grabbing Fn — BTT with a Fn trigger will steal the event before Typeless sees it

## Tap-vs-Hold: Do NOT Set Fn as a Held-Down Target

Attempted pattern: "tap top button → Return, hold top button → Fn" using Karabiner's `to_if_alone` + `to_if_held_down`.

**This breaks Fn system-wide**. Verified failure 2026-04-21: after loading a rule with `to_if_held_down: [{"apple_vendor_top_case_key_code": "keyboard_fn"}]`, macOS's native Fn key stopped producing Fn even when pressed directly on the built-in keyboard. Full rollback required.

The reason is still unclear — possibly Karabiner's held-down state-machine holds the Fn-flag in a way that conflicts with real hardware Fn events. Until Karabiner upstream fixes it, use a separate button for Fn.

## Why BTT Fails (One-Line Version)

BTT's "Trigger Key Sequence" and "Send Shortcut" actions go through `CGEventPost` with `CGEventCreateKeyboardEvent` + `CGEventSetFlags`. The flag `kCGEventFlagMaskSecondaryFn` is accepted by `CGEventSetFlags` (no error) but dropped by the input event manager before delivery. Apple has never documented this constraint; it's consistent across macOS 13 / 14 / 15.

## Why hidutil Fails

`hidutil property --set '{"UserKeyMapping":[...]}'` operates at the HID report level and can swap keycodes, but it cannot synthesize the Fn _flag_. The flag is set by the keyboard driver (DriverKit or Apple's internal keyboard driver) based on which key was pressed — you can't forge it at the HID report level because it's a per-event computed property, not a persisted one.

## Why QMK on Flashable Boards Can Work (but Jieli-Class Can't)

A QMK board with `NKRO + Apple Fn keycode` on an actual USB HID report descriptor that advertises `Usage Page 0x00FF`, `Usage 0x03` can emit Fn natively. The kernel accepts it because it's a _real_ hardware report.

But **cheap Jieli/Realtek/CH57x pads are not flashable** — their firmware is burned in and exposes a fixed HID descriptor (usually standard keyboard Usage Page `0x07`). No amount of reflashing with QMK/VIA/Vial works because the bootloader won't accept new firmware.

For flashable boards see: <https://github.com/qmk/qmk_firmware> → `APPLE_FN_ENABLE`.

## Deep References

- [`../configure-macro-keyboard/references/03-patterns.md`](../configure-macro-keyboard/references/03-patterns.md) — "Apple vendor Fn encoding" pattern with full rule excerpt
- [`../configure-macro-keyboard/references/04-anti-patterns.md`](../configure-macro-keyboard/references/04-anti-patterns.md) — BTT `CGEventPost` failure, tap-vs-hold Fn failure, QMK/VIA-on-Jieli failure
- [`./references/failed-approaches.md`](./references/failed-approaches.md) — condensed failure catalog for this specific task

## Sibling Skills

- [`configure-macro-keyboard`](../configure-macro-keyboard/SKILL.md) — the end-to-end setup workflow that uses this skill as one step (wiring an external macro pad's button to Fn inside a larger Karabiner rule)
- [`diagnose-hid-keycodes`](../diagnose-hid-keycodes/SKILL.md) — use this FIRST if you don't yet know which keycode your hardware emits; only then come back here to remap it to Fn

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Confirm this SKILL.md is the canonical file before any edit.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Update vendor IDs, keycodes, or FOSS-tool versions if reality disagrees with the doc.
4. **Log it.** — Add an evolution-log entry (or `04-anti-patterns.md` row) with trigger, fix, evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
