---
name: mesh-forge
description: Generate a high-fidelity textured 3D GLB from a text prompt, a single reference image, or 2–4 multi-view photos of the same object. Use when you or the user want image-to-3D, multi-view reconstruction, a Granite-directed text-to-3D mesh, or a higher-quality mesh than the free draft lane. Covers "image to 3D", "reconstruct this object", "make a 3D model from these photos". Paid lane ($0.25 USDC via x402).
---

# Mesh Forge — directed text/image/multi-view → 3D

The full-fidelity mesh lane: a chain of specialist models (IBM Granite prompt director → FLUX reference render → Microsoft TRELLIS / Tencent Hunyuan3D reconstruction), or direct reconstruction from your own photos.

## Tool

`mesh_forge` (three.ws MCP server, `@three-ws/mcp-server`).

- **Lane:** PAID — **$0.25 USDC** per call over x402. Returns `PaymentRequired` if no payment payload is attached.
- **Modes:**
  - **Text:** Granite rewrites your prompt into an optimized 3D spec, FLUX renders a reference, TRELLIS/Hunyuan3D build the mesh.
  - **Image:** pass `image_url` to reconstruct a single reference image directly (prompt-director + text-to-image stages skipped).
  - **Multi-view:** pass `image_urls` (1–4 angles, e.g. front/back/left/right) and the backend fuses them — no hallucinated back of the object.

## Inputs

| Param | Required | Notes |
| --- | --- | --- |
| `prompt` | text mode | 3–1000 chars describing one object, e.g. `"a worn leather armchair"`. Optional when an image is supplied (then used as guidance). |
| `image_url` | image mode | http(s) URL to a single reference image. |
| `image_urls` | multi-view | 1–4 http(s) URLs of the same object from different angles. Takes precedence over `image_url`. |
| `direct` | no | Run the Granite prompt-director stage (text mode). Default `true`. |
| `aspect_ratio` | no | Reference image aspect ratio for text mode: `1:1` (default), `4:3`, `3:4`, `16:9`, `9:16`. |

## Outputs

- `glbUrl` — the generated mesh `.glb`.
- `viewerUrl` — `https://three.ws/viewer?src=<glbUrl>`.
- how many views were fused, which backend handled it, the directed prompt (text mode), and timing.

## How to run

1. Choose the mode from the user's input (text / single image / multi-view). Prefer multi-view when several angles of one object are available — it gives the cleanest geometry.
2. Call `mesh_forge`. On `PaymentRequired`, surface the $0.25 USDC price and funding path rather than retrying.
3. Return `glbUrl` + `viewerUrl`. Feed `glbUrl` to `auto-rig` (`rig_mesh`) for an animation-ready model.

## Notes

- For a free, text-only draft, use `forge-3d` (`forge_free`) instead — no payment.
- One object per call. For multi-object placed scenes, use the `scene` server's `compose_scene`.
