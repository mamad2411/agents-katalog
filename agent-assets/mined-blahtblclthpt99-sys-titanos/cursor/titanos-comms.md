---
description: TitanCom — low-latency PTT, reconnect, audio, permissions, notifications
alwaysApply: true
---

# COMMS (TitanCom)

Crew push-to-talk must feel like a radio: fast press-to-audio, survive drops, respect channel access, and notify reliably.

## Requirements

| Area | Rule |
|---|---|
| Low latency | Warm mic (mute/unmute tracks). Keep peer connections across PTT presses; do not reopen `getUserMedia` or tear the mesh every release |
| Reconnect | On `CHANNEL_ERROR` / `TIMED_OUT` / `online` / visible tab: backoff reconnect with honest status (`reconnecting`, not fake “Live”) |
| Background audio | Keep receive path playing when possible; label native background / Bluetooth limits honestly until Capacitor audio session plugins ship |
| Bluetooth | Prefer `audio` constraints that allow BT headsets (`echoCancellation` / NS / AGC on). Do not hard-bind to a device id |
| Channel permissions | Gate Realtime topic join via membership / network channel rules before `subscribe` |
| Voice quality | AEC + noise suppression + AGC; STUN always; TURN from `VITE_TURN_*` when set |
| PTT | Pointer + Space; haptic on press; floor claim with lease/timeout so stuck floors clear |
| Notifications | Channel text → inbox (`messages`) + OS push when permitted; skip self; link to `/comms?channel=` |

## Honesty

- Public `tc-*` radios are open network channels — label them as such  
- Without TURN, some NATs will fail — surface reconnect / “audio may not reach” when ICE fails  
- Background audio on mobile browsers is limited; native keep-alive is best-effort until a plugin owns the session  

## Definition of done

Incomplete if mic opens every press, reconnect is a label with no retry, custom channels join Realtime without membership, or channel messages never notify peers.
