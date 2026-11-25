---
name: product-visualizer
description: Generate precise AI image prompts for six professional product visualization styles. Use when the user runs /anatomy, /billboard, /explodedview, /aerialview, /productad, or /360view — or asks for a product shot in any of these styles. Returns a ready-to-paste prompt optimized for Midjourney, DALL-E 3, Firefly, or Flux.
---

# Product Visualizer — Six Slash-Command Prompt Generator

Six professional product photography and visualization styles, each producing a structured AI image prompt you can paste directly into any image generation tool.

## Commands

### /anatomy
Cross-section cutaway revealing internal components.

**Prompt template:**
```
Detailed anatomical cutaway cross-section of [PRODUCT], studio white background, precise technical illustration style, internal components clearly labeled with thin hairlines, Pantone color-matched materials, photorealistic surfaces, 8K render, product design visualization, isometric-leaning perspective, sharp edges, professional industrial design portfolio quality
```

**Best for:** Tech gadgets, appliances, vehicles, medical devices, watches, speakers.

---

### /billboard
Larger-than-life outdoor billboard advertisement mockup.

**Prompt template:**
```
[PRODUCT] featured in a massive outdoor billboard advertisement, dusk golden-hour city skyline backdrop, dramatic cinematic lighting, bold marketing typography space at top, hyperrealistic product rendering, photorealistic billboard material with slight weathering, ad agency hero shot, wide angle, atmospheric depth, award-winning commercial photography style
```

**Best for:** Consumer goods, beverages, fashion, automotive, lifestyle brands.

---

### /explodedview
Product disassembled into floating parts in perfect order.

**Prompt template:**
```
Technical exploded-view diagram of [PRODUCT], all components separated and floating in perfect assembly sequence on clean white background, thin leader lines connecting each part, numbered components, isometric perspective, precise engineering illustration, Keyshot render quality, soft studio shadows under each part, blueprint-meets-product-photography aesthetic
```

**Best for:** Electronics, furniture, machinery, sneakers, cameras, packaging.

---

### /aerialview
Bird's-eye aerial perspective capturing scale and layout.

**Prompt template:**
```
Dramatic aerial bird's-eye-view photograph of [PRODUCT/SCENE], shot from directly above at 90 degrees, symmetrical composition, vivid colors, long shadows, ultra high detail, shot on Hasselblad drone, golden hour light, architectural photography scale, minimal negative space, editorial layout composition
```

**Best for:** Architecture, travel/hospitality, food spreads, fashion flatlay, urban scenes.

---

### /productad
High-impact commercial product advertisement hero shot.

**Prompt template:**
```
Premium advertising hero shot of [PRODUCT], dramatic studio lighting with colored gels, product on [surface material: glass/marble/obsidian/water], atmospheric smoke or mist, cinematic color grade, shallow depth of field, product label/logo perfectly legible, Apple-level product photography quality, 8K, commercial advertisement ready, typographic space reserved at [top/bottom]
```

**Best for:** Any consumer product — beverages, cosmetics, tech, food, fragrance.

---

### /360view
Seamless 360-degree showcase from every angle.

**Prompt template:**
```
Professional 360-degree turntable product photography composite of [PRODUCT], 8 views arranged in two rows (front, 45°, side, 135°, back, 225°, side, 315°), pure white seamless background, consistent studio three-point lighting, perfect shadows, photorealistic render, e-commerce ready, each angle sharply defined, product catalog quality
```

**Best for:** Fashion, footwear, electronics, watches, bags, vehicles.

---

## Usage

1. User types `/anatomy [product name]` (or any command + product)
2. Fill `[PRODUCT]` placeholder with the specific product
3. Optionally add: brand colors, material finishes, mood, target platform (Midjourney/DALL-E/Firefly)
4. Output the completed prompt ready to copy-paste

## Tips

- Midjourney: append `--ar 4:5 --v 6.1 --style raw` for commercial quality
- DALL-E 3: prompts work as-is
- Firefly: add `"generative fill, Adobe Firefly"` to the end
- For real products, add specific color/material: `"matte black aluminum chassis"`, `"frosted glass with gold trim"`
