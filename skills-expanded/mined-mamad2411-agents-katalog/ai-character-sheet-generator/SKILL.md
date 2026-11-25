---
name: ai-character-sheet-generator
description: This skill should be used when the user asks to "create a character sheet", "build a character reference", "design a consistent character", "generate character angles", "lock character appearance", or mentions character consistency, multi-angle references, or reusable character designs for AI video or image generation.
---

# AI Character Sheet Generator

## Overview

A structured workflow for creating comprehensive character reference sheets that maintain visual consistency across AI-generated images and video clips. The character sheet locks every visual attribute — face, build, clothing, accessories — so that any future generation of this character matches the original.

Without a locked character sheet, AI tools generate a different-looking person in every frame, destroying continuity instantly.

## When to Use

- Before generating any multi-shot AI video sequence
- When a character must appear consistently across multiple images
- When building a cast for an AI short film or ad
- When establishing a visual identity for a recurring AI character

## Character Sheet Structure

Every character sheet must define three sections: **Identity**, **Visual Attributes**, and **Reference Angles**.

### Section 1 — Identity

```
Name:        [Character name or identifier]
Role:        [Brief narrative role — protagonist, antagonist, bystander]
Age Range:   [Apparent age bracket]
Archetype:   [Visual archetype — corporate exec, street artist, soldier, etc.]
```

### Section 2 — Visual Attributes

Lock every attribute explicitly. Ambiguity causes drift between generations.

| Category | Attributes to Lock |
|----------|-------------------|
| **Face** | Face shape, skin tone, skin texture, eye color, eye shape, eyebrow thickness, nose shape, lip shape, facial hair |
| **Hair** | Color, length, style, texture (straight/curly/wavy), parting direction |
| **Build** | Height impression (tall/average/short), body type, shoulder width, posture |
| **Clothing** | Exact outfit description — fabric, color, fit, layers, accessories |
| **Distinctive** | Scars, tattoos, piercings, glasses, birthmarks, jewelry, watch |
| **Hands** | Ring details, nail style, gloves, visible veins/calluses if relevant |

### Section 3 — Reference Angles

Generate four canonical views using identical prompt attributes:

```
1. FRONT VIEW    — Face-on, neutral expression, arms relaxed at sides
2. SIDE VIEW     — Full profile (left or right), same pose
3. BACK VIEW     — Full rear view showing hair and clothing from behind
4. 3/4 VIEW      — Three-quarter angle, slight turn, most natural pose
```

All four must share: same lighting, same background (neutral gray or white), same clothing, same lens (85mm portrait).

## Image Prompt Template

Use this template for each of the four reference angles:

```
[ANGLE] view of [IDENTITY SUMMARY].
[FACE ATTRIBUTES]. [HAIR ATTRIBUTES]. [BUILD DESCRIPTION].
Wearing [EXACT CLOTHING DESCRIPTION]. [DISTINCTIVE FEATURES].
Neutral gray studio background, soft diffused lighting,
85mm portrait lens, photorealistic, high detail, no motion blur.
```

### Example — Front View

```
Front view of a 30-year-old East Asian man with a sharp jawline.
Warm olive skin with natural texture, dark brown almond-shaped eyes,
thin eyebrows, straight nose, clean-shaven. Black straight hair,
medium length, side-parted left. Athletic build, broad shoulders,
upright posture.
Wearing a fitted dark navy crew-neck sweater over a white t-shirt,
black slim-fit jeans, silver wristwatch on left wrist.
Small scar above right eyebrow.
Neutral gray studio background, soft diffused lighting,
85mm portrait lens, photorealistic, high detail, no motion blur.
```

Repeat for SIDE, BACK, and 3/4 views — changing only the angle line.

## Output Format

When generating a character sheet, always return:

```
## Character Identity
[Name, role, age range, archetype]

## Locked Visual Attributes
[Full attribute table — face, hair, build, clothing, distinctive]

## Reference Angle Prompts
### Front View
[Complete image generation prompt]

### Side View
[Complete image generation prompt]

### Back View
[Complete image generation prompt]

### Three-Quarter View
[Complete image generation prompt]

## Usage Notes
[Tips for maintaining consistency when using this sheet in scenes]
```

## Consistency Rules

1. **Never improvise attributes** — every generation must reference the locked sheet
2. **Same lighting across all angles** — soft diffused, neutral background
3. **Same lens across all angles** — 85mm portrait for consistency
4. **Same clothing in every reference** — outfit changes get a separate sheet variant
5. **Copy attributes verbatim** — when using the character in scene prompts, paste the locked attributes directly rather than paraphrasing

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague face description ("attractive man") | Lock every facial feature explicitly |
| Different clothing between angles | Copy exact clothing string across all four prompts |
| Fancy backgrounds in reference shots | Use neutral gray studio — backgrounds add visual noise |
| Missing distinctive features | Always include scars, tattoos, accessories — they anchor identity |
| Paraphrasing attributes in scene prompts | Copy-paste the locked attribute strings verbatim |
| Forgetting hand details | Rings, watches, gloves are continuity anchors — lock them |

## Integration with Other Skills

This skill feeds directly into **ai-cinematic-video-director** and **ai-storyboard-to-video**:
- Generate the character sheet FIRST
- Reference it in every start frame prompt and animation prompt
- Store as a reusable asset for the entire production

## Additional Resources

For expression variants, wardrobe changes, and multi-character ensemble sheets, consult **`references/advanced-character-design.md`**.
