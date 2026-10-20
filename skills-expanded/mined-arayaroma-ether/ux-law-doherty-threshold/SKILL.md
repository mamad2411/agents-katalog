---
name: ux-law-doherty-threshold
description: Use when reviewing perceived performance of an interaction (page load, save action, search, API call) — Doherty Threshold (productivity/engagement rises when system response is under ~400ms; anything slower needs explicit feedback). Triggers on "feels slow", "loading state", "response time", "spinner vs skeleton", "perceived performance".
allowed-tools: Read, Edit, Grep, Glob
---

# Doherty Threshold

Keep system response under ~400ms to preserve flow. When real latency exceeds that, perceived latency still matters more than actual latency — manage it explicitly.

## Rules of thumb
- Under ~100ms: no feedback needed, feels instant.
- 100ms-1s: user notices delay but stays in flow if something acknowledges the action immediately (button press state, optimistic UI update).
- 1s: show a loading indicator. Prefer skeleton screens over spinners for content loads — they reduce perceived wait by previewing layout.
- Multi-second operations: show progress (percentage, steps) rather than an indeterminate spinner; a determinate indicator feels faster even at equal real duration.
- Use optimistic UI (apply the change locally, reconcile with the server after) for actions that rarely fail, to make them feel instant regardless of real network latency.

## Review checklist
1. Is there any interaction with no immediate feedback on click/tap?
2. Are spinners used where a skeleton or optimistic update would read faster?
3. Is real latency ever masked by fake artificial delay ("looks too fast to be real")? — don't add fake delay; only smooth genuinely fast responses if it causes UI flicker.
