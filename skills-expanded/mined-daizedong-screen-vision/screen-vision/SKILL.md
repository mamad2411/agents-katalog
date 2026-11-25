---
name: screen-vision
description: Screenshot and read on-screen UI elements/buttons with pixel coordinates (accessibility tree + OCR); optional click. For desktop/native/game GUIs beyond the browser.
---

# screen-vision

Read structured UIA data first and use OCR for uncovered text. Incomplete
accessibility trees remain a limitation; actions require fresh, verified UIA
identity. See [PHILOSOPHY.md](../../PHILOSOPHY.md).

## When to use / when to stop

Use this when an agent needs to *see and act on the desktop*, capture the screen, get a structured
list of buttons/text/inputs with **physical-pixel** coordinates, optionally click one.

- Native apps, Win32/WinUI, Electron, games, remote-desktop, any non-browser window → **here**.
- A web page's DOM/elements → **route to Playwright** (it reads the live DOM directly; this tool would
  only OCR pixels). "beyond the browser" in the description is the boundary.
- Generating pixel art / editing an image file → not this skill (`pixel-art` / image tools).

## Workflow

1. **Probe once**, `python scripts/probe.py`. It separates installed backends from session readiness;
   unavailable desktop access or unverified physical coordinates disables screen/input capabilities
   and returns a nonzero exit. Unknown GPU queries include a reason instead of claiming absence.
   Monitor enumeration must succeed with usable rectangles; no guessed monitor or whole-desktop
   substitution may satisfy a narrow target. Non-Windows geometry comes from the capture backend.
2. **Capture (read-only, the default)**, `python scripts/capture.py --target ...`. Writes
   `screen.png`, an optional Set-of-Mark `annotated.png`, `elements.json` (full), and `capture.json`, and prints a
   compact JSON summary + artifact paths to stdout. Read the summary to pick an element by **id**.
3. **Decide from JSON, confirm layout from the annotated PNG**, the JSON carries `center`, `rect`,
   `label`, `clickable`, `patterns`, `source`. Read the JSON to save tokens; only `Read` the annotated
   image when you need to eyeball the layout.
4. **Click (opt-in)**, `python scripts/click.py --elements-json <path> --id <N>`. **Dry-run by
   default** (reports what it *would* click). Add `--confirm` to actuate; it prefers a coordinate-free
   UIA `Invoke`/`Toggle`/`Select`/`Expand`. A physical fallback requires the same verified UIA identity
   and a matching current hit test. Failed identity checks never authorize a fallback.

```bash
python scripts/capture.py --target 'window:Calculator' --layers uia,ocr --clickable-only
python scripts/click.py   --elements-json <path> --id 30            # dry-run preview
python scripts/click.py   --elements-json <path> --id 30 --confirm  # actuate (Invoke)
```

The [CLI and element schema](reference/schema.md) defines output and action checks.
[Backends](reference/backends.md) covers installation, platforms and DPI.

## Hard rules

1. **Verify effective DPI awareness.** Scripts attempt setup on import and query effective
   awareness before coordinate operations. Capture and actions require verified per-monitor
   awareness; `dpi_awareness_unverified` requires a fresh process with working DPI setup.
2. **Read-only by default; clicking is an explicit, dry-run-first opt-in.** Only login / payment /
   2FA / destructive confirmations go to the human, never auto-click those.
3. **Coordinates are physical pixels** with `{monitor, scale, origin}` metadata. Real screen point =
   element `center` (already absolute). Multi-monitor origins can be negative.
4. **Pick elements by `id`; let the script resolve the coordinate.** Never have the model emit raw
   x/y, use the Set-of-Mark id and let `click.py` re-resolve via UIA.
5. **Report unavailable observations.** Missing backend, black/occluded capture, locked desktop, Wayland →
   surfaced as a `warnings[]`/error in the JSON, never a confident-but-wrong result.

## Privacy & safety

Screenshots can capture passwords/tokens. Prefer `--target window:...` or `--target region:...` over
full-screen. Invalid narrow targets return an error before capture. Only the explicit
`--allow-full-screen-fallback` flag permits scope expansion; `capture.json` records both scopes.

Set `SCREEN_VISION_CONFIG` to an existing private companion, or
`SCREEN_VISION_DATA_DIR` to its exact `data/` directory. Explicit selection uses
DATA_DIR, CONFIG, then a proven sibling `screen-vision-config`, with no home fallback. Declared
output paths outside this worktree are required before reading pixels. `--out-dir` must select a new direct child of
`data/captures/`. Missing storage or annotation write failures are errors.
[DATA.md](../../DATA.md) defines output admission and
inactive JSON staging recovery. Keep the tool uninitialized until storage is needed.

OCR processes a cropped, masked PNG containing only pixels outside named UIA Text rectangles.
Container names and AutomationIds do not suppress OCR. The intermediate PNG stays beside the
capture in private storage. macOS readiness uses native Screen Recording preflight; Linux still
requires a display session. Native macOS/Linux behavior needs separate live validation.

Actions require a capture younger than 60 seconds and unchanged process creation time, window,
UIA runtime IDs, element properties and geometry. `recapture_required` means inspect the application
and capture again. OCR-only and old unverified records remain readable but cannot authorize actions.
An uncertain dispatch returns `action_outcome_unknown`; check its result before retrying.

## Progressive loading

This `SKILL.md` is the only always-loaded file. Load `reference/schema.md` (CLI + JSON contract) or
`reference/backends.md` (libraries, install, platform caveats) on demand, never both preemptively.
