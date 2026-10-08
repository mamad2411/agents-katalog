---
name: diagnose-hid-keycodes
description: Find out what an unknown USB/Bluetooth HID button actually emits without assuming the label or documentation. Uses Karabiner's.
allowed-tools: Read, Edit, Write, Bash
---

# Diagnose HID Keycodes

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Given an unknown macro pad, mouse button, foot pedal, or HID gadget, find out exactly what each button emits at the OS level — **without guessing from labels, vendor docs, or photos**. Cheap HID pads frequently ship with arbitrary or mis-labeled keycodes (the Jieli/Free3-P ships with buttons labeled top/middle/bottom emitting Ctrl+C/Ctrl+V/Ctrl+X — which isn't the cut/copy/paste convention; it's hardware-random).

## When to Use This Skill

- A new HID device arrived and you don't know what its buttons emit
- A pad has multiple firmware modes and you need to map each mode's keycodes
- A rule isn't firing and you suspect you guessed the wrong `from.key_code`
- You need to document a device for a reproducible setup

## The Three-Tool Workflow

| Tool                      | Purpose                                                 |
| ------------------------- | ------------------------------------------------------- |
| Karabiner `ignore: true`  | Make Karabiner _observe_ the device without grabbing it |
| Karabiner-EventViewer     | Display raw HID events as text                          |
| Quartz `screencapture -l` | Capture EventViewer's window without stealing focus     |

`ignore: true` is the key insight: with it enabled, Karabiner doesn't remap anything but still logs the device's events — so you can see the raw keycodes the firmware emits.

## Workflow

### Step 1 — Identify the device's VID/PID

```bash
# USB
ioreg -p IOUSB -l -w 0 | grep -B 2 -A 6 "<product name or partial>"

# Bluetooth (after pairing)
system_profiler SPBluetoothDataType | grep -A 15 "<pad name>"
```

Record VID/PID in **decimal** (Karabiner's JSON format).

### Step 2 — Add a no-op diagnostic rule (forces Karabiner to grab the device)

**Why not just `"ignore": true` in `devices[]`?** That tells Karabiner to leave the device entirely alone — EventViewer then won't see its events either. `ignore: true` is for "hands off this device," not "inspect this device."

**Correct approach**: add an inert `complex_modifications` rule scoped to the device. Karabiner grabs the device (so EventViewer captures every HID report) but the rule does nothing. Edit `~/.config/karabiner/karabiner.json` → profile 0 → `complex_modifications.rules` and insert:

```json
{
  "description": "[DIAGNOSTIC] Grab <pad> (no remap)",
  "manipulators": [
    {
      "type": "basic",
      "from": { "key_code": "vk_none" },
      "to": [{ "key_code": "vk_none" }],
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

`vk_none` is a Karabiner virtual key that never matches real input, so the manipulator is inert. The `device_if` scoping makes Karabiner grab the device for inspection.

Reload Karabiner: Karabiner-Elements menu bar icon → Restart Karabiner-Elements.

### Step 3 — Open EventViewer and press each button

```bash
open -a "Karabiner-EventViewer"
```

- Main tab: shows `key_down` / `key_up` with decoded keycode names (`c`, `left_control`, `page_up`, etc.)
- Devices tab: shows which device emitted each event — confirms you're grabbing the right VID/PID
- Unknown Events tab: shows events Karabiner couldn't decode — relevant for consumer keys or custom HID descriptors

Press each button slowly. For modifier-combos emitted in one HID report (common on cheap pads), you'll see multiple key_down events in tight sequence:

```
13:44:02.123  key_down  left_control
13:44:02.123  key_down  c
13:44:02.198  key_up    c
13:44:02.198  key_up    left_control
```

Same microsecond timestamp for `left_control` + `c` = emitted in one HID report → you need `simultaneous` matcher.

### Step 4 — Capture without stealing focus

If you bring EventViewer to the foreground to read it, you lose the ability to press buttons on the test window. Workaround — capture by window ID:

```bash
# List windows; find EventViewer's window ID
python3 -c '
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID
for w in CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID):
    if "EventViewer" in w.get("kCGWindowOwnerName", "") or "EventViewer" in w.get("kCGWindowName", ""):
        print(w["kCGWindowNumber"], w.get("kCGWindowName"))
'

# Screenshot that window without focusing it
screencapture -l <WID> -o -x /tmp/eventviewer.png
```

`-l <WID>` captures a specific window, `-o` excludes shadow, `-x` suppresses the capture sound. The window does not need to be foregrounded.

### Step 5 — Repeat for each firmware mode (Bluetooth pads)

Many cheap BT pads have undocumented firmware modes triggered by button combos (hold all 3 keys 5s, hold top 10s, etc.). Each mode can emit completely different keycodes. For each mode you discover:

1. Switch the pad into that mode
2. Repeat step 3 — log keycode for each button
3. Document in a table

Example (Jieli/Free3-P):

| Mode | Top                | Middle             | Bottom                  |
| ---- | ------------------ | ------------------ | ----------------------- |
| 1    | `volume_increment` | `volume_decrement` | `spacebar` (play/pause) |
| 4    | `page_up`          | `page_down`        | `equal_sign`            |

### Step 6 — Clean up

Remove the `[DIAGNOSTIC]` rule from `complex_modifications.rules` and reload Karabiner. Or convert it into your real remap rule by replacing `vk_none` with the actual `from` / `to` bindings.

## Avoid Touch-ID-Triggering Audits

Do NOT query TCC.db or SQLite files under `/Library/Application Support/com.apple.TCC/` to "audit permissions" during this workflow — those queries require sudo and trigger the Touch ID prompt on every invocation. Instead:

```bash
# Non-sudo audit: is Karabiner actually grabbing the device?
karabiner_cli --list-connected-devices | jq '.[] | select(.product == "<pad-name>")'
# Returns { ..., "is_grabbed": true/false } — same info, no biometric prompt
```

The working tool IS the audit. This was discovered the hard way; see [`../configure-macro-keyboard/references/04-anti-patterns.md`](../configure-macro-keyboard/references/04-anti-patterns.md) → "Sudo-based TCC.db audits trigger Touch ID".

## Deep References

- [`../configure-macro-keyboard/references/03-patterns.md`](../configure-macro-keyboard/references/03-patterns.md) — "`ignore: true` diagnostic" + "Quartz window-ID capture" patterns in full
- [`../configure-macro-keyboard/references/04-anti-patterns.md`](../configure-macro-keyboard/references/04-anti-patterns.md) — `{"any": "key_code"}` at top-level fails silently; position-inference mistakes
- [`./references/diagnostic-workflow.md`](./references/diagnostic-workflow.md) — expanded step-by-step with screenshots

## Sibling Skills

- [`configure-macro-keyboard`](../configure-macro-keyboard/SKILL.md) — once you know what your buttons emit, use this to write the device-scoped Karabiner rule. The `vk_none` no-op rule from Step 2 here converts directly into the real rule by swapping `from` / `to` bindings.
- [`emit-fn-key-on-macos`](../emit-fn-key-on-macos/SKILL.md) — if one of the keycodes you discovered should be remapped to real Fn (for Typeless, dictation, globe key), this sibling skill explains the one correct Karabiner incantation.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Confirm this SKILL.md is the canonical file before any edit.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Update vendor IDs, keycodes, or FOSS-tool versions if reality disagrees with the doc.
4. **Log it.** — Add an evolution-log entry (or `04-anti-patterns.md` row) with trigger, fix, evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
