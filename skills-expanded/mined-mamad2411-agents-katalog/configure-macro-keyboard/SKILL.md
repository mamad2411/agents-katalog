---
name: configure-macro-keyboard
description: Configure a cheap 3-key USB-C/Bluetooth macro pad on macOS end-to-end with Karabiner-Elements.
allowed-tools: Read, Edit, Write, Bash
---

# Configure a Macro Keyboard on macOS

End-to-end workflow for cheap 3-key USB-C/Bluetooth macro pads (Jieli, Realtek, CH57x, AliExpress-class): identify the device, figure out what each button actually emits, write a Karabiner rule scoped to that device only, and handle USB + Bluetooth in one rule even when the pad's BT firmware emits different keycodes than its USB side.

> **Just want the turnkey recipe?** [`references/09-turnkey-walkthrough.md`](./references/09-turnkey-walkthrough.md) is a copy-paste-ready 30-minute walkthrough that replicates the "MacroKeyBot" setup used as this plugin's worked example — tap/double-tap on all three buttons: top (Fn for Typeless toggle / Cmd+V paste), middle (Shift+Return / Return), bottom (up_arrow / down_arrow), across USB + Bluetooth. The bottom button uses two different mechanisms (USB: software discrimination; BT: pad-firmware discrimination via separate `equal_sign` / `Option+Z` keycodes) — see [`03-patterns.md`](./references/03-patterns.md). Start there if you know what you want; come back here when you need the reusable workflow or deeper pattern references.

> **Self-Evolving Skill**: If a step breaks on a new pad, fix this file immediately. Every dead-end discovered belongs in `references/04-anti-patterns.md`.

## When to Use This Skill

- User mentions "macro pad", "macro keyboard", "3-key pad", "Stream Deck alternative" on macOS
- User wants to remap a cheap HID pad they bought from AliExpress / Amazon
- User wants buttons to emit Fn, Return, media keys, or custom shortcuts
- User hits a wall with BetterTouchTool (BTT can't emit real Fn — see sibling skill `emit-fn-key-on-macos`)
- User asks about dual USB + Bluetooth configuration for the same pad
- User mentions Jieli, Free3-P, or any pad with "USB Composite Device" as its product string

## Prerequisite Check

```bash
# 1. Karabiner-Elements installed?
test -d /Applications/Karabiner-Elements.app && echo OK || brew install --cask karabiner-elements

# 2. Input Monitoring + Accessibility granted?
#    System Settings → Privacy & Security → Input Monitoring → Karabiner = ON
#    System Settings → Privacy & Security → Accessibility → Karabiner = ON

# 3. On macOS Sequoia+: Login Items toggle for privileged daemon
#    System Settings → General → Login Items → Allow in the Background → Karabiner-Elements Privileged Daemon = ON
```

If any of the three is off, the remap will silently fail to grab the device.

## Workflow (5 Steps)

### Step 1 — Identify the device (USB)

```bash
# USB product string, VID, PID, serial, interface layout
ioreg -p IOUSB -l -w 0 | grep -B 2 -A 40 "USB Composite Device" | head -80

# Or system_profiler for a human-readable dump
system_profiler SPUSBDataType | grep -A 15 "USB Composite"
```

Record: `idVendor` (hex), `idProduct` (hex), product string, serial, interface count.

**Decode VID/PID → decimal** for Karabiner (Karabiner's JSON uses decimal):

```bash
python3 -c "print(int('0x4c4a', 16), int('0x4155', 16))"
# → 19530 16725
```

See `references/01-hardware-identification.md` for full decode of a Jieli pad including the HID report descriptor and how to infer the chip family.

### Step 2 — Identify the device (Bluetooth, if applicable)

Pair via System Settings → Bluetooth → Connect. Then:

```bash
# Pad's BT address + VID/PID + firmware
system_profiler SPBluetoothDataType | grep -A 20 "Free3-P\|<pad-name>"

# Confirm Karabiner sees it as a grabbable device
karabiner_cli --list-connected-devices | jq '.[] | select(.product == "<pad-name>")'
```

**Expect different VID/PID than USB**. Cheap pads borrow Samsung's `0x04E8` VID for macOS HID compatibility. Your one Karabiner rule must scope to both VID/PIDs via a single `device_if` with two identifiers.

See `references/08-bluetooth-configuration.md` for the Jieli/Free3-P live example.

### Step 3 — Discover what each button actually emits

Do not assume the stock mapping. Cheap pads ship with arbitrary keycodes (Jieli/Free3-P ships as Ctrl+C/Ctrl+V/Ctrl+X — _not_ cut/copy/paste convention — button order is hardware-random).

**Use `ignore: true` diagnostic rule** (zero-effect remap that logs raw events). See sibling skill `diagnose-hid-keycodes` for the full workflow. Quick version:

1. Add a disabled rule with `"conditions": [{"type": "device_if", "identifiers": [{...}]}]` and `"ignore": true` on the device
2. Open Karabiner-EventViewer → Main tab
3. Press each button, screenshot the emitted keycode
4. Repeat for BT (in each firmware mode if the pad has multiple)

### Step 4 — Write the Karabiner rule

Location: `~/.config/karabiner/karabiner.json` → profile 0 → `complex_modifications.rules` → append a new rule.

**Backup first**:

```bash
cp ~/.config/karabiner/karabiner.json ~/.config/karabiner/karabiner.json.bak.$(date +%Y%m%d-%H%M%S)
```

**Rule skeleton** (one rule, N manipulators = buttons × transports):

```json
{
  "description": "<pad-name>: Top → Fn, Middle → Return, Bottom → Command+Delete",
  "manipulators": [
    {
      "type": "basic",
      "from": {
        "simultaneous": [{ "key_code": "left_control" }, { "key_code": "c" }],
        "simultaneous_options": {
          "detect_key_down_uninterruptedly": true,
          "key_down_order": "strict_inverse",
          "key_up_order": "strict_inverse",
          "to_after_key_up": []
        },
        "modifiers": { "optional": ["any"] }
      },
      "to": [{ "apple_vendor_top_case_key_code": "keyboard_fn" }],
      "conditions": [
        {
          "type": "device_if",
          "identifiers": [
            { "vendor_id": 19530, "product_id": 16725 },
            { "vendor_id": 1256, "product_id": 28705 }
          ]
        }
      ]
    }
  ]
}
```

_(Repeat the manipulator block for middle, bottom, and the BT-mode variants — **6 manipulators** for a pure 3-key pad × 2 transports; **+2 manipulators per button per transport** for each button that uses Karabiner-side tap-vs-double-tap discrimination (see `references/03-patterns.md`). The Jieli/Free3-P live example uses tap-vs-double-tap on all three buttons → 12 manipulators total. Note: the bottom button uses Karabiner-side discrimination on USB only (Ctrl+X for both presses); on BT the pad's firmware emits two different keycodes (`equal_sign` single, `Option+Z` double), so its 2 BT manipulators are simple immediate translations rather than a detector/handler pair. Total stays at 12 either way: 8 (top + middle, both transports, software discrimination) + 2 (bottom USB, software discrimination) + 2 (bottom BT, firmware-decided keycode translation). JSON does not support `//` comments, so do not paste comment lines into your config.)_

**Five rules to remember**:

1. **`simultaneous` with `detect_key_down_uninterruptedly: true`** — needed when the pad emits modifier + key in one HID report. Default `mandatory` matcher misses these.
2. **`apple_vendor_top_case_key_code: keyboard_fn`** is the only way to emit real Fn. `key_code: fn` does nothing; `modifiers: ["fn"]` does nothing.
3. **`device_if` with MULTIPLE identifiers** — put the USB VID/PID and the BT VID/PID both in the same `identifiers` array. One rule handles both transports.
4. **Scope every manipulator to the device**. Without `device_if`, you'll remap your MacBook's built-in keyboard and break Apple's native keys.
5. **`modifiers: {"optional": ["any"]}`** — lets the firmware's modifier report flow through without blocking the rule.

Full live example (Jieli + Free3-P, 12 manipulators with tap/double-tap on all three buttons; bottom button uses asymmetric mechanisms — software discrimination on USB, firmware-decided-keycode translation on BT): `references/raw/karabiner-rule.json`.

### Step 5 — Verify the grab + test

```bash
# Karabiner sees and grabs the device
karabiner_cli --list-connected-devices | jq '.[] | select(.product == "<pad-name>") | {product, is_grabbed}'

# Should return {"product": "...", "is_grabbed": true}

# Live event test
open -a "Karabiner-EventViewer"
# Press buttons → should see your TARGET keycode, not the SOURCE
```

If `is_grabbed: false`, re-check Input Monitoring + Accessibility + Login Items (step Prerequisite Check).

If grabbed but buttons pass through unchanged: your `simultaneous` matcher is probably wrong — the pad emits the combo in one report but you wrote `mandatory`. Revisit step 3.

If real Fn stops working system-wide after your rule loads: **revert immediately**. Do not set `to_if_held_down` with `keyboard_fn` as the target — this breaks Fn-emission on the whole system (verified failure). See `references/04-anti-patterns.md` → "Tap-vs-hold Fn emission".

## Decision Tree: Which Target Keycode?

| You want button to emit…                    | Target JSON                                                                                                             |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Return / Enter                              | `{"key_code": "return_or_enter"}`                                                                                       |
| Shift+Return (newline without submitting)   | `{"key_code": "return_or_enter", "modifiers": ["left_shift"]}`                                                          |
| Fn (for Typeless, dictation)                | `{"apple_vendor_top_case_key_code": "keyboard_fn"}`                                                                     |
| Command+Delete (delete-to-home)             | `{"key_code": "delete_or_backspace", "modifiers": ["left_command"]}`                                                    |
| Option+Delete (delete word)                 | `{"key_code": "delete_or_backspace", "modifiers": ["left_option"]}`                                                     |
| Media play/pause                            | `{"consumer_key_code": "play_or_pause"}`                                                                                |
| Volume up/down                              | `{"consumer_key_code": "volume_increment"}` / `volume_decrement`                                                        |
| Launch an app                               | `{"shell_command": "open -a 'App Name'"}`                                                                               |
| Run a shell command                         | `{"shell_command": "/path/to/script.sh"}`                                                                               |
| **Tap = A, double-tap = B** (single button) | See pattern in `references/03-patterns.md` → "Tap vs. double-tap discrimination" (`set_variable` + `to_delayed_action`) |

## Handling Multiple BT Firmware Modes

Many cheap pads have 2-4 firmware modes that emit different keycodes per mode. The Jieli/Free3-P has 4 modes:

| Mode | Top                | Middle             | Bottom                  |
| ---- | ------------------ | ------------------ | ----------------------- |
| 1    | `volume_increment` | `volume_decrement` | `spacebar` (play/pause) |
| 2    | (unexplored)       | —                  | —                       |
| 3    | (unexplored)       | —                  | —                       |
| 4    | `page_up`          | `page_down`        | `equal_sign`            |

**Pick the mode with the rarest keys** (mode 4 for Free3-P — page_up/page_down are rarely used on laptops). Then add manipulators that match those keycodes plainly (no `simultaneous` needed for single-key firmware modes).

Mode-switch combos are often undocumented. Common attempts: hold all 3 keys ≥ 5s, hold top alone ≥ 5s, press top+bottom simultaneously. Document what works when you find it.

See `references/08-bluetooth-configuration.md` for the full mode-4 setup.

## Deep References (load on demand)

| Topic                                | File                                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------- |
| **Turnkey walkthrough (start here)** | [references/09-turnkey-walkthrough.md](./references/09-turnkey-walkthrough.md)               |
| Device overview (TL;DR tables)       | [references/overview.md](./references/overview.md)                                           |
| Hardware identification              | [references/01-hardware-identification.md](./references/01-hardware-identification.md)       |
| Live USB config (Jieli)              | [references/02-usb-wired-configuration.md](./references/02-usb-wired-configuration.md)       |
| Reusable patterns                    | [references/03-patterns.md](./references/03-patterns.md)                                     |
| Anti-patterns / dead-ends            | [references/04-anti-patterns.md](./references/04-anti-patterns.md)                           |
| BT pairing roadmap (historical)      | [references/05-bluetooth-roadmap.md](./references/05-bluetooth-roadmap.md)                   |
| BT ecosystem survey                  | [references/06-bluetooth-landscape-survey.md](./references/06-bluetooth-landscape-survey.md) |
| BT toolbox (evaluated tools)         | [references/07-bluetooth-toolbox.md](./references/07-bluetooth-toolbox.md)                   |
| Live BT config (Jieli mode 4)        | [references/08-bluetooth-configuration.md](./references/08-bluetooth-configuration.md)       |
| Raw dumps                            | [references/raw/](./references/raw/)                                                         |

## Sibling Skills

- `emit-fn-key-on-macos` — focused coverage of why only Karabiner can emit real Fn (BTT / hidutil / QMK on locked firmware all fail)
- `diagnose-hid-keycodes` — `ignore: true` + EventViewer + Quartz focus-free screencap workflow for figuring out what a mystery button emits

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Confirm this SKILL.md is the canonical file before any edit.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Update vendor IDs, keycodes, or FOSS-tool versions if reality disagrees with the doc.
4. **Log it.** — Add an evolution-log entry (or `04-anti-patterns.md` row) with trigger, fix, evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
