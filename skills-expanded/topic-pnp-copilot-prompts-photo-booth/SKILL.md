---
name: photo-booth
description: Create a photorealistic 3x3 reference-locked couple photo-booth grid with synchronized expressions, poses, and strict visual continuity.
---

# photo-booth

## When to use this skill

- Use when the user wants a photo-booth grid, emotion grid, couple selfie grid, synchronized pose sheet, or multiple portrait variations from reference images.
- Trigger on requests for a 3x3 grid with the same subjects, room, wardrobe, framing, and lighting while expressions or micro-poses change.

## Required inputs

- A primary reference image for the main person.
- An optional reference image for the partner or character.
- The desired partner concept if no partner reference is supplied.
- Any requested wardrobe, backdrop, photographic era, pose list, or mood.

If the primary reference image is missing, ask the user to attach it. Ask one focused question when the partner concept or intended style is unclear.

## Continuity rules

- Preserve the primary person's visible facial structure, skin tone, distinguishing features, eye color, hair color, and other reference-grounded traits.
- Do not identify the real person or infer private attributes.
- Keep both subjects consistent in all nine panels.
- Lock the environment, curtain or backdrop, lighting direction and softness, camera distance, framing, wardrobe, accessories, material textures, and color treatment.
- Allow only facial expressions, small head movements, and couple micro-poses to change.
- Require both subjects to perform the same or mirrored gesture in each panel. For paired actions such as an embrace, require balanced and symmetrical blocking.
- Keep both faces visible. Prevent either subject, hands, clothing, or props from blocking the primary person's face.
- Do not add logos, captions, watermarks, or unrequested objects.

## Default visual treatment

- Photorealistic close-up couple selfie portrait.
- Both subjects shoulder-to-shoulder at the same head height and distance from the camera.
- Soft, bright frontal window light with a mild on-camera flash feel.
- Subtle analog film grain, candid realism, natural skin texture, visible pores, and minimal retouching.
- Tasteful, fully opaque wardrobe with realistic fabric texture.
- Thin white separators between panels.
- Square overall output with nine square cells.

Adapt these defaults to the user's reference and request. Do not force a photographic era, costume, gender presentation, or wardrobe that the user did not request.

## Workflow

### 1. Analyze the references

- Describe each visible subject and the visual traits that must remain stable.
- Identify the backdrop, lighting, camera distance, framing, wardrobe, accessories, palette, and texture.
- If a partner reference is absent, use the requested fictional or generic partner concept without claiming brand ownership or a real identity.

### 2. Define the continuity lock

Create a compact list covering:

- Identity and appearance anchors.
- Wardrobe and accessory anchors.
- Partner design anchors.
- Room and backdrop anchors.
- Lighting, camera, lens, grain, and color anchors.
- Face visibility and pose synchronization constraints.

### 3. Plan nine synchronized panels

Use the user's pose list when supplied. Otherwise use this balanced default progression:

1. Soft smile with mirrored peace signs.
2. Bright smile with symmetrical cheek-to-cheek lean.
3. Warm balanced embrace with both faces visible.
4. Candid laugh with the same lean-in angle.
5. Synchronized blown kiss.
6. Tasteful symmetrical affectionate pose requested by the user.
7. Matching playful expression and hand gesture.
8. Calm editorial stance with mirrored arm position.
9. Confident power-couple pose with equivalent silhouette gestures.

For every panel specify:

- Expression and emotion.
- Synchronized or mirrored gesture.
- Head angle and eye direction.
- Face visibility constraints.
- Any allowed micro-variation from the locked composition.

### 4. Generate the grid

- Always call `image_generation`.
- Request one ultra-detailed 3x3 master image containing all nine panels.
- Provide detailed generation instructions that include the reference lock, partner consistency, environment, lighting, camera distance, wardrobe, texture, synchronized pose rule, panel sequence, separators, square layout, and no-text requirement.
- Require consistent photographic realism and natural sharpness across the entire grid.

### 5. Review before responding

Confirm:

- The same subjects appear in all nine panels.
- Identity, wardrobe, backdrop, lighting, framing, and camera distance remain stable.
- Each panel follows its assigned expression and synchronized pose.
- Faces are recognizable and unobstructed.
- No extra characters, limbs, objects, logos, labels, or text were introduced.

If the generated grid violates continuity, revise the generation instructions and retry once. If the retry fails, explain the specific continuity issue and ask whether the user wants another attempt.

## Output

- Present the single generated 3x3 grid.
- Briefly summarize the locked style and subjects.
- List the nine panel poses in order so the user can request a targeted regeneration.