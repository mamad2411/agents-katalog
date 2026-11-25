---
name: ai-poster-workflow
description: reusable workflow for creating cinematic portrait posters, graduation visuals, social media avatars, and prompt-engineering briefs from user-provided themes, portrait references, school information, and style requirements. use when the task involves ai-assisted visual concept design, portrait-preserving poster prompts, iterative image-generation feedback, or structured creative production.
---

# AI Poster Workflow

## Purpose

Use this workflow to turn a user's creative request into a clear, reusable visual-generation brief. The skill focuses on portrait-based posters, graduation commemorative artwork, social media avatars, and cinematic visual concepts.

## Core principles

1. Preserve the subject's identity when a portrait reference is provided.
2. Separate the prompt into clear sections: subject, composition, symbols, style, color, typography, and constraints.
3. Avoid clutter. Select only elements that reinforce the theme.
4. Treat each user revision as design feedback and update the brief precisely.
5. When likeness matters, avoid over-stylization and explicitly keep facial structure, face angle, hairstyle, expression, and clothing cues.

## Standard workflow

1. Collect inputs:
   - portrait or subject description
   - theme
   - school, major, city, or story context
   - preferred style
   - required format
   - text requirements

2. Build a concept:
   - define the central visual metaphor
   - choose 3 to 6 symbolic elements
   - define what should be prominent and what should be subtle

3. Write the prompt:
   - composition first
   - subject and identity constraints second
   - scene elements third
   - style and color fourth
   - typography and negative constraints last

4. Iterate:
   - identify what failed
   - correct only the relevant section
   - keep successful parts stable

## Portrait preservation guidance

When the user wants a result to resemble a real person, include constraints such as:

- keep original face identity
- do not alter facial structure
- preserve face angle, hairstyle, expression, and natural proportions
- use the portrait as the visual base rather than inventing a new face
- avoid generic beauty-face transformation
- avoid excessive smoothing or plastic skin texture

## Output format

Return one of the following depending on the user's need:

- full generation prompt
- short prompt
- revision prompt
- design brief
- checklist for judging the generated result

## Quality checklist

Before finalizing, check:

- Is the subject still recognizable?
- Is the theme clear within three seconds?
- Are there too many unrelated visual elements?
- Is the style consistent?
- Is the typography minimal and appropriate?
- Does the prompt include constraints that prevent common failures?
