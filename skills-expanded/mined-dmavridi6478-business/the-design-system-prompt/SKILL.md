---
name: the-design-system-prompt
description: "Generate cinematic, video-like presentations"
---

Role: You are a Lead UI/UX Designer and Creative Technologist specializing in premium, high-impact digital storytelling.
Task: Create the HTML, CSS, and minimal JavaScript required for a multi-slide presentation deck using a modern, minimalist framework (like Reveal.js or a custom flex-based layout).
Core Visual Requirements:
●	Atmospheric Lighting: Utilize a "Soft-Focus" aesthetic. Use a dark-mode base with deep, muted charcoal backgrounds (#0f0f0f). Incorporate subtle, non-distracting ambient light glows (radial gradients) behind key content containers to create depth without visual noise.
●	Color Palette: Use a "Monochromatic + One" system. Neutral grays and whites for typography, with a single, high-contrast accent color (e.g., Electric Indigo #6366f1 or Soft Amber #f59e0b) used exclusively for call-to-actions or focal points.
●	Typographic Hierarchy: Use a clean, sans-serif font family (Inter or Geist). Ensure high legibility with generous line-heights and letter-spacing for headers.
●	Flow & Motion: Implement "Smooth-Slide" transitions with cubic-bezier(0.4, 0, 0.2, 1) easing. Elements should stagger their entry (fade-in + slight Y-axis slide) to guide the audience’s eye naturally.
Technical Requirements:
●	The design must be responsive and centered.
●	Avoid "busy" backgrounds. Use noise textures or low-opacity mesh gradients if necessary, ensuring they do not interfere with text readability.
●	Include a progress indicator that is minimal and discrete (a thin top-line or subtle dot navigation).
●	Ensure the code is modular so I can easily swap in my own text content later.
Why this approach works
●	Cognitive Load Management: By requesting a "Dark Mode" base with a single accent color, you minimize the visual stimulation that leads to audience fatigue.
●	The "Mesh Gradient" Effect: Using subtle radial gradients (radial-gradient) instead of solid blocks provides a professional, "Apple-esque" depth that makes the content feel like it is floating, which keeps the audience focused on the text.
●	Ease of Maintenance: By requesting a modular structure, you ensure that you aren't fighting the code every time you want to edit a slide.
Recommended Tool Stack
If you are building this from scratch to get that "top-class website" feel:
1.	Reveal.js: The gold standard for HTML-based presentations. It handles the "flow" and navigation logic perfectly so you can focus on the CSS.
2.	Tailwind CSS: Use this for the styling prompt above to ensure your spacing and color utility classes are consistent.
3.	Framer Motion: If you want the "smooth flow" (animations) to feel professional and buttery, add this library to your project for element entrance sequences.

## Related skills in this repo

- **premium-html-presentation**: The more complete cinematic-HTML-deck skill in this repo (full QA checklist, MedTech/healthcare accent-color guidance) — prefer that one by default; use this skill only when its specific prompt framing is what's wanted.
- **theme-factory**: Ready-made visual themes as an alternative to building the palette from scratch.

