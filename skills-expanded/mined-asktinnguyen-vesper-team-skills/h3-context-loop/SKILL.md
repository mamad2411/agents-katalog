---
name: h3-context-loop
description: Plan, render, review, reroll, resume, and assemble long-form MiniMax H3 videos locally with the installed ComfyUI Contex Loop workflow. Use for 22-frame motion/audio continuation, multi-scene H3 productions, scene-by-scene checkpoints, character-reference consistency, or extending a video beyond H3's single-clip duration.
---

# MiniMax H3 context loop

Use the verified ComfyUI installation at `C:\ComfyUI-H3` and the prepared
workflow `h3_context_loop_reddit_recipe.json`. This workflow carries 22 frames
and matching generated-audio context between scenes, trims the repeated head,
checkpoints every take, and assembles accepted scenes without re-encoding them.

## Prepare a production

1. Read [references/recipe.md](references/recipe.md) before writing a scene plan.
2. Run `python scripts/context_loop_control.py doctor`. Run `repair` only when
   doctor reports a missing or corrupt pinned dependency.
3. Run `python scripts/context_loop_control.py start` and open ComfyUI at
   `http://127.0.0.1:8188` with browser/computer control.
4. Load the prepared workflow from `C:\ComfyUI-H3\user\default\workflows`.
5. Replace the proof reference image and edit the Plan node's `prompt_prefix`
   and ordered `shots`. Preserve the workflow's model and continuation wiring.

Use this plan shape:

```json
{
  "prompt_prefix": ["Shared style and stable subject definitions."],
  "defaults": {"duration_seconds": 15, "steps": 6},
  "shots": [
    {"id": "scene_01", "seed": "123", "prompt": ["Opening scene."]},
    {"id": "scene_02", "seed": "456", "prompt": ["Continue exactly..."]}
  ]
}
```

Keep the tested defaults: 24 fps, 22 video/audio context frames, `video`
encoding, `head` anchoring, crop disabled, generated-audio continuation,
`match_tail=true`, Euler with the simple scheduler, six steps, LightX strength
`0.8`, and Spectrum disabled. Use 960x544 for previews and no more than the
verified native 1344x768 target unless the user explicitly requests an
experimental resolution.

H3 scene lengths must follow the `17k+5` frame lattice. Later scenes deliver
their raw frame count minus the 22-frame repeated head, so an arbitrary requested
total duration may require choosing the nearest native duration or a final
post-process trim.

## Write connected scenes

- Put permanent style, character-sheet definitions, speaker IDs, and reference
  meanings in `prompt_prefix`.
- Start every later scene by restating the preceding terminal pose, action,
  camera path, environment, light, and sound. Hold that live state for roughly
  two seconds before introducing a cut or major change.
- End scenes on a still or slowly moving transition beat unless the production
  is one uninterrupted shot. Leave intentional continuous motion explicitly in
  progress at both sides of the boundary.
- Describe secondary characters fully where they appear and state important
  negatives such as different hair or clothing when character bleed is likely.
- Keep `(S1)`, `(S2)`, and other speaker IDs stable across the full production.
  Follow the native H3 Ref2VA label format described in the recipe reference.

## Render and review

Queue the workflow and monitor it with:

```powershell
python scripts/context_loop_control.py status
python scripts/context_loop_control.py outputs --limit 10
```

Keep Review Gate enabled for production. Approve a good take, reroll its seed,
or edit the scene prompt and retry; accepted and superseded revisions remain in
the run's checkpoint directory. Reuse the same `run_name` to resume, and change
it when starting an independent render. Do not queue unrelated work into the
same ComfyUI instance while a loop is active.

Before approving a continuation, compare the final two seconds of the accepted
previous scene with the first two seconds of the new take. The 22-frame context
and trim make a mechanical handoff, but the scene prompt must still preserve the
terminal pose, action, camera, lighting, ambience, and music to make the seam
believable. Reject or revise a scene whose inherited state drifts before it
enters the new action.

For unattended validation, Review Gate may be disabled temporarily. Re-enable
it before handing a production workflow to the user.

## Recover and deliver

Use Manifest Load and the muted recovery Assemble branch to rebuild an existing
run without sampling its final scene again. Final videos and checkpoints live
under `C:\ComfyUI-H3\output\h3_chains\<run_name>`. Verify the newest MP4 has a
nonzero size and return its absolute path.

On failure, run `python scripts/context_loop_control.py status` and then inspect
`C:\ComfyUI-H3\user\skill-server.log`. Preserve checkpoints and partial videos.
Do not update ComfyUI, model weights, or the pinned context-loop node during a
render.
