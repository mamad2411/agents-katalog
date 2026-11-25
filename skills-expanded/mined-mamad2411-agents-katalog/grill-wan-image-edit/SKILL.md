---
name: grill-wan-image-edit
description: Grill the user one question at a time about edit requirements before editing via wan-image-edit.
disable-model-invocation: true
---

# Grill Wan Image Edit

Interview the user relentlessly about the edit, resolving each requirement one at a time with a recommended default, before handing off to `wan-image-edit`. Nothing gets edited until confirmed.

## Steps

1. **Resolve the source image.** A local file path or an image generated earlier in the session. If none, ask. Complete when a readable image is in hand.

2. **Grill one at a time.** Walk down the decision tree below, one question per turn. For each, state your recommended answer and wait. Skip branches already answered or inferable from the source image — state the inference. Adapt or skip based on the edit.

   - **What changes** — the specific edit instruction.
   - **What stays** — elements, composition, subject identity to preserve.
   - **Style consistency** — match original, or deliberately shift?
   - **Size** — keep source size (default), or resize? Maps to `size`.
   - **Variations** — maps to `n`.
   - **Avoid introducing.**

   After each answer, move to the next unresolved branch. Complete when every relevant branch is resolved (user-given, inferred, or waived).

3. **Confirm.** Restate the edit instruction plus `size`/`n`. If the user requests changes, loop back to step 2 for those branches only. Complete when confirmed.

4. **Hand off.** Follow `../wan-image-edit/SKILL.md` from "Determine parameters" — reuse the source image from step 1, don't re-resolve. Prompt/size/n are settled. Complete when that skill finishes.
