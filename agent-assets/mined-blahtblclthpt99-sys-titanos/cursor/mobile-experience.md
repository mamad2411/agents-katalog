---
description: TitanOS mobile experience — thumb, driving, offline, GPS/battery
alwaysApply: true
---

# Mobile Experience

Optimize for one-handed use, thumb reach, driving, large controls, minimal typing, offline honesty, fast resume, background strategy, battery, and GPS efficiency.

## Requirements

| Area | Rule |
|---|---|
| Thumb zone | Primary nav + primary CTAs in the bottom third; no page FABs that collide with MobileNav / MobileActionDock |
| Safe areas | `env(safe-area-inset-*)` on fixed chrome; main clears nav + dock (`AppLayout` / `PageShell` / `--mobile-chrome-bottom`) |
| Driving | On live Driver Hub (shift or delivery): one obvious next action ≥48px; hide or demote Create/AI dock; prefer voice + chips over forms |
| Touch | Interactive ≥44×44; `CONTROL.sm` (36px) is desktop-dense only — ban on mobile primary / driving paths |
| Typing | Prefer chips, pickers, OCR, voice, and smart defaults before free-text on field/driver flows |
| Offline | Banner must match reality (shell/PWA cache + local device data — not a full entity sync queue). Tag local writes with `_source` / show `SyncStatus` |
| Resume | Active shift/delivery survives refresh via persisted seed; flush on `pagehide`; restore explorer/session state |
| Background | Web may suspend GNSS when `document.hidden`; native needs an explicit foreground strategy. **Never dual high-accuracy watches** |
| Battery | Visibility clears intervals; one geolocation watch; throttle persistence (time + Δmiles); wake lock only while delivery/shift needs the screen |
| GPS | Prefer DoorDash watch while delivery active; else Hub session. `maximumAge` + distance filter; `suspendHardware` when hidden |

## Overlap

Battery/GPS details also live in `.cursor/rules/performance.mdc`. This rule owns thumb chrome, driving cognitive load, offline honesty, and Capacitor background strategy.

## Definition of done

Incomplete if a driving screen fights the action dock, offline copy overpromises sync, or two GPS watches run at once.
