---
name: hybrid-psd-ecommerce
description: Use when creating editable ecommerce PSD hero images or main product images that combine an AI-generated background, real product cutouts, editable Photoshop text layers, separated UI layers, and preview validation.
---

# Hybrid PSD Ecommerce

Use this skill when a user wants a polished ecommerce main image as a layered PSD, especially when pure image generation looks attractive but the final product, copy, and offer elements must remain editable.

## Core Pattern

1. Generate or choose a visual direction.
2. Create a no-product, no-text background asset in that style.
3. Insert real product cutouts as separate layers.
4. Rebuild copy, badges, benefit cards, and offer areas as editable Photoshop layers.
5. Export a preview PNG.
6. Validate the preview with visual inspection and optional masked checks.

## Workflow

### 1. Confirm Inputs

Collect or infer:

- Product image paths.
- Target canvas size, usually square ecommerce sizes such as `1440x1440`.
- Reference image or style direction.
- Final product name, headline, benefit copy, badges, and offer text.
- Output folder for the PSD and preview PNG.

Prefer transparent PNG product renders. White-background JPGs can be used, but require local background removal and extra shadow/color matching.

### 2. Generate The Background Asset

Use image generation for the background only, not for final product packaging or final text.

Prompt requirements:

- Ask for a background or stage only.
- Explicitly remove product packaging, logos, readable text, icons, badges, and watermarks.
- Preserve the chosen visual direction: lighting, material, composition, depth, color palette, and atmosphere.
- Leave clear open areas for product placement and editable text.

Prompt skeleton:

```text
Create a clean background-only asset for a layered ecommerce PSD workflow.
Use the reference only for style, lighting, composition, material feeling, and atmosphere.
Remove all product packaging, logos, readable text, icons, badges, labels, and watermarks.
Leave open space for real product cutouts, a headline, benefit cards, and an editable offer area.
No letters, no fake text, no brand marks, no watermark.
```

Save the chosen background inside the project workspace. Do not leave a project-bound asset only in a temporary generation folder.

### 3. Build The PSD

Prefer Photoshop automation when available, because it can create real PSD files with editable text layers.

Recommended layer structure:

- `01_background`: full-size AI background.
- `02_product_group`: real product cutouts and product shadows.
- `03_ui_product_name_shape`
- `03_ui_benefit_card_1`
- `03_ui_benefit_card_2`
- `03_ui_benefit_card_3`
- `03_ui_offer_panel`
- `04_logo_or_brand_shapes`
- All final copy as separate Photoshop text layers.

Never merge all editable UI shapes into one flattened layer if the user expects PSD editing.

Use `scripts/make_psd_hybrid_template.py` as a starting template. Patch or configure:

- Background image path.
- Product image paths.
- PSD output path.
- Canvas size.
- Product placement.
- Copy and layer labels.

Important Photoshop placement rules:

- Save generated PNG assets with `dpi=(72, 72)` before placing them into a 72dpi Photoshop document.
- Avoid scaling transparent PNGs by visible bounds only; transparent layers may land at the wrong size.
- Keep product, UI, and text on separate layers whenever possible.

### 4. Product Integration

For white-background product JPGs:

- Remove near-white background locally.
- Preserve product color and packaging detail.
- Add only subtle color wash when it helps match the background lighting.
- Add product shadow as its own layer or as a clearly separable product-group part.
- Keep product perspective and grounding consistent with the background stage.

If the product appears pasted on, adjust in this order:

1. Size and vertical grounding.
2. Shadow opacity and blur.
3. Color wash opacity.
4. Edge alpha blur or despill.

### 5. Text And Copy

Use Photoshop text layers for all final readable copy.

Do not ask the image model to render final text. Generated text is often wrong and not editable.

Keep copy short and ecommerce-specific:

- Brand or logo text.
- Product name.
- Main headline.
- Three short benefit items.
- Offer or usage notes.

### 6. Validation

Export a preview PNG from the PSD.

Use visual inspection first:

- Product is not distorted.
- Product looks grounded in the scene.
- Text is readable and editable in the PSD.
- Benefit cards and offer areas do not cover important background or product details.
- No fake generated text, watermarks, or stray AI artifacts remain.

Optionally run `scripts/validate_hybrid_psd.py` to compare stable background windows and check that expected content regions are occupied. Adjust validation windows for each layout instead of lowering standards blindly.

### 7. Output Hygiene

When the user wants the final deliverable only, keep:

- Final `.psd`
- Final preview `.png`

Before deleting intermediate files, verify the resolved output path is inside the intended workspace output folder.

## Failure Modes

- **Pretty reference, stiff PSD**: too much visual design was rebuilt with code. Use an AI background asset as the base layer.
- **Wrong product size**: check canvas units, PNG DPI, and Photoshop placement behavior.
- **Product looks pasted on**: fix grounding, shadow, and color matching.
- **Text looks correct but is not editable**: ensure it was created as a Photoshop text layer, not rasterized.
- **Validation fails despite a good preview**: check whether validation windows overlap editable or product regions.

