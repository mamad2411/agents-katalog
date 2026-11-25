---
name: khtn8-biology-lab-creator
description: Build and review KHTN8 biology 3D labs with dense small-detail visuals, organ systems, ecology scenes, measured variables, accessible controls, and stricter frontend/performance benchmarks.
---

# KHTN8 Biology Lab Creator

Use this for KHTN8 biology labs: human body systems, respiration, circulation, excretion, nervous system, skin/temperature regulation, reproduction, populations, ecosystems, food webs, biodiversity, and environment protection.

## Biology Bar

Biology scenes fail when they look like generic blobs. Build a recognizable specimen or system:

- Generate or write a multi-view object reference first: front/side/top/cutaway on a plain background, focused on the organ/system morphology, not a decorative scene.
- Run `$science-model-director` and `$threejs-design-director` before building; do not let detail markers hide bad morphology or illogical annotation copying.
- Run `$threejs-art-director` before visual acceptance; do not pass toy-like organs, flat plant clusters, or weak reference likeness.
- Record each prompt/reference/screenshot/fix round in a visual QA ledger; biology demos cannot pass from memory-only visual judgment.
- Human systems: organ silhouette, tubes/vessels/airways, moving flow markers, measurement readout, and a scale cue.
- Ecology: producers, consumers, decomposers or stressors, visible population groups, arrows/flows, and stability/risk output.
- Cells/tissues: repeated small structures must be instanced or pooled; label only the active structures.
- Keep one primary phenomenon visible within 2 seconds: flow, breathing, pulse, population shift, heat transfer, or signal path.
- Run `$visual-lab-qa-agent` before and after biology demo work; benchmark numbers do not pass a biology lab if the organism/system is not visually recognizable.

## Required State

Every biology lab needs:

- At least 3 controls tied to the model.
- At least 3 measured outputs.
- Reset restoring all biological state.
- A deterministic self-check for the biology formula/model.
- `benchmark.scene.detailMarkers` for small-detail scenes.
- A stated simplification and upgrade path when using a school-level model.

## Stricter FE Benchmark

Before claiming a biology lab is ready:

- Desktop and mobile screenshots from the benchmark run.
- A prompt loop ledger linking 2D reference input to 3D screenshot output and the fix set applied.
- No panel overlap on mobile.
- No text overflow in titles, buttons, readouts, or metric cards.
- Touch targets at least 44 px wide and 28 px tall for panel controls.
- `detailMarkers >= 20` for dense biology scenes.
- Local loaded code/assets under 512 KB unless the model is justified.
- Largest model under 3 MB; total loaded textures under 4 MB.
- Render triangles under 60k unless p95 frame time and mobile layout still pass.

## Solver Choice

- Use formula models for heart output, ventilation, gas exchange, population balance, osmosis, and temperature regulation.
- Use fixed-step models for pulse, breathing, transport, and population animation.
- Use physics engines only for contact/collision lessons; most biology labs do not need them.

## References

Use the shared QA gates too:

- `$learning-lab-3d-creator`
- `$science-model-director`
- `$threejs-design-director`
- `$threejs-art-director`
- `$threejs-model-creator`
- `$threejs-physics-simulation`
- `$threejs-performance-qa`
- `$visual-lab-qa-agent`
- `$learning-lab-qa-pm-reviewer`
