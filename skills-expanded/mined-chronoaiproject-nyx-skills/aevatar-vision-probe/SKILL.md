---
name: aevatar-vision-probe
version: "1.0"
description: Verify the read-image (vision) path end to end — the user sends an image plus the trigger, a workflow vision step describes it, and the run output proves the model actually saw the image (a real description, not "no image received"). Run it before any image-dependent workflow (petty-cash receipt, invoice OCR).
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - vision
    - read-image
    - workflow
    - diagnostics
---

# Aevatar Vision Probe

Use this to confirm an attached image actually reaches a workflow vision step and the model can see
it. Vision works on the WORKFLOW path (an Image input part is auto-attached to the workflow
llm_call); it does NOT work on the plain chat reply path. So this probe drives a workflow.

**You (the agent) interpret the run output honestly.** The expected pass is a real description of
the image the user sent. "No image received" is a real FAIL signal, not something to paper over —
never invent image content.

## Prerequisite (one-time)

The probe workflow `probe_vision_describe` must be registered in this chat's scope (it ships in the
repo's `workflows/` directory; submit it to your scope if `/workflow run` reports it missing).

## How to run it

1. **Tell the user to send the image and the trigger in ONE message** (desktop Lark: paste the
   image into the input box, then type the command, send together):
   `/workflow run probe_vision_describe`
   (alias `/run-workflow probe_vision_describe`). A pure-text command with no image, or an image in
   a separate message, will not carry the attachment into the run.

2. **Read the run output.** The workflow returns JSON: `{"saw_image": true|false, "description":
   "...", "dominant_colors": "...", "text_in_image": "..."}`.

3. **Verdict:**
   - `saw_image: true` + a description that matches the image the user sent → `VISION OK` — the
     read-image path works and the session LLM route is multimodal. Image-dependent workflows can run.
   - `saw_image: false` / "no image received" → `VISION BLOCKED`. Most likely causes, report which:
     the session LLM route is not multimodal (fix: `PUT /api/user-config` preferredLlmRoute to a
     vision route), or the attachment did not reach the run.
   - `未找到 workflow` / `暂未绑定可运行的 actor` → the probe workflow isn't registered/bound in this
     scope; that's a setup step, quote it.

## Output

One block: did the run start, did the workflow return JSON, what was `saw_image`, and the verdict
above. Quote any error verbatim.

## Guardrails

- Read-only: this probe only describes an image; it never sends, stores, or forwards anything.
- Never claim to have seen image content unless the run output actually returned a description;
  `saw_image: false` is an honest, valid result.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
