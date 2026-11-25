---
name: shots
description: Use when the user wants to feed recently captured Yetda screenshots (saved in ~/Yetda/) into the current coding-agent session (Claude Code, Codex, or any agent with skills). Triggers include "/shots", "캡처한 거 넣어줘", "최근 스샷 넣어", feeding pending screenshots. The Yetda menu bar icon shows how many are pending.
---

# shots — feed pending Yetda captures into the session

Yetda saves each capture as a PNG in `~/Yetda/` and shows the pending
count on its menu bar icon. This skill feeds those captures into the current
session and deletes the ones it feeds. It is fast: only the files you feed are
read — there are no descriptions and no selection step.

## Usage

- `/shots` — feed ALL pending captures in `~/Yetda/`.
- `/shots N` — feed only the N most recent captures.

## Steps

1. List the captures in `~/Yetda/` — files named like
   `2026-06-22-143005-042.png` (older ones lack the `-042` part) — newest
   first. Ignore any other files there, and the `.pending/` folder (captures
   still being scanned).
2. If there are none, tell the user "No captures in ~/Yetda/." and stop.
3. Decide how many to feed: if the user supplied a number N, take the newest N
   (capped at the number available); otherwise take all of them.
4. Read each selected PNG into the conversation. This IS the hand-off — the
   images are now available for the current work.
5. Delete the fed files from `~/Yetda/`.
6. Briefly confirm how many shots were fed and that they were removed (the menu
   bar count will drop accordingly).

## Notes

- Operate ONLY inside `~/Yetda/`. Never read or delete files elsewhere.
- No descriptions, no selection prompt — feeding is by recency/count, which
  keeps it fast.
- Do not put images on the clipboard — reading them into the conversation is the
  hand-off. (For a single shot, Yetda's own auto-paste / ⌘⇧1 cover that.)
