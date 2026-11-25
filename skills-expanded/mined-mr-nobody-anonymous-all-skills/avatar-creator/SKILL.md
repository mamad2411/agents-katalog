---
name: avatar-creator
description: Design consistent avatar and asset specifications across required formats and sizes.
category: design
aliases:
- avatar
- profile-image
- icon
- character-design
triggers:
- Create an avatar
- Design a profile image
- Generate character art
- Make an icon
keywords:
- avatar
- profile
- image
- icon
- character
- design
- art
dependencies:
- optional:image-generator
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- avatar-creator
- design
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- avatar
- creator
- design
- icon
- image
- profile
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Avatar Creator

## Purpose
Design consistent avatars and visual assets across multiple formats and sizes.
The skill ensures brand consistency and provides properly sized assets for
different platforms and use cases.

## When to Use
- Creating user profile avatars
- Designing character illustrations
- Generating consistent asset sets
- Updating visual identity materials

## When NOT to Use
- For professional photography or detailed portraits
- When existing brand assets should be used
- For trademarked or copyrighted imagery

## Capabilities
- Avatar design with style consistency
- Multiple format export (PNG, SVG, WebP)
- Size variants (profile, thumbnail, full resolution)
- Color palette adherence
- Background removal
- Batch generation for consistency
- Platform-specific sizing (social media, websites, apps)

## Inputs
- `description` (required) — avatar concept or reference
- `style` (optional) — illustration style (realistic, cartoon, abstract, etc.)
- `palette` (optional) — color constraints
- `formats` (optional) — desired output formats
- `sizes` (optional) — required dimensions

## Workflow
1. **Design** — Create base avatar concept
2. **Generate** — Produce primary avatar image
3. **Export** — Create format variants
4. **Size** — Generate required dimension variants
5. **Package** — Deliver as zip or organized folder
6. **Document** — Provide usage guidelines

## Tools
- Image generation (DALL-E, Stable Diffusion, etc.)
- Image editing (background removal, resizing)

## Examples
**User:** "Create an avatar for my user profile: friendly robot"
**Response:**
```
Design: Friendly robot avatar, blue and white palette, rounded design
Generating base avatar... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%

Exporting variants:
- avatar-full.png (512x512)
- avatar-thumb.png (128x128)  
- avatar-social.png (256x256)
- avatar-bg-removed.png (512x512)

Package: avatar-set-2026-02-09.zip
```

## Safety
- Never generate avatars resembling real people without consent
- Respect intellectual property in reference images
- Ensure consistency for brand applications
- Consider accessibility (color contrast, alt text)

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical design category.
