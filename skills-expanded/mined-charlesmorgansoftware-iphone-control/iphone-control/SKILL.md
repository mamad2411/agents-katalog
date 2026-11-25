---
name: iphone-control
description: Control a paired iPhone through the macOS iPhone Mirroring app. Use when a user asks to operate a mirrored iPhone, navigate the Home Screen, tap, long-press, swipe, drag icons, use folders, or recover reliable iPhone Mirroring control.
---

# iPhone Control

Control the running iPhone Mirroring app with a short, state-aware action batch. Treat the user’s request as authorization only for the named device changes.

## Fast execution loop

1. Inspect once: run `scripts/iphone-control status` and capture one baseline screenshot with Computer Use.
2. Plan a compact batch: start state, window-local coordinates, actions, checkpoint, and invalidators.
3. Execute deterministic steps without redundant screenshots.
4. Verify only at a page transition, folder opening, layout mutation, external interruption, or batch end.
5. Refresh state and re-plan whenever the checkpoint differs from expectation.

Use only window-local coordinates. `scripts/iphone-control` resolves the iPhone Mirroring window immediately before it acts.

## Choose the control path

Use Computer Use for screenshots, accessibility-tree actions, ordinary taps, text entry, and shortcuts. Use `scripts/iphone-control` when a real press-hold drag, waypoint route, or destination hover is needed.

```bash
scripts/iphone-control status
scripts/iphone-control tap 140 260
scripts/iphone-control swipe left
scripts/iphone-control drag --from 120,300 --via 190,300 --to 250,360
scripts/iphone-control folder-drop --from 120,300 --folder 250,360 --slot 285,405
scripts/iphone-control shortcut home
```

Use `--dry-run --fixture-window 100,80,320,640` to inspect parsing, resolved geometry, and gesture stages without touching the device.

## Coordinate invalidators

Discard the active plan immediately when the phone disconnects, its window moves or resizes, the page changes unexpectedly, a folder closes or opens unexpectedly, icons reflow, the user says stop/pause, or the user moves the pointer. Never resume from stale coordinates.

`stop`, `pause`, and equivalents end the current batch immediately. Do not launch an unavailable synthetic launcher surface or repeat timeouts; use the running iPhone Mirroring app.

## Safety and verification

Apply Computer Use confirmation requirements at action time for deletion, permission changes, communications, purchases, medical actions, account changes, and other protected categories. A request to rearrange icons does not authorize unrelated changes.

After a move, verify both sides: the app is present at the destination and absent from its prior Home Screen position. Opening a folder alone is not proof of membership. Report only confirmed changes, then refresh coordinates after every layout mutation.

## Detailed procedures

- Read [gesture-recipes.md](references/gesture-recipes.md) before a long-press, drag, folder drop, or Home Screen edit sequence.
- Read [recovery.md](references/recovery.md) for `iPhone in Use`, missing Accessibility permission, unexpected page swipes, wrong-folder drops, layout changes, and interruption.

