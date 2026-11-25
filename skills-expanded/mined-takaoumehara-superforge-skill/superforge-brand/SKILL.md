---
name: superforge-brand
description: >
  Define brand identity systems (naming, tone, visual tokens, VVA Matrix coordinates)
  and produce AI-generated visual and motion assets through prompt engineering
  for generate_image, Kie.ai, and Higgsfield — with the generation cost, the
  consistency recipe that makes a twelfth image match the first, and commercial
  provenance tracked. Also covers case study write-ups for shipped work.
  Use when the user says "brand", "logo", "identity", "tone of voice", "hero
  image", "banner", "generate an image", "video concept", "moodboard", "VVA matrix",
  "case study", "代名詞", "ブランド", "ロゴ", "トンマナ", "世界観", "ビジュアル",
  "画像を作って", "動画", "生成コスト", "商用利用", "実績紹介", or runs /superforge-brand.
license: MIT
metadata:
  author: Takao Umehara
  version: "3.5"
compatibility: >
  Standalone.
  Reads docs/product-idea.md when present, writes docs/brand.md.
---

# Superforge Brand — Brand Identity & VVA Media Engine

Use this skill whenever crafting brand guidelines, visual identity systems, or generating AI media assets (images, graphics, motion video prompts) for web, mobile, or marketing products.

---

## 1. Superforge VVA Matrix (Visual & Verbal Axis)

Establish explicit coordinate tokens before generating assets or UI components (see `references/vva-matrix.md`):

1. **Tone Register (TR)**: `TR-1 Monolithic Restrained` | `TR-2 Conversational Direct` | `TR-3 Playful Inventive` | `TR-4 Provocative Sharp`
2. **Visual Purity (VD)**: `VD-1 Monolithic Minimalist` | `VD-2 Engineered Precision` | `VD-3 Organic Vibrant` | `VD-4 Maximalist Expressive`
3. **User Stance (UA)**: `UA-1 Oracular Authority` | `UA-2 Co-Builder Peer` | `UA-3 Empathetic Guide` | `UA-4 Provocateur Coach`
4. **Sensory Tempo (ST)**: `ST-1 Static Calm` | `ST-2 Subtle Micro` | `ST-3 Rhythmic Fluid` | `ST-4 Cinematic Immersive`

---

## 2. Color & Typography Architecture

- **Adjectives**: 3 core personality adjectives derived from VVA coordinates.
- **Color Architecture**:
  - Primary Accent (High energy, distinctive)
  - Surface Backgrounds (Deep neutral slate, obsidian, or crisp light)
  - Functional Tokens (Success green, Alert amber, Error crimson)
- **Typography Matrix**: Display font (bold, expressive) + Body font (clean, legible).

---

## 3. AI Image Production (`generate_image` & Kie.ai Prompt Engineering)

When generating visual assets for UI heroes, app cards, or marketing banners:
- **No Frame Rule**: Generate ONLY the interface or graphic itself, without surrounding device mockups.
- **Prompt Formula**:
  ```text
  [Subject] + [Art Style / Medium derived from VD coordinate] + [Lighting & Color Palette] + [Composition / Angle] + [VVA Mood]
  ```
- **Execution Checklist**:
  1. Formulate precise, VVA-aligned prompts.
  2. Invoke `generate_image` (or prepare Kie.ai payload).
  3. Verify contrast and visual alignment with brand color tokens.

---

## 4. AI Motion & Video Concept Production (Higgsfield Integration)

When creating motion concepts or AI video generation scripts:
- **Scene Breakdown**: Keyframe prompts, camera trajectory (pan, zoom), motion pacing.
- **Higgsfield Formula**:
  ```text
  Subject action + Camera movement + Lighting transition + Aesthetic style + ST Motion Tempo
  ```

---

## 5. Cost, Consistency & Rights

- **Cost**: Set an iteration budget per asset set before starting. Record generation totals in unit economics.
- **Consistency**: Fix visual parameters in one session; record prompt seeds in `docs/brand.md`.
- **Rights & Provenance**: Audit commercial licensing, likeness, and trademark rules before shipping.

See full model → **`references/media-production.md`**.

---

## 6. Shipped Work Case Studies

Document shipped work with decision rationales and empirical metrics → **`references/case-study.md`**.

---

## Artifact Output

Write `docs/brand.md`:
- VVA Matrix Coordinates
- Three core adjectives & Tone of Voice rules
- Color Architecture & Typography Matrix
- Generated media prompts, seeds, and provenance tables from `references/media-production.md`

Hand color and type tokens to `superforge-ui` (`docs/design.md`).
