---
name: image-to-3d
description: Convert a local JPG, PNG, or WebP into Pixal3D GLB/STL files, or directly render an existing STL as a freely rotating 10-second GIF on the local ROCm GPU. Use for image/photo-to-3D, printable mesh, GLB, STL, rotating GIF, or interactive preview requests.
compatibility: Local Pixal3D checkout at /home/chihmin/src/Pixal3D and loopback service on port 7866.
---

# Image to 3D

Use the installed Pixal3D resident service. Neural networks remain GPU-resident; CPU image I/O and mesh export are expected.

## Existing STL to rotating GIF

When the input is already an STL and the user wants an animation, do **not** start or call the Pixal3D generation service. Read the STL directly and render the default 10-second looping orbit GIF:

```bash
./scripts/render_stl_gif.py /absolute/path/model.stl \
  --output /absolute/path/model-rotation.gif
```

Defaults are 10 seconds, 12 fps, 512×512, a full 360° yaw with seeded secondary pitch/roll motion, an infinite loop, and soft multi-directional lighting for even exposure. Optional controls are `--duration`, `--fps`, `--size`, and `--seed`.

STL cannot contain UVs or textures. When `model.stl` has a sibling `model.glb`, the renderer automatically loads the GLB geometry, UVs, and embedded base-color texture while keeping the STL as the user's requested input. Without that sibling GLB, it renders the STL with an evenly lit neutral material and must not claim that a texture was loaded. The ROCm renderer normalizes and centers the mesh for display but does not modify either source file. Return the GIF with `[[image: /absolute/path/model-rotation.gif]]`.

## Auto-render rotating GIF from generated GLB

After running `generate.py`, a **36-frame rotating-view GIF** is automatically produced from the GLB. The script `render_rotation_gif.py` uses trimesh's OpenGL-based viewer under Xvfb to render each frame at 512×512, saving an animated GIF with 50 ms/frame (≈1.8 s at 20 fps), looped.

The GIF path is returned in the JSON output under `rotation_gif`. If rendering fails (non-fatal), the GLB/STL are still returned. Return the GIF with `[[image: /absolute/path/rotation.gif]]` or `[[file: /absolute/path/rotation.gif]]`.

## Image to 3D preconditions

1. Require one local JPG/PNG/WebP path. The service upload limit is 20 MB.
2. Check readiness:
   ```bash
   curl -fsS http://127.0.0.1:7866/config -o /dev/null
   ```
3. If inactive, load and follow the existing `restart-service` skill for Pixal3D startup/health. Do not kill processes, launch a second model copy, or alter unrelated services.
4. Wait for both `GPU_READY` in the unit journal and HTTP readiness. Initialization needs at least 48 GiB available UMA.

## Generate

Run from this skill directory:

```bash
./scripts/generate.py /absolute/path/reference.jpg \
  --seed 42 --size-mm 100 --output-dir /absolute/path/output
```

Only resolution 1024 is validated. The service serializes jobs and rejects a concurrent generation; do not fall back to the standalone CLI while it is active.

The script writes `result.json`, copies `model.glb` and `model.stl` into the requested output directory, **then automatically renders a 36-frame rotating-view GIF** from the GLB. It also builds and publishes a unique mobile-friendly HTML5 preview. The preview includes the normalized original input image for side-by-side reference, plus orbit/zoom, auto-rotation, and a texture toggle. Parse the final JSON output and return:

- `glb` and `stl` with `[[file: /absolute/path]]` markers;
- `rotation_gif` (path to the animated GIF) — return with `[[image: /absolute/path/rotation.gif]]` or `[[file: /absolute/path/rotation.gif]]`;
- the `preview_url` as a clickable link;
- `result.json` only when useful or requested.

Every default upload uses a unique timestamped path and does not overwrite earlier previews. Use `--no-upload` only if the user explicitly requests local-only output or publishing fails and local artifacts must still be retained.

## Expectations and safety

- About **26 seconds** is model/service loading time, not image generation time.
- A generation including GLB/STL export has historically taken roughly **5–6 minutes** on this host; do not promise a fixed duration.
- `PIXAL3D_DIRECT_DEVICE_LOAD=1` reduces startup overhead. It is not physical UMA zero-copy and does not prove faster per-image inference.
- Preserve `HIP_LAUNCH_BLOCKING=1`; the asynchronous configuration is not validated stable.
- Do not claim printable success. The STL is scaled to the requested longest dimension but may be non-watertight or have non-manifold geometry, insufficient wall thickness, self-intersections, unsupported islands, or support requirements. Tell the user to inspect/repair and slice it.
- A visually good GLB does not certify the STL.
- Publishing uploads the GLB and viewer to the configured GitHub `TempHtml` repository and exposes them through raw.githack. Do not upload sensitive/private source images or models without user approval; ordinary user-requested preview publishing counts as approval.

For implementation details and measured evidence, read `/home/chihmin/src/Pixal3D/deployment/README.md` and `deployment/TUNING.md`.
