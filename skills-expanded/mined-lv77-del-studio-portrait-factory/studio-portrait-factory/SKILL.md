---
name: studio-portrait-factory
description: Turn uploaded person, couple, family, child, or pet photos into studio-ready ID photos, memes, wedding portraits, personal branding portraits, artistic portraits, pet portraits, proof sheets, and final collections. Use when a photo studio needs guided product options for background, size, style, format, and quantity plus a confirmation-led workflow for preserving identity, generating finished images, reviewing quality, and packaging delivery.
---

# 百变影像工坊

Run a studio production workflow in which the customer explicitly confirms every stage. Never skip a confirmation gate, combine two gates, or treat silence as approval.

## Start every job

When one or more photos arrive, make the first customer-facing sentence exactly:

> 请问您需要生成什么照片？

Do not analyze, edit, or generate the photo before the customer answers. If the customer has already stated the desired product in the same message, repeat the question as a confirmation, summarize the stated product, and wait.

Accept people and pets. Support ID photos, memes, wedding portraits, personal branding portraits, artistic portraits, pet portraits, or a mixed studio collection.

## Enforce the confirmation gates

At every gate:

1. Present only the information needed for the current decision.
2. Ask one direct confirmation question.
3. Wait for an explicit confirmation such as “确认”“同意”“按这个做”.
4. If the customer requests changes, revise the current stage and ask again.
5. If the customer cancels, stop without proceeding.

Use these mandatory gates in order:

### Gate 1 — Intent and authorization

Ask what photos the customer wants. Confirm that the uploader owns the photo or has permission to use it. For a minor, require guardian authorization. Summarize subject type and requested product, then ask: “请确认照片用途和授权信息是否正确？”

### Gate 1A — Product-specific choices

Immediately after the customer names the desired photo type, read `references/selection-options.md` and present a compact set of relevant choices. Do not make the customer invent specifications from scratch. Ask only the fields that apply to the selected product, then wait for the customer to choose and confirm them before assessing or generating the photo.

For every product type, always collect these required fields before asking quantity: visual style, background or scene, framing, aspect ratio or physical size, output pixel preset, and file format. Also ask any product-specific field such as text for memes, wardrobe for wedding portraits, business purpose for branding portraits, or style strength for artistic portraits. Present concrete choices for every field; do not ask only an open-ended “还有什么要求？” question. If the customer says “你推荐”, propose one complete preset and ask for confirmation.

Offer these common digital delivery presets when applicable: square 1:1 at 1024×1024 px, portrait 3:4 at 1536×2048 px, portrait 4:5 at 1638×2048 px, portrait 2:3 at 1365×2048 px, landscape 4:3 at 2048×1536 px, landscape 3:2 at 2048×1365 px, vertical 9:16 at 1152×2048 px, landscape 16:9 at 2048×1152 px, or custom. Offer JPG, PNG, JPG+PNG, and TIFF for print workflows; recommend PNG when transparency is required.

For ID photos, always ask purpose, background color, physical size, file format, and electronic-only versus print layout. Show the common presets with both the Chinese name and exact millimetres. Keep ID-photo sizes separate from photo-paper print sizes. Never present a generic preset as guaranteed valid for a passport, visa, examination, identity card, or other authority; ask for the named use and tell the customer to verify that authority's requirements.

Use this concise customer-facing pattern:

> 好的，请选择证件照规格：  
> 底色：白色、蓝色、红色、浅灰色、透明或自定义；  
> 尺寸：一寸（25×35 mm）、大一寸/小二寸（33×48 mm）、二寸（35×49 mm）、大二寸（35×53 mm）、三寸冲印（63.5×89 mm）、四寸冲印（76×102 mm）、五寸冲印（89×127 mm）或自定义；  
> 用途：日常使用、考试报名、护照/签证、证书档案、相纸冲印或其他。  
> 请回复“底色 + 尺寸 + 用途”。

After receiving the choices, summarize them once and ask: “请确认以上照片规格是否正确？” Do not proceed until confirmed.

For non-ID products, use the same confirmation question after summarizing style, scene, framing, size or ratio, pixels, file format, and product-specific choices. Never begin source-photo assessment, quantity planning, or image generation while any required field is still missing.

### Gate 2 — Source-photo assessment

Assess only visible production qualities: subject count, face visibility, pose coverage, sharpness, lighting, occlusion, and whether more views would improve identity consistency. Do not infer sensitive traits. Read `references/identity-preservation.md`. Present the assessment and ask: “请确认是否使用这些照片作为人物或宠物形象基准？”

### Gate 3 — Package specification

Before discussing or generating any shot, ask exactly: “本次需要生成多少张成片？例如 5 张、6 张或 12 张。” Wait for a positive integer; never assume a default quantity. Clarify that contact sheets and delivery previews do not count as final photos.

Use `direct` production mode by default. In this mode, set `proof_quantity` equal to `final_quantity` internally and do not ask about proofs, selection, watermarks, or additional numbering. Use `proof` mode only when the customer explicitly asks to see extra samples before choosing finals; then ask for `proof_quantity` and require it to be greater than or equal to `final_quantity`.

Read `references/product-catalog.md`. Propose product, style, allocation by category, framing, clothing, background, color, aspect ratio, output size, identity fidelity, and whether text is required. Ensure the category allocation totals exactly `final_quantity`. Offer the V1 25-photo allocation only after the customer has explicitly chosen 25 finals. In `direct` mode, end the summary with: “确认后将立即生成以上数量的无水印正式成品。” Ask: “请确认本次套系规格是否开始制作？” Treat explicit confirmation as authorization to generate the finals immediately.

### Gate 4 — Production after package confirmation

In `direct` mode, do not ask another planning or confirmation question after Gate 3. Briefly acknowledge that production has started, call the image-generation tool in the same turn, and produce exactly `final_quantity` finished, unwatermarked images. Present the actual images before asking for review. Never call these results “小样” or “预览”.

In `proof` mode only, describe exactly `proof_quantity` proof shots grouped by product category. Keep the customer-facing summary concise: use one line per category and never show technical codes such as `ID-01`, `MEME-01`, or `P03`. State the total, then ask: “请确认按以上分类生成共计多少张选片小样？” Generate proofs only after this confirmation.

### Gate 5 — Proof selection

Apply this gate only in `proof` mode. Generate exactly `proof_quantity` watermarked proofs after Gate 4 is confirmed. Present them as a clean grid or gallery without visible code prefixes. Read `references/quality-control.md`, remove obvious failures and replace them so the valid proof count still equals `proof_quantity`. Ask the customer to select exactly `final_quantity` images by directly referencing the thumbnail, visual description, or gallery position; do not print a long numbered list. Do not create finals until the customer explicitly confirms the selected images and the selection count matches `final_quantity`.

### Gate 6 — Final rendering

Apply this gate only in `proof` mode. Summarize the selected images by category or short visual description without exposing internal codes, state the confirmed `final_quantity`, and list final dimensions, retouching level, crop, and color treatment. Ask: “请确认生成以上数量的高清成片？” Generate only after confirmation. In `direct` mode, skip this gate because Gate 3 already authorized final rendering.

### Gate 7 — Final quality review

Inspect finals using `references/quality-control.md`. Report pass items and any proposed rework without displaying internal file codes. Ask: “请确认成片质量，或直接指出需要返修的照片？” Do not package while any requested rework remains unconfirmed.

### Gate 8 — Collection packaging

Propose folder name, included files, contact-sheet layout, watermark policy, and delivery formats. Ask: “请确认按以上方式制作并交付合集？” Package only after confirmation. Present the completed file list and ask one last question: “请确认合集已验收，本次任务是否结束？”

## Generate images

Use an available native image-generation or image-editing tool. Include the uploaded source image in every identity-sensitive generation. Keep the source as an identity reference, not as permission to invent hidden attributes.

Before every image-generation tool call, verify `final_quantity`, the category allocation, and Gate 3 confirmation. In `direct` mode, generate finals immediately after that check. In `proof` mode, also verify `proof_quantity` and Gate 4 confirmation. If any required value is missing or the counts disagree, stop and ask the customer to confirm the quantities.

For each prompt, specify:

- subject identity anchors and features that must remain unchanged;
- product, scene, wardrobe, pose, framing, lens feel, lighting, and color treatment;
- target dimensions and safe crop;
- exclusions for anatomy errors, duplicate subjects, garbled text, warped accessories, and identity drift;
- whether the result is a proof or final.

After generation, use `scripts/format_image.py` to create the confirmed delivery dimensions and file formats. Use pixel dimensions for digital products and millimetres plus DPI for print products. Preserve the original generated file, write converted files into `07-高清成片`, and verify the saved dimensions before claiming delivery. Do not promise exact JPG, PNG, TIFF, pixel, millimetre, or DPI output based only on the generation prompt.

If no image-generation tool is available, prepare prompts and the production plan, explain the limitation, and stop at the current gate.

## Preserve identity and safety

Follow `references/identity-preservation.md` and `references/safety-and-consent.md`. Never promise that an AI-generated ID photo will be accepted by an authority. Keep official-document photos minimally altered and tell the customer to verify local requirements.

## Create and package a job

Use `scripts/create_job.py` immediately after Gate 3 confirmation, passing the production mode and confirmed quantities. Immediately backfill the confirmed decisions from Gates 1–3, including `intent`, `specification`, `source`, `quantity`, and `package`, into the new manifest with `scripts/record_confirmation.py`. Record `final-review` and `packaging` before final delivery; in proof mode also record `proof-plan`, `proof-selection`, and `final-render`. In `direct` mode, generate and present finished images next; do not pause for another text-only step. Use `scripts/build_contact_sheet.py` after Gate 8 confirmation. Use `scripts/validate_delivery.py` before presenting the final collection.

Pass a JSON object containing the confirmed style, background, framing, dimensions, format, color treatment, and category allocation through `create_job.py --spec-file` so the manifest preserves the approved specification. Read `requirements.txt` before running image-processing scripts and install Pillow only if the active Python runtime does not already provide it.

Default output structure:

```text
客户名-日期-套系/
├── 00-封面/
├── 01-证件照/
├── 02-个人形象照/
├── 03-婚纱照/
├── 04-艺术写真/
├── 05-表情包/
├── 06-宠物写真/
├── 07-高清成片/
├── 08-选片合集/
└── job-manifest.json
```

Do not claim completion until validation passes and the customer confirms final acceptance.
