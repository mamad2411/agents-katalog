---
name: tinypilot
description: >-
  Control a remote computer using the TinyPilot REST API for keyboard, mouse,
  screenshot, and paste operations. Use when the user mentions "TinyPilot",
  needs remote machine control, or asks for KVM automation.
metadata:
  author: TinyPilot
compatibility:
  network: required — agent must be able to reach TinyPilot host(s) over HTTP/HTTPS
---

# TinyPilot Automation (Cursor)

Requires TinyPilot Pro **3.2.0+**, an Automation License, and an API key from **System → Automation**.

Use the TinyPilot REST API to control remote systems.

## Session setup

1. Confirm TinyPilot URL (default `https://tinypilot.local`).
2. Use an API key from System → Automation (`Authorization: Bearer`).
3. Capture screenshot to verify connection.

## Operational loop

Use **Screenshot → Act → Verify** for every action — no exceptions. One paste OR one keystroke per step; screenshot before and after.

- Prefer keyboard/terminal over mouse/GUI when possible.
- Add delays after actions (1-2s normal, 3-8s app launch).
- Do not commit API keys.
- In PowerShell use `curl.exe` (not `curl`), and write JSON bodies to a temp file (`-d @path`).
- Keep paste payloads short. One command at a time — chaining can cause multi-line input mode.

## ⚠️ Critical: paste timing

**Wait `(100ms × character count) + 1000ms` after paste before sending any keystroke.** The API returns immediately but characters are still being replayed. Sending Enter early splits the command mid-paste. See examples.md for the timing pattern.

## If something isn't working

**Do not retry the same approach.** Take a screenshot, reassess, and try something meaningfully different — a shorter command, a different tool, or mouse/GUI navigation as a fallback.

## Endpoints

- `GET /api/v1/screenshot`
- `POST /api/v1/keystroke`
- `POST /api/v1/mouseEvent`
- `POST /api/v1/paste`
- `GET /state` (unofficial)

## References

- [API reference](references/api-reference.md)
- [Examples](references/examples.md)
