---
name: ai3d-gen
description: Use when the user asks for generative 3D assets (text-to-3D, image-to-3D, mesh synthesis) via self-hosted open models. Routes to extensions/comfyui-operator/wrapper.py against a local ComfyUI server, with direct-model fallbacks (TRELLIS, TripoSG, InstantMesh, Hunyuan3D). All free/open weights, no paid SaaS.
---

# AI 3D Generation (self-hosted)

Generate 3D assets locally via open-weight models. Two paths:

1. **ComfyUI-3D-Pack** (primary): visual workflow server.
   Wrapper: `extensions/comfyui-operator/wrapper.py` (stdlib HTTP, no deps).
2. **Direct model CLIs** (fallback / batch): run the model repos' own
   Python entrypoints, no ComfyUI needed.

Output of both paths: meshes (GLB/OBJ/PLY) that feed `operate-blender`
for cleanup, retopo, texturing, render, or `mesh-utils` for inspection.

## Prerequisites

- ComfyUI installed locally (user step): `git clone
  https://github.com/comfyanonymous/ComfyUI && pip install -r
  requirements.txt`, then `python main.py --port 8188`.
- `ComfyUI-3D-Pack` custom node pack for full 3D graph coverage:
  `git clone https://github.com/MrForExample/ComfyUI-3D-Pack
  ComfyUI/custom_nodes/ComfyUI-3D-Pack && pip install -r
  ComfyUI/custom_nodes/ComfyUI-3D-Pack/requirements.txt`
- **3D-Pack requires NVIDIA GPU + CUDA toolkit (nvcc).** It eagerly
  imports `nvdiffrast`, `spconv-cu126`, `nerfacc`, `slangtorch`; no CPU
  wheels exist. On CPU-only machines the whole pack fails import
  (ComfyUI core still runs). Use the direct-model fallback path there.
- GPU strongly recommended for generation speed regardless (models are
  diffusion transformers; CPU inference works but is very slow).

## Wrapper commands

```bash
python extensions/comfyui-operator/wrapper.py status          # health + VRAM
python extensions/comfyui-operator/wrapper.py submit wf.json  # queue job
python extensions/comfyui-operator/wrapper.py history <pid>   # poll status + outputs
python extensions/comfyui-operator/wrapper.py download <pid> --out dir/
python extensions/comfyui-operator/wrapper.py upload img.png  # input asset
```

`submit` requires **API-format JSON** (node-id -> {class_type, inputs}),
the shape produced by ComfyUI's "Save (API Format)". Build it
programmatically or export from the UI once.

`history` returns `files`: flattened output descriptors (filename,
subfolder, type) regardless of which node emitted them. `download`
fetches each via `/view`.

## Model choices (open weights, license-verified in research)

| Model | Input | Quality | License | Where |
|---|---|---|---|---|
| TRELLIS | text/img | high, GLB+texture | MIT | microsoft/TRELLIS |
| TripoSG | img | high mesh quality | MIT | VAST-AI/TripoSG |
| InstantMesh | img | fast | Apache-2.0 | TencentARC/InstantMesh |
| Hunyuan3D-2 | text/img | high + PBR | Tencent permissive | Tencent/Hunyuan3D-2 |
| Stable Fast 3D | img | fastest UV+mat | Stability Community | stabilityai/stable-fast-3d |

Prefer TRELLIS/TripoSG for permissive licensing; Hunyuan3D-2 when PBR
texture quality matters; Stable Fast 3D for speed.

## Intake preflight (photo-sourced pipelines)

Before spending a reconstruction/splat run on user photos:

1. **Provenance**: source images should verify as real captures — run
   `extensions/image-forensics/verdict.py` per image when a camera
   reference exists; synthetic inputs break PRNU assumptions and usually
   produce bad splats.
2. **Photometric QC**: run `extensions/ppisp-prep/photo_qc.py` on the
   set; `correct`/`recapture` verdicts route through the PPISP
   correction pass or a re-shoot before generation.

## Recipes

**image -> textured GLB (ComfyUI path)**
1. `wrapper.py upload photo.png`
2. Build/submit a workflow JSON wiring `LoadImage` -> model node ->
   `SaveMesh`/`Preview3D` (node names per ComfyUI-3D-Pack version; query
   `GET /object_info` for exact class_type names on the live server).
3. `wrapper.py submit wf.json`, poll `history`, `download` outputs.
4. `python extensions/mesh-utils/meshops.py info out.glb` to verify.
5. Import into Blender via `operate-blender` for retopo/material work.

**text -> 3D without ComfyUI (direct)**
- Clone the model repo, `pip install -r requirements.txt`, run its
  inference script. E.g. TRELLIS example script produces GLB directly.
  Then `mesh-utils`/`operate-blender` downstream.

## Boundaries

- Never send user assets to hosted APIs (Meshy, Tripo cloud, etc.) unless
  explicitly asked. The point of this stack is self-hosted.
- ComfyUI not running -> wrapper exits 1 with a start hint. Don't spawn
  the server silently; tell the user.
- Check VRAM in `status` before queueing large models (>=8GB typical).
