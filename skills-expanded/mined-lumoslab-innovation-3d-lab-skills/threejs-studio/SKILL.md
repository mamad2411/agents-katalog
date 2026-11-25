---
name: threejs-studio
description: Create image options, get human approval on localhost, author geometry in Three.js or Blender MCP, then code Three.js motion, contraction and interaction for either model. Use for prompt-to-3D, image-to-model, animated interactive assets or resuming visual approval across coding agents. No paid image-to-3D service.
---

# Three.js Studio

Two geometry engines, one interactive runtime: **Three.js code** or **Blender Python via MCP**,
then **Three.js motion, deformation and interaction** for either result. The coding agent authors
the model from the image; never send it to a paid image-to-3D provider. The studio records human
choices, not automatic approval. A reference image cannot establish exact hidden geometry or physics.

## Start or resume

Resolve `scripts/cli.mjs` relative to this SKILL.md; do not assume a checkout or home path.
If a host returns a `skill://` URI (such as OMP), use the real `filePath`/`baseDir` from its read
result before running Node. Never pass a virtual skill URI as a filesystem path.
Run commands from the user's project, with the same `--dir` throughout.
In a Git project, ensure that session directory is ignored without replacing existing ignore rules.

```sh
node <skill>/scripts/cli.mjs doctor
node <skill>/scripts/cli.mjs init --dir .threejs-studio --prompt "<user brief>" --engine threejs
node <skill>/scripts/cli.mjs serve --dir .threejs-studio --background
node <skill>/scripts/cli.mjs status --dir .threejs-studio
```

If `studio.json` already exists, skip `init` and read `status`. The installer supplies runtime
dependencies; for a raw plugin checkout, run `npm ci --omit=dev` in this skill folder if missing.
`serve` opens the browser automatically; reuse the reported URL, including its assigned port.
Open the URL through the host browser tool too when that helps the user see the studio.
If browser auto-open is unavailable, return the live URL. Never claim it opened unless it did.

## Follow `nextAction`

1. **generate_images**: read [image-options.md](references/image-options.md). Use the host's image
   tool to make 2–3 genuinely different options unless the user chose a count. Save separate
   PNG/JPEG/WebP files. Existing user images may be registered directly.
   `add-image --file <path> --title "Option A" --provenance "<provider/model or user file>"`.
2. **wait_for_user_image_approval**: keep the studio open and call `status --wait 55`. Continue
   other independent task work while waiting; if the user is away, hand back the live URL and
   resume on their next message. Do not click approval on their behalf, synthesize an approval,
   edit the journal to bypass it, or begin the model before this gate. A QA fixture is separate
   and must never be presented as a user-approved design.
3. **build_model**: read the chosen image from `imageApproval` and the latest feedback.
   Read [reconstruction.md](references/reconstruction.md), then only the selected engine:
   [threejs.md](references/threejs.md) or [blender.md](references/blender.md). Register each version
   with `add-model --file <model.ts|model.glb> --title "Option A" --reference <imageApproval.sha256>`.
   Both engines must follow [motion-interaction.md](references/motion-interaction.md).
   For Blender, require `--behavior <behavior.ts>` and include `--blend <asset.blend>` when
   exported. The GLB and its Three.js behavior are reviewed together. Do not silently switch engines.
4. **wait_for_user_model_approval**: inspect the live model, front/side/back views, keyboard,
   resize and console errors; compare silhouette, structure and materials against the reference.
   Exercise the requested motion/deformation, parameter changes, picking, pause and reset.
   Camera orbit and whole-object spinning alone do not satisfy an interactive-model request.
   Use feedback to correct the current source, then add a new snapshot. The requester approves
   the model in the browser; agent QA scores do not constitute that approval.
5. **deliver**: report the approved candidate's source/asset paths and reference hash, any
   accepted approximations, and the studio URL. Integrate into the target project only if asked.

`--dir` is accepted by every command. Call `status` after a user decision or context reset.
Image/model IDs and hashes bind the selected design to the emitted artifact. New reference or
revision rounds invalidate previous approval; old files stay available as history.

## Scope and quality

- When asked to extend a README or gallery, preserve existing content/images rather than
  removing or collapsing them. Inventory the requested model
  collection before choosing a subset; record included/excluded models and reasons. A few convenient
  examples do not satisfy a request for most of an existing collection.

- Start with the user's purpose, silhouette, scale, key details and intended camera. Use only
  relevant siblings from `../threejs-skill-router/SKILL.md` for advanced graphics.
- The existing lab/science/physics skills apply when the task is educational; ordinary asset
  work does not need curriculum text, artificial metrics or a mandatory subagent swarm.
- Never replace generated images with CSS/SVG mock art while calling them image-tool results.
  If the host lacks an image tool, ask for a reference image or help configure its existing tool.
  Do not call a separate paid API or bypass the image approval gate.
- Blender MCP is optional for Three.js. If Blender is unavailable, keep the approved image
  and explain the exact setup step; do not emit a dummy GLB or call a different paid service.
- Do not copy credentials into HTML, prompts, model source, `studio.json` or Git. Model preview
  scripts are isolated from review controls, but only run code belonging to the task.
- Keep UI copy to labels, controls and necessary status. All model options must be real files
  that can be opened; no fake progress, fake approval, or claimed physical accuracy from one image.
