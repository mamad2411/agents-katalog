---
name: text-to-avatar
description: Generate a textured 3D GLB avatar from a text prompt or reference image(s). Use when you or the user want an avatar, a 3D character, a person/figure model, or image-to-3D reconstruction of a character. Covers "make me an avatar", "turn this photo into a 3D character", "generate a 3D person". Paid lane ($0.15 USDC via x402).
---

# Text → Avatar

Generate a high-quality textured 3D avatar from a description or one to four reference photos.

## Tool

`text_to_avatar` (three.ws MCP server, `@three-ws/mcp-server`).

- **Lane:** PAID — **$0.15 USDC** per call, settled automatically over x402. Requires a funded wallet on the MCP transport (the `MCP_SVM_PAYMENT_ADDRESS` the plugin wires). If no payment payload is attached, the tool returns a `PaymentRequired` structured result describing what to pay.
- **Backend:** Replicate (Hunyuan-3D 3.1 by default), polled synchronously until a GLB is produced or the timeout fires.

## When to use this vs. the alternatives

- **Free draft, text only:** use `forge-3d` (`forge_free`) — no payment.
- **Static avatar, prompt or photo, best texture:** this skill (`text_to_avatar`).
- **One-call rigged avatar ready to animate:** use `auto-rig` (`forge_avatar`) — it generates *and* rigs in a single call.

## Inputs

| Param | Required | Notes |
| --- | --- | --- |
| `prompt` | one of prompt/images | Natural-language description of the avatar (≤1000 chars). |
| `images` | one of prompt/images | 1–4 reference image URLs. When provided, the model does image-to-3D reconstruction. |
| `texture` | no | Request PBR textures when supported (default `true`). |
| `seed` | no | Integer seed for reproducible output. |

## Outputs

- `glbUrl` — the generated avatar `.glb`.
- the source prompt/images, the picked model version, the Replicate prediction id, and timing metadata.
- Render or share it live with the `avatar` server's inline-render / embed-iframe tools, or open `https://three.ws/viewer?src=<glbUrl>`.

## How to run

1. Decide text vs image mode from the user's request. Gather `prompt` and/or `images` (public http(s) URLs).
2. Call `text_to_avatar`. If it returns `PaymentRequired`, surface the price ($0.15 USDC) and how to fund — do not retry blindly.
3. Return `glbUrl` plus a viewer/embed link. Offer to rig it (`auto-rig` → `rig_mesh`) so it can play the canonical idle/walk animations.

## Notes

- The result is a static mesh. Rigging is a separate step (`rig_mesh`) — or use `forge_avatar` to generate-and-rig in one call.
- The only token this platform uses for payment accounting is `$THREE`; the x402 settlement itself is in USDC.
