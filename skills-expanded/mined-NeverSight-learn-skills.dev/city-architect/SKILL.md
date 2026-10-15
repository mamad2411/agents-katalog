---
name: city-architect
description: Use when the user wants to generate high-fidelity AI prompts for CITYSCAPES, ARCHITECTURE, or URBAN VISUALIZATION (posters, miniatures, time-lapses).
---

# City Architect (v2.1 - The Robust Visionary)

## Overview
This skill acts as a **Specialized Prompt Engineer** for city and architectural visualization. It translates vague city requests (e.g., "Shanghai poster", "Tokyo in a bottle") into **commercial-grade Midjourney/Flux prompts** using specific templates like Time-Flow, Floating Islands, or Master Posters.

## 📂 File Map
*   **SKILL.md** (This file)
*   `styles/visual-styles.md` (Rendering Modes: Cinematic, Lego, Paper, etc.)
*   `engine/city-mixer.md` (Randomization: Weather, Camera, Conflict Resolution)
*   `engine/urban-innovation.md` (Creativity: Transforming landmarks into concepts)
*   `templates/` (Layouts: Time-Flow, Poster, Floating Island, Silk Ribbon, Capsule, Bookmark)

## Architecture & Data Sources (MANDATORY READ)
You **MUST** read these files to execute the skill logic. Do not guess.

1.  **The Styles**: `styles/visual-styles.md`
2.  **The Engine**: `engine/city-mixer.md` & `engine/urban-innovation.md`
3.  **The Templates**: Select dynamically from `templates/*.md`

## The Workflow (Strict Execution Path)

1.  **Analyze Intent & Route**:
    *   "Passage of time" / "Day to night" / "Seasons"? -> `templates/time-flow.md`
    *   "Poster" / "Artistic" / "Graphic Design"? -> `templates/poster-master.md`
    *   "Floating" / "Island" / "Sky"? -> `templates/floating-island.md`
    *   "Ribbon" / "Fabric" / "Silk"? -> `templates/silk-ribbon.md`
    *   "Bottle" / "Capsule" / "Miniature"? -> `templates/crystal-capsule.md`
    *   "Bookmark" / "Souvenir"? -> `templates/bookmark-set.md`
    *   *Default Fallback*: `templates/poster-master.md`

2.  **Select Visual Style**:
    *   **Action**: Read `styles/visual-styles.md`.
    *   **Logic**: Match user vibe (e.g., "Lego", "Realism") to a Style ID.
    *   **Fallback**: If undefined, use `cinematic-realism` for Time-Flow/Capsule, or `oil-painting` for Posters.

3.  **Roll the Dice (Mixer)**:
    *   **Action**: Read `engine/city-mixer.md`.
    *   **Logic**: Randomly select ONE `Weather` and ONE `Camera Angle`.
    *   **Conflict Check**: Apply "Conflict Resolution" rules (e.g., No rain on paper).
    *   **Vibe Check**: Apply "Vibe Protection Protocol" (e.g., No Neon for Historical).

4.  **Inject Innovation**:
    *   **Action**: Read `engine/urban-innovation.md`.
    *   **Logic**: Apply a "Twist" (e.g., Solar Punk, Cyber Noir) if the user asks for "creative", "future", or "magic".
    *   **Unknown City Logic**: If the city is unknown/fictional (e.g., Wakanda), follow the "Unknown City Fallback" rules in `urban-innovation.md`.

5.  **Generate Output**:
    *   **Action**: Fill the selected template with the City Name, Landmarks, Style/Mixer parameters, and Innovation concept.
    *   **Landmark Inference**: If specific landmarks are not provided for an obscure city, you **MUST perform a Web Search** to identify 3 iconic landmarks before generating the prompt.

## Output Format

Return the result in a code block.

```markdown
**🏙️ City Architect: Generated Prompt**

> **Template**: [Selected Template Name]
> **City**: [City Name]
> **Style**: [Visual Style] + [Weather] + [Camera]
> **Innovation**: [Concept from urban-innovation.md, if applied]

```plaintext
[Insert Content from Selected Template, filled with generated values]
```
```

## Anti-Patterns
- **Do not** use generic prompts. Always route to a specific template.
- **Do not** invent landmarks if you don't know them. **Search first.**
- **Do not** ignore physical conflicts (e.g., rain inside a sealed capsule).
- **Do not** apply Cyberpunk styles to Historical requests.
