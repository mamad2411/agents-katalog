---
name: home-icon-motion
description: Generate, package, and integrate the polished cinematic Home/house navigation icon motion as standalone HTML/video or as an inline Web Component with React and Vue wrappers. Use when Codex is asked to animate a Home icon, house icon, homepage navigation control, active Home tab, or integrate the established construct-and-illuminate Home treatment into an existing frontend. Do not use for Delete, Search, or other icon meanings.
---

# Home Icon Motion

Create the established Home animation: a flat house constructs into a crisp faux-3D home, illuminates its porthole and side window, emits a short warm beam, then collapses cleanly to rest.

## Choose the task

- For an asset or preview, generate a standalone artifact.
- For an existing frontend, integrate the developer component into the real Home control. Read [references/frontend-project-integration.md](references/frontend-project-integration.md), then read only the detected framework section in [references/framework-adapters.md](references/framework-adapters.md).
- Before changing timing, geometry, layer order, or light behavior, read [references/motion-language.md](references/motion-language.md).
- Before delivering a Web Component or framework wrapper, read [references/developer-integration.md](references/developer-integration.md).
- Reject Delete, Search, and other non-Home semantics as outside this skill's scope.

## Generate a standalone artifact

Always use a new output directory unless the user explicitly authorizes overwriting generated files.

```bash
python3 <skill-dir>/scripts/generate_home_motion.py \
  --label Home \
  --output <new-output-dir>
```

Default output includes `index.html`, `motion-config.json`, `poster.png`, and `motion.mp4`. Request other formats with `--exports mp4,webm,gif,poster`.

Useful controls:

- `--accent`: product accent; do not use it for emitted light.
- `--light`: porthole, side-window, and beam light; preserve `#F3FF0B` unless the user requests another light color.
- `--background`, `--bar`, `--foreground`, `--muted`, `--shadow`: surrounding palette.
- `--duration`: complete timeline in seconds; default 5.
- `--target web-component|react|vue|all`: add a reusable developer package.
- `--element-name`: unique custom-element name; keep `home-icon-motion` unless the application already registers it.

For a full engineering handoff:

```bash
python3 <skill-dir>/scripts/generate_home_motion.py \
  --label Home \
  --accent "#247CFF" \
  --light "#F3FF0B" \
  --target all \
  --exports mp4,webm,poster \
  --output <new-output-dir>
```

## Integrate into a frontend

Inspect before editing:

```bash
python3 <skill-dir>/scripts/prepare_project_integration.py \
  --project <project> \
  --scan-only
```

Generate project-local source and `integration-plan.json`:

```bash
python3 <skill-dir>/scripts/prepare_project_integration.py \
  --project <project> \
  --label Home \
  --accent <project-accent> \
  --light "#F3FF0B"
```

Then patch the actual Home interaction:

1. Preserve the existing button, route/state action, focus behavior, label, and accessible name.
2. Replace only the static Home glyph with the generated project-local wrapper.
3. Keep the host in the original 24–48 px icon slot with `presentation="inline"`.
4. Call `restart()` on every Home activation, including clicks while Home is already active.
5. Never scale, rotate, skew, or move the navigation surface, label, siblings, or control allocation in inline mode.
6. Add `"use client"` only to the smallest Next.js interactive boundary.
7. Run the application's existing build, test, and lint commands from `integration-plan.json`.

## Verify

For standalone output:

1. Inspect `poster.png` and a contact sheet at 8–12 fps.
2. Confirm the flat opening state, aligned construction, complete house, light-on hold, causal light-off, clean collapse, and matching final flat state.
3. Inspect the 26–30% and 72–76% face crossfades frame by frame; reject any single-frame flat/front swap.
4. Use `ffprobe` to confirm dimensions, duration, and frame rate.

For developer output:

1. Run `node --check` on generated JavaScript and import the Web Component in Node to confirm SSR-safe evaluation.
2. Serve `developer/` over localhost.
3. Run:

```bash
node <skill-dir>/scripts/validate_component.mjs \
  --url http://127.0.0.1:4173/ \
  --output <validation-dir>
```

4. Test first click, repeat click, navigation away and back, narrow and wide viewports, and `prefers-reduced-motion: reduce`.
5. Confirm visible response within 250 ms, fixed host bounds, no sibling/layout shift, replay on every activation, and exactly one completion event when looping is disabled.
6. Confirm dense continuity sampling reports no hard opacity cut across construction or collapse.

If Chrome, Playwright, Node, or FFmpeg is unavailable, still deliver the self-contained `index.html` and state exactly which exports or checks could not run.

## Deliver

Link the generated `index.html`, `poster.png`, requested video files, and developer package when present. State duration, frame rate, target, replay trigger, reduced-motion behavior, and verification results.
