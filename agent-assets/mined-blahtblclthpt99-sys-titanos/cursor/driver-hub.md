---
description: TitanOS Driver Hub — workflow engine, live pinned, auto analytics
alwaysApply: true
---

# Driver Hub

Convert Driver Hub into a **workflow engine**: live ops pinned, analytics in Explorer folders, automatic trip/delivery/rush/idle/analytics generation.

## Shell

- **Mission Control** is sticky live-only: status, one primary next action (≥48px), essential metrics (miles, idle, rush, GPS).
- **Analytics, history, reports, settings** live only under Explorer folders — never dump charts onto Mission Control.
- Explorer folders declare `group`: `live` | `history` | `analytics` | `reports` | `settings` (IA mirror).

## Workflow engine

- Prefer extending `doorDashWorkflow` + session APIs via `src/lib/driverOs/workflowEngine.js` — do not fork a second state machine per platform.
- Stage transitions emit events; Mission Control reads `buildMissionSnapshot` / `resolveDriverIntent` only.
- One GPS watch: DoorDash active owns GNSS; otherwise Hub session (`gpsOwner`).

## Auto-detect / classify

- Trip detection builds on `stepStopDetection` + journal sync — do not invent a parallel tracker.
- Session/trip auto-start is **opt-in** (`prefs.autoStartOnMotion`); never silent start without user-visible status.
- Delivery classification may auto-suggest order type; always allow manual override; persist `classification` with confidence + source.
- Rush: stamp with `classifyRushWindow`; `detectRushIntensity` is additive (quiet/normal/busy).
- Idle: accumulate via tracker `idleSec` + stop dwell + DoorDash wait timers.

## Analytics

- Generate digests on shift/delivery end (`analyticsDigest.js`); Explorer folders prefer cached digests when fresh.
- Live Shift folder stays operational controls only — history/export belong in History/Reports folders.

## Definition of done

Incomplete if analytics land on Mission Control, Explorer folders lack IA groups, dual GPS watches run, or digests are never written on shift/delivery end.
