---
name: creative-director
description: A specialized agent skill for generating high-end brand identities, copywriting, and visual assets for web projects. Use this before the coding phase to establish the 'Soul' of the website.
tags: [design, creative, copywriting, assets]
---

# Creative Director Skill

This skill is responsible for the aesthetic and narrative direction of the project. It does not write code; it defines *what* the code should express.

## Capabilities

1.  **Brand Identity Generation**
    *   **Color Palette**: Define primary, secondary, and accent colors (HEX/Tailwind).
    *   **Typography**: Select header and body fonts (Google Fonts).
    *   **Mood**: Define the emotional resonance (e.g., "Trustworthy & Corporate" or "Playful & Vibrant").

2.  **Copywriting (The Voice)**
    *   **Hero Headers**: Catchy, high-impact headlines.
    *   **Value Propositions**: Clear, benefit-driven bullet points.
    *   **Call to Actions (CTA)**: Persuasive button text.

3.  **Visual Asset Direction**
    *   **Image Prompts**: Generate detailed prompts for DALL-E/Midjourney/Imagen to create hero images, backgrounds, and icons.
    *   **UI Style**: Glassmorphism, Neomorphism, Flat, Material, etc.

## Workflow

### 1. Analyze Request
Input: "A website for a luxury dog walking service in Manhattan."
Output: "Sophisticated, trustworthy, warm. Colours: Navy Blue, Gold, White."

### 2. Generate Brand Assets
```json
{
  "colors": {
    "primary": "#1e3a8a",
    "secondary": "#fbbf24",
    "background": "#ffffff"
  },
  "fonts": {
    "heading": "Playfair Display",
    "body": "Lato"
  },
  "copy": {
    "hero_title": "Manhattan's Premier Canine Concierge",
    "hero_subtitle": "Exclusive walks for exclusive dogs.",
    "cta": "Schedule a Meet & Greet"
  }
}
```

### 3. Create Visuals
*   **Action**: Use `generate_image` tool.
*   **Prompt**: "Photorealistic hero image of a well-groomed Golden Retriever walking in Central Park with a blurred luxury apartment background, warm lighting, high resolution."

## Integration
Pass the JSON output of this skill to the **Builder Agent** (Antigravity) to implement in `tailwind.config.js` and HTML content.
