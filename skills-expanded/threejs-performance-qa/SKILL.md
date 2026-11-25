---
name: threejs-performance-qa
description: Verify and optimize Three.js, React Three Fiber, Babylon, and 3D learning labs before shipping. Use for visual QA, blank canvas debugging, WebGL performance, memory cleanup, responsive canvas checks, build/lint verification, Playwright screenshots, canvas pixel checks, GLB asset failures, and release readiness.
---

# Three.js Performance QA

A 3D lab is not complete when TypeScript passes. It is complete when the learner can see, manipulate, reset, and understand it on the target viewport.

## Checks

1. Build/lint with the repo's scripts.
2. Run static Three.js checks on changed scene files.
3. Start the app and inspect desktop and mobile.
4. Check console errors, asset 404s, nonblank canvas, camera framing, controls, reset, and performance.
5. Run `$visual-lab-qa-agent` end pass for new or visually revised demos.
6. Run `$learning-lab-qa-pm-reviewer` for non-trivial 3D learning labs before claiming done.
7. Report skipped visual checks explicitly.

## Project Defaults

```bash
npm --prefix services/frontend run build
npm --prefix services/frontend run lint
```

Run the plugin static check from a target repo:

```bash
node <sibling-threejs-lab-skill>/scripts/check-threejs-lab.mjs <changed-scene-file.tsx>
```

## Budgets

- Pixel ratio cap: 1.5 for dense lab pages, 2 max for showcase scenes.
- First visible lab frame: under 2 seconds on dev machine.
- Repeated markers/particles: use instancing or pooled objects.
- Dispose everything on unmount.
- No mobile panel overlap that hides the main phenomenon.
- Local loaded code/assets: under 512 KB for dependency-light examples unless the lab has a justified asset.
- Largest curriculum GLB/model: under 3 MB; review and compress anything above 5 MB.
- Loaded texture assets: under 4 MB total for a lab page.
- Dense lab geometry: keep under 60k render triangles unless benchmark evidence justifies more.

## Output Contract

When benchmark tooling exists, report these numbers instead of only saying `PASS`:

- FPS average and p95 frame time.
- Draw calls, triangles, geometries, renderer texture count, points/lines when relevant.
- Loaded local code/assets KB.
- Largest loaded model MB and total loaded texture MB.
- Desktop/mobile screenshot paths.
- State mutation/reset result.
- Panel bounds, touch-target, and text-overflow result for FE-heavy labs.
- Any budget exception and why the visual or science fidelity justifies it.

## References

Read `references/qa-checklist.md` for browser triage, asset QA, and release criteria.
