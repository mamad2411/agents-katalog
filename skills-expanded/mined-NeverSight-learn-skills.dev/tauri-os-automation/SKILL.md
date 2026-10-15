---
name: tauri-os-automation
description: >-
  Windows OS-level automation constraints for Tauri v2 L4 tests — system tray,
  registry, global key hooks, window polling. Defines what is automatable via
  pywinauto / UIA / winreg and what must remain manual. Invoked by
  tauri-test-setup (L4 section) and tauri-test-generator (L4 common mistakes).
  Trigger: "L4 test", "pywinauto", "system tray test", "tray menu automation",
  "global key hook test", "LLKHF_INJECTED", "UIA COM crash 0x80040155",
  "Windows 11 tray icon", "TrayIconBuilder tooltip".
---

# Tauri OS Automation (L4)

> **Platform note:** Windows-only. All gotchas below are WebView2 / UIA /
> winreg specific; macOS and Linux equivalents are unverified.

> **Reference-only skill:** This skill documents L4 test automation patterns
> (pywinauto, UIA, `winreg` for registry read/backup/restore, `FindWindowW`
> for window polling) consumed by `tauri-test-setup` and
> `tauri-test-generator`. It does not execute the patterns itself. Generated
> L4 tests require an interactive desktop session and may mutate
> `HKCU\...\Run` (with backup/restore fixtures) when run.

Accumulated Windows gotchas for Tauri v2 **L4 (OS-level) test automation**.
The same pitfalls hit every new L4 test across every skill that sets up or
generates them — this skill is the single source of truth so the knowledge
does not silently drift between `tauri-test-setup` and `tauri-test-generator`.

## L4 Automatable vs Manual

| Category | Automatable? | Tool | Reference |
|---|:---:|---|---|
| System tray icon presence | ✅ | pywinauto UIA (`SystemTray.NormalButton`) | `windows-tray-uia.md` |
| Tray context menu open | ✅ | pywinauto UIA (`#32768` popup) | `windows-tray-uia.md` |
| Tray menu action click | ✅ | pywinauto UIA `MenuItem` | `pywinauto-patterns.md` |
| Registry read / verify | ✅ | Python `winreg` | `pywinauto-patterns.md` |
| Registry backup / restore (fixture) | ✅ | Python `winreg` + pytest fixture | `pywinauto-patterns.md` |
| Window existence polling | ✅ | `ctypes.windll.user32.FindWindowW` | `polling-stability.md` |
| Window interaction (one-shot) | ✅ | pywinauto UIA | `polling-stability.md` |
| Global key hooks (rdev, `WH_KEYBOARD_LL`) | ❌ | — | `key-hook-constraints.md` |
| Audio playback (rodio / cpal) | ❌ | — | Hardware required — manual |
| Audio / USB device detection | ❌ | — | Physical change required — manual |
| Reboot autostart behavior | ❌ | — | OS reboot required — manual |
| Long-running stability (CPU / RAM) | ❌ | — | Long observation — manual |

See each referenced file under `references/` for the specific code pattern,
trap explanation, or constraint rationale.

## Prerequisites for Automation

1. **Tauri side.** `TrayIconBuilder::new(...).tooltip("Your App")` is
   **mandatory** — without the tooltip the tray icon has an empty UIA name
   and cannot be found by name. See `references/windows-tray-uia.md`.
2. **Python stack.** Python 3.11+, `pywinauto>=0.6.8`, `psutil`, `pytest`,
   `pytest-timeout`. Add `playwright` to the same project if L3+L4 hybrid
   tests are in scope (hybrid infrastructure itself lives in
   `tauri-test-setup`).
3. **Session.** Tests must run in the user's own **interactive desktop
   session** — UIA requires an interactive window station, so CI runners
   headless by default will not work without an autologon agent.

## Invoke Guidance

### From `tauri-test-setup` (L4 section)

1. Load the **L4 Automatable vs Manual** table above verbatim into the L4
   step of the setup guide.
2. For the `conftest.py` app fixture (process lifecycle + CDP env var),
   tray menu click helpers, and registry backup/restore fixture, reference
   `references/pywinauto-patterns.md`.
3. For the `TrayIconBuilder.tooltip()` requirement and the Windows 11
   taskbar vs system-tray pitfall, reference `references/windows-tray-uia.md`.
4. For window existence checks in the `app` fixture and helpers, reference
   `references/polling-stability.md` (`FindWindowW`, not
   `Desktop().windows()`).
5. To justify why key-hook tests remain manual despite pywinauto otherwise
   covering L4, reference `references/key-hook-constraints.md`.
6. For the `TAURI_CDP_PORT` env-var contract consumed by the app fixture,
   invoke `/tauri-multi-instance` — do not duplicate the port rules here.

### From `tauri-test-generator` (L4 or L3+L4 journeys)

1. When generating "L4 Common Mistakes" rows, link to the relevant
   reference file instead of rewriting the content — keep this skill as the
   single source.
2. **Tray icon journeys** → require search via `SystemTray.NormalButton` in
   the overflow area, citing `references/windows-tray-uia.md`.
3. **Window-appearance polling journeys** → require `FindWindowW`, citing
   `references/polling-stability.md`.
4. **Global key hook journeys** → classify as **manual**, citing
   `references/key-hook-constraints.md` as the reason.

## Non-Goals

- **L3+L4 hybrid infrastructure** (Playwright CDP context manager,
  connect-after pattern) lives in `tauri-test-setup`. This skill is
  L4-only.
- **Port / CDP endpoint contract** lives in `tauri-multi-instance`.
- **Cross-platform equivalents** (AppleScript, xdotool, AT-SPI) are
  unverified and out of scope.
