---
name: cueframe-reference-video
description: Use when recreating a supplied video or matching its motion, camera, typography, transitions, visual identity or audiovisual timing in CueFrame.
---

# CueFrame reference-video reconstruction

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

For a reconstruction, the reference film and full-frame captures are analysis inputs, not finished reconstruction layers; source excerpts remain valid when the user requests an edit or remix.

Treat the supplied film as the acceptance anchor. Reconstruct what it communicates and how its objects move; matching endpoint stills alone does not match a film. Preserve the requested duration, style and intentional holds. Typography, gradients and reconstructed interface artwork are valid when the reference calls for them; do not present reconstructed UI as a capture of a working product.

## Inspect before choosing the technique

Use the current runtime's advertised source and motion-inspection capabilities. An overview finds the phrases; denser samples around a transformation reveal its path, overlap, masking, occlusion and settling. Increase coverage where adjacent observations do not explain the motion. Distinguish a visible cut from an inferred continuous morph.

Before dependent authoring, the receiving author must inspect the actual reference media or delivered frames and relevant consecutive motion. An asset ID, path or prose description alone is not delivery. Recover missing evidence through supported tools; continue independent work while it is unavailable. Reference assets may remain analysis-only and need not appear in the output.

Keep a concise [reference ledger](references/measurement-and-comparison.md) linking observed timing, geometry, type, materials and sound events to evidence. Measure relevant landmarks and projected dimensions before guessing easing or camera behavior. Record unknown assets, fonts and audio separately from observations.

Eve may have no shell or local media access. Use delivered source/motion evidence through available tools; do not assume FFmpeg, downloads or local scripts can run. A capable local host can use FFprobe/FFmpeg for analysis, comparisons and decode checks. These are not substitute renderers for CueFrame. Report missing observation capabilities rather than claiming unseen motion or unheard sound.

For a local file, `bash scripts/motion-grid.sh INPUT OUTPUT_DIR` creates overview/dense grids and TSV indices with actual source frame numbers and presentation timestamps. Optional `--start SEC --duration SEC` selects an interval relative to the first presented frame; `--overview-fps N --dense-fps N` controls sampling. Each requested instant selects the first source frame at or after it, without duplicate frames; read the recorded actual time rather than assuming the requested rate landed exactly. Use a fresh output directory. The script requires FFprobe/FFmpeg and is an optional local observation aid.

## Author, compare and deliver

Choose useful fidelity anchors and prove the difficult motion early through supported component or timeline previews. Use CueFrame tools for saved authoring, previews and rendering. Keep related motion and sound tied to the same timing decisions; preserve editable text and meaningful parameters. Native peers can help when separate authored work is useful, but continuity still needs integrated review. Hand off inspectable reference evidence and, once available, candidate evidence with their identities, timestamps and current findings, and verify that the receiver inspected it; coordinator inspection alone is insufficient. Share existing media even while a render slot is busy. See the [comparison handoff guidance](references/measurement-and-comparison.md#handoff-and-review-continuity).

Compare actual output at the reference's timestamps and inspect the intervening motion. When available, use `compare_frames` on an identified source frame and saved preview artifact; its unaligned pair/overlay exposes layout drift without rendering the composition again. Read the [worked comparison](references/measurement-and-comparison.md) for geometry, intentional retiming and evidence limits. Fix located mismatches in scale, pose, direction, timing, readability or material before decorative polish. A score or successful compile cannot approve a failed reference requirement. Separate measured audio properties from listening and reused audio from new sound design.

For a finished-film request, deliver an actual CueFrame-produced MP4, verify its format/decode and identify remaining fidelity gaps. Do not invent the user's verdict. For a narrow revision, retain approved work and use the scoped preview workflow in `cueframe-compose-loop`; a new full export is only needed for requested final delivery.
