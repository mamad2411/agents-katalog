---
name: ai-cinematic-video-director
description: This skill should be used when the user asks to "generate an AI video prompt", "create a cinematic video prompt", "plan AI video scenes", "build a character sheet for video", "break down a storyboard", "animate an image", "write a video generation prompt", or mentions AI filmmaking, video generation workflows, or character consistency across video clips. Provides structured filmmaking methodology for AI video tools.
---

# AI Cinematic Video Director

## Overview

A structured filmmaking methodology for generating cinematic AI video prompts. Enforces five core rules that prevent the most common mistakes making AI videos look fake. The focus is on thinking like a film director rather than a prompt engineer — controlling composition, continuity, and camera through disciplined workflows.

## When to Use

- Generating prompts for AI video tools (Runway, Kling, Sora, Pika, etc.)
- Planning multi-shot AI video sequences
- Creating character sheets for consistent AI characters
- Breaking scenes into manageable animation clips
- Converting simple animation ideas into detailed directorial prompts

## The Five Core Rules

### Rule 1 — Start Frame First

Never generate video from text alone when realism is required. Text-to-video without a start frame removes control over composition and structure.

**Required workflow:**
1. Generate a high-quality image first
2. Use that image as the **start frame**
3. Animate the image with a structured prompt

```
BAD:  "A man running down a street"

GOOD:
  Start Frame: Photorealistic image of a man running through a quiet city street at sunset
  Animation Prompt: The man continues running past the camera as the camera slowly tracks beside him
```

### Rule 2 — Production Quality Images Only

Bad images create bad animation. AI video inherits every artifact from the start frame — blurry faces, plastic skin, distorted anatomy. If the image is flawed, the video stays flawed.

**Always specify in image prompts:**
- Lighting conditions
- Composition and camera framing
- Clothing and environment details
- Mood and atmosphere
- Skin texture and material realism

```
Photorealistic skateboarder in a city park, golden hour lighting,
35mm lens, natural skin texture, high detail, film still composition
```

### Rule 3 — Structured Prompting

Direct the AI like a film director. Every animation prompt must define six elements:

| Element | Description |
|---------|-------------|
| **WHO** | Subject identity and appearance |
| **WHERE** | Location and environment |
| **WHAT ACTION** | Specific movement or behavior |
| **CAMERA** | Movement type, lens, angle |
| **MOOD** | Tone, atmosphere, color grade |
| **PACING** | Speed, rhythm of action |

```
Subject:  A young man skateboarding
Location: Urban park with concrete ramps
Action:   Performs a kickflip then continues skating forward
Camera:   Handheld camera tracking beside him
Mood:     Energetic, cinematic realism
Pacing:   Medium speed, slight slow-motion on trick
```

### Rule 4 — Character Consistency

Characters changing appearance between shots breaks realism instantly.

**Create a Character Sheet:**

Generate multiple angles of the character:
- Front view, side view, back view, three-quarter view

Store fixed attributes:
- Hair color, eye color, face shape
- Clothing, height, build
- Distinct features (scars, tattoos, accessories)

Reuse the same reference images across all scenes in the sequence.

### Rule 5 — One Action Per Scene

Overloading scenes causes AI failures. Keep each clip focused on a single action.

```
BAD:  "earthquake, explosions, emotional dialogue, collapsing buildings"

GOOD:
  Scene 1 — Wide shot of explosion
  Scene 2 — Medium shot of shaking building
  Scene 3 — Close-up dialogue reaction
```

Edit clips together in post-production to build complexity.

## Output Format

When generating AI video prompts, always return all five sections:

```
## Start Frame Prompt
[Detailed image generation prompt with lighting, composition, lens]

## Animation Prompt
[Specific action, movement, and behavior description]

## Camera Settings
[Movement type, lens, angle, shake level]

## Scene Structure
[Numbered scene breakdown with shot types]

## Editing Notes
[Speed ramps, cuts, transitions, audio cues]
```

### Example Output

**Start Frame Prompt:**
Photorealistic young man skateboarding in an urban park, golden hour lighting, cinematic composition, 35mm lens, shallow depth of field.

**Animation Prompt:**
The skateboarder performs a kickflip and continues skating past the camera while the camera tracks beside him with subtle handheld motion.

**Camera:**
Handheld tracking shot, 35mm lens, slight camera shake, eye-level angle.

**Scene Structure:**
1. Establishing wide shot — park environment
2. Tracking action shot — kickflip sequence
3. Slow motion close-up — landing detail

**Editing Notes:**
Speed ramp during the trick. Cut to close-up on landing. Ambient park audio with emphasized board sounds.

## Behavior

When this skill is active, operate as:
- An **AI filmmaking director** controlling composition and continuity
- A **prompt engineer** structuring outputs for maximum tool compatibility
- A **cinematography advisor** selecting lenses, angles, and camera movement

The goal is to maximize **realism, control, and consistency** in AI-generated video.

## Advanced Techniques

For LLM prompt expansion, motion control workflows, and the slow-motion trick, consult **`references/advanced-techniques.md`**.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Text-to-video with no start frame | Always generate image first, then animate |
| Low-quality or distorted start image | Specify lighting, lens, texture in image prompt |
| Vague animation prompts ("cool cinematic shot") | Use the six-element structure (WHO/WHERE/ACTION/CAMERA/MOOD/PACING) |
| Character appearance changes between shots | Create and reuse a Character Sheet |
| Too many actions in one clip | One action per scene, edit together in post |
| Fast actions causing morph artifacts | Generate in slow motion, speed up in editing |
