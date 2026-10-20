---
name: persistent-process-memory-scanner-for-ui-state-extraction
description: Cheat-Engine-style differential memory scanning to locate dynamic UI state fields in processes that don't expose them via API or DOM.
category: automation
version: 1.0.0
tags: [automation, windows, memory-scanning, reverse-engineering, ui-extraction]
source_type: extracted-from-git
source_url: https://github.com/lsdefine/GenericAgent.git
source_ref: main
source_commit: ec34b7e1c0f11fbb9709680ccfe313187a1b942b
source_project: GenericAgent
source_path: memory/procmem_scanner_sop.md
imported_at: 2026-04-18T00:00:00Z
confidence: high
version_origin: extracted
---

# Process-memory scanner for UI-state extraction

A Cheat-Engine-style differential scanning workflow for reading dynamic state out of closed-source, self-rendered GUI applications (WeChat, QQ, legacy games, self-drawn controls) that don't expose the information via Accessibility APIs, DOM, or any public IPC.

## When to use

- You need to read a piece of state (e.g., "which chat is currently selected?") from an application whose UI is self-drawn (DirectX / custom GDI / Skia) and accessibility-invisible.
- Vision/OCR works but is too slow or too expensive for a tight automation loop.
- The application does expose the data visibly (so you can force it to change by user action), just not programmatically.

## Core idea

On Windows, any running process exposes readable memory if you have `PROCESS_QUERY_INFORMATION | PROCESS_VM_READ` access (admin is NOT always required for user-owned processes). Strings the UI renders are somewhere in that memory. Your job is to pin the exact address of the *dynamic* copy (the one that moves with state changes), not the static ones sitting in caches or logs.

## The workflow (converges in three observations)

Assumption: you have at least three distinguishable states — call them `A`, `B`, `C`.

1. **Force state to A.** Scan all memory for the string representation of `A`. Get the full candidate set `S`.
2. **Switch to state B.** Re-read *every address in S* (do NOT re-scan — see pitfall below). Keep addresses whose content ≠ `A`. Call this set `S'`. (Rationale: the static/cached copies of `A` don't change when the UI switches.)
3. **Switch back to A.** Re-read every address in `S'`. Keep addresses whose content == `A` again. Usually narrows to 1–3 candidates.
4. **Still multiple?** Repeat with `B`, `C`. Convergence is rapid — three observations is usually enough.

### Critical pitfall: do NOT re-scan

At step 2 and later, a naive implementation re-runs the full scan for `B`. That's wrong — the dynamic-copy address is now holding `B`, but the scan finds it along with every stale "B" from chat history, notifications, etc. You get a muddle and possibly zero overlap with `S`. You must re-read the exact addresses from the previous step with `ReadProcessMemory`, not re-scan.

## Minimal helper (Windows, `ctypes`)

```python
import ctypes

def read_addrs(pid: int, addrs: list[int], buflen: int = 256) -> dict[int, str]:
    """Read a list of addresses from pid; return {addr: decoded-string}."""
    k32 = ctypes.windll.kernel32
    hp = k32.OpenProcess(0x10, False, pid)   # PROCESS_VM_READ
    buf = ctypes.create_string_buffer(buflen)
    rd = ctypes.c_size_t()
    out = {}
    try:
        for a in addrs:
            a = int(a, 16) if isinstance(a, str) else a
            k32.ReadProcessMemory(hp, ctypes.c_void_p(a), buf, buflen, ctypes.byref(rd))
            out[a] = buf.raw.split(b"\x00")[0].decode("utf-8", errors="ignore").strip()
    finally:
        k32.CloseHandle(hp)
    return out
```

## State-change driver

You also need a way to *force* the app into states `A`, `B`, `C`. Options (preferred first):

1. Programmatic switch via whatever interface the app accepts (for a chat app: search → Ctrl+V → Enter).
2. Physical click via coordinate automation (`pyautogui`, `ljqCtrl`, equivalent). Compute DPI-corrected coordinates; add ~500ms settle delay before re-reading.
3. Vision-assisted click for scenarios where layout is non-deterministic (e.g., list order changes with messages).

Always **verify** the switch actually took effect by reading at least one known address before proceeding. Don't blind-trust that the click landed.

## Picking the state samples

When the source of states comes from an adjacent data source (e.g., a SQLite database, IPC dump), pick unambiguous real samples. **Avoid ad-hoc typed-in names** — typing into a search box may trigger ads, autocomplete, or recommendations that contaminate the scan result set. Pull from a real, known-good index.

## Operational pitfalls (learned the hard way)

- The process name may not match marketing ("Weixin.exe" not "WeChat.exe"). `win32gui.GetWindowThreadProcessId` on a *window* you can see is more reliable than `tasklist` + name match. Multi-process apps have lots of PIDs; pick the one that owns the visible window.
- Scan results may come back as strings like `"Addr: 0x1234...\nHex: ..."` — parse the address with `int(token, 16)` before using it.
- The first scan result can be a sponsored/ad entry (for apps with built-in search). Filter or pick the second hit, or force a settle delay ≥ 1.5s before confirming.
- Disambiguation via the **sidebar** (not search) is the final step — search contaminates the state; a direct sidebar click is clean.
- `read_addrs` narrow buffers (256 bytes) are fine for short strings. Increase for longer payloads. UTF-8 / UTF-16 depends on the app — sniff once, then lock.

## Why this works

Static copies of a string (history, caches, sent-message logs) don't move with UI state. The dynamic pointer — the one the render loop dereferences every frame — does. Differential scanning systematically eliminates the static set by requiring the value to *follow* the UI through multiple state changes. Three observations is usually sufficient because each cuts the candidate pool by a large factor.

## Anti-patterns

- Using this when the app has a public API, IPC, or database you could read instead.
- Re-scanning instead of re-reading at steps ≥ 2.
- Picking state samples by typing arbitrary strings (triggers ads / recommendations).
- Skipping the verify-the-switch check — you'll chase addresses for states that never happened.

---

Adapted from GenericAgent's `procmem_scanner_sop.md` (WeChat current-chat extraction). Generalized to any self-rendered GUI.
