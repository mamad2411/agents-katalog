---
name: vis-anime-stylize
description: Transform real human portrait photos into clean Japanese anime-style cel-shaded illustrations with Eastern aesthetic scenic backgrounds. Use when generating anime avatars, stylizing portraits, preserving facial identity across artistic transformations, or compiling Midjourney/SD prompts for anime character art.
---

# Anime Portrait Stylize (Japanese Cel-Shaded Illustration)

Transform real human portrait photos into clean, vibrant Japanese anime-style (cel-shaded) character illustrations while rigorously preserving the original subject's facial identity, hair color, expression, clothing, and composition against an Eastern aesthetic scenic background.

## Core Rules & Constraint Hierarchy (P0 > P1 > P2)

- **P0 (Absolute Inviolable Constraints)**:
  - **Facial Identity Preservation**: Must preserve eye shape, nose bridge/tip contour, lip shape/corner curvature, jawline, and cheekbone proportions.
  - **Composition & Aspect Ratio**: 3:4 aspect ratio. Never crop, move, or rescale the subject.
  - **Eastern Aesthetic Background**: Scenic landscape background (mountains, sakura, clouds, traditional garden) harmonized with the subject without overwhelming it.
- **P1 (Strong Constraints - Executed after P0)**:
  - **Pure Anime Cel-Shading**: Clean line art, flat color fills, distinct cel shadow steps. Strictly NO photorealistic skin texture, oil painting brushwork, or watercolor bleeding.
  - **Color & Clothing Fidelity**: Exact replication of original hair color, eye color, and clothing patterns.
- **P2 (Aesthetic Enhancements - Executed only if P0/P1 pass)**:
  - Polished dynamic highlights, atmospheric lighting, soft windblown hair strands.

---

## 5-Step Transformation Pipeline

```
[1. Input Image QA & Facial Extraction] ➔ [2. Cel-Shade Mapping & Palette Extraction] ➔ [3. Eastern Scenic Design] ➔ [4. Prompt Compilation / Generation] ➔ [5. P0-P2 Quality Verification Gate]
```

### Step 1: Input Image Validation & Feature Extraction
1. Verify single-subject portrait with clear, unobstructed facial features (at least 200x200px facial resolution).
2. Extract key biometric anchors: eye corner angle, eyelid fold, nose width, lip fullness, hair silhouette, and lighting angle.

### Step 2: Anime Line Art & Cel-Shade Mapping
1. Translate facial contours into clean vector-like line art.
2. Formulate 2-to-3 tone cel shading (base tone, mid-shadow tone, edge highlight).
3. Boost color vibrancy while retaining accurate base hair, skin, and wardrobe tones.

### Step 3: Eastern Aesthetic Scenic Background Design
1. Select complementary landscape elements (e.g. dawn clouds, misty mountains, cherry blossoms, courtyard pavilions).
2. Apply cel-shading principles to background elements to ensure total style unity between character and environment.

### Step 4: Prompt Compilation (For Diffusion / Multimodal Gen)
Synthesize detailed positive and negative prompts:
- **Positive Core**: `masterpiece, best quality, clean anime lineart, cel shading, studio anime key visual, exact facial likeness of reference photo, <extracted_hair_color> hair, <extracted_clothing>, beautiful eastern scenic landscape background, soft sunlight, 3:4 aspect ratio`
- **Negative Core**: `photorealistic, 3d render, western comic, oil painting, watercolor, blurry lineart, extra limbs, bad anatomy, deformed eyes, cropped head, noisy background`

### Step 5: Verification & Deliverable Assembly

---

## Deliverable Format

```markdown
# Anime Character Translation Package

## 1. Biometric Feature Mapping
- **Facial Anchors**: <Mapped eye/nose/lip/jaw attributes>
- **Hair & Wardrobe**: <Exact colors and garments extracted>
- **Background Scene**: <Eastern landscape theme selected>

## 2. Image Generation Prompt Specification
- **Engine Target**: Midjourney v6 / Niji 6 / Stable Diffusion XL / Flux Anime
- **Positive Prompt**:
  ```text
  clean anime portrait of a [gender/age], [exact hair color and style], [exact facial expression], wearing [exact clothing details], clean sharp lineart, flat colors, vibrant cel shading, 2D anime style, beautiful eastern mountain and sakura landscape background, harmonious lighting, 3:4 aspect ratio, masterpiece, highly detailed --ar 3:4 --niji 6
  ```
- **Negative Prompt**:
  ```text
  photorealistic, realistic skin pores, 3d cgi, western comic, messy lines, lowres, bad anatomy, deformed face, wrong hair color, cluttered background
  ```

## 3. P0/P1/P2 Quality Gate Audit
- [x] P0: Facial identity preserved & 3:4 framing intact
- [x] P1: Cel-shading style unified across subject and landscape
- [x] P2: Polish highlights and atmospheric rim lighting applied
```

---

## Checkable Completion Criteria

- [ ] P0 anchors held: facial geometry preserved, 3:4 composition uncropped, Eastern scenic background present.
- [ ] P1 fidelity held: pure cel-shading with no photoreal texture; hair, eye, and clothing colors replicated exactly.
- [ ] Delivered prompts (positive and negative) encode the P0/P1 constraints for the target model.
- [ ] Output passed the Step 5 P0-P2 verification gate before delivery.
